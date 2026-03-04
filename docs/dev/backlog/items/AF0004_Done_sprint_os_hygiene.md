# AF0004 — Sprint OS hygiene: sprint log + docs/dev pointers + handoff rules
# Version number: v0.3

## Metadata
- **ID:** AF-0004
- **Type:** Docs
- **Status:** Done
- **Priority:** P0
- **Area:** Docs
- **Owner:** Jeff
- **Completed in:** Sprint 01
- **Completion date:** 2026-02-24

## Problem
Sprint 00 established cornerstone docs and templates, but Sprint 01 needs a low-overhead cadence. We must avoid per-sprint folder sprawl and standardize where Jacob stores outputs so PR review has a single place to look.

## Goal
Repo uses a single sprint log, docs/dev pointers are consistent, and Jacob's reports/output files are stored under `/docs/dev/backlog/completion/` and linked from PRs and completion notes.

## Non-goals
- Creating separate folders per sprint.
- Changing cornerstone doc content beyond link/path corrections.
- Implementing runtime behavior.

## Acceptance criteria (Definition of Done)
- [x] `/docs/dev/sprints/SPRINT_LOG.md` exists/updated with a Sprint 01 section linking targeted AF items and PRs.
- [x] `/docs/dev/backlog/completion/README.md` exists/updated: all completion notes land here; files must be linked from PR description and completion note.
- [x] Check all INDEX files and update where necessary, specially in prompts, decisions, backlog. Check the other doc files for the correct links
- [x] Docs/dev indexes/pointers link to canonical locations for backlog, decisions, reviews, and completion.
- [x] Operating docs do not reference per-sprint folders; any references are corrected.
- [x] A short completion note is added under `/docs/dev/backlog/completion/` describing what was standardized and verified (or a review entry if required by REVIEW_GUIDE).

## Implementation notes
- Docs-only.
- Minimal edits: patch pointers; don't reorganize unrelated files.
- Recommend completion filename convention: `YYYY-MM-DD_AF-XXXX_<slug>.md`.

## Risks
Low. Primary risk is conflicting pointers; mitigate by linking to canonical docs only.

## PR plan
1. PR (chore/docs-os): Add/update sprint log + completion README + docs/dev pointers (docs-only).

---
# Completion section (fill when done)

**Completion date:** 2026-02-24  
**Author:** Jacob (Junior Engineer)

**Summary:**
Established sprint tracking hygiene for ag_foundation: created central sprint log, standardized handoff location, and fixed all INDEX files and per-sprint folder references.

**What Was Done:**

1. **Created `/docs/dev/sprints/SPRINT_LOG.md`** — Central log file for all sprints. Each sprint gets a section (no per-sprint folders).

2. **Created `/docs/dev/handoff/README.md`** — Documented the canonical location for engineer outputs with file naming convention.

3. **Updated INDEX Files:**
   - `sprints/INDEX.md` — Removed per-sprint folder structure; now points to SPRINT_LOG.md
   - `sprints/PROCESS.md` — Updated to v0.2; removed folder creation steps
   - `decisions/INDEX.md` — Fixed content (was showing prompts content)
   - `backlog/INDEX.md` — Added Sprint 01 items
   - `cornerstone/INDEX.md` — Marked all cornerstone docs as v0.1 complete
   - `prompts/INDEX.md` — Added links to actual prompt files

4. **No Per-Sprint Folder References Remain** — Searched and verified that no operating docs still reference per-sprint folder creation.

**Files Modified:**
- Created: SPRINT_LOG.md, handoff/README.md, completion note
- Updated: Multiple INDEX files as listed above

**Verification:** All acceptance criteria verified via file inspection and grep search.
