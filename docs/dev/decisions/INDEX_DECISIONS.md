# INDEX_DECISIONS
# Version number: v0.4

> **FOUNDATION RULE**
> INDEX integrity is mandatory.
> Filename status must match internal status.
> Update required:
> - at sprint start ritual
> - whenever status changes
> See `/docs/dev/foundation/FOUNDATION_MANUAL.md` → Section 7: Index Discipline.

> **Location:** `/docs/dev/decisions/INDEX_DECISIONS.md`
> **Naming (required):** `ADR###_<STATUS>_<three_word_description>.md` in `/docs/dev/decisions/files/`
> **Linking convention:** Filename column uses clickable links: `[🔗](files/filename)`

---

## Current ADRs
| ID | Status | Title | Filename |
|---:|:--:|---|---|
| ADR-0001 | ACCEPTED | Architecture baseline | [🔗](files/ADR001_ACCEPTED_architecture_baseline.md) |
| ADR-0002 | ACCEPTED | Trace versioning strategy | [🔗](files/ADR002_ACCEPTED_trace_versioning_strategy.md) |
| ADR-0003 | ACCEPTED | Manual mode gating | [🔗](files/ADR003_ACCEPTED_manual_mode_gating.md) |
| ADR-0004 | ACCEPTED | Storage baseline | [🔗](files/ADR004_ACCEPTED_storage_baseline.md) |
| ADR-0005 | ACCEPTED | Orchestrator threshold | [🔗](files/ADR005_ACCEPTED_orchestrator_threshold.md) |
| ADR-0006 | PROPOSED | Workspace folder structure | [🔗](files/ADR006_PROPOSED_workspace_folder_structure.md) |
| ADR-0007 | PROPOSED | Configuration state separation | [🔗](files/ADR007_PROPOSED_configuration_state_separation.md) |
| ADR-0008 | ACCEPTED | CLI global flags | [🔗](files/ADR008_ACCEPTED_cli_global_flags.md) |

---

## How to use
1. Create ADR from `/docs/dev/decisions/templates/ADR_TEMPLATE.md`
2. Link ADR from the relevant AF item + PR
3. Update status: PROPOSED → ACCEPTED → SUPERSEDED/DEPRECATED

