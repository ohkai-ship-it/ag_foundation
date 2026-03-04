# Pull Request Template (ag_foundation)
# Version number: v0.2

> **FOUNDATION GOVERNANCE**
> This PR is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md` — Section 4: Branching & PR Discipline
> `/docs/dev/foundation/SPRINT_MANUAL.md` — Section 6: PR Creation Protocol
>
> Critical invariants:
> - 1 PR = 1 primary AF (exactly)
> - CI discipline (ruff + pytest -W error + coverage)
> - Evidence required for behavior changes (RunTrace ID)
> - INDEX update required if statuses change

## Primary work item
- **Backlog (primary):** AF####
- **Related (secondary):** AF#### (optional)
- **Bugs:** BUG#### (optional)
- **ADRs:** ADR### (optional)

## Summary
What changed and why (2–5 bullets).

## Scope / Non-goals
- In scope:
- Out of scope:

## Files changed (required)
List important files/folders touched (especially under `/docs/dev`).

- `...`
- `...`

## Architecture & contracts
- Layers touched (adapter/core/skill/storage/docs):
- Interfaces touched (TaskSpec/RunTrace/Planner/Orchestrator/Executor/Verifier/Recorder/...):
- Contract changes? (yes/no). If yes: updated where (ARCHITECTURE / CLI_REFERENCE / etc.)

## Evidence (required)
### Lint / format
- `ruff check src tests`:
- `ruff format --check src tests`:

### Tests
- Command(s):
  - `pytest -W error`
  - `pytest --cov=src/ag --cov-report=term-missing`
- Result summary:

### Run evidence (required for behavior changes)
- RunTrace ID(s): `run_...`
- Repro command(s):
  - `ag run ...`
- What reviewers should look for in the trace:

### Artifacts (if applicable)
- `artifact://...`

## Docs updates (required when process/contracts touched)
- Updated `/docs/dev/...` files:
  - `...`
- Notes:

## Risk level
- P0 | P1 | P2
- Notes:

## Checklist (must be true to request review)
- [ ] This PR references exactly one primary AF item
- [ ] PR is reviewable in ~15–30 minutes (or split plan exists)
- [ ] Truthful UX preserved (labels trace-derived)
- [ ] Tests run and results included
- [ ] AF completion section filled (for merged PRs)
- [ ] INDEX files updated (if statuses or entries changed):
  - [ ] `/docs/dev/backlog/INDEX_BACKLOG.md`
  - [ ] `/docs/dev/bugs/INDEX_BUGS.md`
  - [ ] `/docs/dev/decisions/INDEX_DECISIONS.md`
  - [ ] `/docs/dev/sprints/INDEX_SPRINTS.md`

## Completion reference
- Backlog file: `/docs/dev/backlog/items/AF####_<Status>_<desc>.md`
- Completion section: included at bottom of the backlog file (required for merge)
