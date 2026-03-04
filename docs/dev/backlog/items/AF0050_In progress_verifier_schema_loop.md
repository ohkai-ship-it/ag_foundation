# BACKLOG ITEM --- AF0050 --- Verifier schema loop

## Metadata

-   **ID:** AF0050
-   **Type:** Feature
-   **Status:** In progress
-   **Priority:** P0
-   **Area:** Verifier
-   **Owner:** Jacob
-   **Target sprint:** Sprint05 --- High_Pressure_Skills

------------------------------------------------------------------------

## Problem

Current architecture has not been forced through a realistic, multi-file
structured-output scenario.

------------------------------------------------------------------------

## Goal

Implement JSON schema validation step with repair loop recorded in
RunTrace.

------------------------------------------------------------------------

## Non-goals

-   No API layer
-   No full RAG implementation
-   No policy engine formalization

------------------------------------------------------------------------

## Acceptance criteria

-   [x] Implementation complete
-   [x] Naming conventions applied
-   [x] INDEX updated
-   [x] CI passes (ruff + pytest -W error + coverage)
-   [ ] Evidence captured (RunTrace ID)
-   [ ] Completion section filled when done

------------------------------------------------------------------------

## Risks

-   Architectural stress may expose hidden contract weaknesses

------------------------------------------------------------------------

# Completion section (to fill when done)
## Implementation summary

Created `src/ag/core/schema_verifier.py` with:

1. **ValidationAttempt** - Pydantic model to record each validation attempt
2. **ValidationResult** - Final result of validation loop with all attempts
3. **SchemaValidator** - Class to validate data against Pydantic models with repair loop
4. **record_validation_steps()** - Records validation attempts as VERIFICATION steps in RunTrace
5. **run_validation_loop()** - Main entry point for schema validation with RunTrace integration
6. **create_verification_step()** - Creates a Step from a ValidationAttempt

The repair loop pattern:
- Attempts validation against a Pydantic schema
- On failure, calls optional repair function (e.g., LLM-based fix)
- Records each attempt as a VERIFICATION step with EvidenceRef
- Retries up to max_attempts (default: 3)
- Updates RunTrace verifier status based on final result

All new types exported via `ag.core` module.

## Files changed

- `src/ag/core/schema_verifier.py` (new) - 338 lines, 100% coverage
- `src/ag/core/__init__.py` - exports for new types
- `tests/test_schema_verifier.py` (new) - 34 tests

## Test results

- 34 new tests, all passing
- 100% coverage on schema_verifier.py
- Overall coverage: 90%