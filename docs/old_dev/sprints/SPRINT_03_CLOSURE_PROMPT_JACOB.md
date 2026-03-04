# Sprint 03 Closure Prompt --- Jacob

# Version: v1.0

# Date: 2026-02-27

## Role

Junior Engineer --- Implementation & Repository Hygiene

## Sprint

Sprint 03 --- Observability & Truthful UX

## Status

Approved (PM + Architect)

------------------------------------------------------------------------

# Objective

Formally close Sprint 03 with full documentation alignment, backlog
updates, and repository hygiene.

Follow strictly:

-   COLLABORATION_MANIFEST.md
-   GITHUB_FLOW.md
-   REPO_HYGIENE_LIST.md

No shortcuts.

------------------------------------------------------------------------

# 1. Completion Notes

Create:

/docs/dev/sprints/S03_COMPLETION_NOTE.md

Using COMPLETION_NOTE_TEMPLATE.md

Include: - Summary of sprint - Delivered AFs (0027--0033) - BUG-0006
resolved - Coverage metrics (188 tests) - Architectural validation -
Deferred AFs (0034--0038) - Risk summary - Sign-off statement

------------------------------------------------------------------------

# 2. Backlog & Status Updates

## Update Backlog Index

-   AF-0027 → AF-0033 → Completed
-   BUG-0006 → Resolved
-   AF-0034, 0035, 0037, 0038 → Ready
-   AF-0036 → Proposed

Ensure consistency between: - Backlog index - Individual AF files - Bug
files

## Update Individual Files

For completed items: - Status → Completed - Completed in Sprint → Sprint
03 - Add completion date - Add PR reference (if available)

For BUG-0006: - Status → Resolved - Link to AF-0033

------------------------------------------------------------------------

# 3. Sprint Report Finalization

Create or update:

/docs/dev/sprints/SPRINT_03_REPORT.md

Using SPRINT_REPORT_TEMPLATE.md

Include: - Metrics - Test delta - Risk log - Lessons learned -
Improvement candidates (AF-0034--0038)

------------------------------------------------------------------------

# 4. Documentation Consistency Audit

Validate:

-   Naming conventions consistent
-   Sprint numbering correct
-   No orphan references
-   No stale TODO markers
-   No duplicated status fields

------------------------------------------------------------------------

# 5. Git Hygiene

Ensure:

-   1 PR = 1 AF discipline maintained
-   All PRs merged cleanly
-   No direct-to-main exceptions (or document them)

------------------------------------------------------------------------

# 6. Repository Hygiene

Execute:

-   pytest -W error
-   Coverage report
-   Ruff lint
-   Remove dead imports
-   Remove debug prints
-   Ensure no secrets persisted
-   Ensure .env not committed
-   Ensure no workspace artifacts versioned

Document results in completion note.

------------------------------------------------------------------------

# 7. Final Validation Checklist

-   All tests pass
-   Coverage regenerated
-   No P0/P1 open
-   All indices synchronized
-   Completion note exists

------------------------------------------------------------------------

# Guardrails

-   No feature work
-   No refactors
-   No scope expansion
-   No behavior changes

This is a closure pass only.

------------------------------------------------------------------------

# Definition of Done

Sprint 03 is closed when:

-   Documentation consistent
-   Backlog synchronized
-   Hygiene checks pass
-   Completion note finalized
