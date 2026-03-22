"""Core runtime modules and interfaces."""

from ag.playbooks import (
    DEFAULT_V0,
    DELEGATE_V0,
    SUMMARIZE_V0,
    get_playbook,
    list_playbooks,
)

from .execution_plan import (
    DEFAULT_PLAN_TTL_SECONDS,
    ExecutionPlan,
    PlannedStep,
    PlanStatus,
    PolicyFlag,
    create_execution_plan,
)
from .executor import V0Executor
from .interfaces import (
    Executor,
    Normalizer,
    Orchestrator,
    Planner,
    Recorder,
)
from .interfaces import (
    Verifier as VerifierProtocol,
)
from .orchestrator import (
    TrackingLLMProvider,
    V0Orchestrator,
    V1Orchestrator,
    _adapt_document_to_source,
)
from .planner import (
    PlannerError,
    V0Planner,
    V1Planner,
    V2Planner,
    V3Planner,
)
from .playbook import (
    Playbook,
    PlaybookBuilder,
    PlaybookStep,
    PlaybookStepType,
    ReasoningMode,
)
from .recorder import V0Recorder
from .run_trace import (
    Artifact,
    ArtifactCategory,
    AutonomyMetadata,
    AutonomyMode,
    CapabilityGap,
    EvidenceRef,
    FeasibilityAssessment,
    FeasibilityLevel,
    FinalStatus,
    LLMExecution,
    PlaybookMetadata,
    RunTrace,
    RunTraceBuilder,
    SemanticVerification,
    Step,
    StepConfirmation,
    StepType,
    Verifier,
    VerifierStatus,
    WorkspaceSource,
    infer_artifact_category,
)
from .runtime import (
    Runtime,
    V0Normalizer,
    create_runtime,
)
from .schema_verifier import (
    DEFAULT_MAX_VALIDATION_ATTEMPTS,
    MAX_VALIDATION_ATTEMPTS_CEILING,
    SchemaValidator,
    ValidationAttempt,
    ValidationResult,
    create_verification_step,
    record_validation_steps,
    run_validation_loop,
)
from .task_spec import (
    Budgets,
    Constraints,
    ExecutionMode,
    TaskSpec,
    TaskSpecBuilder,
)
from .verifier import V0Verifier, V1Verifier, V2Verifier

__all__ = [
    # task_spec
    "TaskSpec",
    "TaskSpecBuilder",
    "ExecutionMode",
    "Budgets",
    "Constraints",
    # run_trace
    "RunTrace",
    "RunTraceBuilder",
    "Artifact",
    "ArtifactCategory",
    "AutonomyMetadata",
    "AutonomyMode",
    "EvidenceRef",
    "LLMExecution",
    "Step",
    "StepConfirmation",
    "StepType",
    "PlaybookMetadata",
    "Verifier",
    "VerifierStatus",
    "FinalStatus",
    "WorkspaceSource",
    "infer_artifact_category",
    # run_trace feasibility (AF-0121)
    "FeasibilityLevel",
    "FeasibilityAssessment",
    "CapabilityGap",
    # run_trace semantic verification (AF-0123)
    "SemanticVerification",
    # playbook
    "Playbook",
    "PlaybookBuilder",
    "PlaybookStep",
    "PlaybookStepType",
    "ReasoningMode",
    # playbooks
    "DEFAULT_V0",
    "DELEGATE_V0",
    "SUMMARIZE_V0",
    "get_playbook",
    "list_playbooks",
    # interfaces
    "Normalizer",
    "Planner",
    "Orchestrator",
    "Executor",
    "VerifierProtocol",
    "Recorder",
    # runtime
    "Runtime",
    "V0Normalizer",
    "V0Planner",
    "V0Orchestrator",
    "V1Orchestrator",
    "V0Executor",
    "V0Verifier",
    "V1Verifier",
    "V2Verifier",
    "V0Recorder",
    "TrackingLLMProvider",
    "_adapt_document_to_source",
    "create_runtime",
    # planner (AF-0102, AF-0121)
    "V1Planner",
    "V2Planner",
    "V3Planner",
    "PlannerError",
    # execution_plan (AF-0098)
    "ExecutionPlan",
    "PlannedStep",
    "PlanStatus",
    "PolicyFlag",
    "create_execution_plan",
    "DEFAULT_PLAN_TTL_SECONDS",
    # schema_verifier (AF-0050)
    "SchemaValidator",
    "ValidationAttempt",
    "ValidationResult",
    "create_verification_step",
    "record_validation_steps",
    "run_validation_loop",
    "DEFAULT_MAX_VALIDATION_ATTEMPTS",
    "MAX_VALIDATION_ATTEMPTS_CEILING",
]
