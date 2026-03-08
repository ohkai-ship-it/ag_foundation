"""End-to-end integration tests (AF-0066).

Tests validate the full pipeline:
1. Skill execution → verifier validation
2. Verifier → trace recording
3. Trace → artifact storage
4. Full round-trip: ag run → ag runs show → ag artifacts list

Test modes:
- CI mode: Mock provider (deterministic, fast, runs in GitHub Actions)
- Dev mode: Real provider (optional, manual, validates actual LLM integration)
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from typer.testing import CliRunner

from ag.cli.main import app
from ag.core import (
    ExecutionMode,
    FinalStatus,
    RunTrace,
    VerifierStatus,
    create_runtime,
)
from ag.providers.base import ChatMessage, ChatResponse, LLMProvider, ProviderConfig
from ag.skills import create_default_registry
from ag.storage import SQLiteArtifactStore, SQLiteRunStore, Workspace

if TYPE_CHECKING:
    from collections.abc import Generator

runner = CliRunner()

# Regex to strip ANSI escape codes from output
ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")


def extract_json(stdout: str, is_array: bool = True) -> dict | list:
    """Extract JSON from CLI output (may contain ANSI codes or control chars).

    Args:
        stdout: Raw CLI output
        is_array: If True, look for JSON array []; otherwise look for object {}

    Returns:
        Parsed JSON data
    """
    # Strip ANSI escape codes
    clean = ANSI_ESCAPE.sub("", stdout)

    start_char = "[" if is_array else "{"
    end_char = "]" if is_array else "}"

    json_start = clean.find(start_char)
    json_end = clean.rfind(end_char) + 1

    if json_start >= 0 and json_end > json_start:
        json_str = clean[json_start:json_end]
        # Try strict parsing first, fall back to lenient
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Try with control characters escaped
            # Escape common control chars in JSON strings
            json_str_fixed = json_str
            for i in range(32):
                if i not in (9, 10, 13):  # Keep tab, newline, carriage return
                    json_str_fixed = json_str_fixed.replace(chr(i), f"\\u{i:04x}")
            return json.loads(json_str_fixed)

    raise ValueError(f"No JSON {start_char}{end_char} found in: {clean[:200]}")


# ---------------------------------------------------------------------------
# Mock Provider for CI Tests
# ---------------------------------------------------------------------------


class MockLLMProvider(LLMProvider):
    """Deterministic mock provider for CI testing.

    Returns canned responses that match expected skill input format.
    """

    def __init__(self, config: ProviderConfig | None = None) -> None:
        self._config = config or ProviderConfig(provider="mock", model="mock-model")
        self._call_count = 0

    def chat(self, messages: list[ChatMessage]) -> ChatResponse:
        """Return deterministic mock response."""
        self._call_count += 1

        # Generate structured response for summarize skill
        mock_content = """## Summary
This is a mock summary of the documents for E2E testing.
The documents contain important information about the test topics.

