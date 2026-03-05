# BACKLOG ITEM — AF0064 — sprint_pr_timing_clarification
# Version number: v0.2

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - 1 PR = 1 primary AF
> - INDEX update rule (status ↔ filename integrity)

> **File naming (required):** `AF0064_Proposed_sprint_pr_timing_clarification.md`
> Status values: `Proposed | Ready | In progress | Blocked | Done | Dropped`

---

## Metadata
- **ID:** AF0064
- **Type:** Process
- **Status:** Proposed
- **Priority:** P1
- **Area:** Process / Docs
- **Owner:** Kai
- **Target sprint:** Sprint06

---

## Problem
There is a misunderstanding in the sprint process documentation about when PRs should be created. The current SPRINT_MANUAL.md mentions "1 PR = 1 primary AF" which can be interpreted as creating PRs continuously during the sprint.

**Intended workflow:**
1. **Sprint start:** Create feature branch from main
2. **During sprint:** Commit work to feature branch (multiple commits per AF is fine)
3. **Sprint end:** Create ONE PR to merge the entire sprint branch to main

This is a single-branch-per-sprint model, not a PR-per-AF model.

---

## Goal
Clarify in SPRINT_MANUAL.md and FOUNDATION_MANUAL.md:
1. Sprint branch lifecycle (create at start, merge at end)
2. PR timing (end of sprint only)
3. Commit convention (atomic commits during sprint, PR at close)

---

## Non-goals
- Changing the commit convention
- Adding CI automation for PRs
- Changing the AF completion section requirements

---

## Acceptance criteria (Definition of Done)
- [ ] SPRINT_MANUAL.md updated with clear branch/PR lifecycle
- [ ] Section 1.1 (Branch Creation) clarifies: one branch per sprint
- [ ] Section 6 (PR Creation Protocol) clarifies: PR at sprint end only
- [ ] "1 PR = 1 primary AF" rule clarified or removed if misleading
- [ ] FOUNDATION_MANUAL.md updated if PR rules are duplicated there
- [ ] INDEX file updated

---

## Implementation notes

### Proposed clarification (SPRINT_MANUAL.md)

#### Section 1.1 — Branch Creation
Add:
```markdown
> **Branch lifecycle:**
> - Create ONE branch per sprint at sprint start
> - Commit all sprint work to this branch
> - Merge to main via PR at sprint close only
```

#### Section 5 — PR plan
Clarify:
```markdown
> **PR timing:** PRs are created at the END of the sprint, not continuously.
> The "1 PR = 1 primary AF" refers to the PR description referencing
> primary work items, not creating separate PRs per AF.
```

#### Section 6 — PR Creation Protocol
Add explicit timing:
```markdown
### 6.0 When to Create a PR
PRs are created ONLY at sprint close, not during the sprint.
- During sprint: commit work directly to feature branch
- At sprint close: create PR to merge feature branch → main
```

### Files to update
- `/docs/dev/foundation/SPRINT_MANUAL.md`
- `/docs/dev/foundation/FOUNDATION_MANUAL.md` (if applicable)

---

## Risks
- Low: Documentation-only change
- May require team alignment if current interpretation differs

---

## Related items
- SPRINT_MANUAL.md Section 1, 5, 6
- FOUNDATION_MANUAL.md PR rules (if any)
