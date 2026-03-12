# SPRINT REVIEW — S10_REVIEW_01 — gate_b_readiness
# Version number: v0.2

> **Purpose:** This file contains (A) the review tasks Jacob must execute and (B) the final review entry Jeff+Kai use to decide: **ACCEPT / ACCEPT WITH FOLLOW-UPS / REJECT**.
> **Location:** `/docs/dev/sprints/documentation/Sprint10_gate_b_readiness/S10_REVIEW_01.md`

---

## A) Review execution tasks (Jacob)

### Metadata
- **Review ID:** S10_REVIEW_01
- **Scope:** Sprint10
- **Executor:** Jacob
- **Date:** 2026-03-12
- **Commit / tag:** working tree review
- **Environment:** Windows, Python 3.14.0, venv (.venv)

### Inputs (links)
- Sprint description: `S10_DESCRIPTION.md`
- AF items in scope:
  - `/docs/dev/backlog/items/AF0090_DONE_artifact_evidence_deepdive.md`
  - `/docs/dev/backlog/items/AF0091_DONE_verifier_failure_path_maturity.md`
  - `/docs/dev/backlog/items/AF0093_DONE_skills_test_coverage_hardening.md`
  - `/docs/dev/backlog/items/AF0012_DONE_cli_reference_surface.md`
  - `/docs/dev/backlog/items/AF0081_DONE_inventory_sync_discipline.md`
  - `/docs/dev/backlog/items/AF0082_DONE_human_readable_result.md`
  - `/docs/dev/backlog/items/AF0084_DONE_index_link_emoji_fix.md`
  - `/docs/dev/backlog/items/AF0077_DONE_skills_plugin_architecture.md`
  - `/docs/dev/backlog/items/AF0078_DONE_playbooks_plugin_architecture.md`
  - `/docs/dev/backlog/items/AF0036_DONE_remove_global_cli.md` (completed during planning)
- ADR created:
  - `/docs/dev/decisions/files/ADR008_ACCEPTED_cli_global_flags.md`
- Bug reports discovered during sprint:
  - `/docs/dev/bugs/reports/BUG0015_OPEN_runs_list_count_mismatch.md`
- New backlog items from testing:
  - `/docs/dev/backlog/items/AF0094_PROPOSED_trace_full_io_enrichment.md`
  - `/docs/dev/backlog/items/AF0095_PROPOSED_research_v0_skill_output_audit.md`
- Cornerstones (root): ARCHITECTURE.md, CLI_REFERENCE.md, REVIEW_GUIDE.md

### Outputs (paths)
Create an evidence folder:
- `/docs/dev/sprints/documentation/Sprint10_gate_b_readiness/artifacts/review_S10_01/`

Recommended evidence files:
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
- [ ] Confirm ADR008 is in INDEX_DECISIONS.md

Evidence: `scope_links.md`, `index_diff_notes.md`

---

### Pass 2 — Lint/format + test suite verification (authoritative)
- [ ] `ruff check src tests`
- [ ] `ruff format --check src tests` (or apply `ruff format src tests`)
- [ ] `pytest -q`
- [ ] `pytest -W error`
- [ ] Verify skills coverage thresholds (AF-0093):
  - [ ] fetch_web_content ≥80%
  - [ ] web_search ≥80%
  - [ ] synthesize_research ≥90%

Evidence: `ruff_summary.txt`, `pytest_summary.txt`

---

### Pass 2.5 — Autonomy Gate verification (Gate B focus)
- [ ] Verify all user-visible labels are trace-derived
- [ ] Verify policy checks are enforced where applicable (permission/confirmation/budget)
- [ ] Verify retry/timeout/failure behavior is trace-aligned
- [ ] Verify workspace isolation under failure-path scenarios
- [ ] Verify artifact metadata truthfulness (AF-0090):
  - [ ] artifact_type matches actual file format
  - [ ] artifacts stored in `runs/<id>/artifacts/` directory
- [ ] Verify verifier failure-path consistency (AF-0091)

Evidence: `cli_outputs.txt`, `happy_trace.json`, `failure_trace.json`, `pytest_summary.txt`

---

### Pass 3 — CLI "truthful UX" spot-check
- [ ] Run at least one happy-path command and capture output
- [ ] Verify labels shown are trace-derived
- [ ] Capture trace JSON and confirm it matches labels
- [ ] Verify CLI surface matches CLI_REFERENCE (AF-0012)
- [ ] Verify global flags behavior per ADR008 (hybrid approach)

