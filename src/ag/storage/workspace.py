"""Workspace management and directory layout.

Workspace structure (v0.2 - AF0058):
    <workspace_root>/
        db.sqlite          # SQLite index for runs/artifacts
        inputs/            # User content (read by skills)
            *.md, *.txt, etc.
        runs/              # System outputs (per-run folders)
            <run_id>/
                trace.json     # RunTrace JSON
                artifacts/     # Artifacts for this run
                    <filename>
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

    INPUTS_DIR = "inputs"
    RUNS_DIR = "runs"
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
    def inputs_path(self) -> Path:
        """Directory for user input files (read by skills)."""
        return self._path / self.INPUTS_DIR

    @property
    def runs_path(self) -> Path:
        """Directory for run outputs (per-run folders)."""
        return self._path / self.RUNS_DIR

    # Backward compatibility alias
    @property
    def runs_dir(self) -> Path:
        """Alias for runs_path (backward compatibility)."""
        return self.runs_path

    @property
    def db_path(self) -> Path:
        """Path to SQLite database."""
        return self._path / self.DB_FILE

    def ensure_exists(self) -> None:
        """Create workspace directory structure if it doesn't exist."""
        self._path.mkdir(parents=True, exist_ok=True)
        self.inputs_path.mkdir(exist_ok=True)
        self.runs_path.mkdir(exist_ok=True)

    def exists(self) -> bool:
        """Check if workspace exists."""
        return self._path.exists()

    def run_dir(self, run_id: str) -> Path:
        """Get directory for a specific run's outputs."""
        _validate_safe_path_component(run_id)
        return self.runs_path / run_id

    def run_path(self, run_id: str) -> Path:
        """Get path for a specific run's trace JSON file."""
        return self.run_dir(run_id) / "trace.json"

    def artifact_dir_for_run(self, run_id: str) -> Path:
        """Get artifact directory for a specific run."""
        return self.run_dir(run_id) / "artifacts"

    def artifact_path(self, run_id: str, artifact_id: str, filename: str) -> Path:
        """Get path for a specific artifact.

        Args:
            run_id: Run identifier
            artifact_id: Artifact identifier (used for uniqueness)
            filename: Artifact filename

        Returns:
            Path: runs/<run_id>/artifacts/<artifact_id>_<filename>
        """
        _validate_safe_path_component(run_id)
        _validate_safe_path_component(artifact_id)
        _validate_safe_filename(filename)
        artifact_dir = self.artifact_dir_for_run(run_id)
        artifact_dir.mkdir(parents=True, exist_ok=True)
        return artifact_dir / f"{artifact_id}_{filename}"


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
