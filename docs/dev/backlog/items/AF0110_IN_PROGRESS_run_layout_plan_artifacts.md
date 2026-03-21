# BACKLOG ITEM — AF0110 — run_layout_plan_artifacts
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
- **ID:** AF0110
- **Type:** Refactor
- **Status:** IN_PROGRESS
- **Priority:** P1
- **Area:** Runtime / Storage / CLI
- **Owner:** TBD
- **Target sprint:** Sprint 12 — autonomy_boundaries
- **Depends on:** AF-0109

---

## Problem
Run output layout and plan persistence are fragmented:
- deprecated `-result_result.md` style outputs
- workspace-level `/plans` storage separate from run artifacts

This makes investigation harder and breaks the one-run-one-folder mental model.

---

## Goal
Adopt canonical run-centered layout with no backward compatibility:
- `runs/<run_id>/trace.json`
- `runs/<run_id>/result.md`
- `runs/<run_id>/artifacts/*` (including plan file)

Also remove deprecated workspace-level `/plans` persistence and associated code paths.

---

## Non-goals
- Migration tooling for historic runs
- Compatibility fallback for old plan locations

---

## Acceptance criteria (Definition of Done)
- [ ] New runs produce canonical folder structure
- [ ] No new `-result_result.md` files are generated
- [ ] Plan file is stored under `runs/<run_id>/artifacts/`
- [ ] Workspace-level `/plans` path is deprecated and unused for new runs
- [ ] CLI plan/run flows resolve plan location from run artifacts
- [ ] Tests updated for path/layout changes
- [ ] CI passes (`ruff`, `pytest -W error`)

---

## Implementation notes
- Primary files: `src/ag/core/runtime.py`, `src/ag/storage/workspace.py`, `src/ag/storage/plan_store.py`, `src/ag/core/execution_plan.py`, `src/ag/cli/main.py`, tests under `tests/test_plan.py`, `tests/test_artifacts.py`, `tests/test_storage.py`
- Keep trace-backed UX labels truthful

---

## Risks
| Risk | Mitigation |
|------|------------|
| Path regressions in CLI commands | Add end-to-end plan/run path tests |
| Artifact naming collisions | Enforce deterministic naming strategy |

---

# Completion section (fill when done)

_To be filled upon completion_
