"""Contract tests for v0.1 schemas: TaskSpec, RunTrace, Playbook.

These tests enforce:
1. JSON round-trip stability
2. Version fields present and correct  
3. Additive evolution guardrails (required fields)
4. Stable defaults
"""

from datetime import UTC, datetime, timedelta

import pytest

from ag.core import (
    Artifact,
    Budgets,
    Constraints,
    ExecutionMode,
    FinalStatus,
    Playbook,
    PlaybookBuilder,
    PlaybookMetadata,
    PlaybookStep,
    PlaybookStepType,
    ReasoningMode,
    RunTrace,
    RunTraceBuilder,
    Step,
    StepType,
    TaskSpec,
    TaskSpecBuilder,
    Verifier,
    VerifierStatus,
)


# ===========================================================================
# TaskSpec v0.1 Contract Tests
# ===========================================================================


class TestTaskSpecContract:
    """Contract tests for TaskSpec v0.1."""

    def test_version_field_present(self) -> None:
        """Version field must exist with correct default."""
        spec = TaskSpec(prompt="test", workspace_id="ws-1")
        assert spec.task_spec_version == "0.1"

    def test_required_fields(self) -> None:
        """Required fields: prompt, workspace_id."""
        # Missing prompt
        with pytest.raises(Exception):
            TaskSpec(workspace_id="ws-1")  # type: ignore
        # Missing workspace_id
        with pytest.raises(Exception):
            TaskSpec(prompt="test")  # type: ignore

    def test_json_roundtrip(self) -> None:
        """JSON serialization must be lossless."""
        spec = TaskSpec(
            prompt="Build a feature",
            workspace_id="ws-123",
            mode=ExecutionMode.SUPERVISED,
            playbook_preference="default",
            budgets=Budgets(max_steps=10, max_tokens=5000),
            constraints=Constraints(blocked_skills=["shell"]),
        )
        json_str = spec.to_json()
        restored = TaskSpec.from_json(json_str)
        assert restored == spec

    def test_stable_defaults(self) -> None:
        """Default values must be stable across versions."""
        spec = TaskSpec(prompt="test", workspace_id="ws-1")
        assert spec.mode == ExecutionMode.MANUAL
        assert spec.playbook_preference is None
        assert spec.budgets.max_steps is None
        assert spec.budgets.max_tokens is None
        assert spec.budgets.max_duration_seconds is None
        assert spec.constraints.allowed_skills is None
        assert spec.constraints.blocked_skills is None

    def test_builder_produces_valid_spec(self) -> None:
        """Builder must produce valid TaskSpec."""
        spec = (
            TaskSpecBuilder("Do task", "ws-1")
            .mode(ExecutionMode.AUTONOMOUS)
            .playbook_preference("fast")
            .budgets(max_steps=5)
            .constraints(blocked_skills=["deploy"])
            .build()
        )
        assert spec.prompt == "Do task"
        assert spec.workspace_id == "ws-1"
        assert spec.mode == ExecutionMode.AUTONOMOUS
        assert spec.playbook_preference == "fast"
        assert spec.budgets.max_steps == 5
        assert spec.constraints.blocked_skills == ["deploy"]


class TestTaskSpecAdditiveEvolution:
    """Guardrail tests: v0.1 fields must remain additive-only."""

    # These fields MUST exist in v0.1 - removal would break contract
    REQUIRED_FIELDS_V01 = {
        "task_spec_version",
        "prompt",
        "workspace_id",
        "mode",
        "playbook_preference",
        "budgets",
        "constraints",
    }

    def test_all_v01_fields_present(self) -> None:
        """All v0.1 contract fields must be present in schema."""
        field_names = set(TaskSpec.model_fields.keys())
        missing = self.REQUIRED_FIELDS_V01 - field_names
        assert not missing, f"Missing v0.1 fields: {missing}"


# ===========================================================================
# RunTrace v0.1 Contract Tests
# ===========================================================================


