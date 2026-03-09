# BACKLOG ITEM — AF0070 — playbooks_architecture_documentation
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

> **File naming (required):** `AF0070_<Status>_playbooks_registry_deep_dive.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0070
- **Type:** Documentation
- **Status:** PROPOSED
- **Priority:** P1
- **Area:** Playbooks/Architecture
- **Owner:** Kai
- **Target sprint:** Sprint08

---

## Key Architectural Insight

**Skills are CAPABILITIES, Playbooks are PROCEDURES.**

| Concept | Role | Example |
|---------|------|---------|
| **Skill** | Atomic capability — does ONE thing | `load_documents` (file I/O), `summarize_docs` (LLM call) |
| **Playbook** | Orchestration — sequences capabilities | `summarize_v0` chains load → summarize → emit |

This explains the architectural simplicity difference:
- **Playbooks** are pure configuration (Pydantic models) — they describe WHAT to do
- **Skills** have behavior (ABC with `execute()`) — they DO things
- **Runtime** interprets playbooks and invokes skills

### Design Problem: Stub-Dependent Playbooks

`default_v0` and `delegate_v0` reference process-oriented stubs (`analyze_task`, `execute_task`, `verify_result`) that cannot be implemented as capability-oriented skills. These playbooks need redesign to use real capabilities.

Only `summarize_v0` follows the correct pattern: it sequences concrete capabilities (load → summarize → emit).

---

## Summary

Deep dive analysis of the playbooks registry to understand architecture, document patterns, identify hardcoded elements, and plan future playbook additions.

---

## Current State Analysis

### Playbook Inventory

| Name | File | Skills Used | Status | Problem |
|------|------|-------------|--------|---------|
| summarize_v0 | `summarize_v0.py` | load_documents, summarize_docs, emit_result | ✅ PRODUCTION | None — correct design |
| default_v0 | `default_v0.py` | analyze_task, execute_task, verify_result | ❌ STUB-DEPENDENT | Skills are process-oriented, not capabilities |
| delegate_v0 | `delegate_v0.py` | normalize_input, plan_subtasks, execute_subtask, verify_delegation, finalize_result | ❌ STUB-DEPENDENT | Skills are process-oriented, not capabilities |

### Architecture Comparison: Playbooks vs Skills

| Aspect | Skills | Playbooks |
|--------|--------|-----------|
| Role | **Capability** — atomic operation | **Procedure** — orchestration |
| Base Class | `Skill` ABC with `execute()` | `Playbook` Pydantic model (data only) |
| Behavior | Executable | Declarative configuration |
| Schema | Custom per-skill I/O types | Generic `PlaybookStep` |
| Registration | `SkillRegistry` class | Simple `_REGISTRY` dict |

### ReasoningMode Enum

Defined in `ag.core.playbook.ReasoningMode`:

| Mode | Value | Usage |
|------|-------|-------|
| DIRECT | `"direct"` | Standard single-pass execution |
| CHAIN_OF_THOUGHT | `"chain_of_thought"` | Step-by-step reasoning |
| TREE_OF_THOUGHT | `"tree_of_thought"` | Multi-branch exploration |
| REFLECTION | `"reflection"` | Self-critique and revision |

**Current Usage:**
- `default_v0`: DIRECT only
- `delegate_v0`: DIRECT + CHAIN_OF_THOUGHT
- `summarize_v0`: DIRECT only

**Question**: Is ReasoningMode actually used by runtime? Or is it metadata only?

---

## Hardcoded Elements

### File: `registry.py`

```python
# Lines 13-15: Imports
from ag.playbooks.default_v0 import DEFAULT_V0
from ag.playbooks.delegate_v0 import DELEGATE_V0
from ag.playbooks.summarize_v0 import SUMMARIZE_V0

# Lines 21-31: Registry dict
_REGISTRY: dict[str, "Playbook"] = {
    "default_v0": DEFAULT_V0,
    "default": DEFAULT_V0,  # Alias
    "delegate_v0": DELEGATE_V0,
    "delegate": DELEGATE_V0,  # Alias
    "summarize_v0": SUMMARIZE_V0,
    "summarize": SUMMARIZE_V0,  # Alias
}

