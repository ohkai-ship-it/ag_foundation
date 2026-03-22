# SPRINT REVIEW — S15_REVIEW_01 — llm_intelligence_layer
# Version number: v0.2

> **Purpose:** This file contains (A) the review tasks Jacob must execute and (B) the final review entry Jeff+Kai use to decide: **ACCEPT / ACCEPT WITH FOLLOW-UPS / REJECT**.
> **Location:** `/docs/dev/sprints/documentation/Sprint15_llm_intelligence_layer/S15_REVIEW_01.md`

---

## A) Review execution tasks (Jacob)

### Metadata
- **Review ID:** S15_REVIEW_01
- **Scope:** Sprint15
- **Executor:** Jacob
- **Date:** 2026-03-22
- **Commit / tag:** `cfd1a0f` (feat/sprint15-llm-intelligence-layer)
- **Environment:** Windows 11, Python 3.14.0, pip venv

### Inputs (links)
- Sprint description: `S15_DESCRIPTION.md`
- AF items in scope (shipped — DONE):
  - `../../backlog/items/AF0121_DONE_v3planner_feasibility_assessment.md`
  - `../../backlog/items/AF0123_DONE_v2_verifier_semantic_checks.md`
  - `../../backlog/items/AF0124_DONE_v2_executor_llm_repair.md`
  - `../../backlog/items/AF0122_DONE_cli_planning_pipeline_display.md`
- Bug reports (FIXED):
  - `../../bugs/reports/BUG0020_FIXED_empty_plan_reports_success.md`
- Cornerstones (root): `ARCHITECTURE.md`, `CLI_REFERENCE.md`
- ⚠️ **Pre-known issues from live testing (2026-03-22):**
  - BUG-0022 (OPEN): V3Planner makes real LLM calls in non-integration tests — some CLI tests are `@pytest.mark.skip`; these skips are expected and intentional
  - BUG-0023 (OPEN): V2Executor logs repair failure via `logging.warning()` (console bleed); V2Verifier semantic scores not visible in CLI
  - BUG-0024 (OPEN): Planner proposes `emit_result` after playbooks that already contain it

### Outputs (paths)
Create an evidence folder:
- `/docs/dev/sprints/documentation/Sprint15_llm_intelligence_layer/artifacts/review_S15_01/`

Required evidence files:
- `env.txt`
- `scope_links.md`
- `pytest_summary.txt`
- `ruff_summary.txt`
- `cli_outputs.txt`
- `happy_trace.json`
- `failure_trace.json`
- `index_diff_notes.md`
- `bug_triage.md`

---

### Pass 0 — Setup & invariants

```powershell
python --version
pip freeze > artifacts/review_S15_01/env.txt
ag --help
```

- [x] Fresh venv; install project (`pip install -e ".[dev]"`)
- [x] Record `python --version` → expected: 3.14.0a6 — **actual: 3.14.0**
- [x] Record `pip freeze` → save to `env.txt`
- [x] Confirm `ag --help` works — **9 subcommands visible** (run, doctor, runs, ws, artifacts, skills, playbooks, config, plan)
- [x] Confirm manual gate: `AG_DEV=1` is NOT set by default; `ag run` in default mode is supervised/guided

Evidence: `env.txt`

---

### Pass 1 — Scope verification (what shipped)

Expected file list (all must exist with DONE status):
```
docs/dev/backlog/items/AF0121_DONE_v3planner_feasibility_assessment.md
docs/dev/backlog/items/AF0123_DONE_v2_verifier_semantic_checks.md
docs/dev/backlog/items/AF0124_DONE_v2_executor_llm_repair.md
docs/dev/backlog/items/AF0122_DONE_cli_planning_pipeline_display.md
docs/dev/bugs/reports/BUG0020_FIXED_empty_plan_reports_success.md
```

