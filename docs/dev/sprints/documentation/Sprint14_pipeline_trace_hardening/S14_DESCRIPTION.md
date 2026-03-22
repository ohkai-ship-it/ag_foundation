# SPRINT DESCRIPTION — Sprint14 — pipeline_trace_hardening
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

> **Folder naming (required):** `/docs/dev/sprints/documentation/Sprint14_pipeline_trace_hardening/`
> **Files (required):**
> - `S14_DESCRIPTION.md` (this file; includes plan + report)
> - `S14_REVIEW_01.md` (created by Jeff+Kai; executed by Jacob)
> - `S14_PR_01.md` (PR checklist for sprint finalization)

---

## 1) Metadata
- **Sprint:** Sprint14
- **Name:** pipeline_trace_hardening
- **Dates:** 2026-03-22 → TBD
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **State:** In Progress

---

## 2) Sprint goal
Harden the remaining pipeline components (Executor output validation,
Orchestrator per-step verification loop, Recorder evidence capture), fix
two discovered bugs (planner misclassification, orchestrator required-flag
drop), and make runs fully auditable with planner trace, per-step LLM
attribution, and component manifest in RunTrace.

---

## 3) Scope (what we intend to ship)

### Must-have (P0)
- AF-0116 — V1 Executor: output schema validation (Owner: TBD)
- AF-0117 — V1 Orchestrator: per-step verification remainder (Owner: TBD)
- BUG-0018 — V2Planner misclassifies playbook as skill (Owner: TBD)
- BUG-0019 — V1Orchestrator drops required flag on expansion (Owner: TBD)

### Should-have (P1)
- AF-0118 — V1 Recorder: verification evidence (Owner: TBD)
- AF-0119 — Planner trace + per-step LLM attribution (Owner: TBD)
- AF-0113 — Per-step output verification (Owner: TBD)

### Nice-to-have (P2)
- AF-0096 — Test workspace cleanup pollution (Owner: TBD)
- AF-0104 — LLM Planner V3 feasibility (Owner: TBD)
- AF-0120 — Component manifest in RunTrace (Owner: TBD)

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
- [x] Create branch
- [x] Create sprint folder
- [x] Update INDEX files (ritual at sprint start):
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

- Branch: `feat/sprint14-pipeline-trace-hardening`
- Commit plan:
  - BUG-0019 — V1Orchestrator drops required flag (one-liner fix)
  - BUG-0018 — V2Planner misclassifies playbook as skill
  - AF-0116 — V1 Executor: output schema validation
  - AF-0117 — V1 Orchestrator: per-step verification remainder
  - AF-0118 — V1 Recorder: verification evidence
  - AF-0119 — Planner trace + per-step LLM attribution
  - AF-0113 — Per-step output verification
  - AF-0096 — Test workspace cleanup pollution
  - AF-0104 — LLM Planner V3 feasibility
  - AF-0120 — Component manifest in RunTrace

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
- Risk: Large scope (10 items) may exceed sprint capacity
  - Mitigation: P2 items (AF-0096, AF-0104, AF-0120) are deferrable; P0 bugs are small fixes
- Risk: AF-0119 (planner trace) touches multiple components
  - Mitigation: Two-part design (Part A: planner preamble, Part B: per-step attribution) allows incremental delivery
- Risk: AF-0104 (V3 Planner feasibility) may reveal significant design work
  - Mitigation: Scoped as feasibility study only, no implementation required

---

## 8) Dependencies
- Internal: Sprint 13 must be merged (AF-0103, AF-0114, AF-0115, AF-0117 partial)
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
- ...

---

## 11) Not completed / carried over
- ...

---

## 12) Evidence
- Review file(s):
  - `S14_REVIEW_01.md`
- Representative RunTrace IDs:
  - `run_...`
- Test summary:
  - `pytest ...` (PASS/FAIL)

---

## 13) Learnings
- What worked:
- What to improve:

---

## 14) Next sprint candidate slice
- P0:
- P1:
- P2:
