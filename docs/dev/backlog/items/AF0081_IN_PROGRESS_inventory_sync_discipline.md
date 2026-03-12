# BACKLOG ITEM — AF0081 — inventory_sync_discipline
# Version number: v0.2

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
- **Status:** DONE
- **Priority:** P2
- **Area:** Docs/Process
- **Owner:** Jacob
- **Target sprint:** Sprint 10
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

- [x] SCHEMA_INVENTORY.md updated with all current schemas
- [x] CONTRACT_INVENTORY.md updated with all current implementations
- [x] Registry-based drift test added to `test_documentation_drift.py`
- [x] Test passes in CI (blocks merge if schemas undocumented)
- [ ] Remove manual checklist from SPRINT_MANUAL (trust CI instead) — N/A: no manual checklist exists

---

## Implementation notes

### 1. Schema/Contract Inventory Updates

Update both inventory documents to reflect current state:
- Run `ag skills list` to get all registered skills
- Cross-reference input/output schemas with SCHEMA_INVENTORY.md

### 2. Automated Enforcement via Registry

**Chosen approach:** Extend `test_documentation_drift.py` with registry-based test.

Add to `TestSchemaInventoryDrift`:

```python
def test_all_registered_skill_schemas_documented(self, schema_inventory_content: str) -> None:
    """All Pydantic schemas from registered skills should be documented."""
    from ag.skills import get_default_registry
    
    registry = get_default_registry()
    missing = []
    
    for skill_name in registry.list_skills():
        skill_info = registry.get_skill(skill_name)
        if skill_info is None:
            continue
            
        # Check input schema
        input_name = skill_info.input_schema.__name__
        if input_name not in schema_inventory_content:
            missing.append(f"{skill_name}:input:{input_name}")
            
        # Check output schema  
        output_name = skill_info.output_schema.__name__
        if output_name not in schema_inventory_content:
            missing.append(f"{skill_name}:output:{output_name}")
    
    assert not missing, f"Undocumented skill schemas: {missing}"
```

**Why registry-based:**
- Tests what's actually available at runtime
- Consistent with `ag skills list` behavior
- Works with future plugin architecture (AF0078 entry points)
- Unregistered code doesn't trigger false positives

### 3. Remove Manual Checklist

Once CI enforces schema documentation, remove manual checklist from SPRINT_MANUAL.
Trust the test — if it passes, docs are in sync.

---

## Risks

| Risk | Mitigation |
|------|------------|
| Test not run locally | CI blocks merge |
| New schema types missed | Extend test as needed |

---

## Context

**Discovery:** Sprint 08 closure verification (run `7eaba88d-7683-46c9-a762-4430e6027b63`)

**Related items:**
- BUG-0013: research_v0 pipeline broken (revealed schema bridging gap)
- AF-0063: Schema inventory documentation (original setup)
- AF-0013: Contract inventory hardening (original setup)

---

# Completion section (fill when done)

## Summary

Implemented registry-based drift detection for inventory documents. CI now
fails if new skills or schemas are added without updating documentation.

## Changes

### SCHEMA_INVENTORY.md
Added missing skill schemas:
- `WebSearchInput`, `WebSearchOutput`, `SearchResult` (web_search.py)
- `LoadDocumentsInput`, `LoadDocumentsOutput` (load_documents.py)
- `SummarizeDocsInput`, `SummarizeDocsOutput` (summarize_docs.py)
- `EmitResultInput`, `EmitResultOutput` (emit_result.py)
- `EchoInput`, `EchoOutput` (stubs.py)

### CONTRACT_INVENTORY.md
- Expanded `Skill` implementation row into full table
- Added all registered skills with their input/output schemas

### test_documentation_drift.py
- Added `test_all_registered_skill_schemas_documented()` — validates all
  registered skill schemas are in SCHEMA_INVENTORY.md
- Added `TestContractImplementationDrift` class with
  `test_all_registered_skills_documented()` — validates all registered
  skills are in CONTRACT_INVENTORY.md

## Test Results
- 563 tests passing (2 new drift tests)
- Drift detection now blocks CI if documentation is out of sync