- [x] Confirm each AF file exists in `/docs/dev/backlog/items/` with `DONE` in filename — **all 4 confirmed**
- [x] Confirm filename Status matches internal `Status:` field in each file
- [x] Confirm `INDEX_BACKLOG.md` Sprint 15 table shows all 5 items DONE — **confirmed**
- [x] Confirm `INDEX_BUGS.md` shows BUG-0020 FIXED, BUG-0021/0022/0023/0024 OPEN — **confirmed**
- [x] Confirm no stale `READY` versions of S15 AFs remain in `/docs/dev/backlog/items/` — **none found**

> **Note:** BUG-0023 and BUG-0024 were filed during live testing on 2026-03-22 and ARE
> expected to appear in `INDEX_BUGS.md` OPEN table as P2 follow-ups.

Evidence: `scope_links.md`, `index_diff_notes.md`

---

### Pass 2 — Lint/format + test suite verification (authoritative)

```powershell
ruff check src tests 2>&1 | Tee-Object artifacts/review_S15_01/ruff_summary.txt
ruff format --check src tests 2>&1 | Tee-Object -Append artifacts/review_S15_01/ruff_summary.txt
pytest -W error 2>&1 | Tee-Object artifacts/review_S15_01/pytest_summary.txt
pytest --cov=src/ag --cov-report=term-missing 2>&1 | Tee-Object -Append artifacts/review_S15_01/pytest_summary.txt
```

- [x] `ruff check src tests` → **0 errors**
- [x] `ruff format --check src tests` → **0 reformats needed** (69 files already formatted)
- [x] `pytest -W error` → **783 passed, 9 skipped, 0 failed** — BUG-0022 skips as expected
  - ⚠️ During review, 4 tests in `TestInlinePlanConfirmRun` failed (mocked `plan()` after BUG-0023 fix switched code to `plan_with_metadata()`). **Fixed in commit `cfd1a0f`** — not a new production bug.
- [x] `pytest --cov=src/ag --cov-report=term-missing` → **thresholds met**:
  - Overall: **87%** ≥ 85% ✅
  - CLI (`src/ag/cli/`): **78%** ≥ 72% ✅
  - Providers (`src/ag/providers/`): **97%** ≥ 95% ✅
  - Storage (`src/ag/storage/`): **96%** ≥ 95% ✅
  - Core (`src/ag/core/`): **~88% avg** ≥ 85% ✅

> **Expected skip annotations:** Several tests in `test_cli.py` carry
> `@pytest.mark.skip(reason="Flaky in full suite — see BUG-0022")`. These are intentional
> and documented. They should appear as SKIPPED, not FAILED. Count and record them.

Evidence: `ruff_summary.txt`, `pytest_summary.txt`

---

### Pass 2.5 — Autonomy Gate verification

Sprint 15 adds LLM-powered components to the pipeline. Specific checks required:

**V3Planner feasibility (AF-0121):**
- [x] Confirm `test_planner.py` tests for V3Planner feasibility pass — **9/9 feasibility tests pass**
- [x] Confirm `planning.feasibility_level` and `planning.feasibility_score` appear in RunTrace — **confirmed in happy_trace.json** (`feasibility_level: mostly_feasible`, `feasibility_score: 0.7`)
- [x] Confirm `MOSTLY_FEASIBLE` / `PARTIALLY_FEASIBLE` / `NOT_FEASIBLE` labels in CLI output are derived from the trace field — **confirmed via test_cli_truthful.py (19 passed)**

**V2Verifier (AF-0123):**
- [x] Confirm `test_runtime.py` or `test_contracts.py` cover the V2Verifier path — **test_runtime.py: 68 passed**
- [x] Confirm `verifier.evidence.semantic` is written into trace when V2Verifier is used
- [x] Confirm V2Verifier degrades gracefully (V1 result used) when LLM provider is None — covered by test suite

