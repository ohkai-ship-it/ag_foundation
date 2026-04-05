# INDEX_BACKLOG
# Version number: v1.3

> **FOUNDATION RULE**
> INDEX integrity is mandatory.
> Status must match between internal file metadata and INDEX row.
> Update required:
> - at sprint start ritual
> - whenever status changes
> See `/docs/dev/foundation/FOUNDATION_MANUAL.md` → Section 7: Index Discipline.

> **Location:** `/docs/dev/backlog/INDEX_BACKLOG.md`
> **Naming:** See SPRINT_MANUAL §2 for naming conventions (legacy and new).
> Status values: `PROPOSED | READY | BLOCKED | DONE | DROPPED`
> **Linking convention:** Link column is the sole file reference: `[🔗](items/filename)` or `[✅](items/filename)`

## Status legend
PROPOSED → READY → DONE (or BLOCKED / DROPPED)

---

## Backlog (unprioritized) *KEEP ALWAYS ON TOP*
| ID | Priority | Status | Title | Area | Owner | Link |
|---:|:--:|:--|---|---|---|---|
| AF-0007 | P2 | READY | Governance automation script (gov.py) | Process / Tooling | Jacob | [🔗](items/AF0007_READY_governance_automation_script.md) |
| AF-0009 | P1 | PROPOSED | Chat session gate: context refresh at session boundaries | Process / Governance | Jeff + Kai | [🔗](items/AF0009_PROPOSED_chat_session_gate.md) |
| AF-0012 | P0 | DONE | GVS convergent folder creation | Process / Governance | Kai | [✅](items/AF0012_DONE_gvs_convergent_folder_creation.md) |

---
## Sprints *IN DESCENDING ORDER*

### Sprint 01 Scope (governance_simplification)
| Order | ID | Priority | Status | Title | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF-0001 | P0 | DONE | Eliminate filename-status coupling | Process / Docs | Jacob | [✅](items/AF0001_DONE_eliminate_filename_status.md) |
| 2 | AF-0002 | P1 | DONE | Drop redundant sprint artifacts | Process / Docs | Jacob | [✅](items/AF0002_DONE_drop_sprint_artifacts.md) |
| 3 | AF-0003 | P1 | DONE | Template enhancements: time, model, docs impact | Process / Docs | Jacob | [✅](items/AF0003_DONE_template_enhancements.md) |
| 4 | AF-0004 | P1 | DONE | HITL framework in governance docs | Process / Governance | Jacob | [✅](items/AF0004_DONE_hitl_framework_docs.md) |
| 5 | AF-0005 | P1 | DONE | Copilot instructions: ToDo discipline | Process / Tooling | Jacob | [✅](items/AF0005_DONE_copilot_todo_discipline.md) |
| 6 | AF-0006 | P1 | DONE | Streamline INDEX files | Process / Docs | Jacob | [✅](items/AF0006_DONE_streamline_index_files.md) |
| 7 | AF-0010 | P1 | DONE | v1.3 transition brief | Process / Docs | Jacob | [✅](items/AF0010_DONE_v1_3_transition_brief.md) |
| 8 | AF-0008 | P1 | DONE | Governance docs consolidation | Process / Docs | Jacob | [✅](items/AF0008_DONE_governance_docs_consolidation.md) |

### Pre-Sprint (standalone)
| ID | Priority | Status | Title | Area | Owner | Link |
|---:|:--:|:--|---|---|---|---|
| AF-0011 | P0 | READY | GVS folder structure seed | Process / Governance | Jacob | [🔗](items/AF0011_READY_gvs_folder_structure_seed.md) |
