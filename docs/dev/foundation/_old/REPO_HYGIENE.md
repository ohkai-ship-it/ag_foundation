# DEPRECATED — see FOUNDATION_MANUAL.md

> **This document is deprecated.**
> All rules have been consolidated into:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> This file is retained for historical reference only.
> Do not update this file. Update the operating manual instead.

---

# Repo Hygiene (ag_foundation)
# Version number: v0.2 (DEPRECATED)
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
- [ ] Canonical process docs live in `/docs/dev/foundation/`
- [ ] Canonical templates live in:
  - `/docs/dev/backlog/templates/`
  - `/docs/dev/bugs/templates/`
  - `/docs/dev/decisions/templates/`
  - `/docs/dev/sprints/templates/`
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
