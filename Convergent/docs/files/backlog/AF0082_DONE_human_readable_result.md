# BACKLOG ITEM — AF0082 — human_readable_result
# Version number: v0.2

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0082
- **Type:** Feature
- **Status:** DONE
- **Priority:** P2
- **Area:** Core Runtime / CLI
- **Owner:** Jacob
- **Target sprint:** Sprint 10
- **Depends on:** AF-0089 (report output format — DONE Sprint 09)

---

## Problem

AF-0089 (Sprint 09) fixed the fundamental issue: `report.md` now outputs
proper markdown instead of raw JSON. However, the report still lacks
structured metadata and polish that would make it a professional,
shareable document:

### Current State (Post AF-0089)
1. **`report.md`** — Proper markdown with synthesized content ✅
2. **Missing:** No metadata header (duration, model, run ID, playbook)
3. **Missing:** No structured sources table with clickable links
4. **Missing:** No execution details table (step/skill/duration)
5. **Missing:** No structural tests verifying report format

### What AF-0089 Fixed
- report.md outputs markdown instead of JSON ✅
- MIME type correctly set for .md files ✅
- Extension-based format selection works ✅

### What Remains (This AF)
- Metadata header with execution context
- Sources table with clickable links
- Execution details table
- Structure validation tests

---

## Goal

Enhance `report.md` from basic markdown to a **polished, structured report**
with metadata header, sources table, and execution details that users can
share directly as a professional document.

---

## Non-goals

- Interactive report (HTML/web)
- PDF export
- Custom templates (future enhancement)
- Changing trace.json format
- Changing the basic markdown output (AF-0089 already handled)

---

## Proposed Output Format

```markdown
# Research Report: <query snippet>

**Generated:** 2026-03-10 14:11:02 UTC
**Duration:** 39.5 seconds
**Model:** gpt-4o-mini
**Playbook:** research_v0@1.1.0

---

## Summary

<actual report content from synthesize_research — already in markdown>

---

## Key Findings

- Finding 1
- Finding 2

---

## Sources

| # | Source | URL |
|---|--------|-----|
| 1 | AccuWeather | [accuweather.com/...](https://...) |
| 2 | BBC Weather | [bbc.com/weather/...](https://...) |

---

## Execution Details

| Step | Skill | Duration | Output |
|------|-------|----------|--------|
| 0 | load_documents | 2ms | Loaded 5 documents |
| 1 | web_search | 830ms | Found 5 results |
| 2 | fetch_web_content | 3,250ms | Fetched 5/5 URLs |
| 3 | synthesize_research | 35,432ms | Synthesized from 5 sources |
| 4 | emit_result | 2ms | Artifact stored |

**Total Duration:** 39,518ms
**Run ID:** `d95b9f81-...`
```

---

## Acceptance criteria (Definition of Done)

- [x] Report includes metadata header (generated, duration, model, playbook version)
- [x] Report includes sources table with clickable markdown links
- [x] Report includes execution details table (step, skill, duration, output)
- [x] Report includes run ID and total duration footer
- [x] Unicode characters render correctly (verify BUG-0014 fix holds)
- [x] Tests verify report structure (header present, sources table present, execution table present)
- [x] `ruff check src tests` passes
- [x] `pytest -W error` passes

---

## Implementation Notes

### Recommended Approach: Enhance `emit_result` skill

The `_format_markdown()` method added by AF-0089 should be extended to:
1. Accept trace metadata (duration, model, run ID) from orchestrator context
2. Extract sources from skill output fields
3. Build structured sections

### Data Sources for Report

| Field | Source |
|-------|--------|
| Query | `trace.steps[0].input_summary` or task_spec |
| Summary | `emit_result` output → `document_summary` / `report` |
| Key Findings | `emit_result` output → `key_points` / `key_findings` |
| Sources | `emit_result` output → `sources` / `sources_used` |
| Duration | `trace.duration_ms` |
| Model | `trace.llm.model` |
| Step details | `trace.steps[*]` |

---

## Completion Summary

**Completed:** Sprint 10

### Implementation

1. **Extended SkillContext** (`src/ag/skills/base.py`):
   - Added `trace_metadata: dict[str, Any]` optional field
   - Allows runtime to pass execution context to skills

2. **Runtime metadata population** (`src/ag/core/runtime.py`):
   - Populates `trace_metadata` when building SkillContext
   - Includes: elapsed_ms, model, playbook_name, playbook_version, steps_summary

3. **Enhanced emit_result** (`src/ag/skills/emit_result.py`):
   - `_format_markdown()` now produces polished reports with:
     - Visible metadata header (generated timestamp, duration, model, playbook)
     - Sources as clickable markdown table with URL detection
     - Execution details table (step, skill, duration, output)
     - Run ID footer

### Tests Added

- `test_summarize_skills.py::test_emit_result_metadata_header` — verifies metadata header rendering
- `test_summarize_skills.py::test_emit_result_execution_table` — verifies execution details table

### Metrics

- Tests: 565 passing
- Ruff: Clean

## Risks

| Risk | Mitigation |
|------|------------|
| Schema changes break formatting | Use schema bridging pattern |
| Large reports slow generation | Limit to summary + first N findings |
| Report format varies by playbook | Define minimal common structure |

---

## Related Items

- **AF-0089:** Report output format (DONE — prerequisite, fixed markdown vs JSON)
- **AF-0057:** Playbook artifacts in trace (DONE — artifact content in trace)
- **AF-0090:** Artifact evidence deepdive (related — artifact metadata truthfulness)
- **AF-0081:** Inventory sync discipline (schema consistency)
- **BUG-0014:** Trace summary encoding degradation (FIXED — verify unicode holds)

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF0082
- **PR:** #<number>
- **Author:** <name>
- **Date:** YYYY-MM-DD
- **Branch:** feat/human-readable-result
- **Risk level:** P2
- **Runtime mode used for verification:** llm
