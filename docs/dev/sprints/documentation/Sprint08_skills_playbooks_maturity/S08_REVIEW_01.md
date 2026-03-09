# SPRINT REVIEW - S08_REVIEW_01 - skills_playbooks_maturity
# Version number: v0.2

> **Purpose:** This file contains (A) the review tasks Jacob must execute and (B) the final review entry Jeff+Kai use to decide: **ACCEPT / ACCEPT WITH FOLLOW-UPS / REJECT**.
> **Location:** `/docs/dev/sprints/documentation/Sprint08_skills_playbooks_maturity/S08_REVIEW_01.md`

---

## A) Review execution tasks (Jacob)

### Metadata
- **Review ID:** S08_REVIEW_01
- **Scope:** Sprint08
- **Executor:** Jacob
- **Date:** 2026-03-09
- **Commit / tag:** `58547da`
- **Environment:** Windows, Python 3.14.0, pip 25.2

### Inputs (links)
- Sprint description: `S08_DESCRIPTION.md`
- AF items in scope:
  - `/docs/dev/backlog/items/AF0073_DONE_index_file_linking.md`
  - `/docs/dev/backlog/items/AF0079_DONE_skills_framework_v1_removal.md`
  - `/docs/dev/backlog/items/AF0074_DONE_research_v0_playbook.md`
  - `/docs/dev/backlog/items/AF0059_DONE_implement_playbooks_list.md`
  - `/docs/dev/backlog/items/AF0076_DONE_playbooks_registry_cleanup.md`
  - `/docs/dev/backlog/items/AF0069_DONE_skills_registry_deep_dive.md`
  - `/docs/dev/backlog/items/AF0070_DONE_playbooks_registry_deep_dive.md`
- Bug reports (if any):
  - `/docs/dev/bugs/reports/BUG0013_OPEN_research_v0_pipeline_broken.md`
  - `/docs/dev/bugs/reports/BUG0012_OPEN_test_workspace_cleanup.md`
  - `/docs/dev/bugs/reports/BUG0007_OPEN_openai_test_isolation.md`
- Cornerstones (root):
  - `/ARCHITECTURE.md`
  - `/CLI_REFERENCE.md`

### Outputs (paths)
Create an evidence folder:
- `/docs/dev/sprints/documentation/Sprint08_skills_playbooks_maturity/artifacts/`

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

### Pass 0 - Setup & invariants
- [x] Fresh venv; install project
- [x] Record `python --version`
- [x] Record `pip freeze | head -n 50`
- [x] Confirm `ag --help` works
- [x] Confirm manual gate (e.g., `AG_DEV=1`) behavior

Evidence: `env.txt`

---

### Pass 1 - Scope verification (what shipped)
- [x] Confirm each AF file exists in `/docs/dev/backlog/items/`
- [x] Confirm filename Status matches internal Status field
- [x] Confirm each PR maps to exactly one primary AF
- [x] Confirm indices include all new/changed items

Evidence: `scope_links.md`, `index_diff_notes.md`

**Finding:** AF-0059 DONE file missing. INDEX references it but file doesn't exist.
Functionality absorbed into AF-0076.

---

### Pass 2 - Lint/format + test suite verification (authoritative)
- [x] `ruff check src tests`
- [x] `ruff format --check src tests` (or apply `ruff format src tests`)
- [x] `pytest -q`
- [x] `pytest -W error`

Evidence: `pytest_summary.txt`

**Finding:** `pytest -W error` has 1 failure due to unclosed SQLite connections (BUG-0012).
This is a pre-existing issue, not introduced by Sprint 08.

---

### Pass 3 - CLI "truthful UX" spot-check (if CLI touched)
- [x] Run at least one happy-path command and capture output
- [x] Verify labels shown are trace-derived
- [x] Capture trace JSON and confirm it matches labels

Evidence: `cli_outputs.txt`, `happy_trace.json`

**Finding:** All CLI labels (Mode, Status, Verifier, Playbook) verified against trace JSON.
`ag playbooks list` and `ag skills list` commands work correctly.

