# BACKLOG ITEM — AF0108 — unify_summarization_skill
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
- **ID:** AF0108
- **Type:** Refactor
- **Status:** DONE
- **Priority:** P1
- **Area:** Skills / Playbooks
- **Owner:** TBD
- **Target sprint:** Sprint 12 — autonomy_boundaries
- **Depends on:** AF-0107

---

## Problem
`summarize_docs` and `synthesize_research` overlap heavily but produce divergent output contracts. This creates inconsistent plan behavior and unnecessary complexity.

---

## Goal
Unify summarization into a single skill:
- Keep `synthesize_research` as canonical summarization capability
- Remove `summarize_docs` from registry/playbook execution paths
- Normalize output contract expected by downstream consumers

---

## Non-goals
- Adding new analysis modes
- Backward compatibility aliases for removed skill

---

## Acceptance criteria (Definition of Done)
- [ ] `summarize_docs` is removed from runtime skill selection/registry
- [ ] Playbooks and planner flows use `synthesize_research` only
- [ ] Tests updated for single-skill summarization path
- [ ] Docs updated to reflect unified capability
- [ ] CI passes (`ruff`, `pytest -W error`)

---

## Implementation notes
- Primary files: `src/ag/skills/synthesize_research.py`, `src/ag/skills/summarize_docs.py`, `src/ag/skills/registry.py`, `src/ag/playbooks/*.py`
- Update tests and docs together to avoid drift

---

## Risks
| Risk | Mitigation |
|------|------------|
| Planner still emitting removed skill | Add strict validation + planner tests |
| Output field mismatch in emit step | Add schema normalization tests |

---

# Completion section (fill when done)

_To be filled upon completion_
