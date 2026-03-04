# Repo Hygiene (ag_foundation)
# Version number: v0.2
# Effective date: 2026-03-03

This checklist keeps the repository consistent, reviewable, and low-drag.

## Daily / per-PR
- [ ] Branch name follows convention: `feat/`, `fix/`, `chore/`
- [ ] PR references AF/BUG/ADR ids as applicable
- [ ] Ruff passes:
  - [ ] `ruff check src tests`
  - [ ] `ruff format --check src tests` (or applied)
- [ ] Tests run locally:
  - [ ] `pytest -W error`
  - [ ] coverage thresholds maintained
- [ ] RunTrace captured for behavior changes (especially CLI labels / planner/orchestrator changes)
- [ ] No large unrelated diffs (split PR if needed)

## Docs hygiene
- [ ] Canonical process docs live in `/docs/new_dev/foundation/`
- [ ] Canonical templates live in:
  - `/docs/new_dev/backlog/templates/`
  - `/docs/new_dev/bugs/templates/`
  - `/docs/new_dev/decisions/templates/`
  - `/docs/new_dev/sprints/templates/`
- [ ] If contracts changed, update root cornerstone docs (ARCHITECTURE / CLI_REFERENCE etc.)
- [ ] Update INDEX files when statuses change (and at sprint start ritual)

## Code hygiene
- [ ] No business logic in adapters
- [ ] Workspace boundaries respected (paths, storage, artifacts)
- [ ] Trace logging included for new behaviors
- [ ] Errors are captured into traces (no silent failure)

## Naming conventions
- [ ] Backlog: `AF####_<Status>_<desc>.md`
- [ ] Bugs: `BUG####_<Status>_<desc>.md`
- [ ] ADRs: `ADR###_<desc>.md`
- [ ] Sprints: `Sprint##_.../S##_DESCRIPTION.md` etc.
