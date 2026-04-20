# BACKLOG ITEM — AF0080 — web_search_skill
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

> **File naming (required):** `AF0080_<STATUS>_web_search_skill.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0080
- **Type:** Feature / Implementation
- **Status:** DONE
- **Priority:** P1
- **Area:** Skills / Playbooks
- **Owner:** Jacob
- **Target sprint:** Sprint08
- **Related items:** AF0074 (research_v0_playbook), BUG-0013 (pipeline broken)

---

## Executive Summary

Implement a `web_search` skill that performs real web searches via search engine APIs, returning URLs for the `fetch_web_content` skill. This completes the autonomous research pipeline by bridging the gap between user query and web content fetching.

**Core Problem:** The `research_v0` playbook (AF0074) cannot function autonomously because `fetch_web_content` requires URLs, but no skill produces URLs from a user's research query.

**Solution:** Add `web_search` skill as the missing link: `query → URLs → documents → report`

---

## Problem Statement

### Current State

```
User: "Research the Düsseldorf meteorite"
          │
          ▼
    ┌─────────────────────┐
    │  fetch_web_content  │  ← WHERE DO URLs COME FROM?
    │  Input: urls=???    │
    └─────────────────────┘
```

The `fetch_web_content` skill is a pure HTTP capability — it fetches content from given URLs. But the pipeline has no mechanism to *discover* relevant URLs from the user's research query.

Current workarounds (both inadequate):
1. **Manual `urls.txt` file** — Requires user to curate URLs beforehand (defeats autonomous research)
2. **Hardcoded URLs in playbook** — Static, not query-responsive

### Desired State

```
User: "Research the Düsseldorf meteorite"
          │
          ▼
    ┌─────────────────────┐
    │     web_search      │  ← NEW: Query → URLs
    │  Input: query       │
    │  Output: urls       │
    └──────────┬──────────┘
               │ urls
               ▼
    ┌─────────────────────┐
    │  fetch_web_content  │
    │  Input: urls        │
    │  Output: documents  │
    └─────────────────────┘
```

---

## Goal

Implement a production-ready `web_search` skill that:

1. **Accepts a search query** (from user prompt or LLM-refined)
2. **Calls a real search engine API** (not a stub/mock)
3. **Returns structured URL results** that chain directly to `fetch_web_content`
4. **Handles errors gracefully** (API failures, rate limits, no results)

**Verifiable outcome:** Running `ag run --playbook research_v0 "Research topic"` produces a research report without requiring manual URL curation.

---

## Non-goals

- **Building a search engine** — We use existing APIs (Google, Bing, DuckDuckGo)
- **LLM-powered query refinement** — Future enhancement; v1 uses query as-is
- **Caching/deduplication** — Future optimization
- **Image/video search** — Text search only for v1

---

## Architecture Alignment

### Skill Design Principles (from SKILLS_ARCHITECTURE_0.1.md)

| Principle | How `web_search` Complies |
|-----------|---------------------------|
| **Skills = Capabilities** | Web search is a distinct capability (API call) |
| **Single Responsibility** | Only searches; does not fetch content |
| **Schema-Bounded I/O** | Strict Pydantic input/output schemas |
| **No LLM Required** | Pure API call — `requires_llm = False` |
| **Graceful Failure** | Returns empty results on error, not exceptions |

### Pipeline Position

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         research_v0 Pipeline                               │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  Step 1: web_search                                          [NEW]         │
│  ────────────────────                                                      │
│  Capability: Search Engine API                                             │
│  Input:  query (from task.prompt)                                          │
│  Output: urls: list[str]                                                   │
│                                                                            │
│                              │                                             │
│                              ▼ urls                                        │
│                                                                            │
│  Step 2: fetch_web_content                                   [EXISTS]      │
│  ────────────────────────────                                              │
│  Capability: HTTP I/O                                                      │
│  Input:  urls (from web_search)                                            │
│  Output: documents: list[FetchedDocument]                                  │
│                                                                            │
│                              │                                             │
│                              ▼ documents                                   │
│                                                                            │
│  Step 3: synthesize_research                                 [EXISTS]      │
│  ────────────────────────────────                                          │
│  Capability: LLM                                                           │
│  Input:  documents, prompt                                                 │
│  Output: report, key_findings, sources                                     │
│                                                                            │
│                              │                                             │
│                              ▼ report                                      │
│                                                                            │
│  Step 4: emit_result                                         [EXISTS]      │
│  ───────────────────                                                       │
│  Capability: File I/O                                                      │
│  Output: artifact (research_report.md)                                     │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Technical Specification

### Schemas

```python
# ---------------------------------------------------------------------------
# Input Schema
# ---------------------------------------------------------------------------

