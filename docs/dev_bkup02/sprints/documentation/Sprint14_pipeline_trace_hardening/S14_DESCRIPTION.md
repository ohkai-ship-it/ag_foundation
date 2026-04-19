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
- **State:** Closed

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
- [x] All P0 items are merged
- [x] Each merged AF has its completion section filled
- [x] Evidence captured for behavior changes (tests + RunTrace ID(s))
- [x] Review completed (ACCEPT WITH FOLLOW-UPS — 2026-03-22)
- [x] Repo hygiene executed (per checklist)
- [x] Indices updated and consistent

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
- Shipped (all items):
  - BUG-0019: V1Orchestrator drops `required` flag — fixed
  - BUG-0018: V2Planner misclassifies playbook as skill — fixed
  - AF-0116: V1 Executor output schema validation with retry logic
  - AF-0117: V1 Orchestrator per-step verification loop (complete)
  - AF-0118: V1 Recorder verification evidence written to RunTrace
  - AF-0119: Planner trace + per-step LLM attribution (`PlanningMetadata`, `PlanningResult`)
  - AF-0113: Per-step output verification (Verifier/Skills integration)
  - AF-0096: Test workspace isolation via `AG_WORKSPACE_DIR` env redirect
  - AF-0104: LLM Planner V3 feasibility study (ADR-0009 written; implementation deferred)
  - AF-0120: Component manifest in RunTrace (`PipelineManifest`, `RunTrace.pipeline`)
  - Extra: Graceful `PlannerError` when LLM returns empty steps (infeasible task)
- Not shipped:
  - None — all 10 sprint items completed

---

## 10) Completed work
- **BUG-0019** (P0): One-liner fix — `required` flag preserved through `_expand_step()` in V1Orchestrator
- **BUG-0018** (P0): V2Planner `_validate_skills()` now correctly distinguishes playbook names from skill names
- **AF-0116** (P1): `V1Executor` validates each skill output against its declared schema; retries up to 3 attempts; stores last validation errors in trace
- **AF-0117** (P1): `V1Orchestrator` full per-step verification loop; per-step status written to RunTrace
- **AF-0118** (P1): `V1Recorder` writes verifier evidence (pass/fail per step, counts) into `RunTrace.verifier`
- **AF-0119** (P1): `PlanningMetadata` + `PlanningResult` dataclass; planner wraps output; `RunTrace.planning` populated; LLM model and confidence attributed per-step
- **AF-0113** (P1): `V0Verifier`/`V1Verifier` enforce per-step output contracts; integration with executor retry loop
- **AF-0096** (P2): `tests/conftest.py` session autouse fixture; `AG_WORKSPACE_DIR` redirected to temp dir; `TestUserWorkspaceNonPollution` tests added
- **AF-0104** (P2): ADR-0009 written: two-phase LLM feasibility design, `FeasibilityLevel`/`CapabilityGap` schemas, S15 implementation plan (7 steps)
- **AF-0120** (P2): `PipelineManifest` model; `RunTrace.pipeline` field; `create_runtime()` populates from component class names; 5 tests in `TestPipelineManifest`
- **Extra fix**: `LLMPlanResponse.steps` default to `[]`; `_validate_skills()` raises friendly `PlannerError` for infeasible tasks

---

## 11) Not completed / carried over
- Nothing carried over. All 10 sprint items shipped.
- Follow-up items filed for Sprint 15:
  - BUG-0020 (P0): Empty plan reports success — must be fixed before S15 ships
  - BUG-0021 (P2): `pytest -W error` flaky from ddgs/primp SSL socket GC noise
  - AF-0121 (P1): V3Planner feasibility assessment implementation
  - AF-0123 (P1): V2Verifier LLM semantic checks
  - AF-0124 (P2): V2Executor LLM output repair

---

## 12) Evidence
- Review file(s):
  - `S14_REVIEW_01.md` — ACCEPT WITH FOLLOW-UPS (2026-03-22)
- Review artifacts:
  - `artifacts/review_S14_01/env.txt`
  - `artifacts/review_S14_01/ruff_summary.txt` — 0 errors
  - `artifacts/review_S14_01/pytest_summary.txt` — 751 passed, 88% coverage
  - `artifacts/review_S14_01/happy_trace.json` — run `883779d3-aa89-430d-85dc-0b72d687236c`
  - `artifacts/review_S14_01/failure_trace.json` — failure-path verified
  - `artifacts/review_S14_01/bug_triage.md`
- Test summary:
  - `pytest -q`: 751 passed, 3 deselected (2026-03-22)
  - Coverage: 88% (4280 stmts, 534 missed)
  - `ruff check src tests`: 0 errors

---

## 13) Learnings
- What worked:
  - Full P0/P1/P2 delivery with 0 carry-overs: setting P2 items (AF-0096, AF-0104, AF-0120) as deferrable created no pressure but paid off
  - Feasibility study (AF-0104) as a sprint-level deliverable: produces ADR without blocking implementation
  - `AG_WORKSPACE_DIR` env-based workspace isolation (AF-0096) is the cleanest lever; avoids patching all test fixtures
  - Splitting planner attribution (AF-0119) into `PlanningResult` dataclass + `RunTrace.planning` kept scope tight
- What to improve:
  - 7 pre-existing ruff lint errors (E501/E402/I001) should have been caught by the pre-commit gate, not the review
  - `pytest -W error` flakiness from ddgs/primp SSL socket GC noise (BUG-0021) is a CI ergonomics problem
  - AF status (DONE/READY) should be updated in AF file + INDEX immediately on commit, not left for review to correct

---

## 14) Next sprint candidate slice
- P0:
  - BUG-0020: Empty plan reports success (must fix before S15 ships)
- P1:
  - AF-0121: V3Planner feasibility assessment (implementation per ADR-0009; ~7 steps)
  - AF-0123: V2Verifier LLM semantic checks
- P2:
  - AF-0122: CLI planning pipeline display
  - AF-0124: V2Executor LLM output repair
  - BUG-0021: Fix `pytest -W error` ddgs/primp SSL socket noise
