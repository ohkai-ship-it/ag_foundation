"""test_skill playbook — Dummy playbook for testing skill execution.

This is a minimal test playbook that uses the zero_skill skill twice.
Used for testing playbook execution without any actual functionality.

Skills Used:
    - zero_skill: Dummy skill with no functionality (runs twice)

Usage:
    ag run --playbook test_skill "any prompt"
"""

from ag.core.playbook import (
    Budgets,
    Playbook,
    PlaybookStep,
    PlaybookStepType,
    ReasoningMode,
)

TEST_SKILL = Playbook(
    playbook_version="0.1",
    name="test_skill",
    version="1.0.0",
    description="Test playbook: runs zero_skill twice",
    reasoning_modes=[ReasoningMode.DIRECT],
    budgets=Budgets(
        max_steps=3,
        max_tokens=None,
        max_duration_seconds=60,
    ),
    steps=[
        PlaybookStep(
            step_id="step_0",
            name="zero_first",
            step_type=PlaybookStepType.SKILL,
            skill_name="zero_skill",
            description="First invocation of zero_skill",
            required=True,
            retry_count=0,
            parameters={},
        ),
        PlaybookStep(
            step_id="step_1",
            name="zero_second",
            step_type=PlaybookStepType.SKILL,
            skill_name="zero_skill",
            description="Second invocation of zero_skill",
            required=True,
            retry_count=0,
            parameters={},
        ),
    ],
    metadata={
        "author": "ag_foundation",
        "stability": "test",
        "note": "Dummy playbook for testing",
    },
)
