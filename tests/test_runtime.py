"""Runtime integration tests.

Tests:
1. Happy path: full runtime execution produces valid RunTrace
2. Failure path: missing skill or step error records failure correctly
"""

from pathlib import Path

import pytest

from ag.core import (
    ExecutionMode,
    FinalStatus,
    RunTrace,
    VerifierStatus,
    create_runtime,
)
from ag.core.runtime import Runtime
from ag.skills import SkillRegistry, create_default_registry
from ag.storage import SQLiteArtifactStore, SQLiteRunStore

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def temp_root(tmp_path: Path) -> Path:
    """Temporary workspace root directory."""
    return tmp_path / "workspaces"


@pytest.fixture
def run_store(temp_root: Path) -> SQLiteRunStore:
    """Test run store."""
    store = SQLiteRunStore(temp_root)
    yield store
    store.close()


@pytest.fixture
def artifact_store(temp_root: Path) -> SQLiteArtifactStore:
    """Test artifact store."""
    store = SQLiteArtifactStore(temp_root)
    yield store
    store.close()


@pytest.fixture
def registry() -> SkillRegistry:
    """Test skill registry with default skills."""
    return create_default_registry()


@pytest.fixture
def runtime(
    registry: SkillRegistry,
    run_store: SQLiteRunStore,
    artifact_store: SQLiteArtifactStore,
) -> "Runtime":
    """Configured runtime for testing."""
    from ag.core import create_runtime

    return create_runtime(
        registry=registry,
        run_store=run_store,
        artifact_store=artifact_store,
    )


# ---------------------------------------------------------------------------
# Happy Path Tests
# ---------------------------------------------------------------------------


class TestRuntimeHappyPath:
    """Happy path integration tests."""

    def test_execute_produces_run_trace(
        self, runtime: "Runtime", run_store: SQLiteRunStore
    ) -> None:
        """Runtime execution produces a valid RunTrace."""
        trace = runtime.execute(
            prompt="Test task",
            workspace="ws-test",
            mode="manual",
        )

        assert isinstance(trace, RunTrace)
        assert trace.workspace_id == "ws-test"
        assert trace.mode == ExecutionMode.MANUAL
        assert trace.run_id is not None
        assert len(trace.run_id) > 0

    def test_trace_has_all_required_fields(self, runtime: "Runtime") -> None:
        """RunTrace has all required v0.1 contract fields."""
        trace = runtime.execute(prompt="Test task", workspace="ws-test")

        # Version
        assert trace.trace_version == "0.1"

        # Identifiers
        assert trace.run_id
        assert trace.workspace_id == "ws-test"

        # Mode
        assert trace.mode in (ExecutionMode.MANUAL, ExecutionMode.SUPERVISED)

        # Playbook
        assert trace.playbook.name
        assert trace.playbook.version

        # Timestamps
        assert trace.started_at is not None
        assert trace.ended_at is not None
        assert trace.duration_ms is not None
        assert trace.duration_ms >= 0

        # Steps
        assert isinstance(trace.steps, list)

        # Verifier
        assert trace.verifier.status in (
            VerifierStatus.PASSED,
            VerifierStatus.FAILED,
            VerifierStatus.PENDING,
            VerifierStatus.SKIPPED,
        )

        # Final status
        assert trace.final in (
            FinalStatus.SUCCESS,
            FinalStatus.FAILURE,
            FinalStatus.ABORTED,
            FinalStatus.TIMEOUT,
        )

    def test_manual_mode_sets_trace_mode(self, runtime: "Runtime") -> None:
        """Manual mode flag is reflected in trace."""
        trace = runtime.execute(
            prompt="Test task",
            workspace="ws-test",
            mode="manual",
        )

        assert trace.mode == ExecutionMode.MANUAL

    def test_llm_mode_sets_trace_mode(self, runtime: "Runtime") -> None:
        """LLM mode flag is reflected in trace."""
        trace = runtime.execute(
            prompt="Test task",
            workspace="ws-test",
            mode="llm",
        )

        assert trace.mode == ExecutionMode.SUPERVISED

    def test_trace_persisted_to_storage(
        self, runtime: "Runtime", run_store: SQLiteRunStore
    ) -> None:
        """RunTrace is persisted to storage."""
        trace = runtime.execute(
            prompt="Test task",
            workspace="ws-test",
            mode="manual",
        )

        # Retrieve from storage
        stored = run_store.get("ws-test", trace.run_id)

        assert stored is not None
        assert stored.run_id == trace.run_id
        assert stored.workspace_id == trace.workspace_id
        assert stored.final == trace.final

    def test_playbook_executes_all_steps(self, runtime: "Runtime") -> None:
        """Runtime executes all playbook steps."""
        trace = runtime.execute(prompt="Test task", workspace="ws-test")

        # default_v0 has 1 echo step (AF0079 simplified stub playbook)
        assert len(trace.steps) >= 1

        # Check steps have proper structure
        for step in trace.steps:
            assert step.step_id is not None
            assert step.step_number >= 0
            assert step.started_at is not None

    def test_successful_run_has_passed_verifier(self, runtime: "Runtime") -> None:
        """Successful execution has verifier status 'passed'."""
        trace = runtime.execute(prompt="Test task", workspace="ws-test")

        # If all steps succeed, verifier should pass
        if trace.final == FinalStatus.SUCCESS:
            assert trace.verifier.status == VerifierStatus.PASSED

    def test_default_playbook_selected(self, runtime: "Runtime") -> None:
        """Default playbook is selected when no preference given."""
        trace = runtime.execute(prompt="Test task", workspace="ws-test")

        assert trace.playbook.name == "default_v0"