**V2Executor repair (AF-0124):**
- [x] Confirm `test_executor.py` covers the repair path — **test_executor.py: 25 passed**
- [x] Confirm `step.output_data.repair_result` appears in trace for a repaired step
- [x] Confirm BUG-0023a symptom: `logging.WARNING` console output when repair fails — **observed in cli_outputs.txt** (both runs show `LLM-repaired output still invalid for 'load_documents'` on stderr)

**CLI planning/pipeline display (AF-0122):**
- [x] Confirm `test_cli_truthful.py` passes — **19/19 passed**
- [x] Confirm `ag runs show <id>` output includes a **Planning** section — **confirmed**: `Planning — Planner: V3Planner` with tokens/duration/confidence
- [x] Confirm `ag runs show <id>` output includes a **Pipeline** section — **confirmed**: `V3Planner -> V1Orchestrator -> V2Executor -> V2Verifier -> V0Recorder`
- [x] Confirm pipeline labels match `run_trace.pipeline` fields — **confirmed via happy_trace.json**

**Policy / workspace isolation:**
- [x] `test_confirmation_hooks.py` — **15/15 passed**
- [x] `test_storage.py::TestUserWorkspaceNonPollution` — **passes**; workspace isolation confirmed

Evidence: `cli_outputs.txt`, `happy_trace.json`, `failure_trace.json`, `pytest_summary.txt`

---

### Pass 3 — CLI "truthful UX" spot-check

Run the following and capture full terminal output to `cli_outputs.txt`:

```powershell
# Happy path: feasible task — should produce a plan + run
ag run "summarize this text: the quick brown fox"

# Capture the run ID from output, then inspect trace
ag runs list --limit 1
ag runs show <run-id>
ag runs show <run-id> --json > artifacts/review_S15_01/happy_trace.json
```

Verify in `happy_trace.json`:
- [x] `planning.planner` = `"V3Planner"` — **confirmed**: `V3Planner`
- [x] `planning.feasibility_level` = `"MOSTLY_FEASIBLE"` or `"FULLY_FEASIBLE"` — **confirmed**: `mostly_feasible`
- [x] `planning.llm_call.model` is populated (not null) — **confirmed**: `gpt-4o-mini-2024-07-18`
- [x] `planning.llm_call.total_tokens` > 0 — **confirmed**: `1779`
- [x] `pipeline.executor` = `"V2Executor"` — **confirmed**
- [x] `pipeline.verifier` = `"V2Verifier"` — **confirmed**
- [x] CLI Planning section labels match these trace fields — **confirmed via `ag runs show` output**

Verify in CLI output:
- [x] Planning section visible in `ag run` interactive output — **confirmed in cli_outputs.txt**: `Planning: V3Planner (1779 tokens, 6.9s, confidence: 85%)`
- [x] Pipeline arrow notation visible (e.g. `V3Planner → V1Orchestrator → ...`) — **confirmed**: `V3Planner -> V1Orchestrator -> V2Executor -> V2Verifier -> V0Recorder`
- [x] Feasibility level and score shown and match trace — **confirmed**: `Feasibility: Mostly Feasible (70%)`

Evidence: `cli_outputs.txt`, `happy_trace.json`

---

### Pass 4 — Failure-path run

```powershell
# Failure path 1: infeasible task — should report NOT_FEASIBLE or PARTIALLY_FEASIBLE
ag run "access my email account and delete all messages"

# Failure path 2: invalid workspace
ag -w nonexistent-workspace-xyz run "hello"

# Capture trace if one was written
ag runs list --limit 1
ag runs show <run-id> --json > artifacts/review_S15_01/failure_trace.json
```

- [x] Infeasible task: CLI exits cleanly (no Python traceback), message references feasibility — **confirmed**: `Planning failed: Task is not feasible (score: 0.10)` with capability gaps listed
- [x] Invalid workspace: CLI exits 1 with clear message, no crash — **confirmed**: `Error: Workspace 'nonexistent-workspace-xyz' does not exist.`
- [x] `failure_trace.json`: V3Planner in pipeline, status=failure, verifier=failed — **confirmed** (from run `4ddb9655`)
- [x] `final` field in trace is appropriate for the outcome — **confirmed**: `failure`
- [x] BUG-0023a note: `logging.WARNING` line appears in console when repair fails — **documented in cli_outputs.txt**

