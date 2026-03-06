# BACKLOG ITEM --- AF0054 --- citation_model_unification

# Version number: v0.1

## Metadata

-   **ID:** AF0054
-   **Type:** Architecture
-   **Status:** Done
-   **Priority:** P1
-   **Area:** Core / Skills
-   **Owner:** Jacob
-   **Target sprint:** Sprint05 --- High_Pressure_Skills (follow-up)

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

-   [x] Single citation model defined and used consistently
-   [x] Trace contract updated (if required)
-   [x] Backward compatibility preserved
-   [x] Tests updated accordingly

------------------------------------------------------------------------

## Risks

-   Trace schema change may require ADR if breaking
-   Migration complexity if references already persisted

------------------------------------------------------------------------

# Completion section (fill when done)

## Summary

Clarified ownership between `Citation` (skill output) and `EvidenceRef` (trace metadata):

- **EvidenceRef** (Core): Canonical trace-level evidence model in `run_trace.py`
- **Citation** (Skill): Lightweight output artifact model in skill modules

Added `Citation.to_evidence_ref()` for conversion when recording to trace.

## Changes

1. `src/ag/skills/strategic_brief.py`:
   - Added module docstring explaining model relationship
   - Added `to_evidence_ref()` method to `Citation` class

2. `src/ag/core/run_trace.py`:
   - Enhanced `EvidenceRef` docstring with ownership note and source_type docs

3. `ARCHITECTURE.md`:
   - Added Section 6.2 "Citation models" documenting the two-layer pattern

4. `tests/test_strategic_brief.py`:
   - Added 5 tests for `Citation.to_evidence_ref()` conversion

## Results

- 322 tests pass
- Coverage: 88%
- No breaking changes (additive only)
- Backward compatible: existing Citation usage unchanged
