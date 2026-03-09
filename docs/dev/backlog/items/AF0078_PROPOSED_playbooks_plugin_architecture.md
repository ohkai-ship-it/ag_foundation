# BACKLOG ITEM — AF0078 — playbooks_plugin_architecture
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

> **File naming (required):** `AF0078_<Status>_playbooks_plugin_architecture.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0078
- **Type:** Architecture / Feature
- **Status:** PROPOSED
- **Priority:** P3
- **Area:** Playbooks / Architecture
- **Owner:** TBD
- **Target sprint:** Backlog (v1+)

---

## Summary

Design and implement a plugin architecture for playbooks that allows external playbook registration and YAML-based playbook definitions.

---

## Problem

Current playbook registration is hardcoded in `registry.py`:
- Adding a playbook requires modifying Python code
- Users cannot define custom playbooks without code changes
- No declarative playbook format

---

## Proposed Architecture

### Option A: YAML Playbooks (Recommended)

Allow playbooks to be defined in YAML files:

```yaml
# ~/.ag/playbooks/my_playbook.yaml
name: my_playbook_v0
version: "1.0.0"
description: "My custom playbook"
reasoning_modes: [direct]
budgets:
  max_steps: 10
  max_duration_seconds: 300
steps:
  - step_id: step_0
    name: load
    skill_name: load_documents
  - step_id: step_1
    name: process
    skill_name: my_custom_skill
  - step_id: step_2
    name: emit
    skill_name: emit_result
```

**Pros:**
- Declarative — no Python knowledge needed
- Easy to share and version
- Can validate against Playbook schema

**Cons:**
- Limited to what Playbook schema supports
- No custom logic in steps

### Option B: Entry Points

Same as skills — use Python entry points:

```toml
[project.entry-points."ag.playbooks"]
my_playbook = "my_package.playbooks:MY_PLAYBOOK_V0"
```

**Pros:**
- Consistent with skills plugin approach
- Works with packages

**Cons:**
- Requires Python code

### Option C: Hybrid

- YAML for simple playbooks
- Entry points for complex playbooks with custom logic

---

## Recommended Approach

**Phase 1:** YAML playbook loading from `~/.ag/playbooks/`
**Phase 2:** Entry points for packaged playbooks
**Phase 3:** Workspace-local playbooks (`./playbooks/`)

---

## Implementation Sketch

```python
def _discover_playbooks() -> dict[str, Playbook]:
    """Discover all playbooks."""
    playbooks = {}
    
    # 1. Built-in playbooks
    playbooks.update(_BUILTIN_PLAYBOOKS)
    
    # 2. YAML playbooks from user directory
    yaml_dir = Path.home() / ".ag" / "playbooks"
    for yaml_file in yaml_dir.glob("*.yaml"):
        pb = _load_yaml_playbook(yaml_file)
        playbooks[pb.name] = pb
    
    # 3. Entry point playbooks
    eps = entry_points(group="ag.playbooks")
    for ep in eps:
        pb = ep.load()
        playbooks[pb.name] = pb
    
    return playbooks

def _load_yaml_playbook(path: Path) -> Playbook:
    """Load and validate a YAML playbook."""
    import yaml
    with open(path) as f:
        data = yaml.safe_load(f)
    return Playbook.model_validate(data)
```

---

## Deliverables

- [ ] YAML playbook schema documentation
- [ ] YAML loading implementation
- [ ] User playbook directory scanning
- [ ] Entry point discovery
- [ ] Example YAML playbook
- [ ] Validation and error messages

---

## Acceptance Criteria

- [ ] YAML playbooks load correctly
- [ ] `ag playbooks list` shows user playbooks
- [ ] Invalid YAML shows helpful errors
- [ ] Documentation for creating playbook files
- [ ] Workspace-local playbooks supported

---

## Schema Validation

YAML playbooks must pass Pydantic validation:
- All required fields present
- Step IDs unique
- Referenced skills exist (warning if not)
- Budgets within limits

---

## Related Items

- **AF-0070:** Playbooks architecture documentation
- **AF-0076:** Playbooks registry cleanup
- **AF-0077:** Skills plugin architecture
