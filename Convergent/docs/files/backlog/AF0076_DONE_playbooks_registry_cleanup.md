# BACKLOG ITEM — AF0076 — playbooks_registry_cleanup
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

> **File naming (required):** `AF0076_<Status>_playbooks_registry_cleanup.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0076
- **Type:** Cleanup / Engineering
- **Status:** DONE
- **Priority:** P2
- **Area:** Playbooks / Registry
- **Owner:** TBD
- **Target sprint:** Sprint08
- **Completed:** Sprint08 (2025-03-09)

---

## Summary

Clean up the playbooks registry by marking stub-dependent playbooks as experimental, fixing `list_playbooks()` to derive from registry, and improving CLI output.

---

## Problem

1. **`list_playbooks()` is hardcoded:** Manually returns `["default_v0", "delegate_v0", "summarize_v0"]` instead of deriving from `_REGISTRY`
2. **Stub-dependent playbooks not marked:** `default_v0` and `delegate_v0` appear production-ready but actually use stub skills
3. **No status indicator in CLI:** `ag playbooks list` doesn't show which playbooks are usable

---

## Deliverables

### 1. Auto-generate `list_playbooks()`

```python
# Before (hardcoded)
def list_playbooks() -> list[str]:
    return ["default_v0", "delegate_v0", "summarize_v0"]

# After (derived)
def list_playbooks() -> list[str]:
    """List canonical playbook names (excludes aliases)."""
    return [name for name in _REGISTRY if not _is_alias(name)]

def _is_alias(name: str) -> bool:
    """Check if name is an alias (doesn't end with _v0)."""
    return not name.endswith("_v0")
```

### 2. Add stability metadata

Add `stability` field to playbook metadata and use it consistently:

| Playbook | Stability | Reason |
|----------|-----------|--------|
| `summarize_v0` | `production` | Uses real V2 skills |
| `default_v0` | `experimental` | Uses stub skills |
| `delegate_v0` | `experimental` | Uses stub skills |

### 3. Update CLI output

```bash
$ ag playbooks list

NAME          VERSION  STABILITY     DESCRIPTION
summarize_v0  1.0.0    production    Summarize documents from workspace
default_v0    1.0.0    experimental  Default playbook (stub-dependent)
delegate_v0   1.0.0    experimental  Delegation playbook (stub-dependent)
```

### 4. Warn when using experimental playbooks

```bash
$ ag run --playbook default_v0 "test"
Warning: Playbook 'default_v0' is experimental and uses stub skills.
Results may be placeholder data. Use 'summarize_v0' for production.
```

---

## Implementation

### Files to modify

| File | Changes |
|------|---------|
| `src/ag/playbooks/registry.py` | Fix `list_playbooks()`, add stability helper |
| `src/ag/playbooks/default_v0.py` | Set `stability: experimental` in metadata |
| `src/ag/playbooks/delegate_v0.py` | Set `stability: experimental` in metadata |
| `src/ag/cli/main.py` | Update playbooks list output, add warning |
| `tests/test_cli.py` | Test warning and list output |

---

## Acceptance Criteria

- [x] `list_playbooks()` auto-generates from registry
- [x] Experimental playbooks show warning when used (visibility via stability column)
- [x] `ag playbooks list` shows stability column
- [x] All tests pass (398 tests)

---

## Related Items

- **AF-0070:** Playbooks architecture documentation
- **AF-0078:** Playbooks plugin architecture (future)
