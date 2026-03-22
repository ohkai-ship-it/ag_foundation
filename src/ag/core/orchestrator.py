"""V0 Orchestrator implementation.

Extracted from runtime.py (AF-0114).
Contains V0Orchestrator + helpers used only by orchestration:
- TrackingLLMProvider (AF-0094)
- _adapt_document_to_source (AF-0108)
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from ag.core.executor import V0Executor, V1Executor
from ag.core.playbook import Playbook, PlaybookStep
from ag.core.recorder import V0Recorder
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
from ag.core.task_spec import ExecutionMode, TaskSpec
from ag.core.verifier import V0Verifier, V1Verifier
from ag.providers.base import ChatMessage, ChatResponse, LLMProvider, ProviderConfig
from ag.providers.registry import get_provider
from ag.skills import SkillContext
from ag.storage import Workspace

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
# V0 Orchestrator Implementation
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
                # AF-0115: Propagate required flag from playbook step
                required=playbook_step.required,
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

        # AF-0115: Build evidence if verifier supports it
        verify_evidence: dict[str, Any] = {}
        if hasattr(self._verifier, "build_evidence"):
            verify_evidence = self._verifier.build_evidence(steps)

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
                evidence=verify_evidence,
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
# V1 Orchestrator — per-step verification (AF-0103, AF-0117)
# ---------------------------------------------------------------------------


class V1Orchestrator(V0Orchestrator):
    """Orchestrator with per-step verification (AF-0117).

    Extends V0 with:
    - Mixed skill+playbook plans (AF-0103)
    - Per-step verification after each skill execution
    - VERIFICATION steps interleaved with SKILL_CALL steps in trace
    - V1Executor (output schema validation) + V1Verifier (step-aware)
    """

    def __init__(
        self,
        executor: V0Executor | V1Executor | None = None,
        verifier: V0Verifier | V1Verifier | None = None,
        recorder: V0Recorder | None = None,
    ) -> None:
        # V1Orchestrator defaults to V1 components
        super().__init__(
            executor=executor or V1Executor(),
            verifier=verifier or V1Verifier(),
            recorder=recorder or V0Recorder(),
        )

    def _expand_steps(self, playbook: Playbook) -> list[PlaybookStep]:
        """Expand PLAYBOOK steps into their constituent skill steps.

        Returns a flat list of PlaybookSteps where all PLAYBOOK-type steps
        are replaced by the skills from the referenced playbook.
        """
        from ag.core.playbook import PlaybookStepType
        from ag.playbooks import get_playbook as get_pb

        expanded: list[PlaybookStep] = []
        for step in playbook.steps:
            if step.step_type == PlaybookStepType.PLAYBOOK:
                # Load the referenced playbook and inline its steps
                referenced_name = step.skill_name  # playbook name stored in skill_name
                if not referenced_name:
                    # No playbook referenced — skip
                    expanded.append(step)
                    continue

                referenced_playbook = get_pb(referenced_name)
                if referenced_playbook is None:
                    # Playbook not found — keep original step, executor will fail
                    expanded.append(step)
                    continue

                # Inline the playbook's skill steps, inheriting parameters
                for sub_step in referenced_playbook.steps:
                    # Merge parent step params into sub-step params (parent overrides)
                    merged_params = {**sub_step.parameters, **step.parameters}
                    inlined = PlaybookStep(
                        step_id=f"{step.step_id}_{sub_step.step_id}",
                        name=f"{referenced_name}/{sub_step.name}",
                        step_type=sub_step.step_type,
                        skill_name=sub_step.skill_name,
                        description=sub_step.description,
                        required=step.required and sub_step.required,  # AND logic: both must agree
                        retry_count=sub_step.retry_count,
                        timeout_seconds=sub_step.timeout_seconds,
                        parameters=merged_params,
                    )
                    expanded.append(inlined)
            else:
                expanded.append(step)
        return expanded

    def _record_verification(
        self,
        run_id: str,
        step_index: int,
        verified_step: Step,
        passed: bool,
        message: str,
    ) -> Step:
        """Create a VERIFICATION step for the trace (AF-0117)."""
        now = datetime.now(UTC)
        return Step(
            step_id=f"{run_id}-verify-{step_index}",
            step_number=step_index,
            step_type=StepType.VERIFICATION,
            skill_name=None,
            input_summary=f"Verifying step {verified_step.step_number}: {verified_step.skill_name}",
            output_summary=message,
            started_at=now,
            ended_at=now,
            duration_ms=0,
            error=None if passed else message,
            subtasks=None,
            artifacts=[],
            input_data={"verified_step": verified_step.step_number},
            output_data={"passed": passed, "message": message},
            required=False,  # Verification steps are never "required" themselves
        )

    def run(
        self, task: TaskSpec, playbook: Playbook, workspace_source: str | None = None
    ) -> RunTrace:
        """Execute a playbook with per-step verification (AF-0117).

        Flow:
        1. Expand PLAYBOOK steps to skill steps
        2. For each skill step:
           a. Execute skill
           b. Record SKILL_CALL step
           c. Run per-step verification
           d. Record VERIFICATION step
           e. Stop if required step failed verification
        3. Run end-of-run verification summary
        """
        # Expand PLAYBOOK steps to skill steps
        expanded_playbook = Playbook(
            playbook_version=playbook.playbook_version,
            name=playbook.name,
            version=playbook.version,
            description=playbook.description,
            reasoning_modes=playbook.reasoning_modes,
            budgets=playbook.budgets,
            steps=self._expand_steps(playbook),
            metadata=playbook.metadata,
        )

        # Check if verifier supports per-step verification
        has_verify_step = hasattr(self._verifier, "verify_step")

        if not has_verify_step:
            # No per-step verification, fall back to V0 behavior
            return super().run(task, expanded_playbook, workspace_source=workspace_source)

        # --- Full V1 per-step verification loop ---
        run_id = str(uuid4())
        started_at = datetime.now(UTC)
        steps: list[Step] = []
        artifacts: list[Artifact] = []
        final_status = FinalStatus.SUCCESS
        error_message: str | None = None

        # Resolve workspace path for skill context
        workspace_path: Path | None = None
        if task.workspace_id:
            try:
                ws = Workspace(task.workspace_id)
                if ws.exists():
                    workspace_path = ws.path
            except Exception:
                pass

        # Track subtasks and step results
        planned_subtasks: list[dict[str, Any]] = []
        step_results: list[dict[str, Any]] = []
        accumulated_result: dict[str, Any] = {}

        # Create LLM provider
        llm_provider: LLMProvider | None = None
        tracking_provider: TrackingLLMProvider | None = None
        provider_config: ProviderConfig | None = None
        if task.mode != ExecutionMode.MANUAL:
            try:
                provider_config = ProviderConfig(
                    provider="openai",
                    model="gpt-4o-mini",
                )
                raw_provider = get_provider(provider_config)
                tracking_provider = TrackingLLMProvider(raw_provider)
                llm_provider = tracking_provider
            except Exception:
                pass

        # Track pending artifacts
        pending_artifacts: list[tuple[str, str, bytes, str]] = []

        # Step counter for trace (includes verification steps)
        trace_step_index = 0

        # Execute each step with per-step verification
        for i, playbook_step in enumerate(expanded_playbook.steps):
            step_started = datetime.now(UTC)
            step_error: str | None = None
            output_summary = ""
            skill_name = playbook_step.skill_name
            step_subtasks: list[Subtask] | None = None
            result: dict[str, Any] = {}
            step_artifact_ids: list[str] = []

            try:
                if skill_name:
                    # Build skill parameters
                    chained_result = accumulated_result.copy()
                    if skill_name == "synthesize_research" and "documents" in chained_result:
                        chained_result = {
                            **chained_result,
                            "documents": [
                                _adapt_document_to_source(doc)
                                for doc in chained_result["documents"]
                            ],
                        }
                    step_params = {
                        k: v
                        for k, v in playbook_step.parameters.items()
                        if not (isinstance(v, str) and v.startswith("previous_step."))
                    }
                    skill_params = {
                        "prompt": task.prompt,
                        "step": i,
                        **step_params,
                        **chained_result,
                    }
                    if skill_name == "execute_subtask" and planned_subtasks:
                        skill_params["subtasks"] = planned_subtasks

                    trace_metadata: dict[str, Any] = {
                        "elapsed_ms": int((datetime.now(UTC) - started_at).total_seconds() * 1000),
                        "playbook_name": expanded_playbook.name,
                        "playbook_version": expanded_playbook.version,
                        "steps_summary": [
                            {
                                "skill": s.skill_name or "no-skill",
                                "duration_ms": s.duration_ms,
                                "output_summary": (
                                    s.output_summary[:100] if s.output_summary else ""
                                ),
                            }
                            for s in steps
                            if s.step_type == StepType.SKILL_CALL  # Only skill steps for summary
                        ],
                    }
                    if provider_config:
                        trace_metadata["model"] = provider_config.model

                    skill_context = SkillContext(
                        provider=llm_provider,
                        workspace_path=workspace_path,
                        step_number=i,
                        run_id=run_id,
                        trace_metadata=trace_metadata,
                    )

                    success, output_summary, result = self._executor.execute(
                        skill_name, skill_params, skill_context
                    )
                    if not success:
                        step_error = output_summary
                    else:
                        step_results.append(result)
                        accumulated_result.update(result)

                        if "artifact_id" in result:
                            artifact_id = result["artifact_id"]
                            step_artifact_ids.append(artifact_id)
                            artifact = Artifact(
                                artifact_id=artifact_id,
                                path=result.get("artifact_path", f"{skill_name}_output"),
                                artifact_type=result.get("artifact_type", "application/json"),
                                size_bytes=result.get("bytes_written"),
                            )
                            artifacts.append(artifact)

                        if result:
                            step_output_artifact_id = f"{run_id}-step-{i}-{skill_name}_output"
                            step_output_path = f"{i}_{skill_name}_output.json"
                            step_output_content = json.dumps(result, indent=2).encode("utf-8")
                            step_artifact_ids.append(step_output_artifact_id)
                            step_output_artifact = Artifact(
                                artifact_id=step_output_artifact_id,
                                path=step_output_path,
                                artifact_type="application/json",
                                size_bytes=len(step_output_content),
                            )
                            artifacts.append(step_output_artifact)
                            pending_artifacts.append(
                                (
                                    step_output_artifact_id,
                                    step_output_path,
                                    step_output_content,
                                    "application/json",
                                )
                            )

                    if skill_name == "plan_subtasks" and success:
                        raw_subtasks = result.get("subtasks", [])
                        planned_subtasks = raw_subtasks
                        step_subtasks = [
                            Subtask(
                                subtask_id=st.get("subtask_id", f"subtask_{idx}"),
                                description=st.get("description", ""),
                                status=st.get("status", "pending"),
                            )
                            for idx, st in enumerate(raw_subtasks)
                        ]
                else:
                    output_summary = "No skill defined for step"

            except KeyError as e:
                step_error = str(e)
            except ValueError as e:
                step_error = str(e)
            except Exception as e:
                step_error = f"Unexpected error: {e}"

            step_ended = datetime.now(UTC)
            duration_ms = int((step_ended - step_started).total_seconds() * 1000)

            # Determine step type
            if skill_name == "plan_subtasks":
                step_type = StepType.PLANNING
            elif skill_name:
                step_type = StepType.SKILL_CALL
            else:
                step_type = StepType.REASONING

            step_input_data: dict[str, Any] | None = skill_params if skill_name else None
            step_output_data: dict[str, Any] | None = result if skill_name and result else None

            # Record the skill step
            step = Step(
                step_id=f"{run_id}-step-{trace_step_index}",
                step_number=trace_step_index,
                step_type=step_type,
                skill_name=skill_name,
                input_summary=f"prompt={task.prompt[:50]}...",
                output_summary=output_summary,
                started_at=step_started,
                ended_at=step_ended,
                duration_ms=duration_ms,
                error=step_error,
                subtasks=step_subtasks,
                artifacts=step_artifact_ids,
                input_data=step_input_data,
                output_data=step_output_data,
                required=playbook_step.required,
            )
            steps.append(step)
            trace_step_index += 1

            # --- AF-0117: Per-step verification ---
            verify_passed, verify_msg = self._verifier.verify_step(step)
            verification_step = self._record_verification(
                run_id, trace_step_index, step, verify_passed, verify_msg
            )
            steps.append(verification_step)
            trace_step_index += 1

            # Decision: stop or continue?
            if not verify_passed and playbook_step.required:
                # Required step failed verification → stop execution
                final_status = FinalStatus.FAILURE
                error_message = f"Required step '{playbook_step.name}' failed: {step_error}"
                break
            # Optional step failure or verification passed → continue

        # Calculate total duration
        ended_at = datetime.now(UTC)
        duration_ms = int((ended_at - started_at).total_seconds() * 1000)

        # End-of-run verification summary
        verify_status, verify_message = self._verifier.verify_components(steps, final_status)
        checked_at = datetime.now(UTC)

        verify_evidence: dict[str, Any] = {}
        if hasattr(self._verifier, "build_evidence"):
            # Filter to just skill steps for evidence building
            skill_steps = [s for s in steps if s.step_type != StepType.VERIFICATION]
            verify_evidence = self._verifier.build_evidence(skill_steps)

        ws_source_enum = WorkspaceSource(workspace_source) if workspace_source else None

        llm_execution: LLMExecution | None = None
        if provider_config is not None:
            usage = tracking_provider.get_usage() if tracking_provider else {}
            llm_execution = LLMExecution(
                provider=provider_config.provider,
                model=provider_config.model,
                call_count=usage.get("call_count", 0),
                total_tokens=usage.get("total_tokens"),
                input_tokens=usage.get("input_tokens"),
                output_tokens=usage.get("output_tokens"),
            )

        trace = RunTrace(
            run_id=run_id,
            workspace_id=task.workspace_id,
            workspace_source=ws_source_enum,
            mode=task.mode,
            playbook=PlaybookMetadata(name=expanded_playbook.name, version=expanded_playbook.version),
            started_at=started_at,
            ended_at=ended_at,
            duration_ms=duration_ms,
            steps=steps,
            artifacts=artifacts,
            verifier=VerifierModel(
                status=VerifierStatus(verify_status),
                checked_at=checked_at,
                message=verify_message,
                evidence=verify_evidence,
            ),
            final=final_status,
            error=error_message,
            llm=llm_execution,
        )

        self._recorder.record(trace)

        for artifact_id, path, content, artifact_type in pending_artifacts:
            self._recorder.register_artifact(
                trace=trace,
                artifact_id=artifact_id,
                path=path,
                content=content,
                artifact_type=artifact_type,
            )

        return trace
