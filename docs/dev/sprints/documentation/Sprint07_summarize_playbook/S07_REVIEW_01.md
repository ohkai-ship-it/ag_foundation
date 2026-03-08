# SPRINT REVIEW — S07_REVIEW_01 — summarize_playbook
# Version number: v0.2

> **Purpose:** This file contains (A) the review tasks Jacob must execute and (B) the final review entry Jeff+Kai use to decide: **ACCEPT / ACCEPT WITH FOLLOW-UPS / REJECT**.
> **Location:** `/docs/dev/sprints/documentation/Sprint07_summarize_playbook/S07_REVIEW_01.md`

---

## A) Review execution tasks (Jacob)

### Metadata
- **Review ID:** S07_REVIEW_01
- **Scope:** Sprint07
- **Executor:** Jacob
- **Date:** 2026-03-08
- **Commit / tag:** `06ee456`
- **Environment:** Windows, Python 3.14.0, pip venv

### Inputs (links)
- Sprint description: `S07_DESCRIPTION.md`
- AF items in scope:
  - `/docs/dev/backlog/items/AF0065_*_first_skill_set.md`
  - `/docs/dev/backlog/items/AF0068_*_skills_playbooks_folder_restructure.md`
  - `/docs/dev/backlog/items/AF0066_*_e2e_integration_test.md`
  - `/docs/dev/backlog/items/AF0062_*_trace_llm_model_tracking.md`
  - `/docs/dev/backlog/items/AF0067_*_skill_code_documentation.md`
- Bug reports to watch during review:
  - `/docs/dev/bugs/reports/BUG0007_OPEN_openai_test_isolation.md`
  - `/docs/dev/bugs/reports/BUG0012_OPEN_test_workspace_cleanup.md`
- Cornerstones / governance:
  - `/docs/dev/foundation/FOUNDATION_MANUAL.md`
  - `/docs/dev/foundation/SPRINT_MANUAL.md`
  - `/ARCHITECTURE.md`
  - `/CLI_REFERENCE.md`
  - `/docs/dev/additional/SKILLS_ARCHITECTURE_0.1.md`
  - `/docs/dev/additional/SCHEMA_INVENTORY.md`
  - `/docs/dev/additional/CONTRACT_INVENTORY.md`

### Outputs (paths)
Create an evidence folder:
- `/docs/dev/sprints/documentation/Sprint07_summarize_playbook/artifacts/review_S07_01/`

Required evidence files:
- `env.txt`
- `scope_links.md`
- `pytest_summary.txt`
- `ruff_summary.txt`
- `cli_outputs.txt`
- `happy_trace.json`
- `failure_trace.json`
- `index_diff_notes.md`
- `doc_review_notes.md`
- `bug_triage.md` (if applicable)

---

### Pass 0 — Setup & invariants
Goal: verify the environment and baseline invariants before reviewing Sprint 07 behavior.

- [ ] Create a fresh venv and install project in editable mode
- [ ] Record `python --version`
- [ ] Record `pip freeze | head -n 50`
- [ ] Confirm `ag --help` works
- [ ] Confirm manual mode gate still works:
  - negative case: `ag run --mode manual "gate check"` without `AG_DEV=1` must fail clearly
  - positive case: set `AG_DEV=1` and confirm manual mode is allowed and banner is explicit
- [ ] Record whether OpenAI-backed real-provider review is possible in this environment (`OPENAI_API_KEY` present or not)

Evidence: `env.txt`

---

### Pass 1 — Scope verification (what actually shipped)
Goal: confirm the sprint scope and detect source-of-truth mismatches before judging implementation quality.

- [ ] Confirm Sprint 07 folder and required files exist:
  - `S07_DESCRIPTION.md`
  - `S07_REVIEW_01.md`
  - `S07_PR_01.md`
- [ ] Confirm each Sprint 07 AF file exists in `/docs/dev/backlog/items/`
- [ ] Confirm filename status matches internal `Status:` field for all Sprint 07 AFs
- [ ] Compare `S07_DESCRIPTION.md` against `INDEX_BACKLOG.md` and note any mismatches
  - expected from current sources: AF0065 and AF0068 still appear `READY`, while AF0066 / AF0062 / AF0067 already appear `DONE`
- [ ] Confirm each merged PR maps to exactly one primary AF
- [ ] Confirm index updates exist in all relevant indices:
  - `/docs/dev/backlog/INDEX_BACKLOG.md`
  - `/docs/dev/bugs/INDEX_BUGS.md`
  - `/docs/dev/decisions/INDEX_DECISIONS.md`
  - `/docs/dev/sprints/INDEX_SPRINTS.md`
