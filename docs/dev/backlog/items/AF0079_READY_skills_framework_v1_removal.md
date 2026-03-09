# BACKLOG ITEM — AF0079 — skills_framework_v1_removal
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

> **File naming (required):** `AF0079_<Status>_skills_framework_v1_removal.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0079
- **Type:** Refactor / Breaking Change
- **Status:** READY
- **Priority:** P1
- **Area:** Skills / Framework
- **Owner:** TBD
- **Target sprint:** Sprint08

---

## Summary

Remove the V1 skill framework entirely, including all stub skills. Simplify the registry to only support the Pydantic-based skill pattern.

---

## Background

The skills framework currently supports two patterns:

| Pattern | Description | Status |
|---------|-------------|--------|
| **V1** | Legacy callable functions with `SkillFn` type | Stubs only, no production use |
| **V2** | Pydantic schemas + ABC with `execute()` | Production (`load_documents`, `summarize_docs`, `emit_result`) |

V1 was scaffolding for early development. All production skills use V2. The V1 stubs (`analyze_task`, `execute_task`, etc.) are process-oriented and cannot be meaningfully implemented.

**Decision:** Remove V1 entirely. All new skills use Pydantic schemas.

---

## Scope

### Remove

| File/Component | Action |
|----------------|--------|
| `SkillFn` type alias | Delete |
| `SkillInfo` dataclass (V1) | Delete |
| `register()` method (V1) | Delete |
| `list_skills()` (V1) | Delete |
| V1 stub skills | Delete all |
| V1 registration in `create_default_registry()` | Delete |

### V1 Stub Skills to Remove

- `echo_tool` (test fixture)
- `analyze_task`
- `execute_task`
- `verify_result`
- `normalize_input`
- `plan_subtasks`
- `execute_subtask`
- `verify_delegation`
- `finalize_result`
- `fail_skill` (test fixture)
- `error_skill` (test fixture)

### Keep / Rename

| Current | After |
|---------|-------|
| `SkillV2Info` → | `SkillInfo` |
| `register_v2()` → | `register()` |
| `list_v2_skills()` → | `list_skills()` |
| `get_v2_skill()` → | `get_skill()` |

---

## Implementation

### 1. Simplify `SkillRegistry`

```python
# Before: Two registration paths
class SkillRegistry:
    def register(self, name: str, fn: SkillFn, ...): ...  # V1
    def register_v2(self, skill: Skill): ...              # V2
    def list_skills(self): ...      # V1
    def list_v2_skills(self): ...   # V2

# After: Single registration path
class SkillRegistry:
    def register(self, skill: Skill): ...
    def list_skills(self) -> list[SkillInfo]: ...
    def get_skill(self, name: str) -> Skill | None: ...
```

### 2. Update `create_default_registry()`

```python
# Before: Mixed V1/V2
def create_default_registry() -> SkillRegistry:
    registry = SkillRegistry()
    registry.register("echo_tool", echo_tool_fn, ...)  # V1 stub
    registry.register_v2(LoadDocumentsSkill())         # V2 real
    ...

# After: V2 only
def create_default_registry() -> SkillRegistry:
    registry = SkillRegistry()
    registry.register(LoadDocumentsSkill())
    registry.register(SummarizeDocsSkill())
    registry.register(EmitResultSkill())
    return registry
```

### 3. Update CLI

- `ag skills list` — use simplified `list_skills()`
- Remove any V1-specific handling

### 4. Update Tests

- Remove V1 stub tests
- Keep/update integration tests using real skills
- Create test-specific skills if needed (not registered by default)

---

## Deliverables

- [ ] Delete V1 types and methods from `registry.py`
- [ ] Delete all V1 stub skill implementations
- [ ] Rename V2 methods to standard names
- [ ] Update `create_default_registry()` 
- [ ] Update CLI `skills list` command
- [ ] Update/remove affected tests
- [ ] Update imports in `__init__.py`
- [ ] Verify `summarize_v0` playbook still works

---

## Acceptance Criteria

- [ ] No V1 code paths remain in `registry.py`
- [ ] `ag skills list` shows only: `load_documents`, `summarize_docs`, `emit_result`
- [ ] `ag run --playbook summarize_v0` works unchanged
- [ ] All tests pass
- [ ] Coverage ≥95%

---

## Breaking Changes

- Any code using `registry.register(name, fn, ...)` must migrate
- Any code using `list_skills()` for V1 must migrate to new API

**Impact:** Low — V1 was internal scaffolding, not public API.

---

## Related Items

- **AF-0075:** Skills registry cleanup (simplified — just add `--all` flag)
- **AF-0074:** research_v0 playbook (new skills use simplified framework)
- **AF-0069:** Skills architecture documentation (document final pattern)
