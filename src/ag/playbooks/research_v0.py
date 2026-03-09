"""research_v0 playbook — Research pipeline with web fetching (AF0074).

This playbook implements a complete research workflow:
1. Load local reference documents (optional)
2. Fetch content from URLs (optional)
3. Synthesize research report using LLM
4. Emit result as artifact

Architecture Principle: Skills = Capabilities, Playbooks = Procedures

Skills Used:
    - load_documents: File I/O capability (existing)
    - fetch_web_content: HTTP capability (new)
    - synthesize_research: LLM capability (new)
    - emit_result: File I/O capability (existing)

Usage:
    ag run --playbook research_v0 "Research question here"

    # With workspace containing:
    # workspace/inputs/*.md - local reference docs
    # workspace/urls.txt - URLs to fetch (one per line)
"""

from ag.core.playbook import (
    Budgets,
    Playbook,
    PlaybookStep,
    PlaybookStepType,
    ReasoningMode,
)

RESEARCH_V0 = Playbook(
    playbook_version="0.1",
    name="research_v0",
    version="1.0.0",
    description="Research pipeline: load docs, fetch URLs, synthesize report",
    reasoning_modes=[ReasoningMode.DIRECT],
    budgets=Budgets(
        max_steps=10,
        max_tokens=None,
        max_duration_seconds=300,  # 5 minute timeout (web fetching can be slow)
    ),
    steps=[
        PlaybookStep(
            step_id="step_0",
            name="load_local",
            step_type=PlaybookStepType.SKILL,
            skill_name="load_documents",
            description="Load local reference documents from workspace/inputs",
            required=False,  # Optional - no local docs is fine
            retry_count=0,
            parameters={
                "file_patterns": ["*.md", "*.txt", "*.pdf"],
                "max_files": 10,
            },
        ),
        PlaybookStep(
            step_id="step_1",
            name="fetch_web",
            step_type=PlaybookStepType.SKILL,
            skill_name="fetch_web_content",
            description="Fetch content from URLs (if provided in workspace)",
            required=False,  # Optional - no URLs is fine
            retry_count=1,  # Retry once for transient network issues
            parameters={
                "timeout_seconds": 30,
                "max_content_length": 50000,  # 50KB per page
            },
        ),
        PlaybookStep(
            step_id="step_2",
            name="synthesize",
            step_type=PlaybookStepType.SKILL,
            skill_name="synthesize_research",
            description="Synthesize research report from all sources",
            required=True,  # Core step - must succeed
            retry_count=1,  # Retry once for LLM transient issues
            parameters={
                "output_format": "markdown",
                "include_citations": True,
                "max_tokens": 4000,
            },
        ),
        PlaybookStep(
            step_id="step_3",
            name="emit",
            step_type=PlaybookStepType.SKILL,
            skill_name="emit_result",
            description="Store research report as artifact",
            required=True,
            retry_count=0,
            parameters={
                "artifact_name": "research_report.md",
            },
        ),
    ],
    metadata={
        "author": "ag_foundation",
        "stability": "experimental",
        "af_item": "AF-0074",
        "pipeline": "load → fetch → synthesize → emit",
    },
)
