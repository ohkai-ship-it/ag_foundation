"""
CLI tests for ag_foundation.

These tests verify the CLI entrypoint and manual mode gating.
"""

import os

import pytest
from typer.testing import CliRunner

from ag.cli.main import app, DEV_ENV_VAR

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
        """ag run with a prompt should work."""
        monkeypatch.delenv(DEV_ENV_VAR, raising=False)

        result = runner.invoke(app, ["run", "Hello world"])

        assert result.exit_code == 0
        assert "Hello world" in result.stdout

    def test_run_with_workspace_option(self, monkeypatch):
        """ag run --workspace should accept workspace option."""
        monkeypatch.delenv(DEV_ENV_VAR, raising=False)

        result = runner.invoke(app, ["run", "--workspace", "my_ws", "Test"])

        assert result.exit_code == 0
        assert "my_ws" in result.stdout

    def test_run_with_playbook_option(self, monkeypatch):
        """ag run --playbook should accept playbook option."""
        monkeypatch.delenv(DEV_ENV_VAR, raising=False)

        result = runner.invoke(app, ["run", "--playbook", "custom", "Test"])

        # Should not fail; option is accepted (stub doesn't use it yet)
        assert result.exit_code == 0
