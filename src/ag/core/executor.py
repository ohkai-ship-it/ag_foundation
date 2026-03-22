"""V0, V1, and V2 Executor implementations.

Extracted from runtime.py (AF-0114).
V1Executor adds output schema validation with retry (AF-0116).
V2Executor adds LLM output repair after retry exhaustion (AF-0124).
"""

from __future__ import annotations

import json
import logging
import time
from typing import TYPE_CHECKING, Any

from pydantic import ValidationError

from ag.skills import SkillContext, SkillRegistry, get_default_registry
from ag.skills.base import SkillOutput

if TYPE_CHECKING:
    from ag.core.run_trace import ExecutionMetadata
    from ag.providers.base import LLMProvider

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
                logger.debug(f"Skill '{skill_name}' output validated on attempt {attempt}")
                return output.to_legacy_tuple()

            # Log validation failure
            error_msg = f"Output validation failed: {'; '.join(errors)}"
            self._last_validation_errors.append(f"Attempt {attempt}: {error_msg}")
            logger.warning(
                f"Skill '{skill_name}' output validation failed "
                f"(attempt {attempt}/{self._max_attempts}): {errors}"
            )

            if attempt < self._max_attempts:
                logger.info(f"Retrying skill '{skill_name}'...")
                continue

        # All attempts exhausted
        final_msg = (
            f"Output validation failed after {self._max_attempts} attempts for '{skill_name}'"
        )
        logger.error(final_msg)
        return (
            False,
            final_msg,
            {
                "error": "output_validation_failed",
                "attempts": self._last_validation_attempts,
                "errors": self._last_validation_errors,
            },
        )

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


