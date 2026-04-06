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

    def test_manual_mode_without_env_var_fails(self, monkeypatch, tmp_path):
        """--mode manual without AG_DEV=1 should fail."""
        # Ensure env var is not set
        monkeypatch.delenv(DEV_ENV_VAR, raising=False)
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        # Create workspace first
        from ag.storage import Workspace

        ws = Workspace("test-ws", tmp_path)
        ws.ensure_exists()

        result = runner.invoke(
            app,
            ["run", "--mode", "manual", "--workspace", "test-ws", "test prompt"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )

        assert result.exit_code == 1
        assert DEV_ENV_VAR in result.stdout or DEV_ENV_VAR in (result.stderr or "")

    def test_manual_mode_with_env_var_succeeds(self, monkeypatch, tmp_path):
        """--mode manual with AG_DEV=1 should succeed (stub output)."""
        monkeypatch.setenv(DEV_ENV_VAR, "1")
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        # Create workspace first
        from ag.storage import Workspace

        ws = Workspace("test-ws", tmp_path)
        ws.ensure_exists()

        result = runner.invoke(
            app,
            ["run", "--mode", "manual", "--workspace", "test-ws", "test prompt"],
            env={"AG_DEV": "1", "AG_WORKSPACE_DIR": str(tmp_path)},
        )

        assert result.exit_code == 0
        assert "DEV MODE" in result.stdout
        assert "manual" in result.stdout.lower()

    def test_llm_mode_without_env_var_succeeds(self, monkeypatch, tmp_path):
        """--mode llm (default) should work without AG_DEV."""
        monkeypatch.delenv(DEV_ENV_VAR, raising=False)
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        # Create workspace first
        from ag.storage import Workspace

        ws = Workspace("test-ws", tmp_path)
        ws.ensure_exists()

        result = runner.invoke(
            app,
            ["run", "--workspace", "test-ws", "test prompt"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )

        assert result.exit_code == 0
        # Should NOT print dev mode banner
        assert "DEV MODE" not in result.stdout

    def test_manual_mode_with_dotenv_file_succeeds(self, tmp_path):
        """AF-0033/BUG-0006: --mode manual should work when AG_DEV=1 is in .env file."""
        import subprocess
        import sys

        from ag.storage import Workspace

        # Create workspace
        ws = Workspace("dotenv-test-ws", tmp_path)
        ws.ensure_exists()

        # Create .env file with AG_DEV=1
        dotenv_path = tmp_path / ".env"
        dotenv_path.write_text("AG_DEV=1\n")

        # Run CLI via subprocess from tmp_path (where .env is located)
        # This ensures a fresh process that will load .env
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "ag.cli.main",
                "run",
                "--mode",
                "manual",
                "--workspace",
                "dotenv-test-ws",
                "test dotenv loading",
            ],
            cwd=str(tmp_path),
            capture_output=True,
            text=True,
            env={
                **{k: v for k, v in __import__("os").environ.items()},
                "AG_WORKSPACE_DIR": str(tmp_path),
            },
        )

        # Should succeed because .env contains AG_DEV=1
        assert result.returncode == 0, f"stderr: {result.stderr}, stdout: {result.stdout}"
        assert "DEV MODE" in result.stdout