class WebSearchInput(SkillInput):
    """Input for web_search skill.
    
    Schema: SCHEMA_INVENTORY.md#WebSearchInput
    """
    
    query: str = Field(
        default="",
        min_length=0,
        max_length=500,
        description="Search query; if empty, derive from prompt"
    )
    max_results: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of URLs to return"
    )
    search_engine: str = Field(
        default="duckduckgo",
        description="Search engine: 'duckduckgo' | 'google' | 'bing' | 'serper'"
    )
    region: str = Field(
        default="wt-wt",  # Worldwide
        description="Region code for localized results"
    )
    safe_search: bool = Field(
        default=True,
        description="Enable safe search filtering"
    )
    
    model_config = {"extra": "forbid"}

    @model_validator(mode="after")
    def ensure_query(self) -> "WebSearchInput":
        """Use prompt as fallback to satisfy runtime chaining contract.

        Runtime injects `prompt` by default for every skill step.
        This keeps playbook parameters minimal while ensuring query is always present.
        """
        if not self.query and self.prompt:
            self.query = self.prompt
        if not self.query:
            raise ValueError("Either query or prompt must be provided")
        return self


# ---------------------------------------------------------------------------
# Output Schema
# ---------------------------------------------------------------------------

class SearchResult(BaseModel):
    """A single search result."""
    
    url: str = Field(..., description="Result URL")
    title: str = Field(default="", description="Result title")
    snippet: str = Field(default="", description="Result snippet/description")
    position: int = Field(default=0, description="Position in search results")
    
    model_config = {"extra": "forbid"}


class WebSearchOutput(SkillOutput):
    """Output from web_search skill.
    
    Schema: SCHEMA_INVENTORY.md#WebSearchOutput
    
    NOTE: The 'urls' field is the PRIMARY output for pipeline chaining.
    It matches FetchWebContentInput.urls directly.
    """
    
    urls: list[str] = Field(
        default_factory=list,
        description="URLs found (primary output for chaining to fetch_web_content)"
    )
    results: list[SearchResult] = Field(
        default_factory=list,
        description="Detailed search results with titles and snippets"
    )
    search_query: str = Field(
        default="",
        description="Actual query used (may differ from input if refined)"
    )
    search_engine: str = Field(
        default="",
        description="Search engine used"
    )
    total_results: int = Field(
        default=0,
        description="Number of results returned"
    )
    
    model_config = {"extra": "forbid"}
```

### Pipeline Data Flow

The key design decision is the `urls` field name in `WebSearchOutput`:

```python
# web_search returns:
{
    "urls": ["https://...", "https://...", ...],  # ← KEY FIELD
    "results": [...],
    "search_query": "Düsseldorf meteorite",
    "total_results": 5
}

# Runtime merges into next step:
parameters = {
    "prompt": "Research the Düsseldorf meteorite",
    **playbook_step.parameters,
    **previous_result,  # ← urls injected here
}

# fetch_web_content receives:
{
    "prompt": "Research the Düsseldorf meteorite",
    "urls": ["https://...", "https://...", ...],  # ← FROM web_search
    "timeout_seconds": 30,
    ...
}
```

---

## Search Engine Options

### Option 1: DuckDuckGo (Recommended for v1)

**Implementation:** Use `duckduckgo-search` Python package

```python
from duckduckgo_search import DDGS

def search_duckduckgo(query: str, max_results: int) -> list[SearchResult]:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
        return [
            SearchResult(
                url=r["href"],
                title=r["title"],
                snippet=r["body"],
                position=i,
            )
            for i, r in enumerate(results)
        ]
```

**Pros:**
- Free, no API key required
- No rate limiting (reasonable use)
- Privacy-focused
- Simple Python package

**Cons:**
- Unofficial API (may break)
- Limited advanced features

**Dependency:** `pip install duckduckgo-search`

---

### Option 2: Google Custom Search API

**Implementation:** Google's official API

```python
import httpx

def search_google(query: str, max_results: int, api_key: str, cx: str) -> list[SearchResult]:
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,  # Custom Search Engine ID
        "q": query,
        "num": min(max_results, 10),  # Max 10 per request
    }
    response = httpx.get(url, params=params)
    data = response.json()
    
    return [
        SearchResult(
            url=item["link"],
            title=item["title"],
            snippet=item.get("snippet", ""),
            position=i,
        )
        for i, item in enumerate(data.get("items", []))
    ]
