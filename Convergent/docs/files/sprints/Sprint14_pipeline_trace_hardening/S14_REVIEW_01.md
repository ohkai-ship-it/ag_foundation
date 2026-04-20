# SPRINT REVIEW — S14_REVIEW_01 — pipeline_trace_hardening
# Version number: v0.2

> **Purpose:** This file contains (A) the review tasks Jacob must execute and (B) the final review entry Jeff+Kai use to decide: **ACCEPT / ACCEPT WITH FOLLOW-UPS / REJECT**.
> **Location:** `/docs/dev/sprints/documentation/Sprint14_pipeline_trace_hardening/S14_REVIEW_01.md`

---

## A) Review execution tasks (Jacob)

### Metadata
- **Review ID:** S14_REVIEW_01
- **Scope:** Sprint14
- **Executor:** Jacob
- **Date:** 2026-03-22
- **Commit / tag:** `0ab7411` (feat/sprint14-pipeline-trace-hardening)
- **Environment:** Windows 11 (NT 10.0.22631.0), Python 3.14.0, pip venv

### Inputs (links)
- Sprint description: `S14_DESCRIPTION.md`
- AF items in scope (shipped — DONE):
  - `docs/dev/backlog/items/AF0116_DONE_v1_executor_output_validation.md`
  - `docs/dev/backlog/items/AF0117_DONE_v1_orchestrator_perstep_loop.md`
  - `docs/dev/backlog/items/AF0118_DONE_v1_recorder_verification_evidence.md`
  - `docs/dev/backlog/items/AF0104_DONE_llm_planner_v3_feasibility.md`
  - `docs/dev/backlog/items/AF0113_DONE_per_step_output_verification.md`
  - `docs/dev/backlog/items/AF0119_DONE_planner_trace_llm_attribution.md`
- AF items in scope (shipped during review — DONE as of Pass 1):
  - `docs/dev/backlog/items/AF0096_DONE_test_workspace_cleanup.md`
  - `docs/dev/backlog/items/AF0120_DONE_component_manifest_trace.md`
- Bug reports (FIXED):
  - `docs/dev/bugs/reports/BUG0018_FIXED_v2planner_misclassifies_playbook.md`
  - `docs/dev/bugs/reports/BUG0019_FIXED_orchestrator_drops_required_flag.md`
- Cornerstones (root): ARCHITECTURE.md, CLI_REFERENCE.md
- ⚠️ **Hygiene issue:** `AF0113_READY_per_step_output_verification.md` still exists alongside the DONE version — stale file, must be deleted

### Outputs (paths)
Create an evidence folder:
- `/docs/dev/sprints/documentation/Sprint14_pipeline_trace_hardening/artifacts/review_S14_01/`

Recommended evidence files:
- `env.txt`
- `scope_links.md`
- `pytest_summary.txt`
- `ruff_summary.txt`
- `cli_outputs.txt`
- `happy_trace.json`
- `failure_trace.json`
- `index_diff_notes.md`
- `bug_triage.md` (if applicable)

---

### Pass 0 — Setup & invariants
- [x] Fresh venv; install project
- [x] Record `python --version` — Python 3.14.0
- [x] Record `pip freeze | head -n 50` — 35 packages captured
- [x] Confirm `ag --help` works — OK, 9 subcommands visible
- [x] Confirm manual gate (e.g., `AG_DEV=1`) behavior — `AG_DEV` not set by default; manual gate active

Evidence: `env.txt`

---

### Pass 1 — Scope verification (what shipped)
- [x] Confirm each AF file exists in `/docs/dev/backlog/items/` — all 8 AF files confirmed
- [x] Confirm filename Status matches internal Status field — AF0096 & AF0120 corrected READY→DONE during this pass
- [x] Confirm each PR maps to exactly one primary AF — all AFs map to unique implementations
- [x] Confirm indices include all new/changed items — INDEX_BACKLOG.md updated for AF0096/AF0120
- [x] Stale file hygiene: `AF0113_READY_per_step_output_verification.md` deleted via `git rm`

Evidence: `scope_links.md`, `index_diff_notes.md`

---

