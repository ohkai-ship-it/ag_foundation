"""v0 Runtime implementation.

Implements the core runtime loop: Normalizer -> Planner -> Orchestrator -> Recorder
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from ag.core.playbook import Playbook
from ag.core.run_trace import (
    Artifact,
    FinalStatus,
    LLMExecution,
    PlaybookMetadata,
    RunTrace,
    Step,
    StepType,
    Subtask,
    VerifierStatus,
    WorkspaceSource,
)
from ag.core.run_trace import (
    Verifier as VerifierModel,
)
from ag.core.task_spec import Budgets, Constraints, ExecutionMode, TaskSpec
from ag.playbooks import DEFAULT_V0, get_playbook
from ag.providers.base import ChatMessage, ChatResponse, LLMProvider, ProviderConfig
from ag.providers.registry import get_provider
from ag.skills import SkillContext, SkillRegistry, get_default_registry
from ag.storage import SQLiteArtifactStore, SQLiteRunStore, Workspace


class RuntimeError(Exception):
    """Runtime execution error."""

    pass


# ---------------------------------------------------------------------------
# AF-0094: LLM Usage Tracking Wrapper
# ---------------------------------------------------------------------------


class TrackingLLMProvider:
    """Wrapper around LLMProvider that tracks token usage (AF-0094).

    This wraps an underlying provider and accumulates usage statistics
    from each chat() call for later inclusion in the RunTrace.
    """

    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider
        self.call_count: int = 0
        self.total_tokens: int = 0
        self.input_tokens: int = 0
        self.output_tokens: int = 0

    @property
    def name(self) -> str:
        """Delegate to underlying provider."""
        return self._provider.name

    @property
    def is_stub(self) -> bool:
        """Delegate to underlying provider."""
        return self._provider.is_stub

    def chat(
        self,
        messages: list[ChatMessage] | list[dict[str, str]],
        model: str | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        """Forward chat request and track usage."""
        response = self._provider.chat(messages, model, **kwargs)

        # Track usage from response
        self.call_count += 1
        if response.tokens_used is not None:
            self.total_tokens += response.tokens_used
        if response.input_tokens is not None:
            self.input_tokens += response.input_tokens
        if response.output_tokens is not None:
            self.output_tokens += response.output_tokens

        return response

    def get_usage(self) -> dict[str, int | None]:
        """Get accumulated usage statistics."""
        return {
            "call_count": self.call_count,
            "total_tokens": self.total_tokens if self.total_tokens > 0 else None,
            "input_tokens": self.input_tokens if self.input_tokens > 0 else None,
            "output_tokens": self.output_tokens if self.output_tokens > 0 else None,
        }


# ---------------------------------------------------------------------------
# AF-0108: Pipeline document conversion adapter
# ---------------------------------------------------------------------------


def _adapt_document_to_source(doc: dict[str, Any] | Any) -> dict[str, Any]:
    """Convert a Document dict to SourceDocument-compatible dict.

    Bridges load_documents output (Document schema) to synthesize_research
    input (SourceDocument schema) during pipeline chaining.
    """
    if isinstance(doc, dict) and "path" in doc and "source" not in doc:
        return {
            "source": doc["path"],
            "content": doc.get("content", ""),
            "title": None,
            "source_type": "file",
        }
    return doc


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
# v0 Planner Implementation
# ---------------------------------------------------------------------------


class V0Planner:
    """v0 Planner: selects playbook (always default_v0 for now)."""

    def plan(self, task: TaskSpec) -> Playbook:
        """Select playbook for task execution."""
        # v0: Honor preference if valid, otherwise use default
        if task.playbook_preference:
            playbook = get_playbook(task.playbook_preference)
            if playbook:
                return playbook

        return DEFAULT_V0


# ---------------------------------------------------------------------------
# v0 Executor Implementation
# ---------------------------------------------------------------------------


class V0Executor:
    """v0 Executor: executes skills from registry."""

    def __init__(self, registry: SkillRegistry | None = None) -> None:
        self._registry = registry or get_default_registry()

    def execute(
        self,
        skill_name: str,
        parameters: dict[str, Any],
        context: SkillContext | None = None,
    ) -> tuple[bool, str, dict[str, Any]]:
        """Execute a skill.

        Args:
            skill_name: Name of the skill to execute
            parameters: Skill parameters
            context: Optional SkillContext with workspace, provider, etc.

        Returns:
            Tuple of (success, output_summary, result_data)
        """
        if not self._registry.has(skill_name):
            raise KeyError(f"Skill not found: {skill_name}")

        return self._registry.execute(skill_name, parameters, context)


# ---------------------------------------------------------------------------
# v0 Verifier Implementation
# ---------------------------------------------------------------------------


class V0Verifier:
    """v0 Verifier: basic verification (checks for errors in trace)."""

    def verify(self, trace: RunTrace) -> tuple[str, str | None]:
        """Verify a run's results.

        v0 verification:
        - If any step has an error, return 'failed'
        - If final status is not success, return 'failed'
        - Otherwise return 'passed'
        """
        return self.verify_components(trace.steps, trace.final)

    def verify_components(
        self, steps: list[Step], final_status: FinalStatus
    ) -> tuple[str, str | None]:
        """Verify run components without requiring a full trace (AF-0029)."""
        # Check for step errors
        for step in steps:
            if step.error:
                return "failed", f"Step {step.step_number} failed: {step.error}"

        # Check final status
        if final_status != FinalStatus.SUCCESS:
            return "failed", f"Run ended with status: {final_status.value}"

        return "passed", "All steps completed successfully"


# ---------------------------------------------------------------------------
# v0 Recorder Implementation
# ---------------------------------------------------------------------------


class V0Recorder:
    """v0 Recorder: persists traces and artifacts to storage."""

    def __init__(
        self,
        run_store: SQLiteRunStore | None = None,
        artifact_store: SQLiteArtifactStore | None = None,
    ) -> None:
        self._run_store = run_store or SQLiteRunStore()
        self._artifact_store = artifact_store or SQLiteArtifactStore()

    def record(self, trace: RunTrace) -> None:
        """Persist a RunTrace."""
        self._run_store.save(trace)

    def register_artifact(
        self,
        trace: RunTrace,
        artifact_id: str,
        path: str,
        content: bytes,
        artifact_type: str = "application/octet-stream",
    ) -> str:
        """Register an artifact for a run."""
        artifact = Artifact(
            artifact_id=artifact_id,
            path=path,
            artifact_type=artifact_type,
            size_bytes=len(content),
        )
        return self._artifact_store.save(trace.workspace_id, trace.run_id, artifact, content)

    def close(self) -> None:
        """Close storage connections."""
        self._run_store.close()
        self._artifact_store.close()


# ---------------------------------------------------------------------------
# v0 Orchestrator Implementation
# ---------------------------------------------------------------------------


class V0Orchestrator:
    """v0 Orchestrator: linear step execution."""

    def __init__(
        self,
        executor: V0Executor | None = None,
        verifier: V0Verifier | None = None,
        recorder: V0Recorder | None = None,
    ) -> None:
        self._executor = executor or V0Executor()
        self._verifier = verifier or V0Verifier()
        self._recorder = recorder or V0Recorder()

    def run(
        self, task: TaskSpec, playbook: Playbook, workspace_source: str | None = None
    ) -> RunTrace:
        """Execute a playbook for the given task.

        v0 execution:
        - Linear step execution (no branching/loops)
        - Stop on first error for required steps
        - Skip optional steps on error
        - Verifier runs at end
        - AF-0019: Delegation support with subtask tracking
        """
        run_id = str(uuid4())
        started_at = datetime.now(UTC)
        steps: list[Step] = []
        artifacts: list[Artifact] = []
        final_status = FinalStatus.SUCCESS
        error_message: str | None = None

        # AF-0065: Resolve workspace path for skill context
        # Use task.workspace_id (the actual workspace ID) to get path
        workspace_path: Path | None = None
        if task.workspace_id:
            try:
                ws = Workspace(task.workspace_id)
                if ws.exists():
                    workspace_path = ws.path
            except Exception:
                pass  # Workspace resolution failed, skills will handle missing path

        # AF-0019: Track subtasks from planning step for delegation
        planned_subtasks: list[dict[str, Any]] = []

        # AF-0065: Track step results for pipeline chaining
        step_results: list[dict[str, Any]] = []
        # Accumulated results across all successful steps so that data
        # from earlier steps (e.g. synthesize_research output) remains
        # available even after intermediate steps (e.g. a first emit_result)
        # that produce unrelated output.  Later keys override earlier ones.
        accumulated_result: dict[str, Any] = {}

        # AF-0065: Create LLM provider for non-manual modes
        # AF-0062: Track provider configuration for LLMExecution in trace
        # AF-0094: Wrap provider with tracking for token usage
        llm_provider: LLMProvider | None = None
        tracking_provider: TrackingLLMProvider | None = None
        provider_config: ProviderConfig | None = None
        if task.mode != ExecutionMode.MANUAL:
            try:
                # Create OpenAI provider (default for v0)
                provider_config = ProviderConfig(
                    provider="openai",
                    model="gpt-4o-mini",  # Default model
                )
                raw_provider = get_provider(provider_config)
                # AF-0094: Wrap with tracking
                tracking_provider = TrackingLLMProvider(raw_provider)
                llm_provider = tracking_provider  # Use tracker as the provider
            except Exception:
                # Provider creation failed - will use fallback mode in skills
                pass  # Skills handle missing provider gracefully

        # AF-0094: Track pending artifacts to register after trace is built
        # Each entry is (artifact_id, path, content_bytes, artifact_type)
        pending_artifacts: list[tuple[str, str, bytes, str]] = []

        # Execute each step in sequence
        for i, playbook_step in enumerate(playbook.steps):
            step_started = datetime.now(UTC)
            step_error: str | None = None
            output_summary = ""
            skill_name = playbook_step.skill_name
            step_subtasks: list[Subtask] | None = None
            result: dict[str, Any] = {}
            step_artifact_ids: list[str] = []  # AF-0057: Track artifacts per step

            try:
                if skill_name:
                    # Build skill parameters: merge step params with task context
                    # AF-0065: Include previous step result for pipeline chaining
                    # Use accumulated_result so data from earlier steps (e.g.
                    # synthesize_research) survives through intermediate steps
                    # like a first emit_result when multiple emits are planned.
                    chained_result = accumulated_result.copy()
                    # AF-0108: Convert Document dicts to SourceDocument format
                    # when chaining load_documents output to synthesize_research
                    if skill_name == "synthesize_research" and "documents" in chained_result:
                        chained_result = {
                            **chained_result,
                            "documents": [
                                _adapt_document_to_source(doc)
                                for doc in chained_result["documents"]
                            ],
                        }
                    # Strip "previous_step.*" placeholder strings from plan
                    # parameters — these are LLM-generated references that the
                    # runtime never resolves; actual values come from chained_result.
                    step_params = {
                        k: v
                        for k, v in playbook_step.parameters.items()
                        if not (isinstance(v, str) and v.startswith("previous_step."))
                    }
                    skill_params = {
                        "prompt": task.prompt,
                        "step": i,
                        **step_params,
                        **chained_result,  # Chain previous step output
                    }
                    # AF-0019: Pass subtasks context to execute_subtask skills
                    if skill_name == "execute_subtask" and planned_subtasks:
                        skill_params["subtasks"] = planned_subtasks

                    # AF-0065: Build SkillContext with workspace, provider, and run info
                    # AF-0082: Include trace metadata for emit_result to build polished reports
                    trace_metadata: dict[str, Any] = {
                        "elapsed_ms": int((datetime.now(UTC) - started_at).total_seconds() * 1000),
                        "playbook_name": playbook.name,
                        "playbook_version": playbook.version,
                        "steps_summary": [
                            {
                                "skill": s.skill_name or "no-skill",
                                "duration_ms": s.duration_ms,
                                "output_summary": (
                                    s.output_summary[:100] if s.output_summary else ""
                                ),
                            }
                            for s in steps
                        ],
                    }
                    # Add model info if available
                    if provider_config:
                        trace_metadata["model"] = provider_config.model

                    skill_context = SkillContext(
                        provider=llm_provider,
                        workspace_path=workspace_path,
                        step_number=i,
                        run_id=run_id,
                        trace_metadata=trace_metadata,
                    )

                    # Execute the skill with context
                    success, output_summary, result = self._executor.execute(
                        skill_name, skill_params, skill_context
                    )
                    if not success:
                        step_error = output_summary
                    else:
                        # AF-0065: Store result for next step
                        step_results.append(result)
                        # Accumulate: merge into running dict so earlier data
                        # (report, key_findings, …) persists across steps.
                        accumulated_result.update(result)

                        # AF-0057: Capture skill-produced artifacts in trace
                        if "artifact_id" in result:
                            artifact_id = result["artifact_id"]
                            step_artifact_ids.append(artifact_id)
                            # Create Artifact for run-level tracking
                            artifact = Artifact(
                                artifact_id=artifact_id,
                                path=result.get("artifact_path", f"{skill_name}_output"),
                                artifact_type=result.get("artifact_type", "application/json"),
                                size_bytes=result.get("bytes_written"),
                            )
                            artifacts.append(artifact)

                        # AF-0094: Save step output as artifact for full trace enrichment
                        if result:
                            step_output_artifact_id = f"{run_id}-step-{i}-{skill_name}_output"
                            step_output_path = f"{i}_{skill_name}_output.json"
                            step_output_content = json.dumps(result, indent=2).encode("utf-8")
                            step_artifact_ids.append(step_output_artifact_id)
                            # Create Artifact metadata
                            step_output_artifact = Artifact(
                                artifact_id=step_output_artifact_id,
                                path=step_output_path,
                                artifact_type="application/json",
                                size_bytes=len(step_output_content),
                            )
                            artifacts.append(step_output_artifact)
                            # Queue for registration after trace is built
                            pending_artifacts.append(
                                (
                                    step_output_artifact_id,
                                    step_output_path,
                                    step_output_content,
                                    "application/json",
                                )
                            )

                    # AF-0019: Capture subtasks from plan_subtasks skill
                    if skill_name == "plan_subtasks" and success:
                        raw_subtasks = result.get("subtasks", [])
                        planned_subtasks = raw_subtasks
                        # Convert to Subtask models for the trace
                        step_subtasks = [
                            Subtask(
                                subtask_id=st.get("subtask_id", f"subtask_{idx}"),
                                description=st.get("description", ""),
                                status=st.get("status", "pending"),
                            )
                            for idx, st in enumerate(raw_subtasks)
                        ]
                else:
                    # No skill - just mark as skipped
                    output_summary = "No skill defined for step"

            except KeyError as e:
                # Skill not found
                step_error = str(e)
            except Exception as e:
                # Unexpected error
                step_error = f"Unexpected error: {e}"

            step_ended = datetime.now(UTC)
            duration_ms = int((step_ended - step_started).total_seconds() * 1000)

            # Determine step type: PLANNING for plan_subtasks, otherwise SKILL_CALL
            if skill_name == "plan_subtasks":
                step_type = StepType.PLANNING
            elif skill_name:
                step_type = StepType.SKILL_CALL
            else:
                step_type = StepType.REASONING

            # AF-0094: Prepare input_data and output_data for trace
            step_input_data: dict[str, Any] | None = skill_params if skill_name else None
            step_output_data: dict[str, Any] | None = result if skill_name and result else None

            # Record the step
            step = Step(
                step_id=f"{run_id}-step-{i}",
                step_number=i,
                step_type=step_type,
                skill_name=skill_name,
                input_summary=f"prompt={task.prompt[:50]}...",
                output_summary=output_summary,
                started_at=step_started,
                ended_at=step_ended,
                duration_ms=duration_ms,
                error=step_error,
                subtasks=step_subtasks,  # AF-0019: Only set for plan step
                artifacts=step_artifact_ids,  # AF-0057: Skill-produced artifacts
                # AF-0094: Full step I/O for trace enrichment
                input_data=step_input_data,
                output_data=step_output_data,
            )
            steps.append(step)

            # Handle step failure
            if step_error:
                if playbook_step.required:
                    # Required step failed - stop execution
                    final_status = FinalStatus.FAILURE
                    error_message = f"Required step '{playbook_step.name}' failed: {step_error}"
                    break
                # Optional step failed - continue

        # Calculate total duration
        ended_at = datetime.now(UTC)
        duration_ms = int((ended_at - started_at).total_seconds() * 1000)

        # Run verification before constructing trace (AF-0029)
        verify_status, verify_message = self._verifier.verify_components(steps, final_status)
        checked_at = datetime.now(UTC)

        # Convert workspace_source string to enum if provided (AF-0030)
        ws_source_enum = WorkspaceSource(workspace_source) if workspace_source else None

        # AF-0062: Build LLMExecution for trace (None for manual mode)
        # AF-0094: Include tracked token usage
        llm_execution: LLMExecution | None = None
        if provider_config is not None:
            # Get usage from tracking provider if available
            usage = tracking_provider.get_usage() if tracking_provider else {}
            llm_execution = LLMExecution(
                provider=provider_config.provider,
                model=provider_config.model,
                call_count=usage.get("call_count", 0),  # AF-0094: Tracked call count
                total_tokens=usage.get("total_tokens"),  # AF-0094: Tracked tokens
                input_tokens=usage.get("input_tokens"),
                output_tokens=usage.get("output_tokens"),
            )

        # Build trace with verification result included
        trace = RunTrace(
            run_id=run_id,
            workspace_id=task.workspace_id,
            workspace_source=ws_source_enum,
            mode=task.mode,
            playbook=PlaybookMetadata(name=playbook.name, version=playbook.version),
            started_at=started_at,
            ended_at=ended_at,
            duration_ms=duration_ms,
            steps=steps,
            artifacts=artifacts,
            verifier=VerifierModel(
                status=VerifierStatus(verify_status),
                checked_at=checked_at,
                message=verify_message,
            ),
            final=final_status,
            error=error_message,
            llm=llm_execution,  # AF-0062: Include LLM provider info
        )

        # Persist the trace
        self._recorder.record(trace)

        # AF-0094: Register pending step output artifacts
        for artifact_id, path, content, artifact_type in pending_artifacts:
            self._recorder.register_artifact(
                trace=trace,
                artifact_id=artifact_id,
                path=path,
                content=content,
                artifact_type=artifact_type,
            )

        return trace

    def close(self) -> None:
        """Close underlying storage connections."""
        self._recorder.close()

    def __enter__(self) -> "V0Orchestrator":
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


# ---------------------------------------------------------------------------
# Runtime Factory
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
        if playbook_object is not None:
            selected_playbook = playbook_object
        else:
            selected_playbook = self._planner.plan(task)

        # Execute
        trace = self._orchestrator.run(task, selected_playbook, workspace_source=workspace_source)

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
    verifier = V0Verifier()
    orchestrator = V0Orchestrator(executor, verifier, recorder)

    return Runtime(
        normalizer=V0Normalizer(),
        planner=V0Planner(),
        orchestrator=orchestrator,
    )
