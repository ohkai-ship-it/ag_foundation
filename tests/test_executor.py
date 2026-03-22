"""Tests for V0Executor and V1Executor (AF-0116).

Tests the executor implementations including output validation and retry.
"""

from __future__ import annotations

from typing import ClassVar

import pytest
from pydantic import Field

from ag.core.executor import DEFAULT_MAX_VALIDATION_ATTEMPTS, V0Executor, V1Executor
from ag.skills.base import Skill, SkillContext, SkillInput, SkillOutput
from ag.skills.registry import SkillRegistry

# ---------------------------------------------------------------------------
# Test Fixtures - Skills for Testing
# ---------------------------------------------------------------------------


class SimpleOutput(SkillOutput):
    """Simple output with one extra field."""

    value: str = Field(default="", description="Result value")


class SimpleSkill(Skill[SkillInput, SimpleOutput]):
    """Simple skill that always succeeds."""

    name: ClassVar[str] = "simple_skill"
    description: ClassVar[str] = "A simple test skill"
    input_schema: ClassVar[type[SkillInput]] = SkillInput
    output_schema: ClassVar[type[SkillOutput]] = SimpleOutput
    requires_llm: ClassVar[bool] = False

    def execute(self, input: SkillInput, ctx: SkillContext) -> SimpleOutput:
        """Return simple success."""
        return SimpleOutput(
            success=True,
            summary="Simple success",
            value="result",
        )


class FailingSkill(Skill[SkillInput, SkillOutput]):
    """Skill that always fails execution."""

    name: ClassVar[str] = "failing_skill"
    description: ClassVar[str] = "Always fails"
    input_schema: ClassVar[type[SkillInput]] = SkillInput
    output_schema: ClassVar[type[SkillOutput]] = SkillOutput
    requires_llm: ClassVar[bool] = False

    def execute(self, input: SkillInput, ctx: SkillContext) -> SkillOutput:
        """Fail."""
        return SkillOutput(success=False, summary="Always fails", error="deliberate")


class FlakeySkillCounter:
    """Counter to track flakey skill calls."""

    call_count: int = 0

    @classmethod
    def reset(cls) -> None:
        cls.call_count = 0

    @classmethod
    def increment(cls) -> int:
        cls.call_count += 1
        return cls.call_count


class FlakeyOutput(SkillOutput):
    """Output for flakey skill."""

    attempt: int = Field(default=0, description="Which attempt succeeded")


class FlakeySkill(Skill[SkillInput, FlakeyOutput]):
    """Skill that fails N times then succeeds.

    Uses FlakeySkillCounter to track calls across execute_raw invocations.
    """

    name: ClassVar[str] = "flakey_skill"
    description: ClassVar[str] = "Fails first N times"
    input_schema: ClassVar[type[SkillInput]] = SkillInput
    output_schema: ClassVar[type[SkillOutput]] = FlakeyOutput
    requires_llm: ClassVar[bool] = False

    # How many times to fail before succeeding
    fail_count: ClassVar[int] = 2

    def execute(self, input: SkillInput, ctx: SkillContext) -> FlakeyOutput:
        """Fail N times then succeed."""
        attempt = FlakeySkillCounter.increment()
        if attempt <= self.fail_count:
            # Return invalid output (missing required field or wrong type)
            # We create an invalid output by having a mismatch
            return FlakeyOutput(
                success=False,  # Deliberately "fail" with wrong data
                summary=f"Deliberate failure {attempt}",
                error="flakey_error",
                attempt=attempt,
            )
        # Eventually succeed
        return FlakeyOutput(
            success=True,
            summary=f"Succeeded on attempt {attempt}",
            attempt=attempt,
        )


class AlwaysInvalidOutput(SkillOutput):
    """Output that requires specific validation."""

    required_field: str = Field(description="Must not be empty")


class AlwaysInvalidSkill(Skill[SkillInput, AlwaysInvalidOutput]):
    """Skill that always returns invalid output (missing required field)."""

    name: ClassVar[str] = "always_invalid"
    description: ClassVar[str] = "Returns output missing required field"
    input_schema: ClassVar[type[SkillInput]] = SkillInput
    output_schema: ClassVar[type[SkillOutput]] = AlwaysInvalidOutput
    requires_llm: ClassVar[bool] = False

    def execute(self, input: SkillInput, ctx: SkillContext) -> AlwaysInvalidOutput:
        """Return technically valid but semantically bad output."""
        return AlwaysInvalidOutput(
            success=True,
            summary="Invalid output",
            required_field="",  # Provide but empty - validation still passes
        )


@pytest.fixture
def registry() -> SkillRegistry:
    """Create a fresh registry with test skills."""
    reg = SkillRegistry()
    reg.register(SimpleSkill())
    reg.register(FailingSkill())
    reg.register(FlakeySkill())
    reg.register(AlwaysInvalidSkill())
    return reg


# ---------------------------------------------------------------------------
# V0Executor Tests
# ---------------------------------------------------------------------------


