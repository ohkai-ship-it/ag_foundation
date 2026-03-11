# BACKLOG ITEM — AF0064 — process_documentation_hardening
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

> **File naming (required):** `AF0064_Proposed_process_documentation_hardening.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0064
- **Type:** Process
- **Status:** DONE
- **Priority:** P1
- **Area:** Process / Docs
- **Owner:** Kai
- **Target sprint:** Sprint09

---

## Problem
Two process documentation issues need addressing:

### 1. Sprint PR timing misunderstanding
The current SPRINT_MANUAL.md mentions "1 PR = 1 primary AF" which can be interpreted as creating PRs continuously during the sprint.

**Intended workflow:**
1. **Sprint start:** Create feature branch from main
2. **During sprint:** Commit work to feature branch (multiple commits per AF is fine)
3. **Sprint end:** Create ONE PR to merge the entire sprint branch to main

### 2. Status convention inconsistencies (from AF0061)
- ADR files missing status in filename (unlike AF/BUG files)
- Status values use title case (`Ready`) instead of ALL CAPS (`READY`)

Affects: filenames, metadata, INDEX files, templates

---

## Goal
Consolidated process documentation fixes:

1. **Sprint branch/PR lifecycle clarity** — SPRINT_MANUAL.md and FOUNDATION_MANUAL.md
2. **Status CAPS convention** — Filenames, metadata, INDEX files (from AF0061)
3. **ADR filename convention** — Include status in ADR filenames (from AF0061)

---

## Non-goals
- Changing the commit convention
- Adding CI automation for PRs
- Changing the AF completion section requirements
- Changing status value meanings or adding new values

---

## Acceptance criteria (Definition of Done)

### Sprint PR timing
- [x] SPRINT_MANUAL.md updated with clear branch/PR lifecycle
- [x] Section 1.1 (Branch Creation) clarifies: one branch per sprint
- [x] Section 6 (PR Creation Protocol) clarifies: PR at sprint end only
- [x] "1 PR = 1 primary AF" rule clarified or removed if misleading
- [x] FOUNDATION_MANUAL.md updated if PR rules are duplicated there

### Status convention (from AF0061)
- [x] All status values use CAPS in filenames (`_PROPOSED_`, `_READY_`, `_DONE_`)
- [x] All status values use CAPS in metadata fields inside files
- [x] All INDEX files use CAPS in status columns
- [x] ADR files include status in filename
- [x] Templates updated with CAPS convention

- [x] INDEX file updated

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
- **AF0061 (Dropped)** — Status CAPS convention (absorbed into this AF)

---

## Completion

### Summary
Updated process documentation to clarify sprint branch/PR lifecycle and verified status CAPS convention.

### Changes made
1. **SPRINT_MANUAL.md Section 1** — Added branch lifecycle callout explaining one branch per sprint, commit to branch during sprint, PR at close only
2. **SPRINT_MANUAL.md Section 6** — Added Section 6.0 "When to Create a PR" with explicit timing guidance
3. **FOUNDATION_MANUAL.md Section 1.5** — Clarified "1 PR = 1 primary AF" rule (for traceability, not separate PRs per AF)
4. **INDEX_BACKLOG.md** — Fixed naming convention from `<Status>` to `<STATUS>` for consistency
5. **Verified** templates already use CAPS convention (BACKLOG_ITEM_TEMPLATE, BUG_REPORT_TEMPLATE, ADR_TEMPLATE)
6. **Verified** ADR files already include status in filename (ADR001_ACCEPTED_*, etc.)
7. **Cleaned up** 3 duplicate stale READY files

### Files changed
- `docs/dev/foundation/SPRINT_MANUAL.md`
- `docs/dev/foundation/FOUNDATION_MANUAL.md`
- `docs/dev/backlog/INDEX_BACKLOG.md`

### Evidence (Documentation-only change)
No runtime evidence required; changes are documentation clarifications.

