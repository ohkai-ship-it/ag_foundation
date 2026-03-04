"""Tests for schema verifier with repair loop (AF-0050)."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel, Field

from ag.core import (
    ExecutionMode,
    RunTraceBuilder,
    SchemaValidator,
    StepType,
    ValidationAttempt,
    ValidationResult,
    VerifierStatus,
    create_verification_step,
    record_validation_steps,
    run_validation_loop,
)

# ---------------------------------------------------------------------------
# Test schemas
# ---------------------------------------------------------------------------


class SimpleOutput(BaseModel):
    """Simple test schema."""

    answer: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)


class ComplexOutput(BaseModel):
    """More complex test schema with nested fields."""

    result: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    scores: list[float] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# ValidationAttempt tests
# ---------------------------------------------------------------------------


class TestValidationAttempt:
    """Tests for ValidationAttempt model."""

    def test_create_valid_attempt(self) -> None:
        """Test creating a validation attempt."""
        attempt = ValidationAttempt(
            attempt_number=1,
            input_data={"key": "value"},
            is_valid=True,
        )
        assert attempt.attempt_number == 1
        assert attempt.is_valid is True
        assert attempt.errors == []
        assert attempt.repaired is False

    def test_create_failed_attempt(self) -> None:
        """Test creating a failed attempt with errors."""
        attempt = ValidationAttempt(
            attempt_number=2,
            input_data={"bad": "data"},
            is_valid=False,
            errors=["Missing required field", "Invalid type"],
        )
        assert attempt.is_valid is False
        assert len(attempt.errors) == 2

    def test_repaired_attempt(self) -> None:
        """Test creating an attempt that was repaired."""
        attempt = ValidationAttempt(
            attempt_number=1,
            input_data={"fixed": "data"},
            is_valid=False,
            errors=["Error"],
            repaired=True,
            repair_summary="Fixed missing field",
        )
        assert attempt.repaired is True
        assert attempt.repair_summary == "Fixed missing field"

    def test_timestamp_default(self) -> None:
        """Test that timestamp is set by default."""
        attempt = ValidationAttempt(
            attempt_number=1,
            input_data={},
            is_valid=True,
        )
        assert attempt.timestamp is not None
        assert attempt.timestamp.tzinfo is not None

    def test_invalid_attempt_number(self) -> None:
        """Test that attempt_number must be >= 1."""
        with pytest.raises(ValueError):
            ValidationAttempt(
                attempt_number=0,
                input_data={},
                is_valid=True,
            )


# ---------------------------------------------------------------------------
# ValidationResult tests
# ---------------------------------------------------------------------------


class TestValidationResult:
    """Tests for ValidationResult model."""

    def test_successful_result(self) -> None:
        """Test creating a successful validation result."""
        result = ValidationResult(
            success=True,
            validated_data={"answer": "42", "confidence": 0.9},
            attempts=[
                ValidationAttempt(
                    attempt_number=1,
                    input_data={"answer": "42", "confidence": 0.9},
                    is_valid=True,
                )
            ],
            total_attempts=1,
        )
        assert result.success is True
        assert result.validated_data is not None
        assert result.total_attempts == 1

    def test_failed_result(self) -> None:
        """Test creating a failed validation result."""
        result = ValidationResult(
            success=False,
            validated_data=None,
            attempts=[
                ValidationAttempt(
                    attempt_number=1,
                    input_data={"bad": "data"},
                    is_valid=False,
                    errors=["Missing field"],
                )
            ],
            total_attempts=1,
            final_errors=["Missing field"],
        )
        assert result.success is False
        assert result.validated_data is None
        assert result.final_errors == ["Missing field"]


# ---------------------------------------------------------------------------
# SchemaValidator tests
# ---------------------------------------------------------------------------


class TestSchemaValidator:
    """Tests for SchemaValidator class."""

    def test_init_valid(self) -> None:
        """Test initializing validator with valid params."""
        validator = SchemaValidator(SimpleOutput)
        assert validator.schema_name == "SimpleOutput"
        assert validator.max_attempts == 3

    def test_init_custom_max_attempts(self) -> None:
        """Test initializing with custom max attempts."""
        validator = SchemaValidator(SimpleOutput, max_attempts=5)
        assert validator.max_attempts == 5

    def test_init_invalid_schema_type(self) -> None:
        """Test that non-BaseModel schema raises TypeError."""
        with pytest.raises(TypeError, match="must be a Pydantic BaseModel subclass"):
            SchemaValidator(dict)  # type: ignore

    def test_init_invalid_max_attempts(self) -> None:
        """Test that max_attempts < 1 raises ValueError."""
        with pytest.raises(ValueError, match="max_attempts must be at least 1"):
            SchemaValidator(SimpleOutput, max_attempts=0)

    def test_validate_once_success(self) -> None:
        """Test single validation that passes."""
        validator = SchemaValidator(SimpleOutput)
        is_valid, errors, model = validator.validate_once({"answer": "42", "confidence": 0.9})
        assert is_valid is True
        assert errors == []
        assert model is not None
        assert model.answer == "42"

    def test_validate_once_failure(self) -> None:
        """Test single validation that fails."""
        validator = SchemaValidator(SimpleOutput)
        is_valid, errors, model = validator.validate_once(
            {"answer": "", "confidence": 2.0}  # Both fields invalid
        )
        assert is_valid is False
        assert len(errors) >= 1
        assert model is None

    def test_validate_once_missing_field(self) -> None:
        """Test validation with missing required field."""
        validator = SchemaValidator(SimpleOutput)
        is_valid, errors, model = validator.validate_once({"answer": "42"})
        assert is_valid is False
        assert model is None

    def test_validate_with_repair_immediate_success(self) -> None:
        """Test validation that passes on first attempt."""
        validator = SchemaValidator(SimpleOutput)
        result = validator.validate_with_repair({"answer": "42", "confidence": 0.9})
        assert result.success is True
        assert result.total_attempts == 1
        assert len(result.attempts) == 1

    def test_validate_with_repair_no_repair_fn(self) -> None:
        """Test validation failure without repair function."""
        validator = SchemaValidator(SimpleOutput, max_attempts=3)
        result = validator.validate_with_repair(
            {"answer": "", "confidence": 0.5}  # Invalid: empty answer
        )
        assert result.success is False
        # Without repair, should only try once (can't repair)
        assert result.total_attempts == 3
        assert len(result.final_errors) >= 1

    def test_validate_with_repair_success_on_retry(self) -> None:
        """Test validation that succeeds after repair."""
        validator = SchemaValidator(SimpleOutput, max_attempts=3)

        # Repair function that fixes the data
        def repair_fn(data: dict, errors: list[str]) -> tuple[dict, str]:
            fixed = data.copy()
            if not fixed.get("answer"):
                fixed["answer"] = "fixed"
            if "confidence" not in fixed:
                fixed["confidence"] = 0.5
            return fixed, "Added missing fields"

        result = validator.validate_with_repair(
            {"answer": "", "confidence": 0.5},  # Invalid: empty answer
            repair_fn=repair_fn,
        )
        assert result.success is True
        assert result.total_attempts == 2
        # First attempt should be marked as repaired
        assert result.attempts[0].repaired is True

    def test_validate_with_repair_exhausted_attempts(self) -> None:
        """Test validation that fails after all repair attempts."""
        validator = SchemaValidator(SimpleOutput, max_attempts=2)

        # Repair function that doesn't actually fix anything
        call_count = 0

        def bad_repair_fn(data: dict, errors: list[str]) -> tuple[dict, str]:
            nonlocal call_count
            call_count += 1
            return data, f"Repair attempt {call_count}"

        result = validator.validate_with_repair(
            {"answer": "", "confidence": 0.5},
            repair_fn=bad_repair_fn,
        )
        assert result.success is False
        assert result.total_attempts == 2
        assert call_count == 1  # Called once between attempt 1 and 2

    def test_validate_with_repair_fn_exception(self) -> None:
        """Test that repair function exceptions are handled."""
        validator = SchemaValidator(SimpleOutput, max_attempts=3)

        def failing_repair_fn(data: dict, errors: list[str]) -> tuple[dict, str]:
            raise RuntimeError("Repair failed!")

        result = validator.validate_with_repair(
            {"answer": "", "confidence": 0.5},
            repair_fn=failing_repair_fn,
        )
        assert result.success is False
        # Check that repair failure was recorded
        assert "Repair failed" in (result.attempts[0].repair_summary or "")


# ---------------------------------------------------------------------------
# record_validation_steps tests
# ---------------------------------------------------------------------------


class TestRecordValidationSteps:
    """Tests for record_validation_steps function."""

    def _create_builder(self) -> RunTraceBuilder:
        """Create a test builder."""
        return RunTraceBuilder(
            workspace_id="test-ws",
            mode=ExecutionMode.MANUAL,
            playbook_name="test",
            playbook_version="1.0",
        )

    def test_record_single_successful_attempt(self) -> None:
        """Test recording a single successful validation."""
        builder = self._create_builder()
        result = ValidationResult(
            success=True,
            validated_data={"answer": "42", "confidence": 0.9},
            attempts=[
                ValidationAttempt(
                    attempt_number=1,
                    input_data={"answer": "42", "confidence": 0.9},
                    is_valid=True,
                )
            ],
            total_attempts=1,
        )

        record_validation_steps(builder, result, "SimpleOutput")
        trace = builder.build()

        assert len(trace.steps) == 1
        step = trace.steps[0]
        assert step.step_type == StepType.VERIFICATION
        assert "SimpleOutput" in step.input_summary
        assert "Valid" in step.output_summary
        assert step.error is None

    def test_record_multiple_attempts(self) -> None:
        """Test recording multiple validation attempts."""
        builder = self._create_builder()
        result = ValidationResult(
            success=True,
            validated_data={"answer": "fixed", "confidence": 0.9},
            attempts=[
                ValidationAttempt(
                    attempt_number=1,
                    input_data={"answer": "", "confidence": 0.9},
                    is_valid=False,
                    errors=["String should have at least 1 character"],
                    repaired=True,
                    repair_summary="Fixed empty answer",
                ),
                ValidationAttempt(
                    attempt_number=2,
                    input_data={"answer": "fixed", "confidence": 0.9},
                    is_valid=True,
                ),
            ],
            total_attempts=2,
        )

        record_validation_steps(builder, result, "SimpleOutput")
        trace = builder.build()

        assert len(trace.steps) == 2
        # First step should show failure and repair
        assert "Invalid" in trace.steps[0].output_summary
        assert "repaired" in trace.steps[0].output_summary
        # Second step should show success
        assert "Valid" in trace.steps[1].output_summary

    def test_record_evidence_refs(self) -> None:
        """Test that evidence refs are properly attached."""
        builder = self._create_builder()
        result = ValidationResult(
            success=True,
            validated_data={"answer": "42", "confidence": 0.9},
            attempts=[
                ValidationAttempt(
                    attempt_number=1,
                    input_data={"answer": "42", "confidence": 0.9},
                    is_valid=True,
                )
            ],
            total_attempts=1,
        )

        record_validation_steps(builder, result, "SimpleOutput")
        trace = builder.build()

        step = trace.steps[0]
        assert step.evidence_refs is not None
        assert len(step.evidence_refs) == 1
        ref = step.evidence_refs[0]
        assert ref.source_type == "validation"
        assert "SimpleOutput" in ref.source_path


# ---------------------------------------------------------------------------
# run_validation_loop tests
# ---------------------------------------------------------------------------


class TestRunValidationLoop:
    """Tests for run_validation_loop function."""

    def _create_builder(self) -> RunTraceBuilder:
        """Create a test builder."""
        return RunTraceBuilder(
            workspace_id="test-ws",
            mode=ExecutionMode.MANUAL,
            playbook_name="test",
            playbook_version="1.0",
        )

    def test_successful_validation(self) -> None:
        """Test full validation loop with success."""
        builder = self._create_builder()
        result, updated_builder = run_validation_loop(
            builder=builder,
            data={"answer": "42", "confidence": 0.9},
            schema_model=SimpleOutput,
        )

        assert result.success is True
        trace = updated_builder.build()

        # Check verifier was set to PASSED
        assert trace.verifier.status == VerifierStatus.PASSED
        assert "passed" in trace.verifier.message.lower()

    def test_failed_validation_updates_verifier(self) -> None:
        """Test that failed validation sets verifier to FAILED."""
        builder = self._create_builder()
        result, updated_builder = run_validation_loop(
            builder=builder,
            data={"answer": "", "confidence": 2.0},  # Invalid
            schema_model=SimpleOutput,
            max_attempts=1,
        )

        assert result.success is False
        trace = updated_builder.build()

        assert trace.verifier.status == VerifierStatus.FAILED
        assert "failed" in trace.verifier.message.lower()

    def test_validation_with_repair(self) -> None:
        """Test validation loop with repair function."""
        builder = self._create_builder()

        def repair_fn(data: dict, errors: list[str]) -> tuple[dict, str]:
            fixed = data.copy()
            fixed["answer"] = "repaired"
            fixed["confidence"] = 0.5
            return fixed, "Applied default values"

        result, updated_builder = run_validation_loop(
            builder=builder,
            data={"answer": "", "confidence": 2.0},  # Both invalid
            schema_model=SimpleOutput,
            repair_fn=repair_fn,
            max_attempts=3,
        )

        assert result.success is True
        assert result.validated_data["answer"] == "repaired"

    def test_custom_max_attempts(self) -> None:
        """Test validation loop with custom max attempts."""
        builder = self._create_builder()
        result, _ = run_validation_loop(
            builder=builder,
            data={"bad": "data"},
            schema_model=SimpleOutput,
            max_attempts=5,
        )

        assert result.success is False
        assert result.total_attempts == 5


# ---------------------------------------------------------------------------
# create_verification_step tests
# ---------------------------------------------------------------------------


class TestCreateVerificationStep:
    """Tests for create_verification_step function."""

    def test_create_step_from_successful_attempt(self) -> None:
        """Test creating a step from a successful attempt."""
        attempt = ValidationAttempt(
            attempt_number=1,
            input_data={"answer": "42", "confidence": 0.9},
            is_valid=True,
        )

        step = create_verification_step(attempt, "SimpleOutput")

        assert step.step_type == StepType.VERIFICATION
        assert "SimpleOutput" in step.input_summary
        assert "attempt 1" in step.input_summary
        assert step.output_summary == "Valid"
        assert step.error is None

    def test_create_step_from_failed_attempt(self) -> None:
        """Test creating a step from a failed attempt."""
        attempt = ValidationAttempt(
            attempt_number=2,
            input_data={"bad": "data"},
            is_valid=False,
            errors=["Missing field 'answer'", "Missing field 'confidence'"],
        )

        step = create_verification_step(attempt, "SimpleOutput")

        assert step.step_type == StepType.VERIFICATION
        assert "Invalid: 2 error(s)" in step.output_summary
        assert step.error is not None
        assert "Missing field" in step.error

    def test_create_step_from_repaired_attempt(self) -> None:
        """Test creating a step from a repaired attempt."""
        attempt = ValidationAttempt(
            attempt_number=1,
            input_data={"answer": ""},
            is_valid=False,
            errors=["Empty answer"],
            repaired=True,
            repair_summary="Added default answer",
        )

        step = create_verification_step(attempt, "SimpleOutput")

        # Repaired attempts should not have error (since repair was attempted)
        assert step.error is None
        assert "repaired" in step.output_summary
        assert "Added default answer" in step.output_summary

    def test_step_has_evidence_refs(self) -> None:
        """Test that created step has evidence refs."""
        attempt = ValidationAttempt(
            attempt_number=1,
            input_data={},
            is_valid=True,
        )

        step = create_verification_step(attempt, "TestSchema")

        assert step.evidence_refs is not None
        assert len(step.evidence_refs) == 1
        assert step.evidence_refs[0].source_type == "validation"
        assert "TestSchema" in step.evidence_refs[0].source_path


# ---------------------------------------------------------------------------
# Contract tests for schema stability
# ---------------------------------------------------------------------------


class TestSchemaVerifierContracts:
    """Contract tests to ensure schema stability."""

    def test_validation_attempt_required_fields(self) -> None:
        """Test that ValidationAttempt has required fields."""
        required_fields = {"attempt_number", "input_data", "is_valid"}
        schema = ValidationAttempt.model_json_schema()
        assert required_fields.issubset(set(schema.get("required", [])))

    def test_validation_result_required_fields(self) -> None:
        """Test that ValidationResult has required fields."""
        required_fields = {"success", "total_attempts"}
        schema = ValidationResult.model_json_schema()
        assert required_fields.issubset(set(schema.get("required", [])))

    def test_validation_attempt_forbids_extra(self) -> None:
        """Test that ValidationAttempt forbids extra fields."""
        with pytest.raises(ValueError):
            ValidationAttempt(
                attempt_number=1,
                input_data={},
                is_valid=True,
                extra_field="not allowed",  # type: ignore
            )

    def test_validation_result_forbids_extra(self) -> None:
        """Test that ValidationResult forbids extra fields."""
        with pytest.raises(ValueError):
            ValidationResult(
                success=True,
                total_attempts=1,
                extra_field="not allowed",  # type: ignore
            )
