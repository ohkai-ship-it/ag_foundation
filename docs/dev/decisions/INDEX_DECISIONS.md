# INDEX_DECISIONS
# Version number: v0.2

> **FOUNDATION RULE**
> INDEX integrity is mandatory.
> Filename status must match internal status.
> Update required:
> - at sprint start ritual
> - whenever status changes
> See `/docs/dev/foundation/FOUNDATION_MANUAL.md` → Section 7: Index Discipline.

> **Location:** `/docs/dev/decisions/INDEX_DECISIONS.md`
> **Naming (required):** `ADR###_<three_word_description>.md` in `/docs/dev/decisions/files/`

---

## Current ADRs
| ID | Status | Title | Filename |
|---:|:--:|---|---|
| ADR-0001 | Accepted | Architecture baseline | `ADR001_architecture_baseline.md` |
| ADR-0002 | Accepted | Trace versioning strategy | `ADR002_trace_versioning_strategy.md` |
| ADR-0003 | Accepted | Manual mode gating | `ADR003_manual_mode_gating.md` |
| ADR-0004 | Accepted | Storage baseline | `ADR004_storage_baseline.md` |
| ADR-0005 | Accepted | Orchestrator threshold | `ADR005_orchestrator_threshold.md` |
| ADR-0006 | Proposed | Workspace folder structure | `ADR006_workspace_folder_structure.md` |
| ADR-0007 | Proposed | Configuration state separation | `ADR007_configuration_state_separation.md` |

---

## How to use
1. Create ADR from `/docs/dev/decisions/templates/ADR_TEMPLATE.md`
2. Link ADR from the relevant AF item + PR
3. Update status: Proposed → Accepted → Superseded/Deprecated
