"""Skill registry for v0 runtime.

Skills are simple callables that take parameters and return results.
v0 includes stub implementations for testing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

# Skill function signature: (params: dict) -> tuple[bool, str, dict]
# Returns: (success, output_summary, result_data)
SkillFn = Callable[[dict[str, Any]], tuple[bool, str, dict[str, Any]]]


@dataclass
class SkillInfo:
    """Metadata about a registered skill."""

    name: str
    description: str
    fn: SkillFn


class SkillRegistry:
    """Registry of available skills.

    v0: Skills are registered at startup. No dynamic loading.
    """

    def __init__(self) -> None:
        self._skills: dict[str, SkillInfo] = {}

    def register(self, name: str, description: str, fn: SkillFn) -> None:
        """Register a skill.

        Args:
            name: Unique skill name
            description: Human-readable description
            fn: Skill function
        """
        self._skills[name] = SkillInfo(name=name, description=description, fn=fn)

    def get(self, name: str) -> SkillInfo | None:
        """Get a skill by name."""
        return self._skills.get(name)

    def execute(
        self, name: str, parameters: dict[str, Any]
    ) -> tuple[bool, str, dict[str, Any]]:
        """Execute a skill by name.

        Args:
            name: Skill name
            parameters: Skill parameters

        Returns:
            Tuple of (success, output_summary, result_data)

        Raises:
            KeyError: If skill not found
        """
        skill = self._skills.get(name)
        if skill is None:
            raise KeyError(f"Skill not found: {name}")
        return skill.fn(parameters)

    def list(self) -> list[str]:
        """List registered skill names."""
        return list(self._skills.keys())

    def has(self, name: str) -> bool:
        """Check if a skill is registered."""
        return name in self._skills


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
# Default Registry
# ---------------------------------------------------------------------------


def create_default_registry() -> SkillRegistry:
    """Create a registry with default stub skills.

    Returns:
        SkillRegistry with v0 stub skills registered
    """
    registry = SkillRegistry()

    # Testing skills
    registry.register("echo_tool", "Echoes input message", _echo_tool)

    # Playbook skills (stubs)
    registry.register("analyze_task", "Analyze task requirements", _analyze_task)
    registry.register("execute_task", "Execute the main task", _execute_task)
    registry.register("verify_result", "Verify execution results", _verify_result)

    # Failure testing skills
    registry.register("fail_skill", "Always fails (for testing)", _fail_skill)
    registry.register("error_skill", "Always raises exception (for testing)", _error_skill)

    return registry


# Global default registry instance
_default_registry: SkillRegistry | None = None


def get_default_registry() -> SkillRegistry:
    """Get the default skill registry (lazy-initialized singleton)."""
    global _default_registry
    if _default_registry is None:
        _default_registry = create_default_registry()
    return _default_registry
