# AF-0021 --- Storage lifecycle hardening (SQLite deterministic closure)

Version: v0.1

## Metadata

-   ID: AF-0021
-   Type: Foundation
-   Status: Done
-   Priority: P1
-   Area: Storage
-   Owner: Jacob
-   Target sprint: Sprint 02 (Hardening follow-up)

## Problem

SQLite connections are not deterministically closed, leading to
ResourceWarnings and intermittent test failures.

## Goal

Ensure all SQLite connections are safely managed and closed under all
execution paths.

## Non-goals

-   No storage backend changes (SQLite remains).
-   No schema redesign.

## Acceptance criteria (Definition of Done)

-   [ ] All sqlite3.connect usage wrapped in context manager or
    explicitly closed.
-   [ ] pytest -W error passes.
-   [ ] No ResourceWarning in test runs.
-   [ ] Regression test added to enforce closure.

## Implementation notes

-   Refactor sqlite_store.py to centralize connection creation.
-   Add context-managed helper method for DB access.
-   Audit workspace lifecycle paths.

## Risks

-   Refactor could unintentionally affect transaction boundaries.

## PR plan

1.  PR #1: Refactor connection handling + add regression test.