- [ ] Verify Sprint 07 sprint status is updated appropriately for review state, or explicitly note why not
- [ ] Capture any filename ↔ status or index ↔ file integrity issues as review findings, not assumptions

Evidence: `scope_links.md`, `index_diff_notes.md`

---

### Pass 2 — Lint / format / full test suite verification (authoritative)
Goal: confirm the repo is green before drilling into Sprint 07 feature behavior.

Run and capture exact outputs:

- [ ] `ruff check src tests`
- [ ] `ruff format --check src tests`
- [ ] `pytest -q`
- [ ] `pytest -W error`
- [ ] `pytest --cov=src/ag --cov-report=term-missing`

Review focus while reading failures:
- [ ] Confirm Sprint 07 changes did not regress provider isolation or workspace cleanup
- [ ] Confirm the E2E integration test for `summarize_v0` is present and passes in CI-style conditions
- [ ] Confirm coverage remains at or above the required thresholds

Evidence: `ruff_summary.txt`, `pytest_summary.txt`

---

### Pass 3 — AF-specific code and documentation inspection
Goal: verify each Sprint 07 AF at the file and behavior level before running end-to-end commands.

#### AF0068 — skills/playbooks folder restructure
- [ ] Confirm `src/ag/playbooks/` exists
- [ ] Confirm playbook implementation is split into the intended file structure (for example `summarize_v0.py`)
- [ ] Confirm `core/playbooks.py` or equivalent registry remains present and delegates cleanly
- [ ] Confirm imports and registry wiring are stable after the restructure
- [ ] Confirm no old playbook path is still the de facto source of truth by accident

#### AF0065 — first skill set (`summarize_v0`)
- [ ] Confirm the three skills exist and are wired in sequence:
  - `load_documents`
  - `summarize_docs`
  - `emit_result`
- [ ] Confirm input/output contracts are explicit and align with the skill framework introduced earlier
- [ ] Confirm `load_documents` reads workspace-scoped inputs only
- [ ] Confirm `summarize_docs` uses provider injection rather than hidden direct provider calls
- [ ] Confirm `emit_result` writes an output artifact into the run artifact path
- [ ] Confirm at least one artifact from summarize flow is registered in trace/artifact store

#### AF0062 — trace LLM model tracking
- [ ] Confirm `RunTrace` contains provider/model metadata for real LLM runs
- [ ] Confirm resolution source is recorded or otherwise inspectable for debugging
- [ ] Confirm traces do not invent provider/model labels when model resolution fails

#### AF0066 — E2E integration test
- [ ] Locate the generic/configurable test for `summarize_v0`
- [ ] Confirm it verifies the full chain: playbook → skills → verifier → trace → artifact
- [ ] Confirm it does not depend on live external network in CI path unless intentionally marked/manual

#### AF0067 — skill code documentation
- [ ] Inspect skill modules for docstrings and key inline documentation
- [ ] Confirm docs explain purpose, expected inputs/outputs, and side effects
- [ ] Note any undocumented non-obvious logic that should become a follow-up

Evidence: `doc_review_notes.md`

---

### Pass 4 — Happy-path end-to-end review run (real feature proof)
Goal: prove that Sprint 07 delivers the summarize playbook end to end.

Prepare workspace fixtures:
- [ ] Create a dedicated review workspace for Sprint 07, separate from prior sprint workspaces
- [ ] Place 2–3 small input files into `<workspace>/inputs/` for summarization
- [ ] Record exact filenames used in evidence

Run these checks:
- [ ] Execute `ag run --playbook summarize_v0 "Summarize the input documents" --workspace <review_ws>`
- [ ] Capture the CLI output verbatim
- [ ] Confirm the run completes successfully
- [ ] Capture `run_id`
- [ ] Run `ag runs show <run_id> --json` and store full output as `happy_trace.json`
- [ ] Verify trace shows:
  - playbook `summarize_v0`
  - step execution for the three summarize skills
  - verifier result
  - recorded artifacts
  - LLM provider/model metadata when run in real LLM mode
- [ ] Confirm artifact output exists under the run artifact folder and matches what the CLI claims
- [ ] Confirm any user-visible labels are directly derivable from persisted trace facts

Evidence: `cli_outputs.txt`, `happy_trace.json`

---

### Pass 5 — Failure-path review run
Goal: prove errors remain truthful and workspace-safe.

Run at least two failure scenarios and capture results:

