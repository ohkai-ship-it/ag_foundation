"""Test stub skills using the V2 Skill framework (AF0079).

This module provides stub skills for testing:
    - EchoSkill: Returns the input message; used in CLI tests

These are NOT production skills. They exist only for testing
playbook execution and CLI skill invocation.
"""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import Field

from ag.skills.base import Skill, SkillContext, SkillInput, SkillOutput

# ---------------------------------------------------------------------------
# Echo Skill (for testing)
# ---------------------------------------------------------------------------


class EchoInput(SkillInput):
    """Input for echo skill."""

    message: str = Field(default="", description="Message to echo back")


class EchoOutput(SkillOutput):
    """Output for echo skill."""

    echoed: str = Field(default="", description="The echoed message")


class EchoSkill(Skill[EchoInput, EchoOutput]):
    """Echo skill that returns the input message.

    Used for testing skill invocation without LLM calls.

    Args:
        message: Message to echo

    Returns:
        The same message echoed back
    """

    name: ClassVar[str] = "echo_tool"
    description: ClassVar[str] = "Echo the input message back"
    input_schema: ClassVar[type[EchoInput]] = EchoInput
    output_schema: ClassVar[type[EchoOutput]] = EchoOutput
    requires_llm: ClassVar[bool] = False

    def execute(self, input: EchoInput, ctx: SkillContext) -> EchoOutput:
        """Echo the input message."""
        # Use message if provided, otherwise fall back to prompt
        msg = input.message or input.prompt
        return EchoOutput(
            success=True,
            summary=f"Echoed: {msg}",
            echoed=msg,
        )


# ---------------------------------------------------------------------------
# Fail Skill (for testing error paths)
# ---------------------------------------------------------------------------


class FailSkill(Skill[SkillInput, SkillOutput]):
    """Skill that always fails (for testing error handling)."""

    name: ClassVar[str] = "fail_skill"
    description: ClassVar[str] = "Always fails (testing)"
    input_schema: ClassVar[type[SkillInput]] = SkillInput
    output_schema: ClassVar[type[SkillOutput]] = SkillOutput
    requires_llm: ClassVar[bool] = False

    def execute(self, input: SkillInput, ctx: SkillContext) -> SkillOutput:
        """Fail with a predetermined error."""
        return SkillOutput(
            success=False,
            summary="Intentional failure for testing",
            error="fail_skill always fails",
        )


# ---------------------------------------------------------------------------
# Error Skill (for testing exception handling)
# ---------------------------------------------------------------------------


class ErrorSkill(Skill[SkillInput, SkillOutput]):
    """Skill that raises an exception (for testing exception handling)."""

    name: ClassVar[str] = "error_skill"
    description: ClassVar[str] = "Always raises exception (testing)"
    input_schema: ClassVar[type[SkillInput]] = SkillInput
    output_schema: ClassVar[type[SkillOutput]] = SkillOutput
    requires_llm: ClassVar[bool] = False

    def execute(self, input: SkillInput, ctx: SkillContext) -> SkillOutput:
        """Raise an exception for testing."""
        raise RuntimeError("Intentional error for testing")


# ---------------------------------------------------------------------------
# Factory Functions
# ---------------------------------------------------------------------------


def get_test_stubs() -> list[Any]:
    """Get all test stub skill instances.

    Returns:
        List of test stub skill instances to register
    """
    return [
        EchoSkill(),
        FailSkill(),
        ErrorSkill(),
    ]
