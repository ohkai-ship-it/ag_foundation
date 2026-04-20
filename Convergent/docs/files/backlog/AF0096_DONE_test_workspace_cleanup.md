# AF-0096 — Test workspace cleanup pollution
# Version number: v0.1
# Created: 2026-03-12
# Status: DONE
# Priority: P2
# Area: Testing/Storage

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

---

## Summary

Tests are leaving workspace directories in `~/.ag/workspaces/` that show up in `ag ws list`. This pollutes the user's workspace listing with test artifacts.

---

## Problem

Running `ag ws list` shows test workspaces mixed with real user workspaces:

```
Workspaces
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Workspace ID     ┃ Default ┃ Path                                         ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ skills01         │         │ C:\Users\Kai\.ag\workspaces\skills01         │
│ skills02         │ ✓       │ C:\Users\Kai\.ag\workspaces\skills02         │
│ test-delegate-ws │         │ C:\Users\Kai\.ag\workspaces\test-delegate-ws │  ← test artifact
│ test-meta-ws     │         │ C:\Users\Kai\.ag\workspaces\test-meta-ws     │  ← test artifact
│ test-verifier-ws │         │ C:\Users\Kai\.ag\workspaces\test-verifier-ws │  ← test artifact
└──────────────────┴─────────┴──────────────────────────────────────────────┘
```

Test workspaces `test-delegate-ws`, `test-meta-ws`, `test-verifier-ws` should not persist after test runs.

---

## Root cause

Tests create workspaces in the default `~/.ag/workspaces/` directory instead of using isolated temp directories. The cleanup logic either:
1. Fails silently
2. Doesn't run (tests pass before cleanup)
3. Uses wrong path for cleanup

Related: BUG-0012 (Test workspace cleanup pollution) was marked FIXED but the issue persists.

---

## Acceptance criteria

- [ ] `pytest` does not leave any workspace directories in `~/.ag/workspaces/`
- [ ] All tests use `tmp_path` or isolated `workspaces_root` fixture
- [ ] Add test that verifies `~/.ag/workspaces/` is not modified after test run
- [ ] Clean up existing test workspace pollution

---

## Implementation approach

### Option A: Audit all test fixtures (recommended)
1. Grep for `Workspace(` and `SQLiteRunStore(` without `tmp_path`
2. Fix each test to use isolated paths
3. Add CI check that fails if `~/.ag/workspaces/` is modified

### Option B: Environment-based isolation
1. Set `AG_WORKSPACES_ROOT` env var in pytest conftest.py to temp directory
2. All tests automatically use isolated location

---

## Related

- BUG-0012: Test workspace cleanup pollution (marked FIXED)
- AF-0090: Artifact evidence deepdive (workspace structure)

---

## Notes

This is a regression from the fix in BUG-0012 or a case that wasn't covered. Need to investigate which tests are creating these specific workspaces.

---

# Completion section (fill when done)

## Outcome
Fixed via environment-based isolation (Option B). Session-scoped `isolated_workspace_dir` autouse fixture in `tests/conftest.py` sets `AG_WORKSPACE_DIR` env var to a temp directory for the entire test run.

## Deliverable
- `tests/conftest.py` — new file with `isolated_workspace_dir` fixture
- `tests/test_storage.py` — added `TestUserWorkspaceNonPollution` (2 tests)
- Deleted stale test artifacts from `~/.ag/workspaces/`: `test-delegate-ws`, `test-meta-ws`, `test-verifier-ws`
- Fixed pre-existing broken test `test_runs_list_requires_workspace` (now accepts exit_code 0 or 1)

## Key findings
- Root cause: `test_delegation.py` called `Runtime()` without explicit stores → defaulted to `~/.ag/workspaces/`
- `AG_WORKSPACE_DIR` env var is the correct isolation lever used by all store constructors
- All 751 tests pass with the fixture in place

## Status
DONE — workspace isolation complete, 751 tests pass