class TestRunCommand:
    """Test ag run command options."""

    def test_run_with_prompt(self, monkeypatch, tmp_path):
        """ag run with a prompt should work and show run summary."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        monkeypatch.setenv(DEV_ENV_VAR, "1")

        # Create workspace first
        from ag.storage import Workspace

        ws = Workspace("test-ws", tmp_path)
        ws.ensure_exists()

        result = runner.invoke(
            app,
            ["run", "--mode", "manual", "--workspace", "test-ws", "Hello world"],
            env={"AG_WORKSPACE_DIR": str(tmp_path), DEV_ENV_VAR: "1"},
        )

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

    def test_run_with_playbook_option(self, monkeypatch, tmp_path):
        """ag run --playbook should accept playbook option."""
        monkeypatch.delenv(DEV_ENV_VAR, raising=False)
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        # Create workspace first
        from ag.storage import Workspace

        ws = Workspace("test-ws", tmp_path)
        ws.ensure_exists()

        result = runner.invoke(
            app,
            ["run", "--workspace", "test-ws", "--playbook", "default_v0", "Test"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )

        # Should succeed with valid playbook
        assert result.exit_code == 0

    def test_run_with_invalid_playbook_fails(self, monkeypatch, tmp_path):
        """ag run --playbook with invalid name should fail (AF-0072)."""
        monkeypatch.delenv(DEV_ENV_VAR, raising=False)
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        # Create workspace first
        from ag.storage import Workspace

        ws = Workspace("test-ws", tmp_path)
        ws.ensure_exists()

        result = runner.invoke(
            app,
            ["run", "--workspace", "test-ws", "--playbook", "nonexistent", "Test"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )

        # Should fail with clear error
        assert result.exit_code == 1
        assert "not found" in result.output
        assert "Available playbooks" in result.output


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

    def test_run_without_workspace_bootstraps_default(self, monkeypatch, tmp_path):
        """AF-0027: ag run without workspace creates 'default' when no workspaces exist."""
        monkeypatch.delenv(DEV_ENV_VAR, raising=False)
        monkeypatch.delenv("AG_WORKSPACE", raising=False)
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        monkeypatch.setenv("AG_CONFIG_DIR", str(tmp_path / ".ag"))  # Isolate state

        # Ensure no workspaces exist
        assert not list(tmp_path.iterdir())

        result = runner.invoke(
            app,
            ["run", "Test prompt"],
            env={"AG_WORKSPACE_DIR": str(tmp_path), "AG_CONFIG_DIR": str(tmp_path / ".ag")},
        )

        # Should succeed by bootstrapping 'default' workspace
        assert result.exit_code == 0, f"stdout: {result.stdout}, stderr: {result.stderr}"
        assert "Workspace: default" in result.stdout
        # Verify default workspace was created
        assert (tmp_path / "default").is_dir()

    def test_run_without_workspace_fails_when_workspaces_exist(self, monkeypatch, tmp_path):
        """AF-0027: ag run without workspace fails when workspaces exist but none selected."""
        monkeypatch.delenv(DEV_ENV_VAR, raising=False)
        monkeypatch.delenv("AG_WORKSPACE", raising=False)
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        monkeypatch.setenv("AG_CONFIG_DIR", str(tmp_path / ".ag"))  # Isolate state

        # Create an existing workspace but don't select it
        from ag.storage import Workspace

        ws = Workspace("existing-ws", tmp_path)
        ws.ensure_exists()

        result = runner.invoke(
            app,
            ["run", "Test prompt"],
            env={"AG_WORKSPACE_DIR": str(tmp_path), "AG_CONFIG_DIR": str(tmp_path / ".ag")},
        )

        # Should fail with guidance
        assert result.exit_code == 1
        assert (
            "No workspace specified" in (result.stderr or "")
            or "No workspace specified" in result.stdout
        )
        assert "--workspace" in (result.stderr or "") or "--workspace" in result.stdout
        assert "ag ws use" in (result.stderr or "") or "ag ws use" in result.stdout

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
        monkeypatch.setenv(DEV_ENV_VAR, "1")
        env = {"AG_WORKSPACE_DIR": str(tmp_path), DEV_ENV_VAR: "1"}

        # Create workspace
        runner.invoke(app, ["ws", "create", "multi-run-ws"], env=env)

        # Run twice in same workspace (manual mode to bypass V1Planner)
        result1 = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "multi-run-ws", "First run"], env=env
        )
        assert result1.exit_code == 0

        result2 = runner.invoke(
            app, ["run", "--mode", "manual", "--workspace", "multi-run-ws", "Second run"], env=env
        )
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


# ---------------------------------------------------------------------------
# AF-0026: Workspace Selection Policy Enforcement Tests
# ---------------------------------------------------------------------------


class TestWorkspaceSelectionPolicy:
    """Tests for workspace selection policy enforcement (AF-0026, AF-0027, BUG-0005).

    Policy (AF-0027):
    1. --workspace flag → use specified workspace
    2. Persisted default workspace (via `ag ws use`)
    3. AG_WORKSPACE env var → use as default
    4. Bootstrap: if no workspaces exist, create 'default'
    5. Error with guidance if workspaces exist but none selected

    Implicit workspace creation is NOT allowed (except bootstrap case).
    """

    def test_workspace_flag_takes_precedence(self, monkeypatch, tmp_path):
        """--workspace flag overrides AG_WORKSPACE env var."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        env = {"AG_WORKSPACE_DIR": str(tmp_path), "AG_WORKSPACE": "env-ws"}

        # Create both workspaces
        from ag.storage import Workspace

        Workspace("env-ws", tmp_path).ensure_exists()
        Workspace("flag-ws", tmp_path).ensure_exists()

        # Run with --workspace flag (should use flag-ws, not env-ws)
        result = runner.invoke(
            app,
            ["run", "--workspace", "flag-ws", "Test"],
            env=env,
        )
        assert result.exit_code == 0
        assert "flag-ws" in result.stdout

    def test_ag_workspace_env_var_used_when_no_flag(self, monkeypatch, tmp_path):
        """AG_WORKSPACE env var is used when no --workspace flag and no persisted default."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        monkeypatch.setenv("AG_CONFIG_DIR", str(tmp_path / ".ag"))  # Isolate
        monkeypatch.setenv("AG_WORKSPACE", "env-default-ws")
        env = {
            "AG_WORKSPACE_DIR": str(tmp_path),
            "AG_CONFIG_DIR": str(tmp_path / ".ag"),
            "AG_WORKSPACE": "env-default-ws",
        }

        # Create the workspace specified by AG_WORKSPACE
        from ag.storage import Workspace

        Workspace("env-default-ws", tmp_path).ensure_exists()

        # Run without --workspace flag (should use AG_WORKSPACE since no persisted default)
        result = runner.invoke(
            app,
            ["run", "Test"],
            env=env,
        )
        assert result.exit_code == 0
        assert "env-default-ws" in result.stdout

    def test_no_workspace_selection_fails_when_workspaces_exist(self, monkeypatch, tmp_path):
        """AF-0027: Without workspace selection, ag run fails if workspaces already exist."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        monkeypatch.setenv("AG_CONFIG_DIR", str(tmp_path / ".ag"))  # Isolate state
        monkeypatch.delenv("AG_WORKSPACE", raising=False)
        env = {"AG_WORKSPACE_DIR": str(tmp_path), "AG_CONFIG_DIR": str(tmp_path / ".ag")}

        # Create a workspace but don't select it
        from ag.storage import Workspace

        Workspace("existing-ws", tmp_path).ensure_exists()

        result = runner.invoke(
            app,
            ["run", "Test"],
            env=env,
        )
        assert result.exit_code == 1
        # Check for helpful error message
        output = result.stdout + (result.stderr or "")
        assert "No workspace specified" in output
        assert "--workspace" in output
        assert "ag ws use" in output  # AF-0027: now suggests ag ws use

    def test_bootstrap_creates_default_when_no_workspaces(self, monkeypatch, tmp_path):
        """AF-0027: Bootstrap case creates 'default' workspace when none exist."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        monkeypatch.setenv("AG_CONFIG_DIR", str(tmp_path / ".ag"))  # Isolate state
        monkeypatch.delenv("AG_WORKSPACE", raising=False)
        env = {"AG_WORKSPACE_DIR": str(tmp_path), "AG_CONFIG_DIR": str(tmp_path / ".ag")}

        # Ensure no workspaces exist
        assert not list(tmp_path.iterdir()) if tmp_path.exists() else True

        # Run without workspace (should bootstrap 'default')
        result = runner.invoke(
            app,
            ["run", "Test"],
            env=env,
        )
        assert result.exit_code == 0

        # Verify 'default' workspace was created
        assert (tmp_path / "default").is_dir(), f"Expected 'default' workspace in {tmp_path}"

    def test_no_implicit_workspace_creation_when_workspaces_exist(self, monkeypatch, tmp_path):
        """AF-0027: ag run must not implicitly create new workspaces when some exist."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        monkeypatch.setenv("AG_CONFIG_DIR", str(tmp_path / ".ag"))  # Isolate state
        monkeypatch.delenv("AG_WORKSPACE", raising=False)
        env = {"AG_WORKSPACE_DIR": str(tmp_path), "AG_CONFIG_DIR": str(tmp_path / ".ag")}

        # Create one workspace
        from ag.storage import Workspace

        Workspace("existing-ws", tmp_path).ensure_exists()

        # Run without workspace (should fail)
        result = runner.invoke(
            app,
            ["run", "Test"],
            env=env,
        )
        assert result.exit_code == 1

        # Verify no additional workspace was created
        workspaces = list(tmp_path.iterdir()) if tmp_path.exists() else []
        # Only count workspace dirs, exclude .ag config dir
        ws_dirs = [w for w in workspaces if w.name != ".ag"]
        assert len(ws_dirs) == 1, f"Should only have 'existing-ws', got: {ws_dirs}"

    def test_repeated_runs_reuse_workspace(self, monkeypatch, tmp_path):
        """Repeated ag run with same workspace reuse same DB."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        monkeypatch.setenv(DEV_ENV_VAR, "1")
        env = {"AG_WORKSPACE_DIR": str(tmp_path), DEV_ENV_VAR: "1"}

        # Create workspace explicitly
        from ag.storage import SQLiteRunStore, Workspace

        Workspace("stable-ws", tmp_path).ensure_exists()

        # Run multiple times (manual mode to bypass V1Planner)
        for i in range(3):
            result = runner.invoke(
                app,
                ["run", "--mode", "manual", "--workspace", "stable-ws", f"Run {i}"],
                env=env,
            )
            assert result.exit_code == 0
            assert "stable-ws" in result.stdout

        # Verify all runs in same workspace
        with SQLiteRunStore(tmp_path) as store:
            runs = store.list("stable-ws")
            assert len(runs) == 3

    def test_persisted_default_workspace_used(self, monkeypatch, tmp_path):
        """AF-0027: Persisted default workspace is used when no flag or env var."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        monkeypatch.setenv("AG_CONFIG_DIR", str(tmp_path / ".ag"))  # Isolate state
        monkeypatch.delenv("AG_WORKSPACE", raising=False)
        env = {"AG_WORKSPACE_DIR": str(tmp_path), "AG_CONFIG_DIR": str(tmp_path / ".ag")}

        # Create workspace and set as default via ag ws use
        from ag.storage import Workspace

        Workspace("my-default-ws", tmp_path).ensure_exists()

        # Set default via CLI
        result = runner.invoke(
            app,
            ["ws", "use", "my-default-ws"],
            env=env,
        )
        assert result.exit_code == 0
        assert "Default workspace set to" in result.stdout

        # Run without --workspace flag (should use persisted default)
        result = runner.invoke(
            app,
            ["run", "Test using persisted default"],
            env=env,
        )
        assert result.exit_code == 0
        assert "my-default-ws" in result.stdout


