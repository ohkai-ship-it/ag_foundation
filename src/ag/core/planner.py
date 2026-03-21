"""V1Planner — LLM-based skill composition planner (AF0102).

This module implements V1Planner, which uses an LLM to compose execution plans
from the available skill catalog. V1Planner is a pure function — it returns an
in-memory Playbook object with zero disk I/O.

Design Principles:
- Pure function: plan(task) -> Playbook (no side effects)
- Implements Planner Protocol from interfaces.py
- Orchestrator handles param chaining at runtime (no placeholder syntax)
- Graceful degradation on LLM errors

Architecture Position:
- V0Planner: Registry lookup, requires --playbook flag
- V1Planner: LLM composes skill sequence from task description (this module)
- V2Planner: Uses skills AND playbooks as building blocks (future)
- V3Planner: Judges feasibility, identifies capability gaps (future)

Usage:
    from ag.core.planner import V1Planner
    from ag.providers.registry import get_provider
    from ag.skills import get_default_registry

    provider = get_provider(ProviderConfig(provider="openai", model="gpt-4o-mini"))
    registry = get_default_registry()
    planner = V1Planner(provider, registry)

    playbook = planner.plan(task_spec)
"""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, ValidationError

from ag.core.playbook import (
    Budgets,
    Playbook,
    PlaybookStep,
    PlaybookStepType,
    ReasoningMode,
)
from ag.core.task_spec import TaskSpec
from ag.providers.base import ChatMessage, LLMProvider, MessageRole
from ag.skills import SkillRegistry

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Planner Schemas (internal — for LLM response parsing)
# ---------------------------------------------------------------------------


class PlannedStep(BaseModel):
    """A single step in the LLM-generated plan."""

    skill: str = Field(..., description="Skill name from catalog")
    params: dict[str, Any] = Field(default_factory=dict, description="Initial parameters")
    rationale: str = Field(default="", description="Why this step is needed")

    model_config = {"extra": "forbid"}


class LLMPlanResponse(BaseModel):
    """Schema for LLM's JSON response."""

    steps: list[PlannedStep] = Field(..., min_length=1, description="Ordered skill steps")
    estimated_tokens: int = Field(default=0, ge=0, description="Estimated total tokens")
    confidence: float = Field(default=0.5, ge=0.0, le=1.0, description="Plan confidence")
    warnings: list[str] = Field(default_factory=list, description="Any warnings or caveats")

    model_config = {"extra": "ignore"}  # Allow extra fields from LLM


class PlannerError(Exception):
    """Error during plan generation."""

    pass


# ---------------------------------------------------------------------------
# V1Planner Implementation
# ---------------------------------------------------------------------------


