"""
CLI tests for ag_foundation.

These tests verify the CLI entrypoint and manual mode gating.
"""

from typer.testing import CliRunner

from ag.cli.main import DEV_ENV_VAR, app

runner = CliRunner()


class TestCLIHelp:
    """Test that CLI help commands work."""

    def test_main_help(self):
        """ag --help should show help text."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "ag_foundation" in result.stdout

    def test_version(self):
        """ag --version should show version."""
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.stdout

    def test_run_help(self):
        """ag run --help should show help text."""
        result = runner.invoke(app, ["run", "--help"])
        assert result.exit_code == 0
        assert "prompt" in result.stdout.lower()

    def test_runs_help(self):
        """ag runs --help should show help text."""
        result = runner.invoke(app, ["runs", "--help"])
        assert result.exit_code == 0
        assert "list" in result.stdout.lower() or "show" in result.stdout.lower()

    def test_ws_help(self):
        """ag ws --help should show help text."""
        result = runner.invoke(app, ["ws", "--help"])
        assert result.exit_code == 0

    def test_artifacts_help(self):
        """ag artifacts --help should show help text."""
        result = runner.invoke(app, ["artifacts", "--help"])
        assert result.exit_code == 0

    def test_doctor(self):
        """ag doctor should run without error."""
        result = runner.invoke(app, ["doctor"])
        assert result.exit_code == 0
        assert "0.1.0" in result.stdout


class TestManualModeGate:
    """Test manual mode dev gate enforcement."""

    def test_manual_mode_without_env_var_fails(self, monkeypatch):
        """--mode manual without AG_DEV=1 should fail."""
        # Ensure env var is not set
        monkeypatch.delenv(DEV_ENV_VAR, raising=False)

        result = runner.invoke(app, ["run", "--mode", "manual", "test prompt"])

        assert result.exit_code == 1
        assert DEV_ENV_VAR in result.stdout or DEV_ENV_VAR in (result.stderr or "")

    def test_manual_mode_with_env_var_succeeds(self, monkeypatch):
        """--mode manual with AG_DEV=1 should succeed (stub output)."""
        monkeypatch.setenv(DEV_ENV_VAR, "1")

        result = runner.invoke(app, ["run", "--mode", "manual", "test prompt"])

        assert result.exit_code == 0
        assert "DEV MODE" in result.stdout
        assert "manual" in result.stdout.lower()

    def test_llm_mode_without_env_var_succeeds(self, monkeypatch):
        """--mode llm (default) should work without AG_DEV."""
        monkeypatch.delenv(DEV_ENV_VAR, raising=False)

        result = runner.invoke(app, ["run", "test prompt"])

        assert result.exit_code == 0
        # Should NOT print dev mode banner
        assert "DEV MODE" not in result.stdout


class TestRunCommand:
    """Test ag run command options."""

    def test_run_with_prompt(self, monkeypatch):
        """ag run with a prompt should work and show run summary."""
        monkeypatch.delenv(DEV_ENV_VAR, raising=False)

        result = runner.invoke(app, ["run", "Hello world"])

        assert result.exit_code == 0
        assert "Run completed" in result.stdout
        assert "Status: success" in result.stdout

    def test_run_with_workspace_option(self, monkeypatch, tmp_path):
        """ag run --workspace should accept workspace option when workspace exists."""
        monkeypatch.delenv(DEV_ENV_VAR, raising=False)
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        # First create the workspace
        from ag.storage import Workspace

        ws = Workspace("my_ws", tmp_path)
        ws.ensure_exists()

        result = runner.invoke(
            app,
            ["run", "--workspace", "my_ws", "Test"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )
        assert result.exit_code == 0
        assert "my_ws" in result.stdout

    def test_run_with_playbook_option(self, monkeypatch):
        """ag run --playbook should accept playbook option."""
        monkeypatch.delenv(DEV_ENV_VAR, raising=False)

        result = runner.invoke(app, ["run", "--playbook", "custom", "Test"])

        # Should not fail; option is accepted (stub doesn't use it yet)
        assert result.exit_code == 0


# ---------------------------------------------------------------------------
# AF-0024: Workspace Lifecycle Tests
# ---------------------------------------------------------------------------


class TestWorkspaceLifecycle:
    """Tests for workspace lifecycle (AF-0024)."""

    def test_run_with_nonexistent_workspace_fails(self, monkeypatch, tmp_path):
        """ag run --workspace should fail if workspace doesn't exist."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        result = runner.invoke(
            app,
            ["run", "--workspace", "nonexistent", "Test prompt"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )
        assert result.exit_code == 1
        assert "does not exist" in result.stdout or "does not exist" in (result.stderr or "")
        assert "ag ws create" in result.stdout or "ag ws create" in (result.stderr or "")

    def test_run_without_workspace_autocreates(self, monkeypatch):
        """ag run without --workspace should auto-create a new workspace."""
        monkeypatch.delenv(DEV_ENV_VAR, raising=False)

        result = runner.invoke(app, ["run", "Test prompt"])

        assert result.exit_code == 0
        assert "Run completed" in result.stdout
        # Workspace ID should be auto-generated
        assert "Workspace: ws-" in result.stdout

    def test_ws_create_command(self, monkeypatch, tmp_path):
        """ag ws create should create a new workspace."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        result = runner.invoke(
            app,
            ["ws", "create", "test-workspace"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )
        assert result.exit_code == 0
        assert "Created workspace" in result.stdout
        assert "test-workspace" in result.stdout

        # Verify workspace was actually created
        from ag.storage import Workspace

        ws = Workspace("test-workspace", tmp_path)
        assert ws.exists()

    def test_ws_create_duplicate_fails(self, monkeypatch, tmp_path):
        """ag ws create should fail if workspace already exists."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        env = {"AG_WORKSPACE_DIR": str(tmp_path)}

        # Create workspace first time
        result1 = runner.invoke(app, ["ws", "create", "duplicate-ws"], env=env)
        assert result1.exit_code == 0

        # Try to create again
        result2 = runner.invoke(app, ["ws", "create", "duplicate-ws"], env=env)
        assert result2.exit_code == 1
        assert "already exists" in result2.stdout or "already exists" in (result2.stderr or "")

    def test_multiple_runs_same_workspace_reuse_db(self, monkeypatch, tmp_path):
        """Multiple runs in same workspace should reuse the same DB file."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        env = {"AG_WORKSPACE_DIR": str(tmp_path)}

        # Create workspace
        runner.invoke(app, ["ws", "create", "multi-run-ws"], env=env)

        # Run twice in same workspace
        result1 = runner.invoke(app, ["run", "--workspace", "multi-run-ws", "First run"], env=env)
        assert result1.exit_code == 0

        result2 = runner.invoke(app, ["run", "--workspace", "multi-run-ws", "Second run"], env=env)
        assert result2.exit_code == 0

        # Verify both runs are in the same workspace
        from ag.storage import Workspace

        ws = Workspace("multi-run-ws", tmp_path)
        assert ws.exists()

        # Check there's only one DB file
        db_path = ws.db_path
        assert db_path.exists()

        # Check both runs are stored
        from ag.storage import SQLiteRunStore

        with SQLiteRunStore(tmp_path) as store:
            runs = store.list("multi-run-ws")
            assert len(runs) == 2

    def test_ws_list_command(self, monkeypatch, tmp_path):
        """ag ws list should show created workspaces."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        env = {"AG_WORKSPACE_DIR": str(tmp_path)}

        # Create workspaces
        runner.invoke(app, ["ws", "create", "ws-alpha"], env=env)
        runner.invoke(app, ["ws", "create", "ws-beta"], env=env)

        # List workspaces
        result = runner.invoke(app, ["ws", "list"], env=env)
        assert result.exit_code == 0
        assert "ws-alpha" in result.stdout
        assert "ws-beta" in result.stdout
