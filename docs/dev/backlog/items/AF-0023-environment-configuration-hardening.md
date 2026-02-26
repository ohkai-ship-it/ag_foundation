# AF-0023 --- Environment & configuration hardening

# Version number: v0.1

## Metadata

-   **ID:** AF-0023
-   **Type:** Foundation
-   **Status:** Done
-   **Priority:** P1
-   **Area:** Docs \| CLI \| Kernel
-   **Owner:** Jacob
-   **Target sprint:** Sprint 02 (Hardening Extension)

## Problem

We recently introduced `.env` configuration. Hardcoded paths, implicit
defaults, or embedded secrets may still exist. This creates portability
risks and violates configuration resolution rules.

## Goal

Ensure configuration and environment handling is fully centralized,
portable, and deterministic.

## Non-goals

-   No feature expansion
-   No storage backend changes

## Acceptance criteria (Definition of Done)

-   [ ] No hardcoded filesystem paths outside configuration layer
-   [ ] No secrets hardcoded in source files
-   [ ] Centralized `.env` loading mechanism
-   [ ] Configuration resolution order enforced: TaskSpec → Workspace →
    .env → Defaults
-   [ ] Tests verifying config precedence behavior
-   [ ] `ag doctor` validates environment consistency

## Implementation notes

-   Audit repository for hardcoded paths and secrets
-   Refactor config access to single entry point
-   Add regression tests for config resolution order

## Risks

-   Misordered resolution could alter runtime behavior

## PR plan (PR-sized)

1.  PR #1: Audit + refactor configuration loading and precedence
