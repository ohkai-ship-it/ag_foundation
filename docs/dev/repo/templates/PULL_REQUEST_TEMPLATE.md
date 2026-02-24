# Pull request template (ag_foundation)
# Version number: v0.1

## Primary work item
- **Backlog (primary):** AF-000x
- **Related (secondary):** AF-000y (optional)
- **Bugs:** BUG-000x (optional)

## Summary
What changed and why (2–5 bullets).

## Scope / Non-goals
- In scope:
- Out of scope:

## Architecture & contracts
- Layers touched (adapter/core/skill/storage):
- Interfaces touched (TaskSpec/RunTrace/Planner/Orchestrator/...):
- Contract changes? (yes/no). If yes: docs updated where?

## Evidence (required)
### Tests
- Command(s):
  - `pytest ...`
- Result summary:

### Run evidence (required for behavior changes)
- RunTrace ID(s): `run_...`
- Repro command(s):
  - `ag run ...`
- What reviewers should look for in the trace:

### Artifacts (if applicable)
- `artifact://...`

## Risk level
- P0 | P1 | P2
- Notes:

## Checklist (must be true to request review)
- [ ] This PR references exactly one primary AF item
- [ ] PR is reviewable in ~15–30 minutes (or split plan exists)
- [ ] Truthful UX preserved (labels trace-derived)
- [ ] Tests run and results included
- [ ] Completion note created (MD) and linked here:
  - Link/path: `/docs/dev/backlog/items/AF-000x/` or wherever stored

## Completion note
Paste the link to the completion note MD file:
- `<link or path>`
