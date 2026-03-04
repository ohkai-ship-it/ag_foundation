# BACKLOG ITEM --- AF0052 --- restore_coverage_threshold

# Version number: v0.1

## Metadata

-   **ID:** AF0052
-   **Type:** Foundation
-   **Status:** Ready
-   **Priority:** P0
-   **Area:** Testing / CI
-   **Owner:** Jacob
-   **Target sprint:** Sprint06 --- TBD

------------------------------------------------------------------------

## Problem

Sprint05 reduced overall coverage to 79%, below the mandatory ≥85%
threshold defined in FOUNDATION_MANUAL.md.

This violates CI discipline invariants.

------------------------------------------------------------------------

## Goal

Restore overall coverage to ≥85% while maintaining: - Provider ≥95% -
Storage ≥95% - Core ≥85%

------------------------------------------------------------------------

## Non-goals

-   No feature expansion
-   No architectural refactor beyond what is required for coverage
    compliance

------------------------------------------------------------------------

## Acceptance criteria

-   [ ] `pytest --cov=src/ag --cov-report=term-missing` shows ≥85%
    overall
-   [ ] Provider coverage ≥95%
-   [ ] No test exclusions added to mask coverage gaps
-   [ ] CI green on main
-   [ ] Completion section filled when done

------------------------------------------------------------------------

## Risks

-   Reveals untested architectural assumptions
-   May require minor refactoring to enable testability

------------------------------------------------------------------------

# Completion section (fill when done)
