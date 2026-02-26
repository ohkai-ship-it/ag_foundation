"""AF-0019: Delegation playbook integration tests.

Tests for:
- Manual delegated run using stub skills
- Delegated playbook CLI integration
- Multi-step trace with subtasks in JSON output
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ag.cli.main import app
from ag.core.playbooks import get_playbook, list_playbooks
from ag.core.run_trace import StepType, Subtask
from ag.core.runtime import Runtime
from ag.skills import get_default_registry
from ag.storage import Workspace

runner = CliRunner()


# ---------------------------------------------------------------------------
# Test: delegate_v0 playbook structure
# ---------------------------------------------------------------------------


class TestDelegateV0Playbook:
    """Test delegate_v0 playbook definition."""

    def test_delegate_v0_exists(self) -> None:
        """delegate_v0 playbook can be retrieved."""
        playbook = get_playbook("delegate_v0")
        assert playbook is not None
        assert playbook.name == "delegate_v0"

    def test_delegate_v0_alias(self) -> None:
        """'delegate' alias returns delegate_v0."""
        playbook = get_playbook("delegate")
        assert playbook is not None
        assert playbook.name == "delegate_v0"

    def test_delegate_v0_in_list(self) -> None:
        """delegate_v0 appears in playbook list."""
        playbooks = list_playbooks()
        assert "delegate_v0" in playbooks

    def test_delegate_v0_has_six_steps(self) -> None:
        """delegate_v0 has at least 6 steps per AF-0019."""
        playbook = get_playbook("delegate_v0")
        assert playbook is not None
        assert len(playbook.steps) >= 6
        # Check expected step names
        step_names = [s.name for s in playbook.steps]
        assert "normalize" in step_names
        assert "plan" in step_names
        assert "execute_subtask_1" in step_names
        assert "execute_subtask_2" in step_names
        assert "verify" in step_names
        assert "finalize" in step_names

    def test_delegate_v0_plan_step_has_min_subtasks_param(self) -> None:
        """Plan step has min_subtasks parameter."""
        playbook = get_playbook("delegate_v0")
        assert playbook is not None
        plan_step = next(s for s in playbook.steps if s.name == "plan")
        assert plan_step.parameters.get("min_subtasks") == 2


# ---------------------------------------------------------------------------
# Test: Delegation skills registration
# ---------------------------------------------------------------------------


class TestDelegationSkills:
    """Test delegation skills are registered."""

    def test_normalize_input_registered(self) -> None:
        """normalize_input skill exists."""
        registry = get_default_registry()
        assert registry.has("normalize_input")

    def test_plan_subtasks_registered(self) -> None:
        """plan_subtasks skill exists."""
        registry = get_default_registry()
        assert registry.has("plan_subtasks")

    def test_execute_subtask_registered(self) -> None:
        """execute_subtask skill exists."""
        registry = get_default_registry()
        assert registry.has("execute_subtask")

    def test_verify_delegation_registered(self) -> None:
        """verify_delegation skill exists."""
        registry = get_default_registry()
        assert registry.has("verify_delegation")

    def test_finalize_result_registered(self) -> None:
        """finalize_result skill exists."""
        registry = get_default_registry()
        assert registry.has("finalize_result")

    def test_plan_subtasks_returns_at_least_two(self) -> None:
        """plan_subtasks generates at least 2 subtasks."""
        registry = get_default_registry()
        success, summary, result = registry.execute(
            "plan_subtasks", {"prompt": "Test task", "min_subtasks": 2}
        )
        assert success is True
        assert "subtasks" in result
        assert len(result["subtasks"]) >= 2


# ---------------------------------------------------------------------------
# Test: Manual delegated run
# ---------------------------------------------------------------------------


class TestManualDelegatedRun:
    """Test delegation playbook execution in manual mode."""

    def test_delegate_v0_executes_all_steps(self) -> None:
        """All 6 steps execute successfully."""
        with Runtime() as runtime:
            trace = runtime.execute(
                prompt="Analyze this code and explain it",
                workspace="test-delegate-ws",
                mode="manual",
                playbook="delegate_v0",
            )

            # Should have 6 steps
            assert len(trace.steps) == 6

            # All steps should succeed
            for step in trace.steps:
                assert step.error is None, f"Step {step.step_number} failed: {step.error}"

    def test_delegate_v0_plan_step_has_subtasks(self) -> None:
        """Plan step records subtasks in trace."""
        with Runtime() as runtime:
            trace = runtime.execute(
                prompt="Test task",
                workspace="test-subtask-ws",
                mode="manual",
                playbook="delegate_v0",
            )

            # Find the plan step (step 1)
            plan_step = next(s for s in trace.steps if s.skill_name == "plan_subtasks")
            assert plan_step.subtasks is not None
            assert len(plan_step.subtasks) >= 2
            # Check subtask structure
            for subtask in plan_step.subtasks:
                assert isinstance(subtask, Subtask)
                assert subtask.subtask_id
                assert subtask.description

    def test_delegate_v0_plan_step_type_is_planning(self) -> None:
        """Plan step has PLANNING step type."""
        with Runtime() as runtime:
            trace = runtime.execute(
                prompt="Test task",
                workspace="test-steptype-ws",
                mode="manual",
                playbook="delegate_v0",
            )

            plan_step = next(s for s in trace.steps if s.skill_name == "plan_subtasks")
            assert plan_step.step_type == StepType.PLANNING

    def test_delegate_v0_trace_has_delegation_metadata(self) -> None:
        """Trace playbook metadata shows delegate_v0."""
        with Runtime() as runtime:
            trace = runtime.execute(
                prompt="Test task",
                workspace="test-meta-ws",
                mode="manual",
                playbook="delegate_v0",
            )

            assert trace.playbook.name == "delegate_v0"
            assert trace.playbook.version == "1.0.0"


# ---------------------------------------------------------------------------
# Test: CLI integration
# ---------------------------------------------------------------------------


class TestDelegationCLI:
    """Test CLI with delegation playbook."""

    def test_cli_run_with_delegate_playbook(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """CLI can run delegate_v0 playbook."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            workspace = f"cli-delegate-{os.getpid()}"

            # Set workspace root via environment variable
            monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

            # Create workspace
            ws = Workspace(workspace, tmp_path)
            ws.ensure_exists()

            result = runner.invoke(
                app,
                [
                    "run",
                    "Test delegation task",
                    "--workspace",
                    workspace,
                    "--mode",
                    "manual",
                    "--playbook",
                    "delegate_v0",
                ],
                env={"AG_DEV": "1", "AG_WORKSPACE_DIR": str(tmp_path)},
            )
            assert result.exit_code == 0, f"CLI failed: {result.output}"
            # Should mention the playbook
            assert "delegate_v0" in result.output or "completed" in result.output.lower()

    def test_cli_runs_show_json_has_subtasks(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """ag runs show --json displays subtasks from delegation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            workspace = f"cli-json-{os.getpid()}"
            env = {"AG_DEV": "1", "AG_WORKSPACE_DIR": str(tmp_path)}

            # Set workspace root via environment variable
            monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

            # Create workspace
            ws = Workspace(workspace, tmp_path)
            ws.ensure_exists()

            # First, run the delegation playbook
            run_result = runner.invoke(
                app,
                [
                    "run",
                    "Test task",
                    "--workspace",
                    workspace,
                    "--mode",
                    "manual",
                    "--playbook",
                    "delegate_v0",
                ],
                env=env,
            )
            assert run_result.exit_code == 0

            # Now get the list of runs with --json for reliable parsing
            list_result = runner.invoke(
                app,
                ["runs", "list", "--workspace", workspace, "--json"],
                env=env,
            )
            assert list_result.exit_code == 0
            runs_data = json.loads(list_result.stdout)
            assert len(runs_data) > 0
            run_id = runs_data[0]["run_id"]

            # Now show the run as JSON
            show_result = runner.invoke(
                app,
                ["runs", "show", run_id, "--workspace", workspace, "--json"],
                env=env,
            )
            assert show_result.exit_code == 0

            # Parse the JSON
            trace_json = json.loads(show_result.stdout)

            # Should have 6 steps
            assert len(trace_json["steps"]) == 6

            # Find plan step and check subtasks
            plan_step = next(
                s for s in trace_json["steps"] if s.get("skill_name") == "plan_subtasks"
            )
            assert plan_step["step_type"] == "planning"
            assert "subtasks" in plan_step
            assert len(plan_step["subtasks"]) >= 2

    def test_cli_delegate_with_default_alias(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """CLI accepts 'delegate' as playbook name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            workspace = f"cli-alias-{os.getpid()}"

            # Set workspace root via environment variable
            monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

            # Create workspace
            ws = Workspace(workspace, tmp_path)
            ws.ensure_exists()

            result = runner.invoke(
                app,
                [
                    "run",
                    "Test",
                    "--workspace",
                    workspace,
                    "--mode",
                    "manual",
                    "--playbook",
                    "delegate",  # Use alias
                ],
                env={"AG_DEV": "1", "AG_WORKSPACE_DIR": str(tmp_path)},
            )
            assert result.exit_code == 0


# ---------------------------------------------------------------------------
# Test: Subtask model
# ---------------------------------------------------------------------------


class TestSubtaskModel:
    """Test Subtask model from run_trace."""

    def test_subtask_creation(self) -> None:
        """Subtask can be created with required fields."""
        subtask = Subtask(
            subtask_id="st-001",
            description="Analyze requirements",
        )
        assert subtask.subtask_id == "st-001"
        assert subtask.description == "Analyze requirements"
        assert subtask.status == "pending"
        assert subtask.result_summary is None

    def test_subtask_serialization(self) -> None:
        """Subtask serializes to dict correctly."""
        subtask = Subtask(
            subtask_id="st-002",
            description="Execute plan",
            status="completed",
            result_summary="Done",
        )
        data = subtask.model_dump()
        assert data["subtask_id"] == "st-002"
        assert data["status"] == "completed"
        assert data["result_summary"] == "Done"

    def test_subtask_forbids_extra_fields(self) -> None:
        """Subtask rejects unknown fields (pydantic extra=forbid)."""
        with pytest.raises(Exception):  # ValidationError
            Subtask(
                subtask_id="st-003",
                description="Test",
                unknown_field="rejected",  # type: ignore
            )


# ---------------------------------------------------------------------------
# Test: StepType.PLANNING
# ---------------------------------------------------------------------------


class TestPlanningStepType:
    """Test PLANNING step type added for delegation."""

    def test_planning_step_type_exists(self) -> None:
        """PLANNING is a valid StepType."""
        assert StepType.PLANNING == "planning"
        assert StepType.PLANNING.value == "planning"

    def test_planning_in_step_types(self) -> None:
        """PLANNING is in the StepType enum."""
        step_types = [st.value for st in StepType]
        assert "planning" in step_types
