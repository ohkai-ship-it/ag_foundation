"""Core runtime interfaces using typing.Protocol.

Design Decision: We use typing.Protocol for structural subtyping (duck typing)
rather than abc.ABC for nominal subtyping. This allows more flexibility and
better integration with testing (any object matching the interface works).

Interface Style:
- All interfaces are Protocols
- Methods use explicit type hints
- No default implementations in interfaces
- Implementations are in separate modules
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from ag.core import Playbook, RunTrace, TaskSpec


class Normalizer(Protocol):
    """Normalizes and validates incoming task requests.

    Responsibilities:
    - Parse and validate user input
    - Resolve defaults (workspace, mode, etc.)
    - Produce a validated TaskSpec
    """

    def normalize(self, prompt: str, **options: object) -> TaskSpec:
        """Normalize user input into a TaskSpec.

        Args:
            prompt: Raw user prompt string
            **options: CLI options (workspace, mode, playbook, etc.)

        Returns:
            Validated TaskSpec ready for planning
        """
        ...


class Planner(Protocol):
    """Selects and configures the execution playbook.

    Responsibilities:
    - Match task to appropriate playbook
    - Apply budget/constraint overrides
    - Return execution-ready playbook
    """

    def plan(self, task: TaskSpec) -> Playbook:
        """Select playbook for task execution.

        Args:
            task: Validated TaskSpec

        Returns:
            Playbook to execute
        """
        ...


class Orchestrator(Protocol):
    """Coordinates execution of playbook steps.

    Responsibilities:
    - Execute steps in sequence (v0: linear only)
    - Track step results and timing
    - Handle errors and early termination
    - Delegate to Executor for skill calls
    """

    def run(self, task: TaskSpec, playbook: Playbook) -> RunTrace:
        """Execute a playbook for the given task.

        Args:
            task: Validated TaskSpec
            playbook: Selected playbook

        Returns:
            RunTrace capturing execution history
        """
        ...


class Executor(Protocol):
    """Executes individual skills/tools.

    Responsibilities:
    - Resolve skill by name from registry
    - Execute skill with parameters
    - Capture output and errors
    """

    def execute(
        self, skill_name: str, parameters: dict[str, object]
    ) -> tuple[bool, str, dict[str, object]]:
        """Execute a skill.

        Args:
            skill_name: Name of skill to execute
            parameters: Skill parameters

        Returns:
            Tuple of (success, output_summary, result_data)
        """
        ...


class Verifier(Protocol):
    """Verifies execution results.

    Responsibilities:
    - Check step outputs against expectations
    - Run validation rules
    - Produce verification status
    """

    def verify(self, trace: RunTrace) -> tuple[str, str | None]:
        """Verify a run's results.

        Args:
            trace: RunTrace to verify

        Returns:
            Tuple of (status: 'passed'|'failed'|'skipped', message)
        """
        ...


class Recorder(Protocol):
    """Records run traces and artifacts.

    Responsibilities:
    - Persist RunTrace to storage
    - Register artifacts
    - Maintain run index
    """

    def record(self, trace: RunTrace) -> None:
        """Persist a RunTrace.

        Args:
            trace: RunTrace to persist
        """
        ...

    def register_artifact(
        self, trace: RunTrace, artifact_id: str, path: str, content: bytes
    ) -> str:
        """Register an artifact for a run.

        Args:
            trace: RunTrace that produced the artifact
            artifact_id: Unique artifact identifier
            path: Logical path/filename
            content: Artifact content

        Returns:
            Storage path/URI for the artifact
        """
        ...
