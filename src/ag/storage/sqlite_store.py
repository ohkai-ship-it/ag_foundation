"""SQLite-based storage implementation.

Provides workspace-scoped storage for runs and artifacts.
"""

from __future__ import annotations

import hashlib
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

from ag.config import get_workspace_dir

from .workspace import Workspace

if TYPE_CHECKING:
    from ag.core import Artifact, RunTrace


# ---------------------------------------------------------------------------
# SQLite Schema
# ---------------------------------------------------------------------------

SCHEMA_VERSION = 1

SCHEMA_SQL = """
-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY
);

-- Runs index (JSON stored on filesystem, indexed here)
CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    mode TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    duration_ms INTEGER,
    playbook_name TEXT NOT NULL,
    playbook_version TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_runs_workspace ON runs(workspace_id);
CREATE INDEX IF NOT EXISTS idx_runs_started ON runs(workspace_id, started_at DESC);

-- Artifacts index
CREATE TABLE IF NOT EXISTS artifacts (
    artifact_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    path TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    size_bytes INTEGER,
    checksum TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES runs(run_id)
);

CREATE INDEX IF NOT EXISTS idx_artifacts_run ON artifacts(run_id);
CREATE INDEX IF NOT EXISTS idx_artifacts_workspace ON artifacts(workspace_id);
"""


