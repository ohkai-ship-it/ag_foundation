# AF-0025 --- Test discipline enforcement (coverage + warnings + Ruff)

# Version number: v0.1

## Metadata

-   **ID:** AF-0025
-   **Type:** Docs \| Foundation
-   **Status:** Done
-   **Priority:** P1
-   **Area:** Docs \| Repo
-   **Owner:** Jacob
-   **Target sprint:** Sprint 02 (Hardening Extension)

## Problem

Coverage thresholds, warning policy, and linting enforcement are not
formally codified in documentation and workflow.

## Goal

Enforce engineering discipline via documentation and CI expectations: -
Coverage thresholds defined - Warnings treated as errors - Ruff
mandatory

## Non-goals

-   No CI provider migration
-   No new documentation files created

## Acceptance criteria (Definition of Done)

-   [ ] Testing Guidelines updated with coverage thresholds: - Overall
    ≥85% - CLI ≥72% - Providers ≥95% - Storage ≥95%
-   [ ] Policy added: warnings fail CI (`pytest -W error`)
-   [ ] PR Checklist updated to require Ruff
-   [ ] Repo Hygiene updated to require Ruff check/format
-   [ ] Collaboration Manifest reflects stricter discipline

## Implementation notes

-   Update existing docs only
-   Do not introduce new documentation files
-   Ensure CI instructions reflect new enforcement rules

## Risks

-   Increased strictness may initially surface hidden issues

## PR plan (PR-sized)

1.  PR #1: Documentation updates + enforcement instructions
