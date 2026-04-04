# AF-0130 — Drop Redundant Sprint Artifacts
# Version number: v0.2
# Created: 2026-04-04
# Started:
# Completed:
# Status: READY
# Priority: P1
# Area: Process / Docs
# Models:

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> **CI workflow (CRITICAL):**
> - **During AF development:** run targeted tests only
>   `pytest tests/test_documentation_drift.py -W error`
> - **Before commit (full gate):** run the complete CI gate
>   1. `ruff check src tests`
>   2. `ruff format --check src tests`
>   3. `pytest -W error`
>   4. `pytest --cov=src/ag --cov-report=term-missing`

---

## Metadata
- **ID:** AF-0130
- **Type:** Process
- **Status:** READY
- **Priority:** P1
- **Area:** Process / Docs
- **Owner:** Jacob
- **Target sprint:** Sprint 16 — governance_simplification
- **Phase:** 2 (no dependencies)

---

## Problem

`S##_PR_01.md` duplicates the GitHub PR body verbatim — no additional value. `S##_REVIEW_01.md`'s 46-item checklist duplicates checks already mandated by SPRINT_MANUAL §8 and §9. The deeper problem is that the current design merges *planning data* (goals, scope, AF list) with *outcomes data* (what shipped, review decision, cognitive health) into one mutating `S##_DESCRIPTION.md`. A mutating artifact is worse at both jobs: the plan is harder to use as a reference mid-sprint; the review harder to write at close because it shares space with stable planning content.

---

## Goal

- GitHub PR is the canonical PR artifact (no separate `S##_PR_01` file)
- **MECE split:** `S##_DESCRIPTION.md` is the *planning* artifact; new lightweight `S##_REVIEW.md` is the *outcomes* artifact
- `S##_DESCRIPTION.md` — written at kickoff, stable during sprint: goal, scope, AF list, implementation notes
- `S##_REVIEW.md` — written at sprint close: work items table, review decision, cognitive health, learnings
- Sprint folder contains: `S##_DESCRIPTION.md` + `S##_REVIEW.md` + `artifacts/`
- Review rigour preserved — same checks, cleaner separation

---

## Non-goals

- Touching any S01–S15 historical PR or review documents
- Changes to `src/`, `tests/`, or `scripts/`

---

## Acceptance Criteria
- [ ] `SPRINT_DESCRIPTION_TEMPLATE.md` is a pure planning artifact: metadata, goal, scope, start checklist, PR plan, work items, implementation notes — no close/review section
- [ ] `SPRINT_REVIEW_TEMPLATE.md` (new) exists with: work items table, review decision (ACCEPTED / ACCEPT WITH FOLLOW-UPS / REJECTED), rationale, follow-ups, PR link
- [ ] `SPRINT_REVIEW_TEMPLATE.md` includes Sprint Cognitive Health section (seven fields):
  - Collapse events (INCOMPLETE_IMPL follow-ups)
  - Drift events (AF spec revised mid-implementation)
  - Repair events
  - Agent-initiated HITL gates
  - Negative test coverage added
  - LLM avoidance events
  - Integration coverage (E2E result)
- [ ] `SPRINT_REVIEW_TEMPLATE.md` includes Learnings section (optional, 2–3 bullets)
- [ ] `SPRINT_PR_TEMPLATE.md` and old `REVIEW_TEMPLATE.md` moved to `docs/dev/sprints/templates/archived/`
- [ ] SPRINT_MANUAL §6–§8 updated — no references to S##_PR_01 or S##_REVIEW_01 creation
- [ ] SPRINT_MANUAL §8: sprint close ritual creates `S##_REVIEW.md`, fills it, then makes review decision
- [ ] SPRINT_MANUAL §8 includes review decision rules: ACCEPTED / ACCEPT WITH FOLLOW-UPS / REJECTED
- [ ] SPRINT_MANUAL §8 includes quickfix budget rule (30 min cumulative, human-overridable)
- [ ] Sprint 17 (first sprint under new rules) uses the new template pair (description + review)
- [ ] Docs impact checked: README / CLI_REFERENCE / ARCHITECTURE (updated or N/A)
- [ ] AI functionality check: N/A (no AI functionality)

---

## Implementation Notes

### SPRINT_DESCRIPTION_TEMPLATE.md — pure planning artifact

```
# S##_DESCRIPTION — <sprint_name>
# Version number: v1.3
# Status: PLANNED | DONE | REJECTED

## Metadata
- Sprint:, Name:, Dates:, Branch:, Owner:, Tech lead:, Implementer:, Models:

## Sprint Goal
One sentence, outcome-focused.

## Scope
- P0: AF####
- P1: AF####

## Sprint Start Checklist

## PR Plan

## Work Items
| Order | ID | Status | Title |

## Implementation Notes
(space for mid-sprint decisions and observations)
```

### SPRINT_REVIEW_TEMPLATE.md — new outcomes artifact

```
# S##_REVIEW — <sprint_name>
# Version number: v1.3

## Sprint Reference
- Sprint: S##, PR: #<number>

## Work Items
| ID | Title | Status | Notes |

## Review Decision
- **Decision:** ACCEPTED / ACCEPT WITH FOLLOW-UPS / REJECTED
- **Rationale:** (1–2 sentences)
- **Follow-ups:** (AF IDs, if any)
- **PR link:**

## Sprint Cognitive Health
- Collapse events (INCOMPLETE_IMPL follow-ups): [N]
- Drift events (AF spec revised mid-implementation): [N, list AF IDs]
- Repair events: [informal]
- Agent-initiated HITL gates: [G codes, or "none"]
- Negative test coverage added: [yes / no / partial]
- LLM avoidance events: [N, list AF IDs]
- Integration coverage: [pass / partial / fail — unit-level vs. component-boundary]

## Learnings (optional)
```

### Review function mapping
| Review function | Old home | New home |
|---|---|---|
| CI gate | REVIEW_01 checklist | SPRINT_MANUAL §8 (unchanged) |
| INDEX consistency | REVIEW_01 checklist | SPRINT_MANUAL §8 + gov.py check |
| Evidence verification | REVIEW_01 checklist | `S##_REVIEW.md` |
| Autonomy gate | REVIEW_01 checklist | SPRINT_MANUAL §9 (unchanged) |
| Decision record | REVIEW_01 summary | `S##_REVIEW.md` |
| Follow-up items | REVIEW_01 action items | Filed as new AF/BUG items |
| Cognitive health | (new) | `S##_REVIEW.md` |

---

## Files Touched
- `docs/dev/sprints/templates/SPRINT_DESCRIPTION_TEMPLATE.md` (simplify — remove close section, add Status field)
- `docs/dev/sprints/templates/SPRINT_REVIEW_TEMPLATE.md` (new)
- `docs/dev/sprints/templates/SPRINT_PR_TEMPLATE.md` (move to `archived/`)
- `docs/dev/sprints/templates/REVIEW_TEMPLATE.md` (move to `archived/`)
- `docs/dev/sprints/templates/archived/` (create folder)
- `docs/dev/foundation/SPRINT_MANUAL.md` (§6, §7, §8)

---

## Risks

**Low.** Template change and doc archive only. Historical files untouched. Validated on first sprint using new template (Sprint 17).

---

## Completion

*(fill when Status = DONE)*
- **Review decision:**
- **Rationale:**
- **Follow-ups:**
- **PR link:**
