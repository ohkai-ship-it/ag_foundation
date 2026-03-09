"""delegate_v0 playbook — Multi-step echo playbook for testing (AF0079).

This is a minimal test playbook demonstrating multi-step execution.
The original delegation skills (normalize_input, plan_subtasks, etc.)
were removed in AF0079 as they were V1 stubs.

For production delegation patterns, implement real V2 skills.
"""

from ag.core.playbook import (
    Budgets,
    Playbook,
    PlaybookStep,
    PlaybookStepType,
    ReasoningMode,
)

DELEGATE_V0 = Playbook(
    playbook_version="0.1",
    name="delegate_v0",
    version="1.0.0",
    description="Delegation playbook: multi-step echo for testing",
    reasoning_modes=[ReasoningMode.DIRECT],
    budgets=Budgets(
        max_steps=5,
        max_tokens=None,
        max_duration_seconds=60,
    ),
    steps=[
        PlaybookStep(
            step_id="delegate_step_0",
            name="echo_1",
            step_type=PlaybookStepType.SKILL,
            skill_name="echo_tool",
            description="Echo step 1: normalize",
            required=True,
            retry_count=0,
            parameters={"message": "Normalized: {{prompt}}"},
        ),
        PlaybookStep(
            step_id="delegate_step_1",
            name="echo_2",
            step_type=PlaybookStepType.SKILL,
            skill_name="echo_tool",
            description="Echo step 2: plan",
            required=True,
            retry_count=0,
            parameters={"message": "Planned: {{prompt}}"},
        ),
    ],
    metadata={
        "orchestration": "delegation_stub",
        "author": "ag_foundation",
        "stability": "test",
        "note": "Original V1 delegation skills removed in AF0079",
    },
)
