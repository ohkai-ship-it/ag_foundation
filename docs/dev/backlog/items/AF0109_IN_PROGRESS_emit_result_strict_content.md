# BACKLOG ITEM — AF0109 — emit_result_strict_content
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - 1 PR = 1 primary AF
> - INDEX update rule (status ↔ filename integrity)

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0109
- **Type:** Feature
- **Status:** IN_PROGRESS
- **Priority:** P1
- **Area:** Skills / Artifacts
- **Owner:** TBD
- **Target sprint:** Sprint 12 — autonomy_boundaries
- **Depends on:** AF-0108

---

## Problem
`emit_result` can write human-readable artifacts with empty or placeholder content (for example stub synthesis text), which violates output quality expectations.

---

## Goal
Enforce strict output validity in `emit_result`:
- fail hard when summary/report content is empty or placeholder
- do not write root human-readable output on invalid content
- emit clear traceable error explaining why output was rejected

---

## Non-goals
- Silent fallback generation
- Auto-healing by re-planning

---

## Acceptance criteria (Definition of Done)
- [ ] Placeholder/empty content is detected before write
- [ ] Invalid output path returns explicit skill failure
- [ ] No root human-readable file is written on invalid content
- [ ] Tests cover valid, empty, and placeholder content cases
- [ ] CI passes (`ruff`, `pytest -W error`)

---

## Implementation notes
- Primary files: `src/ag/skills/emit_result.py`, `tests/test_summarize_skills.py`, `tests/test_artifacts.py`
- Keep artifact metadata truthful in trace

---

## Risks
| Risk | Mitigation |
|------|------------|
| False positives in placeholder detection | Use explicit marker set + tests |
| New failure path surprises users | Improve CLI error messaging |

---

# Completion section (fill when done)

_To be filled upon completion_
