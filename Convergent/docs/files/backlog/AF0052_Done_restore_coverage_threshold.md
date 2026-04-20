# BACKLOG ITEM --- AF0052 --- restore_coverage_threshold

# Version number: v0.1

## Metadata

-   **ID:** AF0052
-   **Type:** Foundation
-   **Status:** Done
-   **Priority:** P0
-   **Area:** Testing / CI
-   **Owner:** Jacob
-   **Target sprint:** Sprint05 --- High_Pressure_Skills (follow-up)

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

-   [x] `pytest --cov=src/ag --cov-report=term-missing` shows ≥85%
    overall
-   [x] Provider coverage ≥95%
-   [x] No test exclusions added to mask coverage gaps
-   [x] CI green on main
-   [x] Completion section filled when done

------------------------------------------------------------------------

## Risks

-   Reveals untested architectural assumptions
-   May require minor refactoring to enable testability

------------------------------------------------------------------------

# Completion section (fill when done)

## Summary

Fixed test timing issue in `test_providers.py` where environment variable
was cleared AFTER provider initialization, causing the provider to capture
the API key at init time.

## Changes

- `tests/test_providers.py`: Reordered `test_openai_validate_without_key_raises`
  and `test_openai_chat_without_key_raises` to clear `OPENAI_API_KEY` BEFORE
  creating the provider instance.

## Results

- 317 tests pass (was 315 passed, 2 failed)
- Overall coverage: 88% (≥85% ✓)
- Provider module coverage: 97% (≥95% ✓)
- Storage module coverage: 96% (≥95% ✓)

## Commit

`6c2b27c` - fix(AF0052): correct provider test timing - clear env before provider init

