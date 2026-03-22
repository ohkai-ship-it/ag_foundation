"""V0 and V1 Executor implementations.

Extracted from runtime.py (AF-0114).
V1Executor adds output schema validation with retry (AF-0116).
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import ValidationError

from ag.skills import SkillContext, SkillRegistry, get_default_registry
from ag.skills.base import SkillOutput

logger = logging.getLogger(__name__)

# Default max attempts for output validation (AF-0116)
# 3 total: 1 initial + 2 retries
DEFAULT_MAX_VALIDATION_ATTEMPTS = 3


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


class V1Executor(V0Executor):
    """V1 Executor: adds output schema validation with bounded retry (AF-0116).

    After each skill execution, validates the output against the skill's
    declared output_schema. If invalid, retries up to max_attempts times.
    """

    def __init__(
        self,
        registry: SkillRegistry | None = None,
        max_attempts: int = DEFAULT_MAX_VALIDATION_ATTEMPTS,
    ) -> None:
        super().__init__(registry)
        self._max_attempts = max_attempts
        self._last_validation_attempts: int = 0
        self._last_validation_errors: list[str] = []

    def execute(
        self,
        skill_name: str,
        parameters: dict[str, Any],
        context: SkillContext | None = None,
    ) -> tuple[bool, str, dict[str, Any]]:
        """Execute a skill with output validation and retry.

        Args:
            skill_name: Name of the skill to execute
            parameters: Skill parameters
            context: Optional SkillContext

        Returns:
            Tuple of (success, output_summary, result_data)
        """
        if not self._registry.has(skill_name):
            raise KeyError(f"Skill not found: {skill_name}")

        skill_info = self._registry.get_skill(skill_name)
        if skill_info is None:
            raise KeyError(f"Skill not found: {skill_name}")

        output_schema = skill_info.output_schema
        self._last_validation_attempts = 0
        self._last_validation_errors = []

        for attempt in range(1, self._max_attempts + 1):
            self._last_validation_attempts = attempt

            # Execute skill and get raw output
            try:
                output = self._registry.execute_raw(skill_name, parameters, context)
            except (ValueError, RuntimeError) as e:
                # Input validation or execution failed - no retry
                error_msg = str(e)
                self._last_validation_errors.append(f"Attempt {attempt}: {error_msg}")
                return False, error_msg, {"error": error_msg}

            # Validate output against schema
            is_valid, errors = self._validate_output(output, output_schema)

            if is_valid:
                logger.debug(
                    f"Skill '{skill_name}' output validated on attempt {attempt}"
                )
                return output.to_legacy_tuple()

            # Log validation failure
            error_msg = f"Output validation failed: {'; '.join(errors)}"
            self._last_validation_errors.append(f"Attempt {attempt}: {error_msg}")
            logger.warning(
                f"Skill '{skill_name}' output validation failed (attempt {attempt}/{self._max_attempts}): {errors}"
            )

            if attempt < self._max_attempts:
                logger.info(f"Retrying skill '{skill_name}'...")
                continue

        # All attempts exhausted
        final_msg = (
            f"Output validation failed after {self._max_attempts} attempts for '{skill_name}'"
        )
        logger.error(final_msg)
        return False, final_msg, {
            "error": "output_validation_failed",
            "attempts": self._last_validation_attempts,
            "errors": self._last_validation_errors,
        }

    def _validate_output(
        self, output: SkillOutput, schema: type[SkillOutput]
    ) -> tuple[bool, list[str]]:
        """Validate output against its declared schema.

        Args:
            output: The SkillOutput instance to validate
            schema: The expected output schema class

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors: list[str] = []

        # Check type match
        if not isinstance(output, schema):
            # Try to re-validate the output data through the schema
            try:
                schema.model_validate(output.model_dump())
                return True, []
            except ValidationError as e:
                for error in e.errors():
                    loc = ".".join(str(x) for x in error["loc"])
                    errors.append(f"{loc}: {error['msg']}")
                return False, errors

        # Output is already the correct type, validate its data
        try:
            # Re-validate to catch any schema violations
            schema.model_validate(output.model_dump())
            return True, []
        except ValidationError as e:
            for error in e.errors():
                loc = ".".join(str(x) for x in error["loc"])
                errors.append(f"{loc}: {error['msg']}")
            return False, errors

    @property
    def last_validation_attempts(self) -> int:
        """Number of attempts in the last execute() call."""
        return self._last_validation_attempts

    @property
    def last_validation_errors(self) -> list[str]:
        """Validation errors from the last execute() call."""
        return self._last_validation_errors