Evidence: `cli_outputs.txt`, `happy_trace.json`

---

### Pass 4 — Failure-path run
- [ ] Run a failure-path scenario (invalid workspace / invalid input / etc.)
- [ ] Confirm trace records errors
- [ ] Confirm CLI output aligns with trace
- [ ] Test verifier failure scenarios (AF-0091)

Evidence: `failure_trace.json`

---

### Pass 5 — Plugin architecture verification (AF-0077, AF-0078)
- [ ] Verify skills entry points mechanism works
- [ ] Verify YAML playbook loading + validation works
- [ ] Test `ag skills list` includes entry-point registered skills
- [ ] Test `ag playbooks list` includes YAML-loaded playbooks

Evidence: `cli_outputs.txt`

---

### Pass 6 — Bugs triage
- [ ] Review BUG-0015 (runs list count mismatch) — discovered during testing
- [ ] Confirm new backlog items indexed (AF-0094, AF-0095)
- [ ] Create any additional bug reports in `/docs/dev/bugs/reports/`

Evidence: `bug_triage.md`

---

## Jacob completion
- **Executed by:** Jacob
- **Date:** 2026-03-12
- **Evidence folder:** `artifacts/review_S10_01/`
- **Notes:** Review pending execution

---

## B) Review entry (Jeff + Kai)

### Review metadata
- **Reviewed by:** Jeff + Kai
- **Date:** _pending_
- **Scope:** Sprint10
- **Decision:** _pending_

---

### What changed (high-level)

**Group 1: Artifact Truthfulness & Verification (Gate B track)**
- AF-0090: Artifact metadata now truthful (type matches format, proper storage path)
- AF-0091: Verifier failure-path consistency improved
- AF-0093: Skills test coverage hardened

**Group 2: CLI Completeness**
- AF-0036: Global CLI flags decision made (ADR008 — hybrid approach: `--workspace` global, output flags command-level)
- AF-0012: CLI surface parity with CLI_REFERENCE (stubs + playbooks list)

**Group 3: Documentation Hygiene**
- AF-0081: Inventory sync discipline via registry-based drift detection
- AF-0082: Report polish
- AF-0084: Index link emoji consistency

**Group 4: Plugin Architecture Foundation**
- AF-0077: Skills entry points mechanism
- AF-0078: YAML playbook loading (Option A chosen)

**Dropped**
- AF-0092: Evidence CLI commands (separate evidence concept rejected)

**New items from testing**
- AF-0094: Trace full I/O enrichment (deferred Phase 2 from AF-0090)
- AF-0095: research_v0 skill output audit
- BUG-0015: Runs list count mismatch (SQLite index vs filesystem)

---

### Verification performed (summary)
- Commands executed:
  - `ruff check src tests`
  - `ruff format --check src tests`
  - `pytest -q`
  - `pytest -W error`
  - `ag run --help`
  - `ag skills list`
  - `ag playbooks list`
  - `ag runs list -w skills02 --all`
- Evidence inspected:
  - Manual testing by Kai (AF-0094, AF-0095, BUG-0015 discovery)

---

### Findings
- ✅ What works / improved:
  - All 9 planned AFs completed (plus AF-0036 during planning)
  - ADR008 established clear CLI flags architecture
  - Plugin architecture foundation in place
  - Documentation hygiene enforcement automated
- ⚠️ Issues found (with severity):
  - P2: BUG-0015 — `ag runs list` count mismatch (orphaned SQLite entries)
  - P3: AF-0094 — Trace lacks full step I/O (deferred)
  - P2: AF-0095 — research_v0 skill output needs audit
- 🧩 Follow-ups created:
  - AF-0094 (proposed)
  - AF-0095 (proposed)
  - BUG-0015 (open)

---

### Decision rationale
_To be completed after review execution_

---

### Gate B assessment
| Gate B Condition | Status | Evidence |
|------------------|--------|----------|
| Policy enforcement present | ✅ | AF-0087 (Sprint 09) |
| Verifier/failure rigor | ✅ | AF-0091 |
| Trace-derived labels | _pending_ | Review pass 2.5 |
| Artifact truthfulness | ✅ | AF-0090 |

---

### Next actions
- [ ] Execute review passes (Jacob)
- [ ] Complete Gate B assessment
- [ ] Decision: ACCEPT / ACCEPT WITH FOLLOW-UPS / REJECT
- [ ] Close sprint (if ACCEPT/ACCEPT WITH FOLLOW-UPS)
- [ ] Update INDEX_SPRINTS status to Closed
