"""default_v0 playbook — Simple linear execution with balanced reasoning.

v0 playbook for basic task execution with analyze/execute/verify steps.
"""

from ag.core.playbook import (
    Budgets,
    Playbook,
    PlaybookStep,
    PlaybookStepType,
    ReasoningMode,
)

DEFAULT_V0 = Playbook(
    playbook_version="0.1",
    name="default_v0",
    version="1.0.0",
    description="Default v0 playbook: linear execution with balanced reasoning",
    reasoning_modes=[ReasoningMode.DIRECT],  # balanced = direct in v0
    budgets=Budgets(
        max_steps=10,
        max_tokens=None,  # No token budget in v0
        max_duration_seconds=300,  # 5 minute timeout
    ),
    steps=[
        PlaybookStep(
            step_id="step_0",
            name="analyze",
            step_type=PlaybookStepType.SKILL,
            skill_name="analyze_task",
            description="Analyze the task and determine approach",
            required=True,
            retry_count=0,
        ),
        PlaybookStep(
            step_id="step_1",
            name="execute",
            step_type=PlaybookStepType.SKILL,
            skill_name="execute_task",
            description="Execute the main task logic",
            required=True,
            retry_count=1,  # Allow one retry
        ),
        PlaybookStep(
            step_id="step_2",
            name="verify",
            step_type=PlaybookStepType.SKILL,
            skill_name="verify_result",
            description="Verify the execution result",
            required=False,  # Optional verification
            retry_count=0,
        ),
    ],
    metadata={
        "reasoning_mode": "balanced",  # Human-readable mode name
        "author": "ag_foundation",
        "stability": "experimental",
    },
)
