"""Storage tests including workspace isolation.

Tests:
1. Workspace directory creation
2. RunStore basic operations
3. ArtifactStore basic operations
4. Isolation: two workspaces with runs, no cross-visibility
"""

from pathlib import Path

import pytest

from ag.core import (
    Artifact,
    ExecutionMode,
    FinalStatus,
    RunTrace,
    RunTraceBuilder,
    Step,
    StepType,
    VerifierStatus,
)
from ag.storage import (
    SQLiteArtifactStore,
    SQLiteRunStore,
    Workspace,
    WorkspaceError,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def temp_root(tmp_path: Path) -> Path:
    """Temporary workspace root directory."""
    return tmp_path / "workspaces"


@pytest.fixture
def workspace(temp_root: Path) -> Workspace:
    """Test workspace."""
    ws = Workspace("test-ws", temp_root)
    ws.ensure_exists()
    return ws


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


def _make_run_trace(workspace_id: str, run_id: str | None = None) -> RunTrace:
    """Create a test RunTrace."""
    return (
        RunTraceBuilder(workspace_id, ExecutionMode.MANUAL, "default", "1.0")
        .verify(VerifierStatus.PASSED)
        .complete(FinalStatus.SUCCESS)
        .build()
    )


# ---------------------------------------------------------------------------
# Workspace Tests
# ---------------------------------------------------------------------------


class TestWorkspace:
    """Tests for Workspace directory management."""

    def test_ensure_exists_creates_structure(self, temp_root: Path) -> None:
        """Workspace creates required directories on demand (AF0058 structure)."""
        ws = Workspace("my-workspace", temp_root)
        assert not ws.exists()

        ws.ensure_exists()

        assert ws.exists()
        assert ws.path.exists()
        assert ws.inputs_path.exists()  # AF0058: inputs/ folder for user content
        assert ws.runs_path.exists()  # AF0058: runs/ folder for run outputs

    def test_db_filename_is_canonical(self, temp_root: Path) -> None:
        """Workspace uses canonical db.sqlite filename (AF-0015)."""
        ws = Workspace("test-ws", temp_root)
        ws.ensure_exists()

        # Verify the canonical filename constant
        assert ws.DB_FILE == "db.sqlite"

        # Verify db_path uses the canonical filename
        assert ws.db_path.name == "db.sqlite"
        assert ws.db_path == ws.path / "db.sqlite"

    def test_path_safety_rejects_traversal(self, temp_root: Path) -> None:
        """Path components with traversal are rejected."""
        ws = Workspace("test-ws", temp_root)
        ws.ensure_exists()

        with pytest.raises(WorkspaceError):
            ws.run_path("../malicious")

        with pytest.raises(WorkspaceError):
            ws.run_path("foo/bar")

        with pytest.raises(WorkspaceError):
            ws.artifact_path("run1", "..", "file.txt")

    def test_path_safety_rejects_empty(self, temp_root: Path) -> None:
        """Empty path components are rejected."""
        ws = Workspace("test-ws", temp_root)
        ws.ensure_exists()

        with pytest.raises(WorkspaceError):
            ws.run_path("")

    def test_artifact_path_creates_run_dir(self, temp_root: Path) -> None:
        """Artifact path creates run-specific directory."""
        ws = Workspace("test-ws", temp_root)
        ws.ensure_exists()

        path = ws.artifact_path("run-123", "art-1", "output.txt")

        assert ws.artifact_dir_for_run("run-123").exists()
        assert path.parent == ws.artifact_dir_for_run("run-123")


# ---------------------------------------------------------------------------
# RunStore Tests
# ---------------------------------------------------------------------------


class TestRunStore:
    """Tests for SQLiteRunStore."""

    def test_save_and_get(self, run_store: SQLiteRunStore, temp_root: Path) -> None:
        """Can save and retrieve a RunTrace."""
        trace = _make_run_trace("ws-1")

        run_store.save(trace)
        retrieved = run_store.get("ws-1", trace.run_id)

        assert retrieved is not None
        assert retrieved.run_id == trace.run_id
        assert retrieved.workspace_id == trace.workspace_id
        assert retrieved.final == trace.final

    def test_get_nonexistent_returns_none(self, run_store: SQLiteRunStore, temp_root: Path) -> None:
        """Getting nonexistent run returns None."""
        result = run_store.get("ws-1", "nonexistent-run")
        assert result is None

    def test_list_returns_runs_ordered(self, run_store: SQLiteRunStore, temp_root: Path) -> None:
        """List returns runs in reverse chronological order."""
        trace1 = _make_run_trace("ws-1")
        trace2 = _make_run_trace("ws-1")

        run_store.save(trace1)
        run_store.save(trace2)

        runs = run_store.list("ws-1")

        assert len(runs) == 2
        # Most recent first (trace2 was saved after trace1)
        assert runs[0].run_id == trace2.run_id
        assert runs[1].run_id == trace1.run_id

    def test_delete(self, run_store: SQLiteRunStore, temp_root: Path) -> None:
        """Can delete a run."""
        trace = _make_run_trace("ws-1")
        run_store.save(trace)

        deleted = run_store.delete("ws-1", trace.run_id)
        assert deleted is True

        result = run_store.get("ws-1", trace.run_id)
        assert result is None

    def test_json_file_persisted(self, run_store: SQLiteRunStore, temp_root: Path) -> None:
        """RunTrace JSON is persisted to filesystem."""
        trace = _make_run_trace("ws-1")
        run_store.save(trace)

        ws = Workspace("ws-1", temp_root)
        json_path = ws.run_path(trace.run_id)

        assert json_path.exists()
        assert trace.run_id in json_path.read_text()

    def test_count_empty_workspace(self, run_store: SQLiteRunStore, temp_root: Path) -> None:
        """Count returns 0 for empty/nonexistent workspace."""
        assert run_store.count("nonexistent-ws") == 0

    def test_count_returns_total(self, run_store: SQLiteRunStore, temp_root: Path) -> None:
        """Count returns total number of runs in workspace."""
        # Save 3 runs
        for _ in range(3):
            trace = _make_run_trace("ws-1")
            run_store.save(trace)

        assert run_store.count("ws-1") == 3

        # Add one more
        run_store.save(_make_run_trace("ws-1"))
        assert run_store.count("ws-1") == 4

    def test_count_per_workspace(self, run_store: SQLiteRunStore, temp_root: Path) -> None:
        """Count is per-workspace."""
        run_store.save(_make_run_trace("ws-1"))
        run_store.save(_make_run_trace("ws-1"))
        run_store.save(_make_run_trace("ws-2"))

        assert run_store.count("ws-1") == 2
        assert run_store.count("ws-2") == 1

    def test_unicode_preserved_in_trace(self, run_store: SQLiteRunStore, temp_root: Path) -> None:
        """BUG-0014: Unicode characters in trace are preserved through save/load."""
        # Create workspace first
        ws = Workspace("ws-unicode", temp_root)
        ws.ensure_exists()

        # Build trace with Unicode characters
        builder = RunTraceBuilder("ws-unicode", ExecutionMode.MANUAL, "test", "1.0")
        builder.verify(VerifierStatus.PASSED)
        builder.complete(FinalStatus.SUCCESS)
        trace = builder.build()

        # Manually add a step with Unicode (since builder doesn't expose add_step simply)
        trace.steps.append(
            Step(
                step_id="unicode-step",
                step_number=0,
                step_type=StepType.SKILL_CALL,
                input_summary="Research the Düsseldorf meteorite",
                output_summary="Found information about météorites in München",
                started_at=trace.started_at,
                ended_at=trace.ended_at,
                duration_ms=100,
            )
        )

        run_store.save(trace)
        retrieved = run_store.get("ws-unicode", trace.run_id)

        assert retrieved is not None
        assert len(retrieved.steps) == 1
        assert retrieved.steps[0].input_summary == "Research the Düsseldorf meteorite"
        assert retrieved.steps[0].output_summary == "Found information about météorites in München"

        # Also verify via JSON file directly
        json_path = ws.run_path(trace.run_id)
        content = json_path.read_text(encoding="utf-8")

        # Verify Unicode chars are properly encoded in JSON
        assert "Düsseldorf" in content
        assert "météorites" in content
        assert "München" in content


# ---------------------------------------------------------------------------
# ArtifactStore Tests
# ---------------------------------------------------------------------------


class TestArtifactStore:
    """Tests for SQLiteArtifactStore."""

    def test_save_and_get(self, artifact_store: SQLiteArtifactStore, temp_root: Path) -> None:
        """Can save and retrieve an artifact."""
        artifact = Artifact(
            artifact_id="art-1",
            path="output.txt",
            artifact_type="text/plain",
        )
        content = b"Hello, world!"

        path = artifact_store.save("ws-1", "run-1", artifact, content)
        assert Path(path).exists()

        result = artifact_store.get("ws-1", "run-1", "art-1")
        assert result is not None
        retrieved_artifact, retrieved_content = result
        assert retrieved_artifact.artifact_id == "art-1"
        assert retrieved_content == content

    def test_list_empty(self, artifact_store: SQLiteArtifactStore, temp_root: Path) -> None:
        """Listing artifacts for nonexistent run returns empty list."""
        artifacts = artifact_store.list("ws-1", "run-1")
        assert artifacts == []

    def test_list_artifacts(self, artifact_store: SQLiteArtifactStore, temp_root: Path) -> None:
        """Can list artifacts for a run."""
        art1 = Artifact(artifact_id="art-1", path="file1.txt", artifact_type="text/plain")
        art2 = Artifact(artifact_id="art-2", path="file2.txt", artifact_type="text/plain")

        artifact_store.save("ws-1", "run-1", art1, b"content1")
        artifact_store.save("ws-1", "run-1", art2, b"content2")

        artifacts = artifact_store.list("ws-1", "run-1")

        assert len(artifacts) == 2
        ids = {a.artifact_id for a in artifacts}
        assert ids == {"art-1", "art-2"}

    def test_delete(self, artifact_store: SQLiteArtifactStore, temp_root: Path) -> None:
        """Can delete an artifact."""
        artifact = Artifact(
            artifact_id="art-1",
            path="output.txt",
            artifact_type="text/plain",
        )
        path = artifact_store.save("ws-1", "run-1", artifact, b"content")

        assert Path(path).exists()

        deleted = artifact_store.delete("ws-1", "run-1", "art-1")
        assert deleted is True

        assert not Path(path).exists()
        result = artifact_store.get("ws-1", "run-1", "art-1")
        assert result is None


# ---------------------------------------------------------------------------
# Workspace Isolation Tests (Critical for AF-0006)
# ---------------------------------------------------------------------------


class TestWorkspaceIsolation:
    """Tests proving workspace isolation - no cross-visibility of runs or artifacts."""

    def test_runs_isolated_between_workspaces(
        self, run_store: SQLiteRunStore, temp_root: Path
    ) -> None:
        """Runs in ws_a are not visible from ws_b and vice versa."""
        # Create runs in two separate workspaces
        trace_a = _make_run_trace("ws_a")
        trace_b = _make_run_trace("ws_b")

        run_store.save(trace_a)
        run_store.save(trace_b)

        # List runs in ws_a - should only see trace_a
        runs_a = run_store.list("ws_a")
        assert len(runs_a) == 1
        assert runs_a[0].run_id == trace_a.run_id
        assert runs_a[0].workspace_id == "ws_a"

        # List runs in ws_b - should only see trace_b
        runs_b = run_store.list("ws_b")
        assert len(runs_b) == 1
        assert runs_b[0].run_id == trace_b.run_id
        assert runs_b[0].workspace_id == "ws_b"

        # Cannot get ws_b's run from ws_a
        cross_get = run_store.get("ws_a", trace_b.run_id)
        assert cross_get is None

        # Cannot get ws_a's run from ws_b
        cross_get = run_store.get("ws_b", trace_a.run_id)
        assert cross_get is None

    def test_artifacts_isolated_between_workspaces(
        self, artifact_store: SQLiteArtifactStore, temp_root: Path
    ) -> None:
        """Artifacts in ws_a are not visible from ws_b."""
        art_a = Artifact(artifact_id="art-a", path="file_a.txt", artifact_type="text/plain")
        art_b = Artifact(artifact_id="art-b", path="file_b.txt", artifact_type="text/plain")

        artifact_store.save("ws_a", "run-1", art_a, b"content_a")
        artifact_store.save("ws_b", "run-1", art_b, b"content_b")

        # List artifacts in ws_a - should only see art_a
        artifacts_a = artifact_store.list("ws_a", "run-1")
        assert len(artifacts_a) == 1
        assert artifacts_a[0].artifact_id == "art-a"

        # List artifacts in ws_b - should only see art_b
        artifacts_b = artifact_store.list("ws_b", "run-1")
        assert len(artifacts_b) == 1
        assert artifacts_b[0].artifact_id == "art-b"

        # Cannot get ws_b's artifact from ws_a
        cross_get = artifact_store.get("ws_a", "run-1", "art-b")
        assert cross_get is None

    def test_disk_directories_separate(self, temp_root: Path) -> None:
        """Workspaces have physically separate directories."""
        ws_a = Workspace("ws_a", temp_root)
        ws_b = Workspace("ws_b", temp_root)

        ws_a.ensure_exists()
        ws_b.ensure_exists()

        # Directories are separate
        assert ws_a.path != ws_b.path
        assert ws_a.path.exists()
        assert ws_b.path.exists()

        # Write a file in ws_a
        test_file_a = ws_a.runs_dir / "test.txt"
        test_file_a.write_text("ws_a content")

        # File should not exist in ws_b
        test_file_b = ws_b.runs_dir / "test.txt"
        assert not test_file_b.exists()

    def test_sqlite_databases_separate(self, run_store: SQLiteRunStore, temp_root: Path) -> None:
        """Each workspace has its own SQLite database."""
        # Save runs to force database creation
        trace_a = _make_run_trace("ws_a")
        trace_b = _make_run_trace("ws_b")
        run_store.save(trace_a)
        run_store.save(trace_b)

        ws_a = Workspace("ws_a", temp_root)
        ws_b = Workspace("ws_b", temp_root)

        # Each workspace has its own db.sqlite
        assert ws_a.db_path.exists()
        assert ws_b.db_path.exists()
        assert ws_a.db_path != ws_b.db_path

    def test_multiple_runs_per_workspace_isolated(
        self, run_store: SQLiteRunStore, temp_root: Path
    ) -> None:
        """Multiple runs in each workspace stay isolated."""
        # Create 3 runs in ws_a, 2 runs in ws_b
        runs_a = [_make_run_trace("ws_a") for _ in range(3)]
        runs_b = [_make_run_trace("ws_b") for _ in range(2)]

        for trace in runs_a + runs_b:
            run_store.save(trace)

        # Verify counts
        listed_a = run_store.list("ws_a")
        listed_b = run_store.list("ws_b")

        assert len(listed_a) == 3
        assert len(listed_b) == 2

        # Verify all runs in list_a are from ws_a
        for trace in listed_a:
            assert trace.workspace_id == "ws_a"

        # Verify all runs in list_b are from ws_b
        for trace in listed_b:
            assert trace.workspace_id == "ws_b"

    def test_delete_in_one_workspace_does_not_affect_other(
        self, run_store: SQLiteRunStore, temp_root: Path
    ) -> None:
        """Deleting a run in ws_a does not affect ws_b."""
        trace_a = _make_run_trace("ws_a")
        trace_b = _make_run_trace("ws_b")

        run_store.save(trace_a)
        run_store.save(trace_b)

        # Delete from ws_a
        run_store.delete("ws_a", trace_a.run_id)

        # ws_b should still have its run
        retrieved_b = run_store.get("ws_b", trace_b.run_id)
        assert retrieved_b is not None
        assert retrieved_b.run_id == trace_b.run_id


# ---------------------------------------------------------------------------
# Connection Lifecycle Tests (AF-0021 regression)
# ---------------------------------------------------------------------------


class TestConnectionLifecycle:
    """Tests for deterministic connection closure (AF-0021, BUG-0001)."""

    def test_run_store_context_manager(self, temp_root: Path) -> None:
        """SQLiteRunStore works as context manager."""
        with SQLiteRunStore(temp_root) as store:
            trace = _make_run_trace("ctx-ws")
            store.save(trace)
            retrieved = store.get("ctx-ws", trace.run_id)
            assert retrieved is not None
        # Exiting context should have closed connections
        assert store._connections == {}

    def test_artifact_store_context_manager(self, temp_root: Path) -> None:
        """SQLiteArtifactStore works as context manager."""
        from ag.core import Artifact

        with SQLiteArtifactStore(temp_root) as store:
            artifact = Artifact(
                artifact_id="art-ctx",
                path="test.txt",
                artifact_type="text/plain",
                size_bytes=4,
            )
            store.save("ctx-ws", "run-1", artifact, b"test")
            artifacts = store.list("ctx-ws", "run-1")
            assert len(artifacts) == 1
        # Exiting context should have closed connections
        assert store._connections == {}

    def test_close_clears_connections(self, temp_root: Path) -> None:
        """Calling close() clears the connections dict."""
        store = SQLiteRunStore(temp_root)
        trace = _make_run_trace("close-ws")
        store.save(trace)
        # Connection should be cached
        assert len(store._connections) > 0

        store.close()
        assert store._connections == {}

    def test_multiple_workspaces_all_closed(self, temp_root: Path) -> None:
        """Multiple workspace connections are all closed."""
        with SQLiteRunStore(temp_root) as store:
            trace_a = _make_run_trace("multi-ws-a")
            trace_b = _make_run_trace("multi-ws-b")
            store.save(trace_a)
            store.save(trace_b)
            # Should have 2 connections (one per workspace)
            assert len(store._connections) == 2
        # After exit, all should be closed
        assert store._connections == {}
