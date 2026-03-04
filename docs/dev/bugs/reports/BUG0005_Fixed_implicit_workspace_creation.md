# BUG-0005 --- Implicit workspace creation on `ag run`

# Version number: v0.1

## Metadata

-   **ID:** BUG-0005
-   **Status:** Fixed
-   **Severity:** P0
-   **Area:** CLI \| Storage \| Runtime
-   **Reported by:** Architect review
-   **Date:** 2026-02-26
-   **Related backlog item(s):** AF-0026
-   **Related PR(s):** N/A

## Summary

When no workspace is explicitly selected, running `ag run` silently
creates a new workspace per invocation. This violates the architectural
invariant that workspaces are explicit isolation boundaries and that
runs must live inside an existing workspace.

## Expected behavior

-   `ag run` must NOT implicitly create new workspaces.
-   If no workspace is selected:
    -   Use explicit `--workspace`
    -   Or use configured default workspace
    -   Otherwise fail with a clear message

## Actual behavior

-   Each `ag run` without `--workspace` creates a new workspace
    automatically.
-   This results in workspace proliferation and incorrect isolation
    semantics.

## Reproduction steps

1.  Ensure no default workspace configured.
2.  Run: `ag run "test"`
3.  Observe new workspace created automatically.
4.  Repeat and observe another new workspace.

## Impact

-   Breaks workspace isolation model.
-   Conflicts with CLI contract and architectural design.
-   Makes run reproducibility unreliable.

## Proposed fix

-   Enforce explicit workspace selection or configured default.
-   Fail fast if no workspace exists.
-   Add regression tests ensuring no implicit creation.

## Acceptance criteria

-   [x] `ag run` does not create workspace implicitly.
-   [x] Clear error shown if workspace not selected.
-   [x] Repeated runs reuse same workspace DB.
-   [x] Regression tests added.
