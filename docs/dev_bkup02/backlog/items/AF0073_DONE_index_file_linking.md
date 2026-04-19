# BACKLOG ITEM — AF0073 — index_file_linking
# Version number: v0.2

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Index integrity
> - Documentation accessibility

> **File naming (required):** `AF####_<Status>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0073
- **Type:** Documentation / Process
- **Status:** DONE
- **Priority:** P2
- **Area:** Docs/Process
- **Owner:** Jacob
- **Target sprint:** Sprint 08
- **Depends on:** None

---

## Problem

Index files (INDEX_BACKLOG.md, INDEX_BUGS.md, INDEX_DECISIONS.md, INDEX_SPRINTS.md) list items with IDs and filenames, but navigating from the index to individual item files requires manual navigation through the file system.

**Current state:**
- ID column shows plain text like `AF-0069`
- Filename column shows path like `(items/AF0069_PROPOSED_skills_registry_deep_dive.md)`
- No direct clickable links to open item files

**Desired state:**
- Filename colummn contains: [🔗](items/AF0074_PROPOSED_research_v0_playbook.md)

Rational here is to keep each row as short as possible for better viewability while providing a direct link

---

## Scope

### In scope
1. Update INDEX_BACKLOG.md filename column to use clickable links
2. Update INDEX_BUGS.md filename column to use clickable links  
3. Update INDEX_DECISIONS.md filename column to use clickable links
4. Document the linking convention in FOUNDATION_MANUAL.md or templates

### Out of scope
- Automated link validation
- Bidirectional linking (item → index)

---

## Implementation

### Link format
Change from:
```markdown
| AF-0069 | ... | (items/AF0069_PROPOSED_skills_registry_deep_dive.md) |
```

To:
```markdown
| AF-0069 | ... | [AF0069_PROPOSED_skills_registry_deep_dive.md](items/AF0069_PROPOSED_skills_registry_deep_dive.md) |
```

### Files to update
- `/docs/dev/backlog/INDEX_BACKLOG.md`
- `/docs/dev/bugs/INDEX_BUGS.md`
- `/docs/dev/decisions/INDEX_DECISIONS.md`
- `/docs/dev/backlog/templates/` (if applicable)
- `/docs/dev/bugs/templates/` (if applicable)
- `/docs/dev/decisions/templates/` (if applicable)

---

## Acceptance criteria
- [x] All index files use clickable links in filename column
- [x] Links work correctly in VS Code and GitHub markdown preview
- [x] Templates updated to show correct format for new entries (convention documented in index headers)
- [x] FOUNDATION_MANUAL.md section on Index Discipline updated (if needed)

---

## Notes
- This improves developer experience when navigating documentation
- Relative paths (`items/filename.md`) work from the index file location

---

# Completion section

## 1) Metadata
- **Backlog item (primary):** AF0073
- **PR:** sprint08/skills-playbooks-maturity
- **Author:** Jacob
- **Date:** 2026-03-09
- **Branch:** sprint08/skills-playbooks-maturity
- **Risk level:** P2
- **Runtime mode used for verification:** N/A (documentation only)

---

## 2) Acceptance criteria verification
- [x] All index files use clickable links in filename column
- [x] Links work correctly in VS Code and GitHub markdown preview
- [x] Linking convention documented in each index file header
- [x] FOUNDATION_MANUAL.md section 7.4 added for linking convention

---

## 3) What changed (file-level)
- `docs/dev/backlog/INDEX_BACKLOG.md` — All filename entries converted to clickable links, version bumped to v0.3
- `docs/dev/bugs/INDEX_BUGS.md` — All filename entries converted to clickable links, version bumped to v0.3
- `docs/dev/decisions/INDEX_DECISIONS.md` — All filename entries converted to clickable links, version bumped to v0.3
- `docs/dev/foundation/FOUNDATION_MANUAL.md` — Added section 7.4 documenting the linking convention

---

## 4) Architecture alignment
- **Layering:** Documentation/process change only, no code affected
- **Pattern:** Markdown relative links (`[text](path)`) work in VS Code, GitHub, and most markdown renderers
