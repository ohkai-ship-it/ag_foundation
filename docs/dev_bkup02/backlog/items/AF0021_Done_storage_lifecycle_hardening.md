# AF0021 — Storage lifecycle hardening (SQLite deterministic closure)
# Version number: v0.2

## Metadata
- **ID:** AF-0021
- **Type:** Foundation
- **Status:** DONE
- **Priority:** P1
- **Area:** Storage
- **Owner:** Jacob
- **Completed in:** Sprint 02 (Hardening)
- **Completion date:** 2026-02-26

## Problem
SQLite connections are not deterministically closed, leading to ResourceWarnings and intermittent test failures.

## Goal
Ensure all SQLite connections are safely managed and closed under all execution paths.

## Non-goals
- No storage backend changes (SQLite remains).
- No schema redesign.

## Acceptance criteria (Definition of Done)
- [x] All sqlite3.connect usage wrapped in context manager or explicitly closed.
- [x] pytest -W error passes.
- [x] No ResourceWarning in test runs.
- [x] Regression test added to enforce closure.

## Implementation notes
- Refactor sqlite_store.py to centralize connection creation.
- Add context-managed helper method for DB access.
- Audit workspace lifecycle paths.

## Risks
- Refactor could unintentionally affect transaction boundaries.

## PR plan
1. PR #1: Refactor connection handling + add regression test.

---
# Completion section (fill when done)

**Completion date:** 2026-02-26  
**Author:** Jacob

**Summary:**
Closed SQLite connections deterministically via context manager pattern. Eliminated ResourceWarning from connection leaks. Storage module coverage ≥95%.

**What Changed:**
- `src/ag/storage/sqlite_store.py` — Added `__enter__`, `__exit__` context manager methods, connection cleanup
- `src/ag/storage/workspace.py` — Added `__enter__`, `__exit__` context manager methods
- `tests/test_storage.py` — Added tests for connection lifecycle, context manager behavior

**Architecture Alignment:**
- Storage layer only; clean separation maintained
- Context manager is additive; direct usage still works

**Tests Executed:**
- pytest tests/test_storage.py: PASS (23 tests)
- pytest -W error: PASS (174 tests, no ResourceWarning)
- Storage coverage: 96%

**Run Evidence:**
- `pytest -W error` — no ResourceWarning
- `with Workspace(...) as ws:` pattern works

