"""Workspace management and directory layout.

Workspace structure:
    <workspace_root>/
        db.sqlite          # SQLite index for runs/artifacts
        runs/              # RunTrace JSON files
            <run_id>.json
        artifacts/         # Artifact storage
            <run_id>/
                <artifact_id>_<filename>
"""

from __future__ import annotations

import os
from pathlib import Path

from ag.config import get_workspace_dir


class WorkspaceError(Exception):
    """Raised when workspace operations fail."""

    pass


class Workspace:
    """Manages a workspace directory and its structure."""

    RUNS_DIR = "runs"
    ARTIFACTS_DIR = "artifacts"
    DB_FILE = "db.sqlite"

    def __init__(self, workspace_id: str, root_path: Path | None = None) -> None:
        """Initialize workspace.

        Args:
            workspace_id: Unique identifier for the workspace
            root_path: Base path for workspaces. Defaults to ~/.ag/workspaces/
        """
        self.workspace_id = workspace_id
        self._root = root_path or get_workspace_dir()
        self._path = self._root / workspace_id

    @property
    def path(self) -> Path:
        """Workspace root directory."""
        return self._path

    @property
    def runs_dir(self) -> Path:
        """Directory for RunTrace JSON files."""
        return self._path / self.RUNS_DIR

    @property
    def artifacts_dir(self) -> Path:
        """Directory for artifact storage."""
        return self._path / self.ARTIFACTS_DIR

    @property
    def db_path(self) -> Path:
        """Path to SQLite database."""
        return self._path / self.DB_FILE

    def ensure_exists(self) -> None:
        """Create workspace directory structure if it doesn't exist."""
        self._path.mkdir(parents=True, exist_ok=True)
        self.runs_dir.mkdir(exist_ok=True)
        self.artifacts_dir.mkdir(exist_ok=True)

    def exists(self) -> bool:
        """Check if workspace exists."""
        return self._path.exists()

    def run_path(self, run_id: str) -> Path:
        """Get path for a specific run's JSON file."""
        _validate_safe_path_component(run_id)
        return self.runs_dir / f"{run_id}.json"

    def artifact_dir_for_run(self, run_id: str) -> Path:
        """Get artifact directory for a specific run."""
        _validate_safe_path_component(run_id)
        return self.artifacts_dir / run_id

    def artifact_path(self, run_id: str, artifact_id: str, filename: str) -> Path:
        """Get path for a specific artifact."""
        _validate_safe_path_component(run_id)
        _validate_safe_path_component(artifact_id)
        _validate_safe_filename(filename)
        run_artifact_dir = self.artifact_dir_for_run(run_id)
        run_artifact_dir.mkdir(exist_ok=True)
        return run_artifact_dir / f"{artifact_id}_{filename}"


def _validate_safe_path_component(component: str) -> None:
    """Validate that a path component is safe (no traversal)."""
    if not component:
        raise WorkspaceError("Path component cannot be empty")
    if "/" in component or "\\" in component:
        raise WorkspaceError(f"Path component cannot contain slashes: {component}")
    if component in (".", ".."):
        raise WorkspaceError(f"Invalid path component: {component}")
    if os.path.sep in component:
        raise WorkspaceError(f"Path component cannot contain separator: {component}")


def _validate_safe_filename(filename: str) -> None:
    """Validate that a filename is safe."""
    _validate_safe_path_component(filename)
    # Additional filename checks
    forbidden = '<>:"|?*'
    for char in forbidden:
        if char in filename:
            raise WorkspaceError(f"Filename contains forbidden character '{char}': {filename}")
