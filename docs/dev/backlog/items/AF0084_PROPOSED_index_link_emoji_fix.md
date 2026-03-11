# BACKLOG ITEM — AF0084 — index_link_emoji_fix
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - INDEX integrity
> - Documentation consistency

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0084
- **Type:** Docs / Process
- **Status:** PROPOSED
- **Priority:** P3
- **Area:** Docs/Process
- **Owner:** TBD
- **Target sprint:** TBD
- **Depends on:** None

---

## Problem

INDEX_BUGS.md and INDEX_DECISIONS.md are missing the 🔗 emoji in their file links.

### Current State (Incorrect)

**INDEX_BUGS.md:**
```markdown
| BUG-0012 | P2 | OPEN | ... | [](reports/BUG0012_OPEN_test_workspace_cleanup.md) |
```

**INDEX_DECISIONS.md:**
```markdown
| ADR-0001 | ACCEPTED | ... | [](files/ADR001_ACCEPTED_architecture_baseline.md) |
```

### Expected State (Per AF-0073)

**INDEX_BUGS.md:**
```markdown
| BUG-0012 | P2 | OPEN | ... | [🔗](reports/BUG0012_OPEN_test_workspace_cleanup.md) |
```

**INDEX_DECISIONS.md:**
```markdown
| ADR-0001 | ACCEPTED | ... | [🔗](files/ADR001_ACCEPTED_architecture_baseline.md) |
```

### Reference (Correct)

**INDEX_BACKLOG.md** (correct format):
```markdown
| AF-0083 | P1 | PROPOSED | ... | [🔗](items/AF0083_PROPOSED_artifact_evidence_strategy.md) |
```

---

## Goal

1. Add 🔗 emoji to all file links in INDEX_BUGS.md
2. Add 🔗 emoji to all file links in INDEX_DECISIONS.md
3. Update templates/documentation to ensure consistency

---

## Non-goals

- Changing link targets
- Restructuring index files

---

## Acceptance criteria (Definition of Done)

- [ ] INDEX_BUGS.md: All filename links use `[🔗](reports/...)` format
- [ ] INDEX_DECISIONS.md: All filename links use `[🔗](files/...)` format
- [ ] Templates updated (if linking convention documented there)
- [ ] FOUNDATION_MANUAL.md linking convention section (if exists) updated

---

## Implementation Notes

### Files to Update

1. `/docs/dev/bugs/INDEX_BUGS.md`
   - OPEN bugs section: 5 links
   - FIXED bugs section: 8 links

2. `/docs/dev/decisions/INDEX_DECISIONS.md`
   - Current ADRs section: 7 links

3. Check templates:
   - `/docs/dev/bugs/templates/BUG_REPORT_TEMPLATE.md` (if references linking)
   - `/docs/dev/decisions/templates/ADR_TEMPLATE.md` (if references linking)

### Pattern

Replace all occurrences of:
```
[](reports/BUG...
[](files/ADR...
```

With:
```
[🔗](reports/BUG...
[🔗](files/ADR...
```

---

## Risks

None — cosmetic fix only.

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF0084
- **PR:** #<number>
- **Author:** <name>
- **Date:** YYYY-MM-DD
- **Branch:** chore/index-link-emoji
- **Risk level:** P3
- **Runtime mode used for verification:** manual