# ─────────────────────────────────────────────────────────────────────────────
# AF-0048: Skill CLI Commands (BUG0008 fix)
# ─────────────────────────────────────────────────────────────────────────────


class TestSkillsCommands:
    """Test ag skills CLI commands."""

    def test_skills_list_shows_registered_skills(self):
        """ag skills list should show all registered skills."""
        result = runner.invoke(app, ["skills", "list"])
        assert result.exit_code == 0
        # Should show production skills (AF-0065)
        assert "load_documents" in result.output
        # Should show some standard skills
        assert "echo" in result.output
        assert "Registered Skills" in result.output

    def test_skills_info_shows_skill_details(self):
        """ag skills info <name> should show skill description."""
        result = runner.invoke(app, ["skills", "info", "load_documents"])
        assert result.exit_code == 0
        assert "load_documents" in result.output
        assert "Description" in result.output

    def test_skills_info_unknown_skill_fails(self):
        """ag skills info <unknown> should fail with helpful message."""
        result = runner.invoke(app, ["skills", "info", "nonexistent_skill"])
        assert result.exit_code == 1
        assert "Skill not found" in result.output
        # Should list available skills
        assert "Available skills" in result.output


class TestRunWithSkillFlag:
    """Test ag run --skill flag for direct skill execution."""

    def test_run_with_skill_flag_executes_skill(self, tmp_path, monkeypatch):
        """ag run --skill <name> should execute skill directly."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        env = {"AG_WORKSPACE_DIR": str(tmp_path)}

        # Create workspace first
        from ag.storage import Workspace

        Workspace("skill-test-ws", tmp_path).ensure_exists()

        result = runner.invoke(
            app,
            ["run", "--skill", "echo_tool", "--workspace", "skill-test-ws", "Hello world"],
            env=env,
        )
        assert result.exit_code == 0
        assert "Skill executed" in result.output
        assert "echo_tool" in result.output
        assert "Success" in result.output

    def test_run_with_skill_flag_unknown_skill_fails(self, tmp_path, monkeypatch):
        """ag run --skill <unknown> should fail with helpful message."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        env = {"AG_WORKSPACE_DIR": str(tmp_path)}

        # Create workspace first
        from ag.storage import Workspace

        Workspace("skill-test-ws", tmp_path).ensure_exists()

        result = runner.invoke(
            app,
            ["run", "--skill", "nonexistent", "--workspace", "skill-test-ws", "test"],
            env=env,
        )
        assert result.exit_code == 1
        assert "Skill not found" in result.output
        assert "Available skills" in result.output

    def test_run_skill_json_output(self, tmp_path, monkeypatch):
        """ag run --skill --json should output JSON."""
        import json

        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        env = {"AG_WORKSPACE_DIR": str(tmp_path)}

        from ag.storage import Workspace

        Workspace("skill-test-ws", tmp_path).ensure_exists()

        result = runner.invoke(
            app,
            ["run", "--skill", "echo_tool", "--json", "--workspace", "skill-test-ws", "test msg"],
            env=env,
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["skill"] == "echo_tool"
        assert data["success"] is True

    def test_run_help_shows_skill_option(self):
        """ag run --help should document --skill option."""
        result = runner.invoke(app, ["run", "--help"])
        assert result.exit_code == 0
        assert "--skill" in result.output
        assert "-s" in result.output


# ---------------------------------------------------------------------------
# Tests for playbooks list (AF-0076)
# ---------------------------------------------------------------------------


class TestPlaybooksListCommand:
    """Tests for `ag playbooks list` command (AF-0076)."""

    def test_playbooks_list_shows_table(self):
        """ag playbooks list should display a table."""
        result = runner.invoke(app, ["playbooks", "list"])
        assert result.exit_code == 0
        assert "Available Playbooks" in result.output
        # Check columns exist
        assert "Name" in result.output
        assert "Version" in result.output
        assert "Stability" in result.output
        assert "Description" in result.output

    def test_playbooks_list_shows_all_playbooks(self):
        """ag playbooks list should show all registered playbooks."""
        result = runner.invoke(app, ["playbooks", "list"])
        assert result.exit_code == 0
        # Check all playbooks appear
        assert "default_v0" in result.output
        assert "delegate_v0" in result.output
        assert "summarize_v0" in result.output
        assert "research_v0" in result.output

    def test_playbooks_list_json_output(self):
        """ag playbooks list --json should output JSON."""
        import json

        result = runner.invoke(app, ["playbooks", "list", "--json"])
        assert result.exit_code == 0

        data = json.loads(result.output)
        assert isinstance(data, list)
        assert len(data) >= 4  # At least 4 playbooks

        # Check structure
        names = [pb["name"] for pb in data]
        assert "default_v0" in names
        assert "summarize_v0" in names

        # Check fields exist (AF0078: source field added)
        for pb in data:
            assert "name" in pb
            assert "version" in pb
            assert "stability" in pb
            assert "description" in pb
            assert "source" in pb  # AF0078: entry-point discovery

    def test_playbooks_list_shows_source_column(self):
        """ag playbooks list shows source column (AF0078)."""
        result = runner.invoke(app, ["playbooks", "list"])
        assert result.exit_code == 0
        assert "Source" in result.output
        assert "entry-point" in result.output

    def test_playbooks_list_stability_values(self):
        """ag playbooks list should show correct stability values."""
        import json

        result = runner.invoke(app, ["playbooks", "list", "--json"])
        assert result.exit_code == 0

        data = json.loads(result.output)
        stability_map = {pb["name"]: pb["stability"] for pb in data}

        # Check expected stability values
        assert stability_map.get("default_v0") == "test"
        assert stability_map.get("delegate_v0") == "test"
        assert stability_map.get("summarize_v0") == "experimental"
        assert stability_map.get("research_v0") == "experimental"


class TestPlaybooksShow:
    """Tests for AF-0147: ag playbooks show command."""

    def test_playbooks_show_research_v0(self):
        """ag playbooks show research_v0 displays correct detail."""
        result = runner.invoke(app, ["playbooks", "show", "research_v0"])
        assert result.exit_code == 0
        assert "research_v0" in result.output
        assert "Steps" in result.output
        # Check header fields
        assert "Version" in result.output
        assert "Reasoning" in result.output
        # Check step names appear
        assert "load_local" in result.output or "search_web" in result.output

    def test_playbooks_show_summarize_v0(self):
        """ag playbooks show summarize_v0 displays correct detail."""
        result = runner.invoke(app, ["playbooks", "show", "summarize_v0"])
        assert result.exit_code == 0
        assert "summarize_v0" in result.output
        assert "Steps" in result.output

    def test_playbooks_show_unknown_error(self):
        """ag playbooks show nonexistent gives clean error (exit code 1)."""
        result = runner.invoke(app, ["playbooks", "show", "nonexistent"])
        assert result.exit_code == 1
        assert "not found" in result.output.lower()
        assert "ag playbooks list" in result.output

    def test_playbooks_show_json(self):
        """ag playbooks show --json returns valid JSON with all fields."""
        import json

        result = runner.invoke(app, ["playbooks", "show", "research_v0", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["name"] == "research_v0"
        assert "version" in data
        assert "description" in data
        assert "reasoning_modes" in data
        assert "budgets" in data
        assert "steps" in data
        assert isinstance(data["steps"], list)
        assert len(data["steps"]) > 0
        # Check step structure
        step = data["steps"][0]
        assert "order" in step
        assert "name" in step
        assert "skill" in step
        assert "type" in step
        assert "required" in step

    def test_playbooks_show_json_unknown_error(self):
        """ag playbooks show --json with unknown playbook returns JSON error."""
        import json

        result = runner.invoke(app, ["playbooks", "show", "nonexistent", "--json"])
        assert result.exit_code == 1
        data = json.loads(result.output)
        assert data["error"] == "not_found"

    def test_playbooks_show_step_order(self):
        """Step order matches playbook definition."""
        import json

        result = runner.invoke(app, ["playbooks", "show", "research_v0", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        orders = [s["order"] for s in data["steps"]]
        assert orders == list(range(1, len(orders) + 1))

    def test_playbooks_show_alias_resolution(self):
        """ag playbooks show with alias (no _v0 suffix) works."""
        result = runner.invoke(app, ["playbooks", "show", "research"])
        assert result.exit_code == 0
        assert "research_v0" in result.output


class TestRunsListPagination:
    """Tests for AF-0088: runs list pagination."""

    def test_runs_list_shows_pagination_info(self, monkeypatch, tmp_path):
        """runs list shows total count and displayed count."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        from ag.storage import SQLiteRunStore, Workspace

        ws = Workspace("test-ws", tmp_path)
        ws.ensure_exists()

        # Create multiple runs
        from tests.test_storage import _make_run_trace

        store = SQLiteRunStore(tmp_path)
        for _ in range(5):
            store.save(_make_run_trace("test-ws"))
        store.close()

        result = runner.invoke(
            app,
            ["runs", "list", "--workspace", "test-ws", "--limit", "3"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )

        assert result.exit_code == 0
        # Should show "showing X of Y"
        assert "showing 3 of 5" in result.stdout

    def test_runs_list_all_flag(self, monkeypatch, tmp_path):
        """runs list --all shows all runs."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        from ag.storage import SQLiteRunStore, Workspace

        ws = Workspace("test-ws", tmp_path)
        ws.ensure_exists()

        from tests.test_storage import _make_run_trace

        store = SQLiteRunStore(tmp_path)
        for _ in range(15):
            store.save(_make_run_trace("test-ws"))
        store.close()

        result = runner.invoke(
            app,
            ["runs", "list", "--workspace", "test-ws", "--all"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )

        assert result.exit_code == 0
        # Should show total without "showing X of Y"
        assert "15 total" in result.stdout

    def test_runs_list_json_includes_counts(self, monkeypatch, tmp_path):
        """runs list --json includes total and showing counts."""
        import json

        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        from ag.storage import SQLiteRunStore, Workspace

        ws = Workspace("test-ws", tmp_path)
        ws.ensure_exists()

        from tests.test_storage import _make_run_trace

        store = SQLiteRunStore(tmp_path)
        for _ in range(5):
            store.save(_make_run_trace("test-ws"))
        store.close()

        result = runner.invoke(
            app,
            ["runs", "list", "--workspace", "test-ws", "--limit", "3", "--json"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )

        assert result.exit_code == 0
        data = json.loads(result.stdout)
        assert data["total"] == 5
        assert data["showing"] == 3
        assert len(data["runs"]) == 3

    def test_runs_list_hint_when_truncated(self, monkeypatch, tmp_path):
        """runs list shows hint when output is truncated."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        from ag.storage import SQLiteRunStore, Workspace

        ws = Workspace("test-ws", tmp_path)
        ws.ensure_exists()

        from tests.test_storage import _make_run_trace

        store = SQLiteRunStore(tmp_path)
        for _ in range(15):
            store.save(_make_run_trace("test-ws"))
        store.close()

        result = runner.invoke(
            app,
            ["runs", "list", "--workspace", "test-ws"],  # default limit 10
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )

        assert result.exit_code == 0
        assert "--all" in result.stdout
        assert "--limit" in result.stdout


class TestRunsListFilters:
    """Tests for AF-0144: runs list --playbook and --mode filters."""

    def _create_runs(self, tmp_path, specs):
        """Helper: create runs with specific playbook/mode combos.

        specs: list of (playbook_name, mode) tuples
        """
        from ag.core.run_trace import FinalStatus, RunTraceBuilder, VerifierStatus
        from ag.storage import SQLiteRunStore, Workspace

        ws = Workspace("test-ws", tmp_path)
        ws.ensure_exists()
        store = SQLiteRunStore(tmp_path)
        for pb_name, exec_mode in specs:
            trace = (
                RunTraceBuilder("test-ws", exec_mode, pb_name, "1.0")
                .verify(VerifierStatus.PASSED)
                .complete(FinalStatus.SUCCESS)
                .build()
            )
            store.save(trace)
        store.close()

    def test_filter_by_playbook(self, monkeypatch, tmp_path):
        """--playbook returns only matching runs."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        from ag.core.task_spec import ExecutionMode

        self._create_runs(
            tmp_path,
            [
                ("research_v0", ExecutionMode.MANUAL),
                ("research_v0", ExecutionMode.MANUAL),
                ("default_v0", ExecutionMode.MANUAL),
            ],
        )

        result = runner.invoke(
            app,
            ["runs", "list", "--workspace", "test-ws", "--playbook", "research_v0", "--json"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )
        assert result.exit_code == 0
        import json

        data = json.loads(result.stdout)
        assert data["showing"] == 2
        for run in data["runs"]:
            assert run["playbook"]["name"] == "research_v0"

    def test_filter_by_mode_manual(self, monkeypatch, tmp_path):
        """--mode manual returns only manual-mode runs."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        from ag.core.task_spec import ExecutionMode

        self._create_runs(
            tmp_path,
            [
                ("default_v0", ExecutionMode.MANUAL),
                ("default_v0", ExecutionMode.SUPERVISED),
                ("default_v0", ExecutionMode.AUTONOMOUS),
            ],
        )

        result = runner.invoke(
            app,
            ["runs", "list", "--workspace", "test-ws", "--mode", "manual", "--json"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )
        assert result.exit_code == 0
        import json

        data = json.loads(result.stdout)
        assert data["showing"] == 1
        assert data["runs"][0]["mode"] == "manual"

    def test_filter_by_mode_llm(self, monkeypatch, tmp_path):
        """--mode llm returns only non-manual runs."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        from ag.core.task_spec import ExecutionMode

        self._create_runs(
            tmp_path,
            [
                ("default_v0", ExecutionMode.MANUAL),
                ("default_v0", ExecutionMode.SUPERVISED),
                ("default_v0", ExecutionMode.AUTONOMOUS),
            ],
        )

        result = runner.invoke(
            app,
            ["runs", "list", "--workspace", "test-ws", "--mode", "llm", "--json"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )
        assert result.exit_code == 0
        import json

        data = json.loads(result.stdout)
        assert data["showing"] == 2
        for run in data["runs"]:
            assert run["mode"] in ("supervised", "autonomous")

    def test_combined_filters(self, monkeypatch, tmp_path):
        """Combined --status --playbook --mode filters work together."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        from ag.core.run_trace import FinalStatus, RunTraceBuilder, VerifierStatus
        from ag.core.task_spec import ExecutionMode
        from ag.storage import SQLiteRunStore, Workspace

        ws = Workspace("test-ws", tmp_path)
        ws.ensure_exists()
        store = SQLiteRunStore(tmp_path)

        # success + research_v0 + manual
        store.save(
            RunTraceBuilder("test-ws", ExecutionMode.MANUAL, "research_v0", "1.0")
            .verify(VerifierStatus.PASSED)
            .complete(FinalStatus.SUCCESS)
            .build()
        )
        # failure + research_v0 + manual
        store.save(
            RunTraceBuilder("test-ws", ExecutionMode.MANUAL, "research_v0", "1.0")
            .verify(VerifierStatus.FAILED)
            .complete(FinalStatus.FAILURE)
            .build()
        )
        # success + default_v0 + manual
        store.save(
            RunTraceBuilder("test-ws", ExecutionMode.MANUAL, "default_v0", "1.0")
            .verify(VerifierStatus.PASSED)
            .complete(FinalStatus.SUCCESS)
            .build()
        )
        store.close()

        result = runner.invoke(
            app,
            [
                "runs",
                "list",
                "--workspace",
                "test-ws",
                "--status",
                "success",
                "--playbook",
                "research_v0",
                "--json",
            ],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )
        assert result.exit_code == 0
        import json

        data = json.loads(result.stdout)
        assert data["showing"] == 1

    def test_unknown_playbook_returns_empty(self, monkeypatch, tmp_path):
        """Unknown playbook filter returns empty list, not an error."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        from ag.core.task_spec import ExecutionMode

        self._create_runs(
            tmp_path,
            [
                ("default_v0", ExecutionMode.MANUAL),
            ],
        )

        result = runner.invoke(
            app,
            ["runs", "list", "--workspace", "test-ws", "--playbook", "nonexistent", "--json"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )
        assert result.exit_code == 0
        import json

        data = json.loads(result.stdout)
        assert data["showing"] == 0


# ---------------------------------------------------------------------------
# Tests for CLI stubs (AF-0012)
# ---------------------------------------------------------------------------


class TestCLIStubs:
    """Tests for not-implemented CLI commands (AF-0012).

    All stubs must:
    - Exit with code 1
    - Show "Not implemented in v0" message
    - Support --json flag for structured error output
    """

    def test_runs_tail_stub(self):
        """ag runs tail <id> exits with code 1."""
        result = runner.invoke(app, ["runs", "tail", "some-run-id"])
        assert result.exit_code == 1
        assert "not implemented" in result.output.lower()

    def test_runs_tail_stub_json(self):
        """ag runs tail --json returns structured error."""
        import json

        result = runner.invoke(app, ["runs", "tail", "--json", "some-run-id"])
        assert result.exit_code == 1
        data = json.loads(result.stdout)
        assert data["error"] == "not_implemented"
        assert "runs tail" in data["command"]

    def test_ws_config_get_stub(self):
        """ag ws config get <key> exits with code 1."""
        result = runner.invoke(app, ["ws", "config", "get", "some-key"])
        assert result.exit_code == 1
        assert "not implemented" in result.output.lower()

    def test_ws_config_set_stub(self):
        """ag ws config set <key> <value> exits with code 1."""
        result = runner.invoke(app, ["ws", "config", "set", "some-key", "some-value"])
        assert result.exit_code == 1
        assert "not implemented" in result.output.lower()

    def test_artifacts_open_stub(self):
        """ag artifacts open <id> exits with code 1."""
        result = runner.invoke(app, ["artifacts", "open", "--run", "r1", "artifact-id"])
        assert result.exit_code == 1
        assert "not implemented" in result.output.lower()

    def test_skills_test_stub(self):
        """ag skills test <name> exits with code 1."""
        result = runner.invoke(app, ["skills", "test", "some-skill"])
        assert result.exit_code == 1
        assert "not implemented" in result.output.lower()

    def test_skills_enable_stub(self):
        """ag skills enable <name> exits with code 1."""
        result = runner.invoke(app, ["skills", "enable", "some-skill"])
        assert result.exit_code == 1
        assert "not implemented" in result.output.lower()

    def test_skills_disable_stub(self):
        """ag skills disable <name> exits with code 1."""
        result = runner.invoke(app, ["skills", "disable", "some-skill"])
        assert result.exit_code == 1
        assert "not implemented" in result.output.lower()

    def test_playbooks_show_unknown(self):
        """ag playbooks show <unknown> exits with code 1."""
        result = runner.invoke(app, ["playbooks", "show", "nonexistent-playbook"])
        assert result.exit_code == 1
        assert "not found" in result.output.lower()

    def test_playbooks_validate_stub(self):
        """ag playbooks validate <path> exits with code 1."""
        result = runner.invoke(app, ["playbooks", "validate", "path/to/playbook"])
        assert result.exit_code == 1
        assert "not implemented" in result.output.lower()

    def test_playbooks_set_default_stub(self):
        """ag playbooks set-default <name> exits with code 1."""
        result = runner.invoke(app, ["playbooks", "set-default", "research"])
        assert result.exit_code == 1
        assert "not implemented" in result.output.lower()

    def test_config_list_stub(self):
        """ag config list exits with code 1."""
        result = runner.invoke(app, ["config", "list"])
        assert result.exit_code == 1
        assert "not implemented" in result.output.lower()

    def test_config_get_stub(self):
        """ag config get <key> exits with code 1."""
        result = runner.invoke(app, ["config", "get", "some-key"])
        assert result.exit_code == 1
        assert "not implemented" in result.output.lower()

    def test_config_set_stub(self):
        """ag config set <key> <value> exits with code 1."""
        result = runner.invoke(app, ["config", "set", "some-key", "some-value"])
        assert result.exit_code == 1
        assert "not implemented" in result.output.lower()

    def test_stub_json_output_format(self):
        """All stubs with --json return consistent error structure."""
        import json

        # Test a representative sample of stubs
        stub_commands = [
            ["skills", "test", "--json", "x"],
            ["skills", "enable", "--json", "x"],
            ["skills", "disable", "--json", "x"],
            ["playbooks", "validate", "--json", "x"],
            ["playbooks", "set-default", "--json", "x"],
            ["config", "list", "--json"],
            ["config", "get", "--json", "x"],
            ["config", "set", "--json", "x", "y"],
        ]

        for cmd in stub_commands:
            result = runner.invoke(app, cmd)
            assert result.exit_code == 1, f"Expected exit 1 for {' '.join(cmd)}"
            data = json.loads(result.stdout)
            assert "error" in data, f"Missing 'error' key for {' '.join(cmd)}"
            assert data["error"] == "not_implemented"


class TestPlanningPipelineDisplay:
    """Tests for AF-0122: planning and pipeline display in ag runs show."""

    def test_runs_show_displays_planning_section(self, monkeypatch, tmp_path):
        """ag runs show displays Planning section when trace has planning metadata."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        from datetime import datetime, timezone

        from ag.core.run_trace import PipelineManifest, PlanningLLMCall, PlanningMetadata
        from ag.storage import SQLiteRunStore, Workspace
        from tests.test_storage import _make_run_trace

        ws = Workspace("pln-ws", tmp_path)
        ws.ensure_exists()

        trace = _make_run_trace("pln-ws")
        now = datetime.now(timezone.utc)
        trace.planning = PlanningMetadata(
            planner="V3Planner",
            started_at=now,
            ended_at=now,
            duration_ms=1234,
            llm_call=PlanningLLMCall(
                model="gpt-4o-mini",
                input_tokens=11333,
                output_tokens=645,
                total_tokens=11978,
            ),
            confidence=0.85,
        )
        trace.pipeline = PipelineManifest(
            planner="V3Planner",
            orchestrator="V1Orchestrator",
            executor="V0Executor",
            verifier="V1Verifier",
            recorder="V0Recorder",
        )

        store = SQLiteRunStore(tmp_path)
        store.save(trace)
        store.close()

        result = runner.invoke(
            app,
            ["runs", "show", trace.run_id, "--workspace", "pln-ws"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )

        assert result.exit_code == 0
        assert "Planning" in result.stdout
        assert "V3Planner" in result.stdout
        assert "1234ms" in result.stdout
        assert "11978" in result.stdout
        assert "gpt-4o-mini" in result.stdout
        assert "85%" in result.stdout

    def test_runs_show_displays_pipeline_section(self, monkeypatch, tmp_path):
        """ag runs show displays Pipeline section when trace has pipeline manifest."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        from ag.core.run_trace import PipelineManifest
        from ag.storage import SQLiteRunStore, Workspace
        from tests.test_storage import _make_run_trace

        ws = Workspace("pip-ws", tmp_path)
        ws.ensure_exists()

        trace = _make_run_trace("pip-ws")
        trace.pipeline = PipelineManifest(
            planner="V3Planner",
            orchestrator="V1Orchestrator",
            executor="V2Executor",
            verifier="V2Verifier",
            recorder="V0Recorder",
        )

        store = SQLiteRunStore(tmp_path)
        store.save(trace)
        store.close()

        result = runner.invoke(
            app,
            ["runs", "show", trace.run_id, "--workspace", "pip-ws"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )

        assert result.exit_code == 0
        assert "Pipeline" in result.stdout
        assert "V1Orchestrator" in result.stdout
        assert "V2Executor" in result.stdout

    def test_runs_show_omits_planning_for_old_traces(self, monkeypatch, tmp_path):
        """ag runs show renders gracefully for old traces without planning/pipeline."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        from ag.storage import SQLiteRunStore, Workspace
        from tests.test_storage import _make_run_trace

        ws = Workspace("old-ws", tmp_path)
        ws.ensure_exists()

        trace = _make_run_trace("old-ws")
        # planning and pipeline are None by default

        store = SQLiteRunStore(tmp_path)
        store.save(trace)
        store.close()

        result = runner.invoke(
            app,
            ["runs", "show", trace.run_id, "--workspace", "old-ws"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )

        assert result.exit_code == 0
        # Planning/Pipeline sections omitted for old traces
        assert "Planning" not in result.stdout
        assert "Pipeline" not in result.stdout
