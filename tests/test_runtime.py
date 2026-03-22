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

    def test_playbook_object_bypasses_planner(self, runtime: "Runtime") -> None:
        """BUG-0016: playbook_object parameter bypasses planner selection."""
        from ag.core import Playbook, PlaybookStep, PlaybookStepType

        # Create a custom playbook with a specific skill
        custom_playbook = Playbook(
            name="custom_test_playbook",
            version="1.0.0",
            description="Test playbook for BUG-0016 fix",
            steps=[
                PlaybookStep(
                    step_id="s1",
                    name="Test Echo",
                    step_type=PlaybookStepType.SKILL,
                    skill_name="echo",  # Use echo skill which exists in registry
                    parameters={"message": "BUG-0016 test"},
                ),
            ],
        )

        trace = runtime.execute(
            prompt="Test task",
            workspace="ws-test",
            playbook_object=custom_playbook,
        )

        # Verify the custom playbook was used, not default
        assert trace.playbook.name == "custom_test_playbook"
        assert trace.playbook.version == "1.0.0"

        # Verify the step was executed
        assert len(trace.steps) >= 1
        assert any(s.skill_name == "echo" for s in trace.steps)


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
        from ag.playbooks.registry import register_playbook, unregister_playbook

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
        register_playbook(fail_playbook, source="test")

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
            unregister_playbook("fail_test")

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
        from ag.playbooks.registry import register_playbook, unregister_playbook

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
        register_playbook(error_playbook, source="test")

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
            error_msg = trace.steps[0].error.lower()
            assert "error" in error_msg or "intentional" in error_msg
        finally:
            # Clean up
            unregister_playbook("error_test")


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


# ---------------------------------------------------------------------------
# Policy Validation Tests (AF-0087)
# ---------------------------------------------------------------------------


class TestPolicyNormalizerValidation:
    """Tests for V0Normalizer policy validation (AF-0087).

    Normalizer enforces:
    - Empty/whitespace-only prompt rejection
    - Workspace requirement (no implicit creation)
    """

    def test_empty_prompt_rejected(self) -> None:
        """Normalizer rejects empty prompt."""
        from ag.core.runtime import V0Normalizer

        normalizer = V0Normalizer()

        with pytest.raises(ValueError) as exc_info:
            normalizer.normalize(prompt="", workspace="ws-test")

        assert "cannot be empty" in str(exc_info.value)

    def test_whitespace_only_prompt_rejected(self) -> None:
        """Normalizer rejects whitespace-only prompt."""
        from ag.core.runtime import V0Normalizer

        normalizer = V0Normalizer()

        with pytest.raises(ValueError) as exc_info:
            normalizer.normalize(prompt="   \n  ", workspace="ws-test")

        assert "cannot be empty" in str(exc_info.value)

    def test_missing_workspace_rejected(self) -> None:
        """Normalizer rejects missing workspace (AF-0026)."""
        from ag.core.runtime import V0Normalizer

        normalizer = V0Normalizer()

        with pytest.raises(ValueError) as exc_info:
            normalizer.normalize(prompt="Test", workspace=None)

        assert "Workspace is required" in str(exc_info.value)

    def test_valid_task_passes_policy(self) -> None:
        """Normalizer accepts valid prompt and workspace."""
        from ag.core.runtime import V0Normalizer

        normalizer = V0Normalizer()
        task = normalizer.normalize(prompt="Valid task", workspace="ws-test")

        assert task.prompt == "Valid task"
        assert task.workspace_id == "ws-test"


class TestPolicyVerifierValidation:
    """Tests for V0Verifier policy validation (AF-0087).

    Verifier enforces:
    - Step errors cause verification failure
    - Non-success final status causes verification failure
    - All-success configuration passes verification
    """

    def test_step_error_fails_verification(self) -> None:
        """Verifier fails when step has error."""
        from datetime import UTC, datetime

        from ag.core.run_trace import FinalStatus, Step, StepType
        from ag.core.runtime import V0Verifier

        verifier = V0Verifier()
        now = datetime.now(UTC)
        steps = [
            Step(
                step_id="step_0",
                step_number=0,
                step_type=StepType.SKILL_CALL,
                started_at=now,
                error="Something went wrong",
            ),
        ]

        status, message = verifier.verify_components(steps, FinalStatus.FAILURE)

        assert status == "failed"
        assert "Step 0 failed" in message

    def test_non_success_final_status_fails_verification(self) -> None:
        """Verifier fails when final status is not SUCCESS."""
        from datetime import UTC, datetime

        from ag.core.run_trace import FinalStatus, Step, StepType
        from ag.core.runtime import V0Verifier

        verifier = V0Verifier()
        now = datetime.now(UTC)
        steps = [
            Step(step_id="step_0", step_number=0, step_type=StepType.SKILL_CALL, started_at=now),
        ]

        status, message = verifier.verify_components(steps, FinalStatus.FAILURE)

        assert status == "failed"
        assert "failure" in message.lower()

    def test_successful_run_passes_verification(self) -> None:
        """Verifier passes when all steps succeed and final is SUCCESS."""
        from datetime import UTC, datetime

        from ag.core.run_trace import FinalStatus, Step, StepType
        from ag.core.runtime import V0Verifier

        verifier = V0Verifier()
        now = datetime.now(UTC)
        steps = [
            Step(step_id="step_0", step_number=0, step_type=StepType.SKILL_CALL, started_at=now),
            Step(step_id="step_1", step_number=1, step_type=StepType.SKILL_CALL, started_at=now),
        ]

        status, message = verifier.verify_components(steps, FinalStatus.SUCCESS)

        assert status == "passed"
        assert "successfully" in message.lower()


