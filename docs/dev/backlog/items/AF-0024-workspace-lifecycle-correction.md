# AF-0024 --- Workspace lifecycle correction

# Version number: v0.1

## Metadata

-   **ID:** AF-0024
-   **Type:** Foundation
-   **Status:** Done
-   **Priority:** P0
-   **Area:** Storage \| CLI
-   **Owner:** Jacob
-   **Target sprint:** Sprint 02 (Hardening Extension)

## Problem

Workspaces appear to be created implicitly per run. Runs must live
inside explicit workspace boundaries. Automatic workspace creation
violates architectural intent and storage isolation guarantees.

## Goal

Ensure workspace lifecycle is explicit and consistent: - Workspaces
created only via `ag ws create` - `ag run` never silently creates new
workspaces - Repeated runs reuse the same workspace database

## Non-goals

-   No redesign of workspace schema
-   No multi-tenant features

## Acceptance criteria (Definition of Done)

-   [ ] No implicit workspace creation during `ag run`
-   [ ] Multiple runs in same workspace reuse same DB file
-   [ ] `--workspace` flag strictly honored
-   [ ] Workspace ID correctly recorded in RunTrace
-   [ ] Tests covering repeated runs inside same workspace
-   [ ] Workspace isolation validated

## Implementation notes

-   Audit CLI run flow and workspace initialization logic
-   Add tests for repeated run behavior
-   Confirm DB path consistency

## Risks

-   Incorrect refactor could break run storage behavior

## PR plan (PR-sized)

1.  PR #1: Workspace lifecycle audit + fix + tests
