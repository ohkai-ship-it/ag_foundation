# BUG REPORT — BUG0025 — leftover_ready_duplicates
# Version number: v1.3

---

## Metadata
- **ID:** BUG0025
- **Status:** OPEN
- **Severity:** P2
- **Area:** Process
- **Reported by:** Jacob (Sprint Review S16_REVIEW_01)
- **Date:** 2026-04-05
- **Related backlog item(s):** AF-0129, AF-0132, AF-0133, AF-0134, AF-0138
- **Related PR(s):** —

---

## Summary
Five Sprint 16 AF files have both a `*_READY_*` and `*_DONE_*` copy on disk. The READY files are identical duplicates of the DONE files (including `Status: DONE` internally). They should have been deleted during the READY→DONE rename.

---

## Expected behavior
After renaming READY→DONE per old convention, only the DONE file should remain.

---

## Actual behavior
Both files exist for AF-0129, AF-0132, AF-0133, AF-0134, AF-0138.

---

## Reproduction steps
1. `Get-ChildItem docs\dev\backlog\items -Filter "AF0129*"` — shows two files
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
- [ ] Only DONE files remain for AF-0129, AF-0132, AF-0133, AF-0134, AF-0138
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes
