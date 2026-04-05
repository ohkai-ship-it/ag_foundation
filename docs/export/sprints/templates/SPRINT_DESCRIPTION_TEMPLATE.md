# S##_DESCRIPTION — Sprint## — <sprint_name>
# Version number: v1.3
# Status: PLANNED | DONE | REJECTED

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
> `/docs/dev/foundation/SPRINT_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - 1 PR = 1 sprint
> - INDEX update rule

> **Folder naming (required):** `/docs/dev/sprints/documentation/Sprint##_three_word_description/`
> **Files (required):**
> - `S##_DESCRIPTION.md` (this file — planning artifact, stable during sprint)
> - `S##_REVIEW.md` (outcomes artifact, written at sprint close)

---

## 1) Metadata
- **Sprint:** Sprint##
- **Name:** <three_word_description>
- **Dates:** YYYY-MM-DD → YYYY-MM-DD
- **Branch:**
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **Status:** PLANNED
- **Models:**
- **Started:**
- **Completed:**

---

## 2) Sprint goal

One sentence, outcome-focused.

---

## 3) Scope (what we intend to ship)

### Must-have (P0)
- AF#### — <title> (Owner: ...)

### Should-have (P1)
- AF#### — <title> (Owner: ...)

### Nice-to-have (P2)
- AF#### — <title> (Owner: ...)

---

## 4) Execution sequence

*(Optional: dependency diagram or ordered list showing AF execution order)*

---

## 5) Sprint start checklist (ritual)

### Jeff + Kai
- [ ] Create AFs (Status = READY)
- [ ] Create this sprint description file
- [ ] Define sprint ID + sprint name

### Jacob
- [ ] Read this sprint description
- [ ] Read all AF files in scope
- [ ] Ask clarifying questions in chat (no writing required)
- [ ] Create branch
- [ ] Update INDEX files (ritual at sprint start):
  - `/docs/dev/backlog/INDEX_BACKLOG.md`
  - `/docs/dev/bugs/INDEX_BUGS.md`
  - `/docs/dev/decisions/INDEX_DECISIONS.md`
  - `/docs/dev/sprints/INDEX_SPRINTS.md` (Sprint ## → In Progress)
- [ ] Confirm with Kai before starting implementation (G1 + G3)

> **INDEX update rule (strict):**
> 1) Update when any AF/BUG/ADR/SPRINT status changes
> 2) Also update as a ritual at sprint start

---

## 6) PR plan

> Rule: **1 commit per AF, 1 PR per sprint.**
> All AFs are committed separately to the sprint branch. The branch is merged to main via one PR at sprint close.

- Branch: `<type>/sprint##-<description>`
- Commit plan (in execution order):
  - AF#### — <title>
  - AF#### — <title>

---

## 7) Definition of Done (Sprint-level)
- [ ] All P0 items merged and CI passes
- [ ] All shipped AFs have completion sections filled
- [ ] Review completed (`S##_REVIEW.md` filled, decision recorded)
- [ ] Repo hygiene executed
- [ ] INDEX files updated and consistent

---

## 8) Risks & mitigations
- Risk: ...
  - Mitigation: ...

---

## 9) Dependencies
- Internal: ...
- External: ...

---

## 10) Key references
- AF files: `docs/dev/backlog/items/AF####_*.md`
- FOUNDATION_MANUAL: `docs/dev/foundation/FOUNDATION_MANUAL.md`
- SPRINT_MANUAL: `docs/dev/foundation/SPRINT_MANUAL.md`

---

## 11) Implementation Notes

*(Space for mid-sprint decisions, observations, and notes. This section may be updated during the sprint.)*
