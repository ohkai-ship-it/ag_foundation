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
    RunTrace,
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


@pytest.fixture
def workspace_setup(temp_root: Path, monkeypatch: pytest.MonkeyPatch):
    """Set up workspace environment for CLI tests.

    Creates the 'ws-test' workspace and sets AG_WORKSPACE_DIR env var.
    """
    from ag.storage import Workspace

    # Create the workspace used by most tests
    ws = Workspace("ws-test", temp_root)
    ws.ensure_exists()

    # Set the workspace directory via environment variable
    monkeypatch.setenv("AG_WORKSPACE_DIR", str(temp_root))

    return temp_root


# ---------------------------------------------------------------------------
# Manual Mode Gate Tests (Extended)
# ---------------------------------------------------------------------------


class TestManualModeGateExtended:
    """Extended manual mode gate tests."""

    def test_manual_mode_banner_printed(
        self, env_with_dev: None, workspace_setup: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Manual mode prints correct banner."""
        result = runner.invoke(
            app,
            ["run", "--mode", "manual", "--workspace", "ws-test", "Test task"],
            env={"AG_WORKSPACE_DIR": str(workspace_setup), "AG_DEV": "1"},
        )

        assert "DEV MODE: manual (LLMs disabled)" in result.stdout

    def test_manual_mode_trace_has_manual_mode(
        self, env_with_dev: None, workspace_setup: Path
    ) -> None:
        """Manual mode sets trace.mode to 'manual'."""
        result = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test task"]
        )

        assert result.exit_code == 0
        trace_data = json.loads(result.stdout)
        assert trace_data["mode"] == "manual"

    def test_without_ag_dev_manual_mode_fails(self, workspace_setup: Path) -> None:
        """Without AG_DEV=1, manual mode fails."""
        # Ensure AG_DEV is not set
        if "AG_DEV" in os.environ:
            del os.environ["AG_DEV"]

        result = runner.invoke(
            app,
            ["run", "--mode", "manual", "--workspace", "ws-test", "Test task"],
            env={"AG_WORKSPACE_DIR": str(workspace_setup)},
        )

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
        with create_runtime(
            run_store=run_store,
            artifact_store=artifact_store,
        ) as runtime:
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

    def test_cli_mode_label_matches_trace(self, env_with_dev: None, workspace_setup: Path) -> None:
        """CLI mode label matches RunTrace.mode."""
        # Run in manual mode
        result = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test"]
        )

        trace_data = json.loads(result.stdout)

        # Verify mode in trace
        assert trace_data["mode"] == "manual"

    def test_cli_verifier_status_matches_trace(
        self, env_with_dev: None, workspace_setup: Path
    ) -> None:
        """CLI verifier status matches RunTrace.verifier.status."""
        result = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test"]
        )

        trace_data = json.loads(result.stdout)

        # Verify verifier status is present and valid
        assert "verifier" in trace_data
        assert "status" in trace_data["verifier"]
        assert trace_data["verifier"]["status"] in ["passed", "failed", "pending", "skipped"]

    def test_cli_duration_matches_trace(self, env_with_dev: None, workspace_setup: Path) -> None:
        """CLI duration matches RunTrace.duration_ms."""
        result = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test"]
        )

        trace_data = json.loads(result.stdout)

        # Duration should be present and non-negative
        assert "duration_ms" in trace_data
        assert trace_data["duration_ms"] >= 0

    def test_cli_workspace_source_matches_trace(
        self, env_with_dev: None, workspace_setup: Path
    ) -> None:
        """AF-0030/AF-0031: CLI workspace_source label matches RunTrace field."""
        result = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test"]
        )

        trace_data = json.loads(result.stdout)

        # workspace_source should be present and valid
        assert "workspace_source" in trace_data
        assert trace_data["workspace_source"] in ["cli", "persisted", "env", "bootstrap", None]

    def test_extract_labels_includes_workspace_source(
        self, run_store: SQLiteRunStore, artifact_store: SQLiteArtifactStore
    ) -> None:
        """AF-0031: extract_labels includes workspace_source from trace."""
        with create_runtime(
            run_store=run_store,
            artifact_store=artifact_store,
        ) as runtime:
            trace = runtime.execute(
                prompt="Test task",
                workspace="ws-test",
                mode="manual",
                workspace_source="cli",
            )

            labels = extract_labels(trace)

            # workspace_source should be in labels and match trace
            assert "workspace_source" in labels
            assert labels["workspace_source"] == trace.workspace_source.value


# ---------------------------------------------------------------------------
# ag runs show --json Schema Conformance Tests
# ---------------------------------------------------------------------------


class TestRunsShowJsonConformance:
    """Tests that ag runs show --json conforms to RunTrace schema."""

    def test_runs_show_json_has_all_required_fields(
        self, env_with_dev: None, workspace_setup: Path
    ) -> None:
        """ag runs show --json output has all RunTrace v0.1 required fields."""
        # First create a run
        result = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test"]
        )
        trace_data = json.loads(result.stdout)
        run_id = trace_data["run_id"]

        # Now show it
        result = runner.invoke(app, ["runs", "show", run_id, "--workspace", "ws-test", "--json"])

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
        self, env_with_dev: None, workspace_setup: Path
    ) -> None:
        """ag runs show --json output can be parsed back as RunTrace."""
        # Create a run
        result = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test"]
        )
        trace_data = json.loads(result.stdout)
        run_id = trace_data["run_id"]

        # Show it
        result = runner.invoke(app, ["runs", "show", run_id, "--workspace", "ws-test", "--json"])

        # Parse as RunTrace
        parsed = RunTrace.from_json(result.stdout)

        assert parsed.run_id == run_id
        assert parsed.workspace_id == "ws-test"
        assert parsed.mode == ExecutionMode.MANUAL

    def test_runs_show_json_matches_original_trace(
        self, env_with_dev: None, workspace_setup: Path
    ) -> None:
        """ag runs show --json output matches original trace from ag run."""
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

    def test_runs_list_shows_runs(self, env_with_dev: None, workspace_setup: Path) -> None:
        """ag runs list shows created runs."""
        # Create a run
        result = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test"]
        )
        trace_data = json.loads(result.stdout)
        run_id = trace_data["run_id"]

        # List runs
        result = runner.invoke(app, ["runs", "list", "--workspace", "ws-test", "--json"])

        assert result.exit_code == 0
        # AF-0088: JSON output includes pagination info
        data = json.loads(result.stdout)
        runs = data["runs"]
        assert len(runs) >= 1
        assert any(r["run_id"] == run_id for r in runs)

    def test_runs_list_empty_workspace(
        self, temp_root: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """ag runs list on empty workspace returns empty list."""
        from ag.storage import Workspace

        monkeypatch.setenv("AG_WORKSPACE_DIR", str(temp_root))
        # Create empty workspace for the test
        ws = Workspace("empty-ws", temp_root)
        ws.ensure_exists()

        result = runner.invoke(
            app,
            ["runs", "list", "--workspace", "empty-ws", "--json"],
            env={"AG_WORKSPACE_DIR": str(temp_root)},
        )

        assert result.exit_code == 0
        # AF-0088: JSON output includes pagination info
        data = json.loads(result.stdout)
        assert data["runs"] == []
        assert data["total"] == 0

    def test_runs_list_requires_workspace(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """ag runs list requires --workspace or default workspace (AF-0097)."""
        # Remove AG_WORKSPACE env var to ensure no fallback
        monkeypatch.delenv("AG_WORKSPACE", raising=False)

        result = runner.invoke(app, ["runs", "list"])

        # With AF-0097, command now uses default workspace if available
        # If no default set, it should succeed with empty list or fail gracefully
        # The implementation falls back to persisted default, then env var
        assert result.exit_code == 0 or "workspace" in result.stdout.lower()


# ---------------------------------------------------------------------------
# Label Consistency Tests
# ---------------------------------------------------------------------------


class TestLabelConsistency:
    """Tests that labels are consistent across CLI commands."""

    def test_run_and_show_labels_match(self, env_with_dev: None, workspace_setup: Path) -> None:
        """Labels from ag run match labels from ag runs show."""
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


# ---------------------------------------------------------------------------
# AF-0032: ag runs stats Tests
# ---------------------------------------------------------------------------


class TestRunsStats:
    """Tests for ag runs stats command (AF-0032)."""

    def test_stats_empty_workspace(self, temp_root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """ag runs stats on empty workspace shows zero runs."""
        from ag.storage import Workspace

        monkeypatch.setenv("AG_WORKSPACE_DIR", str(temp_root))
        ws = Workspace("empty-stats-ws", temp_root)
        ws.ensure_exists()

        result = runner.invoke(
            app,
            ["runs", "stats", "--workspace", "empty-stats-ws", "--json"],
            env={"AG_WORKSPACE_DIR": str(temp_root)},
        )

        assert result.exit_code == 0
        stats = json.loads(result.stdout)
        assert stats["total_runs"] == 0

    def test_stats_with_runs(self, env_with_dev: None, workspace_setup: Path) -> None:
        """ag runs stats shows correct stats after creating runs."""
        # Create a few runs
        for _ in range(3):
            runner.invoke(
                app, ["run", "--mode", "manual", "--workspace", "ws-test", "--json", "Test"]
            )

        result = runner.invoke(app, ["runs", "stats", "--workspace", "ws-test", "--json"])

        assert result.exit_code == 0
        stats = json.loads(result.stdout)

        # Should have at least 3 runs
        assert stats["total_runs"] >= 3
        assert "by_status" in stats
        assert "by_verifier_status" in stats
        assert "by_mode" in stats
        assert "avg_duration_ms" in stats

    def test_stats_requires_workspace(self) -> None:
        """ag runs stats requires --workspace flag."""
        result = runner.invoke(app, ["runs", "stats"])
        assert result.exit_code == 1  # Should fail without workspace
