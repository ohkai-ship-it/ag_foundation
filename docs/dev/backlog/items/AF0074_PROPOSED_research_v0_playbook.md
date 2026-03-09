# BACKLOG ITEM — AF0074 — research_v0_playbook
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

> **File naming (required):** `AF0074_<Status>_research_v0_playbook.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0074
- **Type:** Feature / Implementation
- **Status:** PROPOSED
- **Priority:** P1
- **Area:** Playbooks / Skills
- **Owner:** TBD
- **Target sprint:** Sprint08

---

## Summary

Implement `research_v0` playbook with accompanying skills to create a working research pipeline that loads local documents, fetches web content, and synthesizes a research report.

This follows the architectural principle: **Skills = Capabilities, Playbooks = Procedures**.

---

## Playbook Design

### Pipeline

```
load_documents → fetch_web_content → synthesize_research → emit_result
```

### Steps

| Step | Skill | Capability | Status |
|------|-------|------------|--------|
| 1 | `load_documents` | File I/O: read local files | ✅ Exists |
| 2 | `fetch_web_content` | HTTP: fetch URLs | **NEW** |
| 3 | `synthesize_research` | LLM: combine sources into report | **NEW** |
| 4 | `emit_result` | File I/O: write output | ✅ Exists |

---

## New Skills

### `fetch_web_content`

**Capability:** Fetch content from user-provided URLs.

**Input:**
```python
class FetchWebContentInput(SkillInput):
    urls: list[str]  # URLs to fetch
    timeout_seconds: int = 30
    max_content_length: int = 100000  # Truncate large pages
```

**Output:**
```python
class FetchWebContentOutput(SkillOutput):
    documents: list[FetchedDocument]  # URL, content, status
    failed_urls: list[str]
```

**Implementation notes:**
- Use `httpx` or `aiohttp` for HTTP requests
- Handle common failures gracefully (timeout, 404, etc.)
- Extract text content from HTML (strip tags or use readability)
- NOT a search engine — user provides specific URLs

---

### `synthesize_research`

**Capability:** LLM-powered synthesis of multiple source documents.

**Input:**
```python
class SynthesizeResearchInput(SkillInput):
    prompt: str  # Research question
    documents: list[SourceDocument]  # From load_documents + fetch_web_content
    output_format: str = "markdown"  # markdown, json, plain
```

**Output:**
```python
class SynthesizeResearchOutput(SkillOutput):
    report: str  # Synthesized research report
    sources_used: list[str]  # Citations
    key_findings: list[str]  # Bullet points
```

**Implementation notes:**
- Similar to `summarize_docs` but focused on synthesis
- Include source citations in output
- Requires LLM provider (`requires_llm = True`)

---

## Playbook Definition

```python
RESEARCH_V0 = Playbook(
    playbook_version="0.1",
    name="research_v0",
    version="1.0.0",
    description="Research pipeline: load docs, fetch URLs, synthesize report",
    reasoning_modes=[ReasoningMode.DIRECT],
    budgets=Budgets(max_steps=10, max_duration_seconds=300),
    steps=[
        PlaybookStep(
            step_id="step_0",
            name="load_local",
            skill_name="load_documents",
            description="Load local reference documents",
            required=False,  # Optional if no local docs
        ),
        PlaybookStep(
            step_id="step_1",
            name="fetch_web",
            skill_name="fetch_web_content",
            description="Fetch content from provided URLs",
            required=False,  # Optional if no URLs
        ),
        PlaybookStep(
            step_id="step_2",
            name="synthesize",
            skill_name="synthesize_research",
            description="Synthesize research report from all sources",
            required=True,
        ),
        PlaybookStep(
            step_id="step_3",
            name="emit",
            skill_name="emit_result",
            description="Store research report as artifact",
            required=True,
        ),
    ],
    metadata={"author": "ag_foundation", "stability": "experimental"},
)
```

---

## Deliverables

- [ ] `src/ag/skills/fetch_web_content.py` — skill implementation
- [ ] `src/ag/skills/synthesize_research.py` — skill implementation
- [ ] `src/ag/playbooks/research_v0.py` — playbook definition
- [ ] Register new skills in `skills/registry.py`
- [ ] Register playbook in `playbooks/registry.py`
- [ ] Unit tests for both skills
- [ ] Integration test: `ag run --playbook research_v0`
- [ ] Update `ag playbooks list` output

---

## Acceptance Criteria

- [ ] `ag run --playbook research_v0 "Research topic X"` works end-to-end
- [ ] Can fetch and process at least 3 URLs
- [ ] Research report includes citations to sources
- [ ] All tests pass with coverage ≥95%
- [ ] CLI shows research_v0 in playbook list

---

## Dependencies

- **AF-0079:** Skills framework V1 removal (simplifies skill registration)
- Requires HTTP library (httpx recommended)
- Requires HTML text extraction (could be simple regex or library)
- LLM provider for synthesis step

---

## Related Items

- **AF-0069:** Skills architecture documentation
- **AF-0070:** Playbooks architecture documentation
- **AF-0076:** Playbooks registry cleanup
