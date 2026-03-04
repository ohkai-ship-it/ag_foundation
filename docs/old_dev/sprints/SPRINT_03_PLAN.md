# Sprint Plan --- Sprint 03 --- Observability & Truthful UX

# Version number: v1.0

## Metadata

-   Sprint: Sprint 03
-   Updated: 2026-02-26
-   Owner: Kai
-   Tech Lead: Jeff
-   Implementer: Jacob

## Sprint Goal

Strengthen workspace maturity, fix manual mode gating, and enforce
observability + truthful UX per PROJECT_PLAN Sprint 03.

------------------------------------------------------------------------

## Scope (P0 Must Ship)

-   AF-0027 --- Default workspace policy (intuitive precedence)
-   AF-0028 --- Run ID truncation fix
-   AF-0029 --- RunTrace verification hardening
-   AF-0030 --- RunTrace metadata completeness
-   AF-0031 --- CLI truthfulness enforcement
-   AF-0032 --- Observability command expansion
-   AF-0033 --- Early .env loading + manual mode gate fix
-   BUG-0006 --- Manual mode .env loading defect

------------------------------------------------------------------------

## Workspace Resolution Order (Final Model)

1.  --workspace flag
2.  Persisted default workspace (CLI-set)
3.  AG_WORKSPACE env var
4.  If no default and no workspaces exist → create 'default'
5.  Else error with guidance

------------------------------------------------------------------------

## Definition of Done

-   [ ] Workspace precedence implemented and tested
-   [ ] Manual mode works with .env AG_DEV=1
-   [ ] No implicit workspace creation except bootstrap case
-   [ ] CLI labels trace-derived
-   [ ] pytest clean (no warnings)
-   [ ] Coverage maintained ≥ previous sprint