### Pass 2 — Lint/format + test suite verification (authoritative)
- [x] `ruff check src tests` — **0 errors** (7 pre-existing fixed during review)
- [x] `ruff format --check src tests` — **69 files formatted** (exit 0)
- [x] `pytest` — **751 passed, 3 deselected** — clean
- [x] `pytest --cov=src/ag --cov-report=term-missing` — **88% coverage** (4280 stmts)
- ⚠️ `pytest -W error` — **flaky intermittent failure** due to pre-existing `ddgs`/`primp` SSL socket
  GC noise (see `bug_triage.md`). Not caused by S14 work. Flagged as P2 follow-up.

Evidence: `ruff_summary.txt`, `pytest_summary.txt`

---

### Pass 2.5 — Autonomy Gate verification (if behavior touched)
- [x] Verify all user-visible labels are trace-derived — `test_cli_truthful.py` 19/19 pass; labels in `ag runs show` match trace JSON fields
- [x] Verify policy checks are enforced — `test_confirmation_hooks.py` all pass; skills declare correct policy flags
- [x] Verify retry/timeout/failure behavior is trace-aligned — `test_trace_enrichment.py` all pass
- [x] Verify workspace isolation under failure-path scenarios — `test_storage.py::TestUserWorkspaceNonPollution` pass; `~/.ag/workspaces/` unmodified by test runs

Evidence: `cli_outputs.txt`, `happy_trace.json`, `failure_trace.json`, `pytest_summary.txt`

---

### Pass 3 — CLI "truthful UX" spot-check (if CLI touched)
- [x] Run at least one happy-path command — `ag -w review-test runs show <id>` and `--json`
- [x] Verify labels shown are trace-derived — status, mode, workspace_source, duration all match trace
- [x] Capture trace JSON and confirm it matches labels — `happy_trace.json` captured; fields consistent

Evidence: `cli_outputs.txt`, `happy_trace.json`

---

### Pass 4 — Failure-path run (if behavior touched)
- [x] Run failure-path scenario — invalid workspace + invalid run ID
- [x] Confirm no crash — CLI exits 1 with clear message, no exception traceback
- [x] Confirm trace behavior — no partial trace written for lookup failures (correct)

Evidence: `failure_trace.json`

---

### Pass 5 — Bugs triage (if any discovered)
- [x] One issue flagged: `pytest -W error` intermittent failure from `ddgs`/`primp` SSL socket GC noise
- [ ] Formal bug report not created (P2, test infra only, not runtime behavior) — follow-up AF recommended

Evidence: `bug_triage.md`

---

## Jacob completion
- **Executed by:** Jacob
- **Date:** 2026-03-22
- **Evidence folder:** `artifacts/review_S14_01/`
- **Notes:**
  - All 8 AF items confirmed DONE (AF0096 and AF0120 corrected from READY during Pass 1)
  - INDEX_BACKLOG.md updated; stale AF0113_READY deleted
  - Ruff: 0 errors after fixing 7 pre-existing lint issues (not S14 regressions)
  - Pytest: 751 passed, 88% coverage — clean
  - `pytest -W error` flaky due to pre-existing ddgs/primp SSL socket leak — P2 follow-up recommended
  - Autonomy gate: all truthful UX, confirmation hooks, workspace isolation tests pass
  - CLI happy-path and failure-path both behave correctly
  - One additional bug fix shipped (not in sprint plan): graceful PlannerError for empty LLM steps

---

## B) Review entry (Jeff + Kai)

### Review metadata
- **Reviewed by:** Jeff + Kai
- **Date:** 2026-03-22
- **Scope:** Sprint14
- **Decision:** ACCEPT WITH FOLLOW-UPS

---