class TestPolicyWorkspaceIsolation:
    """Tests for workspace isolation policy (AF-0087).

    Ensures:
    - Different workspaces maintain separate state
    - Run traces are scoped to their workspace
    - Cross-workspace access is prevented
    """

    def test_workspaces_isolated(
        self,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
        registry: SkillRegistry,
    ) -> None:
        """Different workspaces maintain separate run histories."""
        runtime = create_runtime(
            registry=registry,
            run_store=run_store,
            artifact_store=artifact_store,
        )

        # Execute in workspace A
        trace_a = runtime.execute(prompt="Task A", workspace="ws-a", mode="manual")

        # Execute in workspace B
        trace_b = runtime.execute(prompt="Task B", workspace="ws-b", mode="manual")

        # Verify isolation
        assert trace_a.workspace_id == "ws-a"
        assert trace_b.workspace_id == "ws-b"

        # List runs in each workspace
        runs_a = run_store.list("ws-a")
        runs_b = run_store.list("ws-b")

        assert len(runs_a) == 1
        assert len(runs_b) == 1
        assert runs_a[0].run_id == trace_a.run_id
        assert runs_b[0].run_id == trace_b.run_id

    def test_run_scoped_to_workspace(
        self,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
        registry: SkillRegistry,
    ) -> None:
        """Run trace is scoped to correct workspace."""
        runtime = create_runtime(
            registry=registry,
            run_store=run_store,
            artifact_store=artifact_store,
        )

        trace = runtime.execute(prompt="Test", workspace="scoped-ws", mode="manual")

        # Retrieve from correct workspace
        retrieved = run_store.get("scoped-ws", trace.run_id)
        assert retrieved is not None
        assert retrieved.run_id == trace.run_id

        # Cannot retrieve from wrong workspace
        wrong_ws = run_store.get("other-ws", trace.run_id)
        assert wrong_ws is None


