# FOLDER STRUCTURE
#### Description: Canonical folder layout for governed repositories. Delegated by GS §DS01. Specifies where foundation documents, project files, INDEX files, sprint folders, and artifact files reside. Also defines status value taxonomy and naming rules within the hierarchy. Files outside canonical locations are governance violations.
#### Convergent: v1.3.2
#### governs: ag_foundation

## Folder Structure 
```
Convergent/
├── CHANGELOG.md
│
├── docs/
│   ├── additional/                        ← Agent-generated artifacts, diagrams, ad-hoc analysis (not INDEX-governed)
│   │
│   ├── INDEX_BACKLOG.md                   ← Backlog index
│   ├── INDEX_BUGS.md                      ← Bug index
│   ├── INDEX_DECISIONS.md                 ← Decision index
│   ├── INDEX_SPRINTS.md                   ← Sprint index
│   │
│   ├── files/
│   │   ├── backlog/
│   │   │   └── AF####_<desc>.md
│   │   ├── bugs/
│   │   │   └── BUG####_<desc>.md
│   │   ├── decisions/
│   │   │   └── ADR###_<desc>.md
│   │   └── sprints/
│   │       └── S##/
│   │           ├── S##_DESCRIPTION.md     (planning artifact)
│   │           ├── S##_REVIEW.md          (outcomes artifact, written at sprint close)
│   │           ├── S##_PULL_REQUEST.md    (PR artifact, written at review)
│   │           └── artifacts/             (review outputs, traces, logs)
│   │
│   └── project/
│       ├── PROJECT_ROADMAP.md             ← User-facing project roadmap (GVS plan) <!-- generic name — use highest version on disk -->
│       ├── PROJECT_CONTROL.md             ← project specific invariants and rules <!-- generic name — use highest version on disk -->
│       └── prompts/                       ← Agent prompt templates
│
└── foundation/
    ├── GOVERNANCE_STANDARD.md             ← Canonical operating rules (lifecycle-organized)
    ├── SPRINT_PLAYBOOK.md                 ← Deterministic sprint execution script
    ├── templates/                         ← All artifact templates (centralized)
    │   ├── BACKLOG_ITEM_TEMPLATE.md
    │   ├── BUG_REPORT_TEMPLATE.md
    │   ├── ADR_TEMPLATE.md
    │   ├── SPRINT_DESCRIPTION_TEMPLATE.md
    │   ├── SPRINT_REVIEW_TEMPLATE.md
    │   ├── PULL_REQUEST_TEMPLATE.md
    │   ├── PROJECT_CONTROL_TEMPLATE.md
    │   ├── PROJECT_ROADMAP_TEMPLATE.md
    │   ├── INDEX_BACKLOG_TEMPLATE.md
    │   ├── INDEX_BUGS_TEMPLATE.md
    │   ├── INDEX_DECISIONS_TEMPLATE.md
    │   └── INDEX_SPRINTS_TEMPLATE.md
    └── sources/                           ← Surfaceable sources of truth
        ├── FOLDER_STRUCTURE.md            ← This file (current)
        ├── LIFECYCLE_REGISTRY.md          ← Phase/step/gate reference
        └── SESSION_CHAIN.md              ← Session continuity model
```

---

## Canonical Locations

> All paths are relative to the consumer project's governance root. Translate to your project's actual layout.

| Artifact Type | Location |
|---------------|----------|
| Backlog items | `docs/files/backlog/` |
| Backlog index | `docs/INDEX_BACKLOG.md` |
| Bug reports | `docs/files/bugs/` |
| Bug index | `docs/INDEX_BUGS.md` |
| ADRs | `docs/files/decisions/` |
| ADR index | `docs/INDEX_DECISIONS.md` |
| Sprint docs | `docs/files/sprints/S##/` |
| Sprint index | `docs/INDEX_SPRINTS.md` |
| Project docs | `docs/project/` |
| Ad-hoc artifacts | `docs/additional/` |
| Foundation docs | `foundation/` |
| Templates (all) | `foundation/templates/` |
| Sources of truth | `foundation/sources/` |

**INDEX Linking Convention:**

Filename columns in index files MUST use clickable markdown links:
- Format: `[🔗](subfolder/filename)` or `[✅](subfolder/filename)`
- Links must be relative to the index file location

---


## Naming Conventions

| Artifact | Filename convention |
|----------|--------------------|
| Backlog items | `AF####_<three_word_description>.md` |
| Bug reports | `BUG####_<three_word_description>.md` |
| ADRs | `ADR###_<three_word_description>.md` |
| Sprint folders | `S##/` |

**Status tracking:** Status lives in exactly **2 places**: internal file metadata + INDEX row. Status changes require exactly **2 edits**, zero renames.

> Historical files and entries are immutable. Do not retroactively rename, restructure, or normalize historical records.

---

## Branch Naming

- `feat/<short-name>` — new features
- `fix/<short-name>` — bug fixes
- `chore/<short-name>` — maintenance, docs, refactors

---

## File Creation Workflow

When creating new artifacts, follow these steps exactly:

| Step | AF | BUG | ADR |
|------|-----|-----|-----|
| 1. Copy template | `foundation/templates/BACKLOG_ITEM_TEMPLATE.md` | `foundation/templates/BUG_REPORT_TEMPLATE.md` | `foundation/templates/ADR_TEMPLATE.md` |
| 2. Save to | `docs/files/backlog/AF####_<desc>.md` | `docs/files/bugs/BUG####_<desc>.md` | `docs/files/decisions/ADR###_<desc>.md` |
| 3. Fill | All metadata fields (including `Status:`) | All metadata fields | All sections |
| 4. Update INDEX | `docs/INDEX_BACKLOG.md` | `docs/INDEX_BUGS.md` | `docs/INDEX_DECISIONS.md` |

**Folder Invariants:**
- Process docs canonical location: `foundation/`
- Templates canonical location: `foundation/templates/`
- Index files must exist at the top of the `docs/` folder
- No stray files outside canonical locations

---

## Sprint Folder Structure

Each sprint has one folder under `docs/files/sprints/` containing:
- `S##_DESCRIPTION.md` — planning artifact (scope, sequence, checklist)
- `S##_PULL_REQUEST.md` — PR artifact (work items, evidence, checklist)
- `S##_REVIEW.md` — outcomes artifact (review decision, cognitive health, learnings)
- `artifacts/` — review outputs, traces, logs

---

## References

- Sibling source: `foundation/sources/LIFECYCLE_REGISTRY.md`
- Sibling source: `foundation/sources/SESSION_CHAIN.md`
