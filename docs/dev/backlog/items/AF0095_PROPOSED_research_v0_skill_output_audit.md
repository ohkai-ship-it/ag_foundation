# BACKLOG ITEM — AF0095 — research_v0_skill_output_audit
# Version number: v0.1

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
- **ID:** AF0095
- **Type:** Investigation / Bug Fix
- **Status:** PROPOSED
- **Priority:** P2
- **Area:** Skills / Playbooks / research_v0
- **Owner:** TBD
- **Target sprint:** TBD
- **Depends on:** None

---

## Context

The `research_v0` playbook orchestrates a 5-step research pipeline:
1. `load_documents` — Load local reference docs (optional)
2. `web_search` — Discover URLs from query (optional)
3. `fetch_web_content` — Fetch content from URLs (optional)
4. `synthesize_research` — LLM-powered synthesis (required)
5. `emit_result` — Save artifact (required)

Observed discrepancies between skill behavior and CLI reporting suggest potential issues in:
- Skill output schemas vs actual returned data
- Summary/output truncation masking errors
- Step success reporting not matching actual outcomes
- Data flow between skills (output of one → input of next)

---

## Problem

### 1. Behavior vs Reporting Discrepancies
- CLI reports may show "success" when skill behavior is partially correct
- Output summaries may not reflect actual skill execution state
- Error conditions may be masked by summary truncation

### 2. Skill Output Verification Gaps
- No systematic verification of skill outputs against their schemas
- Intermediate outputs between pipeline steps not easily inspectable
- `output_summary` is lossy — cannot reconstruct full picture

### 3. Data Flow Integrity
- research_v0 passes data between skills implicitly
- `web_search` → `fetch_web_content` URL handoff unclear
- `fetch_web_content` → `synthesize_research` content handoff unclear

---

## Scope

### Investigation Phase
1. **Audit each skill in research_v0:**
   - `web_search` — Verify search results match expected schema
   - `fetch_web_content` — Verify fetched content matches expected schema
   - `synthesize_research` — Verify synthesis output matches expected schema
   - `emit_result` — Verify artifact storage matches expectations

2. **Trace inspection:**
   - Run research_v0 with logging enabled
   - Capture full input/output at each step
   - Compare trace data with CLI display
   - Document any discrepancies

3. **Schema compliance:**
   - Verify each skill's output matches its `output_schema`
   - Check for undocumented fields or missing required fields
   - Validate Pydantic model dumps

### Fix Phase (if issues found)
4. **Fix identified discrepancies:**
   - Correct skill output schemas
   - Fix output summary generation
   - Ensure CLI displays truthful status

5. **Add regression tests:**
   - Test each skill's output schema compliance
   - Test data flow between steps
   - Test CLI output matches trace data

---

## Test Commands

```bash
# Run research_v0 playbook
ag run --playbook research_v0 "What is the capital of France?"

# Run individual skills for isolated testing
ag run --skill web_search "capital of France"
ag run --skill fetch_web_content --urls "https://example.com"
ag run --skill synthesize_research --sources "test content"

# Inspect trace
ag runs inspect <run-id> --json

# Run with debug logging
AG_LOG_LEVEL=DEBUG ag run --playbook research_v0 "test query"
```

---

## Acceptance Criteria

- [ ] Each skill in research_v0 audited for output correctness
- [ ] Identified discrepancies documented
- [ ] Fixes implemented for any behavior/reporting mismatches
- [ ] Trace data matches CLI display
- [ ] Regression tests prevent future discrepancies
- [ ] SCHEMA_INVENTORY.md updated if schemas change

---

## Skills to Audit

| Skill | Module | Schema | Priority |
|-------|--------|--------|----------|
| `web_search` | `ag.skills.web_search` | `WebSearchOutput` | High |
| `fetch_web_content` | `ag.skills.fetch_web_content` | `FetchWebContentOutput` | High |
| `synthesize_research` | `ag.skills.synthesize_research` | `SynthesizeResearchOutput` | High |
| `load_documents` | `ag.skills.load_documents` | `LoadDocumentsOutput` | Medium |
| `emit_result` | `ag.skills.emit_result` | `EmitResultOutput` | Medium |

---

## Notes

- May overlap with AF0094 (trace_full_io_enrichment) — full I/O capture would help this audit
- Consider adding verbose/debug mode for skill execution
- Zero skill (`zero_skill`) provides minimal baseline for comparison
