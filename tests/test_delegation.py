"""AF-0079: Delegation playbook tests (stub-based).

Tests for delegate_v0 playbook which now uses echo stubs
after V1 delegation skills were removed in AF0079.

Original V1 delegation tests verified:
- 6-step playbook (normalize, plan, execute_x2, verify, finalize)
- Subtask generation from plan_subtasks skill
- Planning step type

Current V2 stub tests verify:
- 2-step echo playbook structure
- Basic playbook execution
- CLI integration
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ag.cli.main import app
from ag.core.runtime import Runtime
from ag.playbooks import get_playbook, list_playbooks
from ag.storage import Workspace

runner = CliRunner()


# ---------------------------------------------------------------------------
# Test: delegate_v0 playbook structure (AF0079 updated)
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

    def test_delegate_v0_has_echo_steps(self) -> None:
        """delegate_v0 uses echo_tool steps (AF0079 stub-based)."""
        playbook = get_playbook("delegate_v0")
        assert playbook is not None
        # Now has 2 echo steps instead of 6 delegation steps
        assert len(playbook.steps) == 2
        # Both steps use echo_tool
        for step in playbook.steps:
            assert step.skill_name == "echo_tool"

    def test_delegate_v0_metadata_indicates_stub(self) -> None:
        """Playbook metadata indicates it's a test stub."""
        playbook = get_playbook("delegate_v0")
        assert playbook is not None
        assert playbook.metadata.get("stability") == "test"
        assert "AF0079" in playbook.metadata.get("note", "")


# ---------------------------------------------------------------------------
# Test: Manual delegated run (AF0079 updated)
# ---------------------------------------------------------------------------


class TestManualDelegatedRun:
    """Test delegation playbook execution in manual mode."""

    def test_delegate_v0_executes_echo_steps(self) -> None:
        """Echo steps execute successfully."""
        with Runtime() as runtime:
            trace = runtime.execute(
                prompt="Test delegation stub",
                workspace="test-delegate-ws",
                mode="manual",
                playbook="delegate_v0",
            )

            # Should have 2 steps (echo stubs)
            assert len(trace.steps) == 2

            # All steps should succeed
            for step in trace.steps:
                assert step.error is None, f"Step {step.step_number} failed: {step.error}"
                assert step.skill_name == "echo_tool"

    def test_delegate_v0_trace_has_playbook_metadata(self) -> None:
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

    def test_delegate_v0_verifier_passes(self) -> None:
        """Verifier passes for successful execution."""
        with Runtime() as runtime:
            trace = runtime.execute(
                prompt="Test task",
                workspace="test-verifier-ws",
                mode="manual",
                playbook="delegate_v0",
            )

            assert trace.verifier.status.value == "passed"


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

    def test_cli_runs_show_json_has_echo_steps(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """ag runs show --json displays echo steps from delegation stub."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            workspace = f"cli-json-{os.getpid()}"
            env = {"AG_DEV": "1", "AG_WORKSPACE_DIR": str(tmp_path)}

            # Set workspace root via environment variable
            monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

            # Create workspace
            ws = Workspace(workspace, tmp_path)
            ws.ensure_exists()

            # Run the delegation playbook
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

            # Get the list of runs with --json for reliable parsing
            list_result = runner.invoke(
                app,
                ["runs", "list", "--workspace", workspace, "--json"],
                env=env,
            )
            assert list_result.exit_code == 0
            runs_data = json.loads(list_result.stdout)
            assert len(runs_data) > 0
            run_id = runs_data[0]["run_id"]

            # Show the run as JSON
            show_result = runner.invoke(
                app,
                ["runs", "show", run_id, "--workspace", workspace, "--json"],
                env=env,
            )
            assert show_result.exit_code == 0

            # Parse the JSON
            trace_json = json.loads(show_result.stdout)

            # Should have 2 steps (echo stubs)
            assert len(trace_json["steps"]) == 2

            # Both steps should use echo_tool
            for step in trace_json["steps"]:
                assert step["skill_name"] == "echo_tool"

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
            # Should show playbook name in output
            assert "delegate_v0" in result.output
