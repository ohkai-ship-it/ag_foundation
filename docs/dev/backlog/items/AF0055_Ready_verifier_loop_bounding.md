# BACKLOG ITEM --- AF0055 --- verifier_loop_bounding

# Version number: v0.1

## Metadata

-   **ID:** AF0055
-   **Type:** Architecture
-   **Status:** Done
-   **Priority:** P1
-   **Area:** Verifier / Orchestrator
-   **Owner:** Jacob
-   **Target sprint:** Sprint05 --- High_Pressure_Skills (follow-up)

------------------------------------------------------------------------

## Problem

Verifier repair loop introduced in Sprint05 must be bounded and
trace-visible to avoid unbounded retries and hidden instability.

------------------------------------------------------------------------

## Goal

Formalize verifier loop control by: - Explicit max retry count -
Trace-visible retry metadata - Deterministic repair loop structure

------------------------------------------------------------------------

## Non-goals

-   No policy/budget engine implementation
-   No change to reasoning modes

------------------------------------------------------------------------

## Acceptance criteria

-   [x] Repair loop bounded by configurable limit
-   [x] Retry count recorded in RunTrace
-   [x] Tests validate loop termination
-   [x] No infinite retry scenarios possible

------------------------------------------------------------------------

## Risks

-   Requires orchestrator interface clarification
-   May expose deeper execution coupling

------------------------------------------------------------------------

# Completion section (fill when done)

## Summary

Formalized verifier loop bounding with explicit constants and safety ceiling:

- `DEFAULT_MAX_VALIDATION_ATTEMPTS = 3` (conservative default)
- `MAX_VALIDATION_ATTEMPTS_CEILING = 10` (safety ceiling, enforced)

Loop is mathematically guaranteed to terminate:
- max_attempts must be >= 1 (enforced at init)
- max_attempts cannot exceed ceiling (enforced at init)
- Loop counter runs from 1 to max_attempts (inclusive)
- No early exits bypass the counter

## Changes

1. `src/ag/core/schema_verifier.py`:
   - Added `DEFAULT_MAX_VALIDATION_ATTEMPTS` constant (3)
   - Added `MAX_VALIDATION_ATTEMPTS_CEILING` constant (10)
   - Added ceiling enforcement in `SchemaValidator.__init__`
   - Updated docstrings with loop bounding documentation

2. `src/ag/core/__init__.py`:
   - Exported both constants

3. `tests/test_schema_verifier.py`:
   - Added 10 new tests in `TestLoopBounding` class
   - Tests verify constants, ceiling enforcement, termination, trace metadata

## Results

- 332 tests pass
- 10 new loop bounding tests
- Coverage: 88%
- Infinite retry scenarios impossible by construction