# SPRINT REVIEW — S13_REVIEW_01 — intelligent_pipeline
# Version number: v0.2

> **Purpose:** This file contains (A) the review tasks Jacob must execute and (B) the final review entry Jeff+Kai use to decide: **ACCEPT / ACCEPT WITH FOLLOW-UPS / REJECT**.  
> **Location:** `/docs/dev/sprints/documentation/Sprint13_intelligent_pipeline/S13_REVIEW_01.md`

---

## A) Review execution tasks (Jacob)

### Metadata
- **Review ID:** S13_REVIEW_01
- **Scope:** Sprint13 — intelligent_pipeline
- **Executor:** Jacob
- **Date:** 2026-03-22
- **Commit / tag:** `04b1e9e` (HEAD of `feat/sprint13-intelligent-pipeline`)
- **Environment:** Windows, Python 3.x, venv

### Inputs (links)
- Sprint description: [`S13_DESCRIPTION.md`](S13_DESCRIPTION.md)
- AF items in scope:
  - [`AF0114_DONE_extract_pipeline_v0_files.md`](../../backlog/items/AF0114_DONE_extract_pipeline_v0_files.md)
  - [`AF0115_DONE_v1_verifier_step_aware.md`](../../backlog/items/AF0115_DONE_v1_verifier_step_aware.md)
  - [`AF0103_DONE_llm_planner_v2_playbooks.md`](../../backlog/items/AF0103_DONE_llm_planner_v2_playbooks.md)
  - [`AF0117_DONE_v1_orchestrator_perstep_loop.md`](../../backlog/items/AF0117_DONE_v1_orchestrator_perstep_loop.md) (partial — Sprint 13 scope only)
  - [`AF0112_DONE_inline_plan_confirm_run.md`](../../backlog/items/AF0112_DONE_inline_plan_confirm_run.md) (pre-existing DONE, merged in prior PR)
- Bug reports: BUG-0017 (fix included in AF-0115)
- Cornerstones: ARCHITECTURE.md, CLI_REFERENCE.md

### Outputs (paths)
Evidence folder:
- `/docs/dev/sprints/documentation/Sprint13_intelligent_pipeline/artifacts/review_S13_01/`

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
- [ ] Fresh venv; install project (`pip install -e ".[dev]"`)
- [ ] Record `python --version`
- [ ] Record `pip freeze | head -n 50`
- [ ] Confirm `ag --help` works
- [ ] Confirm manual gate (`AG_DEV=1`) behavior

Evidence: `env.txt`

---

### Pass 1 — Scope verification (what shipped)
- [ ] Confirm each AF file exists in `/docs/dev/backlog/items/`:
  - [ ] `AF0114_DONE_extract_pipeline_v0_files.md`
  - [ ] `AF0115_DONE_v1_verifier_step_aware.md`
  - [ ] `AF0103_DONE_llm_planner_v2_playbooks.md`
  - [ ] `AF0117_DONE_v1_orchestrator_perstep_loop.md`
- [ ] Confirm filename Status matches internal Status field for all four
- [ ] Confirm each commit maps to exactly one primary AF:
  - `08988ca` → AF-0114
  - `373d01b` + `a8b32c8` → AF-0115
  - `464e0f8` → AF-0103 + AF-0117 (partial)
  - `9c60be9` → Sprint 13 setup
  - `04b1e9e` → INDEX/status updates
- [ ] Confirm indices include all new/changed items:
  - [ ] `INDEX_BACKLOG.md` — Sprint 13 section shows all 5 items as DONE
  - [ ] `INDEX_SPRINTS.md` — Sprint 13 row present, status = In Progress
- [ ] **Stale file check:** Verify no leftover READY copies exist:
  - [ ] `AF0103_READY_llm_planner_v2_playbooks.md` — should NOT exist (delete if found)
  - [ ] `AF0117_READY_v1_orchestrator_perstep_loop.md` — should NOT exist (delete if found)

Evidence: `scope_links.md`, `index_diff_notes.md`

