# REVIEW_TASKS_SPRINT01
# Version number: v0.2

## Metadata
- **Review ID:** REVIEW_S01_2026-02-24
- **Scope:** Sprint 01 strict audit (AF-0004..AF-0010 + BUG-0001..BUG-0003)
- **Reviewer:** Jacob
- **Date:** 2026-02-24
- **Repo commit / tag:** (fill in)
- **Environment:** (fill in: OS, Python, venv)

## Inputs (files)
### Sprint report
- `SPRINT_REPORT_SPRINT01.md`

### Completion notes / handoffs
- `2026-02-24_AF-0004_sprint-os-hygiene.md`
- `2026-02-24_AF-0010_python-bootstrap.md`
- `2026-02-24_AF-0005_contracts.md`
- `2026-02-24_AF-0006_storage-baseline.md`
- `2026-02-24_AF-0007_runtime-skeleton.md`
- `2026-02-24_AF-0008_cli-v0-truthful.md`
- `2026-02-24_AF-0009_artifacts-v0.md`

### Bug reports
- `BUG-0001-global-options-not-global.md`
- `BUG-0002-missing-run-options.md`
- `BUG-0003-missing-cli-subcommands.md`

## Outputs (paths)
- Review entry: `/docs/dev/reviews/entries/REVIEW_S01_2026-02-24.md`
- Evidence bundle folder: `/docs/dev/reviews/entries/REVIEW_S01_2026-02-24/`

> Create this folder first and place all outputs below inside it.

---

# Pass 0 — Setup & invariants
## Tasks
- [ ] Create fresh venv and install editable (Linux/macOS example):
  - `python -m venv .venv && source .venv/bin/activate`
  - `pip install -U pip`
  - `pip install -e .[dev]` (or equivalent)
- [ ] Record:
  - `python --version`
  - `pip freeze | head -n 50`
- [ ] Verify entrypoint:
  - `ag --help`
- [ ] Gate expectation:
  - Without `AG_DEV=1`, `ag run --mode manual "gate test"` should fail.

## Evidence
- [ ] Save transcript: `/docs/dev/reviews/entries/REVIEW_S01_2026-02-24/env.txt`
- [ ] Link:

---

# Pass 1 — Scope verification
## Tasks
- [ ] Confirm all completion notes listed above exist and are discoverable.
- [ ] Confirm sprint report is present and references the AF items above.
- [ ] Confirm bug reports exist and are discoverable/linked.

## Evidence
- [ ] `/docs/dev/reviews/entries/REVIEW_S01_2026-02-24/scope_links.md` containing links to AF + BUG docs (+ optional PR/commit refs)
- [ ] Link:

---

# Pass 2 — Test suite verification
## Tasks
Run and record outputs:
- [ ] `pytest -q`
- [ ] `pytest -q -rs`
- [ ] Contracts: `pytest -q tests/test_contracts.py`
- [ ] Storage: `pytest -q tests/test_storage.py`
- [ ] Runtime: `pytest -q tests/test_runtime.py`
- [ ] CLI truthful: `pytest -q tests/test_cli_truthful.py`
- [ ] Artifacts: `pytest -q tests/test_artifacts.py`

## Evidence
- [ ] `/docs/dev/reviews/entries/REVIEW_S01_2026-02-24/pytest_summary.txt`
- [ ] Link:

---

# Pass 3 — Contracts audit
## Tasks
- [ ] Confirm TaskSpec required fields exist (version, prompt, workspace_id, mode, playbook preference, budgets, constraints).
- [ ] Confirm RunTrace required fields exist (version, run_id, timestamps, workspace_id, mode, steps, artifacts, verifier, final).
- [ ] Confirm Playbook schema exists and is linear.
- [ ] Confirm contract tests include JSON round-trip + additive evolution guardrails.

## Evidence
- [ ] `/docs/dev/reviews/entries/REVIEW_S01_2026-02-24/contracts_notes.md`
- [ ] Link:

---

# Pass 4 — Storage & workspace isolation audit
## Tasks (black-box)
Run and record outputs (adjust flags if CLI differs):
- [ ] With `AG_DEV=1`, create/runs:
  - `ag run --workspace ws_a --mode manual "hello ws_a"`
  - `ag run --workspace ws_b --mode manual "hello ws_b"`
- [ ] Record `run_id_a` and `run_id_b`.
- [ ] Verify isolation:
  - `ag runs list --workspace ws_a` shows `run_id_a` not `run_id_b`
  - `ag runs list --workspace ws_b` shows `run_id_b` not `run_id_a`
- [ ] Verify show isolation expectation:
  - `ag runs show <run_id_a> --workspace ws_b` should not succeed (not found / error)

## Evidence
- [ ] `/docs/dev/reviews/entries/REVIEW_S01_2026-02-24/storage_isolation_transcript.txt`
- [ ] Link:

---

# Pass 5 — Runtime pipeline audit
## Tasks
- [ ] Happy-path run (manual mode, gated): record run_id + copy persisted trace JSON into evidence bundle.
- [ ] Failure-path run (e.g., missing skill) if supported: record run_id + copy trace JSON.

## Evidence
- [ ] `/docs/dev/reviews/entries/REVIEW_S01_2026-02-24/happy_trace.json`
- [ ] `/docs/dev/reviews/entries/REVIEW_S01_2026-02-24/failure_trace.json` (or note why not applicable)
- [ ] Link:

---

# Pass 6 — CLI truthful UX audit
## Tasks
- [ ] Gate test:
  - Without `AG_DEV=1`: `ag run --mode manual "gate test"` must fail clearly.
  - With `AG_DEV=1`: command succeeds and RunTrace.mode == "manual".
- [ ] Truthful label check:
  - Run: `ag run --workspace ws_truth --mode manual "truthful test"`
  - Show: `ag runs show <run_id> --json`
  - Verify human output labels match JSON fields (mode, verifier.status, duration, playbook name/version).

## Evidence
- [ ] `/docs/dev/reviews/entries/REVIEW_S01_2026-02-24/cli_outputs.txt`
- [ ] (Optional) `/docs/dev/reviews/entries/REVIEW_S01_2026-02-24/label_check.md`
- [ ] Link:

---

# Pass 7 — Artifacts audit
## Tasks
- [ ] If artifact creation shipped: run artifact-producing task and list artifacts.
- [ ] `ag artifacts list --run <run_id> --workspace <ws>` (human + JSON if supported)
- [ ] Verify empty list behavior for runs without artifacts.

## Evidence
- [ ] `/docs/dev/reviews/entries/REVIEW_S01_2026-02-24/artifacts_outputs.txt`
- [ ] Link:

---

# Pass 8 — Bug triage (BUG-0001..BUG-0003)
## Tasks
For each bug:
- [ ] Reproduce (if feasible) and record expected vs actual.
- [ ] Set severity and classification (Defect vs Deferred scope).
- [ ] Propose follow-up AF/BUG IDs.

## Evidence
- [ ] `/docs/dev/reviews/entries/REVIEW_S01_2026-02-24/bug_triage.md` (include spec compliance table)
- [ ] Link:

---

## Finalization — Fill the review entry (REVIEW_TEMPLATE)
## Tasks
- [ ] Create `/docs/dev/reviews/entries/REVIEW_S01_2026-02-24.md` using REVIEW_TEMPLATE.
- [ ] Decision: **ACCEPT / ACCEPT WITH FOLLOW-UPS / REJECT**
- [ ] List blocking issues (if any) and follow-up IDs.

## Deliverables checklist
- [ ] Review entry created and linked to evidence bundle
- [ ] Evidence bundle folder complete
- [ ] All links verified
