"""Skill registry for v0 runtime.

Skills are simple callables that take parameters and return results.
v0 includes stub implementations for testing.

AF0060: Added support for new Skill protocol alongside legacy callables.
The registry supports both:
- Legacy: SkillFn = Callable[[dict], tuple[bool, str, dict]]
- New: Skill protocol with typed input/output schemas
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from ag.skills.base import Skill, SkillContext, SkillInput, SkillOutput
from ag.skills.strategic_brief import StrategicBriefSkillV2, strategic_brief_skill

# Skill function signature: (params: dict) -> tuple[bool, str, dict]
# Returns: (success, output_summary, result_data)
SkillFn = Callable[[dict[str, Any]], tuple[bool, str, dict[str, Any]]]


@dataclass
class SkillInfo:
    """Metadata about a registered legacy skill."""

    name: str
    description: str
    fn: SkillFn
    is_stub: bool = True  # Mark if this is a stub skill


@dataclass
class SkillV2Info:
    """Metadata about a registered v2 skill (AF0060).

    v2 skills use the Skill protocol with typed schemas.
    """

    name: str
    description: str
    skill: Skill[Any, Any]
    input_schema: type[SkillInput]
    output_schema: type[SkillOutput]
    requires_llm: bool = False


class SkillRegistry:
    """Registry of available skills.

    Supports both legacy (v1) and new (v2) skill formats:
    - v1: SkillFn = Callable[[dict], tuple[bool, str, dict]]
    - v2: Skill protocol with typed schemas (AF0060)

    v0: Skills are registered at startup. No dynamic loading.
    """

    def __init__(self) -> None:
        self._skills: dict[str, SkillInfo] = {}
        self._skills_v2: dict[str, SkillV2Info] = {}

    def register(
        self,
        name: str,
        description: str,
        fn: SkillFn,
        is_stub: bool = True,
    ) -> None:
        """Register a legacy (v1) skill.

        Args:
            name: Unique skill name
            description: Human-readable description
            fn: Skill function
            is_stub: Whether this is a stub skill (default True for legacy)
        """
        self._skills[name] = SkillInfo(
            name=name, description=description, fn=fn, is_stub=is_stub
        )

    def register_v2(self, skill: Skill[Any, Any]) -> None:
        """Register a v2 skill (AF0060).

        Args:
            skill: Skill instance implementing the Skill protocol
        """
        self._skills_v2[skill.name] = SkillV2Info(
            name=skill.name,
            description=skill.description,
            skill=skill,
            input_schema=skill.input_schema,
            output_schema=skill.output_schema,
            requires_llm=skill.requires_llm,
        )

    def get(self, name: str) -> SkillInfo | None:
        """Get a legacy skill by name."""
        return self._skills.get(name)

    def get_v2(self, name: str) -> SkillV2Info | None:
        """Get a v2 skill by name."""
        return self._skills_v2.get(name)

    def is_v2(self, name: str) -> bool:
        """Check if a skill is a v2 skill."""
        return name in self._skills_v2

    def execute(
        self,
        name: str,
        parameters: dict[str, Any],
        context: SkillContext | None = None,
    ) -> tuple[bool, str, dict[str, Any]]:
        """Execute a skill by name.

        Handles both v1 and v2 skills transparently:
        - v1: Calls fn(parameters)
        - v2: Builds typed input, calls execute(input, ctx), converts output

        Args:
            name: Skill name
            parameters: Skill parameters
            context: Optional SkillContext for v2 skills

        Returns:
            Tuple of (success, output_summary, result_data)

        Raises:
            KeyError: If skill not found
        """
        # Check v2 skills first (preferred)
        if name in self._skills_v2:
            return self._execute_v2(name, parameters, context)

        # Fall back to v1 skill
        skill = self._skills.get(name)
        if skill is None:
            raise KeyError(f"Skill not found: {name}")
        return skill.fn(parameters)

    def _execute_v2(
        self,
        name: str,
        parameters: dict[str, Any],
        context: SkillContext | None,
    ) -> tuple[bool, str, dict[str, Any]]:
        """Execute a v2 skill with typed schemas."""
        skill_info = self._skills_v2[name]
        skill = skill_info.skill

        # Build context if not provided
        ctx = context or SkillContext()

        # Validate context requirements
        try:
            skill.validate_context(ctx)
        except ValueError as e:
            return False, str(e), {"error": "context_validation_failed"}

        # Parse input from parameters
        try:
            input_data = skill_info.input_schema.model_validate(parameters)
        except Exception as e:
            return False, f"Invalid input: {e}", {"error": "input_validation_failed"}

        # Execute skill
        try:
            output = skill.execute(input_data, ctx)
            return output.to_legacy_tuple()
        except Exception as e:
            return False, f"Skill execution failed: {e}", {"error": str(e)}

    def list(self) -> list[str]:
        """List all registered skill names (v1 and v2)."""
        all_names = set(self._skills.keys()) | set(self._skills_v2.keys())
        return sorted(all_names)

    def has(self, name: str) -> bool:
        """Check if a skill is registered (v1 or v2)."""
        return name in self._skills or name in self._skills_v2

    def get_info(self, name: str) -> dict[str, Any] | None:
        """Get skill info dict (works for both v1 and v2).

        Returns dict with: name, description, is_stub, is_v2,
        and for v2: input_schema, output_schema, requires_llm
        """
        if name in self._skills_v2:
            info = self._skills_v2[name]
            return {
                "name": info.name,
                "description": info.description,
                "is_stub": False,
                "is_v2": True,
                "requires_llm": info.requires_llm,
                "input_schema": info.input_schema.model_json_schema(),
                "output_schema": info.output_schema.model_json_schema(),
            }
        if name in self._skills:
            info = self._skills[name]
            return {
                "name": info.name,
                "description": info.description,
                "is_stub": info.is_stub,
                "is_v2": False,
            }
        return None


# ---------------------------------------------------------------------------
# Stub Skills for v0 Testing
# ---------------------------------------------------------------------------


def _echo_tool(params: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    """Echo skill: returns input as output. Useful for testing."""
    message = params.get("message", "")
    return True, f"Echo: {message}", {"echoed": message}


def _analyze_task(params: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    """Stub analyze skill: pretends to analyze a task."""
    prompt = params.get("prompt", "")
    return True, f"Analyzed task: {prompt[:50]}...", {"analysis": "Task understood"}


def _execute_task(params: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    """Stub execute skill: pretends to execute a task."""
    return True, "Task executed successfully", {"result": "completed"}


def _verify_result(params: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    """Stub verify skill: pretends to verify results."""
    return True, "Verification passed", {"verified": True}


def _fail_skill(params: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    """Skill that always fails. Useful for failure testing."""
    return False, "Intentional failure for testing", {"error": "forced_failure"}


def _error_skill(params: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    """Skill that raises an exception. Useful for error handling tests."""
    raise RuntimeError("Intentional error for testing")


# ---------------------------------------------------------------------------
# AF-0019: Delegation Skills
# ---------------------------------------------------------------------------


def _normalize_input(params: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    """Normalize and validate task input for delegation.

    Returns prepared context for subsequent steps.
    """
    prompt = params.get("prompt", "")
    if not prompt.strip():
        return False, "Empty prompt", {"error": "prompt_empty"}

    # Simple normalization: trim, lowercase for analysis
    normalized = prompt.strip()
    return (
        True,
        f"Input normalized: {normalized[:50]}...",
        {
            "normalized_prompt": normalized,
            "word_count": len(normalized.split()),
            "ready_for_planning": True,
        },
    )


def _plan_subtasks(params: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    """Generate subtasks from the prompt.

    v0 heuristic: Split prompt into analysis + execution subtasks.
    Returns at least 2 subtasks as required by AF-0019.
    """
    prompt = params.get("prompt", "")
    params.get("min_subtasks", 2)

    # v0 simple planning: always generate exactly 2 subtasks
    subtasks = [
        {
            "subtask_id": "subtask_0",
            "description": f"Analyze requirements: {prompt[:30]}...",
            "status": "pending",
        },
        {
            "subtask_id": "subtask_1",
            "description": f"Execute solution: {prompt[:30]}...",
            "status": "pending",
        },
    ]

    return (
        True,
        f"Planned {len(subtasks)} subtasks",
        {
            "subtasks": subtasks,
            "plan_complete": True,
        },
    )


def _execute_subtask(params: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    """Execute a single subtask from the plan.

    Args via params:
        subtask_index: Which subtask to execute (0 or 1)
        subtasks: List of subtasks from planning (optional, for context)
    """
    subtask_index = params.get("subtask_index", 0)

    # v0 stub: pretend to execute the subtask
    result = f"Subtask {subtask_index} executed successfully"
    return (
        True,
        result,
        {
            "subtask_index": subtask_index,
            "status": "completed",
            "result_summary": result,
        },
    )


def _verify_delegation(params: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    """Verify all subtask results and aggregate evidence."""
    # v0 stub: always pass verification
    return (
        True,
        "All subtasks verified",
        {
            "verification_status": "passed",
            "evidence": {"subtasks_checked": 2, "all_passed": True},
        },
    )


def _finalize_result(params: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    """Summarize delegation results and prepare final output."""
    return (
        True,
        "Delegation completed successfully",
        {
            "summary": "All subtasks executed and verified",
            "finalized": True,
        },
    )


# ---------------------------------------------------------------------------
# Default Registry
# ---------------------------------------------------------------------------


def create_default_registry() -> SkillRegistry:
    """Create a registry with default skills.

    Skills are categorized as:
    - Real skills: Do actual work (strategic_brief)
    - Stub skills: Placeholder implementations for testing

    Returns:
        SkillRegistry with default skills registered
    """
    registry = SkillRegistry()

    # Testing skills (stubs)
    registry.register("echo_tool", "Echoes input message", _echo_tool, is_stub=True)

    # Playbook skills (stubs)
    registry.register("analyze_task", "Analyze task requirements", _analyze_task, is_stub=True)
    registry.register("execute_task", "Execute the main task", _execute_task, is_stub=True)
    registry.register("verify_result", "Verify execution results", _verify_result, is_stub=True)

    # AF-0019: Delegation skills (stubs)
    registry.register("normalize_input", "Normalize task input", _normalize_input, is_stub=True)
    registry.register(
        "plan_subtasks", "Generate subtasks from prompt", _plan_subtasks, is_stub=True
    )
    registry.register(
        "execute_subtask", "Execute a single subtask", _execute_subtask, is_stub=True
    )
    registry.register(
        "verify_delegation", "Verify delegation results", _verify_delegation, is_stub=True
    )
    registry.register(
        "finalize_result", "Finalize delegation output", _finalize_result, is_stub=True
    )

    # Failure testing skills (stubs)
    registry.register("fail_skill", "Always fails (for testing)", _fail_skill, is_stub=True)
    registry.register(
        "error_skill", "Always raises exception (for testing)", _error_skill, is_stub=True
    )

    # AF-0048: Strategic brief skill (REAL - does actual file reading)
    registry.register(
        "strategic_brief",
        "Generate strategic brief from workspace markdown files",
        strategic_brief_skill,
        is_stub=False,
    )

    # AF-0060: Strategic brief v2 skill (with LLM support)
    registry.register_v2(StrategicBriefSkillV2())

    return registry


# Global default registry instance
_default_registry: SkillRegistry | None = None


def get_default_registry() -> SkillRegistry:
    """Get the default skill registry (lazy-initialized singleton)."""
    global _default_registry
    if _default_registry is None:
        _default_registry = create_default_registry()
    return _default_registry
