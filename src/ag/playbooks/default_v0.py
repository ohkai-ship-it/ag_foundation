"""default_v0 playbook — Simple echo playbook for testing (AF0079).

This is a minimal test playbook that uses the echo_tool skill.
For production use, consider the summarize_v0 playbook.

Note: The original default_v0 used V1 stub skills (analyze_task, execute_task,
verify_result) which were removed in AF0079.
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
    description="Default v0 playbook: simple echo for testing",
    reasoning_modes=[ReasoningMode.DIRECT],
    budgets=Budgets(
        max_steps=3,
        max_tokens=None,
        max_duration_seconds=60,
    ),
    steps=[
        PlaybookStep(
            step_id="step_0",
            name="echo",
            step_type=PlaybookStepType.SKILL,
            skill_name="echo_tool",
            description="Echo the input prompt",
            required=True,
            retry_count=0,
            parameters={"message": "{{prompt}}"},
        ),
    ],
    metadata={
        "author": "ag_foundation",
        "stability": "test",
        "note": "For production, use summarize_v0",
    },
)
