# SPRINT REVIEW — S04_REVIEW_01 — Process Hardening
# Version number: v0.2

> **Status:** Pending (created by PM for Jacob to execute)

---

## A) Review execution tasks (Jacob)

### Metadata
- **Review ID:** S04_REVIEW_01
- **Scope:** Sprint04
- **Executor:** Jacob
- **Date:** TBD
- **Commit / tag:** TBD
- **Environment:** TBD

### Inputs (links)
- Sprint description: `S04_DESCRIPTION.md`
- AF items in scope:
  - `/docs/new_dev/backlog/items/AF0041_Done_backlog_migration.md`
  - `/docs/new_dev/backlog/items/AF0042_Done_bugs_decisions.md`
  - `/docs/new_dev/backlog/items/AF0043_Done_sprint_system.md`
  - `/docs/new_dev/backlog/items/AF0045_Done_ci_enforcement.md`
- Bug reports: None (docs-only sprint)

### Outputs (paths)
Evidence folder: `/docs/new_dev/sprints/documentation/Sprint04_process_hardening/artifacts/review_S04_01/`

---

### Pass 0 — Setup & invariants
- [ ] Fresh venv; install project
- [ ] Record `python --version`
- [ ] Record `pip freeze | head -n 50`
- [ ] Confirm `ag --help` works
- [ ] Confirm manual gate (AG_DEV=1) behavior

---

### Pass 1 — Scope verification (what shipped)
- [ ] Confirm each AF file exists in `/docs/new_dev/backlog/items/`
- [ ] Confirm filename Status matches internal Status field
- [ ] Confirm indices include all new/changed items

---

### Pass 2 — Lint/format + test suite verification
- [ ] `ruff check src tests`
- [ ] `ruff format --check src tests`
- [ ] `pytest -q`
- [ ] `pytest -W error`

---

### Pass 3 — Documentation structure verification
- [ ] All INDEX files exist and link correctly
- [ ] All renamed files accessible via new paths
- [ ] Legacy deprecation notices in place

---

## B) Review entry (Jeff + Kai)

### Decision
**Status:** PENDING

### Notes
(To be filled by Jeff + Kai after Jacob executes review tasks)
