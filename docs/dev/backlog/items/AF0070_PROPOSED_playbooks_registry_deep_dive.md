# AF-0070: Playbooks Registry Deep Dive

| Field         | Value                                   |
|---------------|-----------------------------------------|
| **ID**        | AF-0070                                 |
| **Status**    | PROPOSED                                |
| **Priority**  | P1                                      |
| **Area**      | Playbooks/Architecture                  |
| **Owner**     | Kai                                     |
| **Created**   | 2026-03-08                              |
| **Sprint**    | Backlog                                 |

---

## Summary

Deep dive analysis of the playbooks registry to understand architecture, document patterns, identify hardcoded elements, and plan future playbook additions.

---

## Current State Analysis

### Playbook Inventory

| Name | File | Skills Used | Reasoning | Status |
|------|------|-------------|-----------|--------|
| default_v0 | `default_v0.py` | analyze_task, execute_task, verify_result | DIRECT | STUB-DEPENDENT |
| delegate_v0 | `delegate_v0.py` | normalize_input, plan_subtasks, execute_subtask, verify_delegation, finalize_result | DIRECT, CHAIN_OF_THOUGHT | STUB-DEPENDENT |
| summarize_v0 | `summarize_v0.py` | load_documents, summarize_docs, emit_result | DIRECT | PRODUCTION |

**Status Legend:**
- **PRODUCTION**: Uses real V2 skills that can execute
- **STUB-DEPENDENT**: Uses stub skills that return mock data

### Architecture Comparison: Playbooks vs Skills

| Aspect | Skills | Playbooks |
|--------|--------|-----------|
| Base Class | `Skill` ABC in `base.py` | None — uses `Playbook` Pydantic model from `ag.core.playbook` |
| Behavior | Has `run()` method — executable | Pure declarative data — no behavior |
| Schema | Custom per-skill Pydantic models | Generic `Playbook` + `PlaybookStep` models |
| V1/V2 Pattern | Yes — legacy callables vs typed classes | No — all use same pattern |
| Registration | Complex (`SkillRegistry` class) | Simple (`_REGISTRY` dict) |
| Discovery | `get_skill()` returns callable or Skill instance | `get_playbook()` returns Playbook |

**Key Insight**: Playbooks are simpler because they're pure configuration. They don't need a base class — they're just instances of `Playbook` Pydantic model.

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

## New Playbook Suggestions

### 1. `review_v0` — Code Review Pipeline

**Purpose**: Analyze code files and produce structured feedback.

**Steps**:
1. `load_documents` — Read source files
2. `analyze_code` — Static analysis / pattern detection (NEW SKILL)
3. `review_code` — LLM-based review (NEW SKILL)
4. `emit_result` — Output review findings

**Skills Needed**: `analyze_code`, `review_code`

### 2. `research_v0` — Multi-Source Research Compilation

**Purpose**: Gather information from multiple sources and synthesize.

**Steps**:
1. `load_documents` — Read reference materials
2. `search_web` — Fetch external sources (NEW SKILL)
3. `synthesize_research` — Combine and analyze (NEW SKILL)
4. `emit_result` — Output research report

**Skills Needed**: `search_web`, `synthesize_research`

### 3. `transform_v0` — File Transformation Pipeline

**Purpose**: Convert/transform files from one format to another.

**Steps**:
1. `load_documents` — Read input files
2. `transform_content` — Apply transformation rules (NEW SKILL)
3. `validate_output` — Check transformation result (NEW SKILL)
4. `emit_result` — Store transformed output

**Skills Needed**: `transform_content`, `validate_output`

### 4. `validate_v0` — Schema/Contract Validation

**Purpose**: Validate files against schemas or contracts.

**Steps**:
1. `load_documents` — Read files to validate
2. `load_schema` — Load validation schema (NEW SKILL)
3. `validate_against_schema` — Run validation (NEW SKILL)
4. `emit_result` — Output validation report

**Skills Needed**: `load_schema`, `validate_against_schema`

### 5. `chat_v0` — Interactive Conversation

**Purpose**: Single-turn Q&A without file operations.

**Steps**:
1. `parse_query` — Extract user intent (NEW SKILL)
2. `generate_response` — LLM response generation (NEW SKILL)

**Skills Needed**: `parse_query`, `generate_response` (simple skills)

---

## Implementation Roadmap

### Phase 1: Documentation Audit
- [ ] Document ReasoningMode actual usage in runtime
- [ ] Verify all playbooks in CLI `ag playbooks list`
- [ ] Check if PlaybookStepType.BRANCH/LOOP/GATE are implemented

### Phase 2: Registry Cleanup
- [ ] Auto-generate `list_playbooks()` from `_REGISTRY.keys()` (exclude aliases)
- [ ] Consider auto-discovery pattern (scan `ag.playbooks` for `*_V0` constants)

### Phase 3: New Playbooks
- [ ] Implement `chat_v0` (simplest — no file I/O)
- [ ] Implement `transform_v0` (file-based)
- [ ] Implement `review_v0` (code-focused)

### Phase 4: Advanced Features
- [ ] Make ReasoningMode affect execution
- [ ] Implement branching/looping step types
- [ ] YAML playbook loading

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