# Lines 47-53: list_playbooks return value
def list_playbooks() -> list[str]:
    return ["default_v0", "delegate_v0", "summarize_v0"]
```

### File: `__init__.py`

```python
# Lines 22-25: Re-exports
from ag.playbooks.default_v0 import DEFAULT_V0
from ag.playbooks.delegate_v0 import DELEGATE_V0
from ag.playbooks.summarize_v0 import SUMMARIZE_V0

# Lines 28-35: __all__
__all__ = [
    "DEFAULT_V0",
    "DELEGATE_V0",
    "SUMMARIZE_V0",
    "get_playbook",
    "list_playbooks",
]
```

---

## How to Add New Playbooks

### Step-by-Step Process

1. **Create playbook file**: `src/ag/playbooks/{name}_v0.py`
   ```python
   """{name}_v0 playbook — Description."""
   from ag.core.playbook import (
       Budgets, Playbook, PlaybookStep, PlaybookStepType, ReasoningMode
   )
   
   NAME_V0 = Playbook(
       playbook_version="0.1",
       name="{name}_v0",
       version="1.0.0",
       description="...",
       reasoning_modes=[ReasoningMode.DIRECT],
       budgets=Budgets(...),
       steps=[...],
       metadata={...},
   )
   ```

2. **Update `registry.py`**:
   - Add import at top
   - Add entry to `_REGISTRY` dict
   - Add alias if desired
   - Update `list_playbooks()` return list

3. **Update `__init__.py`**:
   - Add import
   - Add to `__all__`

4. **Ensure skills exist**: All `skill_name` references must be registered skills

5. **Add tests**: Create `test_{name}_playbook.py`

---

---

## Deliverables

- [ ] Document architectural principle (Playbooks = Procedures)
- [ ] Update ARCHITECTURE.md with playbooks section
- [ ] Complete "How to add playbooks" guide (above)
- [ ] Document playbook inventory with status
- [ ] Document versioning convention (`_v0` suffix for playbooks, not skills)
- [ ] Clarify ReasoningMode usage in runtime

---

## Related Implementation AFs

| AF | Title | Scope |
|----|-------|-------|
| AF-0076 | Playbooks registry cleanup | Auto-generate list_playbooks(), add stability markers |
| AF-0078 | Playbooks plugin architecture | YAML loading, entry points (v1+) |
| AF-0074 | research_v0 playbook | First new capability-oriented playbook |

---

## Non-goals

- Building new playbooks (see AF-0074)
- Registry cleanup/CLI fixes (see AF-0076)
- Plugin architecture/YAML loading (see AF-0078)

---

## Acceptance Criteria

- [ ] Playbooks architecture section added to ARCHITECTURE.md
- [ ] "How to add a playbook" documented and accurate
- [ ] Playbook inventory table complete
- [ ] ReasoningMode behavior clarified

---

## CLI Integration Check

### Command: `ag playbooks list`

**Expected Output**: Should show all 3 playbooks with descriptions.

**Known Issues**: None identified yet.

### Command: `ag run --playbook <name>`

**Behavior**: Uses `get_playbook()` to resolve playbook.

---

## Questions to Resolve

1. **ReasoningMode**: Is it actually used by runtime, or just metadata?
2. **Step types**: Are BRANCH/LOOP/GATE implemented or just defined?
3. **Budgets**: Are `max_tokens`/`max_duration_seconds` enforced?
4. **Aliases**: Should `list_playbooks()` include aliases or just canonical names?
5. **Versioning**: When do we increment playbook version (e.g., "1.0.0" → "1.1.0")?

---

## Acceptance Criteria

- [ ] All hardcoded elements documented
- [ ] How-to guide for adding new playbooks
- [ ] At least 2 new playbook candidates ready for implementation
- [ ] ReasoningMode usage clarified
- [ ] CLI integration verified

---

## References

- Related: [AF-0069: Skills registry deep dive](AF0069_PROPOSED_skills_registry_deep_dive.md)
- Related: [AF-0059: Implement playbooks list](AF0059_PROPOSED_implement_playbooks_list.md)
- Related: [AF-0065: First skill set (summarize_v0)](AF0065_READY_first_skill_set.md)
- Schema: `src/ag/core/playbook.py`
- Registry: `src/ag/playbooks/registry.py`
