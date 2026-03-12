"""
Configuration precedence tests for ag_foundation (AF-0023).

Tests verify:
- Environment variable overrides work correctly
- Config resolution order is honored
- Centralized configuration from config.py is used throughout
"""

from pathlib import Path

import pytest


class TestWorkspaceDirResolution:
    """Tests for workspace directory resolution via get_workspace_dir()."""

    def test_default_workspace_dir(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """get_workspace_dir() returns default when no env var set."""
        # Clear any existing env var
        monkeypatch.delenv("AG_WORKSPACE_DIR", raising=False)

        from ag.config import DEFAULT_WORKSPACES_ROOT, get_workspace_dir

        result = get_workspace_dir()
        assert result == DEFAULT_WORKSPACES_ROOT
        assert str(result).endswith(".ag/workspaces") or str(result).endswith(".ag\\workspaces")

    def test_env_var_overrides_default(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """AG_WORKSPACE_DIR env var overrides default workspace directory."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        from ag.config import get_workspace_dir

        result = get_workspace_dir()
        assert result == tmp_path

    def test_env_var_with_path_separators(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """AG_WORKSPACE_DIR handles paths with various separators."""
        custom_path = tmp_path / "custom" / "workspace"
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(custom_path))

        from ag.config import get_workspace_dir

        result = get_workspace_dir()
        assert result == custom_path


class TestDefaultWorkspaceResolution:
    """Tests for default workspace ID resolution via get_default_workspace()."""

    def test_default_workspace_id(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """get_default_workspace() returns 'ws_default' when no env var set."""
        monkeypatch.delenv("AG_WORKSPACE", raising=False)

        from ag.config import get_default_workspace

        result = get_default_workspace()
        assert result == "ws_default"

    def test_env_var_overrides_default_workspace(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """AG_WORKSPACE env var overrides default workspace ID."""
        monkeypatch.setenv("AG_WORKSPACE", "my-custom-workspace")

        from ag.config import get_default_workspace

        result = get_default_workspace()
        assert result == "my-custom-workspace"


class TestConfigPathResolution:
    """Tests for config file path resolution via get_config_path()."""

    def test_default_config_path(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """get_config_path() returns default when no env var set."""
        monkeypatch.delenv("AG_CONFIG_PATH", raising=False)

        from ag.config import DEFAULT_CONFIG_FILE, get_config_path

        result = get_config_path()
        assert result == DEFAULT_CONFIG_FILE
        assert str(result).endswith("config.yaml")

    def test_env_var_overrides_config_path(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """AG_CONFIG_PATH env var overrides default config file path."""
        custom_config = tmp_path / "my-config.yaml"
        monkeypatch.setenv("AG_CONFIG_PATH", str(custom_config))

        from ag.config import get_config_path

        result = get_config_path()
        assert result == custom_config


class TestStorageUsesConfigModule:
    """Tests that storage modules use config.py for path resolution."""

    def test_sqlite_run_store_uses_config(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """SQLiteRunStore uses get_workspace_dir() from config module."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        from ag.storage import SQLiteRunStore

        store = SQLiteRunStore()
        assert store._root == tmp_path

    def test_sqlite_artifact_store_uses_config(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """SQLiteArtifactStore uses get_workspace_dir() from config module."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        from ag.storage import SQLiteArtifactStore

        store = SQLiteArtifactStore()
        assert store._root == tmp_path

    def test_workspace_uses_config(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """Workspace class uses get_workspace_dir() from config module."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))

        from ag.storage import Workspace

        ws = Workspace("test-ws")
        assert ws._root == tmp_path
        assert ws.path == tmp_path / "test-ws"


class TestConfigConstants:
    """Tests for configuration constants."""

    def test_default_paths_are_under_home(self) -> None:
        """Default config and workspace paths are under user home directory."""
        from ag.config import DEFAULT_CONFIG_DIR, DEFAULT_WORKSPACES_ROOT

        home = Path.home()
        assert DEFAULT_CONFIG_DIR.is_relative_to(home) or str(DEFAULT_CONFIG_DIR).startswith(
            str(home)
        )
        assert DEFAULT_WORKSPACES_ROOT.is_relative_to(home) or str(
            DEFAULT_WORKSPACES_ROOT
        ).startswith(str(home))

    def test_env_vars_documented(self) -> None:
        """All expected environment variables are documented in ENV_VARS."""
        from ag.config import ENV_VARS

        expected_vars = [
            "AG_CONFIG_PATH",
            "AG_WORKSPACE",
            "AG_WORKSPACE_DIR",
            "AG_LLM_API_KEY",
            "AG_LLM_MODEL",
            "AG_DEV",
            "AG_TELEMETRY",
        ]
        for var in expected_vars:
            assert var in ENV_VARS, f"Missing env var documentation: {var}"


class TestDoctorCommand:
    """Tests for ag doctor command."""

    def test_doctor_runs_without_error(self) -> None:
        """ag doctor command runs without error."""
        from typer.testing import CliRunner

        from ag.cli.main import app

        runner = CliRunner()
        result = runner.invoke(app, ["doctor"])

        assert result.exit_code == 0
        assert "ag doctor" in result.stdout

    def test_doctor_shows_version(self) -> None:
        """ag doctor shows version information."""
        from typer.testing import CliRunner

        from ag.cli.main import app

        runner = CliRunner()
        result = runner.invoke(app, ["doctor"])

        assert "Version:" in result.stdout

    def test_doctor_shows_python_version(self) -> None:
        """ag doctor shows Python version."""
        from typer.testing import CliRunner

        from ag.cli.main import app

        runner = CliRunner()
        result = runner.invoke(app, ["doctor"])

        assert "Python:" in result.stdout

    def test_doctor_shows_workspace_info(self) -> None:
        """ag doctor shows workspace storage information."""
        from typer.testing import CliRunner

        from ag.cli.main import app

        runner = CliRunner()
        result = runner.invoke(app, ["doctor"])

        assert "Workspace Storage" in result.stdout or "Workspace root" in result.stdout

    def test_doctor_shows_env_vars(self) -> None:
        """ag doctor shows environment variable status."""
        from typer.testing import CliRunner

        from ag.cli.main import app

        runner = CliRunner()
        result = runner.invoke(app, ["doctor"])

        assert "AG_DEV" in result.stdout

    def test_doctor_shows_config_resolution_order(self) -> None:
        """ag doctor shows configuration resolution order."""
        from typer.testing import CliRunner

        from ag.cli.main import app

        runner = CliRunner()
        result = runner.invoke(app, ["doctor"])

        assert "Resolution Order" in result.stdout or "resolution" in result.stdout.lower()


# ---------------------------------------------------------------------------
# Tests for persisted state (AF-0012 coverage boost)
# ---------------------------------------------------------------------------


class TestPersistedWorkspaceState:
    """Tests for persisted workspace default state file operations."""

    def test_get_persisted_default_workspace_returns_none_when_no_state(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """get_persisted_default_workspace() returns None when no state file exists."""
        # Use a clean temp directory for config
        monkeypatch.setenv("AG_CONFIG_DIR", str(tmp_path))

        from ag.config import get_persisted_default_workspace

        result = get_persisted_default_workspace()
        assert result is None

    def test_set_and_get_persisted_default_workspace(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """set_persisted_default_workspace() persists and get retrieves it."""
        monkeypatch.setenv("AG_CONFIG_DIR", str(tmp_path))

        from ag.config import (
            get_persisted_default_workspace,
            set_persisted_default_workspace,
        )

        # Initially none
        assert get_persisted_default_workspace() is None

        # Set a default
        set_persisted_default_workspace("my-workspace")
        assert get_persisted_default_workspace() == "my-workspace"

        # Change it
        set_persisted_default_workspace("another-ws")
        assert get_persisted_default_workspace() == "another-ws"

    def test_clear_persisted_default_workspace(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """set_persisted_default_workspace(None) clears the default."""
        monkeypatch.setenv("AG_CONFIG_DIR", str(tmp_path))

        from ag.config import (
            get_persisted_default_workspace,
            set_persisted_default_workspace,
        )

        # Set then clear
        set_persisted_default_workspace("my-workspace")
        assert get_persisted_default_workspace() == "my-workspace"

        set_persisted_default_workspace(None)
        assert get_persisted_default_workspace() is None

    def test_state_file_is_valid_json(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """State file contains valid JSON."""
        import json

        monkeypatch.setenv("AG_CONFIG_DIR", str(tmp_path))

        from ag.config import set_persisted_default_workspace

        set_persisted_default_workspace("test-ws")

        state_file = tmp_path / "state.json"
        assert state_file.exists()

        data = json.loads(state_file.read_text())
        assert data["default_workspace"] == "test-ws"

    def test_load_state_handles_corrupt_json(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """_load_state() returns empty dict on corrupt JSON."""
        monkeypatch.setenv("AG_CONFIG_DIR", str(tmp_path))

        # Write corrupt JSON
        state_file = tmp_path / "state.json"
        tmp_path.mkdir(parents=True, exist_ok=True)
        state_file.write_text("{ not valid json")

        from ag.config import get_persisted_default_workspace

        # Should not raise, returns None (empty state)
        result = get_persisted_default_workspace()
        assert result is None

    def test_config_dir_created_on_save(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Config directory is created if it doesn't exist when saving."""
        # Use a nested path that doesn't exist
        nested_config = tmp_path / "nested" / "config" / "dir"
        monkeypatch.setenv("AG_CONFIG_DIR", str(nested_config))

        from ag.config import set_persisted_default_workspace

        # Should create the directory
        set_persisted_default_workspace("new-ws")

        assert nested_config.exists()
        assert (nested_config / "state.json").exists()

    def test_load_config_returns_empty_dict(self) -> None:
        """load_config() returns empty dict (stub behavior)."""
        from ag.config import load_config

        result = load_config()
        assert result == {}
