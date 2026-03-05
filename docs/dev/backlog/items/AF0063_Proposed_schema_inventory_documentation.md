# BACKLOG ITEM — AF0063 — schema_inventory_documentation
# Version number: v0.2

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

> **File naming (required):** `AF0063_Proposed_schema_inventory_documentation.md`
> Status values: `Proposed | Ready | In progress | Blocked | Done | Dropped`

---

## Metadata
- **ID:** AF0063
- **Type:** Docs
- **Status:** Proposed
- **Priority:** P2
- **Area:** Docs / Core
- **Owner:** Kai
- **Target sprint:** TBD

---

## Problem
We have 19 Pydantic models across 5 modules but no centralized inventory or documentation of our schema landscape. As we evolve schemas (AF0062 extends RunTrace, AF0060 adds skill definitions), we risk:
- Drift between docs and implementation
- Uncoordinated schema changes
- No visibility into versioning strategy
- Unclear dependencies between schemas

Current schema distribution (undocumented):
- `task_spec.py`: TaskSpec, Budgets, Constraints
- `run_trace.py`: RunTrace, Step, Artifact, Subtask, EvidenceRef, PlaybookMetadata, Verifier
- `playbook.py`: Playbook, PlaybookStep
- `schema_verifier.py`: ValidationAttempt, ValidationResult
- `strategic_brief.py`: StrategicBrief, BriefSection, SourceFile, SourceExcerpt, Citation

---

## Goal
Create and maintain a schema inventory that:
1. Lists all Pydantic models with their module, purpose, and version
2. Documents dependencies between schemas (e.g., RunTrace contains Step, Artifact)
3. Tracks which AFs will modify which schemas
4. Provides guidance on schema evolution (additive changes, versioning)

---

## Non-goals
- Redesigning existing schemas
- Implementing schema versioning (separate AF)
- Auto-generating docs from code (future enhancement)

---

## Acceptance criteria (Definition of Done)
- [ ] `ARCHITECTURE.md` updated with schema inventory section
- [ ] Each schema has: name, module path, purpose (1 line), version info
- [ ] Dependency graph documented (which models contain/reference others)
- [ ] Schema evolution guidelines added (additive-only for 0.x, versioning strategy)
- [ ] Cross-reference to relevant AFs (AF0062, AF0060) added
- [ ] INDEX file updated

---

## Implementation notes

### Proposed structure (in ARCHITECTURE.md or separate SCHEMAS.md)

```markdown
## Schema Inventory

### Core Schemas (src/ag/core/)

| Model | Module | Purpose | Version |
|-------|--------|---------|---------|
| TaskSpec | task_spec.py | Input contract for agent runs | 0.1 |
| Budgets | task_spec.py | Resource limits (tokens, time, cost) | 0.1 |
| Constraints | task_spec.py | Run constraints (network, fs, output) | 0.1 |
| RunTrace | run_trace.py | Complete execution record | 0.1 |
| Step | run_trace.py | Single reasoning/action step | 0.1 |
| Artifact | run_trace.py | Output file metadata | 0.1 |
| ... | ... | ... | ... |

### Dependency Graph
- RunTrace → contains → [Step[], Artifact[], PlaybookMetadata, Verifier]
- Step → contains → [Subtask[], EvidenceRef[]]
- Playbook → contains → [PlaybookStep[]]

### Evolution Guidelines
- 0.x: Additive changes only (new optional fields)
- Breaking changes: Bump version, provide migration notes
- Deprecation: Mark field, keep for 2 sprints, then remove
```

### Design questions
1. **Location:** Section in ARCHITECTURE.md vs separate SCHEMAS.md?
2. **Auto-generation:** Should we add a script to extract schema info from code?
3. **Versioning:** Per-schema versions or single schema_version for all?

---

## Risks
- Low: Documentation-only change
- Maintenance burden: Must update when schemas change

### Mitigation
- Add checklist item to AF template: "Schema inventory updated if applicable"
- Consider automation later

---

## Related items
- **AF0062:** Will extend RunTrace (add LLM execution tracking)
- **AF0060:** Will add new skill definition schemas
- **ADR002 (future):** Trace versioning strategy

---

## Documentation impact
- **ARCHITECTURE.md:** New schema inventory section
- **BACKLOG_ITEM_TEMPLATE:** Consider adding schema-update checklist item