class TestRunTraceContract:
    """Contract tests for RunTrace v0.1."""

    def test_version_field_present(self) -> None:
        """Version field must exist with correct default."""
        trace = RunTrace(
            workspace_id="ws-1",
            mode=ExecutionMode.MANUAL,
            playbook=PlaybookMetadata(name="default", version="1.0"),
            started_at=datetime.now(UTC),
            verifier=Verifier(status=VerifierStatus.PENDING),
            final=FinalStatus.SUCCESS,
        )
        assert trace.trace_version == "0.1"

    def test_required_fields(self) -> None:
        """Required fields must be validated."""
        # Missing workspace_id, mode, playbook, started_at, verifier, final
        with pytest.raises(Exception):
            RunTrace()  # type: ignore

    def test_json_roundtrip(self) -> None:
        """JSON serialization must be lossless."""
        now = datetime.now(UTC)
        trace = RunTrace(
            workspace_id="ws-123",
            mode=ExecutionMode.SUPERVISED,
            playbook=PlaybookMetadata(name="fast", version="2.0"),
            started_at=now,
            ended_at=now + timedelta(seconds=10),
            duration_ms=10000,
            steps=[
                Step(
                    step_id="step-1",
                    step_number=0,
                    step_type=StepType.SKILL_CALL,
                    skill_name="read_file",
                    started_at=now,
                    ended_at=now + timedelta(seconds=1),
                    duration_ms=1000,
                )
            ],
            artifacts=[
                Artifact(
                    artifact_id="art-1",
                    path="/output/file.txt",
                    artifact_type="text/plain",
                    size_bytes=100,
                )
            ],
            verifier=Verifier(
                status=VerifierStatus.PASSED,
                message="All checks passed",
                checked_at=now,
            ),
            final=FinalStatus.SUCCESS,
        )
        json_str = trace.to_json()
        restored = RunTrace.from_json(json_str)
        assert restored.workspace_id == trace.workspace_id
        assert restored.mode == trace.mode
        assert restored.playbook.name == trace.playbook.name
        assert len(restored.steps) == len(trace.steps)
        assert len(restored.artifacts) == len(trace.artifacts)
        assert restored.verifier.status == trace.verifier.status
        assert restored.final == trace.final

    def test_stable_defaults(self) -> None:
        """Default values must be stable."""
        trace = RunTrace(
            workspace_id="ws-1",
            mode=ExecutionMode.MANUAL,
            playbook=PlaybookMetadata(name="default", version="1.0"),
            started_at=datetime.now(UTC),
            verifier=Verifier(status=VerifierStatus.PENDING),
            final=FinalStatus.SUCCESS,
        )
        assert trace.steps == []
        assert trace.artifacts == []
        assert trace.error is None
        assert trace.metadata == {}

    def test_builder_produces_valid_trace(self) -> None:
        """Builder must produce valid RunTrace."""
        trace = (
            RunTraceBuilder("ws-1", ExecutionMode.MANUAL, "default", "1.0")
            .add_step(StepType.SKILL_CALL, skill_name="read_file", duration_ms=100)
            .add_artifact("/out/result.txt", "text/plain", size_bytes=50)
            .verify(VerifierStatus.PASSED, message="OK")
            .complete(FinalStatus.SUCCESS)
            .build()
        )
        assert trace.workspace_id == "ws-1"
        assert len(trace.steps) == 1
        assert len(trace.artifacts) == 1
        assert trace.verifier.status == VerifierStatus.PASSED
        assert trace.final == FinalStatus.SUCCESS


class TestRunTraceAdditiveEvolution:
    """Guardrail tests: v0.1 fields must remain additive-only."""

    REQUIRED_FIELDS_V01 = {
        "trace_version",
        "run_id",
        "workspace_id",
        "mode",
        "playbook",
        "started_at",
        "ended_at",
        "duration_ms",
        "steps",
        "artifacts",
        "verifier",
        "final",
        "error",
        "metadata",
    }

    def test_all_v01_fields_present(self) -> None:
        """All v0.1 contract fields must be present in schema."""
        field_names = set(RunTrace.model_fields.keys())
        missing = self.REQUIRED_FIELDS_V01 - field_names
        assert not missing, f"Missing v0.1 fields: {missing}"


# ===========================================================================
# Playbook v0.1 Contract Tests
# ===========================================================================


