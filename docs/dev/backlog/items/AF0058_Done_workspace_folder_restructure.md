# BACKLOG ITEM — AF0058 — workspace_folder_restructure
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - 1 PR = 1 primary AF
> - INDEX update rule (status ↔ filename integrity)

> **File naming (required):** `AF####_<Status>_<three_word_description>.md`
> Status values: `Proposed | Ready | In progress | Blocked | Done | Dropped`

---

## Metadata
- **ID:** AF0058
- **Type:** Refactor
- **Status:** Done
- **Priority:** P0
- **Area:** Storage
- **Owner:** Jacob
- **Target sprint:** Sprint06
- **Related ADR(s):** ADR006 (workspace folder structure)

---

## Problem
Current workspace folder structure mixes user input files with system-generated
artifacts and run traces at the workspace root. This causes:

1. **Unclear boundaries** - User doesn't know which files are safe to edit
2. **Cluttered root** - Run artifacts pollute the workspace directory
3. **Hard to export** - No clean way to package a single run with all its data
4. **Artifact naming** - Long prefixed filenames to avoid collisions
5. **DB filename inconsistency** - Docs say `ag.db`, code uses `db.sqlite` (AF0015 absorbed)

**Current structure:**
```
dev01/
├── db.sqlite
├── CODING_GUIDELINES.md      # User input
├── TESTING_GUIDELINES.md     # User input
├── artifacts/
│   └── <run_id>/
│       └── <run_id>-<artifact_name>.json
└── runs/
    └── <run_id>.json
```

---

## Goal
Reorganize workspace folders to clearly separate user inputs from system outputs,
and make each run self-contained for easy export/deletion.

**Target structure:**
```
dev01/
├── db.sqlite                 # Index layer (workspace root)
├── inputs/                   # User content (read by skills)
│   ├── CODING_GUIDELINES.md
│   ├── TESTING_GUIDELINES.md
│   └── subdir/
│       └── nested_doc.md
└── runs/                     # System outputs (per-run folders)
    └── <run_id>/
        ├── trace.json        # Simplified name (run_id in folder)
        └── artifacts/
            ├── brief.md      # Simplified names (scoped by folder)
            └── result.json
```

---

## MANDATORY TESTING WORKFLOW

> **THIS MUST WORK FIRST BEFORE ANY OTHER SPRINT WORK**

AF0058 is a foundational change affecting storage, paths, and skill interfaces.
Strict verification is required before considering it complete:

1. **Run all tests** — `pytest -W error` must pass with 100% of existing tests green
2. **Stop the sprint** — Pause work and notify Kai for review
3. **Confirm with Kai** — Human approval required before proceeding
4. **Human testing** — Manual walkthrough of:
   - `ag ws create` creates correct folder structure
   - Files placed in `inputs/` are readable by skills
   - Run traces appear in `runs/<id>/trace.json`
   - Artifacts appear in `runs/<id>/artifacts/`
5. **Results documented** — Record test outcomes in completion section

**No exceptions.** If tests fail or human testing reveals issues, stop and fix before continuing the sprint.

---

## Non-goals
- Migration of existing workspaces (manual cleanup acceptable for v0.x)
- Changing the SQLite schema
- Changing the RunTrace JSON schema

---

## Acceptance criteria (Definition of Done)
- [x] `Workspace` class has `inputs_path` property returning `<ws>/inputs/`
- [x] `Workspace.ensure_exists()` creates both `inputs/` and `runs/` folders
- [x] `RunStore` saves traces to `runs/<run_id>/trace.json`
- [x] `ArtifactStore` saves to `runs/<run_id>/artifacts/<name>`
- [x] Artifact filenames no longer include run_id prefix
- [x] `strategic_brief` skill reads from `inputs/` folder
- [x] **DB filename unified** — single constant `DB_FILENAME` used everywhere (from AF0015)
- [x] **Docs updated** — ARCHITECTURE.md, CLI_REFERENCE.md use canonical DB filename
- [x] All existing tests pass with updated paths
- [x] New tests verify folder structure creation
- [x] `ag ws create` creates the new structure
- [x] `ruff check src tests` passes
- [x] `pytest -W error` passes (2 ResourceWarnings pre-existing, tracked by BUG-0007)
- [x] Coverage threshold maintained

