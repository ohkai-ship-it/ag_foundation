# BACKLOG ITEM — AF0141 — gvs_v1_3_export_clean
# Version number: v1.3
# Created: 2026-04-05
# Started: 2026-04-05
# Completed: 2026-04-05
# Status: DONE
# Priority: P0
# Area: Process / Governance
# Models: Claude Opus 4.6 (Copilot)

---

## Metadata
- **ID:** AF-0141
- **Type:** Process
- **Status:** DONE
- **Priority:** P0
- **Area:** Process / Governance
- **Owner:** Jacob
- **Target sprint:** GVS Sprint 1

---

## Goal

Create a clean GVS v1.3 export in `docs/export/` that contains only governance-system-relevant files, with all IDs renumbered to start from 1. This export becomes the content for `convergent/gvs_version_fixed/version1.3/`.

The export preserves the full `docs/dev/` folder structure but strips all ag_foundation runtime content (non-governance AFs, runtime bugs, runtime ADRs, runtime sprint docs).

## Scope

### What to export

**Foundation files (copy as-is):**
- `foundation/FOUNDATION_MANUAL.md`
- `foundation/SPRINT_MANUAL.md`
- `foundation/PROJECT_PLAN_0.1.md`
- `foundation/PROJECT_PLAN_0.2.md`
- `foundation/FOLDER_STRUCTURE_0.1.md`
- `foundation/FOLDER_STRUCTURE_0.2.md`
- `foundation/FOLDER_STRUCTURE_0.3.md`

**Templates (copy as-is):**
- `backlog/templates/BACKLOG_ITEM_TEMPLATE.md`
- `bugs/templates/BUG_REPORT_TEMPLATE.md`
- `decisions/templates/ADR_TEMPLATE.md`
- `sprints/templates/SPRINT_DESCRIPTION_TEMPLATE.md`
- `sprints/templates/SPRINT_REVIEW_TEMPLATE.md`
- `sprints/templates/PULL_REQUEST_TEMPLATE.md`
- `sprints/templates/archived/` (preserve directory)

**Additional docs (copy as-is):**
- `additional/GOVERNANCE_SIMPLIFICATION_PLAN_0.1.md`
- `additional/GVS_PROJECT_PLAN_0.1.md`
- `additional/S16_OBSERVATIONS_0.1.md`
- `additional/SPRINT_VELOCITY_ANALYSIS_0.1.md`
- `additional/SPRINT_VELOCITY_ANALYSIS_0.2.md`
- `additional/sprint_velocity_charts.html`

**AFs (copy + renumber):**

| Source (ag_foundation) | Export filename | GVS ID |
|---|---|---|
| `AF0129_DONE_eliminate_filename_status.md` | `AF0001_DONE_eliminate_filename_status.md` | AF-0001 |
| `AF0130_DONE_drop_sprint_artifacts.md` | `AF0002_DONE_drop_sprint_artifacts.md` | AF-0002 |
| `AF0131_DONE_template_enhancements.md` | `AF0003_DONE_template_enhancements.md` | AF-0003 |
| `AF0132_DONE_hitl_framework_docs.md` | `AF0004_DONE_hitl_framework_docs.md` | AF-0004 |
| `AF0133_DONE_copilot_todo_discipline.md` | `AF0005_DONE_copilot_todo_discipline.md` | AF-0005 |
| `AF0134_DONE_streamline_index_files.md` | `AF0006_DONE_streamline_index_files.md` | AF-0006 |
| `AF0135_READY_governance_automation_script.md` | `AF0007_READY_governance_automation_script.md` | AF-0007 |
| `AF0136_DONE_governance_docs_consolidation.md` | `AF0008_DONE_governance_docs_consolidation.md` | AF-0008 |
| `AF0137_PROPOSED_chat_session_gate.md` | `AF0009_PROPOSED_chat_session_gate.md` | AF-0009 |
| `AF0138_DONE_v1_3_transition_brief.md` | `AF0010_DONE_v1_3_transition_brief.md` | AF-0010 |
| `AF0139_READY_gvs_folder_structure_seed.md` | `AF0011_READY_gvs_folder_structure_seed.md` | AF-0011 |
| `AF0140_DONE_gvs_convergent_folder_creation.md` | `AF0012_DONE_gvs_convergent_folder_creation.md` | AF-0012 |

**Bugs (copy + renumber):**

| Source (ag_foundation) | Export filename | GVS ID |
|---|---|---|
| `BUG0025_leftover_ready_duplicates.md` | `BUG0001_leftover_ready_duplicates.md` | BUG-0001 |
| `BUG0026_pr_template_version_gap.md` | `BUG0002_pr_template_version_gap.md` | BUG-0002 |

**ADRs (copy + renumber):**

| Source (ag_foundation) | Export filename | GVS ID |
|---|---|---|
| `ADR010_governance_simplification.md` | `ADR001_governance_simplification.md` | ADR-0001 |

**Sprint docs (copy + renumber):**

| Source folder | Export folder |
|---|---|
| `Sprint16_governance_simplification/` | `Sprint01_governance_simplification/` |

All internal references in exported files (S16 → S01, AF-0129 → AF-0001, BUG-0025 → BUG-0001, ADR-0010 → ADR-0001, Sprint 16 → Sprint 1, etc.) must be updated.

**INDEX files (export with GVS-only rows, renumbered):**
- `backlog/INDEX_BACKLOG.md` — 12 AFs (AF-0001 through AF-0012), one sprint section (Sprint 01)
- `bugs/INDEX_BUGS.md` — 2 bugs (BUG-0001, BUG-0002)
- `decisions/INDEX_DECISIONS.md` — 1 ADR (ADR-0001)
- `sprints/INDEX_SPRINTS.md` — 1 sprint (Sprint 01)

