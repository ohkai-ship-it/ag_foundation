"""ExecutionPlan schema — proposed execution plan for guided autonomy.

An ExecutionPlan wraps a Playbook with metadata for preview/approval workflow:
- Unique plan ID for reference
- Expiration time for auto-cleanup
- Status tracking (pending, approved, expired, executed, deleted)
- Policy flags for each step

Additive-only policy: no field removals/renames within v0.x.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from .playbook import Playbook

# Default time-to-live for plans (1 hour)
DEFAULT_PLAN_TTL_SECONDS = 3600


class PlanStatus(str, Enum):
    """Status of an execution plan."""

    PENDING = "pending"  # Awaiting approval
    APPROVED = "approved"  # Approved, ready to execute
    EXPIRED = "expired"  # TTL exceeded, no longer valid
    EXECUTED = "executed"  # Execution completed
    DELETED = "deleted"  # Manually deleted by user


class PolicyFlag(str, Enum):
    """Policy flags indicating what a step does."""

    EXTERNAL_API = "external_api"  # Makes external API calls
    FILE_WRITE = "file_write"  # Writes to filesystem
    FILE_READ = "file_read"  # Reads from filesystem
    LLM_CALL = "llm_call"  # Invokes an LLM
    NETWORK = "network"  # General network access
    SENSITIVE = "sensitive"  # Accesses sensitive data


class PlannedStep(BaseModel):
    """A step in the execution plan with policy annotations."""

    step_number: int = Field(..., ge=1, description="1-based step number")
    skill_name: str = Field(..., description="Name of the skill to execute")
    description: str = Field(default="", description="Step description/rationale")
    estimated_tokens: int = Field(default=0, ge=0, description="Estimated token usage")
    policy_flags: list[PolicyFlag] = Field(
        default_factory=list, description="Policy flags for this step"
    )
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Planned parameters"
    )

    model_config = {"extra": "forbid"}


class ExecutionPlan(BaseModel):
    """v0.1 ExecutionPlan — a proposed execution plan for guided autonomy.

    Wraps a Playbook with metadata for the preview/approval workflow.
    Plans have a TTL and can be approved, expired, or executed.
    """

    plan_version: str = Field(
        default="0.1",
        pattern=r"^\d+\.\d+$",
        description="Schema version (semver minor)",
    )
    plan_id: str = Field(..., min_length=1, description="Unique plan identifier")
    workspace_id: str = Field(..., min_length=1, description="Target workspace")
    task_prompt: str = Field(..., min_length=1, description="Original task prompt")
    status: PlanStatus = Field(default=PlanStatus.PENDING, description="Plan status")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Creation timestamp",
    )
    expires_at: datetime = Field(..., description="Expiration timestamp")
    executed_at: datetime | None = Field(
        default=None, description="Execution timestamp (if executed)"
    )
    run_id: str | None = Field(
        default=None, description="Associated run ID (if executed)"
    )

    # Plan content
    planned_steps: list[PlannedStep] = Field(
        default_factory=list, description="Steps with policy annotations"
    )
    total_estimated_tokens: int = Field(
        default=0, ge=0, description="Total estimated token usage"
    )
    confidence: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Planner confidence score"
    )
    warnings: list[str] = Field(
        default_factory=list, description="Planner warnings"
    )

    # The underlying playbook
    playbook: Playbook = Field(..., description="Generated playbook for execution")

    # Metadata
    planner_version: str = Field(default="v1", description="Planner version used")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional plan metadata"
    )

    model_config = {"extra": "forbid"}

    def is_expired(self) -> bool:
        """Check if the plan has expired."""
        return datetime.now(timezone.utc) > self.expires_at

    def is_actionable(self) -> bool:
        """Check if the plan can be approved or executed."""
        return self.status == PlanStatus.PENDING and not self.is_expired()

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return self.model_dump_json(indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> ExecutionPlan:
        """Deserialize from JSON string."""
        return cls.model_validate_json(json_str)


# ---------------------------------------------------------------------------
# Builder for creating ExecutionPlan from Playbook
# ---------------------------------------------------------------------------


def create_execution_plan(
    plan_id: str,
    workspace_id: str,
    task_prompt: str,
    playbook: Playbook,
    confidence: float = 0.0,
    warnings: list[str] | None = None,
    ttl_seconds: int = DEFAULT_PLAN_TTL_SECONDS,
    skill_policy_flags: dict[str, list[PolicyFlag]] | None = None,
) -> ExecutionPlan:
    """Create an ExecutionPlan from a Playbook.

    Args:
        plan_id: Unique plan identifier
        workspace_id: Target workspace
        task_prompt: Original task prompt
        playbook: Generated playbook
        confidence: Planner confidence score (0.0-1.0)
        warnings: Planner warnings
        ttl_seconds: Time-to-live in seconds
        skill_policy_flags: Map of skill_name -> policy flags

    Returns:
        ExecutionPlan ready for storage
    """
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(seconds=ttl_seconds)
    skill_flags = skill_policy_flags or {}

    # Convert playbook steps to planned steps with policy annotations
    planned_steps: list[PlannedStep] = []
    total_tokens = 0

    for i, step in enumerate(playbook.steps, start=1):
        # Get policy flags for this skill
        flags = skill_flags.get(step.skill_name or "", [])

        # Estimate tokens from step parameters or use default
        est_tokens = step.parameters.get("estimated_tokens", 500)
        total_tokens += est_tokens

        planned_steps.append(
            PlannedStep(
                step_number=i,
                skill_name=step.skill_name or step.name,
                description=step.description,
                estimated_tokens=est_tokens,
                policy_flags=flags,
                parameters=step.parameters,
            )
        )

    # Use playbook budgets if available
    if playbook.budgets.max_tokens:
        total_tokens = playbook.budgets.max_tokens

    return ExecutionPlan(
        plan_id=plan_id,
        workspace_id=workspace_id,
        task_prompt=task_prompt,
        created_at=now,
        expires_at=expires_at,
        planned_steps=planned_steps,
        total_estimated_tokens=total_tokens,
        confidence=confidence,
        warnings=warnings or [],
        playbook=playbook,
    )
