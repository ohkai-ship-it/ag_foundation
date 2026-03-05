# ADR006 — workspace_folder_structure
# Version number: v0.2

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - Manual mode remains dev/test-only
> - Interfaces remain swappable
> - See "Guardrails / invariants" section below

> **File naming (required):** `ADR###_<three_word_description>.md`
> Status values: `Proposed | Accepted | Superseded | Deprecated`

---

## Metadata
- **ADR:** ADR006
- **Status:** Proposed
- **Date:** 2026-03-05
- **Owners:** Kai
- **Reviewers:** Kai, Jeff
- **Related backlog item(s):** AF0058
- **Related bug(s):** BUG0011 (workspace context in errors)
- **Related PR(s):** (pending)

---

## Context

The current workspace structure mixes concerns:
- User input files sit at the workspace root alongside system files
- Run traces and artifacts are spread across separate `runs/` and `artifacts/` directories
- Database (`db.sqlite`) location is not clearly defined relative to other components
- Artifact filenames include run_id prefix to avoid collisions

This creates problems:
1. **Unclear boundaries** — Users don't know which files are safe to edit
2. **Export difficulty** — No clean way to package a single run with all its data
3. **Cluttered workspace** — System outputs pollute the workspace root
4. **Verbose naming** — Long artifact filenames due to run_id prefixes

**Current structure:**
```
~/.ag/workspaces/dev01/
├── db.sqlite
├── CODING_GUIDELINES.md      # User input (at root!)
├── TESTING_GUIDELINES.md     # User input (at root!)
├── artifacts/
│   └── <run_id>/
│       └── <run_id>-<artifact_name>.json
└── runs/
    └── <run_id>.json
```

---

## Decision

Restructure workspaces to clearly separate:
1. **Inputs** — User-provided content that skills read
2. **Runs** — System-generated outputs, grouped by run_id
3. **Index** — Database for fast queries

**New structure:**
```
~/.ag/workspaces/dev01/
├── db.sqlite                 # Index layer (workspace root, unchanged)
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

**Key changes:**
| Aspect | Before | After |
|--------|--------|-------|
| User inputs | `<ws>/` (root) | `<ws>/inputs/` |
| Run trace | `<ws>/runs/<id>.json` | `<ws>/runs/<id>/trace.json` |
| Artifacts | `<ws>/artifacts/<id>/<id>-<name>` | `<ws>/runs/<id>/artifacts/<name>` |
| Database | `<ws>/db.sqlite` | `<ws>/db.sqlite` (unchanged) |

---

## Options considered

### Option A — Flat workspace with inputs/ subfolder (chosen)
Keep database at workspace root, add `inputs/` for user content, consolidate run outputs.

**Pros**
- Clear separation: inputs vs outputs vs index
- Each run is self-contained (trace + artifacts together)
- Simple artifact names (no run_id prefix needed)
- Easy to delete or export a single run
- Database stays accessible at workspace root

**Cons**
- Skills need to be updated to read from `inputs/`
- (v0.x: no migration concern — start clean)

### Option B — Fully nested structure
Put database inside a `system/` folder.

```
~/.ag/workspaces/dev01/
├── system/
│   └── db.sqlite
├── inputs/
└── runs/
```

**Pros**
- Even cleaner separation

**Cons**
- Database path becomes longer
- More nesting than necessary
- No real benefit over Option A

### Option C — Keep current structure, add inputs/ only
Add `inputs/` but keep `runs/` and `artifacts/` separate.

**Pros**
- Smaller change
- Less migration work

**Cons**
- Doesn't solve run export problem
- Still have verbose artifact naming
- Artifacts disconnected from traces

---

## Consequences

**Easier:**
- Understanding workspace contents (clear input/output boundary)
- Exporting a run (just zip `runs/<id>/`)
- Cleaning up old runs (delete folder, not scattered files)
- Artifact naming (no run_id prefix)

**Harder:**
- Skills hardcoded to workspace root need updates

**Not a concern (v0.x):**
- Migration — workspaces can be deleted and recreated clean

**Follow-up work:**
- Update `Workspace` class with `inputs_path` property
- Update `RunStore` and `ArtifactStore` path logic
- Update `strategic_brief` skill to read from `inputs/`
- Update tests with new paths
- Document new structure in ARCHITECTURE.md

---

## Guardrails / invariants

1. **Workspace isolation** — Each workspace remains completely independent
2. **Truthful UX** — Trace content unchanged, only file paths change
3. **Run integrity** — A run's trace and artifacts stay together
4. **Input preservation** — User files in `inputs/` are never modified by the system
5. **Database stability** — SQLite schema unchanged; only file location semantics change

---

## Implementation notes

### Workspace class changes
```python
class Workspace:
    @property
    def inputs_path(self) -> Path:
        return self.path / "inputs"
    
    @property  
    def runs_path(self) -> Path:
        return self.path / "runs"
    
    def ensure_exists(self) -> None:
        self.path.mkdir(parents=True, exist_ok=True)
        self.inputs_path.mkdir(exist_ok=True)
        self.runs_path.mkdir(exist_ok=True)
```

### Path changes summary
```python
# Trace path
# Before: runs/<run_id>.json
# After:  runs/<run_id>/trace.json

# Artifact path
# Before: artifacts/<run_id>/<run_id>-<name>.json
# After:  runs/<run_id>/artifacts/<name>.json

# Input path (for skills)
# Before: workspace.path / "file.md"
# After:  workspace.inputs_path / "file.md"
```

### Migration (v0.x)
No migration needed. Existing workspaces can be deleted and recreated with the new structure. This is acceptable for v0.x as:
- No production data exists
- Workspaces are development/test environments
- Users can start clean anytime with `ag ws create <name>`

---

## Links
- ARCHITECTURE.md section: Workspace and Storage (to be updated)
- CLI_REFERENCE.md section: `ag ws create` (path examples)
- AF0058: Implementation backlog item