### Renumbering Rules

1. All IDs restart from 1 (AF-0001, BUG-0001, ADR-0001, Sprint 01)
2. Filenames updated to match new IDs
3. Internal metadata headers updated (`# ID:`, `## Metadata` blocks)
4. Cross-references between files updated (e.g., "see AF-0138" → "see AF-0010" inside AF-0008)
5. INDEX table rows updated with new IDs, new filenames, new links
6. Sprint references updated (S16 → S01, Sprint 16 → Sprint 01)

### Renumbering Cross-Reference Map

```
AF-0129  →  AF-0001       BUG-0025  →  BUG-0001
AF-0130  →  AF-0002       BUG-0026  →  BUG-0002
AF-0131  →  AF-0003
AF-0132  →  AF-0004       ADR-0010  →  ADR-0001
AF-0133  →  AF-0005
AF-0134  →  AF-0006       Sprint 16 →  Sprint 01
AF-0135  →  AF-0007       S16       →  S01
AF-0136  →  AF-0008
AF-0137  →  AF-0009
AF-0138  →  AF-0010
AF-0139  →  AF-0011
AF-0140  →  AF-0012
```

## Non-Goals

- Do NOT modify any files in `docs/dev/` — this is a read-only export
- Do NOT include ag_foundation runtime AFs (AF-0001 through AF-0128)
- Do NOT include non-governance bugs (BUG-0001 through BUG-0024)
- Do NOT include non-governance ADRs (ADR-001 through ADR-009)
- Do NOT include Sprint 04–15 documentation
- Do NOT include ag_foundation-specific additional docs (SKILLS_ARCHITECTURE, LINKEDIN, SCHEMA_INVENTORY, CONTRACT_INVENTORY, ARCHITECTURAL_FINDINGS)
- Do NOT include playbooks/ or prompts/ from additional/

## Output Structure

```
docs/export/
├── additional/
│   ├── GOVERNANCE_SIMPLIFICATION_PLAN_0.1.md
│   ├── GVS_PROJECT_PLAN_0.1.md
│   ├── S16_OBSERVATIONS_0.1.md              (rename to S01_OBSERVATIONS_0.1.md)
│   ├── SPRINT_VELOCITY_ANALYSIS_0.1.md
│   ├── SPRINT_VELOCITY_ANALYSIS_0.2.md
│   └── sprint_velocity_charts.html
├── backlog/
│   ├── INDEX_BACKLOG.md                     (GVS-only, renumbered)
│   ├── items/
│   │   ├── AF0001_DONE_eliminate_filename_status.md
│   │   ├── AF0002_DONE_drop_sprint_artifacts.md
│   │   ├── ...
│   │   └── AF0012_DONE_gvs_convergent_folder_creation.md
│   └── templates/
│       └── BACKLOG_ITEM_TEMPLATE.md
├── bugs/
│   ├── INDEX_BUGS.md                        (GVS-only, renumbered)
│   ├── reports/
│   │   ├── BUG0001_leftover_ready_duplicates.md
│   │   └── BUG0002_pr_template_version_gap.md
│   └── templates/
│       └── BUG_REPORT_TEMPLATE.md
├── decisions/
│   ├── INDEX_DECISIONS.md                   (GVS-only, renumbered)
│   ├── files/
│   │   └── ADR001_governance_simplification.md
│   └── templates/
│       └── ADR_TEMPLATE.md
├── foundation/
│   ├── FOLDER_STRUCTURE_0.1.md
│   ├── FOLDER_STRUCTURE_0.2.md
│   ├── FOLDER_STRUCTURE_0.3.md
│   ├── FOUNDATION_MANUAL.md
│   ├── PROJECT_PLAN_0.1.md
│   ├── PROJECT_PLAN_0.2.md
│   └── SPRINT_MANUAL.md
└── sprints/
    ├── INDEX_SPRINTS.md                     (GVS-only, renumbered)
    ├── documentation/
    │   └── Sprint01_governance_simplification/
    │       ├── S01_DESCRIPTION.md
    │       ├── S01_PR_01.md
    │       ├── S01_REVIEW_01.md
    │       └── artifacts/
    │           └── review_S01_01/
    │               └── pass_evidence_summary.md
    └── templates/
        ├── archived/
        ├── PULL_REQUEST_TEMPLATE.md
        ├── SPRINT_DESCRIPTION_TEMPLATE.md
        └── SPRINT_REVIEW_TEMPLATE.md
```

## Acceptance Criteria

- [ ] `docs/export/` exists with complete folder structure matching `docs/dev/` layout
- [ ] All 12 AF files exported with correct GVS IDs (AF-0001 through AF-0012)
- [ ] All 2 BUG files exported with correct GVS IDs (BUG-0001, BUG-0002)
- [ ] ADR exported as ADR-0001
- [ ] Sprint 16 docs exported as Sprint 01 (folder name, file prefixes, internal refs)
- [ ] All 4 INDEX files contain only GVS rows with renumbered IDs and correct links
- [ ] All cross-references inside exported files updated per renumbering map
- [ ] All 6 template files present and unmodified
- [ ] All 7 foundation files present and unmodified
- [ ] No ag_foundation runtime content in export
- [ ] `docs/dev/` completely untouched
- [ ] Duplicate READY files from BUG-0025 NOT included (export DONE versions only)

## Dependencies

- AF-0140 (DONE) — folder structure exists
- Sprint 16 must be closed before export is finalized

## References

- `docs/dev/additional/GVS_PROJECT_PLAN_0.1.md` §4.3 (folder structure)
- `docs/dev/additional/GVS_PROJECT_PLAN_0.1.md` §3 (component inventory at v1.3)
