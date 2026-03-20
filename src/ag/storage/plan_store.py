"""File-based plan storage implementation.

Stores execution plans as JSON files in the workspace's plans/ directory.
No SQLite indexing needed since plans are temporary and few in number.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

from ag.config import get_workspace_dir

from .workspace import Workspace

if TYPE_CHECKING:
    from ag.core import ExecutionPlan


class FilePlanStore:
    """File-based plan storage.

    Plans are stored as JSON files in <workspace>/plans/<plan_id>.json.
    Expired plans are automatically filtered out on list operations.
    """

    def __init__(self, workspaces_root: Path | None = None) -> None:
        """Initialize plan store.

        Args:
            workspaces_root: Root path for workspaces. Defaults to ~/.ag/workspaces/
        """
        self._root = workspaces_root or get_workspace_dir()

    def _get_workspace(self, workspace_id: str) -> Workspace:
        """Get or create workspace."""
        ws = Workspace(workspace_id, self._root)
        ws.ensure_exists()
        return ws

    def save(self, plan: "ExecutionPlan") -> None:
        """Persist an ExecutionPlan."""
        ws = self._get_workspace(plan.workspace_id)
        plan_path = ws.plan_path(plan.plan_id)
        plan_path.write_text(plan.to_json(), encoding="utf-8")

    def get(self, workspace_id: str, plan_id: str) -> "ExecutionPlan | None":
        """Retrieve an ExecutionPlan by ID."""
        from ag.core import ExecutionPlan

        ws = Workspace(workspace_id, self._root)
        if not ws.exists():
            return None

        plan_path = ws.plan_path(plan_id)
        if not plan_path.exists():
            return None

        return ExecutionPlan.from_json(plan_path.read_text(encoding="utf-8"))

    def list(
        self, workspace_id: str, include_expired: bool = False
    ) -> "list[ExecutionPlan]":
        """List plans in a workspace, most recent first."""
        from ag.core import ExecutionPlan

        ws = Workspace(workspace_id, self._root)
        if not ws.exists():
            return []

        plans: list[ExecutionPlan] = []
        plans_dir = ws.plans_path

        if not plans_dir.exists():
            return []

        now = datetime.now(timezone.utc)

        for plan_file in plans_dir.glob("*.json"):
            try:
                plan = ExecutionPlan.from_json(plan_file.read_text(encoding="utf-8"))

                # Filter expired plans unless requested
                if not include_expired and plan.expires_at < now:
                    continue

                plans.append(plan)
            except Exception:
                # Skip invalid plan files
                continue

        # Sort by created_at descending (most recent first)
        plans.sort(key=lambda p: p.created_at, reverse=True)
        return plans

    def delete(self, workspace_id: str, plan_id: str) -> bool:
        """Delete a plan."""
        ws = Workspace(workspace_id, self._root)
        if not ws.exists():
            return False

        plan_path = ws.plan_path(plan_id)
        if not plan_path.exists():
            return False

        plan_path.unlink()
        return True

    def update_status(
        self,
        workspace_id: str,
        plan_id: str,
        status: str,
        run_id: str | None = None,
    ) -> bool:
        """Update the status of a plan."""
        from ag.core import ExecutionPlan, PlanStatus

        plan = self.get(workspace_id, plan_id)
        if plan is None:
            return False

        # Create updated plan with new status
        plan_data = plan.model_dump()
        plan_data["status"] = status

        if run_id is not None:
            plan_data["run_id"] = run_id

        if status == PlanStatus.EXECUTED.value:
            plan_data["executed_at"] = datetime.now(timezone.utc).isoformat()

        updated_plan = ExecutionPlan.model_validate(plan_data)
        self.save(updated_plan)
        return True

    def cleanup_expired(self, workspace_id: str) -> int:
        """Remove expired plans from a workspace.

        Returns:
            Number of plans deleted
        """
        from ag.core import PlanStatus

        ws = Workspace(workspace_id, self._root)
        if not ws.exists():
            return 0

        plans_dir = ws.plans_path
        if not plans_dir.exists():
            return 0

        now = datetime.now(timezone.utc)
        deleted_count = 0

        for plan_file in plans_dir.glob("*.json"):
            try:
                from ag.core import ExecutionPlan

                plan = ExecutionPlan.from_json(plan_file.read_text(encoding="utf-8"))

                # Delete if expired and still pending
                if plan.status == PlanStatus.PENDING and plan.expires_at < now:
                    plan_file.unlink()
                    deleted_count += 1
            except Exception:
                # Skip invalid files
                continue

        return deleted_count
