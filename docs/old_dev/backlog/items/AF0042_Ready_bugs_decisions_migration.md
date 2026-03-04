# AF0042 — Bugs + Decisions migration: rename/move files + update indexes/templates
# Version number: v0.1

## Metadata
- **ID:** AF0042
- **Type:** Docs | Refactor
- **Status:** Done
- **Priority:** P1
- **Area:** Docs/Bugs/Decisions
- **Owner:** Jacob
- **Target sprint:** Sprint04
- **Completion date:** 2026-03-03

## Problem
BUG and ADR artifacts are in legacy locations and use inconsistent naming (`BUG-000x-...`, `ADR-000x-...`). Index files are generic `INDEX.md` and are spread across many folders.

## Goal
Create canonical bugs and decisions systems in `/docs/dev/bugs` and `/docs/dev/decisions` with strict filenames, updated templates, and renamed indexes.

## Non-goals
No changes to the actual bug/ADR content besides path updates, metadata alignment, and optional slug normalization.

## Renaming / naming conventions (template first)
**BUG filename template**
- `BUG####_STATUS_three_word_description.md`
  - `STATUS` ∈ `Open | In_progress | Fixed | Verified | Dropped`

**ADR filename template**
- `ADR###_three_word_description.md`  (3-digit id)

**Slug rule**
- `three_word_description` is derived from the bug/ADR title (first ~3 meaningful words), snake_case.


## Files that change

### Legacy (`/docs/dev/`)
- `docs/dev/bugs/INDEX.md`
- `docs/dev/bugs/templates/BUG_REPORT_TEMPLATE.md`
- `docs/dev/bugs/reports/BUG-0001-global-options-not-global.md`
- `docs/dev/bugs/reports/BUG-0002-missing-run-options.md`
- `docs/dev/bugs/reports/BUG-0003-missing-cli-subcommands.md`
- `docs/dev/bugs/reports/BUG-0004-sqlite-connection-leak.md`
- `docs/dev/bugs/reports/BUG-0005-implicit-workspace-creation.md`
- `docs/dev/bugs/reports/BUG-0006.md`
- `docs/dev/decisions/INDEX.md`
- `docs/dev/decisions/templates/ADR_TEMPLATE.md`
- `docs/dev/decisions/ADR-0001-architecture-baseline.md`
- `docs/dev/decisions/ADR-0002-trace-versioning.md`
- `docs/dev/decisions/ADR-0003-manual-mode-gating.md`
- `docs/dev/decisions/ADR-0004-storage-baseline.md`
- `docs/dev/decisions/ADR-0005-orchestrator-threshold.md`

### Canonical (`/docs/dev/`)
- `docs/dev/bugs/INDEX_BUGS.md`
- `docs/dev/bugs/templates/BUG_REPORT_TEMPLATE.md`
- `docs/dev/bugs/reports/BUG0001_Fixed_global_options_not.md`
- `docs/dev/bugs/reports/BUG0002_Open_missing_run_options.md`
- `docs/dev/bugs/reports/BUG0003_Open_missing_cli_subcommands.md`
- `docs/dev/bugs/reports/BUG0004_Fixed_sqlite_connection_leak.md`
- `docs/dev/bugs/reports/BUG0005_Fixed_implicit_workspace_creation.md`
- `docs/dev/bugs/reports/BUG0006_Fixed_title_slug_tbd.md`
- `docs/dev/decisions/INDEX_DECISIONS.md`
- `docs/dev/decisions/templates/ADR_TEMPLATE.md`
- `docs/dev/decisions/files/ADR001_architecture_baseline_tbd.md`
- `docs/dev/decisions/files/ADR002_trace_versioning_tbd.md`
- `docs/dev/decisions/files/ADR003_manual_mode_gating.md`
- `docs/dev/decisions/files/ADR004_storage_baseline_tbd.md`
- `docs/dev/decisions/files/ADR005_orchestrator_threshold_tbd.md`

## Acceptance criteria (Definition of Done)
- [ ] All bug reports exist in `/docs/dev/bugs/reports/` using the new BUG filename template
- [ ] All ADR files exist in `/docs/dev/decisions/files/` using the new ADR filename template
- [ ] `INDEX_BUGS.md` and `INDEX_DECISIONS.md` exist and link to the canonical files
- [ ] Statuses are consistent across filename ↔ internal Metadata ↔ index table
- [ ] Legacy locations include clear deprecation pointers (or are removed only after sprint acceptance)

## Implementation notes
Keep bug/ADR IDs stable. Prefer docs-only PR. Update links from backlog/sprints/reviews if they reference old paths.

## Risks
Link rot (AFs or sprint docs referencing old paths); mitigate by running a repo-wide search for `docs/dev/bugs/` and `docs/dev/decisions/` and updating references.

## PR plan (PR-sized)
1. PR: Rename/move BUG reports + update BUG template + create/update INDEX_BUGS
2. PR: Rename/move ADR files + update ADR template + create/update INDEX_DECISIONS
