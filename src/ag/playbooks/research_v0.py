"""research_v0 playbook — Autonomous research pipeline (AF0074, AF0080).

This playbook implements a complete autonomous research workflow:
1. Load local reference documents (optional)
2. Search web for relevant URLs (AF0080)
3. Fetch content from discovered URLs
4. Synthesize research report using LLM
5. Emit result as artifact

Architecture Principle: Skills = Capabilities, Playbooks = Procedures

Skills Used:
    - load_documents: File I/O capability (loads local reference docs)
    - web_search: Search API capability (discovers URLs from query) [AF0080]
    - fetch_web_content: HTTP capability (fetches URL content)
    - synthesize_research: LLM capability (synthesizes report)
    - emit_result: File I/O capability (saves artifact)

Usage:
    ag run --playbook research_v0 "Research question here"

    # Autonomous mode: URLs discovered from query via web_search
    # Fallback mode: Can still use workspace/inputs/urls.txt if provided
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
    version="1.1.0",  # Bumped for AF0080 web_search addition
    description="Research pipeline: load → search → fetch → synthesize → emit",
    reasoning_modes=[ReasoningMode.DIRECT],
    budgets=Budgets(
        max_steps=12,  # Increased for additional step
        max_tokens=None,
        max_duration_seconds=300,  # 5 minute timeout (web fetching can be slow)
    ),
    steps=[
        # Step 0: Load local reference documents (optional)
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
        # Step 1: Web search for URLs (AF0080 - autonomous URL discovery)
        PlaybookStep(
            step_id="step_1",
            name="search_web",
            step_type=PlaybookStepType.SKILL,
            skill_name="web_search",
            description="Search web for URLs relevant to research query",
            required=False,  # Optional - falls back to urls.txt if search unavailable
            retry_count=1,
            parameters={
                "max_results": 5,
                "search_engine": "duckduckgo",  # Free, no API key required
            },
        ),
        # Step 2: Fetch content from URLs
        PlaybookStep(
            step_id="step_2",
            name="fetch_web",
            step_type=PlaybookStepType.SKILL,
            skill_name="fetch_web_content",
            description="Fetch content from discovered URLs",
            required=False,  # Optional - supports local-only research
            retry_count=1,  # Retry once for transient network issues
            parameters={
                "timeout_seconds": 30,
                "max_content_length": 50000,  # 50KB per page
            },
        ),
        # Step 3: Synthesize research report
        PlaybookStep(
            step_id="step_3",
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
        # Step 4: Emit result artifact
        PlaybookStep(
            step_id="step_4",
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
        "af_items": ["AF-0074", "AF-0080"],
        "pipeline": "load → search → fetch → synthesize → emit",
        "compatibility": "urls.txt fallback still supported",
    },
)