#### Scenario A — invalid playbook or invalid input path
- [ ] Execute a deliberate invalid summarize invocation (for example missing input files, bad glob, or invalid playbook name)
- [ ] Confirm the CLI fails clearly
- [ ] Confirm a trace is produced if the system is designed to persist failed runs here; if not, record exact behavior
- [ ] Confirm no misleading success labels are printed

#### Scenario B — workspace / boundary protection
- [ ] Execute a failure case that exercises workspace isolation or invalid workspace selection
- [ ] Confirm no implicit workspace creation occurs
- [ ] Confirm no files are read outside the active workspace boundary

For both scenarios:
- [ ] Capture the exact CLI output
- [ ] Capture the trace JSON or explicitly note that no trace was created and why
- [ ] Confirm failure output aligns with persisted trace facts

Evidence: `failure_trace.json`, `cli_outputs.txt`

---

### Pass 6 — Index and artifact integrity after review execution
Goal: ensure review execution itself did not hide structural issues.

- [ ] Confirm no stray review artifacts were written outside the Sprint 07 artifacts folder
- [ ] Confirm AF/BUG/SPRINT indices still point to valid files after Sprint 07 changes
- [ ] Confirm Sprint 07 completion state in docs matches what was actually reviewed
- [ ] If review uncovers missing updates, record exact required file edits rather than vague notes

Evidence: `index_diff_notes.md`

---

### Pass 7 — Bugs triage and follow-up recommendations
Goal: turn review findings into actionable backlog hygiene.

- [ ] Create bug reports in `/docs/dev/bugs/reports/` for any genuine defects discovered during review
- [ ] Reuse existing bug IDs only if the issue is truly the same defect; otherwise create new IDs
- [ ] Link each bug to the relevant AF and note it in sprint review findings
- [ ] Propose AF follow-ups for non-bug gaps such as missing docs, incomplete index updates, or cleanup work

Evidence: `bug_triage.md`

---

## Jacob completion
- **Executed by:** Jacob
- **Date:** 2026-03-08
- **Evidence folder:** `artifacts/review_S07_01/`
- **Commit:** `06ee456`
- **Notes:**
  - All 7 passes completed successfully
  - pytest -q: 412 passed, 3 deselected
  - pytest -W error: 2 failures (BUG-0012 SQLite warnings)
  - ruff check: PASS, ruff format: 4 files need formatting
  - Happy-path E2E with real OpenAI: SUCCESS
  - Failure-path tests: PASS (proper errors)
  - Index integrity issues found (AF0065/AF0068 status mismatches)
  - No new critical bugs; BUG-0012 remains open

---

## B) Review entry (Jeff + Kai)

### Review metadata
- **Reviewed by:** Jeff + Kai
- **Date:** YYYY-MM-DD
- **Scope:** Sprint07
- **Decision:** ACCEPT | ACCEPT WITH FOLLOW-UPS | REJECT

---

### What changed (high-level)
- Implemented and/or finalized the first summarize playbook and related Sprint 07 hardening.
- Reviewed playbook/skills file structure, model tracking, E2E coverage, and documentation quality.
- Verified sprint/document/index integrity against the shipped code and review evidence.

---

### Verification performed (summary)
- Commands executed:
  - `ruff check src tests`
  - `ruff format --check src tests`
  - `pytest -q`
  - `pytest -W error`
  - `pytest --cov=src/ag --cov-report=term-missing`
  - `ag run --playbook summarize_v0 ...`
  - `ag runs show <run_id> --json`
- Evidence inspected:
  - `artifacts/review_S07_01/env.txt`
  - `artifacts/review_S07_01/ruff_summary.txt`
  - `artifacts/review_S07_01/pytest_summary.txt`
  - `artifacts/review_S07_01/cli_outputs.txt`
  - `artifacts/review_S07_01/happy_trace.json`
  - `artifacts/review_S07_01/failure_trace.json`
  - `artifacts/review_S07_01/index_diff_notes.md`
  - `artifacts/review_S07_01/doc_review_notes.md`
  - `artifacts/review_S07_01/bug_triage.md` (if created)

---

### Findings
- ✅ What works / improved:
  - ...
- ⚠️ Issues found (with severity P0 / P1 / P2):
  - ...
- 🧩 Follow-ups (AF / BUG / ADR to create):
  - AF____
  - BUG____
  - ADR___

---

### Decision rationale
Why this decision was made.

---

### Next actions
- [ ] Close sprint (if ACCEPT / ACCEPT WITH FOLLOW-UPS)
- [ ] Create follow-up AF / BUG / ADR items and update indices
- [ ] If REJECT: specify blocking issues and required fixes
