# AF0044 — Review artifact migration: move future reviews into sprint folders; archive legacy /docs/dev/reviews
# Version number: v0.1

## Metadata
- **ID:** AF0044
- **Type:** Docs | Refactor
- **Status:** Done
- **Priority:** P1
- **Area:** Docs/Reviews
- **Owner:** Jacob
- **Target sprint:** Sprint04

## Problem
Reviews and their evidence bundles live under `/docs/dev/reviews/entries/` and separate subfolders, which is disconnected from sprint context and increases folder sprawl.

## Goal
Define and implement the new canonical review location inside each sprint folder (`S##_REVIEW_##.md` + `artifacts/` evidence), while archiving legacy reviews under `/docs/dev/reviews` (read-only) with pointers.

## Non-goals
No retroactive rewriting of historical review entries. No requirement to rename old review artifacts.

## Renaming / naming conventions (template first)
N/A (no renames required; location and convention change only).

## Files that change

### Legacy (`/docs/dev/`)
- `docs/dev/reviews/INDEX.md`
- `docs/dev/reviews/entries/2026-02-23-kickoff.md`
- `docs/dev/reviews/entries/REVIEW_S01_2026-02-24.md`
- `docs/dev/reviews/entries/REVIEW_S02_2026-02-26.md`
- `docs/dev/reviews/entries/REVIEW_S02_2026-02-26_SIGNOFF_FINDINGS.md`
- `docs/dev/reviews/entries/REVIEW_TASKS_SPRINT01.md`
- `docs/dev/reviews/entries/REVIEW_S01_2026-02-24/artifacts_outputs.txt`
- `docs/dev/reviews/entries/REVIEW_S01_2026-02-24/bug_triage.md`
- `docs/dev/reviews/entries/REVIEW_S01_2026-02-24/cli_outputs.txt`
- `docs/dev/reviews/entries/REVIEW_S01_2026-02-24/contracts_notes.md`
- `docs/dev/reviews/entries/REVIEW_S01_2026-02-24/CONTRACT_INVENTORY.md`
- `docs/dev/reviews/entries/REVIEW_S01_2026-02-24/env.txt`
- `docs/dev/reviews/entries/REVIEW_S01_2026-02-24/failure_trace.json`
- `docs/dev/reviews/entries/REVIEW_S01_2026-02-24/FUTURE_CONTRACTS.md`
- `docs/dev/reviews/entries/REVIEW_S01_2026-02-24/happy_trace.json`
- `docs/dev/reviews/entries/REVIEW_S01_2026-02-24/pytest_summary.txt`
- `docs/dev/reviews/entries/REVIEW_S01_2026-02-24/scope_links.md`
- `docs/dev/reviews/entries/REVIEW_S01_2026-02-24/storage_isolation_transcript.txt`
- `docs/dev/reviews/entries/REVIEW_S01_2026-02-24/TEST_INVENTORY.md`
- `docs/dev/reviews/entries/REVIEW_S02_2026-02-26/sprint02_cli_global.txt`
- `docs/dev/reviews/entries/REVIEW_S02_2026-02-26/sprint02_coverage.txt`
- `docs/dev/reviews/entries/REVIEW_S02_2026-02-26/sprint02_delegation.txt`
- `docs/dev/reviews/entries/REVIEW_S02_2026-02-26/sprint02_e2e_delegation.txt`
- `docs/dev/reviews/entries/REVIEW_S02_2026-02-26/sprint02_integration.txt`
- `docs/dev/reviews/entries/REVIEW_S02_2026-02-26/sprint02_providers.txt`
- `docs/dev/reviews/entries/REVIEW_S02_2026-02-26/sprint02_repl_a10.txt`
- `docs/dev/reviews/entries/REVIEW_S02_2026-02-26/sprint02_repl_a8.txt`
- `docs/dev/reviews/entries/REVIEW_S02_2026-02-26/sprint02_repl_a9.txt`
- `docs/dev/reviews/entries/REVIEW_S02_2026-02-26/sprint02_schemas.txt`
- `docs/dev/reviews/entries/REVIEW_S02_2026-02-26/sprint02_test_full.txt`
- `docs/dev/reviews/entries/REVIEW_S03_2026-02-27/REVIEW_S03_FINDINGS.md`
- `docs/dev/reviews/entries/REVIEW_S03_2026-02-27/REVIEW_S03_PLAN.md`
- `docs/dev/reviews/templates/REVIEW_TASKS_TEMPLATE.md`
- `docs/dev/reviews/templates/REVIEW_TEMPLATE.md`

### Canonical (`/docs/new_dev/`)
- `docs/new_dev/sprints/templates/REVIEW_TEMPLATE.md (canonical)`
- `docs/new_dev/sprints/documentation/Sprint04_process_hardening/S04_REVIEW_01.md (first use)`
- `docs/new_dev/sprints/documentation/Sprint04_process_hardening/artifacts/review_evidence/ (folder; canonical evidence location)`
- `docs/new_dev/sprints/INDEX_SPRINTS.md (links to review files)`

## Acceptance criteria (Definition of Done)
- [ ] Canonical review template exists in `/docs/new_dev/sprints/templates/REVIEW_TEMPLATE.md` and is used for Sprint04 review
- [x] New convention documented: review file + evidence live under the sprint folder
- [ ] Legacy `/docs/dev/reviews` is marked archived/read-only and points reviewers to the sprint-folder model
- [ ] No sprint depends on creating new files under `/docs/dev/reviews` going forward

## Implementation notes
Keep legacy reviews for historical traceability. The only required change is: stop creating new review entries there.

## Risks
Losing discoverability of review history; mitigate by ensuring INDEX_SPRINTS links each sprint’s review files and by keeping legacy reviews indexed/accessible.

## PR plan (PR-sized)
1. PR: Add combined REVIEW_TEMPLATE to `/docs/new_dev/sprints/templates/` and document the new location convention
2. PR: Add archive note/pointer to `/docs/dev/reviews/INDEX.md` (legacy) referencing the new sprint folder approach
