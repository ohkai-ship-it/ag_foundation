"""Hardcoded playbooks for v0 runtime.

v0 Strategy: Playbooks are hardcoded Python objects.
Future: YAML/JSON loading from files.
"""

from __future__ import annotations

from ag.core.playbook import (
    Budgets,
    Playbook,
    PlaybookStep,
    PlaybookStepType,
    ReasoningMode,
)

# ---------------------------------------------------------------------------
# default_v0 Playbook
# ---------------------------------------------------------------------------
# A simple linear playbook for basic task execution.
# All steps use reasoning_mode='balanced' (mapped to DIRECT for simplicity).

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


# ---------------------------------------------------------------------------
# delegate_v0 Playbook — Multi-step delegation with linear orchestration
# ---------------------------------------------------------------------------
# AF-0019: Agent network v0 with delegation flow.
# Steps: normalize -> plan -> execute_subtask_1 -> execute_subtask_2 -> verify -> finalize
# Planner generates ≥2 subtasks recorded in trace metadata.

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
            description="Decompose task into subtasks (planner generates ≥2 subtasks)",
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


# ---------------------------------------------------------------------------
# summarize_v0 Playbook (AF0065)
# ---------------------------------------------------------------------------
# A three-step playbook for document summarization:
# 1. load_documents - Read files from workspace
# 2. summarize_docs - Call LLM to summarize
# 3. emit_result - Store output as artifact

SUMMARIZE_V0 = Playbook(
    playbook_version="0.1",
    name="summarize_v0",
    version="1.0.0",
    description="Summarize documents from workspace using LLM",
    reasoning_modes=[ReasoningMode.DIRECT],
    budgets=Budgets(
        max_steps=5,
        max_tokens=None,
        max_duration_seconds=120,
    ),
    steps=[
        PlaybookStep(
            step_id="step_0",
            name="load_docs",
            step_type=PlaybookStepType.SKILL,
            skill_name="load_documents",
            description="Read files matching patterns from workspace",
            required=True,
            retry_count=0,
        ),
        PlaybookStep(
            step_id="step_1",
            name="summarize",
            step_type=PlaybookStepType.SKILL,
            skill_name="summarize_docs",
            description="Call LLM to summarize document contents",
            required=True,
            retry_count=1,
        ),
        PlaybookStep(
            step_id="step_2",
            name="emit",
            step_type=PlaybookStepType.SKILL,
            skill_name="emit_result",
            description="Store summary as workspace artifact",
            required=True,
            retry_count=0,
        ),
    ],
    metadata={
        "author": "ag_foundation",
        "stability": "experimental",
        "af_item": "AF-0065",
    },
)


# ---------------------------------------------------------------------------
# Playbook Registry
# ---------------------------------------------------------------------------


def get_playbook(name: str) -> Playbook | None:
    """Get a playbook by name.

    Args:
        name: Playbook name

    Returns:
        Playbook if found, None otherwise
    """
    playbooks = {
        "default_v0": DEFAULT_V0,
        "default": DEFAULT_V0,  # Alias
        "delegate_v0": DELEGATE_V0,
        "delegate": DELEGATE_V0,  # Alias
        "summarize_v0": SUMMARIZE_V0,
        "summarize": SUMMARIZE_V0,  # Alias
    }
    return playbooks.get(name)


def list_playbooks() -> list[str]:
    """List available playbook names."""
    return ["default_v0", "delegate_v0", "summarize_v0"]