Evidence: `failure_trace.json`, `cli_outputs.txt`

---

### Pass 5 — Bugs triage

> The following bugs were identified during live testing on 2026-03-22 and are
> pre-documented. Jacob: verify they are present in `INDEX_BUGS.md`, confirm file
> names match, and add any new bugs found during this review pass.

**Pre-filed bugs (verify presence, do NOT re-file):**
| ID | File | Status | Notes |
|---|---|---|---|
| BUG-0022 | `BUG0022_OPEN_v3planner_cli_test_flakiness.md` | OPEN | Causes test skips — expected |
| BUG-0023 | `BUG0023_OPEN_v2_pipeline_evidence_hidden.md` | OPEN | Repair log bleed + semantic scores invisible in CLI |
| BUG-0024 | `BUG0024_OPEN_planner_duplicates_emit_result.md` | OPEN | Planner adds emit_result after playbooks that already have it |

- [x] Confirm all three bug reports exist in `/docs/dev/bugs/reports/` — **all present**
- [x] Confirm all three appear in `INDEX_BUGS.md` OPEN table — **confirmed**
- [x] If any NEW bugs are found during this review execute, file them — **no new bugs filed**; test regression in `TestInlinePlanConfirmRun` treated as BUG-0023 followup (fix committed `cfd1a0f`)

Evidence: `bug_triage.md`

---

## Jacob completion
- **Executed by:** Jacob
- **Date:** 2026-03-22
- **Evidence folder:** `artifacts/review_S15_01/`
- **Notes:** All passes complete. One test regression found and fixed (BUG-0023 followup, commit `cfd1a0f`). BUG-0023a (logging.WARNING repair bleed) and BUG-0024 (emit_result duplication) confirmed observable but pre-known P2 follow-ups. No new P0/P1 issues found. Recommend ACCEPT WITH FOLLOW-UPS.

---

## B) Review entry (Jeff + Kai)

### Review metadata
- **Reviewed by:** Jeff + Kai
- **Date:** 2026-03-22
- **Scope:** Sprint15
- **Decision:** ACCEPT WITH FOLLOW-UPS

---

### What changed (high-level)
- **BUG-0020** Empty plan reports success — fixed: guard added; empty plan now yields `failed` status with clear error message instead of `success`
- **AF-0121** V3Planner: feasibility assessment — two-phase LLM pipeline (feasibility check → plan generation); `PlanningMetadata` extended with `feasibility_level`, `feasibility_score`, `llm_call` (model/tokens/duration); `NOT_FEASIBLE` blocks execution; `PARTIALLY_FEASIBLE` downgrades to best-effort
- **AF-0123** V2Verifier: LLM semantic quality checks — three semantic dimensions (relevance/completeness/consistency) evaluated by LLM after step verification; `SemanticVerification` written to `verifier.evidence.semantic`; graceful degradation to V1 result when LLM unavailable
- **AF-0124** V2Executor: LLM output repair — when schema validation fails after max retries, V2Executor calls LLM to repair output; `RepairResult` (repair_attempted, repair_succeeded, repair_model, repair_tokens, repair_ms) written to `step.output_data.repair_result`; step proceeds or skips based on `required` flag
- **AF-0122** CLI planning and pipeline display — `ag run` summary and `ag runs show` now show a **Planning** section (planner, tokens, duration, confidence, feasibility) and a **Pipeline** section (component arrow notation); all labels derived from `run_trace.planning` and `run_trace.pipeline`

---

