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
    EvidenceRef,
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
    WorkspaceSource,
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
        now = datetime.now(UTC)
        trace = RunTrace(
            workspace_id="ws-1",
            mode=ExecutionMode.MANUAL,
            playbook=PlaybookMetadata(name="default", version="1.0"),
            started_at=now,
            verifier=Verifier(status=VerifierStatus.PASSED, checked_at=now),
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
        now = datetime.now(UTC)
        trace = RunTrace(
            workspace_id="ws-1",
            mode=ExecutionMode.MANUAL,
            playbook=PlaybookMetadata(name="default", version="1.0"),
            started_at=now,
            verifier=Verifier(status=VerifierStatus.PASSED, checked_at=now),
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

    def test_verifier_pending_with_success_rejected(self) -> None:
        """AF-0029: PENDING verifier with SUCCESS final status must be rejected."""
        with pytest.raises(Exception, match="Verifier status cannot be PENDING"):
            RunTrace(
                workspace_id="ws-1",
                mode=ExecutionMode.MANUAL,
                playbook=PlaybookMetadata(name="default", version="1.0"),
                started_at=datetime.now(UTC),
                verifier=Verifier(status=VerifierStatus.PENDING),
                final=FinalStatus.SUCCESS,
            )

    def test_verifier_non_pending_requires_checked_at(self) -> None:
        """AF-0029: Non-PENDING verifier must have checked_at set."""
        with pytest.raises(Exception, match="checked_at must be set"):
            RunTrace(
                workspace_id="ws-1",
                mode=ExecutionMode.MANUAL,
                playbook=PlaybookMetadata(name="default", version="1.0"),
                started_at=datetime.now(UTC),
                verifier=Verifier(status=VerifierStatus.PASSED),  # Missing checked_at
                final=FinalStatus.SUCCESS,
            )

    def test_verifier_pending_without_checked_at_allowed(self) -> None:
        """PENDING verifier status does not require checked_at."""
        trace = RunTrace(
            workspace_id="ws-1",
            mode=ExecutionMode.MANUAL,
            playbook=PlaybookMetadata(name="default", version="1.0"),
            started_at=datetime.now(UTC),
            verifier=Verifier(status=VerifierStatus.PENDING),
            final=FinalStatus.ABORTED,  # Not SUCCESS, so PENDING is OK
        )
        assert trace.verifier.status == VerifierStatus.PENDING
        assert trace.verifier.checked_at is None

    def test_workspace_source_field_optional(self) -> None:
        """AF-0030: workspace_source field is optional for backwards compatibility."""
        now = datetime.now(UTC)
        trace = RunTrace(
            workspace_id="ws-1",
            mode=ExecutionMode.MANUAL,
            playbook=PlaybookMetadata(name="default", version="1.0"),
            started_at=now,
            verifier=Verifier(status=VerifierStatus.PASSED, checked_at=now),
            final=FinalStatus.SUCCESS,
            # workspace_source not provided
        )
        assert trace.workspace_source is None

    def test_workspace_source_all_values(self) -> None:
        """AF-0030: workspace_source accepts all defined enum values."""
        now = datetime.now(UTC)
        for source in WorkspaceSource:
            trace = RunTrace(
                workspace_id="ws-1",
                workspace_source=source,
                mode=ExecutionMode.MANUAL,
                playbook=PlaybookMetadata(name="default", version="1.0"),
                started_at=now,
                verifier=Verifier(status=VerifierStatus.PASSED, checked_at=now),
                final=FinalStatus.SUCCESS,
            )
            assert trace.workspace_source == source


class TestEvidenceRefContract:
    """Contract tests for EvidenceRef v0.1 (AF-0049)."""

    def test_required_fields(self) -> None:
        """EvidenceRef has required fields."""
        ref = EvidenceRef(
            ref_id="ref-1",
            source_type="file",
            source_path="/docs/readme.md",
        )
        assert ref.ref_id == "ref-1"
        assert ref.source_type == "file"
        assert ref.source_path == "/docs/readme.md"

    def test_optional_fields_default_none(self) -> None:
        """Optional fields default to None."""
        ref = EvidenceRef(
            ref_id="ref-1",
            source_type="file",
            source_path="/docs/readme.md",
        )
        assert ref.excerpt is None
        assert ref.line_start is None
        assert ref.line_end is None
        assert ref.relevance is None
        assert ref.confidence is None
        assert ref.metadata == {}

    def test_full_evidence_ref(self) -> None:
        """EvidenceRef with all fields populated."""
        ref = EvidenceRef(
            ref_id="ref-123",
            source_type="file",
            source_path="/docs/architecture.md",
            excerpt="The system uses a layered architecture...",
            line_start=10,
            line_end=25,
            relevance="Describes core architecture principles",
            confidence=0.95,
            metadata={"section": "overview", "heading": "Architecture"},
        )
        assert ref.ref_id == "ref-123"
        assert ref.excerpt == "The system uses a layered architecture..."
        assert ref.line_start == 10
        assert ref.line_end == 25
        assert ref.relevance == "Describes core architecture principles"
        assert ref.confidence == 0.95
        assert ref.metadata["section"] == "overview"

    def test_confidence_bounds(self) -> None:
        """Confidence must be between 0 and 1."""
        # Valid bounds
        ref_low = EvidenceRef(ref_id="r1", source_type="file", source_path="/a.md", confidence=0.0)
        ref_high = EvidenceRef(ref_id="r2", source_type="file", source_path="/b.md", confidence=1.0)
        assert ref_low.confidence == 0.0
        assert ref_high.confidence == 1.0

        # Invalid bounds
        with pytest.raises(Exception):
            EvidenceRef(ref_id="r3", source_type="file", source_path="/c.md", confidence=-0.1)
        with pytest.raises(Exception):
            EvidenceRef(ref_id="r4", source_type="file", source_path="/d.md", confidence=1.1)

    def test_line_numbers_positive(self) -> None:
        """Line numbers must be positive (1-indexed)."""
        ref = EvidenceRef(
            ref_id="r1",
            source_type="file",
            source_path="/a.md",
            line_start=1,
            line_end=10,
        )
        assert ref.line_start == 1

        with pytest.raises(Exception):
            EvidenceRef(ref_id="r2", source_type="file", source_path="/b.md", line_start=0)

    def test_step_with_evidence_refs(self) -> None:
        """Step can include evidence_refs field (AF-0049)."""
        now = datetime.now(UTC)
        refs = [
            EvidenceRef(
                ref_id="ref-1",
                source_type="file",
                source_path="/docs/readme.md",
                excerpt="Project overview",
            ),
            EvidenceRef(
                ref_id="ref-2",
                source_type="file",
                source_path="/docs/design.md",
                line_start=1,
                line_end=20,
            ),
        ]
        step = Step(
            step_id="step-1",
            step_number=0,
            step_type=StepType.SKILL_CALL,
            skill_name="strategic_brief",
            started_at=now,
            evidence_refs=refs,
        )
        assert step.evidence_refs is not None
        assert len(step.evidence_refs) == 2
        assert step.evidence_refs[0].source_path == "/docs/readme.md"
        assert step.evidence_refs[1].line_end == 20

    def test_step_evidence_refs_optional(self) -> None:
        """evidence_refs is optional (backward compatible)."""
        now = datetime.now(UTC)
        step = Step(
            step_id="step-1",
            step_number=0,
            step_type=StepType.SKILL_CALL,
            started_at=now,
        )
        assert step.evidence_refs is None

    def test_builder_with_evidence_refs(self) -> None:
        """RunTraceBuilder supports evidence_refs on steps."""
        refs = [
            EvidenceRef(
                ref_id="ref-1",
                source_type="file",
                source_path="/data/source.md",
            )
        ]
        builder = RunTraceBuilder(
            workspace_id="ws-1",
            mode=ExecutionMode.MANUAL,
            playbook_name="test",
            playbook_version="1.0",
        )
        builder.add_step(
            step_type=StepType.SKILL_CALL,
            skill_name="read_sources",
            evidence_refs=refs,
        )
        builder.verify(VerifierStatus.PASSED)
        builder.complete(FinalStatus.SUCCESS)
        trace = builder.build()

        assert len(trace.steps) == 1
        assert trace.steps[0].evidence_refs is not None
        assert len(trace.steps[0].evidence_refs) == 1
        assert trace.steps[0].evidence_refs[0].source_path == "/data/source.md"


class TestRunTraceAdditiveEvolution:
    """Guardrail tests: v0.1 fields must remain additive-only."""

    REQUIRED_FIELDS_V01 = {
        "trace_version",
        "run_id",
        "workspace_id",
        "workspace_source",  # AF-0030
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
        now = datetime.now(UTC)
        spec = TaskSpec(prompt="test", workspace_id="ws-1", mode=ExecutionMode.SUPERVISED)
        trace = RunTrace(
            workspace_id="ws-1",
            mode=ExecutionMode.SUPERVISED,
            playbook=PlaybookMetadata(name="default", version="1.0"),
            started_at=now,
            verifier=Verifier(status=VerifierStatus.PASSED, checked_at=now),
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


# ===========================================================================
# AF0078: Playbook Plugin Architecture Tests
# ===========================================================================


class TestPlaybookPluginArchitecture:
    """Tests for playbook entry point discovery (AF0078)."""

    def test_playbook_info_has_source_field(self) -> None:
        """PlaybookInfo includes source field."""
        from ag.playbooks.registry import PlaybookInfo

        info = PlaybookInfo(
            name="test_pb",
            playbook=Playbook(
                name="test_pb",
                version="1.0.0",
                steps=[],
            ),
            source="test",
        )

        assert hasattr(info, "source")
        assert info.source == "test"

    def test_get_playbook_info_includes_source(self) -> None:
        """get_playbook_info() dict includes source field."""
        from ag.playbooks.registry import get_playbook_info

        info = get_playbook_info("default_v0")

        assert info is not None
        assert "source" in info
        assert info["source"] == "entry-point"

    def test_register_playbook_function(self) -> None:
        """register_playbook() registers a playbook correctly."""
        from ag.playbooks.registry import (
            get_playbook,
            register_playbook,
            unregister_playbook,
        )

        test_pb = Playbook(
            name="test_register_v0",
            version="1.0.0",
            description="Test playbook for registration",
            steps=[],
        )

        register_playbook(test_pb, source="test")

        try:
            pb = get_playbook("test_register_v0")
            assert pb is not None
            assert pb.name == "test_register_v0"

            # Also check alias works
            pb_alias = get_playbook("test_register")
            assert pb_alias is not None
            assert pb_alias.name == "test_register_v0"
        finally:
            unregister_playbook("test_register_v0")

    def test_unregister_playbook_removes_aliases(self) -> None:
        """unregister_playbook() removes both canonical name and aliases."""
        from ag.playbooks.registry import (
            get_playbook,
            register_playbook,
            unregister_playbook,
        )

        test_pb = Playbook(
            name="test_unregister_v0",
            version="1.0.0",
            steps=[],
        )

        register_playbook(test_pb, source="test")

        # Verify registered
        assert get_playbook("test_unregister_v0") is not None
        assert get_playbook("test_unregister") is not None

        # Unregister
        result = unregister_playbook("test_unregister_v0")
        assert result is True

        # Verify both gone
        assert get_playbook("test_unregister_v0") is None
        assert get_playbook("test_unregister") is None

    def test_default_registry_uses_entry_points(self) -> None:
        """Built-in playbooks are registered via entry points."""
        from ag.playbooks.registry import get_playbook_entry

        # Built-in playbooks should have entry-point source
        entry = get_playbook_entry("default_v0")
        assert entry is not None
        assert entry.source == "entry-point"

        entry = get_playbook_entry("summarize_v0")
        assert entry is not None
        assert entry.source == "entry-point"

    def test_list_playbooks_returns_all_registered(self) -> None:
        """list_playbooks() returns all registered playbook names."""
        from ag.playbooks.registry import list_playbooks

        playbooks = list_playbooks()

        assert "default_v0" in playbooks
        assert "delegate_v0" in playbooks
        assert "research_v0" in playbooks
        assert "summarize_v0" in playbooks

    def test_entry_point_discovery_mock(self, mocker) -> None:
        """Entry point discovery registers playbooks from mock entry points."""
        from ag.playbooks.registry import (
            _discover_entrypoint_playbooks,
            reset_registry,
        )

        # Reset to test discovery in isolation
        reset_registry()

        mock_pb = Playbook(
            name="mock_playbook_v0",
            version="1.0.0",
            steps=[],
        )

        mock_ep = mocker.MagicMock()
        mock_ep.name = "mock_playbook"
        mock_ep.load.return_value = mock_pb

        mocker.patch(
            "ag.playbooks.registry.entry_points",
            return_value=[mock_ep],
        )

        _discover_entrypoint_playbooks()

        from ag.playbooks.registry import get_playbook

        pb = get_playbook("mock_playbook_v0")
        assert pb is not None
        assert pb.name == "mock_playbook_v0"

        # Clean up - re-initialize with real entry points
        reset_registry()