### What changed (high-level)
- **AF-0116** V1 Executor: per-step output schema validation with retry logic
- **AF-0117** V1 Orchestrator: complete per-step verification loop
- **AF-0118** V1 Recorder: verification evidence written into RunTrace
- **AF-0119** Planner trace + per-step LLM attribution (`PlanningMetadata`, `PlanningResult`)
- **AF-0113** Per-step output verification integration (Verifier/Skills)
- **AF-0120** Component manifest in RunTrace (`PipelineManifest`, `RunTrace.pipeline`)
- **AF-0096** Test workspace isolation (`AG_WORKSPACE_DIR` redirect via `tests/conftest.py`)
- **AF-0104** LLM Planner V3 feasibility study (ADR-0009 written, implementation deferred to S15)
- **BUG-0018** V2Planner misclassifies playbook — fixed
- **BUG-0019** Orchestrator drops `required` flag — fixed
- **Extra fix** Graceful `PlannerError` when LLM returns empty steps (infeasible task)

---

### Verification performed (summary)
- Commands executed:
  - `ruff check src tests` — 0 errors
  - `ruff format --check src tests` — formatted
  - `pytest -q` — 751 passed, 3 deselected, 88% coverage
  - `ag -w review-test runs show <id> --json` — happy-path trace captured
  - `ag -w review-test runs show fake-run-id` — failure-path verified
- Evidence inspected:
  - `env.txt`, `scope_links.md`, `index_diff_notes.md`
  - `ruff_summary.txt`, `pytest_summary.txt`
  - `cli_outputs.txt`, `happy_trace.json`, `failure_trace.json`
  - `bug_triage.md`

---

### Findings
- ✅ What works / improved:
  - Full pipeline trace hardening: executor validation, per-step verification, verifier evidence, planner attribution, pipeline manifest — all integrated and tested
  - Workspace isolation: tests no longer pollute `~/.ag/workspaces/`
  - Truthful UX: all CLI labels verified trace-derived
  - ADR-0009 written: V3 feasibility path is documented for S15
  - Graceful infeasibility handling: empty LLM plan gives user-friendly error instead of schema crash
- ⚠️ Issues found (with severity P0/P1/P2):
  - **P2** `pytest -W error` intermittently fails due to `ddgs`/`primp` SSL socket GC noise (pre-existing, not S14 regression; see `bug_triage.md`)
  - **P2** 7 pre-existing ruff lint errors fixed during review (E501 ×4, E402 ×1, I001 ×1, E501+noqa ×1) — should have been caught at commit time
- 🧩 Follow-ups (AF/BUG/ADR to create):
  - BUG-0021: ddgs/primp SSL socket GC noise causes `pytest -W error` flakiness (P2)
  - BUG-0020: Empty plan reports success (P0, already filed, Sprint 15)
  - AF-0121: V3Planner feasibility assessment (P1, already filed, Sprint 15)
  - AF-0123: V2Verifier LLM semantic checks (P1, already filed, Sprint 15)
  - AF-0124: V2Executor LLM output repair (P2, already filed, Sprint 15)

---

### Decision rationale
All 10 sprint items shipped (8 AFs + 2 BUGs). Full pipeline trace hardening
delivered: executor validation, per-step verification, verifier evidence,
planner attribution, pipeline manifest — all integrated and tested.

Autonomy Gate: all checks pass. Truthful UX verified via 19 CLI tests +
manual spot-check. Workspace isolation confirmed. Coverage 88% (above 85% threshold).

Two P2 issues found — both pre-existing, neither S14 regressions:
1. `pytest -W error` intermittent failure from ddgs/primp SSL socket GC noise → BUG-0021
2. 7 pre-existing ruff lint errors fixed during review → addressed by new two-phase CI workflow in templates

No P0 or P1 issues. Per gate rule: P2-only with follow-ups → ACCEPT WITH FOLLOW-UPS.

Decision rule for autonomy-affecting sprints:
- Open P0 Autonomy Gate failure => `REJECT`
- Open P1/P2 items may allow `ACCEPT WITH FOLLOW-UPS` only if follow-up AF/BUG items are created and indexed

---

### Next actions
- [x] Close sprint (ACCEPT WITH FOLLOW-UPS)
- [x] Follow-up items created and indexed:
  - BUG-0020 (P0, Sprint 15)
  - BUG-0021 (P2, filed)
  - AF-0121, AF-0123, AF-0124 (Sprint 15)
- [ ] Merge feature branch to main
- [ ] Update INDEX_SPRINTS: Sprint 14 → Closed
