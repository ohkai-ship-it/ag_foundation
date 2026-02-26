"""Playbook v0.1 schema — workflow definition for task execution.

Additive-only policy: no field removals/renames within v0.x.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from .task_spec import Budgets


class ReasoningMode(str, Enum):
    """Reasoning modes supported by a playbook."""

    DIRECT = "direct"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    TREE_OF_THOUGHT = "tree_of_thought"
    REFLECTION = "reflection"


class PlaybookStepType(str, Enum):
    """Type of step in a playbook definition."""

    SKILL = "skill"
    BRANCH = "branch"
    LOOP = "loop"
    GATE = "gate"


class PlaybookStep(BaseModel):
    """A single step in the playbook sequence."""

    step_id: str = Field(..., min_length=1, description="Unique step identifier")
    name: str = Field(..., min_length=1, description="Human-readable step name")
    step_type: PlaybookStepType = Field(default=PlaybookStepType.SKILL, description="Type of step")
    skill_name: str | None = Field(default=None, description="Skill to invoke (for skill steps)")
    description: str = Field(default="", description="Step description")
    required: bool = Field(default=True, description="Whether step is required")
    retry_count: int = Field(default=0, ge=0, description="Max retry attempts")
    timeout_seconds: int | None = Field(default=None, ge=1, description="Step timeout")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Step parameters")
    on_failure: str | None = Field(default=None, description="Step ID to jump to on failure")

    model_config = {"extra": "forbid"}


class Playbook(BaseModel):
    """v0.1 Playbook — a workflow definition for task execution.

    Defines a linear sequence of steps with optional reasoning modes
    and budgets. The runtime uses playbooks to guide execution.
    """

    playbook_version: str = Field(
        default="0.1",
        pattern=r"^\d+\.\d+$",
        description="Schema version (semver minor)",
    )
    name: str = Field(..., min_length=1, description="Playbook name")
    version: str = Field(..., min_length=1, description="Playbook version")
    description: str = Field(default="", description="Playbook description")
    reasoning_modes: list[ReasoningMode] = Field(
        default_factory=lambda: [ReasoningMode.DIRECT],
        min_length=1,
        description="Supported reasoning modes",
    )
    budgets: Budgets = Field(default_factory=Budgets, description="Default resource budgets")
    steps: list[PlaybookStep] = Field(default_factory=list, description="Linear sequence of steps")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional playbook metadata"
    )

    model_config = {"extra": "forbid"}

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return self.model_dump_json(indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> Playbook:
        """Deserialize from JSON string."""
        return cls.model_validate_json(json_str)


# ---------------------------------------------------------------------------
# Builder pattern for ergonomic construction
# ---------------------------------------------------------------------------


class PlaybookBuilder:
    """Fluent builder for Playbook."""

    def __init__(self, name: str, version: str) -> None:
        self._data: dict[str, Any] = {
            "name": name,
            "version": version,
            "steps": [],
        }
        self._step_counter = 0

    def description(self, desc: str) -> PlaybookBuilder:
        self._data["description"] = desc
        return self

    def reasoning_modes(self, modes: list[ReasoningMode]) -> PlaybookBuilder:
        self._data["reasoning_modes"] = modes
        return self

    def budgets(
        self,
        max_steps: int | None = None,
        max_tokens: int | None = None,
        max_duration_seconds: int | None = None,
    ) -> PlaybookBuilder:
        self._data["budgets"] = Budgets(
            max_steps=max_steps,
            max_tokens=max_tokens,
            max_duration_seconds=max_duration_seconds,
        )
        return self

    def add_step(
        self,
        name: str,
        step_type: PlaybookStepType = PlaybookStepType.SKILL,
        skill_name: str | None = None,
        description: str = "",
        required: bool = True,
        retry_count: int = 0,
        timeout_seconds: int | None = None,
        parameters: dict[str, Any] | None = None,
        on_failure: str | None = None,
    ) -> PlaybookBuilder:
        step = PlaybookStep(
            step_id=f"step_{self._step_counter}",
            name=name,
            step_type=step_type,
            skill_name=skill_name,
            description=description,
            required=required,
            retry_count=retry_count,
            timeout_seconds=timeout_seconds,
            parameters=parameters or {},
            on_failure=on_failure,
        )
        self._data["steps"].append(step)
        self._step_counter += 1
        return self

    def metadata(self, **kwargs: Any) -> PlaybookBuilder:
        self._data["metadata"] = kwargs
        return self

    def build(self) -> Playbook:
        return Playbook(**self._data)
