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
- **Dates:** 2026-03-22 → 2026-03-22
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **State:** Closed

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
- [x] Read sprint description
- [x] Check AFs in `/docs/dev/backlog/items/`
- [x] Ask clarifying questions in chat (no writing required)
- [x] Create branch
- [x] Create sprint folder
- [x] Update INDEX files (ritual at sprint start):
  - `/docs/dev/backlog/INDEX_BACKLOG.md` ✓ (Sprint 15 section present)
  - `/docs/dev/bugs/INDEX_BUGS.md` ✓ (BUG-0020 OPEN)
  - `/docs/dev/decisions/INDEX_DECISIONS.md` ✓ (ADR-0009 ACCEPTED)
  - `/docs/dev/sprints/INDEX_SPRINTS.md` ✓ (Sprint 15 In Progress)
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
  - AF-0125 — Deterministic test provider (follow-up from review)
  - AF-0126 — Executor/verifier LLM trace (follow-up from review)
  - BUG-0021 — ddgs/primp SSL socket GC noise fix
  - BUG-0022 — V3Planner CLI test flakiness fix
  - BUG-0023 — V2 pipeline evidence hidden fix
  - BUG-0024 — Planner duplicates emit_result fix
- PR: #10 (merged to main)

---

## 6) Definition of Done (Sprint-level)
- [x] All P0 items are merged
- [x] Each merged AF has its completion section filled
- [x] Evidence captured for behavior changes (tests + RunTrace ID(s))
- [x] Review completed (ACCEPT WITH FOLLOW-UPS — S15_REVIEW_01)
- [x] Repo hygiene executed (per checklist)
- [x] Indices updated and consistent

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
- Shipped: **11/11 items** — all P0, P1, and P2 items delivered
- Not shipped: None

---

## 10) Completed work

### Batch 1 (initial scope: AF-0121/0122/0123/0124, BUG-0020)
| Commit | Items |
|--------|-------|
| `8d653f8` | BUG-0020 fix, AF-0121 V3Planner, AF-0123 V2Verifier, BUG-0022 filed |
| `a388c4a` | AF-0124 V2Executor LLM output repair |
| `c6554bc` | AF-0122 CLI planning and pipeline display |
| `7819b4e` | Sprint 15 close: mark batch 1 items DONE/FIXED |
| `6ad5c8b` | BUG-0023 fix: pipeline manifest + trace.planning truthfulness |
| `27f4426` | S15_PR_01 filled |
| `cfd1a0f` | BUG-0023 followup: fix TestInlinePlanConfirmRun mocks |
| `d59b326` | S15_REVIEW_01 complete |
| `4fd87be` | Review doc fixes |

### Batch 2 (follow-ups from review: AF-0125/0126, BUG-0021/0022/0023/0024)
| Commit | Items |
|--------|-------|
| `9243ae3` | AF-0125 FakeLLMProvider + BUG-0021 tighten warnings + BUG-0022 unskip tests |
| `b04c2fb` | BUG-0024 strip redundant emit_result |
| `e59d24e` | AF-0126 executor/verifier LLM trace + BUG-0023 evidence display |
| `fd5430d` | Doc status updates for batch 2 |

### Batch 3 (trace gap fixes from live testing)
| Commit | Items |
|--------|-------|
| `a8f4823` | Fix: feasibility tokens + verifier semantic evidence in trace |
| `4d3769d` | Fix: per-step LLM token tracking (tokens_used/model_used on Step) |

---

## 11) Not completed / carried over
- None — all 11 scope items shipped.

---

## 12) Evidence
- Review file(s):
  - `S15_REVIEW_01.md` — ACCEPT WITH FOLLOW-UPS (2026-03-22)
- Representative RunTrace IDs:
  - `6b3de7bf-cf06-44e3-913f-7c509b2e0914` — happy path (review trace)
  - `4ddb9655` — failure path (review trace)
  - `767b3aa9-c2e3-4ad1-9450-959d5aee0cba` — live test (summarize, batch 2)
  - `a0c30c81-7a76-43bf-8fb3-de3bb681fe8f` — live test (Wetterbericht, batch 3)
- Test summary:
  - `pytest -W error` → 794 passed, 3 deselected, 0 failed
  - `ruff check src tests` → All checks passed
  - `ruff format --check src tests` → 69 files already formatted
  - `pytest --cov=src/ag` → 86% overall coverage

---

## 13) Learnings
- What worked:
  - FakeLLMProvider (AF-0125) eliminated all test flakiness from real LLM calls — unskipped 9 tests
  - TrackingLLMProvider delta approach gives per-step token data without modifying any skill code
  - Post-trace semantic verification (calling build_semantic_evidence after RunTrace construction) resolved the chicken-and-egg dependency elegantly
- What to improve:
  - Live testing found 3 trace data gaps (feasibility tokens, verifier semantic, per-step tokens) that unit tests didn't catch — need integration-level trace assertions
  - Review identified follow-up items earlier than sprint close — consider continuous follow-up filing

---

## 14) Next sprint candidate slice
- P0: (none)
- P1: Gate C readiness, skill registry improvements
- P2: Trace visualization, LLM cost tracking dashboard
