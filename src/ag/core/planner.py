"""V0/V1/V2 Planners — skill and playbook composition (AF-0102, AF-0103).

This module implements:
- V0Planner: Registry lookup, requires --playbook flag
- V1Planner: LLM composes skill sequences from task description
- V2Planner: LLM composes mixed skill+playbook plans (AF-0103)

Architecture Position:
- V0Planner: Registry lookup, requires --playbook flag
- V1Planner: LLM composes skill sequence from task description
- V2Planner: Uses skills AND playbooks as building blocks (this module)
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
import re
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
from ag.playbooks import DEFAULT_V0, get_playbook
from ag.providers.base import ChatMessage, LLMProvider, MessageRole
from ag.skills import SkillRegistry

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Planner Schemas (internal — for LLM response parsing)
# ---------------------------------------------------------------------------


class PlannedStep(BaseModel):
    """A single step in the LLM-generated plan."""

    type: str = Field(default="skill", description="Step type: 'skill' or 'playbook'")
    skill: str | None = Field(default=None, description="Skill name (for type='skill')")
    playbook: str | None = Field(default=None, description="Playbook name (for type='playbook')")
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
# AF-0119: Planning metadata for trace attribution
# ---------------------------------------------------------------------------

from dataclasses import dataclass, field


@dataclass
class PlanningResult:
    """Result from a planner including metadata for trace attribution (AF-0119).

    Wraps the generated Playbook plus timing, token usage, and validation info.
    """

    playbook: Playbook
    planner_name: str
    started_at: datetime
    ended_at: datetime
    duration_ms: int
    # LLM call info (None for static planners like V0Planner)
    model_used: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    # Plan metadata
    confidence: float | None = None
    raw_steps: list[dict[str, Any]] = field(default_factory=list)
    validation_corrections: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# V0 Planner Implementation (extracted from runtime.py, AF-0114)
# ---------------------------------------------------------------------------


class V0Planner:
    """v0 Planner: selects playbook (always default_v0 for now)."""

    def plan(self, task: TaskSpec) -> Playbook:
        """Select playbook for task execution."""
        # v0: Honor preference if valid, otherwise use default
        if task.playbook_preference:
            playbook = get_playbook(task.playbook_preference)
            if playbook:
                return playbook

        return DEFAULT_V0

    def plan_with_metadata(self, task: TaskSpec) -> PlanningResult:
        """Select playbook and return with metadata (AF-0119)."""
        started_at = datetime.now(UTC)
        playbook = self.plan(task)
        ended_at = datetime.now(UTC)
        duration_ms = int((ended_at - started_at).total_seconds() * 1000)

        return PlanningResult(
            playbook=playbook,
            planner_name="V0Planner",
            started_at=started_at,
            ended_at=ended_at,
            duration_ms=duration_ms,
        )


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
        # AF-0119: Track last planning call metadata
        self._last_response: Any = None
        self._last_plan_response: LLMPlanResponse | None = None
        self._last_validation_corrections: list[str] = []

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
        # AF-0119: Reset last response tracking
        self._last_response = None
        self._last_plan_response = None
        self._last_validation_corrections = []

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
            self._last_response = response  # AF-0119: Track for metadata
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise PlannerError(f"LLM call failed: {e}") from e

        # Step 4: Parse and validate response
        try:
            plan_response = self._parse_response(response.content)
            self._last_plan_response = plan_response  # AF-0119: Track for metadata
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

    def plan_with_metadata(self, task: TaskSpec) -> PlanningResult:
        """Generate plan and return with timing/LLM metadata (AF-0119)."""
        started_at = datetime.now(UTC)
        playbook = self.plan(task)
        ended_at = datetime.now(UTC)
        duration_ms = int((ended_at - started_at).total_seconds() * 1000)

        # Extract LLM metadata from tracked response
        model_used = None
        input_tokens = None
        output_tokens = None
        total_tokens = None
        if self._last_response is not None:
            model_used = getattr(self._last_response, "model", None)
            input_tokens = getattr(self._last_response, "input_tokens", None)
            output_tokens = getattr(self._last_response, "output_tokens", None)
            total_tokens = getattr(self._last_response, "tokens_used", None)

        # Extract raw steps for trace
        raw_steps: list[dict[str, Any]] = []
        confidence: float | None = None
        if self._last_plan_response is not None:
            confidence = self._last_plan_response.confidence
            for step in self._last_plan_response.steps:
                raw_steps.append({
                    "type": step.type,
                    "skill": step.skill,
                    "playbook": step.playbook,
                    "rationale": step.rationale,
                })

        return PlanningResult(
            playbook=playbook,
            planner_name="V1Planner",
            started_at=started_at,
            ended_at=ended_at,
            duration_ms=duration_ms,
            model_used=model_used,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            confidence=confidence,
            raw_steps=raw_steps,
            validation_corrections=self._last_validation_corrections,
        )

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
3. The runtime automatically chains step outputs to the next step's input — do NOT
   use "previous_step.X" references in params. Only include static configuration
   values that the skill needs (e.g. artifact_name, output_format). Omit fields
   that come from the previous step's output.
4. Minimize steps while ensuring task completion
5. Provide clear rationale for each step
6. For load_documents: prefer the default patterns (["**/*.md"]) unless the task
   explicitly requires other file types. Do not invent patterns like *.docx or
   *.pdf unless the user asks for those formats

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

        # Clean common LLM JSON errors
        # Strip // line comments (outside quoted strings) by processing line-by-line
        cleaned_lines: list[str] = []
        for line in json_str.split("\n"):
            stripped = line.lstrip()
            if stripped.startswith("//"):
                continue  # skip full-line comments
            # Remove trailing // comments only if not inside a string value
            # Simple heuristic: count unescaped quotes before the //
            comment_pos = line.find("//")
            if comment_pos > 0:
                prefix = line[:comment_pos]
                if prefix.count('"') % 2 == 0:
                    line = prefix.rstrip()
            cleaned_lines.append(line)
        json_str = "\n".join(cleaned_lines)
        json_str = re.sub(r",\s*([}\]])", r"\1", json_str)  # strip trailing commas

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


# ---------------------------------------------------------------------------
# V2Planner Implementation (AF-0103)
# ---------------------------------------------------------------------------


class V2Planner(V1Planner):
    """LLM-based planner that composes mixed skill+playbook plans (AF-0103).

    Extends V1Planner by adding playbook awareness: the LLM can use both
    individual skills and existing playbooks as building blocks.

    Implements Planner Protocol: plan(task) -> Playbook
    """

    def plan(self, task: TaskSpec) -> Playbook:
        """Generate a mixed skill+playbook plan from the task."""
        # AF-0119: Reset metadata tracking
        self._last_response = None
        self._last_plan_response = None
        self._last_validation_corrections = []

        catalog = self._get_skill_catalog()
        if not catalog:
            raise PlannerError("No skills available in registry")

        playbook_catalog = self._get_playbook_catalog()

        prompt = self._build_v2_prompt(task, catalog, playbook_catalog)

        try:
            response = self.provider.chat(
                messages=[
                    ChatMessage(role=MessageRole.SYSTEM, content=self._get_v2_system_prompt()),
                    ChatMessage(role=MessageRole.USER, content=prompt),
                ],
            )
            self._last_response = response  # AF-0119: Track for metadata
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise PlannerError(f"LLM call failed: {e}") from e

        try:
            plan_response = self._parse_response(response.content)
            self._last_plan_response = plan_response  # AF-0119: Track for metadata
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}")
            raise PlannerError(f"Failed to parse LLM response: {e}") from e

        self._validate_v2_steps(plan_response)
        playbook = self._build_v2_playbook(task, plan_response)

        logger.info(
            f"V2Planner generated plan with {len(playbook.steps)} steps "
            f"(confidence: {plan_response.confidence:.2f})"
        )
        return playbook

    def _get_playbook_catalog(self) -> list[dict[str, Any]]:
        """Extract playbook metadata for LLM context."""
        from ag.playbooks import list_playbooks
        from ag.playbooks.registry import get_playbook_entry

        catalog = []
        for name in list_playbooks():
            entry = get_playbook_entry(name)
            if entry is None:
                continue
            pb = entry.playbook
            skill_sequence = [s.skill_name for s in pb.steps if s.skill_name]
            catalog.append(
                {
                    "name": pb.name,
                    "description": pb.description,
                    "steps": skill_sequence,
                }
            )
        return catalog

    def _get_v2_system_prompt(self) -> str:
        """System prompt that includes playbook awareness."""
        return """You are an execution planner for an agent system. Your job is to create
