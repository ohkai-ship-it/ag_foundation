"""RunTrace v0.1 schema — the evidence log for a single run.

Additive-only policy: no field removals/renames within v0.x.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from .task_spec import ExecutionMode


class VerifierStatus(str, Enum):
    """Status from the verifier module."""

    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class FinalStatus(str, Enum):
    """Final outcome of the run."""

    SUCCESS = "success"
    FAILURE = "failure"
    ABORTED = "aborted"
    TIMEOUT = "timeout"


class StepType(str, Enum):
    """Type of step in the run trace."""

    SKILL_CALL = "skill_call"
    REASONING = "reasoning"
    VERIFICATION = "verification"
    USER_INPUT = "user_input"


class Artifact(BaseModel):
    """An artifact produced during the run."""

    artifact_id: str = Field(..., min_length=1, description="Unique artifact identifier")
    path: str = Field(..., min_length=1, description="Storage path or URI")
    artifact_type: str = Field(..., min_length=1, description="MIME type or category")
    size_bytes: int | None = Field(default=None, ge=0, description="Size in bytes")
    checksum: str | None = Field(default=None, description="SHA256 checksum")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Creation timestamp"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    model_config = {"extra": "forbid"}


class Step(BaseModel):
    """A single step in the run trace."""

    step_id: str = Field(..., min_length=1, description="Unique step identifier")
    step_number: int = Field(..., ge=0, description="Sequential step number")
    step_type: StepType = Field(..., description="Type of step")
    skill_name: str | None = Field(default=None, description="Skill name if skill_call")
    input_summary: str = Field(default="", description="Summary of step input")
    output_summary: str = Field(default="", description="Summary of step output")
    started_at: datetime = Field(..., description="Step start timestamp")
    ended_at: datetime | None = Field(default=None, description="Step end timestamp")
    duration_ms: int | None = Field(default=None, ge=0, description="Duration in milliseconds")
    tokens_used: int | None = Field(default=None, ge=0, description="Tokens consumed")
    error: str | None = Field(default=None, description="Error message if failed")
    artifacts: list[str] = Field(
        default_factory=list, description="Artifact IDs produced by this step"
    )

    model_config = {"extra": "forbid"}


class PlaybookMetadata(BaseModel):
    """Metadata about the playbook used for this run."""

    name: str = Field(..., min_length=1, description="Playbook name")
    version: str = Field(..., min_length=1, description="Playbook version")

    model_config = {"extra": "forbid"}


class Verifier(BaseModel):
    """Verifier result for the run."""

    status: VerifierStatus = Field(..., description="Verification status")
    checked_at: datetime | None = Field(default=None, description="Verification timestamp")
    message: str | None = Field(default=None, description="Verifier message")
    evidence: dict[str, Any] = Field(
        default_factory=dict, description="Verification evidence"
    )

    model_config = {"extra": "forbid"}


class RunTrace(BaseModel):
    """v0.1 RunTrace — the evidence log for a single run.

    Captures the full execution history including steps, artifacts,
    verification status, and timing information.
    """

    trace_version: str = Field(
        default="0.1",
        pattern=r"^\d+\.\d+$",
        description="Schema version (semver minor)",
    )
    run_id: str = Field(
        default_factory=lambda: str(uuid4()),
        min_length=1,
        description="Unique run identifier",
    )
    workspace_id: str = Field(..., min_length=1, description="Workspace identifier")
    mode: ExecutionMode = Field(..., description="Execution mode used")
    playbook: PlaybookMetadata = Field(..., description="Playbook used for this run")
    started_at: datetime = Field(..., description="Run start timestamp")
    ended_at: datetime | None = Field(default=None, description="Run end timestamp")
    duration_ms: int | None = Field(default=None, ge=0, description="Total duration in ms")
    steps: list[Step] = Field(default_factory=list, description="Execution steps")
    artifacts: list[Artifact] = Field(
        default_factory=list, description="Artifacts produced"
    )
    verifier: Verifier = Field(..., description="Verification result")
    final: FinalStatus = Field(..., description="Final run outcome")
    error: str | None = Field(default=None, description="Error message if failed")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional run metadata"
    )

    model_config = {"extra": "forbid"}

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return self.model_dump_json(indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> RunTrace:
        """Deserialize from JSON string."""
        return cls.model_validate_json(json_str)


# ---------------------------------------------------------------------------
# Builder pattern for ergonomic construction
# ---------------------------------------------------------------------------


class RunTraceBuilder:
    """Fluent builder for RunTrace."""

    def __init__(
        self,
        workspace_id: str,
        mode: ExecutionMode,
        playbook_name: str,
        playbook_version: str,
    ) -> None:
        self._data: dict[str, Any] = {
            "workspace_id": workspace_id,
            "mode": mode,
            "playbook": PlaybookMetadata(name=playbook_name, version=playbook_version),
            "started_at": datetime.now(UTC),
            "steps": [],
            "artifacts": [],
            "verifier": Verifier(status=VerifierStatus.PENDING),
            "final": FinalStatus.ABORTED,  # default until completed
        }
        self._step_counter = 0

    def add_step(
        self,
        step_type: StepType,
        skill_name: str | None = None,
        input_summary: str = "",
        output_summary: str = "",
        duration_ms: int | None = None,
        tokens_used: int | None = None,
        error: str | None = None,
        artifacts: list[str] | None = None,
    ) -> RunTraceBuilder:
        now = datetime.now(UTC)
        step = Step(
            step_id=str(uuid4()),
            step_number=self._step_counter,
            step_type=step_type,
            skill_name=skill_name,
            input_summary=input_summary,
            output_summary=output_summary,
            started_at=now,
            ended_at=now,
            duration_ms=duration_ms,
            tokens_used=tokens_used,
            error=error,
            artifacts=artifacts or [],
        )
        self._data["steps"].append(step)
        self._step_counter += 1
        return self

    def add_artifact(
        self,
        path: str,
        artifact_type: str,
        size_bytes: int | None = None,
        checksum: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> RunTraceBuilder:
        artifact = Artifact(
            artifact_id=str(uuid4()),
            path=path,
            artifact_type=artifact_type,
            size_bytes=size_bytes,
            checksum=checksum,
            metadata=metadata or {},
        )
        self._data["artifacts"].append(artifact)
        return self

    def verify(
        self,
        status: VerifierStatus,
        message: str | None = None,
        evidence: dict[str, Any] | None = None,
    ) -> RunTraceBuilder:
        self._data["verifier"] = Verifier(
            status=status,
            checked_at=datetime.now(UTC),
            message=message,
            evidence=evidence or {},
        )
        return self

    def complete(
        self, status: FinalStatus, error: str | None = None
    ) -> RunTraceBuilder:
        now = datetime.now(UTC)
        self._data["final"] = status
        self._data["error"] = error
        self._data["ended_at"] = now
        if "started_at" in self._data:
            delta = now - self._data["started_at"]
            self._data["duration_ms"] = int(delta.total_seconds() * 1000)
        return self

    def build(self) -> RunTrace:
        return RunTrace(**self._data)