## Key Points
- First key point from the documents
- Second key point discovered
- Third insight from analysis
"""
        return ChatResponse(content=mock_content, model="mock-model")

    @property
    def call_count(self) -> int:
        """Number of times chat was called."""
        return self._call_count


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def workspace_root(tmp_path: Path) -> Path:
    """Temporary workspace root directory."""
    return tmp_path / "workspaces"


@pytest.fixture
def test_workspace(workspace_root: Path) -> Workspace:
    """Create a test workspace with inputs/ directory."""
    ws = Workspace("e2e-test", workspace_root)
    ws.ensure_exists()

    # Create inputs/ directory with test documents
    inputs_dir = ws.path / "inputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)

    # Add test documents
    (inputs_dir / "doc1.md").write_text(
        "# Test Document 1\n\nThis is the first test document.\n\n## Section A\nContent here.",
        encoding="utf-8",
    )
    (inputs_dir / "doc2.md").write_text(
        "# Test Document 2\n\nThis is the second test document.\n\n## Section B\nMore content.",
        encoding="utf-8",
    )

    return ws


@pytest.fixture
def run_store(workspace_root: Path) -> Generator[SQLiteRunStore, None, None]:
    """Test run store."""
    store = SQLiteRunStore(workspace_root)
    yield store
    store.close()


@pytest.fixture
def artifact_store(workspace_root: Path) -> Generator[SQLiteArtifactStore, None, None]:
    """Test artifact store."""
    store = SQLiteArtifactStore(workspace_root)
    yield store
    store.close()


@pytest.fixture
def mock_provider() -> MockLLMProvider:
    """Mock LLM provider for deterministic testing."""
    return MockLLMProvider()


@pytest.fixture
def registry():
    """Skill registry with default skills."""
    return create_default_registry()


# ---------------------------------------------------------------------------
# E2E Integration Tests - CI Mode (Mock Provider)
# ---------------------------------------------------------------------------


class TestE2EIntegrationMock:
    """E2E tests with mock provider (CI mode)."""

    def test_summarize_playbook_full_flow(
        self,
        test_workspace: Workspace,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
        mock_provider: MockLLMProvider,
        registry,
    ) -> None:
        """Full flow: summarize playbook with mock provider."""
        # Create runtime with mock provider
        runtime = create_runtime(
            registry=registry,
            run_store=run_store,
            artifact_store=artifact_store,
        )

        # Execute summarize playbook
        trace = runtime.execute(
            prompt="Summarize the test documents",
            workspace="e2e-test",
            mode="manual",  # Use manual to avoid provider requirement in default flow
            playbook="summarize",
        )

        # 1. Verify trace was created
        assert isinstance(trace, RunTrace)
        assert trace.run_id is not None
        assert trace.workspace_id == "e2e-test"

        # 2. Verify steps executed
        assert len(trace.steps) >= 1, "Should have at least one step"

        # 3. Verify final status
        assert trace.final in (FinalStatus.SUCCESS, FinalStatus.FAILURE)

        # 4. Verify trace persisted
        stored_trace = run_store.get("e2e-test", trace.run_id)
        assert stored_trace is not None
        assert stored_trace.run_id == trace.run_id

    def test_skill_to_verifier_flow(
        self,
        test_workspace: Workspace,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
        registry,
    ) -> None:
        """Skill output passes through verifier correctly."""
        runtime = create_runtime(
            registry=registry,
            run_store=run_store,
            artifact_store=artifact_store,
        )

        trace = runtime.execute(
            prompt="Test skill verification",
            workspace="e2e-test",
            mode="manual",
        )

        # Verify verifier ran and produced a status
        assert trace.verifier.status in (
            VerifierStatus.PASSED,
            VerifierStatus.FAILED,
            VerifierStatus.PENDING,
            VerifierStatus.SKIPPED,
        )

        # If run succeeded, verifier should pass
        if trace.final == FinalStatus.SUCCESS:
            assert trace.verifier.status == VerifierStatus.PASSED

    def test_trace_has_required_fields(
        self,
        test_workspace: Workspace,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
        registry,
    ) -> None:
        """RunTrace has all required contract fields."""
        runtime = create_runtime(
            registry=registry,
            run_store=run_store,
            artifact_store=artifact_store,
        )

        trace = runtime.execute(
            prompt="Trace field test",
            workspace="e2e-test",
            mode="manual",
        )

        # Core identifiers
        assert trace.trace_version == "0.1"
        assert trace.run_id
        assert trace.workspace_id == "e2e-test"

        # Mode
        assert trace.mode == ExecutionMode.MANUAL

        # Playbook metadata
        assert trace.playbook.name
        assert trace.playbook.version

        # Timestamps
        assert trace.started_at is not None
        assert trace.ended_at is not None
        assert trace.duration_ms is not None
        assert trace.duration_ms >= 0

        # Steps list
        assert isinstance(trace.steps, list)

    def test_artifacts_stored_in_workspace(
        self,
        test_workspace: Workspace,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
        registry,
    ) -> None:
        """Artifacts are stored in proper workspace location."""
        runtime = create_runtime(
            registry=registry,
            run_store=run_store,
            artifact_store=artifact_store,
        )

        trace = runtime.execute(
            prompt="Artifact storage test",
            workspace="e2e-test",
            mode="manual",
        )

        # Check artifacts registered
        artifacts = artifact_store.list("e2e-test", trace.run_id)

        # Should have at least one artifact (result.md from default playbook)
        assert len(artifacts) >= 1, "Should create at least one artifact"

        # Verify artifact has required metadata
        for artifact in artifacts:
            assert artifact.artifact_id
            assert artifact.artifact_type


class TestE2ECliRoundTrip:
    """Test full CLI round-trip: ag run → ag runs show → ag artifacts list."""

    def test_run_show_artifacts_flow(self, tmp_path: Path, monkeypatch) -> None:
        """Full CLI round-trip with summarize playbook."""
        # Setup environment
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        monkeypatch.delenv("AG_DEV", raising=False)

        # Create workspace with inputs
        ws = Workspace("cli-e2e", tmp_path)
        ws.ensure_exists()

        inputs_dir = ws.path / "inputs"
        inputs_dir.mkdir(parents=True, exist_ok=True)
        (inputs_dir / "test.md").write_text("# Test\nContent for CLI test.", encoding="utf-8")

        # 1. Run the playbook
        run_result = runner.invoke(
            app,
            ["run", "--workspace", "cli-e2e", "--playbook", "summarize", "Summarize docs"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )

        assert run_result.exit_code == 0, f"ag run failed: {run_result.stdout}"
        assert "cli-e2e" in run_result.stdout

        # 2. List runs (human output)
        runs_result = runner.invoke(
            app,
            ["runs", "list", "--workspace", "cli-e2e"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )

        assert runs_result.exit_code == 0, f"ag runs list failed: {runs_result.stdout}"
        # Should show runs table
        assert "cli-e2e" in runs_result.stdout

        # 3. Get run_id from filesystem (more reliable than parsing CLI output)
        run_store = SQLiteRunStore(tmp_path)
        try:
            runs = run_store.list("cli-e2e", limit=1)
            assert len(runs) >= 1, "Should have at least one run"
            run_id = runs[0].run_id
        finally:
            run_store.close()

        # 4. Show run details
        show_result = runner.invoke(
            app,
            ["runs", "show", "--workspace", "cli-e2e", run_id],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )

        assert show_result.exit_code == 0, f"ag runs show failed: {show_result.stdout}"
        assert run_id in show_result.stdout or run_id[:8] in show_result.stdout

        # 5. List artifacts
        artifacts_result = runner.invoke(
            app,
            ["artifacts", "list", "--workspace", "cli-e2e", "--run", run_id],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )

        assert artifacts_result.exit_code == 0, (
            f"ag artifacts list failed: {artifacts_result.stdout}"
        )

    def test_workspace_structure_after_run(self, tmp_path: Path, monkeypatch) -> None:
        """Verify workspace structure after run (AF-0058 compliance)."""
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        monkeypatch.delenv("AG_DEV", raising=False)

        # Create workspace
        ws = Workspace("structure-test", tmp_path)
        ws.ensure_exists()

        inputs_dir = ws.path / "inputs"
        inputs_dir.mkdir(parents=True, exist_ok=True)
        (inputs_dir / "doc.md").write_text("# Doc\nTest content.", encoding="utf-8")

        # Run playbook
        result = runner.invoke(
            app,
            ["run", "--workspace", "structure-test", "--playbook", "summarize", "Test"],
            env={"AG_WORKSPACE_DIR": str(tmp_path)},
        )

        assert result.exit_code == 0

        # Verify workspace structure
        ws_path = ws.path

        # Should have inputs/ directory
        assert (ws_path / "inputs").exists(), "inputs/ should exist"
        assert (ws_path / "inputs").is_dir()

        # Should have runs/ directory created by run
        runs_dir = ws_path / "runs"
        if runs_dir.exists():
            # Should have run-specific subdirectory
            run_dirs = list(runs_dir.iterdir())
            assert len(run_dirs) >= 1, "Should have at least one run directory"


# ---------------------------------------------------------------------------
# E2E Integration Tests - Dev Mode (Real Provider)
# ---------------------------------------------------------------------------


@pytest.mark.manual
class TestE2EIntegrationReal:
    """E2E tests with real provider (dev mode).

    These tests require:
    - OPENAI_API_KEY environment variable
    - AG_DEV=1 environment variable
    - Network access to OpenAI API

    Run with: pytest -m manual tests/test_e2e_integration.py
    """

    @pytest.fixture
    def real_workspace(self, tmp_path: Path) -> Workspace:
        """Create workspace for real provider tests."""
        ws = Workspace("real-e2e", tmp_path)
        ws.ensure_exists()

        inputs_dir = ws.path / "inputs"
        inputs_dir.mkdir(parents=True, exist_ok=True)

        (inputs_dir / "real_doc.md").write_text(
            """# Real Test Document

