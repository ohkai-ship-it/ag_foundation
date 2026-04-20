# BACKLOG ITEM — AF0061 — status_caps_convention
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

> **File naming (required):** `AF####_<Status>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0061
- **Type:** Docs
- **Status:** DONE
- **Priority:** P2
- **Area:** Docs/Process
- **Owner:** Kai
- **Target sprint:** Sprint06
- **Related:** AF0064 (overlapping scope)

---

## Problem
Two inconsistencies in documentation conventions:

### 1. ADR files missing status in filename
Decision files (ADRs) don't follow the same filename convention as other docs:

| Folder | Current naming | Should be |
|--------|---------------|-----------|
| `/backlog/items/` | `AF####_<Status>_<desc>.md` | ✓ consistent |
| `/bugs/reports/` | `BUG####_<Status>_<desc>.md` | ✓ consistent |
| `/decisions/files/` | `ADR###_<desc>.md` | ✗ **missing status** |

### 2. Status values inconsistently capitalized
Current status values use title case (`Ready`, `Proposed`, `Done`) but should be **ALL CAPS** for visibility:

| Current | Target |
|---------|--------|
| `Proposed` | `PROPOSED` |
| `Ready` | `READY` |
| `In progress` | `IN_PROGRESS` |
| `Done` | `DONE` |
| `Accepted` | `ACCEPTED` |
| `Open` | `OPEN` |
| `Fixed` | `FIXED` |

This affects:
- Filenames (e.g., `AF0061_PROPOSED_decision_filename.md`)
- Metadata status fields inside files
- INDEX files status columns
- Foundation documentation (FOUNDATION_MANUAL.md, templates)

---

## Goal
Update conventions for consistency:

1. **ADR filenames include status**
   - Current: `ADR006_workspace_folder_structure.md`
   - Target: `ADR006_PROPOSED_workspace_folder_structure.md`

2. **All statuses use CAPS**
   - Filenames, metadata, and indexes all use uppercase

Deliverables:
- [ ] Update all templates with CAPS status convention
- [ ] Update FOUNDATION_MANUAL.md status value lists
- [ ] Rename ADR files to include status
- [ ] Update all INDEX files with CAPS statuses
- [ ] Rename AF/BUG files to use CAPS status
- [ ] Update metadata inside files to use CAPS

---

## Non-goals
- Changing status value meanings
- Adding new status values

---

## Acceptance criteria (Definition of Done)
- [x] All status values use CAPS in filenames (e.g., `_PROPOSED_`, `_READY_`, `_DONE_`)
- [x] All status values use CAPS in metadata fields inside files
- [x] All INDEX files use CAPS in status columns
- [x] ADR files include status in filename
- [x] Templates updated with CAPS convention
- [x] FOUNDATION_MANUAL.md updated with CAPS status values
- [x] Cross-references updated (grep for old filenames/statuses)

---

## Implementation notes

### Status value mapping
```
Proposed    → PROPOSED
Ready       → READY
In progress → IN_PROGRESS
Blocked     → BLOCKED
Done        → DONE
Dropped     → DROPPED
Open        → OPEN
Fixed       → FIXED
Verified    → VERIFIED
Accepted    → ACCEPTED
Superseded  → SUPERSEDED
Deprecated  → DEPRECATED
```

### ADR files to rename (with CAPS)
```
ADR001_architecture_baseline.md       → ADR001_ACCEPTED_architecture_baseline.md
ADR002_trace_versioning_strategy.md   → ADR002_ACCEPTED_trace_versioning_strategy.md
ADR003_manual_mode_gating.md          → ADR003_ACCEPTED_manual_mode_gating.md
ADR004_storage_baseline.md            → ADR004_ACCEPTED_storage_baseline.md
ADR005_orchestrator_threshold.md      → ADR005_ACCEPTED_orchestrator_threshold.md
ADR006_workspace_folder_structure.md  → ADR006_PROPOSED_workspace_folder_structure.md
ADR007_configuration_state_separation.md → ADR007_PROPOSED_configuration_state_separation.md
```

### Files to update
1. **Templates:**
   - `docs/dev/backlog/templates/BACKLOG_ITEM_TEMPLATE.md`
   - `docs/dev/bugs/templates/BUG_REPORT_TEMPLATE.md`
   - `docs/dev/decisions/templates/ADR_TEMPLATE.md`

2. **Foundation docs:**
   - `docs/dev/foundation/FOUNDATION_MANUAL.md`

3. **Index files:**
   - `docs/dev/backlog/INDEX_BACKLOG.md`
   - `docs/dev/bugs/INDEX_BUGS.md`
   - `docs/dev/decisions/INDEX_DECISIONS.md`

4. **All existing AF/BUG/ADR files** (rename + update metadata)

### Index update pattern
```markdown
| ADR-0006 | PROPOSED | ... | `ADR006_PROPOSED_workspace_folder_structure.md` |
```

---

## Risks
- Low risk — documentation-only change
- Need to update any links referencing old filenames

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF0061
- **PR:** N/A (direct commit to sprint branch)
- **Author:** Jacob
- **Date:** 2026-03-06
- **Branch:** sprint06/skill-foundation
- **Risk level:** P2
- **Runtime mode used for verification:** N/A (docs only)

---

## 2) Acceptance criteria verification
All criteria verified ✓ — see checklist above

---

## 3) What changed (file-level)

**Templates updated:**
- `docs/dev/backlog/templates/BACKLOG_ITEM_TEMPLATE.md`
- `docs/dev/bugs/templates/BUG_REPORT_TEMPLATE.md`
- `docs/dev/decisions/templates/ADR_TEMPLATE.md`

**Foundation docs updated:**
- `docs/dev/foundation/FOUNDATION_MANUAL.md`
- `docs/dev/foundation/SPRINT_MANUAL.md`

**Index files updated:**
- `docs/dev/backlog/INDEX_BACKLOG.md`
- `docs/dev/bugs/INDEX_BUGS.md`
- `docs/dev/decisions/INDEX_DECISIONS.md`

**Files renamed (67 AF, 11 BUG, 7 ADR):**
- All AF files: `_Done_` → `_DONE_`, `_Ready_` → `_READY_`, `_Proposed_` → `_PROPOSED_`
- All BUG files: `_Fixed_` → `_FIXED_`, `_Open_` → `_OPEN_`
- All ADR files: Added status to filename (e.g., `ADR001_ACCEPTED_...`)

**Metadata updated in all files:**
- Status field changed to CAPS in all AF/BUG/ADR files

---

## 4) Architecture alignment (mandatory)
- **Layering:** Docs/Process change only — no code impact

