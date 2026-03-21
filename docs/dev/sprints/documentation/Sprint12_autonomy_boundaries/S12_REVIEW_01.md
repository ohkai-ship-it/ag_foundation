# SPRINT REVIEW — S12_REVIEW_01 — autonomy_boundaries
# Version number: v0.1

> **Purpose:** This file contains (A) the review tasks Jacob must execute and (B) the final review entry Jeff+Kai use to decide: **ACCEPT / ACCEPT WITH FOLLOW-UPS / REJECT**.
> **Location:** `/docs/dev/sprints/documentation/Sprint12_autonomy_boundaries/S12_REVIEW_01.md`

---

## A) Review execution tasks (Jacob)

### Metadata
- **Review ID:** S12_REVIEW_01
- **Scope:** Sprint12
- **Executor:** Jacob
- **Date:** YYYY-MM-DD
- **Commit / tag:** <hash>
- **Environment:** Windows, Python 3.14.0, venv (.venv)

### Inputs (links)
- Sprint description: `S12_DESCRIPTION.md`
- AF items in scope:
  - `/docs/dev/backlog/items/AF0107_READY_load_documents_md_inputs.md`
  - `/docs/dev/backlog/items/AF0108_READY_unify_summarization_skill.md`
  - `/docs/dev/backlog/items/AF0109_READY_emit_result_strict_content.md`
  - `/docs/dev/backlog/items/AF0110_READY_run_layout_plan_artifacts.md`
- Cornerstones (root): ARCHITECTURE.md, CLI_REFERENCE.md

### Outputs (paths)
Create an evidence folder:
- `/docs/dev/sprints/documentation/Sprint12_autonomy_boundaries/artifacts/review_S12_01/`

Recommended evidence files:
- `env.txt`
- `scope_links.md`
- `pytest_summary.txt`
- `ruff_summary.txt`
- `cli_outputs.txt`
- `happy_trace.json`
- `failure_trace.json`
- `index_diff_notes.md`

---

### Pass 0 — Setup & invariants
- [ ] Fresh venv; install project
- [ ] Record `python --version`
- [ ] Record `pip freeze | head -n 50`
- [ ] Confirm `ag --help` works
- [ ] Confirm `ag plan --help` works

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

### Pass 2.5 — Skill and storage contract verification
- [ ] `load_documents` loads `.md` files under `inputs/` reliably
- [ ] `summarize_docs` is removed from runtime path; summarization uses `synthesize_research`
- [ ] `emit_result` rejects empty/placeholder content and writes no root output on rejection
- [ ] No `-result_result.md` is generated for new runs
- [ ] Plan files are stored under `runs/<run_id>/artifacts/` (not workspace `/plans`)
- [ ] New run layout is exactly:
  - `runs/<run_id>/trace.json`
  - `runs/<run_id>/result.md`
  - `runs/<run_id>/artifacts/*`

Evidence: `cli_outputs.txt`, `happy_trace.json`, `failure_trace.json`

---

### Pass 3 — CLI truthful UX spot-check
- [ ] Run one happy-path command and capture output
- [ ] Verify labels shown are trace-derived
- [ ] Capture trace JSON and confirm it matches labels

Evidence: `cli_outputs.txt`, `happy_trace.json`

---

### Pass 4 — Failure-path run
- [ ] Run failure scenario (empty/stub content emission path)
- [ ] Confirm trace records errors
- [ ] Confirm CLI output aligns with trace

Evidence: `failure_trace.json`

---

### Pass 5 — Bugs triage (if any discovered)
- [ ] Create bug reports in `/docs/dev/bugs/reports/` using template
- [ ] Link from relevant AF and note in sprint report

Evidence: `bug_triage.md` (if needed)

---

## Jacob completion
- **Executed by:** _pending_
- **Date:** _pending_
- **Evidence folder:** `artifacts/review_S12_01/`
- **Notes:** _pending_

---

## B) Review entry (Jeff + Kai)

### Review metadata
- **Reviewed by:** Jeff + Kai
- **Date:** _pending_
- **Scope:** Sprint12
- **Decision:** _pending_

---

### What changed (high-level)
_To be filled after review_

---

### Verification performed (summary)
_To be filled after review_

---

### Findings
_To be filled after review_

---

### Decision rationale
_To be filled after review_

---

### Next actions
- [ ] Close sprint (if ACCEPT/ACCEPT WITH FOLLOW-UPS)
- [ ] Create follow-up AF/BUG/ADR items and update indices
- [ ] If REJECT: specify blocking issues and required fixes
