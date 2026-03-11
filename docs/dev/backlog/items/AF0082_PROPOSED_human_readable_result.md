# BACKLOG ITEM — AF0082 — human_readable_result
# Version number: v0.1

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
- **Status:** PROPOSED
- **Priority:** P2
- **Area:** Core Runtime / CLI
- **Owner:** TBD
- **Target sprint:** TBD
- **Depends on:** AF-0057 (playbook artifacts in trace)

---

## Problem

Current run output artifacts are not user-friendly:

### Current State
1. **`research_report.md`** — Actually JSON, not markdown (misleading extension)
2. **`artifacts/*-result_result.md`** — Minimal execution log, no content
3. **`trace.json`** — Machine-readable, not for end users

Users must parse JSON to see their research results. There's no polished, 
readable output they can share or review directly.

### Evidence
Run `d95b9f81-33af-45c0-b071-65294b27901d` for research_v0:
- `research_report.md` contains raw JSON with escaped unicode
- No formatted markdown with clickable source links
- Report buried in JSON `summary` field

---

## Goal

Generate a **polished, human-readable markdown report** that users can:
1. Read directly in any markdown viewer
2. Share with stakeholders
3. Use as-is without post-processing

---

## Non-goals

- Interactive report (HTML/web)
- PDF export
- Custom templates (future enhancement)
- Changing trace.json format

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

<actual report content from synthesize_research — properly formatted markdown>

---

## Key Findings

- Finding 1
- Finding 2
- Finding 3

---

## Sources

| # | Source | URL |
|---|--------|-----|
| 1 | AccuWeather | [accuweather.com/...](https://www.accuweather.com/en/de/düsseldorf/...) |
| 2 | BBC Weather | [bbc.com/weather/...](https://www.bbc.com/weather/2934246) |
| 3 | Weather.com | [wetter.com/...](https://www.wetter.com/deutschland/duesseldorf/...) |

---

## Execution Details

| Step | Skill | Duration | Output |
|------|-------|----------|--------|
| 0 | load_documents | 2ms | Loaded 5 documents (78,788 bytes) |
| 1 | web_search | 830ms | Found 5 results |
| 2 | fetch_web_content | 3,250ms | Fetched 5/5 URLs |
| 3 | synthesize_research | 35,432ms | Synthesized from 5 sources |
| 4 | emit_result | 2ms | Artifact stored |

**Total Duration:** 39,518ms  
**Run ID:** `d95b9f81-33af-45c0-b071-65294b27901d`
```

---

## Acceptance criteria (Definition of Done)

- [ ] `ag run -p research_v0 ...` produces `report.md` with formatted content
- [ ] Report includes: header, summary, key findings, sources table, execution details
- [ ] Sources are clickable markdown links
- [ ] Unicode characters render correctly (ü, ö, etc.)
- [ ] Metadata from trace included (duration, model, run ID)
- [ ] Original JSON artifact still produced (for programmatic access)
- [ ] Tests verify report structure and content

---

## Implementation Notes

### Option A: Enhance `emit_result` skill
Add a `format` parameter:
```python
class EmitResultInput(SkillInput):
    format: Literal["json", "markdown"] = "json"
```

Pros: Self-contained, skill handles output format
Cons: Skill becomes complex, mixing concerns

### Option B: New `format_report` skill
Add pipeline step after emit_result:
```
synthesize_research → emit_result → format_report
```

Pros: Single responsibility, composable
Cons: Extra step, more artifacts

### Option C: Runtime post-processing (Recommended)
Enhance `_build_result_artifact()` in runtime.py:
- Read emit_result output
- Format as markdown
- Write alongside JSON artifact

Pros: No skill changes, consistent for all playbooks
Cons: Runtime knows about skill output shapes

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

### File Naming
- JSON: `<run_id>_data.json` (programmatic access)
- Markdown: `<run_id>_report.md` (human-readable)

Or playbook-specific:
- `research_report.json` + `research_report.md`
- `summary.json` + `summary.md`

---

## Risks

| Risk | Mitigation |
|------|------------|
| Schema changes break formatting | Use schema bridging pattern (see AF-0081) |
| Large reports slow generation | Limit to summary + first N findings |
| Report format varies by playbook | Define minimal common structure |

---

## Related Items

- **AF-0057:** Playbook artifacts in trace (dependency — need artifact content in trace)
- **AF-0054:** Citation model unification (source formatting)
- **AF-0081:** Inventory sync discipline (schema consistency)
- **BUG-0013:** research_v0 pipeline broken (revealed JSON-in-markdown issue)

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
