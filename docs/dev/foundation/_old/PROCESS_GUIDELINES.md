# DEPRECATED — see FOUNDATION_OPERATING_MANUAL.md

> **This document is deprecated.**
> All rules have been consolidated into:
> `/docs/dev/foundation/FOUNDATION_OPERATING_MANUAL.md`
>
> This file is retained for historical reference only.
> Do not update this file. Update the operating manual instead.

---

# Process Guidelines (ag_foundation)
# Version number: v0.2 (DEPRECATED)
# Effective date: 2026-03-03

> **See also:**
> - `/docs/dev/foundation/FOUNDATION_OPERATING_MANUAL.md` — unified operating rules
> - `/docs/dev/foundation/SPRINT_EXECUTION_PLAYBOOK.md` — step-by-step sprint execution

This document consolidates the workflow/process rules previously spread across multiple files.
It is canonical for `/docs/dev`.

## Artifacts and where they live
- Backlog index: `/docs/dev/backlog/INDEX_BACKLOG.md`
- Bugs index: `/docs/dev/bugs/INDEX_BUGS.md`
- Decisions index: `/docs/dev/decisions/INDEX_DECISIONS.md`
- Sprints index: `/docs/dev/sprints/INDEX_SPRINTS.md`

## Naming conventions (strict)
### Backlog items
- File name: `AF####_<Status>_<three_word_description>.md`
- Status: `Proposed | Ready | In progress | Blocked | Done | Dropped`
- Location: `/docs/dev/backlog/items/`

### Bug reports
- File name: `BUG####_<Status>_<three_word_description>.md`
- Status: `Open | In progress | Fixed | Verified | Dropped`
- Location: `/docs/dev/bugs/reports/`

### ADRs
- File name: `ADR###_<three_word_description>.md`
- Status inside file: `Proposed | Accepted | Superseded | Deprecated`
- Location: `/docs/dev/decisions/files/`

### Sprints
- Folder: `/docs/dev/sprints/documentation/Sprint##_three_word_description/`
- Files:
  - `S##_DESCRIPTION.md` (plan + report)
  - `S##_REVIEW_01.md`
  - `S##_PR_01.md`

## Sprint lifecycle (state machine)
Draft → Ready → In Progress → In Review → Accepted → Closed

## Sprint start (ritual)
Jeff + Kai:
- Create AFs (Status = Ready)
- Create sprint description file
- Define sprint ID + name

Jacob:
- Clarify questions (chat only)
- Confirm scope understood (chat only)
- Create branch
- Create sprint folder
- Update INDEX files (ritual at sprint start)
- Confirm with Kai before starting implementation

### INDEX update rule (strict)
1) Update INDEX whenever AF/BUG/ADR/SPRINT status changes  
2) Also update INDEX as a ritual at sprint start

## During sprint
- One PR = one primary AF item.
- Commit/PR boundaries must match AF slicing.
- If new bugs are found: create bug report immediately (don’t bury in PR comments).

## Sprint end
Jeff + Kai:
- Review `S##_DESCRIPTION.md`
- Create `S##_REVIEW_01.md`

Jacob:
- Execute review tasks
- Save evidence under sprint folder `artifacts/`

Jeff + Kai:
- Decide: ACCEPT / ACCEPT WITH FOLLOW-UPS / REJECT
- Create follow-up AF/BUG/ADR items if needed

## Finalize sprint
Jacob:
- Run repo hygiene
- Ensure CI/local checks pass
- Update indices
- Create final PR (if needed) and merge
- Mark sprint as Closed
