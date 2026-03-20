# SPRINT REVIEW — S11_REVIEW_01 — guided_autonomy_enablement
# Version number: v0.1

> **Purpose:** This file contains (A) the review tasks Jacob must execute and (B) the final review entry Jeff+Kai use to decide: **ACCEPT / ACCEPT WITH FOLLOW-UPS / REJECT**.
> **Location:** `/docs/dev/sprints/documentation/Sprint11_guided_autonomy_enablement/S11_REVIEW_01.md`

---

## A) Review execution tasks (Jacob)

### Metadata
- **Review ID:** S11_REVIEW_01
- **Scope:** Sprint11
- **Executor:** Jacob
- **Date:** _pending_
- **Commit / tag:** _pending_
- **Environment:** Windows, Python 3.14.0, venv (.venv)

### Inputs (links)
- Sprint description: `S11_DESCRIPTION.md`
- AF items in scope:
  - `/docs/dev/backlog/items/AF0098_*_plan_preview_command.md`
  - `/docs/dev/backlog/items/AF0099_*_plan_approval_workflow.md`
  - `/docs/dev/backlog/items/AF0100_*_step_confirmation_hooks.md`
  - `/docs/dev/backlog/items/AF0094_*_trace_full_io_enrichment.md`
  - `/docs/dev/backlog/items/AF0097_*_runs_default_workspace.md`
  - `/docs/dev/backlog/items/AF0101_*_autonomy_level_display.md`
- Bug fixes:
  - `/docs/dev/bugs/reports/BUG0015_*_runs_list_count_mismatch.md`
- Cornerstones (root): ARCHITECTURE.md, CLI_REFERENCE.md

### Outputs (paths)
Create an evidence folder:
- `/docs/dev/sprints/documentation/Sprint11_guided_autonomy_enablement/artifacts/review_S11_01/`

---

### Pass 0 — Setup & invariants
- [ ] Fresh venv; install project
- [ ] Record `python --version`
- [ ] Record `pip freeze | head -n 50`
- [ ] Confirm `ag --help` works
- [ ] Confirm `ag plan --help` works (new command)

Evidence: `env.txt`

---

### Pass 1 — Scope verification
- [ ] Confirm each AF file exists with correct status
- [ ] Confirm indices updated
- [ ] Confirm CLI_REFERENCE updated for new commands

Evidence: `scope_links.md`

---

### Pass 2 — Lint/format + test suite
- [ ] `ruff check src tests`
- [ ] `ruff format --check src tests`
- [ ] `pytest -q`
- [ ] `pytest -W error`

Evidence: `ruff_summary.txt`, `pytest_summary.txt`

---

### Pass 3 — Plan preview (AF-0098)
- [ ] `ag plan --task "Research Berlin" --workspace demo` generates plan
- [ ] Plan output shows skills, estimated tokens, policy flags
- [ ] `ag plan show <plan_id>` displays plan
- [ ] `ag plans list --workspace demo` shows pending plans
- [ ] `ag plan delete <plan_id>` removes plan

Evidence: `plan_preview_test.txt`

---

### Pass 4 — Plan approval (AF-0099)
- [ ] `ag run --plan <plan_id>` executes plan
- [ ] Expired plan rejected with error
- [ ] Trace includes `plan_id` reference
- [ ] `--plan` and `--task` mutually exclusive

Evidence: `plan_approval_test.txt`

---

### Pass 5 — Confirmation hooks (AF-0100)
- [ ] Configure workspace confirmation policy
- [ ] Flagged step prompts for confirmation
- [ ] `--yes` bypasses confirmation
- [ ] Confirmation logged in trace

Evidence: `confirmation_test.txt`

---

### Pass 6 — Observability (AF-0094, BUG-0015, AF-0101)
- [ ] Trace includes LLM token counts
- [ ] Full step I/O in trace
- [ ] `ag runs list` count matches displayed rows
- [ ] Autonomy mode displayed in CLI
- [ ] Autonomy in trace

Evidence: `observability_test.txt`

---

## Jacob completion
- **Executed by:** _pending_
- **Date:** _pending_
- **Evidence folder:** `artifacts/review_S11_01/`
- **Notes:** _pending_

---

## B) Review entry (Jeff + Kai)

### Review metadata
- **Reviewed by:** Jeff + Kai
- **Date:** _pending_
- **Scope:** Sprint11
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
- [ ] Execute review passes (Jacob)
- [ ] Decision: ACCEPT / ACCEPT WITH FOLLOW-UPS / REJECT
- [ ] Close sprint (if ACCEPT/ACCEPT WITH FOLLOW-UPS)
- [ ] Update INDEX_SPRINTS status to Closed
