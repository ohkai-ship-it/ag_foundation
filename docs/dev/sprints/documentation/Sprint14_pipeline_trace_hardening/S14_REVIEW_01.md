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
- **Date:** YYYY-MM-DD
- **Commit / tag:** <hash>
- **Environment:** OS, Python version, venv tool

### Inputs (links)
- Sprint description: `S14_DESCRIPTION.md`
- AF items in scope:
  - `docs/dev/backlog/items/AF0116_READY_v1_executor_output_validation.md`
  - `docs/dev/backlog/items/AF0117_READY_v1_orchestrator_perstep_loop.md`
  - `docs/dev/backlog/items/AF0118_READY_v1_recorder_verification_evidence.md`
  - `docs/dev/backlog/items/AF0096_READY_test_workspace_cleanup.md`
  - `docs/dev/backlog/items/AF0104_READY_llm_planner_v3_feasibility.md`
  - `docs/dev/backlog/items/AF0113_READY_per_step_output_verification.md`
  - `docs/dev/backlog/items/AF0119_READY_planner_trace_llm_attribution.md`
  - `docs/dev/backlog/items/AF0120_READY_component_manifest_trace.md`
- Bug reports:
  - `docs/dev/bugs/reports/BUG0018_OPEN_v2planner_misclassifies_playbook.md`
  - `docs/dev/bugs/reports/BUG0019_OPEN_orchestrator_drops_required_flag.md`
- Cornerstones (root): ARCHITECTURE.md, CLI_REFERENCE.md

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
- [ ] Fresh venv; install project
- [ ] Record `python --version`
- [ ] Record `pip freeze | head -n 50`
- [ ] Confirm `ag --help` works
- [ ] Confirm manual gate (e.g., `AG_DEV=1`) behavior

Evidence: `env.txt`

---

### Pass 1 — Scope verification (what shipped)
- [ ] Confirm each AF file exists in `/docs/dev/backlog/items/`
- [ ] Confirm filename Status matches internal Status field
- [ ] Confirm each PR maps to exactly one primary AF
- [ ] Confirm indices include all new/changed items

Evidence: `scope_links.md`, `index_diff_notes.md`

---

### Pass 2 — Lint/format + test suite verification (authoritative)
- [ ] `ruff check src tests`
- [ ] `ruff format --check src tests`
- [ ] `pytest -q`
- [ ] `pytest -W error`

Evidence: `ruff_summary.txt`, `pytest_summary.txt`

---

### Pass 2.5 — Autonomy Gate verification (if behavior touched)
- [ ] Verify all user-visible labels are trace-derived
- [ ] Verify policy checks are enforced where applicable (permission/confirmation/budget)
- [ ] Verify retry/timeout/failure behavior is trace-aligned
- [ ] Verify workspace isolation under failure-path scenarios

Evidence: `cli_outputs.txt`, `happy_trace.json`, `failure_trace.json`, `pytest_summary.txt`

---

### Pass 3 — CLI "truthful UX" spot-check (if CLI touched)
- [ ] Run at least one happy-path command and capture output
- [ ] Verify labels shown are trace-derived
- [ ] Capture trace JSON and confirm it matches labels

Evidence: `cli_outputs.txt`, `happy_trace.json`

---

### Pass 4 — Failure-path run (if behavior touched)
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
- **Evidence folder:** `artifacts/review_S14_01/`
- **Notes:** ...

---

## B) Review entry (Jeff + Kai)

### Review metadata
- **Reviewed by:** Jeff + Kai
- **Date:** YYYY-MM-DD
- **Scope:** Sprint14
- **Decision:** ACCEPT | ACCEPT WITH FOLLOW-UPS | REJECT

---

### What changed (high-level)
- ...

---

### Verification performed (summary)
- Commands executed:
  - `ruff ...`
  - `pytest ...`
- Evidence inspected:
  - `run_...`
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
  - ADR___

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