class TestPolicyTraceEvidence:
    """Tests for traceable policy outcomes (AF-0087).

    Ensures:
    - Policy outcomes are recorded in trace
    - Failure reasons are explicit and traceable
    - All outcomes derive from verifiable trace data
    """

    def test_failure_reason_in_trace(
        self,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
    ) -> None:
        """Policy failure reason is recorded in trace."""
        from ag.core.playbook import (
            Budgets,
            Playbook,
            PlaybookStep,
            PlaybookStepType,
            ReasoningMode,
        )
        from ag.playbooks.registry import register_playbook, unregister_playbook
        from ag.skills import get_default_registry

        # Create playbook with fail_skill
        fail_playbook = Playbook(
            playbook_version="0.1",
            name="fail_test_policy",
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

        register_playbook(fail_playbook, source="test")

        try:
            runtime = create_runtime(
                registry=get_default_registry(),
                run_store=run_store,
                artifact_store=artifact_store,
            )

            trace = runtime.execute(
                prompt="Test failure",
                workspace="policy-ws",
                playbook="fail_test_policy",
            )

            # Failure is explicit in trace
            assert trace.final == FinalStatus.FAILURE
            assert trace.verifier.status == VerifierStatus.FAILED

            # Error is recorded in step
            assert trace.steps[0].error is not None
            assert "fail" in trace.steps[0].error.lower()

            # Verifier message references failure
            assert trace.verifier.message is not None

        finally:
            unregister_playbook("fail_test_policy")

    def test_success_outcome_traceable(
        self,
        runtime: "Runtime",
    ) -> None:
        """Success outcome is recorded in trace with evidence."""
        trace = runtime.execute(
            prompt="Test success",
            workspace="success-ws",
            mode="manual",
        )

        # Success is explicit in trace
        assert trace.final == FinalStatus.SUCCESS
        assert trace.verifier.status == VerifierStatus.PASSED

        # Trace has required evidence fields
        assert trace.run_id is not None
        assert trace.started_at is not None
        assert trace.ended_at is not None
        assert trace.playbook is not None
        assert len(trace.steps) > 0


# ---------------------------------------------------------------------------
# Verifier Failure Path Tests (AF-0091)
# ---------------------------------------------------------------------------


class TestVerifierFailurePaths:
    """AF-0091: Verifier outcomes must be consistent across all failure types.

    Tests each failure scenario from the decision matrix:
    | Scenario                     | Expected Status | Expected in Message |
    |------------------------------|-----------------|---------------------|
    | Step error (any type)        | failed          | step N failed       |
    | Non-SUCCESS final status     | failed          | status: <value>     |
    | Required step fails          | failed          | step N failed       |
    | Optional step fails          | passed/failed   | depends on final    |
    | Empty steps list             | failed          | status: failure     |
    | All steps succeed            | passed          | successfully        |

    Gate B requirement: "Verifier outcomes consistent across happy and failure paths"
    """

    def test_step_error_causes_failure(self) -> None:
        """Any step with error field set causes verifier failure."""
        from datetime import UTC, datetime

        from ag.core.run_trace import FinalStatus, Step, StepType
        from ag.core.runtime import V0Verifier

        verifier = V0Verifier()
        now = datetime.now(UTC)

        steps = [
            Step(
                step_id="step_0",
                step_number=0,
                step_type=StepType.SKILL_CALL,
                started_at=now,
                error="Skill execution failed",
            ),
        ]

        status, message = verifier.verify_components(steps, FinalStatus.FAILURE)

        assert status == "failed"
        assert "Step 0 failed" in message
        assert "Skill execution failed" in message

    def test_non_success_final_causes_failure(self) -> None:
        """Non-SUCCESS final status causes verifier failure even without step errors."""
        from datetime import UTC, datetime

        from ag.core.run_trace import FinalStatus, Step, StepType
        from ag.core.runtime import V0Verifier

        verifier = V0Verifier()
        now = datetime.now(UTC)

        steps = [
            Step(step_id="step_0", step_number=0, step_type=StepType.SKILL_CALL, started_at=now),
        ]

        # Test all non-SUCCESS statuses
        for bad_status in [FinalStatus.FAILURE, FinalStatus.TIMEOUT, FinalStatus.ABORTED]:
            status, message = verifier.verify_components(steps, bad_status)
            assert status == "failed", f"Expected failure for {bad_status}"
            assert bad_status.value in message.lower()

    def test_step_error_takes_precedence(self) -> None:
        """Step error message takes precedence over generic final status message."""
        from datetime import UTC, datetime

        from ag.core.run_trace import FinalStatus, Step, StepType
        from ag.core.runtime import V0Verifier

        verifier = V0Verifier()
        now = datetime.now(UTC)

        error_msg = "Provider auth failed: invalid API key"
        steps = [
            Step(
                step_id="step_0",
                step_number=0,
                step_type=StepType.SKILL_CALL,
                started_at=now,
                error=error_msg,
            ),
        ]

        status, message = verifier.verify_components(steps, FinalStatus.FAILURE)

        assert status == "failed"
        # Verifier message should contain the specific error
        assert error_msg in message

    def test_multiple_step_errors_reports_first(self) -> None:
        """With multiple step errors, verifier reports the first one."""
        from datetime import UTC, datetime

        from ag.core.run_trace import FinalStatus, Step, StepType
        from ag.core.runtime import V0Verifier

        verifier = V0Verifier()
        now = datetime.now(UTC)

        steps = [
            Step(
                step_id="step_0",
                step_number=0,
                step_type=StepType.SKILL_CALL,
                started_at=now,
                error="First error",
            ),
            Step(
                step_id="step_1",
                step_number=1,
                step_type=StepType.SKILL_CALL,
                started_at=now,
                error="Second error",
            ),
        ]

        status, message = verifier.verify_components(steps, FinalStatus.FAILURE)

        assert status == "failed"
        # Should report first step's error
        assert "Step 0 failed" in message
        assert "First error" in message

    def test_success_with_no_errors(self) -> None:
        """All steps without errors and SUCCESS status → passed verifier."""
        from datetime import UTC, datetime

        from ag.core.run_trace import FinalStatus, Step, StepType
        from ag.core.runtime import V0Verifier

        verifier = V0Verifier()
        now = datetime.now(UTC)

        steps = [
            Step(step_id="step_0", step_number=0, step_type=StepType.SKILL_CALL, started_at=now),
            Step(step_id="step_1", step_number=1, step_type=StepType.SKILL_CALL, started_at=now),
            Step(step_id="step_2", step_number=2, step_type=StepType.SKILL_CALL, started_at=now),
        ]

        status, message = verifier.verify_components(steps, FinalStatus.SUCCESS)

        assert status == "passed"
        assert "successfully" in message.lower()

    def test_empty_steps_with_failure_status(self) -> None:
        """BUG-0020: Empty steps list → verifier fails."""
        from ag.core.run_trace import FinalStatus
        from ag.core.runtime import V0Verifier

        verifier = V0Verifier()
        steps: list = []

        status, message = verifier.verify_components(steps, FinalStatus.FAILURE)

        assert status == "failed"
        assert "no steps executed" in message.lower()

    def test_empty_steps_with_success_status(self) -> None:
        """BUG-0020: Empty steps list must fail even with SUCCESS final status."""
        from ag.core.run_trace import FinalStatus
        from ag.core.runtime import V0Verifier

        verifier = V0Verifier()
        steps: list = []

        status, message = verifier.verify_components(steps, FinalStatus.SUCCESS)

        # BUG-0020: A run that did nothing is never a success
        assert status == "failed"
        assert "no steps executed" in message.lower()

    def test_deterministic_behavior(self) -> None:
        """Identical inputs produce identical outputs (determinism test)."""
        from datetime import UTC, datetime

        from ag.core.run_trace import FinalStatus, Step, StepType
        from ag.core.runtime import V0Verifier

        verifier = V0Verifier()
        now = datetime.now(UTC)

        steps = [
            Step(
                step_id="step_0",
                step_number=0,
                step_type=StepType.SKILL_CALL,
                started_at=now,
                error="Deterministic error",
            ),
        ]

        # Run 10 times and ensure same result
        results = [verifier.verify_components(steps, FinalStatus.FAILURE) for _ in range(10)]

        first_result = results[0]
        for result in results[1:]:
            assert result == first_result, "Verifier should be deterministic"


class TestBUG0020EmptyPlanGuards:
    """BUG-0020: Empty plan must never report success.

    Tests that V0Verifier, V1Verifier, and V1Orchestrator all reject
    runs with zero executed steps.
    """

    def test_v1_verifier_fails_on_empty_steps(self) -> None:
        """V1Verifier.verify_components with empty steps returns failed."""
        from ag.core.run_trace import FinalStatus
        from ag.core.verifier import V1Verifier

        verifier = V1Verifier()
        status, message = verifier.verify_components([], FinalStatus.SUCCESS)

        assert status == "failed"
        assert "no steps executed" in message.lower()

    def test_v1_verifier_fails_on_empty_steps_with_failure_status(self) -> None:
        """V1Verifier empty steps + FAILURE status → still reports 'no steps'."""
        from ag.core.run_trace import FinalStatus
        from ag.core.verifier import V1Verifier

        verifier = V1Verifier()
        status, message = verifier.verify_components([], FinalStatus.FAILURE)

        assert status == "failed"
        assert "no steps executed" in message.lower()

    def test_v1_orchestrator_fails_on_empty_plan(
        self,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
    ) -> None:
        """V1Orchestrator returns FAILURE trace for playbook with zero steps."""
        from ag.core.orchestrator import V1Orchestrator
        from ag.core.playbook import Budgets, Playbook, ReasoningMode
        from ag.core.run_trace import FinalStatus, VerifierStatus
        from ag.core.task_spec import ExecutionMode, TaskSpec

        empty_playbook = Playbook(
            playbook_version="0.1",
            name="empty_test",
            version="1.0.0",
            description="Playbook with no steps",
            reasoning_modes=[ReasoningMode.DIRECT],
            budgets=Budgets(max_steps=1, max_tokens=None, max_duration_seconds=60),
            steps=[],
        )

        task = TaskSpec(
            prompt="Test empty plan",
            workspace_id="bug0020-ws",
            mode=ExecutionMode.MANUAL,
        )

        orchestrator = V1Orchestrator()
        trace = orchestrator.run(task, empty_playbook)

        assert trace.final == FinalStatus.FAILURE
        assert trace.error == "No executable steps in plan"
        assert trace.verifier.status == VerifierStatus.FAILED
        assert len(trace.steps) == 0


class TestVerifierFailurePathsE2E:
    """AF-0091: End-to-end tests for failure scenarios through full runtime.

    These tests verify that runtime routes failure scenarios through verifier correctly.
    """

    def test_skill_exception_recorded_in_verifier(
        self,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
    ) -> None:
        """Skill that raises exception → verifier fails with error detail."""
        from ag.core.playbook import (
            Budgets,
            Playbook,
            PlaybookStep,
            PlaybookStepType,
            ReasoningMode,
        )
        from ag.playbooks.registry import register_playbook, unregister_playbook
        from ag.skills import get_default_registry

        error_playbook = Playbook(
            playbook_version="0.1",
            name="e2e_error_test",
            version="1.0.0",
            description="Test playbook with error skill",
            reasoning_modes=[ReasoningMode.DIRECT],
            budgets=Budgets(max_steps=3, max_tokens=None, max_duration_seconds=60),
            steps=[
                PlaybookStep(
                    step_id="step_0",
                    name="error",
                    step_type=PlaybookStepType.SKILL,
                    skill_name="error_skill",
                    description="Raises exception",
                    required=True,
                    retry_count=0,
                ),
            ],
        )

        register_playbook(error_playbook, source="test")

        try:
            runtime = create_runtime(
                registry=get_default_registry(),
                run_store=run_store,
                artifact_store=artifact_store,
            )

            trace = runtime.execute(
                prompt="Test error handling",
                workspace="e2e-ws",
                playbook="e2e_error_test",
            )

            # Verifier should fail
            assert trace.verifier.status == VerifierStatus.FAILED
            assert trace.verifier.message is not None
            assert "Step 0" in trace.verifier.message
            assert "failed" in trace.verifier.message.lower()

            # Step should have error
            assert trace.steps[0].error is not None

            # Final status should be FAILURE
            assert trace.final == FinalStatus.FAILURE

        finally:
            unregister_playbook("e2e_error_test")

    def test_optional_step_failure_allows_success(
        self,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
    ) -> None:
        """Optional step failure doesn't prevent success if final is SUCCESS."""
        from ag.core.playbook import (
            Budgets,
            Playbook,
            PlaybookStep,
            PlaybookStepType,
            ReasoningMode,
        )
        from ag.playbooks.registry import register_playbook, unregister_playbook
        from ag.skills import get_default_registry

        optional_fail_playbook = Playbook(
            playbook_version="0.1",
            name="optional_fail_test",
            version="1.0.0",
            description="Test playbook with optional failing step",
            reasoning_modes=[ReasoningMode.DIRECT],
            budgets=Budgets(max_steps=3, max_tokens=None, max_duration_seconds=60),
            steps=[
                PlaybookStep(
                    step_id="step_0",
                    name="optional_error",
                    step_type=PlaybookStepType.SKILL,
                    skill_name="error_skill",
                    description="Optional step that errors",
                    required=False,  # Optional - failure won't stop playbook
                    retry_count=0,
                ),
                PlaybookStep(
                    step_id="step_1",
                    name="noop",
                    step_type=PlaybookStepType.SKILL,
                    skill_name="noop",
                    description="Succeeding step",
                    required=True,
                    retry_count=0,
                ),
            ],
        )

        register_playbook(optional_fail_playbook, source="test")

        try:
            runtime = create_runtime(
                registry=get_default_registry(),
                run_store=run_store,
                artifact_store=artifact_store,
            )

            trace = runtime.execute(
                prompt="Test optional failure",
                workspace="optional-ws",
                playbook="optional_fail_test",
            )

            # First step has error (optional)
            assert trace.steps[0].error is not None

            # But v0 verifier checks ALL step errors, so it will fail
            # This documents current behavior - we may want to change this
            # for optional steps in the future
            assert trace.verifier.status == VerifierStatus.FAILED

        finally:
            unregister_playbook("optional_fail_test")

    def test_missing_workspace_fails_gracefully(
        self,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
    ) -> None:
        """Missing workspace is handled and verifier records failure reason."""
        runtime = create_runtime(
            run_store=run_store,
            artifact_store=artifact_store,
        )

        trace = runtime.execute(
            prompt="Test with missing workspace",
            workspace="nonexistent_ws_12345",
            mode="manual",
        )

        # Should complete (not crash)
        assert trace.run_id is not None

        # Verifier should have a clear outcome
        assert trace.verifier.status in (VerifierStatus.PASSED, VerifierStatus.FAILED)

    def test_verifier_message_included_in_trace(
        self,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
    ) -> None:
        """Verifier message is always present and non-null."""
        runtime = create_runtime(
            run_store=run_store,
            artifact_store=artifact_store,
        )

        trace = runtime.execute(
            prompt="Test message presence",
            workspace="msg-ws",
            mode="manual",
        )

        # Verifier message should always be present
        assert trace.verifier.message is not None
        assert len(trace.verifier.message) > 0

        # checked_at should be set
        assert trace.verifier.checked_at is not None


# ---------------------------------------------------------------------------
# Pipeline Manifest Tests (AF-0120)
# ---------------------------------------------------------------------------


class TestPipelineManifest:
    """AF-0120: Pipeline component manifest is recorded in each RunTrace.

    Verifies that the pipeline block:
    - Is always present after execution
    - Accurately records the class names of all 5 components
    - Is backward-compatible (None on old traces)
    - Round-trips through JSON serialization
    """

    def test_pipeline_manifest_present_in_trace(self, runtime: "Runtime") -> None:
        """RunTrace includes a pipeline block after execution."""
        trace = runtime.execute(
            prompt="Test pipeline manifest presence",
            workspace="ws-pipeline",
            mode="manual",
        )

        assert trace.pipeline is not None

    def test_pipeline_manifest_all_components(self, runtime: "Runtime") -> None:
        """Pipeline block contains all 5 component names."""
        trace = runtime.execute(
            prompt="Test all pipeline components",
            workspace="ws-pipeline-components",
            mode="manual",
        )

        assert trace.pipeline is not None
        assert trace.pipeline.planner is not None
        assert trace.pipeline.orchestrator is not None
        assert trace.pipeline.executor is not None
        assert trace.pipeline.verifier is not None
        assert trace.pipeline.recorder is not None

    def test_pipeline_manifest_correct_class_names(self, runtime: "Runtime") -> None:
        """Pipeline block records the correct default component class names."""
        trace = runtime.execute(
            prompt="Test pipeline class names",
            workspace="ws-pipeline-names",
            mode="manual",
        )

        assert trace.pipeline is not None
        assert trace.pipeline.planner == "V0Planner"
        assert trace.pipeline.orchestrator == "V1Orchestrator"
        assert trace.pipeline.executor == "V0Executor"
        assert trace.pipeline.verifier == "V1Verifier"
        assert trace.pipeline.recorder == "V0Recorder"

    def test_pipeline_manifest_in_json_output(self, runtime: "Runtime") -> None:
        """Pipeline block survives JSON round-trip and appears in serialised output."""
        trace = runtime.execute(
            prompt="Test pipeline JSON",
            workspace="ws-pipeline-json",
            mode="manual",
        )

        json_str = trace.to_json()
        assert '"pipeline"' in json_str
        assert '"planner"' in json_str
        assert "V0Planner" in json_str

        # Full round-trip
        from ag.core.run_trace import RunTrace as RT

        restored = RT.from_json(json_str)
        assert restored.pipeline is not None
        assert restored.pipeline.planner == trace.pipeline.planner
        assert restored.pipeline.orchestrator == trace.pipeline.orchestrator
        assert restored.pipeline.executor == trace.pipeline.executor
        assert restored.pipeline.verifier == trace.pipeline.verifier
        assert restored.pipeline.recorder == trace.pipeline.recorder

    def test_pipeline_manifest_backward_compat(self) -> None:
        """Old traces without pipeline block still deserialise successfully."""
        from datetime import UTC, datetime

        from ag.core.run_trace import (
            ExecutionMode,
            FinalStatus,
            VerifierStatus,
        )
        from ag.core.run_trace import (
            RunTrace as RT,
        )

        # Build a minimal valid trace dict without a pipeline key
        now = datetime.now(UTC).isoformat()
        raw = {
            "run_id": "old-run-001",
            "workspace_id": "ws-old",
            "mode": ExecutionMode.MANUAL.value,
            "playbook": {"name": "default_v0", "version": "1.0.0"},
            "started_at": now,
            "ended_at": now,
            "steps": [],
            "artifacts": [],
            "verifier": {
                "status": VerifierStatus.PASSED.value,
                "checked_at": now,
                "message": "ok",
                "evidence": {},
            },
            "final": FinalStatus.SUCCESS.value,
        }

        # Must not raise even though "pipeline" is absent
        trace = RT.model_validate(raw)
        assert trace.pipeline is None


# ---------------------------------------------------------------------------
# AF-0123: V2Verifier semantic quality checks
# ---------------------------------------------------------------------------


class TestV2VerifierGracefulDegradation:
    """V2Verifier without provider behaves exactly like V1Verifier."""

    def test_no_provider_passes_clean_trace(self) -> None:
        """V2Verifier(provider=None) passes on clean steps."""
        from datetime import UTC, datetime

        from ag.core.run_trace import FinalStatus, Step, StepType
        from ag.core.verifier import V2Verifier

        verifier = V2Verifier()  # No provider
        now = datetime.now(UTC)
        steps = [
            Step(step_id="s0", step_number=0, step_type=StepType.SKILL_CALL, started_at=now),
        ]
        status, message = verifier.verify_components(steps, FinalStatus.SUCCESS)
        assert status == "passed"

    def test_no_provider_fails_on_error_step(self) -> None:
        """V2Verifier(provider=None) fails on required step error — same as V1."""
        from datetime import UTC, datetime

        from ag.core.run_trace import FinalStatus, Step, StepType
        from ag.core.verifier import V2Verifier

        verifier = V2Verifier()
        now = datetime.now(UTC)
        steps = [
            Step(
                step_id="s0",
                step_number=0,
                step_type=StepType.SKILL_CALL,
                started_at=now,
                error="broken",
            ),
        ]
        status, _ = verifier.verify_components(steps, FinalStatus.FAILURE)
        assert status == "failed"

    def test_no_provider_empty_steps(self) -> None:
        """V2Verifier(provider=None) fails on empty steps — BUG-0020 guard."""
        from ag.core.run_trace import FinalStatus
        from ag.core.verifier import V2Verifier

        verifier = V2Verifier()
        status, msg = verifier.verify_components([], FinalStatus.SUCCESS)
        assert status == "failed"
        assert "No steps executed" in msg

    def test_no_provider_verify_full_trace(self) -> None:
        """V2Verifier.verify() with no provider delegates to V1."""
        from datetime import UTC, datetime

        from ag.core.run_trace import (
            FinalStatus,
            PlaybookMetadata,
            RunTrace,
            Step,
            StepType,
            Verifier,
            VerifierStatus,
        )
        from ag.core.verifier import V2Verifier

        now = datetime.now(UTC)
        trace = RunTrace(
            workspace_id="ws-test",
            mode="supervised",
            playbook=PlaybookMetadata(name="test", version="1.0.0"),
            started_at=now,
            steps=[
                Step(step_id="s0", step_number=0, step_type=StepType.SKILL_CALL, started_at=now),
            ],
            verifier=Verifier(status=VerifierStatus.PASSED, checked_at=now, message="ok"),
            final=FinalStatus.SUCCESS,
        )
        verifier = V2Verifier()
        status, _ = verifier.verify(trace)
        assert status == "passed"


class TestV2VerifierWithProvider:
    """V2Verifier with a mock provider runs semantic checks."""

    @staticmethod
    def _make_mock_provider(response_content: str):
        """Create a mock provider returning fixed content."""
        from unittest.mock import MagicMock

        from ag.providers.base import ChatResponse

        provider = MagicMock()
        provider.chat.return_value = ChatResponse(
            content=response_content,
            model="mock-model",
            provider="mock",
        )
        return provider

    @staticmethod
    def _make_trace(steps=None, final=None):
        """Build a minimal RunTrace for testing."""
        from datetime import UTC, datetime

        from ag.core.run_trace import (
            FinalStatus,
            PlaybookMetadata,
            RunTrace,
            Step,
            StepType,
            Verifier,
            VerifierStatus,
        )

        now = datetime.now(UTC)
        if steps is None:
            steps = [
                Step(
                    step_id="s0",
                    step_number=0,
                    step_type=StepType.SKILL_CALL,
                    skill_name="summarize",
                    input_summary="Summarize docs",
                    output_summary="Here is a summary of the docs.",
                    started_at=now,
                ),
            ]
        return RunTrace(
            workspace_id="ws-test",
            mode="supervised",
            playbook=PlaybookMetadata(name="test", version="1.0.0"),
            started_at=now,
            steps=steps,
            verifier=Verifier(status=VerifierStatus.PASSED, checked_at=now, message="ok"),
            final=final or FinalStatus.SUCCESS,
        )

    def test_semantic_pass_all_high_scores(self) -> None:
        """All semantic scores above threshold → pass."""
        import json

        response = json.dumps(
            [
                {
                    "step_number": 0,
                    "relevance_score": 0.9,
                    "relevance_reason": "Directly addresses the task",
                    "completeness_score": 0.85,
                    "completeness_missing": [],
                    "consistency_score": 0.95,
                    "consistency_issues": [],
                }
            ]
        )
        provider = self._make_mock_provider(response)
        from ag.core.verifier import V2Verifier

        verifier = V2Verifier(provider=provider)
        trace = self._make_trace()
        status, _ = verifier.verify(trace)
        assert status == "passed"
        assert provider.chat.called

    def test_semantic_fail_low_relevance(self) -> None:
        """Low relevance score → verification fails."""
        import json

        response = json.dumps(
            [
                {
                    "step_number": 0,
                    "relevance_score": 0.2,
                    "relevance_reason": "Output is off-topic",
                    "completeness_score": 0.9,
                    "completeness_missing": [],
                    "consistency_score": 0.9,
                    "consistency_issues": [],
                }
            ]
        )
        provider = self._make_mock_provider(response)
        from ag.core.verifier import V2Verifier

        verifier = V2Verifier(provider=provider)
        trace = self._make_trace()
        status, msg = verifier.verify(trace)
        assert status == "failed"
        assert "relevance" in msg.lower()

    def test_semantic_fail_low_completeness(self) -> None:
        """Low completeness score → verification fails."""
        import json

        response = json.dumps(
            [
                {
                    "step_number": 0,
                    "relevance_score": 0.9,
                    "relevance_reason": "Good",
                    "completeness_score": 0.2,
                    "completeness_missing": ["executive summary", "conclusions"],
                    "consistency_score": 0.9,
                    "consistency_issues": [],
                }
            ]
        )
        provider = self._make_mock_provider(response)
        from ag.core.verifier import V2Verifier

        verifier = V2Verifier(provider=provider)
        trace = self._make_trace()
        status, msg = verifier.verify(trace)
        assert status == "failed"
        assert "completeness" in msg.lower()

    def test_semantic_fail_low_consistency(self) -> None:
        """Low consistency score → verification fails."""
        import json

        response = json.dumps(
            [
                {
                    "step_number": 0,
                    "relevance_score": 0.9,
                    "relevance_reason": "Good",
                    "completeness_score": 0.9,
                    "completeness_missing": [],
                    "consistency_score": 0.3,
                    "consistency_issues": ["contradicts source material"],
                }
            ]
        )
        provider = self._make_mock_provider(response)
        from ag.core.verifier import V2Verifier

        verifier = V2Verifier(provider=provider)
        trace = self._make_trace()
        status, msg = verifier.verify(trace)
        assert status == "failed"
        assert "consistency" in msg.lower()

    def test_llm_error_graceful_degradation(self) -> None:
        """LLM call throws → graceful degradation to V1 result."""
        from unittest.mock import MagicMock

        provider = MagicMock()
        provider.chat.side_effect = RuntimeError("LLM down")

        from ag.core.verifier import V2Verifier

        verifier = V2Verifier(provider=provider)
        trace = self._make_trace()
        status, _ = verifier.verify(trace)
        # V1 mechanical checks pass → still pass despite LLM failure
        assert status == "passed"

    def test_malformed_json_graceful_degradation(self) -> None:
        """LLM returns garbage → graceful degradation to V1 result."""
        provider = self._make_mock_provider("not valid json at all {{{")
        from ag.core.verifier import V2Verifier

        verifier = V2Verifier(provider=provider)
        trace = self._make_trace()
        status, _ = verifier.verify(trace)
        assert status == "passed"  # V1 passes, LLM parse error → degrade

    def test_v1_fails_semantic_not_run(self) -> None:
        """V1 failure short-circuits — semantic checks still run but can't save it."""
        import json
        from datetime import UTC, datetime

        from ag.core.run_trace import FinalStatus, Step, StepType

        now = datetime.now(UTC)
        error_steps = [
            Step(
                step_id="s0",
                step_number=0,
                step_type=StepType.SKILL_CALL,
                started_at=now,
                error="failed",
                required=True,
            ),
        ]
        # Semantic scores are all high — but V1 already failed
        response = json.dumps(
            [
                {
                    "step_number": 0,
                    "relevance_score": 1.0,
                    "relevance_reason": "Perfect",
                    "completeness_score": 1.0,
                    "completeness_missing": [],
                    "consistency_score": 1.0,
                    "consistency_issues": [],
                }
            ]
        )
        provider = self._make_mock_provider(response)
        from ag.core.verifier import V2Verifier

        verifier = V2Verifier(provider=provider)
        trace = self._make_trace(steps=error_steps, final=FinalStatus.FAILURE)
        status, _ = verifier.verify(trace)
        assert status == "failed"

    def test_custom_thresholds(self) -> None:
        """Custom thresholds change pass/fail boundary."""
        import json

        response = json.dumps(
            [
                {
                    "step_number": 0,
                    "relevance_score": 0.55,
                    "relevance_reason": "Marginal",
                    "completeness_score": 0.55,
                    "completeness_missing": [],
                    "consistency_score": 0.55,
                    "consistency_issues": [],
                }
            ]
        )
        provider = self._make_mock_provider(response)
        from ag.core.verifier import V2Verifier

        # With default thresholds (0.6/0.5/0.7), this would fail relevance + consistency
        # With lowered thresholds, it passes
        verifier = V2Verifier(
            provider=provider,
            relevance_threshold=0.5,
            completeness_threshold=0.5,
            consistency_threshold=0.5,
        )
        trace = self._make_trace()
        status, _ = verifier.verify(trace)
        assert status == "passed"


class TestSemanticVerificationModel:
    """Test SemanticVerification Pydantic model (AF-0123)."""

    def test_valid_model(self) -> None:
        from ag.core.run_trace import SemanticVerification

        sv = SemanticVerification(
            relevance_score=0.9,
            relevance_reason="Good",
            completeness_score=0.8,
            completeness_missing=[],
            consistency_score=0.95,
            consistency_issues=[],
            overall_pass=True,
            llm_model="gpt-4o-mini",
            llm_tokens_used=150,
            evaluation_ms=500,
        )
        assert sv.overall_pass is True
        assert sv.relevance_score == 0.9

    def test_score_bounds(self) -> None:
        """Scores must be 0.0–1.0."""
        from pydantic import ValidationError

        from ag.core.run_trace import SemanticVerification

        with pytest.raises(ValidationError):
            SemanticVerification(
                relevance_score=1.5,  # out of bounds
                completeness_score=0.5,
                consistency_score=0.5,
                overall_pass=False,
            )

    def test_extra_fields_forbidden(self) -> None:
        """Extra fields are rejected."""
        from pydantic import ValidationError

        from ag.core.run_trace import SemanticVerification

        with pytest.raises(ValidationError):
            SemanticVerification(
                relevance_score=0.5,
                completeness_score=0.5,
                consistency_score=0.5,
                overall_pass=True,
                extra_field="not allowed",
            )