# ---------------------------------------------------------------------------
# Failure Path Tests
# ---------------------------------------------------------------------------


class TestRuntimeFailurePath:
    """Failure path integration tests."""

    def test_missing_skill_stops_execution(
        self,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
        temp_root: Path,
    ) -> None:
        """Missing skill causes execution to stop and record failure."""
        # Create registry without the required skills
        empty_registry = SkillRegistry()
        runtime = create_runtime(
            registry=empty_registry,
            run_store=run_store,
            artifact_store=artifact_store,
        )

        trace = runtime.execute(prompt="Test task", workspace="ws-test")

        # Should fail because skills are missing
        assert trace.final == FinalStatus.FAILURE
        assert trace.error is not None
        assert "not found" in trace.error.lower() or "fail" in trace.error.lower()

    def test_skill_failure_stops_required_step(
        self,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
    ) -> None:
        """Skill failure on required step stops execution (AF0079 updated)."""
        from ag.core.playbook import (
            Budgets,
            Playbook,
            PlaybookStep,
            PlaybookStepType,
            ReasoningMode,
        )
        from ag.playbooks.registry import _REGISTRY

        # Create a test playbook with fail_skill as first required step
        fail_playbook = Playbook(
            playbook_version="0.1",
            name="fail_test",
            version="1.0.0",
            description="Test playbook that fails",
            reasoning_modes=[ReasoningMode.DIRECT],
            budgets=Budgets(max_steps=3, max_tokens=None, max_duration_seconds=60),
            steps=[
                PlaybookStep(
                    step_id="step_0",
                    name="fail",
                    step_type=PlaybookStepType.SKILL,
                    skill_name="fail_skill",
                    description="Intentionally fail",
                    required=True,
                    retry_count=0,
                ),
            ],
            metadata={"stability": "test"},
        )

        # Temporarily register the playbook
        _REGISTRY["fail_test"] = fail_playbook

        try:
            # Use default registry which includes fail_skill
            from ag.skills import get_default_registry

            registry = get_default_registry()

            runtime = create_runtime(
                registry=registry,
                run_store=run_store,
                artifact_store=artifact_store,
            )

            trace = runtime.execute(
                prompt="Test task",
                workspace="ws-test",
                playbook="fail_test",
            )

            # fail_skill is required and fails
            assert trace.final == FinalStatus.FAILURE
            assert trace.verifier.status == VerifierStatus.FAILED
        finally:
            # Clean up
            del _REGISTRY["fail_test"]

    def test_failed_run_persisted(
        self,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
    ) -> None:
        """Failed runs are still persisted to storage."""
        empty_registry = SkillRegistry()
        runtime = create_runtime(
            registry=empty_registry,
            run_store=run_store,
            artifact_store=artifact_store,
        )

        trace = runtime.execute(prompt="Test task", workspace="ws-test")

        # Verify it's persisted
        stored = run_store.get("ws-test", trace.run_id)
        assert stored is not None
        assert stored.final == FinalStatus.FAILURE

    def test_error_recorded_in_step(
        self,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
    ) -> None:
        """Step errors are recorded in the step object."""
        empty_registry = SkillRegistry()
        runtime = create_runtime(
            registry=empty_registry,
            run_store=run_store,
            artifact_store=artifact_store,
        )

        trace = runtime.execute(prompt="Test task", workspace="ws-test")

        # First step should have an error
        assert len(trace.steps) >= 1
        first_step = trace.steps[0]
        assert first_step.error is not None

    def test_skill_exception_handled(
        self,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
    ) -> None:
        """Skills that raise exceptions are handled gracefully (AF0079 updated)."""
        from ag.core.playbook import (
            Budgets,
            Playbook,
            PlaybookStep,
            PlaybookStepType,
            ReasoningMode,
        )
        from ag.playbooks.registry import _REGISTRY

        # Create a playbook with error_skill that raises an exception
        error_playbook = Playbook(
            playbook_version="0.1",
            name="error_test",
            version="1.0.0",
            description="Test playbook that errors",
            reasoning_modes=[ReasoningMode.DIRECT],
            budgets=Budgets(max_steps=3, max_tokens=None, max_duration_seconds=60),
            steps=[
                PlaybookStep(
                    step_id="step_0",
                    name="error",
                    step_type=PlaybookStepType.SKILL,
                    skill_name="error_skill",
                    description="Intentionally raise exception",
                    required=True,
                    retry_count=0,
                ),
            ],
            metadata={"stability": "test"},
        )

        # Temporarily register the playbook
        _REGISTRY["error_test"] = error_playbook

        try:
            # Use default registry which includes error_skill
            from ag.skills import get_default_registry

            registry = get_default_registry()

            runtime = create_runtime(
                registry=registry,
                run_store=run_store,
                artifact_store=artifact_store,
            )

            # Should not raise, should record failure
            trace = runtime.execute(
                prompt="Test task",
                workspace="ws-test",
                playbook="error_test",
            )

            assert trace.final == FinalStatus.FAILURE
            assert "error" in trace.steps[0].error.lower() or "intentional" in trace.steps[0].error.lower()
        finally:
            # Clean up
            del _REGISTRY["error_test"]


