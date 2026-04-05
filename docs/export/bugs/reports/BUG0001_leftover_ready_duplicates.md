# BUG REPORT — BUG0001 — leftover_ready_duplicates
# Version number: v1.3

---

## Metadata
- **ID:** BUG0001
- **Status:** OPEN
- **Severity:** P2
- **Area:** Process
- **Reported by:** Jacob (Sprint Review S01_REVIEW_01)
- **Date:** 2026-04-05
- **Related backlog item(s):** AF-0001, AF-0004, AF-0005, AF-0006, AF-0010
- **Related PR(s):** —

---

## Summary
Five Sprint 01 AF files have both a `*_READY_*` and `*_DONE_*` copy on disk. The READY files are identical duplicates of the DONE files (including `Status: DONE` internally). They should have been deleted during the READY→DONE rename.

---

## Expected behavior
After renaming READY→DONE per old convention, only the DONE file should remain.

---

## Actual behavior
Both files exist for AF-0001, AF-0004, AF-0005, AF-0006, AF-0010.

---

## Reproduction steps
1. `Get-ChildItem docs\dev\backlog\items -Filter "AF0001*"` — shows two files
2. Compare: content is identical

---

## Evidence
- **Environment:** Windows, Python 3.14.0, commit 192cb62

---

## Impact
Cosmetic only. No functional impact. May cause confusion for future audits.

---

## Proposed fix
Delete the 5 leftover READY files.

---

## Acceptance criteria (for verification)
- [ ] Only DONE files remain for AF-0001, AF-0004, AF-0005, AF-0006, AF-0010
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes
