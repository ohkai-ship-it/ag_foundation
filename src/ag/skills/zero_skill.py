"""Zero skill — a minimal dummy skill with no functionality.

This skill exists as a placeholder/dummy for testing and development purposes.
It accepts any prompt and returns a success response with no actual processing.
"""

from __future__ import annotations

from typing import ClassVar

from ag.skills.base import Skill, SkillContext, SkillInput, SkillOutput


class ZeroSkillInput(SkillInput):
    """Input for zero skill (uses base SkillInput with prompt field)."""

    pass


class ZeroSkillOutput(SkillOutput):
    """Output for zero skill (uses base SkillOutput fields)."""

    pass


class ZeroSkill(Skill[ZeroSkillInput, ZeroSkillOutput]):
    """A dummy skill that does nothing.

    This skill is a placeholder with no functionality. It accepts input
    and returns a successful response without performing any processing.
    """

    name: ClassVar[str] = "zero_skill"
    description: ClassVar[str] = "Dummy skill with no functionality"
    input_schema: ClassVar[type[ZeroSkillInput]] = ZeroSkillInput
    output_schema: ClassVar[type[ZeroSkillOutput]] = ZeroSkillOutput
    requires_llm: ClassVar[bool] = False

    def execute(self, input: ZeroSkillInput, ctx: SkillContext) -> ZeroSkillOutput:
        """Execute the zero skill (does nothing)."""
        return ZeroSkillOutput(
            success=True,
            summary="Zero skill executed (no operation)",
        )
