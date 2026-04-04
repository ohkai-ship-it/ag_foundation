# SPRINT DESCRIPTION — Sprint16 — governance_simplification
# Version number: v0.2

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
> - INDEX update rule (status ↔ filename integrity)

> **Folder naming (required):** `/docs/dev/sprints/documentation/Sprint16_governance_simplification/`
> **Files (required):**
> - `S16_DESCRIPTION.md` (this file; plan only — report in S16_REVIEW_01.md)
> - `S16_REVIEW_01.md` (outcomes, cognitive health, review decision)
> - `S16_PR_01.md` (PR checklist for sprint finalization)

> **D11 — THIS SPRINT RUNS UNDER OLD RULES**
> Sprint 16 executes under the current SPRINT_MANUAL (pre-simplification).
> The new naming conventions, templates, and procedures this sprint delivers
> take effect in Sprint 17. Do not apply them here.

---

## 1) Metadata
- **Sprint:** Sprint16
- **Name:** governance_simplification
- **Dates:** 2026-04-04 → TBD
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **State:** Ready

---

## 2) Sprint goal

Reduce sprint ceremony overhead from 30–50 min/sprint to ~10 min/sprint by eliminating filename-status coupling, replacing bloated PR/review artifacts with a MECE description+review pair, formalizing the HITL framework in governance docs, standardising status vocabularies across all governance artifacts, and introducing lightweight automation (`gov.py`).

---

## 3) Scope (what we intend to ship)

### Must-have (P0)
- AF-0129 — Eliminate filename-status coupling (Owner: Jacob)

### Should-have (P1)
- AF-0130 — Drop redundant sprint artifacts / MECE description+review split (Owner: Jacob)
- AF-0131 — Template enhancements: time, model, docs impact & decision capture (Owner: Jacob)
- AF-0132 — HITL framework in governance docs (Owner: Jacob)
- AF-0133 — Copilot instructions: ToDo discipline (Owner: Jacob)
- AF-0134 — Streamline INDEX files (Owner: Jacob) *(depends on AF-0129)*
- AF-0136 — Governance docs consolidation (Owner: Jacob) *(depends on all)*

### Nice-to-have (P2)
- AF-0135 — Governance automation script `gov.py` (Owner: Jacob) *(depends on AF-0129, AF-0134)*

---

## 4) Execution sequence

```
              ┌─ AF-0129 (filenames) ─────┐
              │                            ├─→ AF-0134 (INDEX) ─→ AF-0135 (gov.py) ─┐
              ├─ AF-0130 (artifacts) ──────┘                                         │
 Start ──→    ├─ AF-0131 (templates) ─────────────────────────────────────────────────┼─→ AF-0136 (docs)
              ├─ AF-0132 (HITL) ──────────────────────────────────────────────────────┘
              └─ AF-0133 (Copilot) ───────────────────────────────────────────────────┘
```

**Parallelizable (Phase 1):** AF-0129, AF-0130, AF-0131, AF-0132, AF-0133 — no mutual dependencies.
**Sequential:** AF-0134 waits on AF-0129. AF-0135 waits on AF-0129 + AF-0134. AF-0136 waits on all.

---

## 5) Sprint start checklist (ritual)

### Jeff + Kai
- [x] Create AFs (Status = READY) — AF-0129 through AF-0136
- [x] Create this sprint description file
- [x] Define sprint ID + sprint name

### Jacob
- [ ] Read this sprint description
- [ ] Read all 8 AF files in `/docs/dev/backlog/items/`
- [ ] Read `docs/dev/additional/GOVERNANCE_SIMPLIFICATION_PLAN_0.1.md` (APPROVED)
- [ ] Ask clarifying questions in chat (no writing required)
- [ ] Create branch: `feat/sprint16-governance-simplification`
- [ ] Update INDEX files (ritual at sprint start):
  - `/docs/dev/backlog/INDEX_BACKLOG.md`
  - `/docs/dev/bugs/INDEX_BUGS.md`
  - `/docs/dev/decisions/INDEX_DECISIONS.md`
  - `/docs/dev/sprints/INDEX_SPRINTS.md` (Sprint 16 → In Progress)
- [ ] Confirm with Kai before starting implementation (G1 + G3)

> **INDEX update rule (strict):**
> 1) Update when any AF/BUG/ADR/SPRINT status changes
> 2) Also update as a ritual at sprint start

---

## 6) PR plan

> Rule: **1 commit per AF, 1 PR per sprint.**
> All AFs are committed separately to the sprint branch. The branch is merged to main via one PR at sprint close.

- Branch: `feat/sprint16-governance-simplification`
- Commit plan (in execution order):
  - AF-0129 — Eliminate filename-status coupling
  - AF-0130 — Drop redundant sprint artifacts
  - AF-0131 — Template enhancements
  - AF-0132 — HITL framework in governance docs
  - AF-0133 — Copilot instructions: ToDo discipline
  - AF-0134 — Streamline INDEX files
  - AF-0135 — Governance automation script gov.py *(if time permits)*
  - AF-0136 — Governance docs consolidation

---

## 7) Definition of Done (Sprint-level)
- [ ] AF-0129 (P0) merged and CI passes
- [ ] All shipped AFs have completion sections filled
- [ ] GSV v1.3 bumped across all governance docs (AF-0136 AC)
- [ ] Review completed (S16_REVIEW_01.md filled, decision recorded)
- [ ] Repo hygiene executed
- [ ] INDEX files updated and consistent

---

## 8) Key references
- Governance plan (APPROVED): `docs/dev/additional/GOVERNANCE_SIMPLIFICATION_PLAN_0.1.md`
- AF files: `docs/dev/backlog/items/AF012[9]_READY_*.md` through `AF0136_READY_*.md`
- FOUNDATION_MANUAL: `docs/dev/foundation/FOUNDATION_MANUAL.md`
- SPRINT_MANUAL: `docs/dev/foundation/SPRINT_MANUAL.md`

---

## 9) Risks & mitigations
- **Two naming conventions coexist after this sprint**
  - Mitigation: documented in FOLDER_STRUCTURE_0.3 (AF-0136); `gov.py check` validates both (AF-0135)
- **AF-0136 depends on all other AFs** — if any AF slips, consolidation is blocked
  - Mitigation: AF-0135 (P2) is the only optional item; all P1s feed AF-0136
- **test_documentation_drift.py may need updating for new conventions**
  - Mitigation: AF-0129 AC explicitly requires this; only targeted file touched

---

## 10) Dependencies
- Internal: none — all work is docs + process, no runtime code changes (except `test_documentation_drift.py`)
- External: none
