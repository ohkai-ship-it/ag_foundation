# BACKLOG ITEM — AF0081 — inventory_sync_discipline
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Documentation accuracy
> - Schema/Contract traceability
> - INDEX update rule (status ↔ filename integrity)

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0081
- **Type:** Process / Docs
- **Status:** PROPOSED
- **Priority:** P2
- **Area:** Docs/Process
- **Owner:** TBD
- **Target sprint:** TBD
- **Depends on:** None

---

## Problem

During Sprint 08 closure verification, documentation drift was discovered between the codebase and inventory documents:

### SCHEMA_INVENTORY.md gaps
Missing schemas added in Sprint 08:
- `WebSearchInput` (web_search.py)
- `WebSearchOutput` (web_search.py)
- `SearchResult` (web_search.py)
- Updated `EmitResultInput` aliased fields for schema bridging

### CONTRACT_INVENTORY.md gaps
Skills implementations list missing:
- `fetch_web_content.py`
- `synthesize_research.py`
- `web_search.py`
- `stubs.py` (test utilities)

**Root cause:** No enforcement mechanism exists to ensure inventory documents stay synchronized when new skills/schemas are added.

---

## Goal

1. Update SCHEMA_INVENTORY.md with missing schemas
2. Update CONTRACT_INVENTORY.md with missing implementations
3. **Establish enforcement discipline** to prevent future drift

---

## Non-goals

- Automated code generation from docs
- Full schema documentation (just registry entries)

---

## Acceptance criteria (Definition of Done)

- [ ] SCHEMA_INVENTORY.md updated with all current schemas
- [ ] CONTRACT_INVENTORY.md updated with all current implementations
- [ ] Enforcement discipline documented (see Implementation Notes)
- [ ] INDEX_BACKLOG.md updated
- [ ] CI/local checks pass

---

## Implementation notes

### 1. Schema/Contract Inventory Updates

Update both inventory documents to reflect current state:
- Run `ag skills list` and `ag playbooks list` to verify completeness
- Cross-reference with `src/ag/skills/*.py` and `src/ag/playbooks/*.py`

### 2. Schema and Contract Design Enforcement

**CRITICAL: Enforcement Discipline**

To prevent documentation drift, establish the following rule in FOUNDATION_MANUAL.md:

> **Schema/Contract Sync Rule**
> 
> When adding a new skill or playbook:
> 1. Define Pydantic schemas (Input/Output) in the skill file
> 2. Register skill in `src/ag/skills/__init__.py`
> 3. **Immediately** add schema entries to `SCHEMA_INVENTORY.md`
> 4. **Immediately** add implementation entry to `CONTRACT_INVENTORY.md`
> 5. Write contract verification test in `test_contracts.py`
>
> **Sprint Close Gate:** Inventory verification is part of sprint hygiene checklist.

**Schema Design Guidelines:**

1. **Field naming consistency**: Use canonical names across pipeline boundaries
   - Research pipeline: `report`, `key_findings`, `sources_used`
   - Summarize pipeline: `document_summary`, `key_points`, `sources`
   
2. **Schema bridging pattern**: When a skill must accept multiple upstream formats:
   ```python
   class SkillInput(BaseModel):
       # Canonical fields
       document_summary: str = Field(...)
       
       # Aliased fields for alternate upstreams
       report: str | None = Field(default=None, exclude=True)
       
       @model_validator(mode="before")
       @classmethod
       def normalize_fields(cls, data: dict) -> dict:
           if "report" in data and "document_summary" not in data:
               data["document_summary"] = data.pop("report")
           return data
   ```

3. **Contract test coverage**: Every skill MUST have:
   - Schema validation test (input/output match contracts)
   - Registry presence test  
   - At minimum 1 execution test

**Verification Commands:**
```bash
# List all registered skills/playbooks
ag skills list
ag playbooks list

# Run contract tests  
pytest tests/test_contracts.py -v

# Run skill framework tests
pytest tests/test_skill_framework.py -v
```

### 3. SPRINT_MANUAL.md Update

Add to sprint close hygiene checklist:
```markdown
- [ ] Verify SCHEMA_INVENTORY.md matches codebase
- [ ] Verify CONTRACT_INVENTORY.md matches codebase
- [ ] Run `ag skills list` and confirm all appear in inventories
```

---

## Risks

| Risk | Mitigation |
|------|------------|
| Manual process forgotten | Add to SPRINT_MANUAL checklist |
| New contributors unaware | Document in FOUNDATION_MANUAL |
| Drift accumulates silently | Consider future automated sync test |

---

## Context

**Discovery:** Sprint 08 closure verification (run `7eaba88d-7683-46c9-a762-4430e6027b63`)

**Related items:**
- BUG-0013: research_v0 pipeline broken (revealed schema bridging gap)
- AF-0063: Schema inventory documentation (original setup)
- AF-0013: Contract inventory hardening (original setup)

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF0081
- **PR:** #<number>
- **Author:** <name>
- **Date:** YYYY-MM-DD
- **Branch:** <chore/inventory-sync>
- **Risk level:** P2
- **Runtime mode used for verification:** manual