```

**Pros:**
- Official, stable API
- High-quality results
- Rich metadata

**Cons:**
- Requires API key + Custom Search Engine setup
- $5 per 1000 queries (after free tier)
- More complex setup

**Config required:**
```bash
export GOOGLE_API_KEY="..."
export GOOGLE_SEARCH_ENGINE_ID="..."
```

---

### Option 3: Serper API (Recommended for production)

**Implementation:** Serper.dev Google Search API

```python
import httpx

def search_serper(query: str, max_results: int, api_key: str) -> list[SearchResult]:
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    payload = {"q": query, "num": max_results}
    
    response = httpx.post(url, headers=headers, json=payload)
    data = response.json()
    
    return [
        SearchResult(
            url=item["link"],
            title=item["title"],
            snippet=item.get("snippet", ""),
            position=i,
        )
        for i, item in enumerate(data.get("organic", []))
    ]
```

**Pros:**
- Google results without Custom Search Engine
- Simple API, fast
- 2500 free queries/month
- $50/month for 50,000 queries

**Cons:**
- Third-party service
- Requires API key

**Config required:**
```bash
export SERPER_API_KEY="..."
```

---

### Option 4: Bing Web Search API

**Implementation:** Azure Cognitive Services

```python
import httpx

def search_bing(query: str, max_results: int, api_key: str) -> list[SearchResult]:
    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query, "count": max_results}
    
    response = httpx.get(url, headers=headers, params=params)
    data = response.json()
    
    return [
        SearchResult(
            url=item["url"],
            title=item["name"],
            snippet=item.get("snippet", ""),
            position=i,
        )
        for i, item in enumerate(data.get("webPages", {}).get("value", []))
    ]
```

**Pros:**
- Official Microsoft API
- 1000 free queries/month
- Good result quality

**Cons:**
- Azure account required
- Complex setup

---

## Recommended Approach

### v1 Implementation (This PR)

```
Primary:    DuckDuckGo (free, no API key, works immediately)
Fallback:   Serper API (if SERPER_API_KEY configured)
```

**Rationale:**
- DuckDuckGo allows immediate functionality without setup
- Serper provides production-quality results when needed
- Users can configure their preferred engine via environment

### Configuration

```python
# Environment variables (optional)
SERPER_API_KEY      # Enables Serper API
GOOGLE_API_KEY      # Enables Google Search
BING_API_KEY        # Enables Bing Search

# If no API keys configured, falls back to DuckDuckGo
```

---

## Skill Implementation

```python
"""Web Search Skill — Search Engine API Capability (AF0080).

This skill performs web searches via search engine APIs and returns
URLs for the fetch_web_content skill. It is the discovery phase of
the research pipeline.

Schemas Defined (see docs/dev/additional/SCHEMA_INVENTORY.md):
    SearchResult — Single search result (url, title, snippet)
    WebSearchInput — Input schema (query, max_results, search_engine)
    WebSearchOutput — Output schema (urls, results, total_results)

Contracts Implemented (see docs/dev/additional/CONTRACT_INVENTORY.md):
    Skill[WebSearchInput, WebSearchOutput] — Web search capability

Pipeline Position:
    This is step 1 of the research_v0 playbook:
    web_search → fetch_web_content → synthesize_research → emit_result
"""

from __future__ import annotations

import os
from typing import ClassVar

from pydantic import BaseModel, Field

from ag.skills.base import Skill, SkillContext, SkillInput, SkillOutput


# [... schemas as defined above ...]


class WebSearchSkill(Skill[WebSearchInput, WebSearchOutput]):
    """Search the web for URLs matching a query.
    
    This skill calls search engine APIs to discover relevant URLs.
    It does NOT fetch content — that is handled by fetch_web_content.
    
    Contract: CONTRACT_INVENTORY.md#WebSearchSkill
    
    Supported search engines:
    - duckduckgo (default, free, no API key)
    - serper (requires SERPER_API_KEY)
    - google (requires GOOGLE_API_KEY + GOOGLE_SEARCH_ENGINE_ID)
    - bing (requires BING_API_KEY)
    
    Example:
        skill = WebSearchSkill()
        output = skill.execute(
            WebSearchInput(query="Düsseldorf meteorite", max_results=5),
            SkillContext()
        )
        # output.urls can be passed directly to fetch_web_content
    """
    
    name: ClassVar[str] = "web_search"
    description: ClassVar[str] = "Search the web for URLs matching a query"
    input_schema: ClassVar[type[WebSearchInput]] = WebSearchInput
    output_schema: ClassVar[type[WebSearchOutput]] = WebSearchOutput
    requires_llm: ClassVar[bool] = False
    
    def execute(self, input: WebSearchInput, ctx: SkillContext) -> WebSearchOutput:
        """Execute web search and return URLs.
        
        Args:
            input: Search query and parameters
            ctx: Skill context (unused for this skill)
        
        Returns:
            WebSearchOutput with urls list for pipeline chaining
        """
        engine = self._select_engine(input.search_engine)
        
        try:
            results = engine(
                query=input.query,
                max_results=input.max_results,
                region=input.region,
                safe_search=input.safe_search,
            )
            
            return WebSearchOutput(
                success=True,
                summary=f"Found {len(results)} results for '{input.query}'",
                urls=[r.url for r in results],
                results=results,
                search_query=input.query,
                search_engine=input.search_engine,
                total_results=len(results),
            )
            
        except Exception as e:
            return WebSearchOutput(
                success=False,
                summary=f"Search failed: {e}",
                urls=[],
                results=[],
                search_query=input.query,
                search_engine=input.search_engine,
                total_results=0,
            )
    
    def _select_engine(self, preference: str):
        """Select search engine based on preference and available API keys."""
        # Implementation selects based on env vars and preference
        ...
