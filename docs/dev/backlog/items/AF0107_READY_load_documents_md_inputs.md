# BACKLOG ITEM — AF0107 — load_documents_md_inputs
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
- **ID:** AF0107
- **Type:** Feature
- **Status:** READY
- **Priority:** P1
- **Area:** Skills / Storage
- **Owner:** TBD
- **Target sprint:** Sprint 12 — autonomy_boundaries
- **Depends on:** —

---

## Problem
`load_documents` can fail to discover Markdown files under `inputs/` in practical planner-generated flows, especially when non-recursive patterns are emitted.

---

## Goal
Make Markdown loading from `inputs/` reliable and explicit:
- default behavior must include recursive Markdown discovery in `inputs/`
- planner-emitted patterns must not break MD discovery
- failure messages must clearly explain pattern/base path behavior

---

## Non-goals
- Full file-type auto-classification
- OCR or binary parsing expansion

---

## Acceptance criteria (Definition of Done)
- [ ] `load_documents` consistently loads `.md` files from `inputs/`
- [ ] Pattern handling is deterministic for recursive and non-recursive globs
- [ ] Tests cover `inputs/` present, missing, and mixed-pattern scenarios
- [ ] CI passes (`ruff`, `pytest -W error`)

---

## Implementation notes
- Primary files: `src/ag/skills/load_documents.py`, `tests/test_summarize_skills.py`, `tests/test_research_skills.py`
- Keep workspace isolation and trace truthfulness unchanged

---

## Risks
| Risk | Mitigation |
|------|------------|
| Pattern behavior confusion | Add explicit error/help text + tests |
| Regressions in non-MD flows | Add mixed-file regression tests |

---

# Completion section (fill when done)

_To be filled upon completion_
