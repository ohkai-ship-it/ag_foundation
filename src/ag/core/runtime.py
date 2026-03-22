"""Runtime composition root (AF-0114).

Wires pipeline components together. Implementations live in dedicated files:
- executor.py (V0Executor)
- verifier.py (V0Verifier)
- recorder.py (V0Recorder)
- orchestrator.py (V0Orchestrator, TrackingLLMProvider, _adapt_document_to_source)
- planner.py (V0Planner, V1Planner)
"""

from __future__ import annotations

from ag.core.executor import V0Executor
from ag.core.orchestrator import (
    TrackingLLMProvider,
    V0Orchestrator,
    V1Orchestrator,
    _adapt_document_to_source,
)
from ag.core.planner import PlanningResult, V0Planner
from ag.core.playbook import Playbook
from ag.core.recorder import V0Recorder
from ag.core.run_trace import PipelineManifest, PlanningLLMCall, PlanningMetadata, RunTrace
from ag.core.task_spec import Budgets, Constraints, ExecutionMode, TaskSpec
from ag.core.verifier import V0Verifier, V1Verifier
from ag.skills import SkillRegistry
from ag.storage import SQLiteArtifactStore, SQLiteRunStore


class RuntimeError(Exception):
    """Runtime execution error."""

    pass


# ---------------------------------------------------------------------------
# v0 Normalizer Implementation
# ---------------------------------------------------------------------------


class V0Normalizer:
    """v0 Normalizer: validates input and creates TaskSpec."""

    def normalize(
        self,
        prompt: str,
        workspace: str | None = None,
        mode: str = "llm",
        playbook: str | None = None,
        **options: object,
    ) -> TaskSpec:
        """Normalize user input into a TaskSpec."""
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        # AF-0026: Workspace is required - no implicit creation
        if not workspace:
            raise ValueError("Workspace is required. Implicit workspace creation is not allowed.")
        workspace_id = workspace

        # Parse mode
        mode_enum = ExecutionMode.MANUAL if mode == "manual" else ExecutionMode.SUPERVISED

        return TaskSpec(
            prompt=prompt.strip(),
            workspace_id=workspace_id,
            mode=mode_enum,
            playbook_preference=playbook,
            budgets=Budgets(),
            constraints=Constraints(),
        )


# ---------------------------------------------------------------------------
# Runtime Facade
# ---------------------------------------------------------------------------


class Runtime:
    """High-level runtime facade."""

    def __init__(
        self,
        normalizer: V0Normalizer | None = None,
        planner: V0Planner | None = None,
        orchestrator: V0Orchestrator | None = None,
    ) -> None:
        self._normalizer = normalizer or V0Normalizer()
        self._planner = planner or V0Planner()
        self._orchestrator = orchestrator or V0Orchestrator()

    def execute(
        self,
        prompt: str,
        workspace: str | None = None,
        mode: str = "llm",
        playbook: str | None = None,
        workspace_source: str | None = None,
        playbook_object: Playbook | None = None,
    ) -> RunTrace:
        """Execute a task and return the trace.

        Args:
            prompt: User's task description
            workspace: Workspace ID (auto-generated if not provided)
            mode: Execution mode ('manual' or 'llm')
            playbook: Playbook name preference (used if playbook_object not provided)
            workspace_source: How the workspace was resolved (AF-0030)
            playbook_object: Pre-built Playbook to execute directly (for plan execution)

        Returns:
            RunTrace capturing the execution
        """
        # Normalize
        task = self._normalizer.normalize(
            prompt=prompt,
            workspace=workspace,
            mode=mode,
            playbook=playbook,
        )

        # Plan - skip if playbook_object provided (e.g., from ExecutionPlan)
        planning_metadata: PlanningMetadata | None = None
        if playbook_object is not None:
            selected_playbook = playbook_object
        elif hasattr(self._planner, "plan_with_metadata"):
            # AF-0119: Use plan_with_metadata() to capture planning trace
            result: PlanningResult = self._planner.plan_with_metadata(task)
            selected_playbook = result.playbook
            # Build PlanningMetadata from PlanningResult
            llm_call: PlanningLLMCall | None = None
            if result.model_used or result.total_tokens:
                llm_call = PlanningLLMCall(
                    model=result.model_used,
                    input_tokens=result.input_tokens,
                    output_tokens=result.output_tokens,
                    total_tokens=result.total_tokens,
                )
            planning_metadata = PlanningMetadata(
                planner=result.planner_name,
                started_at=result.started_at,
                ended_at=result.ended_at,
                duration_ms=result.duration_ms,
                llm_call=llm_call,
                raw_plan_steps=result.raw_steps,
                validation_corrections=result.validation_corrections,
                confidence=result.confidence,
            )
        else:
            selected_playbook = self._planner.plan(task)

        # AF-0120: Build pipeline manifest from component class names
        pipeline_manifest = PipelineManifest(
            planner=self._planner.__class__.__name__,
            orchestrator=self._orchestrator.__class__.__name__,
            executor=getattr(self._orchestrator, "_executor", None).__class__.__name__
            if hasattr(self._orchestrator, "_executor") and self._orchestrator._executor is not None
            else None,
            verifier=getattr(self._orchestrator, "_verifier", None).__class__.__name__
            if hasattr(self._orchestrator, "_verifier") and self._orchestrator._verifier is not None
            else None,
            recorder=getattr(self._orchestrator, "_recorder", None).__class__.__name__
            if hasattr(self._orchestrator, "_recorder") and self._orchestrator._recorder is not None
            else None,
        )

        # Execute (pass planning metadata and pipeline manifest if orchestrator is V1)
        if isinstance(self._orchestrator, V1Orchestrator):
            # V1Orchestrator with planning support (AF-0119) and pipeline manifest (AF-0120)
            trace = self._orchestrator.run(
                task,
                selected_playbook,
                workspace_source=workspace_source,
                planning=planning_metadata,
                pipeline=pipeline_manifest,
            )
        else:
            trace = self._orchestrator.run(
                task, selected_playbook, workspace_source=workspace_source
            )

        return trace

    def close(self) -> None:
        """Close underlying storage connections."""
        self._orchestrator.close()

    def __enter__(self) -> "Runtime":
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Context manager exit - ensures storage is closed."""
        self.close()


def create_runtime(
    registry: SkillRegistry | None = None,
    run_store: SQLiteRunStore | None = None,
    artifact_store: SQLiteArtifactStore | None = None,
) -> Runtime:
    """Create a configured runtime instance.

    Args:
        registry: Skill registry (uses default if not provided)
        run_store: Run storage (uses default if not provided)
        artifact_store: Artifact storage (uses default if not provided)

    Returns:
        Configured Runtime instance
    """
    executor = V0Executor(registry)
    recorder = V0Recorder(run_store, artifact_store)
    verifier = V1Verifier()
    orchestrator = V1Orchestrator(executor, verifier, recorder)

    return Runtime(
        normalizer=V0Normalizer(),
        planner=V0Planner(),
        orchestrator=orchestrator,
    )


# Backward-compatible re-exports (AF-0114)
__all__ = [
    "Runtime",
    "RuntimeError",
    "V0Normalizer",
    "V0Planner",
    "V0Executor",
    "V0Verifier",
    "V1Verifier",
    "V0Recorder",
    "V0Orchestrator",
    "V1Orchestrator",
    "TrackingLLMProvider",
    "_adapt_document_to_source",
    "create_runtime",
]