---

### Pass 4 - Failure-path run (if behavior touched)
- [x] Run a failure-path scenario (invalid workspace / invalid input / etc.)
- [x] Confirm trace records errors
- [x] Confirm CLI output aligns with trace

Evidence: `failure_trace.json`

**Finding:** error_skill correctly records failure in trace. Invalid workspace correctly rejected.

---

### Pass 5 - Bugs triage (if any discovered)
- [x] Create bug reports in `/docs/dev/bugs/reports/` using template
- [x] Link from relevant AF and note in sprint report

Evidence: `bug_triage.md`

**Finding:** BUG-0013 (P1) created for research_v0 pipeline data flow issue.

---

## Jacob completion
- **Executed by:** Jacob
- **Date:** 2026-03-09
- **Evidence folder:** `artifacts/`
- **Notes:**
  - All 5 passes executed successfully
  - 6/7 AF files verified (AF-0059 missing DONE version)
  - 404 tests pass, 1 warning-as-error failure (pre-existing SQLite issue)
  - BUG-0013 filed for research_v0 pipeline
  - Lint fixes applied and committed separately

---

## B) Review entry (Jeff + Kai)

### Review metadata
- **Reviewed by:** Jeff + Kai
- **Date:** 2026-03-09
- **Scope:** Sprint08
- **Decision:** ACCEPT WITH FOLLOW-UPS

---

### What changed (high-level)
- **V1 skills framework removed** (AF-0079): All process-oriented stubs deleted, V2-only architecture
- **research_v0 playbook added** (AF-0074): New playbook with fetch_web_content + synthesize_research skills
- **Playbooks registry cleanup** (AF-0076): Auto-derived list_playbooks(), `ag playbooks list` command
- **Architecture documentation** (AF-0069, AF-0070): Skills/playbooks sections added to ARCHITECTURE.md
- **Index file linking** (AF-0073): Standardized markdown link format in index files

---

### Verification performed (summary)
- Commands executed:
  - `ruff check src tests` → All checks passed (after fixes)
  - `ruff format src tests` → 5 files reformatted
  - `pytest -q` → 404 passed, 3 deselected
  - `pytest -W error` → 1 failure (pre-existing SQLite warning)
- Evidence inspected:
  - `happy_trace.json` → Labels match trace ✅
  - `failure_trace.json` → Errors recorded correctly ✅
  - `cli_outputs.txt` → New commands work ✅

---

### Findings
- What works / improved:
  - `ag playbooks list` shows Rich table with stability markers
  - `ag skills list` shows V2 skill descriptions correctly
  - V1 stub removal eliminates confusion between stub/real skills
  - Architecture documentation explains Skills = Capabilities principle
- Issues found (with severity P0/P1/P2):
  - **P1:** BUG-0013 research_v0 pipeline broken (documents not passed between steps)
  - **P2:** AF-0059 DONE file missing (INDEX integrity issue)
  - **P2:** Duplicate old AF files need cleanup
  - **P2:** BUG-0012 SQLite connection warning in tests (pre-existing)
- Follow-ups (AF/BUG/ADR to create):
  - BUG-0013 (already created): Fix research_v0 pipeline data flow
  - Action: Mark AF-0059 as DROPPED (absorbed into AF-0076)
  - Action: Clean up duplicate AF files

---

### Decision rationale
Sprint delivers significant architectural cleanup (V1 removal) and documentation.
BUG-0013 is a P1 but doesn't block existing functionality — research_v0 is new.
Core features (summarize_v0, CLI commands, V2 skills) work correctly.
Accepting with follow-ups to track BUG-0013 resolution.

---

### Next actions
- [x] Close sprint (ACCEPT WITH FOLLOW-UPS)
- [ ] Fix AF-0059 reference (mark as DROPPED or create DONE file)
- [ ] Clean up duplicate AF files
- [ ] Prioritize BUG-0013 for next sprint
- [ ] Commit lint fixes from review
