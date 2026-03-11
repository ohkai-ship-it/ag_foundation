# SPRINT REVIEW — S09_REVIEW_01 — reliability_safety_hardening
# Version number: v0.2

> **Purpose:** This file contains (A) the review tasks Jacob must execute and (B) the final review entry Jeff+Kai use to decide: **ACCEPT / ACCEPT WITH FOLLOW-UPS / REJECT**.
> **Location:** `/docs/dev/sprints/documentation/Sprint09_reliability_safety_hardening/S09_REVIEW_01.md`

---

## A) Review execution tasks (Jacob)

### Metadata
- **Review ID:** S09_REVIEW_01
- **Scope:** Sprint09
- **Executor:** Jacob
- **Date:** 2026-03-11
- **Commit / tag:** working tree review
- **Environment:** Windows, Python 3.14.0, venv (.venv)

### Inputs (links)
- Sprint description: `S09_DESCRIPTION.md`
- AF items in scope:
	- `/docs/dev/backlog/items/AF0046_DONE_test_isolation_framework.md`
	- `/docs/dev/backlog/items/AF0071_DONE_warning_clean_test_discipline.md`
	- `/docs/dev/backlog/items/AF0085_DONE_cli_consistency_audit.md`
	- `/docs/dev/backlog/items/AF0087_DONE_policy_hook_validation.md`
	- `/docs/dev/backlog/items/AF0086_DONE_test_suite_audit.md`
	- `/docs/dev/backlog/items/AF0072_DONE_playbook_validation_error.md`
	- `/docs/dev/backlog/items/AF0015_DONE_resolve_storage_db.md`
	- `/docs/dev/backlog/items/AF0083_DONE_artifact_evidence_strategy.md`
	- `/docs/dev/backlog/items/AF0057_DONE_playbook_artifacts_in_trace.md`
	- `/docs/dev/backlog/items/AF0064_DONE_process_documentation_hardening.md`
- Bug reports (if any):
	- `/docs/dev/bugs/reports/BUG0007_FIXED_openai_test_isolation.md`
	- `/docs/dev/bugs/reports/BUG0012_OPEN_test_workspace_cleanup.md`
	- `/docs/dev/bugs/reports/BUG0002_Open_missing_ag_run.md`
	- `/docs/dev/bugs/reports/BUG0003_Open_missing_cli_subcommands.md`
	- `/docs/dev/bugs/reports/BUG0011_Open_default_workspace_name_leaked.md`
- Cornerstones (root): ARCHITECTURE.md, CLI_REFERENCE.md, REVIEW_GUIDE.md (as applicable)

### Outputs (paths)
Create an evidence folder:
- `/docs/dev/sprints/documentation/Sprint09_reliability_safety_hardening/artifacts/review_S09_01/`

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
- [x] Record `python --version`
- [x] Record `pip freeze | head -n 50`
- [x] Confirm `ag --help` works
- [x] Confirm manual gate (e.g., `AG_DEV=1`) behavior

Evidence: `env.txt`

---

### Pass 1 — Scope verification (what shipped)
- [x] Confirm each AF file exists in `/docs/dev/backlog/items/`
- [x] Confirm filename Status matches internal Status field
- [ ] Confirm each PR maps to exactly one primary AF
- [x] Confirm indices include all new/changed items

Evidence: `scope_links.md`, `index_diff_notes.md`

---

### Pass 2 — Lint/format + test suite verification (authoritative)
- [x] `ruff check src tests`
- [x] `ruff format --check src tests` (or apply `ruff format src tests`)
- [x] `pytest -q`
- [x] `pytest -W error`

Evidence: `ruff_summary.txt`, `pytest_summary.txt`

---

### Pass 2.5 — Autonomy Gate verification (if behavior touched)
- [x] Verify all user-visible labels are trace-derived
- [x] Verify policy checks are enforced where applicable (permission/confirmation/budget)
- [x] Verify retry/timeout/failure behavior is trace-aligned
- [x] Verify workspace isolation under failure-path scenarios

Evidence: `cli_outputs.txt`, `happy_trace.json`, `failure_trace.json`, `pytest_summary.txt`

---

### Pass 3 — CLI “truthful UX” spot-check (if CLI touched)
- [x] Run at least one happy-path command and capture output
- [x] Verify labels shown are trace-derived
- [x] Capture trace JSON and confirm it matches labels

