# AF-0022 --- Provider coverage hardening (OpenAI adapter ≥95%)

Version: v0.1

## Metadata

-   ID: AF-0022
-   Type: Foundation
-   Status: Done
-   Priority: P1
-   Area: Integrations
-   Owner: Jacob
-   Target sprint: Sprint 02 (Hardening follow-up)

## Problem

OpenAI provider adapter coverage is currently 83%, below the required
≥95% bar.

## Goal

Increase coverage of src/ag/providers/openai.py to ≥95%.

## Non-goals

-   No functional feature expansion.
-   No multi-provider feature additions.

## Acceptance criteria (Definition of Done)

-   [ ] Coverage for openai.py ≥95%.
-   [ ] All provider error branches tested.
-   [ ] No real network calls in tests.
-   [ ] pytest --cov shows threshold satisfied.

## Implementation notes

-   Add tests for error paths, invalid model, malformed response,
    timeout handling.
-   Use mocks for provider responses.
-   Validate raw responses are not persisted.

## Risks

-   Over-mocking may reduce realism; focus on contract behavior.

## PR plan

1.  PR #1: Add missing branch coverage tests.