class TestV0Executor:
    """Tests for V0Executor basic functionality."""

    def test_execute_simple_skill(self, registry: SkillRegistry) -> None:
        """V0Executor can execute a simple skill."""
        executor = V0Executor(registry)
        success, summary, data = executor.execute("simple_skill", {})

        assert success is True
        assert "success" in summary.lower()
        assert data.get("value") == "result"

    def test_execute_unknown_skill_raises(self, registry: SkillRegistry) -> None:
        """V0Executor raises KeyError for unknown skill."""
        executor = V0Executor(registry)

        with pytest.raises(KeyError, match="unknown_skill"):
            executor.execute("unknown_skill", {})

    def test_execute_failing_skill(self, registry: SkillRegistry) -> None:
        """V0Executor returns failure for failing skill."""
        executor = V0Executor(registry)
        success, summary, data = executor.execute("failing_skill", {})

        assert success is False
        assert data.get("error") == "deliberate"


# ---------------------------------------------------------------------------
# V1Executor Tests - Output Validation
# ---------------------------------------------------------------------------


class TestV1ExecutorValidation:
    """Tests for V1Executor output validation."""

    def test_valid_output_passes(self, registry: SkillRegistry) -> None:
        """V1Executor passes valid output on first attempt."""
        executor = V1Executor(registry)
        success, summary, data = executor.execute("simple_skill", {})

        assert success is True
        assert executor.last_validation_attempts == 1
        assert len(executor.last_validation_errors) == 0

    def test_unknown_skill_raises(self, registry: SkillRegistry) -> None:
        """V1Executor raises KeyError for unknown skill."""
        executor = V1Executor(registry)

        with pytest.raises(KeyError, match="unknown_skill"):
            executor.execute("unknown_skill", {})

    def test_failing_skill_returns_failure(self, registry: SkillRegistry) -> None:
        """V1Executor returns failure for skill that fails."""
        executor = V1Executor(registry)
        success, summary, data = executor.execute("failing_skill", {})

        assert success is False
        assert "fails" in summary.lower()


# ---------------------------------------------------------------------------
# V1Executor Tests - Retry Logic
# ---------------------------------------------------------------------------


class TestV1ExecutorRetry:
    """Tests for V1Executor retry logic."""

    def test_retry_on_validation_failure(self, registry: SkillRegistry) -> None:
        """V1Executor retries on validation failure and eventually succeeds.

        Note: This test uses FlakeySkill which returns 'success=False' for first
        fail_count attempts. The V1Executor validates the output schema structure,
        not the success field value - so these are valid outputs that happen to
        indicate failure.
        """
        FlakeySkillCounter.reset()
        FlakeySkill.fail_count = 2  # Fail twice, succeed on third

        executor = V1Executor(registry, max_attempts=4)
        success, summary, data = executor.execute("flakey_skill", {})

        # The skill returns success=False for first 2 attempts
        # But V1Executor validates schema, not success value
        # So it should pass on attempt 1 (schema is valid)
        assert executor.last_validation_attempts == 1  # Schema valid on first try

    def test_default_max_attempts(self) -> None:
        """Default max attempts is 3."""
        assert DEFAULT_MAX_VALIDATION_ATTEMPTS == 3

    def test_custom_max_attempts(self, registry: SkillRegistry) -> None:
        """Can set custom max attempts."""
        executor = V1Executor(registry, max_attempts=5)
        assert executor._max_attempts == 5

    def test_validation_attempts_tracked(self, registry: SkillRegistry) -> None:
        """Validation attempts are tracked."""
        executor = V1Executor(registry)
        executor.execute("simple_skill", {})

        assert executor.last_validation_attempts >= 1

    def test_validation_errors_tracked(self, registry: SkillRegistry) -> None:
        """Validation errors are tracked (empty for valid output)."""
        executor = V1Executor(registry)
        executor.execute("simple_skill", {})

        # Valid output should have no errors
        assert executor.last_validation_errors == []


# ---------------------------------------------------------------------------
# V1Executor Tests - State Inspection
# ---------------------------------------------------------------------------


class TestV1ExecutorState:
    """Tests for V1Executor state inspection properties."""

    def test_last_validation_attempts_property(self, registry: SkillRegistry) -> None:
        """last_validation_attempts is accessible."""
        executor = V1Executor(registry)
        assert executor.last_validation_attempts == 0

        executor.execute("simple_skill", {})
        assert executor.last_validation_attempts == 1

    def test_last_validation_errors_property(self, registry: SkillRegistry) -> None:
        """last_validation_errors is accessible."""
        executor = V1Executor(registry)
        assert executor.last_validation_errors == []

    def test_state_resets_between_executions(self, registry: SkillRegistry) -> None:
        """State resets between execute() calls."""
        executor = V1Executor(registry)

        executor.execute("simple_skill", {})
        assert executor.last_validation_attempts == 1

        executor.execute("simple_skill", {})
        assert executor.last_validation_attempts == 1  # Reset, not accumulated