Evidence: `cli_outputs.txt`, `happy_trace.json`

---

### Pass 4 — Failure-path run (if behavior touched)
- [x] Run a failure-path scenario (invalid workspace / invalid input / etc.)
- [x] Confirm trace records errors
- [x] Confirm CLI output aligns with trace

Evidence: `failure_trace.json`

---

### Pass 5 — Bugs triage (if any discovered)
- [x] Create bug reports in `/docs/dev/bugs/reports/` using template
- [x] Link from relevant AF and note in sprint report

Evidence: `bug_triage.md`

---

## Jacob completion
- **Executed by:** Jacob
- **Date:** 2026-03-11
- **Evidence folder:** `artifacts/review_S09_01/`
- **Notes:**
	- Passes executed with evidence captured.
	- Tests pass (`449 passed, 3 deselected`), but lint/format checks are not clean.
	- Manual review findings captured in issues list and bug triage notes.

---

## B) Review entry (Jeff + Kai)

### Review metadata
- **Reviewed by:** Jeff + Kai
- **Date:** 2026-03-11
- **Scope:** Sprint09
- **Decision:** REJECT

---

### What changed (high-level)
- Reliability/safety hardening AF set is present in backlog scope and files.
- Runtime/test/CLI behavior was exercised via happy and failure-path commands with trace evidence.
- Pass 2 quality gate remains non-green due lint/format violations.

---

### Verification performed (summary)
- Commands executed:
	- `ruff check src tests`
	- `ruff format --check src tests`
	- `pytest -q`
	- `pytest -W error`
	- `ag run --playbook research_v0 "Research the Düsseldorf meteorite"`
	- `ag runs list --workspace test-meta-ws`
	- `ag run --playbook nonexistent_playbook "Test invalid playbook" --workspace skills01`
- Evidence inspected:
	- `env.txt`
	- `scope_links.md`
	- `index_diff_notes.md`
	- `ruff_summary.txt`
	- `pytest_summary.txt`
	- `cli_outputs.txt`
	- `happy_trace.json`
	- `failure_trace.json`
	- `bug_triage.md`

---

### Findings
- What works / improved:
	- Scope files exist and filename/internal status alignment is OK for Sprint09 AFs.
	- Test suite passes in both standard and warnings-as-errors runs (`449 passed, 3 deselected`).
	- Invalid playbook now fails with explicit error and available-playbooks hint.
- Issues found (with severity P0/P1/P2):
	- **P2:** `ag runs list --workspace test-meta-ws` appears truncated to 10 rows without explicit pagination indicator (for example, showing `N` of total rows or guidance for `--all`/`--offset`). This reduces run-history visibility during manual review.
	- **P1:** `ag run --playbook research_v0 "Research the Düsseldorf meteorite"` shows no material output difference versus pre-sprint baseline; trace, artifact, and report behavior appear unchanged from before.
	- **P1:** Pass 2 quality gate failed: `ruff check` reports import issues in `tests/test_artifacts.py`, and `ruff format --check` reports formatting drift in `src/ag/cli/main.py`.
	- **P2:** Trace summary encoding/readability issue observed (`Düsseldorf` shown as `D³sseldorf` in `happy_trace.json`).
- Follow-ups (AF/BUG/ADR to create):
	- AF-0088 (runs list pagination/total indicator)
	- AF-0089 (report output path/format truthfulness)
	- BUG-0014 (trace summary encoding degradation)

---

### Decision rationale
Sprint09 cannot be accepted in current state because the authoritative quality gate (Pass 2 lint/format) is not green.
In addition, review identified unresolved user-visible behavior gaps (runs list truncation signaling, report output UX, and trace encoding readability).
Given unresolved P1 issues and non-green CI-equivalent checks, decision is `REJECT` pending corrective changes and re-review evidence.

Decision rule for autonomy-affecting sprints:
- Open P0 Autonomy Gate failure => `REJECT`
- Open P1/P2 items may allow `ACCEPT WITH FOLLOW-UPS` only if follow-up AF/BUG items are created and indexed

---

### Next actions
- [ ] Close sprint (if ACCEPT/ACCEPT WITH FOLLOW-UPS)
- [ ] Create follow-up AF/BUG/ADR items and update indices
- [x] If REJECT: specify blocking issues and required fixes
