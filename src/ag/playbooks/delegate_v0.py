"""delegate_v0 playbook — Multi-step delegation with linear orchestration.

AF-0019: Agent network v0 with delegation flow.
Steps: normalize -> plan -> execute_subtask_1 -> execute_subtask_2 -> verify -> finalize
Planner generates >=2 subtasks recorded in trace metadata.
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
    description="Delegation playbook: multi-step execution with planner-generated subtasks",
    reasoning_modes=[ReasoningMode.DIRECT, ReasoningMode.CHAIN_OF_THOUGHT],
    budgets=Budgets(
        max_steps=20,  # More steps for delegation
        max_tokens=None,
        max_duration_seconds=600,  # 10 minute timeout
    ),
    steps=[
        PlaybookStep(
            step_id="delegate_step_0",
            name="normalize",
            step_type=PlaybookStepType.SKILL,
            skill_name="normalize_input",
            description="Normalize and validate task input, prepare context",
            required=True,
            retry_count=0,
        ),
        PlaybookStep(
            step_id="delegate_step_1",
            name="plan",
            step_type=PlaybookStepType.SKILL,
            skill_name="plan_subtasks",
            description="Decompose task into subtasks (planner generates >=2 subtasks)",
            required=True,
            retry_count=1,
            parameters={"min_subtasks": 2},
        ),
        PlaybookStep(
            step_id="delegate_step_2",
            name="execute_subtask_1",
            step_type=PlaybookStepType.SKILL,
            skill_name="execute_subtask",
            description="Execute first subtask from plan",
            required=True,
            retry_count=1,
            parameters={"subtask_index": 0},
        ),
        PlaybookStep(
            step_id="delegate_step_3",
            name="execute_subtask_2",
            step_type=PlaybookStepType.SKILL,
            skill_name="execute_subtask",
            description="Execute second subtask from plan",
            required=True,
            retry_count=1,
            parameters={"subtask_index": 1},
        ),
        PlaybookStep(
            step_id="delegate_step_4",
            name="verify",
            step_type=PlaybookStepType.SKILL,
            skill_name="verify_delegation",
            description="Verify all subtask results and aggregate evidence",
            required=True,
            retry_count=0,
        ),
        PlaybookStep(
            step_id="delegate_step_5",
            name="finalize",
            step_type=PlaybookStepType.SKILL,
            skill_name="finalize_result",
            description="Summarize delegation results and prepare final output",
            required=True,
            retry_count=0,
        ),
    ],
    metadata={
        "orchestration": "delegation",
        "author": "ag_foundation",
        "stability": "experimental",
        "af_item": "AF-0019",
    },
)
