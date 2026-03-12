# BACKLOG ITEM — AF0094 — trace_full_io_enrichment
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
- **ID:** AF0094
- **Type:** Implementation
- **Status:** PROPOSED
- **Priority:** P3
- **Area:** Core Runtime / Trace
- **Owner:** TBD
- **Target sprint:** Sprint 11+
- **Depends on:** AF-0090 (artifact evidence deepdive — Phase 1 & 3 DONE)

---

## Context

AF-0090 Phase 2 was deferred from Sprint 10. The original scope included:

1. Record full step input/output in trace.json (not just summaries)
2. Add `input_data` and `output_data` fields to Step model (optional, alongside summaries)
3. Categorize artifacts: `ArtifactCategory.RESULT` for deliverables, `.DATA` for intermediates
4. Document artifact lifecycle (skill output → trace → storage → CLI display)

Phase 1 and Phase 3 of AF-0090 are complete:
- ✅ artifact_type now matches actual file format
- ✅ Artifacts stored in `runs/<id>/artifacts/` directory
- ✅ Integration tests verify artifact metadata truthfulness

This AF captures the remaining trace enrichment work.

---

## Problem

### 1. Trace lacks full step I/O
- `input_summary` and `output_summary` are lossy truncations (~50 chars)
- No way to reconstruct what a skill actually received or produced
- Debugging and auditing require full inputs/outputs

### 2. Artifact lifecycle not documented
- No clear documentation of path: skill output → trace → storage → CLI

### 3. Artifact categorization incomplete
- `ArtifactCategory` enum exists but not used consistently
- No automatic inference of result vs intermediate artifacts

---

## Goal

Enrich trace.json with full step I/O data for debugging and audit:

1. Add optional `input_data` and `output_data` fields to Step model
2. Keep existing summaries for display; full data for debug/audit
3. Document artifact lifecycle in ARCHITECTURE.md or dedicated doc
4. Improve artifact categorization (RESULT vs DATA vs INTERMEDIATE)

---

## Non-goals

- Changing trace format version (keep backwards compatible)
- Sensitive data redaction (separate AF)
- Trace compression or optimization
- CLI changes (existing `ag runs show --json` already exposes trace)

---

## Scope

### Task 1: Step Model Enhancement
1. Add `input_data: dict[str, Any] | None` to Step model in run_trace.py
2. Add `output_data: dict[str, Any] | None` to Step model
3. Make fields optional with None default for backwards compatibility
4. Update runtime.py to populate these fields during execution

### Task 2: Artifact Lifecycle Documentation
1. Document full path: skill output → trace → storage → CLI
2. Add sequence diagram or flowchart to ARCHITECTURE.md
3. Include example trace.json with annotated fields

### Task 3: Artifact Categorization
1. Use ArtifactCategory consistently in emit_result skill
2. Add category inference based on step position (final → RESULT, intermediate → DATA)
3. Update artifact display in CLI to show category

---

## Key Files

| File | Role |
|------|------|
| `src/ag/core/run_trace.py` | Step model, Artifact model |
| `src/ag/core/runtime.py` | Step execution, trace building |
| `docs/ARCHITECTURE.md` | System documentation |
| `src/ag/skills/emit_result.py` | Artifact creation |

---

## Acceptance criteria (Definition of Done)

- [ ] Step model has optional `input_data` and `output_data` fields
- [ ] Runtime populates full I/O data during execution
- [ ] Existing tests pass (backwards compatible)
- [ ] Artifact lifecycle documented in ARCHITECTURE.md
- [ ] `ruff check src tests` passes
- [ ] `pytest -W error` passes

---

## Risks

| Risk | Mitigation |
|------|------------|
| Large traces with full I/O | Fields optional; enable via config flag if needed |
| Sensitive data in traces | Separate AF for redaction; document risk |
| Schema version compatibility | Optional fields; no breaking changes |

---

## Related Items

- **AF-0090:** Artifact evidence deepdive (parent — Phase 1 & 3 DONE)
- **AF-0057:** Playbook artifacts in trace (prerequisite — DONE)
- **AF-0089:** Report output format (related — DONE)
