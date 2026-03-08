"""summarize_v0 playbook — Document summarization pipeline.

AF-0065: A three-step playbook for document summarization:
1. load_documents - Read files from workspace
2. summarize_docs - Call LLM to summarize
3. emit_result - Store output as artifact
"""

from ag.core.playbook import (
    Budgets,
    Playbook,
    PlaybookStep,
    PlaybookStepType,
    ReasoningMode,
)

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
