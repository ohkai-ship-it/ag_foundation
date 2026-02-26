"""v0 Runtime implementation.

Implements the core runtime loop: Normalizer -> Planner -> Orchestrator -> Recorder
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from ag.core.playbook import Playbook
from ag.core.playbooks import DEFAULT_V0, get_playbook
from ag.core.run_trace import (
    Artifact,
    FinalStatus,
    PlaybookMetadata,
    RunTrace,
    Step,
    StepType,
    Subtask,
    VerifierStatus,
)
from ag.core.run_trace import (
    Verifier as VerifierModel,
)
from ag.core.task_spec import Budgets, Constraints, ExecutionMode, TaskSpec
from ag.skills import SkillRegistry, get_default_registry
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

        # Resolve workspace
        workspace_id = workspace or f"ws-{uuid4().hex[:8]}"

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
        self, skill_name: str, parameters: dict[str, Any]
    ) -> tuple[bool, str, dict[str, Any]]:
        """Execute a skill."""
        if not self._registry.has(skill_name):
            raise KeyError(f"Skill not found: {skill_name}")

        return self._registry.execute(skill_name, parameters)


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
        # Check for step errors
        for step in trace.steps:
            if step.error:
                return "failed", f"Step {step.step_number} failed: {step.error}"

        # Check final status
        if trace.final != FinalStatus.SUCCESS:
            return "failed", f"Run ended with status: {trace.final.value}"

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

    def run(self, task: TaskSpec, playbook: Playbook) -> RunTrace:
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

        # AF-0019: Track subtasks from planning step for delegation
        planned_subtasks: list[dict[str, Any]] = []

        # Execute each step in sequence
        for i, playbook_step in enumerate(playbook.steps):
            step_started = datetime.now(UTC)
            step_error: str | None = None
            output_summary = ""
            skill_name = playbook_step.skill_name
            step_subtasks: list[Subtask] | None = None
            result: dict[str, Any] = {}

            try:
                if skill_name:
                    # Build skill parameters: merge step params with task context
                    skill_params = {
                        "prompt": task.prompt,
                        "step": i,
                        **playbook_step.parameters,
                    }
                    # AF-0019: Pass subtasks context to execute_subtask skills
                    if skill_name == "execute_subtask" and planned_subtasks:
                        skill_params["subtasks"] = planned_subtasks

                    # Execute the skill
                    success, output_summary, result = self._executor.execute(
                        skill_name, skill_params
                    )
                    if not success:
                        step_error = output_summary

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

        # Build trace (before verification)
        trace = RunTrace(
            run_id=run_id,
            workspace_id=task.workspace_id,
            mode=task.mode,
            playbook=PlaybookMetadata(name=playbook.name, version=playbook.version),
            started_at=started_at,
            ended_at=ended_at,
            duration_ms=duration_ms,
            steps=steps,
            artifacts=artifacts,
            verifier=VerifierModel(status=VerifierStatus.PENDING),
            final=final_status,
            error=error_message,
        )

        # Run verification
        verify_status, verify_message = self._verifier.verify(trace)
        trace = RunTrace(
            **{
                **trace.model_dump(),
                "verifier": VerifierModel(
                    status=VerifierStatus(verify_status),
                    checked_at=datetime.now(UTC),
                    message=verify_message,
                ),
            }
        )

        # Persist the trace
        self._recorder.record(trace)

        # AF-0009: Create result artifact with step summaries
        if steps:
            result_content = self._build_result_artifact(trace, steps)
            artifact_id = f"{run_id}-result"
            self._recorder.register_artifact(
                trace=trace,
                artifact_id=artifact_id,
                path="result.md",
                content=result_content.encode("utf-8"),
                artifact_type="text/markdown",
            )
            # Update trace artifacts list with the new artifact ID
            artifacts.append(artifact_id)

        return trace

    def _build_result_artifact(self, trace: RunTrace, steps: list[Step]) -> str:
        """Build result.md artifact content from step outputs.

        Args:
            trace: The completed run trace
            steps: List of steps that were executed

        Returns:
            Markdown content summarizing the run results
        """
        lines = [
            f"# Run Result: {trace.run_id}",
            "",
            f"- **Status:** {trace.final.value}",
            f"- **Mode:** {trace.mode.value}",
            (
                f"- **Duration:** {trace.duration_ms}ms"
                if trace.duration_ms
                else "- **Duration:** unknown"
            ),
            f"- **Playbook:** {trace.playbook.name}@{trace.playbook.version}",
            "",
            "## Steps",
            "",
        ]

        for step in steps:
            status = "✓" if not step.error else "✗"
            lines.append(f"### {status} Step {step.step_number}: {step.step_type.value}")
            if step.skill_name:
                lines.append(f"- **Skill:** {step.skill_name}")
            lines.append(f"- **Output:** {step.output_summary}")
            if step.error:
                lines.append(f"- **Error:** {step.error}")
            lines.append("")

        return "\n".join(lines)

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
    ) -> RunTrace:
        """Execute a task and return the trace.

        Args:
            prompt: User's task description
            workspace: Workspace ID (auto-generated if not provided)
            mode: Execution mode ('manual' or 'llm')
            playbook: Playbook name preference

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

        # Plan
        selected_playbook = self._planner.plan(task)

        # Execute
        trace = self._orchestrator.run(task, selected_playbook)

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
