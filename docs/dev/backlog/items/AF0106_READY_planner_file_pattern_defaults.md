# BACKLOG ITEM — AF0106 — planner_file_pattern_defaults
# Version number: v0.1

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

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF-0106
- **Title:** V1Planner file pattern defaults
- **Status:** READY
- **Priority:** P2
- **Owner:** TBD
- **Sprint:** TBD
- **Created:** 2026-03-21
- **Tags:** planner, skills, usability

---

## Problem Statement

The V1Planner generates plans with hardcoded file patterns (e.g., `['*.docx', '*.pdf']`) 
that don't match actual workspace contents. When users have MD files in their 
workspace, the `load_documents` skill fails with:

```
Error: Required step 'load_documents_0' failed: No files found matching patterns: ['*.docx', '*.pdf']
```

The `load_documents` skill itself supports MD files (it's the default pattern), 
but the V1Planner's prompt or default parameters assume different file types.

---

## Proposed Solution

### Option B: Workspace-aware pattern detection
Before generating a plan, scan the workspace inputs folder and detect 
available file extensions, then include only relevant patterns in the plan.

**Recommended:** Option B (workspace-aware) provides the best UX by 
generating plans that match actual workspace contents.

Yes, option B
---

## Acceptance Criteria

1. [ ] `ag plan generate` with summarize task uses patterns matching workspace files
2. [ ] MD files in workspace are correctly included in generated plans
3. [ ] Plan execution succeeds when workspace contains only MD files
4. [ ] Test coverage for pattern detection logic
5. [ ] No regression for PDF/DOCX workspaces

---

## Technical Notes

**Affected files:**
- `src/ag/core/planner.py` — V1Planner prompt or skill param generation
- `tests/test_planner.py` — Test for file pattern handling

**Root cause location:**
The V1Planner's system prompt or skill parameter generation likely 
hardcodes document patterns instead of detecting workspace contents.

---

## Dependencies

- None (standalone fix)

---

## Completion Section (filled when done)

### Implementation Summary
_To be filled_

### Files Changed
_To be filled_

### Evidence
_To be filled_

### Acceptance Criteria Verification
_To be filled_