---

## Implementation notes

### Files to modify:

| File | Changes |
|------|---------|
| `src/ag/storage/workspace.py` | Add `inputs_path`, `runs_path` properties; update `ensure_exists()` |
| `src/ag/storage/sqlite_store.py` | Update `SQLiteRunStore` path: `runs/<id>/trace.json` |
| `src/ag/storage/sqlite_store.py` | Update `SQLiteArtifactStore` path: `runs/<id>/artifacts/` |
| `src/ag/cli/main.py` | Update artifact naming (remove run_id prefix) |
| `src/ag/skills/strategic_brief.py` | Read from `workspace_path / "inputs"` |
| `tests/test_storage.py` | Update path expectations |
| `tests/test_cli.py` | Update artifact path checks |

### Key changes:

1. **Workspace class:**
   ```python
   @property
   def inputs_path(self) -> Path:
       return self._path / "inputs"
   
   @property
   def runs_path(self) -> Path:
       return self._path / "runs"
   ```

2. **Run trace path:**
   ```python
   # Before: runs/<run_id>.json
   # After:  runs/<run_id>/trace.json
   ```

3. **Artifact path:**
   ```python
   # Before: artifacts/<run_id>/<run_id>-<name>.json
   # After:  runs/<run_id>/artifacts/<name>.json
   ```

---

## Risks

| Risk | Mitigation |
|------|------------|
| Path changes break tests | Update tests incrementally, run after each component change |
| Skills hardcoded to workspace root | Abstract via `workspace.inputs_path` property |

**Note:** Migration is not a concern — v0.x workspaces can be deleted and recreated clean.

---

## Related
- BUG0011 (workspace name leak) — workspace context improvements
- AF0060 (Skill definition framework) — skills need workspace path abstraction
- **AF0015 (Dropped)** — DB filename consolidation (absorbed into this AF)

---

## Documentation impact
This change may require:
- **ADR:** If significant design decisions are made (e.g., migration strategy, path conventions)
- **ARCHITECTURE.md:** Update workspace/storage sections with new folder structure
- **CLI_REFERENCE.md:** Update any path references in command examples
- **README.md:** Update workspace setup instructions if changed

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF0058
- **PR:** N/A (direct commit to sprint branch)
- **Author:** Jacob
- **Date:** 2026-03-06
- **Branch:** sprint06/skill-foundation
- **Risk level:** P1
- **Runtime mode used for verification:** manual + pytest

---

## 2) Acceptance criteria verification
All criteria verified ✓ — see checklist above

Manual testing performed:
- `ag ws create test-ws` creates `inputs/` and `runs/` folders
- Files in `inputs/` readable by `strategic_brief` skill
- Run traces appear in `runs/<id>/trace.json`
- Artifacts appear in `runs/<id>/artifacts/`

---

## 3) What changed (file-level)

| File | Change |
|------|--------|
| `src/ag/storage/workspace.py` | Added `inputs_path`, `runs_path` properties; updated `ensure_exists()`; updated `run_path()` and `artifact_path()` for new structure |
| `src/ag/storage/sqlite_store.py` | Added run directory creation before saving trace |
| `src/ag/skills/strategic_brief.py` | Read from `inputs/` subfolder with fallback to root |
| `tests/test_storage.py` | Updated `test_ensure_exists_creates_structure` for new folders |
| `ARCHITECTURE.md` | Added workspace directory structure diagram (Section 3.6) |
| `CLI_REFERENCE.md` | Added workspace directory structure documentation |

---

## 4) Architecture alignment (mandatory)
- **Layering:** Storage layer change only; core and CLI adapt via Workspace abstraction
- **Workspace isolation:** Maintained - each workspace has isolated inputs/runs
- **Truthful UX:** Unchanged - trace paths updated but content identical