class V2Executor(V1Executor):
    """V2 Executor: adds LLM output repair after retry exhaustion (AF-0124).

    Flow: validate → fail → retry skill → fail → LLM repair → validate → result.
    Graceful degradation: provider=None behaves identically to V1Executor.
    """

    def __init__(
        self,
        registry: SkillRegistry | None = None,
        provider: LLMProvider | None = None,
        max_attempts: int = DEFAULT_MAX_VALIDATION_ATTEMPTS,
    ) -> None:
        super().__init__(registry, max_attempts=max_attempts)
        self._provider = provider
        self._last_repair_result: dict[str, Any] | None = None
        self._repair_history: list[dict[str, Any]] = []  # AF-0126: track all repairs

    def execute(
        self,
        skill_name: str,
        parameters: dict[str, Any],
        context: SkillContext | None = None,
    ) -> tuple[bool, str, dict[str, Any]]:
        """Execute a skill with V1 retry, then LLM repair on exhaustion."""
        self._last_repair_result = None

        # V1 execution with retry
        success, summary, result = super().execute(skill_name, parameters, context)
        if success or self._provider is None:
            return success, summary, result

        # V1 failed after all retries — attempt LLM repair on last output
        repair_result = self._attempt_repair(skill_name, result)

        # AF-0126: record repair in history
        step_num = context.step_number if context else len(self._repair_history)
        if self._last_repair_result:
            self._repair_history.append(
                {"step_number": step_num, "skill_name": skill_name, **self._last_repair_result}
            )

        return repair_result

    def _attempt_repair(
        self,
        skill_name: str,
        last_result: dict[str, Any],
    ) -> tuple[bool, str, dict[str, Any]]:
        """Attempt LLM repair on the last failed output."""
        from ag.providers.base import ChatMessage, MessageRole

        skill_info = self._registry.get_skill(skill_name)
        if skill_info is None:
            return False, f"Skill not found: {skill_name}", last_result

        # Need the schema to guide repair
        output_schema = skill_info.output_schema
        try:
            schema_dict = output_schema.model_json_schema()
        except Exception:
            logger.debug(f"Cannot get schema for '{skill_name}', skipping repair")
            return False, "Cannot extract schema for repair", last_result

        # Build repair prompt
        errors = self._last_validation_errors
        repair_payload = {
            "output": last_result,
            "schema": schema_dict,
            "errors": errors,
        }

        messages = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content=(
                    "Fix the JSON to match the schema. Only fix the failing fields. "
                    "Return ONLY valid JSON, no explanations."
                ),
            ),
            ChatMessage(
                role=MessageRole.USER,
                content=json.dumps(repair_payload, default=str),
            ),
        ]

        start_ms = time.monotonic_ns() // 1_000_000
        try:
            response = self._provider.chat(messages=messages)
        except Exception as exc:
            logger.debug(f"LLM repair call failed for '{skill_name}': {exc}")
            self._last_repair_result = {
                "repair_attempted": True,
                "repair_succeeded": False,
                "error": str(exc),
            }
            return (
                False,
                f"LLM repair failed: {exc}",
                {**last_result, "repair_result": self._last_repair_result},
            )
        elapsed_ms = (time.monotonic_ns() // 1_000_000) - start_ms

        # Parse repaired output
        try:
            repaired = json.loads(response.content)
        except (json.JSONDecodeError, TypeError) as exc:
            logger.debug(f"LLM repair returned invalid JSON for '{skill_name}': {exc}")
            self._last_repair_result = {
                "repair_attempted": True,
                "repair_succeeded": False,
                "repair_model": getattr(response, "model", ""),
                "repair_tokens": getattr(response, "tokens_used", 0) or 0,
                "repair_ms": elapsed_ms,
                "error": f"Invalid JSON: {exc}",
            }
            return (
                False,
                f"LLM repair returned invalid JSON: {exc}",
                {**last_result, "repair_result": self._last_repair_result},
            )

        # Validate repaired output against schema
        try:
            validated = output_schema.model_validate(repaired)
        except ValidationError as exc:
            error_msgs = [str(e["msg"]) for e in exc.errors()]
            logger.debug(f"LLM-repaired output still invalid for '{skill_name}': {error_msgs}")
            self._last_repair_result = {
                "repair_attempted": True,
                "repair_succeeded": False,
                "repair_model": getattr(response, "model", ""),
                "repair_tokens": getattr(response, "tokens_used", 0) or 0,
                "repair_ms": elapsed_ms,
                "repaired_output": repaired,
                "post_repair_errors": error_msgs,
            }
            return (
                False,
                f"LLM repair output still invalid: {'; '.join(error_msgs)}",
                {**last_result, "repair_result": self._last_repair_result},
            )

        # Repair succeeded
        fields_changed = [
            k for k in repaired if k not in last_result or repaired[k] != last_result.get(k)
        ]
        self._last_repair_result = {
            "repair_attempted": True,
            "repair_succeeded": True,
            "fields_changed": fields_changed,
            "repair_model": getattr(response, "model", ""),
            "repair_tokens": getattr(response, "tokens_used", 0) or 0,
            "repair_ms": elapsed_ms,
        }
        logger.info(
            f"LLM repair succeeded for '{skill_name}': {len(fields_changed)} fields changed"
        )
        return validated.to_legacy_tuple()

    @property
    def last_repair_result(self) -> dict[str, Any] | None:
        """Repair result from the last execute() call, or None if no repair attempted."""
        return self._last_repair_result

    def get_execution_metadata(self) -> "ExecutionMetadata | None":
        """Aggregate repair history into ExecutionMetadata (AF-0126).

        Returns None if no repairs were attempted during this executor's lifetime.
        """
        if not self._repair_history:
            return None

        from ag.core.run_trace import ExecutionMetadata, RepairSummary

        repairs = []
        for entry in self._repair_history:
            repairs.append(
                RepairSummary(
                    step_number=entry.get("step_number", 0),
                    skill_name=entry.get("skill_name", ""),
                    repair_attempted=entry.get("repair_attempted", True),
                    repair_succeeded=entry.get("repair_succeeded", False),
                    repair_tokens=entry.get("repair_tokens", 0),
                    repair_ms=entry.get("repair_ms", 0),
                    repair_model=entry.get("repair_model", ""),
                )
            )

        return ExecutionMetadata(
            total_repair_attempts=len(repairs),
            total_repair_successes=sum(1 for r in repairs if r.repair_succeeded),
            total_repair_tokens=sum(r.repair_tokens for r in repairs),
            repairs=repairs,
        )
