# PR Checklist (ag_foundation)
# Version number: v0.1

This checklist must be completed before requesting review.

## Metadata
- [ ] PR references **exactly one primary** backlog item: AF-000x
- [ ] PR title is a good changelog line
- [ ] PR description includes scope and non-goals

## Architecture & layering
- [ ] No business logic added to adapters (CLI/API/Event)
- [ ] Core logic lives in core modules or skills behind interfaces
- [ ] Workspace isolation respected (no cross-workspace reads/writes)

## Truthful UX
- [ ] Any user-visible label is derived from `RunTrace`
- [ ] No hardcoded “verified/computed/retrieval used” claims

## Tests & evidence
- [ ] Appropriate tests added/updated (see TESTING_GUIDELINES)
- [ ] Tests executed locally and results included in PR description
- [ ] For behavior changes: at least one RunTrace ID captured and included

## Docs
- [ ] If contracts changed, relevant cornerstone docs updated
- [ ] CLI changes reflected in CLI_REFERENCE

## Safety & modes
- [ ] If safety hooks touched: permission/confirmation behavior documented and tested
- [ ] If manual mode touched: dev gate enforced; banner printed; not exposed to end users

## Completion note
- [ ] Completion note created as an MD file using `/docs/dev/backlog/templates/COMPLETION_NOTE_TEMPLATE.md` and linked in PR
