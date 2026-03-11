"""Storage interfaces for runs and artifacts.

All storage operations are scoped by workspace_id.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from ag.core import Artifact, RunTrace


class RunStore(Protocol):
    """Interface for run storage operations."""

    def save(self, trace: RunTrace) -> None:
        """Persist a RunTrace.

        Args:
            trace: The RunTrace to persist
        """
        ...

    def get(self, workspace_id: str, run_id: str) -> RunTrace | None:
        """Retrieve a RunTrace by ID.

        Args:
            workspace_id: Workspace to search in
            run_id: The run ID to retrieve

        Returns:
            The RunTrace if found, None otherwise
        """
        ...

    def list(self, workspace_id: str, limit: int = 100) -> list[RunTrace]:
        """List runs in a workspace.

        Args:
            workspace_id: Workspace to list runs from
            limit: Maximum number of runs to return

        Returns:
            List of RunTrace objects, most recent first
        """
        ...

    def count(self, workspace_id: str) -> int:
        """Count total runs in a workspace.

        Args:
            workspace_id: Workspace to count runs in

        Returns:
            Total number of runs in the workspace
        """
        ...

    def delete(self, workspace_id: str, run_id: str) -> bool:
        """Delete a run.

        Args:
            workspace_id: Workspace containing the run
            run_id: The run ID to delete

        Returns:
            True if deleted, False if not found
        """
        ...


class ArtifactStore(Protocol):
    """Interface for artifact storage operations."""

    def save(self, workspace_id: str, run_id: str, artifact: Artifact, content: bytes) -> str:
        """Store an artifact and its content.

        Args:
            workspace_id: Workspace to store in
            run_id: Run that produced this artifact
            artifact: Artifact metadata
            content: Artifact content bytes

        Returns:
            Storage path/URI for the artifact
        """
        ...

    def get(
        self, workspace_id: str, run_id: str, artifact_id: str
    ) -> tuple[Artifact, bytes] | None:
        """Retrieve an artifact and its content.

        Args:
            workspace_id: Workspace to search in
            run_id: Run that produced the artifact
            artifact_id: The artifact ID to retrieve

        Returns:
            Tuple of (Artifact metadata, content bytes) if found, None otherwise
        """
        ...

    def list(self, workspace_id: str, run_id: str) -> list[Artifact]:
        """List artifacts for a run.

        Args:
            workspace_id: Workspace to search in
            run_id: Run to list artifacts for

        Returns:
            List of Artifact metadata objects
        """
        ...

    def delete(self, workspace_id: str, run_id: str, artifact_id: str) -> bool:
        """Delete an artifact.

        Args:
            workspace_id: Workspace containing the artifact
            run_id: Run that produced the artifact
            artifact_id: The artifact ID to delete

        Returns:
            True if deleted, False if not found
        """
        ...
