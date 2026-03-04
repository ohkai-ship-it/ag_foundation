# AF0040 — Consolidate WORKFLOW + PROCESS into canonical foundation docs
# Version number: v0.1

## Metadata
- **ID:** AF0040
- **Type:** Docs | Refactor
- **Status:** Done
- **Priority:** P1
- **Area:** Docs/Process
- **Owner:** Jeff
- **Target sprint:** Sprint04

## Problem
Process guidance is duplicated/fragmented across `/docs/dev/backlog/WORKFLOW.md`, `/docs/dev/sprints/PROCESS.md`, and other guideline documents, causing drift and inconsistent behavior.

## Goal
Merge WORKFLOW + PROCESS guidance into a single canonical `docs/new_dev/foundation/WORKFLOW.md` (and adjust related foundation docs) while leaving clear deprecation pointers in legacy locations.

## Non-goals
No changes to core runtime behavior. No template redesign beyond link/path updates needed due to new structure.

## Renaming / naming conventions (template first)
N/A (no renames; content consolidation only).

## Files that change

### Legacy (`/docs/dev/`)
- `docs/dev/backlog/WORKFLOW.md`
- `docs/dev/sprints/PROCESS.md`
- `docs/dev/sprints/SPRINT_LOG.md`
- `docs/dev/team/COLLABORATION_MANIFEST.md`
- `docs/dev/engineering/PR_CHECKLIST.md`

### Canonical (`/docs/new_dev/`)
- `docs/new_dev/foundation/WORKFLOW.md`
- `docs/new_dev/foundation/COLLABORATION_MANIFEST.md`
- `docs/new_dev/foundation/PR_CHECKLIST.md`
- `docs/new_dev/sprints/templates/ (references updated)`

## Acceptance criteria (Definition of Done)
- [ ] `docs/new_dev/foundation/WORKFLOW.md` contains the canonical sprint lifecycle + backlog/PR mapping rules (no contradictions)
- [ ] Legacy docs (`/docs/dev/backlog/WORKFLOW.md`, `/docs/dev/sprints/PROCESS.md`) clearly point to the new canonical WORKFLOW doc
- [ ] Any references in PR_CHECKLIST / COLLABORATION_MANIFEST are updated to point to canonical locations
- [ ] SPRINT_LOG is explicitly marked deprecated (canonical sprint tracking is per-sprint folder)

## Implementation notes
Treat this as docs refactor: consolidate content, then add deprecation stubs. Keep wording surgical and avoid adding new policies not agreed in chat.

## Risks
Accidental policy changes; mitigate by copying existing text first, then making only minimal edits required for consistency.

## PR plan (PR-sized)
1. PR: Consolidate docs into `/docs/new_dev/foundation/WORKFLOW.md` + update pointers in legacy docs
