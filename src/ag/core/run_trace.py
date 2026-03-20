"""RunTrace v0.1 schema — the evidence log for a single run.

Additive-only policy: no field removals/renames within v0.x.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any, Self
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator

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


# AF-0051: Typed artifact categories for deterministic handling
class ArtifactCategory(str, Enum):
    """Category of artifact for deterministic export handling.

    These categories map to specific export behaviors and MIME types.
    """

    # Core output types
    RESULT = "result"  # Primary run result (e.g., result.md)
    LOG = "log"  # Execution logs
    TRACE = "trace"  # RunTrace JSON
    CONFIG = "config"  # Configuration/settings

    # Content types
    DOCUMENT = "document"  # Markdown, text, etc.
    DATA = "data"  # JSON, YAML, structured data
    CODE = "code"  # Source code files
    IMAGE = "image"  # Images, charts, diagrams

    # Other
    BINARY = "binary"  # Generic binary content
    UNKNOWN = "unknown"  # Fallback for untyped artifacts


class StepType(str, Enum):
    """Type of step in the run trace."""

    SKILL_CALL = "skill_call"
    REASONING = "reasoning"
    VERIFICATION = "verification"
    USER_INPUT = "user_input"
    # AF-0019: Planning step that generates subtasks
    PLANNING = "planning"


class WorkspaceSource(str, Enum):
    """Source of workspace resolution (AF-0030)."""

    CLI = "cli"  # --workspace flag
    PERSISTED = "persisted"  # persisted default
    ENV = "env"  # AG_WORKSPACE env var
    BOOTSTRAP = "bootstrap"  # auto-created default


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
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    # AF-0051: Optional typed category for deterministic export handling
    category: ArtifactCategory | None = Field(
        default=None, description="Artifact category for export handling (AF-0051)"
    )

    model_config = {"extra": "forbid"}

    def get_category(self) -> ArtifactCategory:
        """Get artifact category, inferring from type/path if not set.

        Returns:
            ArtifactCategory for this artifact
        """
        if self.category is not None:
            return self.category
        return infer_artifact_category(self.artifact_type, self.path)


def infer_artifact_category(artifact_type: str, path: str) -> ArtifactCategory:
    """Infer artifact category from MIME type and path.

    Args:
        artifact_type: MIME type or category string
        path: File path or URI

    Returns:
        Inferred ArtifactCategory
    """
    # Check specific patterns first
    lower_type = artifact_type.lower()
    lower_path = path.lower()

    # Result files
    if "result" in lower_path or lower_type == "result":
        return ArtifactCategory.RESULT

    # Trace files
    if "trace" in lower_path or lower_type == "trace":
        return ArtifactCategory.TRACE

    # Log files
    if ".log" in lower_path or "log" in lower_type:
        return ArtifactCategory.LOG

    # Config files
    if any(ext in lower_path for ext in [".json", ".yaml", ".yml", ".toml", ".ini"]):
        if "config" in lower_path or "settings" in lower_path:
            return ArtifactCategory.CONFIG

    # Code files - check before MIME types to catch .py, .js etc
    code_extensions = [".py", ".js", ".ts", ".java", ".go", ".rs", ".cpp", ".c", ".h"]
    if any(lower_path.endswith(ext) for ext in code_extensions):
        return ArtifactCategory.CODE

    # MIME type based inference
    if lower_type.startswith("text/"):
        if "markdown" in lower_type or lower_path.endswith(".md"):
            return ArtifactCategory.DOCUMENT
        return ArtifactCategory.DOCUMENT

    if lower_type.startswith("application/json") or lower_type.startswith("application/yaml"):
        return ArtifactCategory.DATA

    if lower_type.startswith("image/"):
        return ArtifactCategory.IMAGE

    if lower_type.startswith("application/octet-stream"):
        return ArtifactCategory.BINARY

    return ArtifactCategory.UNKNOWN


class Subtask(BaseModel):
    """A subtask generated by the planner (additive for delegation flows)."""

    subtask_id: str = Field(..., min_length=1, description="Unique subtask identifier")
    description: str = Field(..., min_length=1, description="Subtask description")
    status: str = Field(
        default="pending", description="Subtask status: pending/running/completed/failed"
    )
    result_summary: str | None = Field(default=None, description="Result summary after execution")

    model_config = {"extra": "forbid"}


# AF-0049: Evidence reference for citation traceability
class EvidenceRef(BaseModel):
    """A reference to evidence used in a step (AF-0049).

    Enables citation traceability by linking step outputs to source materials.

    Ownership (AF0054):
        This is the canonical Core-layer evidence model for trace metadata.
        Skills may define lightweight citation models for their output
        artifacts, but should convert to EvidenceRef when recording to
        the trace via to_evidence_ref().

    Source types:
        - file: Local file path
        - url: Remote URL
        - artifact: Reference to another artifact
        - memory: In-memory/ephemeral source
    """

    ref_id: str = Field(..., min_length=1, description="Unique reference identifier")
    source_type: str = Field(..., description="Type of source: file, url, artifact, memory")
    source_path: str = Field(..., description="Path or URI to the source")
    excerpt: str | None = Field(default=None, description="Relevant excerpt from the source")
    line_start: int | None = Field(
        default=None, ge=1, description="Starting line number (1-indexed)"
    )
    line_end: int | None = Field(default=None, ge=1, description="Ending line number (1-indexed)")
    relevance: str | None = Field(
        default=None, description="Why this evidence is relevant to the step"
    )
    confidence: float | None = Field(
        default=None, ge=0.0, le=1.0, description="Confidence score (0-1)"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional reference metadata"
    )

    model_config = {"extra": "forbid"}


# AF-0100: Step confirmation for guided autonomy
class StepConfirmation(BaseModel):
    """Confirmation status for a step requiring user approval (AF-0100)."""

    required: bool = Field(default=False, description="Was confirmation required?")
    policy_flags: list[str] = Field(
        default_factory=list, description="Policy flags triggering confirmation"
    )
    decision: str | None = Field(
        default=None, description="Confirmation decision: approved, denied, skipped"
    )
    decided_at: datetime | None = Field(default=None, description="When decision was made")
    decided_by: str | None = Field(
        default=None,
        description="Who/what made decision: user_interactive, user_yes_flag, policy_allow, etc.",
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
    # AF-0019: Subtasks for delegation flows (additive field)
    subtasks: list[Subtask] | None = Field(
        default=None, description="Subtasks generated by this step (for plan steps)"
    )
    # AF-0049: Evidence references for citation traceability (additive field)
    evidence_refs: list[EvidenceRef] | None = Field(
        default=None, description="Evidence sources referenced by this step"
    )
    # AF-0062: Model used for this step (additive field)
    model_used: str | None = Field(
        default=None, description="LLM model used for this step (AF-0062)"
    )
    # AF-0100: Confirmation status for guided autonomy (additive field)
    confirmation: StepConfirmation | None = Field(
        default=None, description="Confirmation details if step required approval (AF-0100)"
    )
    # AF-0094: Full step I/O for trace enrichment (additive fields)
    input_data: dict[str, Any] | None = Field(
        default=None, description="Full input data passed to the skill (AF-0094)"
    )
    output_data: dict[str, Any] | None = Field(
        default=None, description="Full output data returned by the skill (AF-0094)"
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
    evidence: dict[str, Any] = Field(default_factory=dict, description="Verification evidence")

    model_config = {"extra": "forbid"}


# AF-0062: LLM execution details
class LLMExecution(BaseModel):
    """LLM execution details for a run (AF-0062).

    Captures which provider and model were used for the run,
    enabling truthful UX and model comparison.
    """

    provider: str = Field(
        ..., min_length=1, description="Provider name (openai, anthropic, manual)"
    )
    model: str | None = Field(default=None, description="Model identifier")
    call_count: int = Field(default=0, ge=0, description="Number of LLM calls made")
    total_tokens: int | None = Field(default=None, ge=0, description="Total tokens used")
    input_tokens: int | None = Field(default=None, ge=0, description="Input/prompt tokens")
    output_tokens: int | None = Field(default=None, ge=0, description="Output/completion tokens")

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
    workspace_source: WorkspaceSource | None = Field(
        default=None, description="How workspace was resolved (AF-0030)"
    )
    mode: ExecutionMode = Field(..., description="Execution mode used")
    # AF-0062: LLM execution details (additive field)
    llm: LLMExecution | None = Field(
        default=None, description="LLM execution details (null for manual mode)"
    )
    playbook: PlaybookMetadata = Field(..., description="Playbook used for this run")
    started_at: datetime = Field(..., description="Run start timestamp")
    ended_at: datetime | None = Field(default=None, description="Run end timestamp")
    duration_ms: int | None = Field(default=None, ge=0, description="Total duration in ms")
    steps: list[Step] = Field(default_factory=list, description="Execution steps")
    artifacts: list[Artifact] = Field(default_factory=list, description="Artifacts produced")
    verifier: Verifier = Field(..., description="Verification result")
    final: FinalStatus = Field(..., description="Final run outcome")
    error: str | None = Field(default=None, description="Error message if failed")
    # AF-0099: Plan execution linkage
    plan_id: str | None = Field(
        default=None, description="Plan ID if run executed from approved plan"
    )
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional run metadata")

    model_config = {"extra": "forbid"}

    @model_validator(mode="after")
    def validate_verifier_consistency(self) -> Self:
        """Enforce verifier/final status consistency (AF-0029)."""
        # If run completed successfully, verifier must not be pending
        if self.final == FinalStatus.SUCCESS and self.verifier.status == VerifierStatus.PENDING:
            raise ValueError("Verifier status cannot be PENDING when final status is SUCCESS")
        # If verifier ran (not pending), checked_at must be set
        if self.verifier.status != VerifierStatus.PENDING and self.verifier.checked_at is None:
            raise ValueError(
                f"Verifier checked_at must be set when status is {self.verifier.status.value}"
            )
        return self

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
        evidence_refs: list[EvidenceRef] | None = None,
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
            evidence_refs=evidence_refs,
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

    def complete(self, status: FinalStatus, error: str | None = None) -> RunTraceBuilder:
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
