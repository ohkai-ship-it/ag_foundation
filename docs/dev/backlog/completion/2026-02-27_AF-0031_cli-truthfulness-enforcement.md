# Completion Note — AF-0031 — CLI truthfulness enforcement
# Version number: v1.0

> Strict template. Fill every section. If something is not applicable, write **N/A** (do not delete sections).

## 1) Metadata
- **Backlog item (primary):** AF-0031
- **PR:** N/A (direct commit)
- **Author:** Jacob
- **Date:** 2026-02-27
- **Branch:** main
- **Risk level:** P0
- **Runtime mode used for verification:** manual (dev/test-only)

## 2) Goal and acceptance criteria
### Goal (from backlog item)
Ensure all CLI labels derive strictly from RunTrace fields.

### Acceptance criteria (from backlog item)
- [x] No hardcoded status labels in CLI output
- [x] All labels extracted from RunTrace fields
- [x] `extract_labels()` function for consistent label derivation
- [x] Tests verify label extraction

## 3) What changed (file-level)
- `src/ag/cli/main.py` — Added `extract_labels()` function for trace-derived labels
- `src/ag/cli/main.py` — Updated run display commands to use `extract_labels()`
- `tests/test_cli_truthful.py` — Added `TestExtractLabels` class with tests

## 4) Architecture alignment (mandatory)
- **Layering:** CLI adapter only
- **Interfaces touched:** None (internal refactor)
- **Backward compatibility:** No change to user-facing output

## 5) Truthful UX check (mandatory)
- **User-visible labels affected:** All status labels in CLI output
- **Trace fields backing them:** `final_status`, `verifier_status`, `workspace_source`, etc.
- **Proof:** `extract_labels(trace)` returns dict mapping to trace fields

## 6) Tests executed (mandatory)
- Command: `pytest tests/test_cli_truthful.py::TestExtractLabels -v`
  - Result: PASS
- Command: `pytest -W error --ignore=tests/test_providers.py`
  - Result: PASS (188 tests)

## 7) Run evidence (mandatory for behavior changes)
- **RunTrace ID(s):** N/A (internal refactor)
- **How to reproduce:** `ag runs show <id>` — labels match trace fields
- **Expected outcomes:** Every displayed label is trace-derived

## 8) Artifacts (if applicable)
N/A

## 9) Open issues discovered
None.

## 10) Deferred / follow-up items
None.
