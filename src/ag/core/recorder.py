"""V0 Recorder implementation.

Extracted from runtime.py (AF-0114).
"""

from __future__ import annotations

from ag.core.run_trace import Artifact, RunTrace
from ag.storage import SQLiteArtifactStore, SQLiteRunStore


class V0Recorder:
    """v0 Recorder: persists traces and artifacts to storage."""

    def __init__(
        self,
        run_store: SQLiteRunStore | None = None,
        artifact_store: SQLiteArtifactStore | None = None,
    ) -> None:
        self._run_store = run_store or SQLiteRunStore()
        self._artifact_store = artifact_store or SQLiteArtifactStore()

    def record(self, trace: RunTrace) -> None:
        """Persist a RunTrace."""
        self._run_store.save(trace)

    def register_artifact(
        self,
        trace: RunTrace,
        artifact_id: str,
        path: str,
        content: bytes,
        artifact_type: str = "application/octet-stream",
    ) -> str:
        """Register an artifact for a run."""
        artifact = Artifact(
            artifact_id=artifact_id,
            path=path,
            artifact_type=artifact_type,
            size_bytes=len(content),
        )
        return self._artifact_store.save(trace.workspace_id, trace.run_id, artifact, content)

    def close(self) -> None:
        """Close storage connections."""
        self._run_store.close()
        self._artifact_store.close()
