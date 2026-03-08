# BUG REPORT — BUG0012 — test_workspace_cleanup
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - INDEX update rule (status ↔ filename integrity)
> - Evidence capture requirement (RunTrace ID for CLI/runtime bugs)

> **File naming (required):** `BUG0012_OPEN_test_workspace_cleanup.md`
> Status values: `OPEN | IN_PROGRESS | FIXED | VERIFIED | DROPPED`

---

## Metadata
- **ID:** BUG0012
- **Status:** OPEN
- **Severity:** P2
- **Area:** Testing / Storage
- **Reported by:** Kai
- **Date:** 2026-03-08
- **Related backlog item(s):** AF0046 (test isolation framework)
- **Related ADR(s):** N/A
- **Related PR(s):** N/A

---

## Summary
Tests create workspace folders under the user's real `~/.ag/workspaces/` directory that persist after test completion. Users observe leftover test workspace folders even after deleting them manually, suggesting some tests are not properly isolated to temporary directories.

---

## Expected behavior
All tests should:
1. Use `tmp_path` fixture or `AG_WORKSPACE_DIR` environment override
2. Create workspaces only in temporary directories
3. Leave no artifacts in the user's real `~/.ag/workspaces/` folder after test runs

---

## Actual behavior
After running the test suite, workspace folders appear in `~/.ag/workspaces/` that were created by tests. These folders persist and reappear even after manual deletion, indicating ongoing test pollution.

---

## Reproduction steps
1. Clear `~/.ag/workspaces/` folder
2. Run `pytest tests/`
3. Check `~/.ag/workspaces/` — expect empty, but may find test-created folders
4. Delete any found folders
5. Run tests again — folders may reappear

---

## Evidence
- **Environment:** Windows, Python 3.14.0, pytest 9.0.2
- **Observed folders:** Various test workspace names appearing in real workspace directory
- **Test files potentially affected:** Tests using `Workspace()` without `tmp_path` parameter

---

## Impact
- **User experience:** Confusing leftover folders in workspace directory
- **Disk usage:** Accumulated test artifacts consume space
- **Isolation violation:** Tests should not touch user's real environment

---

## Suspected cause
Some tests may:
1. Call `Workspace("name")` without passing a `tmp_path` root directory
2. Not set `AG_WORKSPACE_DIR` environment variable before workspace operations
3. Use CLI runner without proper environment isolation

Tests that properly isolate use patterns like:
- `Workspace("name", tmp_path)` — explicit temp root
- `monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path))` — env override

---

## Proposed fix
1. Audit all test files for `Workspace()` calls without `tmp_path` parameter
2. Ensure all CLI runner invocations set `AG_WORKSPACE_DIR` in env
3. Add a pytest fixture in `conftest.py` that auto-sets `AG_WORKSPACE_DIR` for all tests
4. Consider adding a test that fails if any test writes to real workspace dir

Example global fixture:
```python
@pytest.fixture(autouse=True)
def isolate_workspace_dir(tmp_path, monkeypatch):
    """Prevent tests from touching real workspace directory."""
    monkeypatch.setenv("AG_WORKSPACE_DIR", str(tmp_path / "workspaces"))
```

---

## Acceptance criteria (for verification)
- [ ] `~/.ag/workspaces/` remains empty after full test suite run
- [ ] All tests use isolated workspace directories
- [ ] No test calls `Workspace()` without explicit temp root or env override
- [ ] `pytest -W error` passes
- [ ] Add regression test to detect future workspace pollution
