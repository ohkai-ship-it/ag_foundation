"""V0 Executor implementation.

Extracted from runtime.py (AF-0114).
"""

from __future__ import annotations

from typing import Any

from ag.skills import SkillContext, SkillRegistry, get_default_registry


class V0Executor:
    """v0 Executor: executes skills from registry."""

    def __init__(self, registry: SkillRegistry | None = None) -> None:
        self._registry = registry or get_default_registry()

    def execute(
        self,
        skill_name: str,
        parameters: dict[str, Any],
        context: SkillContext | None = None,
    ) -> tuple[bool, str, dict[str, Any]]:
        """Execute a skill.

        Args:
            skill_name: Name of the skill to execute
            parameters: Skill parameters
            context: Optional SkillContext with workspace, provider, etc.

        Returns:
            Tuple of (success, output_summary, result_data)
        """
        if not self._registry.has(skill_name):
            raise KeyError(f"Skill not found: {skill_name}")

        return self._registry.execute(skill_name, parameters, context)