class TestPlaybookContract:
    """Contract tests for Playbook v0.1."""

    def test_version_field_present(self) -> None:
        """Version field must exist with correct default."""
        playbook = Playbook(name="default", version="1.0")
        assert playbook.playbook_version == "0.1"

    def test_required_fields(self) -> None:
        """Required fields: name, version."""
        with pytest.raises(Exception):
            Playbook(version="1.0")  # type: ignore
        with pytest.raises(Exception):
            Playbook(name="default")  # type: ignore

    def test_json_roundtrip(self) -> None:
        """JSON serialization must be lossless."""
        playbook = Playbook(
            name="build-feature",
            version="1.0",
            description="Standard feature workflow",
            reasoning_modes=[ReasoningMode.CHAIN_OF_THOUGHT, ReasoningMode.REFLECTION],
            budgets=Budgets(max_steps=20),
            steps=[
                PlaybookStep(
                    step_id="step_0",
                    name="Analyze",
                    step_type=PlaybookStepType.SKILL,
                    skill_name="analyze_code",
                )
            ],
        )
        json_str = playbook.to_json()
        restored = Playbook.from_json(json_str)
        assert restored == playbook

    def test_stable_defaults(self) -> None:
        """Default values must be stable."""
        playbook = Playbook(name="test", version="1.0")
        assert playbook.description == ""
        assert playbook.reasoning_modes == [ReasoningMode.DIRECT]
        assert playbook.budgets.max_steps is None
        assert playbook.steps == []
        assert playbook.metadata == {}

    def test_builder_produces_valid_playbook(self) -> None:
        """Builder must produce valid Playbook."""
        playbook = (
            PlaybookBuilder("fast-path", "1.0")
            .description("Quick execution")
            .reasoning_modes([ReasoningMode.DIRECT])
            .budgets(max_steps=5)
            .add_step("Read", skill_name="read_file")
            .add_step("Write", skill_name="write_file")
            .build()
        )
        assert playbook.name == "fast-path"
        assert playbook.version == "1.0"
        assert len(playbook.steps) == 2
        assert playbook.steps[0].name == "Read"
        assert playbook.steps[1].name == "Write"


class TestPlaybookAdditiveEvolution:
    """Guardrail tests: v0.1 fields must remain additive-only."""

    REQUIRED_FIELDS_V01 = {
        "playbook_version",
        "name",
        "version",
        "description",
        "reasoning_modes",
        "budgets",
        "steps",
        "metadata",
    }

    def test_all_v01_fields_present(self) -> None:
        """All v0.1 contract fields must be present in schema."""
        field_names = set(Playbook.model_fields.keys())
        missing = self.REQUIRED_FIELDS_V01 - field_names
        assert not missing, f"Missing v0.1 fields: {missing}"


# ===========================================================================
# Cross-schema Integration Tests
# ===========================================================================


class TestSchemaIntegration:
    """Integration tests across schemas."""

    def test_taskspec_mode_matches_runtrace_mode(self) -> None:
        """ExecutionMode enum is shared across TaskSpec and RunTrace."""
        spec = TaskSpec(prompt="test", workspace_id="ws-1", mode=ExecutionMode.SUPERVISED)
        trace = RunTrace(
            workspace_id="ws-1",
            mode=ExecutionMode.SUPERVISED,
            playbook=PlaybookMetadata(name="default", version="1.0"),
            started_at=datetime.now(UTC),
            verifier=Verifier(status=VerifierStatus.PENDING),
            final=FinalStatus.SUCCESS,
        )
        assert spec.mode == trace.mode

    def test_budgets_shared_between_taskspec_and_playbook(self) -> None:
        """Budgets model is shared and consistent."""
        spec_budgets = Budgets(max_steps=10, max_tokens=5000)
        playbook_budgets = Budgets(max_steps=10, max_tokens=5000)
        assert spec_budgets == playbook_budgets

    def test_full_workflow_schemas(self) -> None:
        """Simulate a full workflow: TaskSpec -> Playbook -> RunTrace."""
        # 1. Create task spec
        spec = (
            TaskSpecBuilder("Implement feature X", "ws-123")
            .mode(ExecutionMode.SUPERVISED)
            .playbook_preference("standard")
            .budgets(max_steps=10)
            .build()
        )

        # 2. Select playbook
        playbook = (
            PlaybookBuilder("standard", "1.0")
            .reasoning_modes([ReasoningMode.CHAIN_OF_THOUGHT])
            .budgets(max_steps=spec.budgets.max_steps)
            .add_step("Analyze", skill_name="analyze")
            .add_step("Implement", skill_name="implement")
            .add_step("Verify", skill_name="verify")
            .build()
        )

        # 3. Execute and record trace
        trace = (
            RunTraceBuilder(spec.workspace_id, spec.mode, playbook.name, playbook.version)
            .add_step(StepType.SKILL_CALL, skill_name="analyze", duration_ms=500)
            .add_step(StepType.SKILL_CALL, skill_name="implement", duration_ms=2000)
            .add_step(StepType.VERIFICATION, duration_ms=100)
            .add_artifact("/ws-123/output.py", "text/x-python", size_bytes=1024)
            .verify(VerifierStatus.PASSED, message="All tests pass")
            .complete(FinalStatus.SUCCESS)
            .build()
        )

        # Verify linkage
        assert trace.workspace_id == spec.workspace_id
        assert trace.mode == spec.mode
        assert trace.playbook.name == playbook.name
        assert len(trace.steps) == 3
