# SPRINT DESCRIPTION — Sprint15 — llm_intelligence_layer
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

> **Folder naming (required):** `/docs/dev/sprints/documentation/Sprint15_llm_intelligence_layer/`
> **Files (required):**
> - `S15_DESCRIPTION.md` (this file; includes plan + report)
> - `S15_REVIEW_01.md` (created by Jeff+Kai; executed by Jacob)
> - `S15_PR_01.md` (PR checklist for sprint finalization)

---

## 1) Metadata
- **Sprint:** Sprint15
- **Name:** llm_intelligence_layer
- **Dates:** 2026-03-22 → TBD
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **State:** In Progress

---

## 2) Sprint goal
Add LLM-powered semantic verification, output repair, and feasibility
judgment to the pipeline. Fix the empty-plan-as-success bug. Achieve
Gate C (Goals-Only Preparation) readiness.

---

## 3) Scope (what we intend to ship)

### Must-have (P0)
- BUG-0020 — Empty plan reports success (Owner: Jacob)

### Should-have (P1)
- AF-0121 — V3Planner: feasibility assessment (Owner: Jacob)
- AF-0123 — V2Verifier: LLM semantic quality checks (Owner: Jacob)

### Nice-to-have (P2)
- AF-0124 — V2Executor: LLM output repair (Owner: Jacob)
- AF-0122 — CLI planning and pipeline display (Owner: Jacob)

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

- Branch: `feat/sprint15-llm-intelligence-layer`
- Commit plan:
  - BUG-0020 — Empty plan reports success (guard fix)
  - AF-0121 — V3Planner: feasibility assessment
  - AF-0123 — V2Verifier: LLM semantic quality checks
  - AF-0124 — V2Executor: LLM output repair
  - AF-0122 — CLI planning and pipeline display

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
- Risk: LLM integration in V2Verifier and V2Executor adds latency
  - Mitigation: Graceful degradation — V1 results stand if LLM unavailable
- Risk: AF-0121 (V3Planner) touches critical plan generation path
  - Mitigation: V3Planner extends V2Planner; V2 behavior preserved for non-feasibility paths
- Risk: BUG-0020 is P0 — must fix before shipping anything else
  - Mitigation: Scheduled as first commit; small scope (guard + status change)
- Risk: 5 items may exceed sprint capacity
  - Mitigation: P2 items (AF-0124, AF-0122) are deferrable stretch goals

---

## 8) Dependencies
- Internal: Sprint 14 must be merged (V1Executor, V1Verifier, V1Orchestrator, V1Recorder, ADR-0009)
- External: LLM provider access (OpenAI API key for integration tests)

---

# Sprint report section (fill at sprint end)

## 9) Outcome summary
- Shipped:
  - ...
- Not shipped:
  - ...

---

## 10) Completed work
- ...

---

## 11) Not completed / carried over
- ...

---

## 12) Evidence
- Review file(s):
  - `S15_REVIEW_01.md`
- Representative RunTrace IDs:
  - ...
- Test summary:
  - ...

---

## 13) Learnings
- What worked:
- What to improve:

---

## 14) Next sprint candidate slice
- P0:
- P1:
- P2:
