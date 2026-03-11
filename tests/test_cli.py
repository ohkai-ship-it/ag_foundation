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
        monkeypatch.delenv(DEV_ENV_VAR, raising=False)
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        # Create workspace first
        from ag.storage import Workspace

        ws = Workspace("test-ws", tmp_path)
        ws.ensure_exists()

        result = runner.invoke(
            app,
            ["run", "--workspace", "test-ws", "Hello world"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
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
        env = {"AG_WORKSPACE_DIR": str(tmp_path)}

        # Create workspace explicitly
        from ag.storage import SQLiteRunStore, Workspace

        Workspace("stable-ws", tmp_path).ensure_exists()

        # Run multiple times
        for i in range(3):
            result = runner.invoke(
                app,
                ["run", "--workspace", "stable-ws", f"Run {i}"],
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

        # Check fields exist
        for pb in data:
            assert "name" in pb
            assert "version" in pb
            assert "stability" in pb
            assert "description" in pb

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
