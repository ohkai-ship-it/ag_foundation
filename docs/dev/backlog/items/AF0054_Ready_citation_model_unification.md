# BACKLOG ITEM --- AF0054 --- citation_model_unification

# Version number: v0.1

## Metadata

-   **ID:** AF0054
-   **Type:** Architecture
-   **Status:** Ready
-   **Priority:** P1
-   **Area:** Core / Skills
-   **Owner:** Jacob
-   **Target sprint:** Sprint06 --- TBD

------------------------------------------------------------------------

## Problem

Sprint05 introduced overlap between EvidenceRef and Citation models,
creating ambiguity in ownership of citation semantics.

------------------------------------------------------------------------

## Goal

Unify citation representation by: - Defining single canonical citation
model - Clarifying ownership (Skill vs Core) - Updating trace contract
documentation

------------------------------------------------------------------------

## Non-goals

-   No retrieval/indexing implementation
-   No schema breaking changes

------------------------------------------------------------------------

## Acceptance criteria

-   [ ] Single citation model defined and used consistently
-   [ ] Trace contract updated (if required)
-   [ ] Backward compatibility preserved
-   [ ] Tests updated accordingly

------------------------------------------------------------------------

## Risks

-   Trace schema change may require ADR if breaking
-   Migration complexity if references already persisted

------------------------------------------------------------------------

# Completion section (fill when done)