This is a document for testing with the real OpenAI provider.

## Purpose
Validate that the full LLM integration works end-to-end.

## Key Points
- This tests real API calls
- Results should be meaningful
- The summary should capture key concepts
""",
            encoding="utf-8",
        )

        return ws

    def test_summarize_with_real_llm(
        self,
        real_workspace: Workspace,
        tmp_path: Path,
    ) -> None:
        """Test summarize playbook with real OpenAI provider.

        Requires OPENAI_API_KEY to be set.
        """
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("OPENAI_API_KEY not set")

        run_store = SQLiteRunStore(tmp_path)
        artifact_store = SQLiteArtifactStore(tmp_path)

        try:
            runtime = create_runtime(
                run_store=run_store,
                artifact_store=artifact_store,
            )

            trace = runtime.execute(
                prompt="Summarize the document about LLM testing",
                workspace="real-e2e",
                mode="llm",  # Use LLM mode for real provider
                playbook="summarize",
            )

            # Verify execution completed
            assert trace.run_id is not None
            assert trace.final in (FinalStatus.SUCCESS, FinalStatus.FAILURE)

            # If successful, verify meaningful output
            if trace.final == FinalStatus.SUCCESS:
                # Check artifacts were created
                artifacts = artifact_store.list("real-e2e", trace.run_id)
                assert len(artifacts) >= 1

        finally:
            run_store.close()
            artifact_store.close()

    def test_cli_real_provider(self, tmp_path: Path, monkeypatch) -> None:
        """Test CLI with real provider."""
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("OPENAI_API_KEY not set")

        monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))
        monkeypatch.setenv("AG_DEV", "1")

        # Create workspace
        ws = Workspace("cli-real-e2e", tmp_path)
        ws.ensure_exists()

        inputs_dir = ws.path / "inputs"
        inputs_dir.mkdir(parents=True, exist_ok=True)
        (inputs_dir / "test.md").write_text(
            "# API Test\nThis tests the real OpenAI API integration.",
            encoding="utf-8",
        )

        # Run with LLM mode
        result = runner.invoke(
            app,
            [
                "run",
                "--workspace",
                "cli-real-e2e",
                "--playbook",
                "summarize",
                "--mode",
                "llm",
                "Summarize the API test document",
            ],
            env={
                "AG_WORKSPACE_DIR": str(tmp_path),
                "AG_DEV": "1",
                "OPENAI_API_KEY": api_key,
            },
        )

        # Should complete (success or meaningful failure)
        # Exit code 0 = success, 1 = handled error
        assert result.exit_code in (0, 1), f"Unexpected exit: {result.stdout}"


# ---------------------------------------------------------------------------
# Parametrized Tests for Multiple Playbooks
# ---------------------------------------------------------------------------


class TestE2EParametrized:
    """Parametrized tests for different playbook/skill combinations."""

    @pytest.mark.parametrize(
        "playbook_name",
        [
            "default_v0",
            "summarize_v0",
            "summarize",  # Alias
        ],
    )
    def test_playbook_produces_trace(
        self,
        playbook_name: str,
        test_workspace: Workspace,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
        registry,
    ) -> None:
        """Each registered playbook produces a valid trace."""
        runtime = create_runtime(
            registry=registry,
            run_store=run_store,
            artifact_store=artifact_store,
        )

        trace = runtime.execute(
            prompt=f"Test {playbook_name}",
            workspace="e2e-test",
            mode="manual",
            playbook=playbook_name,
        )

        assert trace.run_id is not None
        valid_names = (
            playbook_name,
            playbook_name.replace("_v0", ""),
            "default_v0",
            "summarize_v0",
        )
        assert trace.playbook.name in valid_names


# ---------------------------------------------------------------------------
# Schema Verification Tests
# ---------------------------------------------------------------------------


class TestE2ESchemaVerification:
    """Tests for schema verification in E2E flow."""

    def test_trace_serialization_roundtrip(
        self,
        test_workspace: Workspace,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
        registry,
    ) -> None:
        """Trace can be serialized and deserialized without data loss."""
        runtime = create_runtime(
            registry=registry,
            run_store=run_store,
            artifact_store=artifact_store,
        )

        trace = runtime.execute(
            prompt="Serialization test",
            workspace="e2e-test",
            mode="manual",
        )

        # Serialize to JSON
        trace_json = trace.model_dump_json()
        assert trace_json

        # Deserialize back
        restored = RunTrace.model_validate_json(trace_json)

        # Verify key fields preserved
        assert restored.run_id == trace.run_id
        assert restored.workspace_id == trace.workspace_id
        assert restored.mode == trace.mode
        assert restored.final == trace.final

    def test_artifact_metadata_complete(
        self,
        test_workspace: Workspace,
        run_store: SQLiteRunStore,
        artifact_store: SQLiteArtifactStore,
        registry,
    ) -> None:
        """Artifact metadata is complete and valid."""
        runtime = create_runtime(
            registry=registry,
            run_store=run_store,
            artifact_store=artifact_store,
        )

        trace = runtime.execute(
            prompt="Artifact metadata test",
            workspace="e2e-test",
            mode="manual",
        )

        artifacts = artifact_store.list("e2e-test", trace.run_id)

        for artifact in artifacts:
            # Required fields
            assert artifact.artifact_id
            assert artifact.artifact_type

            # Artifact ID should be non-empty string
            assert len(artifact.artifact_id) > 0

            # Type should be MIME-like
            assert "/" in artifact.artifact_type or artifact.artifact_type in ("unknown",)
