"""TaskSpec v0.1 schema — contract for incoming task requests.

Additive-only policy: no field removals/renames within v0.x.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ExecutionMode(str, Enum):
    """Execution mode for the task."""

    MANUAL = "manual"
    SUPERVISED = "supervised"
    AUTONOMOUS = "autonomous"


class Budgets(BaseModel):
    """Resource budgets for task execution."""

    max_steps: int | None = Field(default=None, ge=1, description="Maximum number of steps")
    max_tokens: int | None = Field(default=None, ge=1, description="Maximum token budget")
    max_duration_seconds: int | None = Field(
        default=None, ge=1, description="Maximum wall-clock duration"
    )

    model_config = {"extra": "forbid"}


class Constraints(BaseModel):
    """Execution constraints for the task."""

    allowed_skills: list[str] | None = Field(
        default=None, description="Whitelist of skill names"
    )
    blocked_skills: list[str] | None = Field(
        default=None, description="Blacklist of skill names"
    )
    allowed_paths: list[str] | None = Field(
        default=None, description="Filesystem path whitelist"
    )
    blocked_paths: list[str] | None = Field(
        default=None, description="Filesystem path blacklist"
    )

    model_config = {"extra": "forbid"}


class TaskSpec(BaseModel):
    """v0.1 TaskSpec — the contract for incoming task requests.

    Required fields define the minimal inputs the runtime needs.
    Optional fields provide hints and guardrails.
    """

    task_spec_version: str = Field(
        default="0.1",
        pattern=r"^\d+\.\d+$",
        description="Schema version (semver minor)",
    )
    prompt: str = Field(..., min_length=1, description="User's task description")
    workspace_id: str = Field(..., min_length=1, description="Workspace identifier")
    mode: ExecutionMode = Field(
        default=ExecutionMode.MANUAL, description="Execution mode"
    )
    playbook_preference: str | None = Field(
        default=None, description="Preferred playbook name (optional hint)"
    )
    budgets: Budgets = Field(default_factory=Budgets, description="Resource budgets")
    constraints: Constraints = Field(
        default_factory=Constraints, description="Execution constraints"
    )

    model_config = {"extra": "forbid"}

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return self.model_dump_json(indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> TaskSpec:
        """Deserialize from JSON string."""
        return cls.model_validate_json(json_str)


# ---------------------------------------------------------------------------
# Builder pattern for ergonomic construction
# ---------------------------------------------------------------------------


class TaskSpecBuilder:
    """Fluent builder for TaskSpec."""

    def __init__(self, prompt: str, workspace_id: str) -> None:
        self._data: dict[str, Any] = {
            "prompt": prompt,
            "workspace_id": workspace_id,
        }

    def mode(self, mode: ExecutionMode) -> TaskSpecBuilder:
        self._data["mode"] = mode
        return self

    def playbook_preference(self, name: str) -> TaskSpecBuilder:
        self._data["playbook_preference"] = name
        return self

    def budgets(
        self,
        max_steps: int | None = None,
        max_tokens: int | None = None,
        max_duration_seconds: int | None = None,
    ) -> TaskSpecBuilder:
        self._data["budgets"] = Budgets(
            max_steps=max_steps,
            max_tokens=max_tokens,
            max_duration_seconds=max_duration_seconds,
        )
        return self

    def constraints(
        self,
        allowed_skills: list[str] | None = None,
        blocked_skills: list[str] | None = None,
        allowed_paths: list[str] | None = None,
        blocked_paths: list[str] | None = None,
    ) -> TaskSpecBuilder:
        self._data["constraints"] = Constraints(
            allowed_skills=allowed_skills,
            blocked_skills=blocked_skills,
            allowed_paths=allowed_paths,
            blocked_paths=blocked_paths,
        )
        return self

    def build(self) -> TaskSpec:
        return TaskSpec(**self._data)
