# Handoff Note — AF-0004 — Sprint OS Hygiene
**Date:** 2026-02-24  
**Author:** Jacob (Junior Engineer)  
**Status:** Ready for review

---

## Summary
Established sprint tracking hygiene for ag_foundation: created central sprint log, standardized handoff location, and fixed all INDEX files and per-sprint folder references.

## What Was Done

### 1. Created `/docs/dev/sprints/SPRINT_LOG.md`
Central log file for all sprints. Each sprint gets a section (no per-sprint folders).
- Sprint 01 section with targeted items table
- Sprint 00 section documenting completed work
- Format documentation for future sprints

### 2. Created `/docs/dev/handoff/README.md`
Documented the canonical location for engineer outputs:
- File naming convention: `YYYY-MM-DD_AF-XXXX_<slug>.md`
- What goes here: handoff notes, captured traces
- How to link from PRs
- Current contents table

### 3. Updated INDEX Files

| File | Change |
|------|--------|
| `sprints/INDEX.md` | Removed per-sprint folder structure; now points to `SPRINT_LOG.md` |
| `sprints/PROCESS.md` | Updated to v0.2; removed folder creation steps; uses `SPRINT_LOG.md` |
| `decisions/INDEX.md` | **Fixed**: had wrong content (prompts content); now shows ADR list |
| `backlog/INDEX.md` | Added Sprint 01 items (AF-0004 through AF-0010); marked Sprint 00 as completed |
| `cornerstone/INDEX.md` | Marked all cornerstone docs as v0.1 complete |
| `prompts/INDEX.md` | Added links to actual prompt files (not just templates) |

### 4. No Per-Sprint Folder References Remain
Searched and verified that no operating docs still reference per-sprint folder creation.

---

## Files Modified

**Created:**
- `/docs/dev/sprints/SPRINT_LOG.md`
- `/docs/dev/handoff/README.md`
- `/docs/dev/handoff/2026-02-24_AF-0004_sprint-os-hygiene.md` (this file)

**Updated:**
- `/docs/dev/sprints/INDEX.md` — removed per-sprint folder structure
- `/docs/dev/sprints/PROCESS.md` — v0.2, uses SPRINT_LOG
- `/docs/dev/decisions/INDEX.md` — fixed content (was showing prompts content)
- `/docs/dev/backlog/INDEX.md` — added Sprint 01 items
- `/docs/dev/cornerstone/INDEX.md` — marked docs as complete
- `/docs/dev/prompts/INDEX.md` — added actual prompt file links

---

## Acceptance Criteria Checklist

| Criteria | Status | Evidence |
|----------|--------|----------|
| `/docs/dev/sprints/SPRINT_LOG.md` exists with Sprint 01 section | ✅ | [SPRINT_LOG.md](../../sprints/SPRINT_LOG.md) |
| `/docs/dev/handoff/README.md` exists with rules | ✅ | [README.md](README.md) |
| INDEX files updated (prompts, handoff, decisions, backlog) | ✅ | See files above |
| Docs/dev indexes link to canonical locations | ✅ | All INDEX files updated |
| No per-sprint folder references in operating docs | ✅ | grep search verified |
| Handoff note created | ✅ | This file |

---

## Verification Commands

```bash
# Verify no stale per-sprint folder references
grep -r "sprint-\d{4}" docs/dev/ --include="*.md" | grep -v "SPRINT-2026"

# Check INDEX files exist and are updated
ls docs/dev/*/INDEX.md

# Verify SPRINT_LOG exists
cat docs/dev/sprints/SPRINT_LOG.md
```

---

## Notes for Reviewers

1. **decisions/INDEX.md had wrong content** — It was showing the prompts INDEX content (copy-paste error from Sprint 00). Now fixed with proper ADR listing.

2. **PROCESS.md is now v0.2** — Significant changes to remove per-sprint folder workflow. Tests/CI unchanged (docs-only).

3. **Handoff README establishes convention** — All future Jacob outputs should follow the naming convention and be linked from PRs.

4. **No code changes** — This is a docs-only PR per AF-0004 scope.