# ---------------------------------------------------------------------------
# Echo Tool Test (Required by AF-0007)
# ---------------------------------------------------------------------------


class TestEchoTool:
    """Tests for echo_tool skill."""

    def test_echo_tool_exists_in_registry(self, registry: SkillRegistry) -> None:
        """echo_tool skill is registered."""
        assert registry.has("echo_tool")

    def test_echo_tool_returns_input(self, registry: SkillRegistry) -> None:
        """echo_tool returns the input message."""
        success, output, result = registry.execute("echo_tool", {"message": "Hello, World!"})

        assert success is True
        assert "Hello, World!" in output
        assert result["echoed"] == "Hello, World!"


# ---------------------------------------------------------------------------
# Playbook Tests
# ---------------------------------------------------------------------------


class TestDefaultPlaybook:
    """Tests for default_v0 playbook."""

    def test_default_v0_exists(self) -> None:
        """default_v0 playbook exists."""
        from ag.core import get_playbook

        playbook = get_playbook("default_v0")
        assert playbook is not None

    def test_default_v0_is_linear(self) -> None:
        """default_v0 playbook has linear steps."""
        from ag.core import DEFAULT_V0

        assert len(DEFAULT_V0.steps) >= 1
        # Check steps have sequential IDs
        for i, step in enumerate(DEFAULT_V0.steps):
            assert step.step_id == f"step_{i}"

    def test_default_v0_uses_direct_reasoning(self) -> None:
        """default_v0 playbook uses direct reasoning mode."""
        from ag.core import DEFAULT_V0, ReasoningMode

        # AF0079: Simplified stub playbook uses DIRECT reasoning
        assert ReasoningMode.DIRECT in DEFAULT_V0.reasoning_modes


# ---------------------------------------------------------------------------
# Interface Tests
# ---------------------------------------------------------------------------


class TestInterfaces:
    """Tests that interfaces are properly defined."""

    def test_interfaces_use_protocol(self) -> None:
        """Interfaces use typing.Protocol."""
        from typing import Protocol

        from ag.core.interfaces import (
            Executor,
            Normalizer,
            Orchestrator,
            Planner,
            Recorder,
            Verifier,
        )

        # Check they're Protocols (structural subtyping)
        for iface in [Normalizer, Planner, Orchestrator, Executor, Verifier, Recorder]:
            assert issubclass(iface, Protocol) or hasattr(iface, "__protocol_attrs__")


# ---------------------------------------------------------------------------
# Runtime Lifecycle Tests (AF-0021 regression)
# ---------------------------------------------------------------------------


class TestRuntimeLifecycle:
    """Tests for Runtime context manager support (AF-0021)."""

    def test_runtime_context_manager(self, tmp_path: Path) -> None:
        """Runtime works as context manager and closes stores."""
        from ag.core import create_runtime
        from ag.storage import SQLiteArtifactStore, SQLiteRunStore

        run_store = SQLiteRunStore(tmp_path)
        artifact_store = SQLiteArtifactStore(tmp_path)

        runtime = create_runtime(run_store=run_store, artifact_store=artifact_store)

        with runtime:
            trace = runtime.execute(
                prompt="Test context manager",
                workspace="ctx-ws",
                mode="manual",
            )
            assert trace is not None

        # After exiting context, stores should be closed
        assert run_store._connections == {}
        assert artifact_store._connections == {}

    def test_runtime_close_explicit(self, tmp_path: Path) -> None:
        """Runtime.close() explicitly closes underlying stores."""
        from ag.core import create_runtime
        from ag.storage import SQLiteArtifactStore, SQLiteRunStore

        run_store = SQLiteRunStore(tmp_path)
        artifact_store = SQLiteArtifactStore(tmp_path)

        runtime = create_runtime(run_store=run_store, artifact_store=artifact_store)
        runtime.execute(prompt="Test", workspace="close-ws", mode="manual")

        # Connections exist
        assert len(run_store._connections) > 0

        runtime.close()

        # After close, stores should be empty
        assert run_store._connections == {}
        assert artifact_store._connections == {}
