# REVIEW_TASKS_TEMPLATE
# Version number: v0.2

## Purpose
This document is a **review execution checklist** used by the implementer (Jacob) to run the necessary verification steps and to prepare evidence.
It is designed to plug into the **REVIEW_TEMPLATE** (the review entry document).

## How to use
1. Copy this template to a new file: `REVIEW_TASKS_<SCOPE>.md` (example: `REVIEW_TASKS_SPRINT01.md`).
2. Fill in Metadata.
3. Execute passes in order. Do **not** skip passes.
4. Save **all review outputs and evidence artifacts** under:
   - `/docs/dev/reviews/entries/<review_id>/`
   and link them from the final review entry (REVIEW_TEMPLATE output).

## Conventions
- **Truthful UX rule:** any user-visible label must be derivable from **persisted RunTrace facts**.
- **Manual mode rule:** dev/test only; must be **gated**; must be recorded in RunTrace.
- **Workspace isolation rule:** no cross-workspace visibility; prove with tests **and** black-box runs.
- **Evidence rule:** for each behavior PR, record at least one `run_id` + a persisted trace JSON.

---

## Metadata
- **Review ID:** REVIEW-XXXX
- **Scope:** (Sprint / Release / AF item / Bugfix batch)
- **Reviewer:** Jacob
- **Date:** YYYY-MM-DD
- **Repo commit / tag:** (hash)
- **Environment:** OS, Python version, venv tool

## Inputs (links)
- Sprint report:
- Completion notes / handoffs:
- Bug reports:
- Cornerstones (ARCHITECTURE / CLI_REFERENCE / REVIEW_GUIDE / PROJECT_PLAN):

## Outputs (paths)
- Review entry (REVIEW_TEMPLATE output): `/docs/dev/reviews/entries/<review_id>.md`
- Evidence bundle folder: `/docs/dev/reviews/entries/<review_id>/`
  - `env.txt`
  - `scope_links.md`
  - `pytest_summary.txt`
  - `contracts_notes.md`
  - `storage_isolation_transcript.txt`
  - `cli_outputs.txt`
  - `happy_trace.json`
  - `failure_trace.json`
  - `artifacts_outputs.txt` (if applicable)
  - `bug_triage.md`

---

# Pass 0 — Setup & invariants (gate before any testing)
## Goal
Reproduce a clean environment and confirm invariant expectations before running tests.

## Tasks
- [ ] Create a fresh venv and install project (editable install).
- [ ] Record `python --version`.
- [ ] Record `pip freeze | head -n 50` (or equivalent).
- [ ] Confirm `ag --help` works (entrypoint).
- [ ] Confirm manual gate mechanism (e.g., `AG_DEV=1`) and how to enable it.

## Evidence to capture
- [ ] `/docs/dev/reviews/entries/<review_id>/env.txt`
- [ ] Link here:

---

# Pass 1 — Scope verification (what shipped)
## Goal
Confirm that sprint/work items, bugs, and reports match what’s in the repository.

## Tasks
- [ ] List all AF completion notes/handoffs in scope and confirm they exist.
- [ ] Confirm “one PR ↔ one AF item” mapping (where applicable).
- [ ] Confirm bug reports exist and are linked.

## Evidence to capture
- [ ] `/docs/dev/reviews/entries/<review_id>/scope_links.md`
- [ ] Link here:

---

# Pass 2 — Test suite verification (authoritative baseline)
## Goal
Re-run the full test suite and key subsets. This is the primary integrity signal.

## Tasks
- [ ] `pytest -q`
- [ ] `pytest -q -rs` (check skips, xfails)
- [ ] Run targeted subsets as relevant (contracts/storage/runtime/cli/artifacts)

## Evidence to capture
- [ ] `/docs/dev/reviews/entries/<review_id>/pytest_summary.txt`
- [ ] Link here:

---

# Pass 3 — Contracts audit (schemas + evolution guardrails)
## Goal
Verify TaskSpec/RunTrace/Playbook contracts, version fields, JSON round-trip, and evolution constraints.

