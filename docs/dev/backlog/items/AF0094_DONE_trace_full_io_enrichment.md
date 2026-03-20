# BACKLOG ITEM — AF0094 — trace_full_io_enrichment
# Version number: v0.2

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - CI discipline (ruff + pytest -W error + coverage)
> - INDEX update rule (status ↔ filename integrity)

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0094
- **Type:** Implementation
- **Status:** READY
- **Priority:** P2 (upgraded based on user feedback)
- **Area:** Core Runtime / Trace
- **Owner:** TBD
- **Target sprint:** Sprint 11
- **Depends on:** AF-0090 (artifact evidence deepdive — Phase 1 & 3 DONE)

---

## Context

AF-0090 Phase 2 was deferred from Sprint 10. User feedback on actual trace.json reveals critical gaps:

**Example trace gaps (real user feedback):**
```json
{
  "llm": {
    "call_count": 0,           // NOT TRACKED - should show actual LLM calls
    "total_tokens": null,      // NOT TRACKED - should show token usage
    "input_tokens": null,
    "output_tokens": null
  },
  "steps": [{
    "skill_name": "web_search",
    "output_summary": "Found 5 results...",  // LOSSY - want full URLs
    "artifacts": []                          // EMPTY - want searchResults.json
  }, {
    "skill_name": "fetch_web_content",
    "output_summary": "Fetched 2/5 URLs",    // WHY? - want failed_urls list
    "artifacts": []                          // EMPTY - want fetchedContent.json
  }]
}
```

---

## Problem

### 1. LLM Usage Not Tracked
- `llm.call_count` always 0 even when LLM was called
- `llm.total_tokens`, `input_tokens`, `output_tokens` always null
- No visibility into LLM costs or usage patterns

### 2. Only Summaries, No Full Step Output
- `output_summary` truncated (e.g., "Found 5 results for..." — which URLs?)
- `input_summary` truncated (e.g., "prompt=Hauptstadt von..." — full input?)
- Cannot reconstruct what skills actually processed

### 3. Intermediate Steps Have No Artifacts
- Only `emit_result` creates artifacts
- `web_search` results not persisted → can't see which URLs were found
- `fetch_web_content` results not persisted → can't see which URLs failed and why
- `synthesize_research` output not persisted → only see final report

### 4. Failure Details Hidden
- "Fetched 2/5 URLs" — which 3 failed? Why?
- `error` field null even when partial failures occur
- `failed_urls` and error messages not surfaced in trace

---

## Goal

Make trace.json a complete audit record:

1. **Track LLM usage** — Wire up provider to report call counts and tokens
2. **Store full step I/O** — Add `input_data` and `output_data` fields
3. **Intermediate artifacts** — Each skill saves its output as artifact
4. **Surface failure details** — Include `failed_urls`, partial success info

---

## Non-goals

- Changing trace format version (keep backwards compatible)
- Sensitive data redaction (separate AF)
- Trace compression or optimization

---

## Scope

### Task 1: LLM Usage Tracking
1. Update `LLMProvider.chat()` to return token counts in `ChatResponse`
2. Track cumulative call_count and tokens in runtime
3. Populate `llm.call_count`, `total_tokens`, `input/output_tokens` in trace

**Files:** `src/ag/providers/base.py`, `src/ag/providers/openai.py`, `src/ag/core/runtime.py`

### Task 2: Full Step I/O in Trace
1. Add `input_data: dict[str, Any] | None` to Step model
2. Add `output_data: dict[str, Any] | None` to Step model
3. Runtime populates these during execution
4. Keep summaries for display; full data for debug

**Files:** `src/ag/core/run_trace.py`, `src/ag/core/runtime.py`

### Task 3: Intermediate Step Artifacts
1. Runtime saves each skill's output as `{step_number}_{skill_name}_output.json`
2. Link artifact IDs in step's `artifacts` array
3. Users can inspect via `ag artifacts show -r <run> <artifact-id>`

**Files:** `src/ag/core/runtime.py`

### Task 4: Surface Failure Details
1. Ensure `failed_urls` from fetch_web_content appears in step output_data
2. Log partial success with details (which succeeded, which failed, why)
3. Consider adding `partial_success` boolean to Step model

**Files:** `src/ag/core/run_trace.py`, `src/ag/skills/fetch_web_content.py`

---

## Expected Result

After implementation, trace.json should look like:
```json
{
  "llm": {
    "call_count": 1,
    "total_tokens": 4523,
    "input_tokens": 3200,
    "output_tokens": 1323
  },
  "steps": [{
    "skill_name": "web_search",
    "output_summary": "Found 5 results for 'query' using duckduckgo",
    "output_data": {
      "urls": ["https://...", "https://...", ...],
      "results": [...],
      "total_results": 5
    },
    "artifacts": ["run-123-step-1-web_search_output"]
  }, {
    "skill_name": "fetch_web_content",
    "output_summary": "Fetched 2/5 URLs",
    "output_data": {
      "documents": [...],
      "failed_urls": ["https://blocked.com", "https://timeout.com", "https://404.com"],
      "total_fetched": 2,
      "total_failed": 3
    },
    "artifacts": ["run-123-step-2-fetch_web_content_output"]
  }]
}
```

---

## Key Files

| File | Role |
|------|------|
| `src/ag/core/run_trace.py` | Step model, LLMExecution model |
| `src/ag/core/runtime.py` | Step execution, trace building, artifact saving |
| `src/ag/providers/base.py` | ChatResponse with token counts |
| `src/ag/providers/openai.py` | Extract usage from OpenAI response |
| `src/ag/skills/fetch_web_content.py` | Surface failed_urls in output |

---

## Acceptance Criteria

- [ ] `llm.call_count` reflects actual LLM calls made
- [ ] `llm.total_tokens` populated from provider responses
- [ ] Step has `input_data` and `output_data` optional fields
- [ ] Each skill step creates an artifact with full output
- [ ] `failed_urls` visible in fetch_web_content step output
- [ ] Existing tests pass (backwards compatible)
- [ ] `ruff check src tests` passes
- [ ] `pytest -W error` passes

---

## Risks

| Risk | Mitigation |
|------|------------|
| Large traces with full I/O | Fields optional; config flag to disable |
| Sensitive data in traces | Separate AF for redaction; document risk |
| Storage bloat from artifacts | Add artifact size limits; cleanup policy |

---

## Related Items

- **AF-0090:** Artifact evidence deepdive (parent — Phase 1 & 3 DONE)
- **AF-0057:** Playbook artifacts in trace (prerequisite — DONE)
- **AF-0095:** research_v0 skill output audit (identified these gaps)