def _init_db(db_path: Path) -> sqlite3.Connection:
    """Initialize database with schema."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA_SQL)

    # Check/set schema version
    cursor = conn.execute("SELECT version FROM schema_version LIMIT 1")
    row = cursor.fetchone()
    if row is None:
        conn.execute("INSERT INTO schema_version (version) VALUES (?)", (SCHEMA_VERSION,))
    conn.commit()
    return conn


# ---------------------------------------------------------------------------
# SQLite RunStore Implementation
# ---------------------------------------------------------------------------


class SQLiteRunStore:
    """SQLite-backed run storage."""

    def __init__(self, workspaces_root: Path | None = None) -> None:
        """Initialize run store.

        Args:
            workspaces_root: Root path for workspaces. Defaults to ~/.ag/workspaces/
        """
        self._root = workspaces_root or get_workspace_dir()
        self._connections: dict[str, sqlite3.Connection] = {}

    def _get_workspace(self, workspace_id: str) -> Workspace:
        """Get or create workspace."""
        ws = Workspace(workspace_id, self._root)
        ws.ensure_exists()
        return ws

    def _get_conn(self, workspace_id: str) -> sqlite3.Connection:
        """Get database connection for workspace."""
        if workspace_id not in self._connections:
            ws = self._get_workspace(workspace_id)
            self._connections[workspace_id] = _init_db(ws.db_path)
        return self._connections[workspace_id]

    def save(self, trace: "RunTrace") -> None:
        """Persist a RunTrace."""

        ws = self._get_workspace(trace.workspace_id)
        conn = self._get_conn(trace.workspace_id)

        # Ensure run directory exists (new in v0.2 structure)
        run_dir = ws.run_dir(trace.run_id)
        run_dir.mkdir(parents=True, exist_ok=True)

        # Write JSON to filesystem
        json_path = ws.run_path(trace.run_id)
        json_path.write_text(trace.to_json(), encoding="utf-8")

        # Index in SQLite
        now = datetime.now(UTC).isoformat()
        conn.execute(
            """
            INSERT OR REPLACE INTO runs
            (run_id, workspace_id, mode, status, started_at, ended_at,
             duration_ms, playbook_name, playbook_version, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                trace.run_id,
                trace.workspace_id,
                trace.mode.value,
                trace.final.value,
                trace.started_at.isoformat(),
                trace.ended_at.isoformat() if trace.ended_at else None,
                trace.duration_ms,
                trace.playbook.name,
                trace.playbook.version,
                now,
            ),
        )
        conn.commit()

    def get(self, workspace_id: str, run_id: str) -> "RunTrace | None":
        """Retrieve a RunTrace by ID."""
        from ag.core import RunTrace

        ws = Workspace(workspace_id, self._root)
        if not ws.exists():
            return None

        json_path = ws.run_path(run_id)
        if not json_path.exists():
            return None

        return RunTrace.from_json(json_path.read_text(encoding="utf-8"))

    def list(self, workspace_id: str, limit: int = 100) -> "list[RunTrace]":
        """List runs in a workspace, most recent first."""

        ws = Workspace(workspace_id, self._root)
        if not ws.exists():
            return []

        conn = self._get_conn(workspace_id)
        cursor = conn.execute(
            """
            SELECT run_id FROM runs
            WHERE workspace_id = ?
            ORDER BY started_at DESC
            LIMIT ?
            """,
            (workspace_id, limit),
        )

        runs = []
        for row in cursor:
            trace = self.get(workspace_id, row["run_id"])
            if trace:
                runs.append(trace)
        return runs

    def count(self, workspace_id: str) -> int:
        """Count total runs in a workspace."""
        ws = Workspace(workspace_id, self._root)
        if not ws.exists():
            return 0

        conn = self._get_conn(workspace_id)
        cursor = conn.execute(
            "SELECT COUNT(*) FROM runs WHERE workspace_id = ?",
            (workspace_id,),
        )
        return cursor.fetchone()[0]

    def delete(self, workspace_id: str, run_id: str) -> bool:
        """Delete a run."""
        ws = Workspace(workspace_id, self._root)
        if not ws.exists():
            return False

        json_path = ws.run_path(run_id)
        if not json_path.exists():
            return False

        # Remove from index
        conn = self._get_conn(workspace_id)
        conn.execute("DELETE FROM runs WHERE run_id = ?", (run_id,))
        conn.commit()

        # Remove file
        json_path.unlink()
        return True

    def close(self) -> None:
        """Close all database connections."""
        for conn in self._connections.values():
            conn.close()
        self._connections.clear()

    def __del__(self) -> None:
        """Ensure connections are closed on garbage collection."""
        self.close()

    def __enter__(self) -> "SQLiteRunStore":
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Context manager exit - ensures connections are closed."""
        self.close()


# ---------------------------------------------------------------------------
# SQLite ArtifactStore Implementation
# ---------------------------------------------------------------------------


class SQLiteArtifactStore:
    """SQLite-backed artifact storage."""

    def __init__(self, workspaces_root: Path | None = None) -> None:
        """Initialize artifact store.

        Args:
            workspaces_root: Root path for workspaces. Defaults to ~/.ag/workspaces/
        """
        self._root = workspaces_root or get_workspace_dir()
        self._connections: dict[str, sqlite3.Connection] = {}

    def _get_workspace(self, workspace_id: str) -> Workspace:
        """Get or create workspace."""
        ws = Workspace(workspace_id, self._root)
        ws.ensure_exists()
        return ws

    def _get_conn(self, workspace_id: str) -> sqlite3.Connection:
        """Get database connection for workspace."""
        if workspace_id not in self._connections:
            ws = self._get_workspace(workspace_id)
            self._connections[workspace_id] = _init_db(ws.db_path)
        return self._connections[workspace_id]

    def save(self, workspace_id: str, run_id: str, artifact: "Artifact", content: bytes) -> str:
        """Store an artifact and its content."""
        ws = self._get_workspace(workspace_id)
        conn = self._get_conn(workspace_id)

        # Compute checksum if not provided
        checksum = artifact.checksum or hashlib.sha256(content).hexdigest()

        # Extract filename from path
        filename = Path(artifact.path).name or "artifact"

        # Write content to filesystem
        artifact_path = ws.artifact_path(run_id, artifact.artifact_id, filename)
        artifact_path.write_bytes(content)

        # Index in SQLite
        now = datetime.now(UTC).isoformat()
        conn.execute(
            """
            INSERT OR REPLACE INTO artifacts
            (artifact_id, run_id, workspace_id, path, artifact_type,
             size_bytes, checksum, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                artifact.artifact_id,
                run_id,
                workspace_id,
                str(artifact_path),
                artifact.artifact_type,
                len(content),
                checksum,
                now,
            ),
        )
        conn.commit()

        return str(artifact_path)

    def get(
        self, workspace_id: str, run_id: str, artifact_id: str
    ) -> "tuple[Artifact, bytes] | None":
        """Retrieve an artifact and its content."""
        from ag.core import Artifact

        ws = Workspace(workspace_id, self._root)
        if not ws.exists():
            return None

        conn = self._get_conn(workspace_id)
        cursor = conn.execute(
            """
            SELECT artifact_id, path, artifact_type, size_bytes, checksum, created_at
            FROM artifacts
            WHERE artifact_id = ? AND run_id = ? AND workspace_id = ?
            """,
            (artifact_id, run_id, workspace_id),
        )
        row = cursor.fetchone()
        if not row:
            return None

        # Read content
        artifact_path = Path(row["path"])
        if not artifact_path.exists():
            return None

        content = artifact_path.read_bytes()

        artifact = Artifact(
            artifact_id=row["artifact_id"],
            path=row["path"],
            artifact_type=row["artifact_type"],
            size_bytes=row["size_bytes"],
            checksum=row["checksum"],
        )
        return artifact, content

    def list(self, workspace_id: str, run_id: str) -> "list[Artifact]":
        """List artifacts for a run."""
        from ag.core import Artifact

        ws = Workspace(workspace_id, self._root)
        if not ws.exists():
            return []

        conn = self._get_conn(workspace_id)
        cursor = conn.execute(
            """
            SELECT artifact_id, path, artifact_type, size_bytes, checksum, created_at
            FROM artifacts
            WHERE run_id = ? AND workspace_id = ?
            ORDER BY created_at
            """,
            (run_id, workspace_id),
        )

        artifacts = []
        for row in cursor:
            artifacts.append(
                Artifact(
                    artifact_id=row["artifact_id"],
                    path=row["path"],
                    artifact_type=row["artifact_type"],
                    size_bytes=row["size_bytes"],
                    checksum=row["checksum"],
                )
            )
        return artifacts

    def delete(self, workspace_id: str, run_id: str, artifact_id: str) -> bool:
        """Delete an artifact."""
        ws = Workspace(workspace_id, self._root)
        if not ws.exists():
            return False

        conn = self._get_conn(workspace_id)

        # Get path first
        cursor = conn.execute("SELECT path FROM artifacts WHERE artifact_id = ?", (artifact_id,))
        row = cursor.fetchone()
        if not row:
            return False

        # Remove from index
        conn.execute("DELETE FROM artifacts WHERE artifact_id = ?", (artifact_id,))
        conn.commit()

        # Remove file
        artifact_path = Path(row["path"])
        if artifact_path.exists():
            artifact_path.unlink()

        return True

    def close(self) -> None:
        """Close all database connections."""
        for conn in self._connections.values():
            conn.close()
        self._connections.clear()

    def __del__(self) -> None:
        """Ensure connections are closed on garbage collection."""
        self.close()

    def __enter__(self) -> "SQLiteArtifactStore":
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Context manager exit - ensures connections are closed."""
        self.close()