```

---

## Updated Playbook Definition

```python
# src/ag/playbooks/research_v0.py

RESEARCH_V0 = Playbook(
    playbook_version="0.1",
    name="research_v0",
    version="1.1.0",  # Bumped for web_search addition
    description="Research pipeline: load → search → fetch → synthesize → emit",
    reasoning_modes=[ReasoningMode.DIRECT],
    budgets=Budgets(
        max_steps=10,
        max_tokens=None,
        max_duration_seconds=300,
    ),
    steps=[
        # Step 0: Load local documents (keep AF-0074 behavior)
        PlaybookStep(
            step_id="step_0",
            name="load_local",
            step_type=PlaybookStepType.SKILL,
            skill_name="load_documents",
            description="Load local reference documents from workspace/inputs",
            required=False,
            retry_count=0,
            parameters={
                "file_patterns": ["*.md", "*.txt", "*.pdf"],
                "max_files": 10,
            },
        ),
        # Step 1: Web search (NEW - adds autonomous URL discovery)
        PlaybookStep(
            step_id="step_1",
            name="search_web",
            step_type=PlaybookStepType.SKILL,
            skill_name="web_search",
            description="Search web for URLs relevant to research query",
            required=False,  # Optional if user already provides urls.txt
            retry_count=1,
            parameters={
                # Optional explicit mapping; query also falls back from prompt
                "query": "",
                "max_results": 5,
                "search_engine": "duckduckgo",  # Free default
            },
        ),
        # Step 2: Fetch content from URLs
        PlaybookStep(
            step_id="step_2",
            name="fetch_web",
            step_type=PlaybookStepType.SKILL,
            skill_name="fetch_web_content",
            description="Fetch content from discovered URLs",
            required=False,  # Optional - supports no-web/local-only runs
            retry_count=1,
            parameters={
                "timeout_seconds": 30,
                "max_content_length": 50000,
            },
        ),
        # Step 3: Synthesize research report
        PlaybookStep(
            step_id="step_3",
            name="synthesize",
            step_type=PlaybookStepType.SKILL,
            skill_name="synthesize_research",
            description="Synthesize research report from all sources",
            required=True,
            retry_count=1,
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
        "af_item": "AF-0080",
        "pipeline": "load → search → fetch → synthesize → emit",
        "compatibility": "urls.txt fallback remains supported",
    },
)
```

---

## Acceptance Criteria (Definition of Done)

### Skill Implementation
- [ ] `WebSearchSkill` class in `src/ag/skills/web_search.py`
- [ ] `WebSearchInput` and `WebSearchOutput` schemas with Pydantic validation  
- [ ] DuckDuckGo search implementation (primary, free)
- [ ] Serper API implementation (optional, via env var)
- [ ] Graceful error handling (returns empty results, not exceptions)
- [ ] Output `urls` field chains correctly to `fetch_web_content`

### Registry & Playbook
- [ ] `web_search` registered in skill registry
- [ ] `research_v0` playbook updated with `web_search` after `load_documents` (no regression of local-doc support)
- [ ] Pipeline data flow verified (web_search.urls → fetch_web_content.urls)

### Testing
- [ ] Unit tests for schema validation
- [ ] Unit tests for each search engine backend
- [ ] Integration test for full pipeline (with mocked search API)
- [ ] E2E test with real DuckDuckGo (marked slow/optional)
- [ ] Coverage thresholds maintained

### Documentation
- [ ] SCHEMA_INVENTORY.md updated with new schemas
- [ ] CONTRACT_INVENTORY.md cross-reference updated to mention conformance to existing `Skill` protocol (no new protocol needed)
- [ ] Docstrings complete per skill conventions

### CI
- [ ] `ruff check src tests` passes
- [ ] `ruff format --check src tests` passes
- [ ] `pytest -W error` passes
- [ ] Coverage thresholds met

---

## Dependencies

### Python Packages (New)

```toml
# pyproject.toml
dependencies = [
    # ... existing ...
    "httpx>=0.27.0",             # Required by fetch_web_content for E2E pipeline
    "duckduckgo-search>=6.0.0",  # Free web search
]

[project.optional-dependencies]
search = [
    "httpx>=0.27.0",
    "duckduckgo-search>=6.0.0",
]
```

### Environment Variables (Optional)

```bash
# For production-quality results (optional)
SERPER_API_KEY="..."      # serper.dev API key
GOOGLE_API_KEY="..."      # Google Custom Search
GOOGLE_SEARCH_ENGINE_ID="..."
BING_API_KEY="..."        # Azure Bing Search
```

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| DuckDuckGo blocking/breaking | Medium | High | Fallback to Serper; document as "experimental" |
| Search results low quality | Low | Medium | Allow engine selection; future: LLM query refinement |
| Rate limiting | Low | Medium | Graceful failure; configurable delays |
| API costs (paid engines) | Low | Low | DuckDuckGo default is free |

---

## Future Enhancements (Out of Scope for v1)

1. **LLM Query Refinement** — Use LLM to improve search query before searching
2. **Result Ranking** — LLM-based relevance scoring of results
3. **Caching** — Cache search results to reduce API calls
4. **Multi-Engine Aggregation** — Search multiple engines, dedupe results
5. **Domain Filtering** — Allow/block specific domains
6. **News Search** — Dedicated news search mode

---

## Example Usage

### CLI

```bash
# Basic research (uses DuckDuckGo)
ag run --playbook research_v0 --workspace my_research "What is the Düsseldorf meteorite?"

# With Serper API (higher quality)
export SERPER_API_KEY="..."
ag run --playbook research_v0 --workspace my_research "History of German meteorites"
```

### Expected Output

```
[Step 0/5] load_local: Loaded 2 local reference documents

[Step 1/5] search_web: Found 5 results for "Düsseldorf meteorite"
  → https://en.wikipedia.org/wiki/Düsseldorf_meteorite
  → https://www.lpi.usra.edu/meteor/metbull.php?code=7745
  → https://www.mindat.org/loc-282461.html
  → ...

[Step 2/5] fetch_web: Fetched 5/5 URLs (2 truncated)

[Step 3/5] synthesize: Generated research report (2847 words, 7 sources)

[Step 4/5] emit: Saved artifact: research_report.md

✓ Run complete: research_report.md
```

---

## Implementation Notes

### File Changes

| File | Change |
|------|--------|
| `src/ag/skills/web_search.py` | **NEW** — Skill implementation |
| `src/ag/skills/__init__.py` | Export `WebSearchSkill` |
| `src/ag/skills/registry.py` | Register `web_search` skill |
| `src/ag/playbooks/research_v0.py` | Update pipeline to `load -> search -> fetch -> synthesize -> emit` |
| `pyproject.toml` | Add `duckduckgo-search` dependency |
| `docs/dev/additional/SCHEMA_INVENTORY.md` | Add new schemas |
| `docs/dev/additional/CONTRACT_INVENTORY.md` | Add note/cross-reference for existing Skill protocol conformance |
| `tests/test_web_search.py` | **NEW** — Unit tests |
| `tests/test_research_pipeline.py` | Integration tests |

### Key Implementation Details

1. **`urls` field naming is critical** — Must match `FetchWebContentInput.urls` for pipeline chaining
2. **DuckDuckGo as default** — No config needed for basic functionality
3. **Graceful degradation** — Always return `WebSearchOutput`, never raise
4. **Region handling** — Default "wt-wt" (worldwide), allow localization

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF0080
- **PR:** #<number>
- **Author:** 
- **Date:** 
- **Branch:** feat/web-search-skill
- **Risk level:** P1
- **Runtime mode used for verification:** llm

---

## 2) Acceptance criteria verification

_To be filled upon completion_

---

## 3) What changed (file-level)

_To be filled upon completion_

---

## 4) Architecture alignment (mandatory)

**Layering:** Skill layer only — no changes to core runtime or adapters

**Compliance:**
- Skills = Capabilities: ✓ Web search is a distinct API capability
- Single Responsibility: ✓ Search only; fetch handled separately
- Schema-Bounded: ✓ Strict Pydantic I/O
- Pipeline Compatible: ✓ Output `urls` matches `fetch_web_content` input
