# PULL REQUEST TEMPLATE
#### Description: Template for sprint pull requests. The PR document summarizes all work completed in a sprint, lists AF completion status, and test results. Created (empty) during Phase 1 (Planning), filled during Phase 4 (Review), and finalized before the Phase 5 merge gate (G5). The agent may extend this template non-destructively to match sprint-specific requirements. Copy into the sprint folder, rename per naming conventions (SP Appendix C.3), and fill all required sections.
#### Convergent: v1.3.2
#### governs: <project_name>

> **FOUNDATION GOVERNANCE**
> This file is governed by: `foundation/SPRINT_PLAYBOOK.md`

## 1) Metadata
- **Sprint:** Sprint##
- **Branch:**

- **Status:** PROPOSED | READY | BLOCKED | DONE | DEPRECATED
- **PRIORITY:** P0 | P1 | P2
- **Area:** CLI | Core Runtime | Orchestrator | Skills | Storage | Docs | Process | CI

- **PROPOSED:** DD-MM-YYYY, hh:mm
- **Started implementation:** DD-MM-YYYY, hh:mm
- **DONE:** DD-MM-YYYY, hh:mm

- **Related backlog item(s):** AF#### (optional)
- **Related bug(s):** BUG#### (optional)
- **Related PR(s):** #<number> (optional)


- **Models:**
- **Description:** (1-3 sentences)

---

## Work Items

| ID | Title | Status | Notes |
|---:|---|:--:|---|
| AF-#### | <title> | PROPOSED / READY / DONE / BLOCKED / DEPRECATED | |
| AF-#### | <title> | PROPOSED / READY / DONE / BLOCKED / DEPRECATED | |

---

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
- Layers touched:
- Interfaces touched:
- Contract changes? (yes/no). If yes: updated where (ARCHITECTURE / CLI_REFERENCE / etc.)

## Evidence (required)
> Evidence format: GS §PO02. Per-type requirements: PROJECT_CONTROL GS:PO09.

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
- [ ] This PR lists all AF items completed in the sprint
- [ ] PR is reviewable in ~15–30 minutes (or split plan exists)
- [ ] Tests results included
- [ ] AF completion section filled (for merged PRs)
- [ ] INDEX files updated (if statuses or entries changed):
  - [ ] `docs/INDEX_BACKLOG.md`
  - [ ] `docs/INDEX_BUGS.md`
  - [ ] `docs/INDEX_DECISIONS.md`
  - [ ] `docs/INDEX_SPRINTS.md`

## Completion reference
- Backlog file: `docs/files/backlog/AF####_<three_word_description>.md`
- Completion section: included at bottom of the backlog file (required for merge)

---

## References

- Sprint execution: `foundation/SPRINT_PLAYBOOK.md`