## Tasks
- [ ] Verify version fields exist in schemas.
- [ ] Verify JSON serialization/deserialization round-trip tests exist and pass.
- [ ] Verify “additive-only” policy is enforced by tests (no rename/remove in v0).
- [ ] Confirm schema fields required for CLI truthful labels exist.

## Evidence to capture
- [ ] `/docs/dev/reviews/entries/<review_id>/contracts_notes.md`
- [ ] Link here:

---

# Pass 4 — Storage & workspace isolation audit
## Goal
Prove strict workspace isolation and storage correctness.

## Tasks (tests)
- [ ] Run storage test subset.
- [ ] Confirm tables/indices exist (runs/artifacts as applicable).

## Tasks (black-box)
- [ ] Create two workspaces: `ws_a`, `ws_b`.
- [ ] Run one task in each and record run IDs.
- [ ] Assert listing and show commands do not leak cross-workspace.
- [ ] Assert on-disk workspace roots are distinct.

## Evidence to capture
- [ ] `/docs/dev/reviews/entries/<review_id>/storage_isolation_transcript.txt`
- [ ] Link here:

---

# Pass 5 — Runtime pipeline audit (interfaces + playbook + skills)
## Goal
Prove the pipeline runs through all modules and that failures are trace-recorded.

## Tasks
- [ ] Confirm interfaces exist (Normalizer/Planner/Orchestrator/Executor/Verifier/Recorder).
- [ ] Confirm `default_v0` playbook exists and is linear.
- [ ] Confirm at least one stub skill exists (e.g., echo).
- [ ] Run happy-path and failure-path runs and persist traces.

## Evidence to capture
- [ ] `/docs/dev/reviews/entries/<review_id>/happy_trace.json`
- [ ] `/docs/dev/reviews/entries/<review_id>/failure_trace.json`
- [ ] Link here:

---

# Pass 6 — CLI “truthful UX” audit
## Goal
Prove CLI outputs are derived from persisted RunTrace facts and manual gating is correct.

## Tasks
- [ ] Verify `--mode manual` requires `AG_DEV=1` and fails clearly without it.
- [ ] Verify manual banner is printed for human output.
- [ ] Verify `ag runs show <id> --json` outputs valid RunTrace JSON.
- [ ] Validate labels (mode, verifier.status, duration, playbook name/version) match trace fields.

## Evidence to capture
- [ ] `/docs/dev/reviews/entries/<review_id>/cli_outputs.txt`
- [ ] Link here:

---

# Pass 7 — Artifacts audit (if in scope)
## Goal
Validate artifact registration/listing is stable, and no leakage occurs.

## Tasks
- [ ] Run an artifact-producing run (if implemented).
- [ ] `ag artifacts list --run <id> --workspace <ws>` (human + `--json` if supported).
- [ ] Verify empty-list behavior is stable for runs without artifacts.

## Evidence to capture
- [ ] `/docs/dev/reviews/entries/<review_id>/artifacts_outputs.txt`
- [ ] Link here:

---

# Pass 8 — Bug triage and spec compliance table
## Goal
Classify each open bug as **defect** vs **deferred scope** and ensure follow-up tracking exists.

## Tasks
- [ ] For each bug: reproduce (if feasible), record expected vs actual, severity, and recommended follow-up.
- [ ] Create a “Spec compliance” table:
  - Requirement
  - Current behavior
  - Classification (Defect / Deferred)
  - Follow-up AF/BUG ID

## Evidence to capture
- [ ] `/docs/dev/reviews/entries/<review_id>/bug_triage.md`
- [ ] Link here:

---

## Finalization — Produce the review entry (REVIEW_TEMPLATE)
## Goal
Summarize results and provide a strict accept/reject decision for the reviewed scope.

## Tasks
- [ ] Fill REVIEW_TEMPLATE using outputs from all passes.
- [ ] Decision must be one of: **ACCEPT / ACCEPT WITH FOLLOW-UPS / REJECT**
- [ ] If not ACCEPT: list blocking issues and exact follow-up item IDs.

## Deliverables checklist
- [ ] Review entry created: `/docs/dev/reviews/entries/<review_id>.md`
- [ ] Evidence bundle folder complete: `/docs/dev/reviews/entries/<review_id>/`
- [ ] Links cross-referenced between entry and evidence bundle
