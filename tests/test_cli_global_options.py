"""AF-0011: CLI global options tests.

Tests for:
- Help includes global options (--workspace, --json, --quiet, --verbose)
- Global options propagate to subcommands
- Precedence: command flag > global flag > defaults
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from typer.testing import CliRunner

from ag.cli.main import CLIContext, app

runner = CliRunner()


# ---------------------------------------------------------------------------
# Test: Help shows global options
# ---------------------------------------------------------------------------


class TestHelpGlobalOptions:
    """Test that help output shows global options."""

    def test_main_help_shows_global_options(self) -> None:
        """ag --help shows --workspace, --json, --quiet, --verbose."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        # Check for global options
        assert "--workspace" in result.output or "-w" in result.output
        assert "--json" in result.output
        assert "--quiet" in result.output or "-q" in result.output
        assert "--verbose" in result.output or "-v" in result.output

    def test_main_help_shows_version(self) -> None:
        """ag --help shows --version."""
        result = runner.invoke(app, ["--help"])
        assert "--version" in result.output

    def test_run_help_shows_local_options(self) -> None:
        """ag run --help shows local --workspace and --json."""
        result = runner.invoke(app, ["run", "--help"])
        assert result.exit_code == 0
        assert "--workspace" in result.output
        assert "--json" in result.output

    def test_runs_help_shows_list_and_show(self) -> None:
        """ag runs --help shows list and show subcommands."""
        result = runner.invoke(app, ["runs", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output
        assert "show" in result.output


# ---------------------------------------------------------------------------
# Test: Global workspace propagation
# ---------------------------------------------------------------------------


class TestGlobalWorkspacePropagation:
    """Test --workspace global option propagates to subcommands."""

    def test_global_workspace_for_runs_list(self) -> None:
        """ag --workspace ws_a runs list uses global workspace."""
        with tempfile.TemporaryDirectory() as tmpdir:
            env = {"AG_WORKSPACE_DIR": tmpdir, "AG_DEV": "1"}

            # First create the workspace explicitly
            from ag.storage import Workspace

            ws = Workspace("global-ws", Path(tmpdir))
            ws.ensure_exists()

            # Then create a run in the workspace
            run_result = runner.invoke(
                app,
                ["run", "Test", "--workspace", "global-ws", "--mode", "manual"],
                env=env,
            )
            assert run_result.exit_code == 0

            # Now use global --workspace to list runs
            result = runner.invoke(
                app, ["--workspace", "global-ws", "runs", "list"], env={"AG_WORKSPACE_DIR": tmpdir}
            )
            assert result.exit_code == 0
            assert "global-ws" in result.output

    def test_local_workspace_overrides_global(self) -> None:
        """Local --workspace overrides global --workspace."""
        with tempfile.TemporaryDirectory() as tmpdir:
            env = {"AG_WORKSPACE_DIR": tmpdir, "AG_DEV": "1"}

            # Create both workspaces explicitly
            from ag.storage import Workspace

            Workspace("global-ws", Path(tmpdir)).ensure_exists()
            Workspace("local-ws", Path(tmpdir)).ensure_exists()

            # Create a run in local-ws
            run_result = runner.invoke(
                app,
                ["run", "Test", "--workspace", "local-ws", "--mode", "manual"],
                env=env,
            )
            assert run_result.exit_code == 0

            # Global workspace points to global-ws, but local overrides to local-ws
            result = runner.invoke(
                app,
                ["--workspace", "global-ws", "runs", "list", "--workspace", "local-ws"],
                env={"AG_WORKSPACE_DIR": tmpdir},
            )
            assert result.exit_code == 0
            assert "local-ws" in result.output


# ---------------------------------------------------------------------------
# Test: Global JSON propagation
# ---------------------------------------------------------------------------


class TestGlobalJsonPropagation:
    """Test --json global option propagates to subcommands."""

    def test_global_json_for_runs_list(self) -> None:
        """ag --json runs list outputs JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = "json-test-ws"
            env = {"AG_WORKSPACE_DIR": tmpdir, "AG_DEV": "1"}

            # Create workspace first
            from ag.storage import Workspace

            Workspace(workspace, Path(tmpdir)).ensure_exists()

            # Create a run
            run_result = runner.invoke(
                app,
                ["run", "Test", "--workspace", workspace, "--mode", "manual"],
                env=env,
            )
            assert run_result.exit_code == 0

            # Use global --json
            result = runner.invoke(
                app,
                ["--json", "--workspace", workspace, "runs", "list"],
                env={"AG_WORKSPACE_DIR": tmpdir},
            )
            assert result.exit_code == 0
            # Should be valid JSON
            data = json.loads(result.output)
            assert isinstance(data, list)

    def test_local_json_overrides_global(self) -> None:
        """Local --json and global --json both work (no conflict)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = "json-override-ws"
            env = {"AG_WORKSPACE_DIR": tmpdir, "AG_DEV": "1"}

            # Create workspace first
            from ag.storage import Workspace

            Workspace(workspace, Path(tmpdir)).ensure_exists()

            # Create a run
            run_result = runner.invoke(
                app,
                ["run", "Test", "--workspace", workspace, "--mode", "manual"],
                env=env,
            )
            assert run_result.exit_code == 0

            # Both global and local --json
            result = runner.invoke(
                app,
                ["--json", "runs", "list", "--workspace", workspace, "--json"],
                env={"AG_WORKSPACE_DIR": tmpdir},
            )
            assert result.exit_code == 0
            data = json.loads(result.output)
            assert isinstance(data, list)


# ---------------------------------------------------------------------------
# Test: Global quiet/verbose propagation
# ---------------------------------------------------------------------------


class TestGlobalQuietVerbosePropagation:
    """Test --quiet and --verbose global options."""

    def test_global_quiet_reduces_output(self) -> None:
        """ag --quiet run produces less output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            env = {"AG_WORKSPACE_DIR": tmpdir, "AG_DEV": "1"}

            # Create workspace first
            from ag.storage import Workspace

            ws = Workspace("quiet-test-ws", Path(tmpdir))
            ws.ensure_exists()

            # Normal run
            normal_result = runner.invoke(
                app, ["run", "Test", "--workspace", "quiet-test-ws", "--mode", "manual"], env=env
            )
            normal_lines = len(normal_result.output.strip().split("\n"))

            # Quiet run (global)
            quiet_result = runner.invoke(
                app,
                ["--quiet", "run", "Test", "--workspace", "quiet-test-ws", "--mode", "manual"],
                env=env,
            )
            quiet_lines = len(quiet_result.output.strip().split("\n"))

            # Quiet should have less or equal output
            assert quiet_lines <= normal_lines

    def test_global_verbose_adds_details(self) -> None:
        """ag --verbose run shows step details."""
        with tempfile.TemporaryDirectory() as tmpdir:
            env = {"AG_WORKSPACE_DIR": tmpdir, "AG_DEV": "1"}

            # Create workspace first
            from ag.storage import Workspace

            ws = Workspace("verbose-test-ws", Path(tmpdir))
            ws.ensure_exists()

            # Verbose run
            result = runner.invoke(
                app,
                ["--verbose", "run", "Test", "--workspace", "verbose-test-ws", "--mode", "manual"],
                env=env,
            )
            assert result.exit_code == 0
            # Verbose should show steps
            assert "Steps:" in result.output or "step" in result.output.lower()


# ---------------------------------------------------------------------------
# Test: ag --workspace equivalent to subcommand --workspace
# ---------------------------------------------------------------------------


class TestWorkspaceEquivalence:
    """Test that global and local --workspace are equivalent."""

    def test_runs_list_workspace_equivalence(self) -> None:
        """ag --workspace ws runs list == ag runs list --workspace ws."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = "equiv-ws"
            env = {"AG_WORKSPACE_DIR": tmpdir, "AG_DEV": "1"}

            # Create workspace first
            from ag.storage import Workspace

            Workspace(workspace, Path(tmpdir)).ensure_exists()

            # Create a run
            runner.invoke(
                app, ["run", "Test", "--workspace", workspace, "--mode", "manual"], env=env
            )

            # Global workspace
            global_result = runner.invoke(
                app, ["--workspace", workspace, "runs", "list"], env={"AG_WORKSPACE_DIR": tmpdir}
            )

            # Local workspace
            local_result = runner.invoke(
                app, ["runs", "list", "--workspace", workspace], env={"AG_WORKSPACE_DIR": tmpdir}
            )

            # Both should succeed and show same workspace
            assert global_result.exit_code == 0
            assert local_result.exit_code == 0
            assert workspace in global_result.output
            assert workspace in local_result.output


# ---------------------------------------------------------------------------
# Test: CLIContext helper
# ---------------------------------------------------------------------------


class TestCLIContextHelper:
    """Test CLIContext and get_cli_ctx helper."""

    def test_cli_context_defaults(self) -> None:
        """CLIContext has correct defaults."""
        ctx = CLIContext()
        assert ctx.workspace is None
        assert ctx.json_output is False
        assert ctx.quiet is False
        assert ctx.verbose is False

    def test_cli_context_with_values(self) -> None:
        """CLIContext stores provided values."""
        ctx = CLIContext(
            workspace="test-ws",
            json_output=True,
            quiet=True,
            verbose=True,
        )
        assert ctx.workspace == "test-ws"
        assert ctx.json_output is True
        assert ctx.quiet is True
        assert ctx.verbose is True
