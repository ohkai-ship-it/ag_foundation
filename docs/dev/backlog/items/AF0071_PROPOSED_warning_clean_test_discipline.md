# BACKLOG ITEM — AF0071 — warning_clean_test_discipline
# Version number: v0.2

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - CI discipline (ruff + pytest -W error + coverage)
> - INDEX update rule (status ↔ filename integrity)

> **File naming (required):** `AF####_<Status>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0071
- **Type:** Bug Fix / Testing
- **Status:** PROPOSED
- **Priority:** P1
- **Area:** Testing / Storage
- **Owner:** TBD
- **Target sprint:** Backlog
- **Depends on:** None
- **Related:** BUG-0012 (test workspace cleanup pollution)

---

## Problem

The CI discipline requires `pytest -W error` to pass cleanly, but Sprint 07 review confirms it currently fails with 2 test failures:

```
FAILED tests/test_cli.py::TestRunWithSkillFlag::test_run_skill_json_output
FAILED tests/test_cli_global_options.py::TestHelpGlobalOptions::test_main_help_shows_global_options
```

**Root cause:** SQLite connections are not being properly closed after CLI tests, generating `ResourceWarning: unclosed database` warnings that become errors under `-W error`.

This is documented in BUG-0012 but remains unresolved.

---

## Evidence

From S07_REVIEW_01 pytest_summary.txt:
```
pytest -q: 412 passed, 3 deselected
pytest -W error: 2 failed, 410 passed, 3 deselected

Failures:
1. test_run_skill_json_output - ResourceWarning unclosed SQLite connection
2. test_main_help_shows_global_options - ResourceWarning unclosed SQLite connection
```

---

## Acceptance Criteria

1. **`pytest -W error` passes cleanly** — Zero warnings promoted to errors
2. **SQLite connections properly closed** — No ResourceWarning for unclosed database
3. **No regression** — All 412+ tests continue to pass
4. **Coverage maintained** — ≥86% coverage threshold

---

## Proposed Solution

Option A: **Connection lifecycle fix in storage layer**
- Ensure `SQLiteRunStore` and `SQLiteArtifactStore` close connections deterministically
- Add `__del__` or context manager pattern for automatic cleanup

Option B: **Test fixture cleanup**
- Add autouse pytest fixture that closes any open connections after each test
- Scope: module or function level depending on performance impact

Option C: **CLI command isolation**
- Ensure CLI commands don't leave database handles open after completion
- May require explicit store closing in CLI command functions

---

## Out of Scope
- BUG-0007 (OpenAI SDK caching) — separate issue
- General test performance optimization

---

## References
- BUG-0012: `/docs/dev/bugs/reports/BUG0012_OPEN_test_workspace_cleanup.md`
- S07_REVIEW_01: `/docs/dev/sprints/documentation/Sprint07_summarize_playbook/S07_REVIEW_01.md`
- pytest_summary: `artifacts/review_S07_01/pytest_summary.txt`
