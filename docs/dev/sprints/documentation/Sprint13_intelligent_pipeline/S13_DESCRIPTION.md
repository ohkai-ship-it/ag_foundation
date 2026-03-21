# SPRINT DESCRIPTION — Sprint13 — intelligent_pipeline
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

> **Folder naming (required):** `/docs/dev/sprints/documentation/Sprint13_intelligent_pipeline/`
> **Files (required):**
> - `S13_DESCRIPTION.md` (this file; includes plan + report)
> - `S13_REVIEW_01.md` (created by Jeff+Kai; executed by Jacob)
> - `S13_PR_01.md` (PR checklist for sprint finalization)

---

## 1) Metadata
- **Sprint:** Sprint13
- **Name:** intelligent_pipeline
- **Dates:** 2026-03-21 → TBD
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **State:** Ready

---

## 2) Sprint goal
Deliver smarter LLM-composed plans with playbook awareness and inline
approval UX, while extracting the monolithic runtime into dedicated
component files, fixing the verifier optional-step bug (BUG-0017), and
building a V1 Orchestrator that handles mixed skill+playbook plans.

---

## 3) Scope (what we intend to ship)

### Must-have (P0)
- AF-0114 — Extract pipeline V0s to dedicated files (Owner: TBD)
- AF-0115 — V1 Verifier: step-aware verification / BUG-0017 fix (Owner: TBD)
- AF-0103 — V2 Planner: playbooks as first-class plan steps (Owner: TBD)
- AF-0117 (partial) — V1 Orchestrator: mixed skill+playbook plan support (Owner: TBD)

### Should-have (P1)
- (AF-0112 already DONE — inline plan preview and confirm in `ag run`)

### Nice-to-have (P2)
- (none)

> **Scope note:** AF-0117 is split across sprints. Sprint 13 delivers V1Orchestrator
> with mixed plan handling (skill + playbook step types). Sprint 14 extends V1Orchestrator
> with per-step verification wiring (V1Executor + V1Verifier integration).

---

## 4) Sprint start checklist (ritual)
### Jeff + Kai
- [x] Create AFs (Status = Ready)
- [x] Create this sprint description file
- [x] Define sprint ID + sprint name

### Jacob
- [ ] Read sprint description
- [ ] Check AFs in `/docs/dev/backlog/items/`
- [ ] Ask clarifying questions in chat (no writing required)
- [ ] Create branch
- [ ] Create sprint folder
- [ ] Update INDEX files (ritual at sprint start):
  - `/docs/dev/backlog/INDEX_BACKLOG.md`
  - `/docs/dev/bugs/INDEX_BUGS.md`
  - `/docs/dev/decisions/INDEX_DECISIONS.md`
  - `/docs/dev/sprints/INDEX_SPRINTS.md`
- [ ] Confirm with Kai before starting implementation

> **INDEX update rule (strict):**
> 1) Update when any AF/BUG/ADR/SPRINT status changes
> 2) Also update as a ritual at sprint start

---

## 5) PR plan
> Rule: **1 commit per AF, 1 PR per sprint.**
> All AFs are committed separately to the sprint branch. The branch is merged to main via one PR at sprint close.

- Branch: `feat/sprint13-intelligent-pipeline`
- Commit plan:
  - AF-0114 — Extract pipeline V0s to dedicated files
  - AF-0115 — V1 Verifier: step-aware verification
  - AF-0103 + AF-0117 (partial) — V2 Planner + V1 Orchestrator for mixed plans

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
- Risk: AF-0114 extraction is a large refactor touching runtime.py
  - Mitigation: Pure structural refactor with zero behavior change; tests must pass identically before and after
- Risk: V2Planner (AF-0103) changes LLM prompt and plan format
  - Mitigation: Existing plan tests + new playbook-aware plan tests; backward-compatible plan schema
- Risk: V1Verifier (AF-0115) changes verification logic
  - Mitigation: Existing verifier tests preserved; new tests for optional-step handling
- Risk: V1Orchestrator (AF-0117 partial) expands scope beyond original sprint plan
  - Mitigation: Only mixed plan handling in Sprint 13; per-step verification wiring deferred to Sprint 14

---

## 8) Dependencies
- Internal: AF-0114 must land before AF-0115 (verifier needs own file first)
- Internal: AF-0115 must land before AF-0103/AF-0117 (V1Verifier wired in create_runtime)
- Internal: AF-0103 and AF-0117 (partial) are co-committed (V2Planner needs V1Orchestrator for mixed plans)
- Internal: AF-0112 (inline plan confirm) already DONE (merged to main)
- External: None

---

# Sprint report section (fill at sprint end)

## 9) Outcome summary
- Shipped:
  - ...
- Not shipped:
  - ...

---

## 10) Completed work
- ✅ AF-0112 — Inline plan preview and confirm in ag run (pre-sprint)

---

## 11) Not completed / carried over
- ⏭️ (none yet)

---

## 12) Evidence
- Review file(s):
  - `S13_REVIEW_01.md`
- Representative RunTrace IDs:
  - (TBD)
- Test summary:
  - (TBD)

---

## 13) Learnings
- What worked:
- What to improve:

---

## 14) Next sprint candidate slice
- P0: AF-0116 (V1 Executor), AF-0117 remainder (per-step verification wiring)
- P1: AF-0118 (V1 Recorder)
- P2: AF-0096 (test workspace cleanup), AF-0104 (V3 Planner feasibility)