execution plans by composing available skills AND playbooks into a sequence of steps.

A playbook is a pre-validated, tested sequence of skills for a specific task pattern.
When a playbook matches the user's need, prefer it over composing individual skills.

Rules:
1. Only use skills and playbooks from the provided catalogs
2. Order steps logically — later steps may depend on earlier outputs
3. The runtime automatically chains step outputs to the next step's input — do NOT
   use "previous_step.X" references in params. Only include static configuration
   values. Omit fields that come from the previous step's output.
4. Prefer playbooks when the task closely matches a playbook's use case
5. Use individual skills when playbooks don't fit or for additional steps
6. You can mix playbooks and skills in a single plan

Respond with valid JSON matching this schema:
{
  "steps": [
    {"type": "skill", "skill": "skill_name", "params": {...}, "rationale": "..."},
    {"type": "playbook", "playbook": "playbook_name", "params": {...}, "rationale": "..."}
  ],
  "estimated_tokens": 5000,
  "confidence": 0.85,
  "warnings": ["optional warnings"]
}"""

    def _build_v2_prompt(
        self,
        task: TaskSpec,
        skill_catalog: list[dict[str, Any]],
        playbook_catalog: list[dict[str, Any]],
    ) -> str:
        """Build user prompt with both skill and playbook catalogs."""
        # Format playbooks
        playbook_lines = []
        for pb in playbook_catalog:
            steps_str = " → ".join(pb["steps"]) if pb["steps"] else "(no skills)"
            playbook_lines.append(f"- **{pb['name']}**: {pb['description']}\n  Steps: {steps_str}")
        playbooks_str = "\n".join(playbook_lines) if playbook_lines else "(none)"

        # Format skills (reuse V1 logic)
        skills_text = []
        for skill in skill_catalog:
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

        constraints = []
        if task.budgets.max_steps:
            constraints.append(f"- Maximum {task.budgets.max_steps} steps")
        if task.constraints.allowed_skills:
            constraints.append(f"- Only use: {', '.join(task.constraints.allowed_skills)}")
        if task.constraints.blocked_skills:
            constraints.append(f"- Do not use: {', '.join(task.constraints.blocked_skills)}")
        constraints_str = "\n".join(constraints) if constraints else "None"

        files_hint = self._detect_workspace_files(task.workspace_id)

        return f"""Create an execution plan for this task:

**Task:** {task.prompt}

**Available Playbooks (pre-built sequences):**
{playbooks_str}

**Available Skills (for custom composition):**
{catalog_str}
{files_hint}
**Constraints:**
{constraints_str}

**Maximum steps:** {self.max_steps}

Strategy:
1. Prefer playbooks when the task closely matches a playbook's use case
2. Use individual skills when playbooks don't fit or for additional steps
3. You can mix playbooks and skills in a single plan

Respond with a JSON plan."""

    def _validate_v2_steps(self, plan: LLMPlanResponse) -> None:
        """Validate skill and playbook references in V2 plan.

        Performs cross-check validation and auto-correction (BUG-0018):
        - If type=skill but name exists only as playbook → correct to playbook, warn
        - If type=playbook but name exists only as skill → correct to skill, warn
        - If name exists in neither → raise PlannerError
        - If name exists in both → trust declared type
        """
        from ag.playbooks import get_playbook as get_pb
        from ag.playbooks import list_playbooks as list_pbs

        for step in plan.steps:
            step_type = step.type
            if step_type == "skill":
                if not step.skill:
                    raise PlannerError("Skill step missing 'skill' field")

                skill_exists = self.skill_registry.has(step.skill)
                playbook_exists = get_pb(step.skill) is not None

                if skill_exists:
                    # Skill found, all good
                    pass
                elif playbook_exists:
                    # BUG-0018: LLM misclassified playbook as skill — auto-correct
                    correction = (
                        f"Auto-corrected step type: '{step.skill}' is a playbook, "
                        f"not a skill (LLM misclassified)"
                    )
                    logger.warning(correction)
                    self._last_validation_corrections.append(correction)  # AF-0119
                    step.type = "playbook"
                    step.playbook = step.skill
                    step.skill = None
                else:
                    raise PlannerError(
                        f"Invalid skill '{step.skill}' in plan. "
                        f"Available skills: {', '.join(self.skill_registry.list_skills())}. "
                        f"Available playbooks: {', '.join(list_pbs())}"
                    )

            elif step_type == "playbook":
                if not step.playbook:
                    raise PlannerError("Playbook step missing 'playbook' field")

                playbook_exists = get_pb(step.playbook) is not None
                skill_exists = self.skill_registry.has(step.playbook)

                if playbook_exists:
                    # Playbook found, all good
                    pass
                elif skill_exists:
                    # BUG-0018: LLM misclassified skill as playbook — auto-correct
                    correction = (
                        f"Auto-corrected step type: '{step.playbook}' is a skill, "
                        f"not a playbook (LLM misclassified)"
                    )
                    logger.warning(correction)
                    self._last_validation_corrections.append(correction)  # AF-0119
                    step.type = "skill"
                    step.skill = step.playbook
                    step.playbook = None
                else:
                    raise PlannerError(
                        f"Invalid playbook '{step.playbook}' in plan. "
                        f"Available playbooks: {', '.join(list_pbs())}. "
                        f"Available skills: {', '.join(self.skill_registry.list_skills())}"
                    )
            else:
                raise PlannerError(
                    f"Unknown step type '{step_type}', expected 'skill' or 'playbook'"
                )

    def _build_v2_playbook(self, task: TaskSpec, plan: LLMPlanResponse) -> Playbook:
        """Convert V2 plan response to Playbook with mixed step types."""
        plan_id = f"v2plan_{uuid4().hex[:8]}"
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

        steps = []
        for i, planned_step in enumerate(plan.steps):
            if planned_step.type == "playbook":
                step = PlaybookStep(
                    step_id=f"step_{i}",
                    name=f"{planned_step.playbook}_{i}",
                    step_type=PlaybookStepType.PLAYBOOK,
                    skill_name=planned_step.playbook,  # reuse skill_name field for playbook name
                    description=planned_step.rationale,
                    required=True,
                    retry_count=0,
                    parameters=planned_step.params,
                )
            else:
                step = PlaybookStep(
                    step_id=f"step_{i}",
                    name=f"{planned_step.skill}_{i}",
                    step_type=PlaybookStepType.SKILL,
                    skill_name=planned_step.skill,
                    description=planned_step.rationale,
                    required=True,
                    retry_count=1,
                    parameters=planned_step.params,
                )
            steps.append(step)

        return Playbook(
            playbook_version="0.1",
            name=plan_id,
            version="1.0.0",
            description=f"V2Planner generated plan for: {task.prompt[:100]}",
            reasoning_modes=[ReasoningMode.DIRECT],
            budgets=Budgets(
                max_steps=len(steps) + 2,
                max_tokens=plan.estimated_tokens or self.DEFAULT_MAX_TOKENS,
                max_duration_seconds=self.DEFAULT_TIMEOUT_SECONDS,
            ),
            steps=steps,
            metadata={
                "generated_by": "V2Planner",
                "generated_at": timestamp,
                "confidence": plan.confidence,
                "warnings": plan.warnings,
                "original_task": task.prompt,
            },
        )

    def plan_with_metadata(self, task: TaskSpec) -> PlanningResult:
        """Generate plan and return with timing/LLM metadata (AF-0119).

        Overrides V1Planner version to use V2Planner name.
        """
        started_at = datetime.now(UTC)
        playbook = self.plan(task)
        ended_at = datetime.now(UTC)
        duration_ms = int((ended_at - started_at).total_seconds() * 1000)

        # Extract LLM metadata from tracked response
        model_used = None
        input_tokens = None
        output_tokens = None
        total_tokens = None
        if self._last_response is not None:
            model_used = getattr(self._last_response, "model", None)
            input_tokens = getattr(self._last_response, "input_tokens", None)
            output_tokens = getattr(self._last_response, "output_tokens", None)
            total_tokens = getattr(self._last_response, "tokens_used", None)

        # Extract raw steps for trace
        raw_steps: list[dict[str, Any]] = []
        confidence: float | None = None
        if self._last_plan_response is not None:
            confidence = self._last_plan_response.confidence
            for step in self._last_plan_response.steps:
                raw_steps.append({
                    "type": step.type,
                    "skill": step.skill,
                    "playbook": step.playbook,
                    "rationale": step.rationale,
                })

        return PlanningResult(
            playbook=playbook,
            planner_name="V2Planner",
            started_at=started_at,
            ended_at=ended_at,
            duration_ms=duration_ms,
            model_used=model_used,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            confidence=confidence,
            raw_steps=raw_steps,
            validation_corrections=self._last_validation_corrections,
        )