### Verification performed (summary)
- Commands executed:
  - `ruff check src tests` → 0 errors
  - `ruff format --check src tests` → 69 files already formatted
  - `pytest -W error --cov=src/ag --cov-report=term-missing` → 783 passed, 9 skipped, 0 failed; 87% coverage
  - `ag run -y "Search for Python programming news"` → happy-path trace `6b3de7bf` (success, verifier passed)
  - `ag run "access my email account and delete all messages"` → NOT_FEASIBLE, clean exit
  - `ag -w nonexistent-workspace-xyz run "hello"` → exit 1, clear error message
  - `ag runs show 6b3de7bf-cf06-44e3-913f-7c509b2e0914` / `--json` → trace verified
- Evidence inspected:
  - `env.txt`, `scope_links.md`, `index_diff_notes.md`
  - `ruff_summary.txt`, `pytest_summary.txt`
  - `cli_outputs.txt`, `happy_trace.json`, `failure_trace.json`
  - `bug_triage.md`

---

### Findings
- ✅ What works / improved:
  - V3Planner feasibility assessment: `feasibility_level`, `feasibility_score`, `llm_call` in trace — correct
  - Planning section in CLI (`ag run` + `ag runs show`): planner name, tokens, duration, confidence — all trace-derived
  - Pipeline section in CLI: `V3Planner -> V1Orchestrator -> V2Executor -> V2Verifier -> V0Recorder` — correct
  - NOT_FEASIBLE path: clean exit with capability gaps, no traceback
  - BUG-0020 fix: empty plan guard confirmed working
  - BUG-0023 (manifest truthfulness) fix: `pipeline.planner = V3Planner` in trace — correct
  - 87% test coverage, 783 tests passing, ruff clean
- ⚠️ Issues found (with severity P0/P1/P2):
  - P2 (pre-known) BUG-0023a: `logging.WARNING` repair failure bleeds to console stderr — observed in cli_outputs.txt
  - P2 (pre-known) BUG-0024: V3Planner proposes `research_v0` with invalid `load_documents` params — LLM repair fails for this step
  - Test regression (BUG-0023 followup): `TestInlinePlanConfirmRun` mocked wrong method — **fixed in `cfd1a0f`**, no production impact
- 🧩 Follow-ups (AF/BUG/ADR to create):
  - AF-0125 — Deterministic test provider (P1, READY, Sprint 16) — unblocks BUG-0022 skips
  - AF-0126 — Executor/verifier LLM trace (P1, READY, Sprint 16) — structured trace for repair + semantic LLM calls
  - BUG-0022 — V3Planner CLI test flakiness (P2, OPEN) — follow-up on BUG-0021 family
  - BUG-0023 — V2 pipeline evidence hidden (P2, OPEN) — repair log bleed + semantic scores invisible
  - BUG-0024 — Planner duplicates emit_result (P2, OPEN)

---

### Decision rationale
No P0 issues. All Autonomy Gate checks passed: labels are trace-derived, workspace isolation confirmed, policy hooks pass, feasibility blocks infeasible tasks cleanly. The two open P2 items (BUG-0023 log bleed, BUG-0024 planner param mismatch) are pre-documented follow-ups with indexed AF items (AF-0125, AF-0126) in the Sprint 16 backlog. Test regression from BUG-0023 fix was caught and corrected during review with no production impact.

Decision rule for autonomy-affecting sprints:
- Open P0 Autonomy Gate failure => `REJECT`
- Open P1/P2 items may allow `ACCEPT WITH FOLLOW-UPS` only if follow-up AF/BUG items are created and indexed

---

### Next actions
- [x] Close sprint — **ACCEPT WITH FOLLOW-UPS**
- [x] Follow-up items created and indexed: AF-0125, AF-0126, BUG-0022, BUG-0023, BUG-0024 all in INDEX
- [ ] Update `S15_DESCRIPTION.md` to **Closed** after PR merge
- [ ] Push updated branch to origin (includes `cfd1a0f` test fix)
