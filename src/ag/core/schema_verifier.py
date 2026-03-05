"""Schema verifier with repair loop (AF-0050).

Implements JSON schema validation with automatic repair attempts,
recording all validation steps in RunTrace.

Loop Bounding (AF-0055):
    All validation loops are bounded by configurable limits to prevent
    unbounded retries. The default is DEFAULT_MAX_VALIDATION_ATTEMPTS (3).
    Bounds can be configured per-validator or per-call.

    Infinite retry scenarios are impossible:
    - max_attempts must be >= 1 (enforced in SchemaValidator.__init__)
    - Loop counter counts from 1 to max_attempts (inclusive)
    - No early exits that bypass the loop counter
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Callable
from uuid import uuid4

from pydantic import BaseModel, Field, ValidationError

from .run_trace import (
    EvidenceRef,
    RunTraceBuilder,
    Step,
    StepType,
    VerifierStatus,
)

# ---------------------------------------------------------------------------
# Constants (AF-0055: Loop bounding)
# ---------------------------------------------------------------------------

#: Default maximum validation attempts. Set conservatively to avoid
#: runaway retries while allowing reasonable repair attempts.
DEFAULT_MAX_VALIDATION_ATTEMPTS: int = 3

#: Absolute maximum allowed for max_attempts (safety ceiling).
#: Prevents misconfiguration from causing excessive retries.
MAX_VALIDATION_ATTEMPTS_CEILING: int = 10


class ValidationAttempt(BaseModel):
    """Record of a single validation attempt."""

    attempt_number: int = Field(..., ge=1, description="Attempt number (1-indexed)")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Attempt timestamp"
    )
    input_data: dict[str, Any] = Field(..., description="Data that was validated")
    is_valid: bool = Field(..., description="Whether validation passed")
    errors: list[str] = Field(default_factory=list, description="Validation error messages")
    repaired: bool = Field(default=False, description="Whether repair was attempted")
    repair_summary: str | None = Field(default=None, description="Summary of repair action")

    model_config = {"extra": "forbid"}


class ValidationResult(BaseModel):
    """Final result of validation loop."""

    success: bool = Field(..., description="Whether validation ultimately succeeded")
    validated_data: dict[str, Any] | None = Field(
        default=None, description="Final validated data (or None if failed)"
    )
    attempts: list[ValidationAttempt] = Field(
        default_factory=list, description="All validation attempts"
    )
    total_attempts: int = Field(..., ge=1, description="Total number of attempts made")
    final_errors: list[str] = Field(
        default_factory=list, description="Errors from final attempt (if failed)"
    )

    model_config = {"extra": "forbid"}


# Type alias for repair function
# Takes (data, errors) and returns (repaired_data, repair_summary)
RepairFn = Callable[[dict[str, Any], list[str]], tuple[dict[str, Any], str]]


class SchemaValidator:
    """Validates data against a Pydantic model with repair loop support.

    Loop bounding (AF-0055):
        - max_attempts defaults to DEFAULT_MAX_VALIDATION_ATTEMPTS (3)
        - max_attempts is capped at MAX_VALIDATION_ATTEMPTS_CEILING (10)
        - Loop is guaranteed to terminate after max_attempts iterations
    """

    def __init__(
        self,
        schema_model: type[BaseModel],
        max_attempts: int = DEFAULT_MAX_VALIDATION_ATTEMPTS,
    ) -> None:
        """Initialize validator.

        Args:
            schema_model: Pydantic model class to validate against
            max_attempts: Maximum validation attempts (including initial).
                          Default: DEFAULT_MAX_VALIDATION_ATTEMPTS (3).
                          Max: MAX_VALIDATION_ATTEMPTS_CEILING (10).

        Raises:
            TypeError: If schema_model is not a Pydantic BaseModel subclass.
            ValueError: If max_attempts < 1 or > MAX_VALIDATION_ATTEMPTS_CEILING.
        """
        if not isinstance(schema_model, type) or not issubclass(schema_model, BaseModel):
            raise TypeError("schema_model must be a Pydantic BaseModel subclass")
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if max_attempts > MAX_VALIDATION_ATTEMPTS_CEILING:
            raise ValueError(
                f"max_attempts cannot exceed {MAX_VALIDATION_ATTEMPTS_CEILING} (got {max_attempts})"
            )

        self._schema_model = schema_model
        self._max_attempts = max_attempts

    @property
    def schema_name(self) -> str:
        """Get the schema model name."""
        return self._schema_model.__name__

    @property
    def max_attempts(self) -> int:
        """Get maximum attempts."""
        return self._max_attempts

    def validate_once(self, data: dict[str, Any]) -> tuple[bool, list[str], BaseModel | None]:
        """Perform single validation attempt.

        Args:
            data: Data to validate

        Returns:
            Tuple of (is_valid, error_messages, validated_model_or_none)
        """
        try:
            validated = self._schema_model.model_validate(data)
            return True, [], validated
        except ValidationError as e:
            errors = [str(err["msg"]) for err in e.errors()]
            return False, errors, None

    def validate_with_repair(
        self,
        data: dict[str, Any],
        repair_fn: RepairFn | None = None,
    ) -> ValidationResult:
        """Validate data with optional repair loop.

        Args:
            data: Initial data to validate
            repair_fn: Optional function to repair invalid data.
                       Signature: (data, errors) -> (repaired_data, repair_summary)

        Returns:
            ValidationResult with all attempts recorded
        """
        attempts: list[ValidationAttempt] = []
        current_data = data
        final_errors: list[str] = []

        for attempt_num in range(1, self._max_attempts + 1):
            is_valid, errors, validated_model = self.validate_once(current_data)

            attempt = ValidationAttempt(
                attempt_number=attempt_num,
                input_data=current_data,
                is_valid=is_valid,
                errors=errors,
            )

            if is_valid:
                attempts.append(attempt)
                return ValidationResult(
                    success=True,
                    validated_data=validated_model.model_dump() if validated_model else None,
                    attempts=attempts,
                    total_attempts=attempt_num,
                )

            # Validation failed
            final_errors = errors

            # Try repair if we have attempts left and a repair function
            if attempt_num < self._max_attempts and repair_fn is not None:
                try:
                    repaired_data, repair_summary = repair_fn(current_data, errors)
                    attempt.repaired = True
                    attempt.repair_summary = repair_summary
                    current_data = repaired_data
                except Exception as e:
                    attempt.repair_summary = f"Repair failed: {e}"

            attempts.append(attempt)

        # All attempts exhausted
        return ValidationResult(
            success=False,
            validated_data=None,
            attempts=attempts,
            total_attempts=len(attempts),
            final_errors=final_errors,
        )


def record_validation_steps(
    builder: RunTraceBuilder,
    result: ValidationResult,
    schema_name: str,
) -> RunTraceBuilder:
    """Record validation attempts as VERIFICATION steps in RunTrace.

    Args:
        builder: RunTraceBuilder to add steps to
        result: ValidationResult with attempts to record
        schema_name: Name of the schema being validated

    Returns:
        Updated RunTraceBuilder
    """
    for attempt in result.attempts:
        error_msg = "; ".join(attempt.errors) if attempt.errors else None
        output_summary = "Valid" if attempt.is_valid else f"Invalid: {len(attempt.errors)} error(s)"
        if attempt.repaired:
            output_summary += f" → repaired: {attempt.repair_summary or 'no summary'}"

        # Create evidence ref for the validation attempt
        status_text = "passed" if attempt.is_valid else "failed"
        evidence = EvidenceRef(
            ref_id=str(uuid4()),
            source_type="validation",
            source_path=f"schema:{schema_name}",
            excerpt=f"Attempt {attempt.attempt_number}: {status_text}",
            relevance="Schema validation result",
            metadata={
                "attempt_number": attempt.attempt_number,
                "is_valid": attempt.is_valid,
                "error_count": len(attempt.errors),
            },
        )

        builder.add_step(
            step_type=StepType.VERIFICATION,
            input_summary=f"Validate against {schema_name} (attempt {attempt.attempt_number})",
            output_summary=output_summary,
            error=error_msg if not attempt.is_valid and not attempt.repaired else None,
            evidence_refs=[evidence],
        )

    return builder


def run_validation_loop(
    builder: RunTraceBuilder,
    data: dict[str, Any],
    schema_model: type[BaseModel],
    repair_fn: RepairFn | None = None,
    max_attempts: int = DEFAULT_MAX_VALIDATION_ATTEMPTS,
) -> tuple[ValidationResult, RunTraceBuilder]:
    """Run full validation loop with RunTrace recording.

    This is the main entry point for schema validation with repair loop.

    Loop bounding (AF-0055):
        - max_attempts defaults to DEFAULT_MAX_VALIDATION_ATTEMPTS (3)
        - max_attempts is capped at MAX_VALIDATION_ATTEMPTS_CEILING (10)
        - Retry count is recorded in verifier evidence for trace visibility

    Args:
        builder: RunTraceBuilder to record steps
        data: Data to validate
        schema_model: Pydantic model to validate against
        repair_fn: Optional repair function for failed validations
        max_attempts: Maximum validation attempts (capped at ceiling)

    Returns:
        Tuple of (ValidationResult, updated RunTraceBuilder)

    Example:
        >>> from pydantic import BaseModel
        >>> class Output(BaseModel):
        ...     answer: str
        ...     confidence: float
        >>>
        >>> result, builder = run_validation_loop(
        ...     builder=builder,
        ...     data={"answer": "42", "confidence": 0.9},
        ...     schema_model=Output,
        ... )
    """
    validator = SchemaValidator(schema_model, max_attempts=max_attempts)
    result = validator.validate_with_repair(data, repair_fn)

    # Record all attempts in the trace
    builder = record_validation_steps(builder, result, validator.schema_name)

    # Update verifier status based on result
    if result.success:
        builder.verify(
            VerifierStatus.PASSED,
            message=f"Schema validation passed after {result.total_attempts} attempt(s)",
            evidence={"schema": validator.schema_name, "attempts": result.total_attempts},
        )
    else:
        error_summary = "; ".join(result.final_errors)
        builder.verify(
            VerifierStatus.FAILED,
            message=(
                f"Schema validation failed after {result.total_attempts} "
                f"attempt(s): {error_summary}"
            ),
            evidence={
                "schema": validator.schema_name,
                "attempts": result.total_attempts,
                "errors": result.final_errors,
            },
        )

    return result, builder


def create_verification_step(
    attempt: ValidationAttempt,
    schema_name: str,
) -> Step:
    """Create a Step from a ValidationAttempt.

    Useful for adding verification steps to existing traces.

    Args:
        attempt: Validation attempt to convert
        schema_name: Name of the schema

    Returns:
        Step configured for verification
    """
    now = datetime.now(UTC)
    error_msg = "; ".join(attempt.errors) if attempt.errors else None
    output_summary = "Valid" if attempt.is_valid else f"Invalid: {len(attempt.errors)} error(s)"
    if attempt.repaired:
        output_summary += f" → repaired: {attempt.repair_summary or 'no summary'}"

    evidence = EvidenceRef(
        ref_id=str(uuid4()),
        source_type="validation",
        source_path=f"schema:{schema_name}",
        excerpt=f"Attempt {attempt.attempt_number}: {'passed' if attempt.is_valid else 'failed'}",
        relevance="Schema validation result",
        metadata={
            "attempt_number": attempt.attempt_number,
            "is_valid": attempt.is_valid,
            "error_count": len(attempt.errors),
        },
    )

    return Step(
        step_id=str(uuid4()),
        step_number=0,  # Caller should set this
        step_type=StepType.VERIFICATION,
        input_summary=f"Validate against {schema_name} (attempt {attempt.attempt_number})",
        output_summary=output_summary,
        started_at=attempt.timestamp,
        ended_at=now,
        error=error_msg if not attempt.is_valid and not attempt.repaired else None,
        evidence_refs=[evidence],
    )
