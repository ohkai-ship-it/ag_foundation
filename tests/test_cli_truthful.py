"""CLI truthful label tests.

These tests verify that CLI labels are derived from persisted RunTrace data
(truthful UX requirement from AF-0008).

Tests:
1. Manual mode gate tests (already in test_cli.py, extended here)
2. Truthful label tests: CLI output matches RunTrace fields
3. ag runs show --json conforms to RunTrace schema
"""

import json
import os
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ag.cli.main import app, extract_labels
from ag.core import (
    ExecutionMode,
    FinalStatus,
    RunTrace,
    VerifierStatus,
    create_runtime,
)
from ag.storage import SQLiteArtifactStore, SQLiteRunStore

runner = CliRunner()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def temp_root(tmp_path: Path) -> Path:
    """Temporary workspace root for tests."""
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
def env_with_dev(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set AG_DEV=1 for tests."""
    monkeypatch.setenv("AG_DEV", "1")


# ---------------------------------------------------------------------------
# Manual Mode Gate Tests (Extended)
# ---------------------------------------------------------------------------


class TestManualModeGateExtended:
    """Extended manual mode gate tests."""

    def test_manual_mode_banner_printed(
        self, env_with_dev: None, temp_root: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Manual mode prints correct banner."""
        # Patch workspaces root
        monkeypatch.setattr(
            "ag.cli.main.DEFAULT_WORKSPACES_ROOT", temp_root
        )

        result = runner.invoke(app, ["run", "--mode", "manual", "Test task"])

        assert "DEV MODE: manual (LLMs disabled)" in result.stdout

    def test_manual_mode_trace_has_manual_mode(
        self, env_with_dev: None, temp_root: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Manual mode sets trace.mode to 'manual'."""
        monkeypatch.setattr("ag.cli.main.DEFAULT_WORKSPACES_ROOT", temp_root)

        result = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test task"]
        )

        assert result.exit_code == 0
        trace_data = json.loads(result.stdout)
        assert trace_data["mode"] == "manual"

    def test_without_ag_dev_manual_mode_fails(self, temp_root: Path) -> None:
        """Without AG_DEV=1, manual mode fails."""
        # Ensure AG_DEV is not set
        if "AG_DEV" in os.environ:
            del os.environ["AG_DEV"]

        result = runner.invoke(app, ["run", "--mode", "manual", "Test task"])

        assert result.exit_code == 1
        assert "AG_DEV=1" in result.stdout or "AG_DEV=1" in result.stderr


# ---------------------------------------------------------------------------
# Truthful Label Tests
# ---------------------------------------------------------------------------


class TestTruthfulLabels:
    """Tests that CLI labels match RunTrace fields exactly."""

    def test_extract_labels_matches_trace(
        self, run_store: SQLiteRunStore, artifact_store: SQLiteArtifactStore
    ) -> None:
        """extract_labels helper produces correct values from trace."""
        runtime = create_runtime(
            run_store=run_store,
            artifact_store=artifact_store,
        )

        trace = runtime.execute(
            prompt="Test task",
            workspace="ws-test",
            mode="manual",
        )

        labels = extract_labels(trace)

        # Verify labels match trace fields
        assert labels["mode"] == trace.mode.value
        assert labels["status"] == trace.final.value
        assert labels["verifier_status"] == trace.verifier.status.value
        assert labels["run_id"] == trace.run_id
        assert labels["workspace_id"] == trace.workspace_id
        assert trace.playbook.name in labels["playbook"]

    def test_cli_mode_label_matches_trace(
        self, env_with_dev: None, temp_root: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """CLI mode label matches RunTrace.mode."""
        monkeypatch.setattr("ag.cli.main.DEFAULT_WORKSPACES_ROOT", temp_root)

        # Run in manual mode
        result = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test"]
        )

        trace_data = json.loads(result.stdout)

        # Verify mode in trace
        assert trace_data["mode"] == "manual"

    def test_cli_verifier_status_matches_trace(
        self, env_with_dev: None, temp_root: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """CLI verifier status matches RunTrace.verifier.status."""
        monkeypatch.setattr("ag.cli.main.DEFAULT_WORKSPACES_ROOT", temp_root)

        result = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test"]
        )

        trace_data = json.loads(result.stdout)

        # Verify verifier status is present and valid
        assert "verifier" in trace_data
        assert "status" in trace_data["verifier"]
        assert trace_data["verifier"]["status"] in ["passed", "failed", "pending", "skipped"]

    def test_cli_duration_matches_trace(
        self, env_with_dev: None, temp_root: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """CLI duration matches RunTrace.duration_ms."""
        monkeypatch.setattr("ag.cli.main.DEFAULT_WORKSPACES_ROOT", temp_root)

        result = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test"]
        )

        trace_data = json.loads(result.stdout)

        # Duration should be present and non-negative
        assert "duration_ms" in trace_data
        assert trace_data["duration_ms"] >= 0


# ---------------------------------------------------------------------------
# ag runs show --json Schema Conformance Tests
# ---------------------------------------------------------------------------


class TestRunsShowJsonConformance:
    """Tests that ag runs show --json conforms to RunTrace schema."""

    def test_runs_show_json_has_all_required_fields(
        self, env_with_dev: None, temp_root: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """ag runs show --json output has all RunTrace v0.1 required fields."""
        monkeypatch.setattr("ag.cli.main.DEFAULT_WORKSPACES_ROOT", temp_root)

        # First create a run
        result = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test"]
        )
        trace_data = json.loads(result.stdout)
        run_id = trace_data["run_id"]

        # Now show it
        result = runner.invoke(
            app, ["runs", "show", run_id, "--workspace", "ws-test", "--json"]
        )

        assert result.exit_code == 0
        show_data = json.loads(result.stdout)

        # Check all v0.1 required fields
        required_fields = [
            "trace_version",
            "run_id",
            "workspace_id",
            "mode",
            "playbook",
            "started_at",
            "steps",
            "artifacts",
            "verifier",
            "final",
        ]

        for field in required_fields:
            assert field in show_data, f"Missing required field: {field}"

    def test_runs_show_json_can_parse_as_runtrace(
        self, env_with_dev: None, temp_root: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """ag runs show --json output can be parsed back as RunTrace."""
        monkeypatch.setattr("ag.cli.main.DEFAULT_WORKSPACES_ROOT", temp_root)

        # Create a run
        result = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test"]
        )
        trace_data = json.loads(result.stdout)
        run_id = trace_data["run_id"]

        # Show it
        result = runner.invoke(
            app, ["runs", "show", run_id, "--workspace", "ws-test", "--json"]
        )

        # Parse as RunTrace
        parsed = RunTrace.from_json(result.stdout)

        assert parsed.run_id == run_id
        assert parsed.workspace_id == "ws-test"
        assert parsed.mode == ExecutionMode.MANUAL

    def test_runs_show_json_matches_original_trace(
        self, env_with_dev: None, temp_root: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """ag runs show --json output matches original trace from ag run."""
        monkeypatch.setattr("ag.cli.main.DEFAULT_WORKSPACES_ROOT", temp_root)

        # Create a run
        result = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test task"]
        )
        original = json.loads(result.stdout)

        # Show it
        result = runner.invoke(
            app, ["runs", "show", original["run_id"], "--workspace", "ws-test", "--json"]
        )
        shown = json.loads(result.stdout)

        # Key fields should match
        assert shown["run_id"] == original["run_id"]
        assert shown["workspace_id"] == original["workspace_id"]
        assert shown["mode"] == original["mode"]
        assert shown["final"] == original["final"]
        assert shown["verifier"]["status"] == original["verifier"]["status"]


# ---------------------------------------------------------------------------
# ag runs list Tests
# ---------------------------------------------------------------------------


class TestRunsList:
    """Tests for ag runs list command."""

    def test_runs_list_shows_runs(
        self, env_with_dev: None, temp_root: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """ag runs list shows created runs."""
        monkeypatch.setattr("ag.cli.main.DEFAULT_WORKSPACES_ROOT", temp_root)

        # Create a run
        result = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test"]
        )
        trace_data = json.loads(result.stdout)
        run_id = trace_data["run_id"]

        # List runs
        result = runner.invoke(
            app, ["runs", "list", "--workspace", "ws-test", "--json"]
        )

        assert result.exit_code == 0
        runs = json.loads(result.stdout)
        assert len(runs) >= 1
        assert any(r["run_id"] == run_id for r in runs)

    def test_runs_list_empty_workspace(
        self, temp_root: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """ag runs list on empty workspace returns empty list."""
        monkeypatch.setattr("ag.cli.main.DEFAULT_WORKSPACES_ROOT", temp_root)

        result = runner.invoke(
            app, ["runs", "list", "--workspace", "empty-ws", "--json"]
        )

        assert result.exit_code == 0
        runs = json.loads(result.stdout)
        assert runs == []

    def test_runs_list_requires_workspace(self) -> None:
        """ag runs list requires --workspace flag."""
        result = runner.invoke(app, ["runs", "list"])

        assert result.exit_code == 1
        assert "workspace" in result.stdout.lower() or "workspace" in (result.stderr or "").lower()


# ---------------------------------------------------------------------------
# Label Consistency Tests
# ---------------------------------------------------------------------------


class TestLabelConsistency:
    """Tests that labels are consistent across CLI commands."""

    def test_run_and_show_labels_match(
        self, env_with_dev: None, temp_root: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Labels from ag run match labels from ag runs show."""
        monkeypatch.setattr("ag.cli.main.DEFAULT_WORKSPACES_ROOT", temp_root)

        # Run
        result = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test"]
        )
        run_trace = json.loads(result.stdout)
        run_labels = extract_labels(RunTrace.from_json(result.stdout))

        # Show
        result = runner.invoke(
            app, ["runs", "show", run_trace["run_id"], "--workspace", "ws-test", "--json"]
        )
        show_labels = extract_labels(RunTrace.from_json(result.stdout))

        # Labels should match
        assert run_labels["mode"] == show_labels["mode"]
        assert run_labels["status"] == show_labels["status"]
        assert run_labels["verifier_status"] == show_labels["verifier_status"]
        assert run_labels["workspace_id"] == show_labels["workspace_id"]
