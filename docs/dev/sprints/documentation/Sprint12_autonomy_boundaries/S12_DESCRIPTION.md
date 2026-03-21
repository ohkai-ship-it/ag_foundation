# SPRINT DESCRIPTION — Sprint12 — autonomy_boundaries
# Version number: v0.1

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

> **Folder naming (required):** `/docs/dev/sprints/documentation/Sprint##_three_word_description/`
> **Files (required):**
> - `S##_DESCRIPTION.md` (this file; includes plan + report)
> - `S##_REVIEW_01.md` (created by Jeff+Kai; executed by Jacob)
> - `S##_PR_01.md` (PR checklist for sprint finalization)

---

## 1) Metadata
- **Sprint:** Sprint12
- **Name:** autonomy_boundaries
- **Dates:** 2026-03-21 → TBD
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **State:** Ready

---

## 2) Sprint goal
Stabilize guided autonomy output quality and storage boundaries by unifying summarization, hardening content emission, and standardizing run-centered artifact/plan layout.

---

## 3) Scope (what we intend to ship)

### Must-have (P0)
- AF0108 — Unify summarization skill (Owner: Jacob)
- AF0109 — emit_result strict content validation (Owner: Jacob)
- AF0110 — Run layout and plan artifacts refactor (Owner: Jacob)

### Should-have (P1)
- AF0107 — load_documents MD inputs reliability (Owner: Jacob)

### Nice-to-have (P2)
- AF0105 — CLI defaults verification audit (Owner: TBD)
- AF0106 — V1Planner file pattern defaults (Owner: TBD)
- AF0096 — Test workspace cleanup pollution (Owner: TBD)
- AF0111 — --workspace flag must never create (Owner: Jacob)

Excluded explicitly for this sprint:
- AF0103 — LLM Planner V2 (skills+playbooks)
- AF0104 — LLM Planner V3 (feasibility)

---

## 4) Sprint start checklist (ritual)
### Jeff + Kai
- [x] Create AFs (Status = Ready)
- [x] Create this sprint description file
- [x] Define sprint ID + sprint name

### Jacob
- [x] Read sprint description
- [x] Check AFs in `/docs/dev/backlog/items/`
- [x] Ask clarifying questions in chat (no writing required)
- [x] Create branch (`feat/sprint12-autonomy-boundaries`)
- [x] Create sprint folder
- [x] Update INDEX files (ritual at sprint start):
  - `/docs/dev/backlog/INDEX_BACKLOG.md` — 4 AFs promoted PROPOSED → READY
  - `/docs/dev/bugs/INDEX_BUGS.md` — no changes needed
  - `/docs/dev/decisions/INDEX_DECISIONS.md` — no changes needed
  - `/docs/dev/sprints/INDEX_SPRINTS.md` — already Active
- [ ] Confirm with Kai before starting implementation

> **INDEX update rule (strict):**
> 1) Update when any AF/BUG/ADR/SPRINT status changes
> 2) Also update as a ritual at sprint start

---

## 5) PR plan (expected slices)
> Rule: **1 PR = 1 sprint (per SPRINT_MANUAL §1.1 + §6.0).**

- **Single branch:** `feat/sprint12-autonomy-boundaries`
- **Single PR at sprint close** covering all scope items:
  - AF0107 — load_documents MD inputs reliability
  - AF0108 — Unify summarization skill
  - AF0109 — emit_result strict content validation
  - AF0110 — Run layout and plan artifacts refactor
  - AF0111 — --workspace flag must never create
  - AF0105 — CLI defaults verification audit
  - AF0106 — V1Planner file pattern defaults
  - AF0096 — Test workspace cleanup pollution

---

## 6) Definition of Done (Sprint-level)
- [ ] All P0 items are merged
- [ ] Each merged AF has its completion section filled
- [ ] Evidence captured for behavior changes (tests + RunTrace ID(s))
- [ ] Review completed (ACCEPT or ACCEPT WITH FOLLOW-UPS)
- [ ] Repo hygiene executed (per checklist)
- [ ] Indices updated and consistent

---

## 7) Risks & mitigations
- Risk: Breaking change due to plan storage path move and removal of deprecated files
  - Mitigation: Explicit no-backward-compatibility scope + targeted runtime/storage tests
- Risk: Skill unification causes planner/playbook references to fail
  - Mitigation: Registry validation + playbook and planner integration tests
- Risk: Strict emit validation blocks expected workflows
  - Mitigation: Clear error messaging + trace evidence for rejection reasons

---

## 8) Dependencies
- Internal: AF0108 depends on AF0107; AF0109 depends on AF0108; AF0110 depends on AF0109
- External: none

---

# Sprint report section (fill at sprint end)

## 9) Outcome summary
- Shipped:
  - _To be filled_
- Not shipped:
  - _To be filled_

---

## 10) Completed work
- ✅ _To be filled_

---

## 11) Not completed / carried over
- ⏭️ _To be filled_

---

## 12) Evidence
- Review file(s):
  - `S12_REVIEW_01.md`
- Representative RunTrace IDs:
  - _To be filled_
- Test summary:
  - _To be filled_

---

## 13) Learnings
- What worked:
- What to improve:

---

## 14) Next sprint candidate slice
- P0:
- P1:
- P2:
