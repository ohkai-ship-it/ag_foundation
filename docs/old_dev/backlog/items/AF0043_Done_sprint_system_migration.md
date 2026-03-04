# AF0043 — Sprint system migration: per-sprint folders + merged templates + deprecate SPRINT_LOG
# Version number: v0.1

## Metadata
- **ID:** AF0043
- **Type:** Docs | Refactor
- **Status:** Done
- **Priority:** P0
- **Area:** Docs/Sprints
- **Owner:** Jacob
- **Target sprint:** Sprint04
- **Completion date:** 2026-03-03

## Problem
Sprint tracking is centralized in `SPRINT_LOG.md` and templates are split (plan vs report; tasks vs review). This makes per-sprint evidence hard to locate and causes redundant logs vs indexes.

## Goal
Introduce per-sprint documentation folders under `/docs/dev/sprints/documentation/`, merge sprint and review templates, and deprecate `SPRINT_LOG.md` in favor of `INDEX_SPRINTS.md` + per-sprint folders.

## Non-goals
No rewriting of historical sprint content beyond moving/archiving and adding pointers. No change to GitHub process itself (still 1 PR = 1 AF).

## Renaming / naming conventions (template first)
**Sprint folder template**
- `/docs/dev/sprints/documentation/Sprint##_three_word_description/`

**Sprint file templates**
- `S##_DESCRIPTION.md` (contains plan + completion report)
- `S##_REVIEW_##.md` (contains review tasks + review entry)
- `S##_PR_##.md` (PR pack / links / evidence pointers)

## Files that change

### Canonical (`/docs/dev/`)
- `docs/dev/sprints/documentation/Sprint04_process_hardening/S04_DESCRIPTION.md`
- `docs/dev/sprints/documentation/Sprint04_process_hardening/S04_REVIEW_01.md`
- `docs/dev/sprints/documentation/Sprint04_process_hardening/S04_PR_01.md`
- `docs/dev/sprints/documentation/Sprint04_process_hardening/artifacts/ (folder)`
- `docs/dev/sprints/INDEX_SPRINTS.md`
- `docs/dev/sprints/templates/SPRINT_DESCRIPTION_TEMPLATE.md`
- `docs/dev/sprints/templates/REVIEW_TEMPLATE.md`
- `docs/dev/sprints/templates/PULL_REQUEST_TEMPLATE.md (path stays; links updated)`

## Acceptance criteria (Definition of Done)
- [ ] `docs/dev/sprints/templates/SPRINT_DESCRIPTION_TEMPLATE.md` exists (plan + report combined)
- [ ] `docs/dev/sprints/templates/REVIEW_TEMPLATE.md` exists (tasks + entry combined)
- [ ] `docs/dev/sprints/INDEX_SPRINTS.md` exists and links to each sprint folder
- [ ] New sprint folder exists for Sprint04 and contains S04_DESCRIPTION / S04_REVIEW_01 / S04_PR_01


## Implementation notes
Copy legacy sprint docs to /docs/dev/sprints/documentation/old.

## Risks
Confusion during transition; mitigate by making Sprint04 the first sprint using the new model and keeping legacy docs read-only with pointers.

## PR plan (PR-sized)
1. PR: Add new sprint templates + INDEX_SPRINTS + Sprint04 folder structure
2. PR (optional/P2): Archive Sprint00–Sprint03 docs into per-sprint folders and add pointers
