# AF0013 — Contract inventory hardening: reconcile docs ↔ implementation and add consistency checks
# Version number: v0.3

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
- **ID:** AF-0013
- **Type:** Docs/Quality
- **Status:** Ready
- **Priority:** P1
- **Area:** Contracts
- **Owner:** Jacob
- **Target sprint:** Sprint06

---

## Problem
The contract inventory exists but is in a sprint review folder (`docs/dev/reviews/entries/REVIEW_S01_2026-02-24/CONTRACT_INVENTORY.md`), not a canonical location. It also needs reconciliation with current implementation state.

### Scope clarification: Contracts vs Schemas

| Term | What it covers | AF |
|------|----------------|-----|
| **Contract** | Protocols/interfaces (behavioral promises) | **AF-0013** (this) |
| **Schema** | Pydantic models (data shapes) | AF-0063 |

This AF focuses on **Protocols** defined in `interfaces.py`:
- Planner, Orchestrator, Executor, Verifier, Recorder, SkillRegistry
- NOT Pydantic schemas (TaskSpec, RunTrace, etc.) — those are AF-0063

---

## Goal
Make contract documentation reliably reflect reality:

1. **Move CONTRACT_INVENTORY.md** to canonical location (`docs/dev/additional/`)
2. **Audit contracts** — verify documented Protocols match implementation
3. **Add drift detection** — CI test to catch discrepancies

---

## Non-goals
- Introducing new runtime features unrelated to contract consistency
- Large refactors of core modules
- Documenting Pydantic schemas (that's AF-0063)
- Heavy doc generation frameworks

---

## Acceptance criteria (Definition of Done)
- [ ] CONTRACT_INVENTORY.md moved to `docs/dev/additional/CONTRACT_INVENTORY.md`
- [ ] All Protocols in `interfaces.py` documented with signature + purpose
- [ ] Discrepancies noted: (a) implemented but undocumented, or (b) documented but not implemented
- [ ] Drift detection test added (`tests/test_contracts_consistency.py`)
- [ ] CI runs drift detection and fails on mismatch
- [ ] ARCHITECTURE.md references CONTRACT_INVENTORY.md
- [ ] Cross-reference to SCHEMA_INVENTORY.md (AF-0063) for complementary coverage

---

## Implementation notes

### Step 1: Move file
```bash
# Move from sprint review folder to canonical location
mv docs/dev/reviews/entries/REVIEW_S01_2026-02-24/CONTRACT_INVENTORY.md docs/dev/additional/CONTRACT_INVENTORY.md
```

### Step 2: Audit Protocols
Check `src/ag/core/interfaces.py` for all Protocol definitions and verify each is documented:
- Planner
- Orchestrator
- Executor
- Verifier
- Recorder
- SkillRegistry (if exists)

### Step 3: Drift detection test
```python
# tests/test_contracts_consistency.py
def test_all_protocols_documented():
    """Every Protocol in interfaces.py should appear in CONTRACT_INVENTORY.md."""
    from ag.core import interfaces
    import inspect
    
    # Get all Protocol classes from interfaces module
    protocols = [name for name, obj in inspect.getmembers(interfaces) 
                 if inspect.isclass(obj) and hasattr(obj, '__protocol_attrs__')]
    
    # Read CONTRACT_INVENTORY.md
    inventory_path = Path("docs/dev/additional/CONTRACT_INVENTORY.md")
    content = inventory_path.read_text()
    
    missing = [p for p in protocols if p not in content]
    assert not missing, f"Undocumented protocols: {missing}"
```

---

## Risks
- Low: Documentation-only change with one test addition
- Risk of scope creep → mitigated by clear scope boundary (contracts only, not schemas)

---

## Related items
- **AF-0063:** Schema inventory (Pydantic models) — complementary documentation
- **SKILLS_ARCHITECTURE_0.1.md:** Section 3.1 defines contract vs schema distinction
- **AF-0060:** May add new Skill protocol — must update CONTRACT_INVENTORY when done

---

## Documentation impact
- **CONTRACT_INVENTORY.md:** Relocated and updated
- **ARCHITECTURE.md:** Add reference to CONTRACT_INVENTORY.md
- **tests/:** Add `test_contracts_consistency.py`

---

# Completion section (fill when done)

Pending completion.
