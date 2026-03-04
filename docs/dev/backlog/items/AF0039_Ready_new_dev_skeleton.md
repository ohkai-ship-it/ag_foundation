# AF0039 — Create canonical /docs/new_dev skeleton + root doc moves + index renames
# Version number: v0.1

## Metadata
- **ID:** AF0039
- **Type:** Docs | Refactor
- **Status:** Done
- **Priority:** P0
- **Area:** Docs/Process
- **Owner:** Kai/Jeff
- **Target sprint:** Sprint04

## Problem
The repo’s process/docs are split across many folders and INDEX naming is inconsistent. Root-level contracts (ARCHITECTURE, CLI_REFERENCE) are not in canonical discoverable locations.

## Goal
Create the canonical `/docs/new_dev/` structure, move ARCHITECTURE + CLI_REFERENCE to repo root, and rename index files to the new naming scheme without breaking references.

## Non-goals
No deletion of `/docs/dev/` in this AF. No content rewrites beyond minimal deprecation pointers.

## Renaming / naming conventions (template first)
**Index files**
- `INDEX.md` → `INDEX_BACKLOG.md`, `INDEX_BUGS.md`, `INDEX_DECISIONS.md`, `INDEX_SPRINTS.md`
- No INDEX files in `/docs/new_dev/additional/**` and `/docs/new_dev/foundation/**`

**Root doc placement**
- `docs/dev/cornerstone/ARCHITECTURE.md` → `/ARCHITECTURE.md`
- `docs/dev/cornerstone/CLI_REFERENCE.md` → `/CLI_REFERENCE.md`


## Files that change

### Legacy (`/docs/dev/`)
- `docs/dev/cornerstone/ARCHITECTURE.md`
- `docs/dev/cornerstone/CLI_REFERENCE.md`
- `docs/dev/cornerstone/INDEX.md`
- `docs/dev/STRUCTURE.md`
- `docs/dev/backlog/INDEX.md`
- `docs/dev/bugs/INDEX.md`
- `docs/dev/decisions/INDEX.md`
- `docs/dev/sprints/INDEX.md`

### Canonical (`/docs/new_dev/`)
- `ARCHITECTURE.md  (moved to repo root)`
- `CLI_REFERENCE.md (moved to repo root)`
- `docs/new_dev/backlog/INDEX_BACKLOG.md`
- `docs/new_dev/bugs/INDEX_BUGS.md`
- `docs/new_dev/decisions/INDEX_DECISIONS.md`
- `docs/new_dev/sprints/INDEX_SPRINTS.md`
- `docs/new_dev/foundation/ (folder; canonical guidelines live here)`
- `docs/new_dev/sprints/documentation/Sprint04_process_hardening/S04_DESCRIPTION.md`

## Acceptance criteria (Definition of Done)
- [ ] `/docs/new_dev/` exists with target folder structure (matching STRUCTURE_TARGET)
- [ ] `/ARCHITECTURE.md` and `/CLI_REFERENCE.md` exist at repo root and contain the current canonical content
- [ ] Index files exist and are renamed: INDEX_BACKLOG, INDEX_BUGS, INDEX_DECISIONS, INDEX_SPRINTS
- [ ] Legacy files in `/docs/dev/` are updated only to add minimal pointers/deprecation notes (no mass edits)
- [ ] All moved/renamed docs build a consistent navigation path for Jacob (start at README → root docs → /docs/new_dev/foundation)

## Implementation notes
Create folders/files first (no deletions). Add deprecation stubs or one-line pointers in legacy locations where needed.

## Risks
Broken links and references; mitigate by adding explicit pointers in legacy files and by doing a quick grep-based link audit.

## PR plan (PR-sized)
1. PR1: Create `/docs/new_dev` folders + add empty INDEX_* placeholders + move ARCHITECTURE/CLI_REFERENCE to root
2. PR2 (optional): Add minimal deprecation notes/pointers in legacy docs/dev locations
