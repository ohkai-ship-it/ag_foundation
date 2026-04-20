# BACKLOG ITEM — AF0075 — skills_registry_cleanup
# Version number: v0.2

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

> **File naming (required):** `AF0075_<Status>_skills_registry_cleanup.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0075
- **Type:** Cleanup / Engineering
- **Status:** DROPPED
- **Priority:** P2
- **Area:** Skills / Registry
- **Owner:** TBD
- **Target sprint:** ~~Sprint08~~

---

## Dropped

**Reason:** Superseded by AF-0079 (Skills framework V1 removal).

The V1 removal refactor addresses all items in this AF:
- Stub skills deleted (not deprecated)
- V2 descriptions fix becomes moot (only one skill type)
- Test fixtures removed from default registry

---

## Original Summary

Clean up the skills registry by marking deprecated stubs, fixing CLI bugs, and improving discoverability.

---

## Problem

1. **Process-oriented stubs exposed:** `analyze_task`, `execute_task`, `verify_result`, etc. are visible to users but cannot be meaningfully implemented
2. **V2 skill descriptions empty:** CLI bug — `ag skills list` shows empty descriptions for V2 skills → **See AF-0059**
3. **No way to distinguish production vs stub skills**
4. **Test fixtures visible:** `echo_tool`, `fail_skill`, `error_skill` shown to users

---

## Deliverables

### 1. Mark deprecated stubs

Add `is_deprecated: bool = False` to `SkillInfo` and `SkillV2Info`:

```python
@dataclass
class SkillInfo:
    name: str
    description: str
    fn: SkillFn
    is_stub: bool = True
    is_deprecated: bool = False  # NEW
```

Mark these as deprecated:
- `analyze_task`
- `execute_task`
- `verify_result`
- `normalize_input`
- `plan_subtasks`
- `execute_subtask`
- `verify_delegation`
- `finalize_result`

### 2. Add `--all` flag to `ag skills list`

By default, hide deprecated and test skills:

```bash
ag skills list           # Production skills only
ag skills list --all     # All skills including deprecated
```

### 3. Hide test fixtures by default

Mark as test-only (hidden by default):
- `echo_tool`
- `fail_skill`
- `error_skill`

---

## Implementation

### Files to modify

| File | Changes |
|------|---------|
| `src/ag/skills/registry.py` | Add `is_deprecated` field, update registrations |
| `src/ag/cli/main.py` | Add `--all` flag |
| `tests/test_cli.py` | Test new flag behavior |

---

## Acceptance Criteria

- [ ] `ag skills list` shows only production skills by default
- [ ] `ag skills list --all` shows all skills with deprecation markers
- [ ] Deprecated skills documented in skill inventory
- [ ] All tests pass

---

## Related Items

- **AF-0059:** CLI list commands (V2 skill descriptions fix)
- **AF-0069:** Skills architecture documentation
- **AF-0077:** Skills plugin architecture (future)