class V1Planner:
    """LLM-based planner that composes skill sequences (AF0102).

    Pure function: no disk I/O. Returns in-memory Playbook.
    Implements Planner Protocol: plan(task) -> Playbook
    """

    # Default budgets for generated playbooks
    DEFAULT_MAX_STEPS = 10
    DEFAULT_MAX_TOKENS = 50000
    DEFAULT_TIMEOUT_SECONDS = 300

    def __init__(
        self,
        provider: LLMProvider,
        skill_registry: SkillRegistry,
        *,
        max_steps: int = DEFAULT_MAX_STEPS,
    ) -> None:
        """Initialize V1Planner.

        Args:
            provider: LLM provider for plan generation
            skill_registry: Registry of available skills
            max_steps: Maximum steps allowed in generated plans
        """
        self.provider = provider
        self.skill_registry = skill_registry
        self.max_steps = max_steps

    def plan(self, task: TaskSpec) -> Playbook:
        """Generate execution plan from task and skill catalog.

        Returns Playbook (not ExecutionPlan) to match Planner Protocol.
        The Playbook contains PlaybookSteps with skill_name and parameters.
        Orchestrator handles param chaining at runtime.

        Args:
            task: Validated TaskSpec with prompt and constraints

        Returns:
            Playbook ready for execution by orchestrator

        Raises:
            PlannerError: If plan generation fails (LLM error, invalid response)
        """
        # Step 1: Build skill catalog for LLM context
        catalog = self._get_skill_catalog()
        if not catalog:
            raise PlannerError("No skills available in registry")

        # Step 2: Build prompt
        prompt = self._build_prompt(task, catalog)

        # Step 3: Call LLM
        try:
            response = self.provider.chat(
                messages=[
                    ChatMessage(role=MessageRole.SYSTEM, content=self._get_system_prompt()),
                    ChatMessage(role=MessageRole.USER, content=prompt),
                ],
            )
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise PlannerError(f"LLM call failed: {e}") from e

        # Step 4: Parse and validate response
        try:
            plan_response = self._parse_response(response.content)
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}")
            raise PlannerError(f"Failed to parse LLM response: {e}") from e

        # Step 5: Validate skill references
        self._validate_skills(plan_response)

        # Step 6: Build Playbook from plan
        playbook = self._build_playbook(task, plan_response)

        logger.info(
            f"V1Planner generated plan with {len(playbook.steps)} steps "
            f"(confidence: {plan_response.confidence:.2f})"
        )

        return playbook

    def _get_skill_catalog(self) -> list[dict[str, Any]]:
        """Extract skill metadata for LLM context."""
        catalog = []
        for skill_name in self.skill_registry.list_skills():
            info = self.skill_registry.get_info(skill_name)
            if info:
                # Simplify schema for LLM context (remove verbose JSON Schema metadata)
                catalog.append(
                    {
                        "name": info["name"],
                        "description": info["description"],
                        "requires_llm": info["requires_llm"],
                        "input": self._simplify_schema(info["input_schema"]),
                        "output": self._simplify_schema(info["output_schema"]),
                    }
                )
        return catalog

    def _simplify_schema(self, schema: dict[str, Any]) -> dict[str, Any]:
        """Simplify JSON Schema for LLM context (reduce token usage)."""
        # Extract just the properties and required fields
        simplified = {}
        if "properties" in schema:
            for prop_name, prop_def in schema["properties"].items():
                prop_type = prop_def.get("type", "any")
                prop_desc = prop_def.get("description", "")
                if prop_desc:
                    simplified[prop_name] = f"{prop_type} — {prop_desc}"
                else:
                    simplified[prop_name] = prop_type
        return simplified

    def _get_system_prompt(self) -> str:
        """Return system prompt for planner LLM."""
        return """You are an execution planner for an agent system. Your job is to create
execution plans by composing available skills into a sequence of steps.

Rules:
1. Only use skills from the provided catalog — no hallucinated capabilities
2. Order steps logically — later steps may depend on earlier outputs
3. The runtime automatically chains step outputs (no placeholder syntax needed)
4. Minimize steps while ensuring task completion
5. Provide clear rationale for each step
6. For load_documents: prefer the default patterns (["**/*.md"]) unless the task explicitly requires other file types. Do not invent patterns like *.docx or *.pdf unless the user asks for those formats

Respond with valid JSON matching this schema:
{
  "steps": [
    {"skill": "skill_name", "params": {"key": "value"}, "rationale": "why needed"}
  ],
  "estimated_tokens": 5000,
  "confidence": 0.85,
  "warnings": ["optional warnings"]
}"""

    def _build_prompt(self, task: TaskSpec, catalog: list[dict[str, Any]]) -> str:
        """Build the user prompt for plan generation."""
        # Format skill catalog
        skills_text = []
        for skill in catalog:
            skill_line = f"- **{skill['name']}**: {skill['description']}"
            if skill["input"]:
                inputs = ", ".join(f"{k}: {v}" for k, v in skill["input"].items())
                skill_line += f"\n  Input: {{{inputs}}}"
            if skill["output"]:
                outputs = ", ".join(f"{k}: {v}" for k, v in skill["output"].items())
                skill_line += f"\n  Output: {{{outputs}}}"
            if skill["requires_llm"]:
                skill_line += "\n  [Requires LLM]"
            skills_text.append(skill_line)

        catalog_str = "\n".join(skills_text)

        # Build constraints section
        constraints = []
        if task.budgets.max_steps:
            constraints.append(f"- Maximum {task.budgets.max_steps} steps")
        if task.constraints.allowed_skills:
            constraints.append(f"- Only use: {', '.join(task.constraints.allowed_skills)}")
        if task.constraints.blocked_skills:
            constraints.append(f"- Do not use: {', '.join(task.constraints.blocked_skills)}")

        constraints_str = "\n".join(constraints) if constraints else "None"

        # AF-0106: Detect workspace file types for better pattern generation
        files_hint = self._detect_workspace_files(task.workspace_id)

        return f"""Create an execution plan for this task:

**Task:** {task.prompt}

**Available Skills:**
{catalog_str}
{files_hint}
**Constraints:**
{constraints_str}

**Maximum steps:** {self.max_steps}

Respond with a JSON plan."""

    def _detect_workspace_files(self, workspace_id: str) -> str:
        """Detect file types in workspace inputs (AF-0106).

        Returns a prompt hint string describing available files, or empty string.
        """
        try:
            from ag.config import get_workspace_dir
            from ag.storage import Workspace

            ws = Workspace(workspace_id, get_workspace_dir())
            inputs_dir = ws.inputs_path
            if not inputs_dir.exists():
                return ""

            extensions: set[str] = set()
            for f in inputs_dir.rglob("*"):
                if f.is_file() and f.suffix:
                    extensions.add(f.suffix.lower())

            if not extensions:
                return ""

            ext_list = ", ".join(sorted(extensions))
            return f"\n**Workspace file types:** {ext_list}\n"
        except Exception:
            return ""

    def _parse_response(self, content: str) -> LLMPlanResponse:
        """Parse and validate LLM response as JSON."""
        # Extract JSON from response (handle markdown code blocks)
        json_str = content.strip()
        if json_str.startswith("```"):
            # Remove markdown code block
            lines = json_str.split("\n")
            # Skip first line (```json) and last line (```)
            json_lines = []
            in_block = False
            for line in lines:
                if line.startswith("```") and not in_block:
                    in_block = True
                    continue
                if line.startswith("```") and in_block:
                    break
                if in_block:
                    json_lines.append(line)
            json_str = "\n".join(json_lines)

        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise PlannerError(f"Invalid JSON in LLM response: {e}") from e

        try:
            return LLMPlanResponse.model_validate(data)
        except ValidationError as e:
            raise PlannerError(f"LLM response doesn't match schema: {e}") from e

    def _validate_skills(self, plan: LLMPlanResponse) -> None:
        """Validate that all referenced skills exist."""
        for step in plan.steps:
            if not self.skill_registry.has(step.skill):
                raise PlannerError(
                    f"Invalid skill '{step.skill}' in plan. "
                    f"Available: {', '.join(self.skill_registry.list_skills())}"
                )

    def _build_playbook(self, task: TaskSpec, plan: LLMPlanResponse) -> Playbook:
        """Convert LLM plan response to Playbook."""
        # Generate unique plan name
        plan_id = f"v1plan_{uuid4().hex[:8]}"
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

        # Build PlaybookSteps from LLM response
        steps = []
        for i, planned_step in enumerate(plan.steps):
            step = PlaybookStep(
                step_id=f"step_{i}",
                name=f"{planned_step.skill}_{i}",
                step_type=PlaybookStepType.SKILL,
                skill_name=planned_step.skill,
                description=planned_step.rationale,
                required=True,  # All V1 plan steps are required
                retry_count=1,  # Allow one retry
                parameters=planned_step.params,
            )
            steps.append(step)

        # Build Playbook
        playbook = Playbook(
            playbook_version="0.1",
            name=plan_id,
            version="1.0.0",
            description=f"V1Planner generated plan for: {task.prompt[:100]}",
            reasoning_modes=[ReasoningMode.DIRECT],
            budgets=Budgets(
                max_steps=len(steps) + 2,  # Allow some buffer
                max_tokens=plan.estimated_tokens or self.DEFAULT_MAX_TOKENS,
                max_duration_seconds=self.DEFAULT_TIMEOUT_SECONDS,
            ),
            steps=steps,
            metadata={
                "generated_by": "V1Planner",
                "generated_at": timestamp,
                "confidence": plan.confidence,
                "warnings": plan.warnings,
                "original_task": task.prompt,
            },
        )

        return playbook
