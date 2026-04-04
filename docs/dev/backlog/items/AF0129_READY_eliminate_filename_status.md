# AF-0129 — Eliminate Filename-Status Coupling
# Version number: v0.2
# Created: 2026-04-04
# Started:
# Completed:
# Status: READY
# Priority: P0
# Area: Process / Docs
# Models:

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> **CI workflow (CRITICAL):**
> - **During AF development:** run targeted tests only
>   `pytest tests/test_documentation_drift.py -W error`
> - **Before commit (full gate):** run the complete CI gate
>   1. `ruff check src tests`
>   2. `ruff format --check src tests`
>   3. `pytest -W error`
>   4. `pytest --cov=src/ag --cov-report=term-missing`

---

## Metadata
- **ID:** AF-0129
- **Type:** Process
- **Status:** READY
- **Priority:** P0
- **Area:** Process / Docs
- **Owner:** Jacob
- **Target sprint:** Sprint 16 — governance_simplification
- **Phase:** 1 (no dependencies)

---

## Problem

Every status change requires **3 synchronized edits**: (1) rename file to change status token, (2) update internal `Status:` metadata field, (3) update INDEX row. This is the #1 source of ceremony overhead and the primary driver of INDEX drift bugs (BUG-0022, BUG-0023). SPRINT_MANUAL §2.2, §2.3, §7.1, §8.4 all exist solely to manage this coupling. ADR files have never carried status tokens — aligning AF and BUG files to that pattern eliminates an entire class of process failure.

---

## Goal

- **New files** use immutable filenames without status tokens: `AF0129_eliminate_filename_status.md`
- **Existing files** keep their current names — no retroactive renames
- Status lives in exactly **2 places**: internal file metadata + INDEX row
- Status changes require exactly **2 edits** (file metadata + INDEX), zero renames

---

## Non-goals

- Renaming any existing AF or BUG files
- Changing ADR file naming (already correct)
- Any changes to `src/` or `tests/` code

---

## Acceptance Criteria
- [ ] New AF/BUG files created after this AF do NOT contain status tokens in filename
- [ ] Existing files remain untouched (old-convention names preserved)
- [ ] All INDEX links resolve to existing files (both old and new convention)
- [ ] `pytest tests/test_documentation_drift.py -W error` passes
- [ ] SPRINT_MANUAL updated: §2.2 (new convention), §2.3 (no rename for new files), §7.1 (no rename step), §8.4 (mismatch scan legacy-only)
- [ ] FOLDER_STRUCTURE updated to document both conventions (legacy + new)
- [ ] Docs impact checked: README / CLI_REFERENCE / ARCHITECTURE (updated or N/A)
- [ ] AI functionality check: N/A (no AI functionality)

---

## Implementation Notes

1. **New naming convention (new files only):**
   - AF files: `AF####_<three_word_description>.md`
   - BUG files: `BUG####_<three_word_description>.md`
   - ADR files: unchanged
2. **INDEX files must accept both conventions** — `test_documentation_drift.py` validation must be updated if it enforces filename patterns narrowly
3. **SPRINT_MANUAL sections to update:** §2.2, §2.3, §7.1, §8.4

---

## Files Touched
- `docs/dev/foundation/SPRINT_MANUAL.md` (§2.2, §2.3, §7.1, §8.4)
- `docs/dev/foundation/FOLDER_STRUCTURE_0.2.md` (add new convention alongside legacy)
- `tests/test_documentation_drift.py` (accept both naming conventions if filename pattern enforced)

---

## Risks

**Low.** No file renames. No code changes. Only documentation and test updates. New convention validated on first new AF created after this one.

---

## Completion

*(fill when Status = DONE)*
- **Review decision:**
- **Rationale:**
- **Follow-ups:**
- **PR link:**