---

### Pass 2 — Lint/format + test suite verification (authoritative)
- [ ] `ruff check src tests`
- [ ] `ruff format --check src tests` (or apply `ruff format src tests`)
- [ ] `pytest -q`
- [ ] `pytest -W error`

Evidence: `ruff_summary.txt`, `pytest_summary.txt`

---

### Pass 2.5 — Autonomy Gate verification (behavior touched)

> Sprint 13 touches Planner, Orchestrator, and Verifier — autonomy gate is **mandatory**.

- [ ] Verify all user-visible labels are trace-derived
- [ ] Verify policy checks are enforced where applicable (permission/confirmation/budget)
- [ ] Verify retry/timeout/failure behavior is trace-aligned
- [ ] Verify workspace isolation under failure-path scenarios
- [ ] Verify V1Verifier correctly handles required vs optional steps
- [ ] Verify V2Planner produces valid plans with PLAYBOOK step types
- [ ] Verify V1Orchestrator expands playbook steps correctly

Evidence: `cli_outputs.txt`, `happy_trace.json`, `failure_trace.json`, `pytest_summary.txt`

---

### Pass 3 — CLI "truthful UX" spot-check (CLI touched via planner/orchestrator)
- [ ] Run at least one happy-path command and capture output
- [ ] Verify labels shown are trace-derived
- [ ] Capture trace JSON and confirm it matches labels

Evidence: `cli_outputs.txt`, `happy_trace.json`

---

### Pass 4 — Failure-path run (behavior touched)
- [ ] Run a failure-path scenario (invalid workspace / invalid input / etc.)
- [ ] Confirm trace records errors
- [ ] Confirm CLI output aligns with trace

Evidence: `failure_trace.json`

---

### Pass 5 — Bugs triage (if any discovered)
- [ ] Create bug reports in `/docs/dev/bugs/reports/` using template
- [ ] Link from relevant AF and note in sprint report

Evidence: `bug_triage.md`

---

## Jacob completion
- **Executed by:** Jacob
- **Date:** YYYY-MM-DD
- **Evidence folder:** `artifacts/review_S13_01/`
- **Notes:** ...

---

## B) Review entry (Jeff + Kai)

### Review metadata
- **Reviewed by:** Jeff + Kai
- **Date:** YYYY-MM-DD
- **Scope:** Sprint13 — intelligent_pipeline
- **Decision:** ACCEPT | ACCEPT WITH FOLLOW-UPS | REJECT

---

### What changed (high-level)
- AF-0114: Extracted monolithic runtime.py into dedicated V0 component files (V0Planner, V0Orchestrator, V0Executor, V0Recorder, V0Verifier)
- AF-0115: V1Verifier with step-aware verification, required/optional step handling, BUG-0017 fix, 9 contract tests
- AF-0103: V2Planner composing mixed skill+playbook plans with PLAYBOOK step type
- AF-0117 (partial): V1Orchestrator handling mixed plan execution with inline playbook expansion

---

### Verification performed (summary)
- Commands executed:
  - `ruff check src tests`
  - `ruff format --check src tests`
  - `pytest -W error`
  - `pytest --cov=src/ag --cov-report=term-missing`
- Evidence inspected:
  - `...`

---

### Findings
- ✅ What works / improved:
  - ...
- ⚠️ Issues found (with severity P0/P1/P2):
  - ...
- 🧩 Follow-ups (AF/BUG/ADR to create):
  - AF____
  - BUG____

---

### Decision rationale
Why this decision was made.

Decision rule for autonomy-affecting sprints:
- Open P0 Autonomy Gate failure => `REJECT`
- Open P1/P2 items may allow `ACCEPT WITH FOLLOW-UPS` only if follow-up AF/BUG items are created and indexed

---

### Next actions
- [ ] Close sprint (if ACCEPT/ACCEPT WITH FOLLOW-UPS)
- [ ] Create follow-up AF/BUG/ADR items and update indices
- [ ] If REJECT: specify blocking issues and required fixes
