# AF-0026 --- Workspace selection policy enforcement

# Version number: v0.1

## Metadata

-   **ID:** AF-0026
-   **Type:** Foundation
-   **Status:** Done
-   **Priority:** P0
-   **Area:** CLI \| Runtime \| Storage
-   **Owner:** Jacob
-   **Target sprint:** Sprint 02 (Hardening Follow-up)

## Problem

`ag run` currently creates workspaces implicitly when none is selected.
This contradicts the architecture contract that workspaces are explicit
isolation boundaries.

## Goal

Implement a deterministic workspace selection policy:

1)  If `--workspace` provided → use it
2)  Else if default workspace configured → use it
3)  Else → fail with explicit error message

Implicit workspace creation must be eliminated.

## Non-goals

-   No redesign of workspace schema.
-   No multi-tenant feature additions.

## Acceptance criteria (Definition of Done)

-   [x] No implicit workspace creation during `ag run`
-   [x] Explicit error message when no workspace selected
-   [x] Default workspace behavior clearly defined
-   [x] Regression tests covering selection logic
-   [x] CLI_REFERENCE updated to reflect final policy

## Implementation notes

-   Audit CLI run path.
-   Remove auto-creation branch.
-   Ensure RunTrace records correct workspace_id.
-   Update documentation accordingly (existing docs only).

## Risks

-   Could temporarily break user flows relying on implicit behavior.
-   Must ensure tests updated accordingly.

## PR plan (PR-sized)

1.  PR #1: Implement workspace selection enforcement + regression tests.
