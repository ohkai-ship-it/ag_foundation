# BUG-0004 --- SQLite connections not closed → unraisable warnings / intermittent test failure

Version: v0.2

## Metadata

-   ID: BUG-0004
-   Status: Fixed
-   Severity: P1
-   Area: Storage
-   Reported by: Kai
-   Date: 2026-02-26
-   Related backlog item(s): AF-0021, AF-0022
-   Related PR(s): N/A

## Summary

On Windows (Python 3.14), pytest may fail with an ExceptionGroup of
unraisable exceptions due to ResourceWarning: unclosed database for
multiple sqlite3.Connection objects. This appears environment / GC
timing sensitive (intermittent).

## Expected behavior

-   All SQLite connections are deterministically closed.
-   No ResourceWarning or PytestUnraisableExceptionWarning.
-   Delegation CLI JSON tests are stable.

## Actual behavior

-   Failure in
    tests/test_delegation.py::TestDelegationCLI::test_cli_runs_show_json_has_subtasks
-   Multiple unclosed sqlite3.Connection objects reported during
    finalization.

## Reproduction steps

1.  Run: pytest -q
2.  Observe intermittent failure with unraisable warnings.

## Evidence

-   Failure stack traces indicating unclosed sqlite3 connections.
-   Coverage run shows warnings count \> 0.

## Impact

-   Test suite instability.
-   Violates Sprint DoD requirement: "no warnings".
-   Indicates improper storage lifecycle handling.

## Suspected cause

-   SQLite connections created but not deterministically closed in
    certain code paths (likely sqlite_store.py or workspace lifecycle
    paths).

## Proposed fix

-   Use context managers for all sqlite3.connect calls.
-   Ensure explicit .close() in teardown paths.
-   Add regression test enforcing no ResourceWarning.

## Acceptance criteria

-   [x] All connections closed deterministically.
-   [x] pytest -W error passes.
-   [x] No ResourceWarning emitted.
-   [x] Delegation CLI JSON test stable.

## Resolution

Fixed in Sprint 02 hardening extension. Context managers added to:
-   `src/ag/storage/sqlite_store.py`: `SQLiteRunStore` and `SQLiteArtifactStore`
-   `src/ag/core/runtime.py`: `V0Orchestrator` and `Runtime` classes

All 207 tests pass with `-W error` flag. No ResourceWarning emitted.

## Notes

This blocks Sprint 02 certification until resolved.
