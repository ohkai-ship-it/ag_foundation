# BUG-0006 --- Manual mode ignores .env AG_DEV

# Version number: v1.0

## Metadata

-   ID: BUG-0006
-   Status: Fixed
-   Severity: P1
-   Area: CLI
-   Reported by: Kai
-   Date: 2026-02-26
-   Resolved: 2026-02-27
-   Resolved by: AF-0033
-   Related backlog item(s): AF-0033

## Summary

Manual mode (--mode manual) fails even when AG_DEV=1 is set in .env.

## Expected behavior

CLI should load .env before checking AG_DEV and allow manual mode.

## Actual behavior

CLI reports AG_DEV not set.

## Reproduction

ag run --mode manual -w development01 "Test the pipeline"

## Acceptance Criteria

-   [ ] .env loaded early in CLI
-   [ ] Manual mode works when AG_DEV=1 in .env
-   [ ] Regression tests added

