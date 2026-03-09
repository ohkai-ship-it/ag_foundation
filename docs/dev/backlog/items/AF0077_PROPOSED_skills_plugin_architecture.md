# BACKLOG ITEM — AF0077 — skills_plugin_architecture
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

> **File naming (required):** `AF0077_<Status>_skills_plugin_architecture.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0077
- **Type:** Architecture / Feature
- **Status:** PROPOSED
- **Priority:** P3
- **Area:** Skills / Architecture
- **Owner:** TBD
- **Target sprint:** Backlog (v1+)

---

## Summary

Design and implement a plugin architecture for skills that allows external skill registration without modifying core code.

---

## Problem

Current skill registration is hardcoded in `create_default_registry()`:
- Adding a skill requires modifying `registry.py`
- No way for users to add custom skills
- All skills bundled with core package

---

## Proposed Architecture

### Option A: Entry Points (Recommended)

Use Python entry points (`pyproject.toml`) for skill discovery:

```toml
# In user's pyproject.toml
[project.entry-points."ag.skills"]
my_skill = "my_package.skills:MySkill"
```

**Pros:**
- Standard Python mechanism
- Works with pip install
- No config files to manage

**Cons:**
- Requires packaging knowledge
- Can't add skills at runtime

### Option B: Directory Scanning

Scan a `~/.ag/skills/` directory for skill modules:

```
~/.ag/skills/
  my_skill.py  # Contains MySkill class
  another.py
```

**Pros:**
- Simple for users
- No packaging required

**Cons:**
- Security concerns (arbitrary code execution)
- Import path complexity

### Option C: Config-Based Registration

YAML/TOML config pointing to skill classes:

```yaml
# ~/.ag/skills.yaml
skills:
  - name: my_skill
    module: my_package.skills
    class: MySkill
```

**Pros:**
- Explicit configuration
- Can enable/disable skills

**Cons:**
- Another config file to manage
- Doesn't auto-discover

---

## Recommended Approach

**Phase 1:** Entry points for packaged skills
**Phase 2:** Directory scanning for quick prototypes
**Phase 3:** Config override for customization

---

## Implementation Sketch

```python
def create_default_registry() -> SkillRegistry:
    registry = SkillRegistry()
    
    # 1. Register built-in skills
    _register_builtin_skills(registry)
    
    # 2. Discover entry point skills
    _discover_entrypoint_skills(registry)
    
    # 3. Scan user directory (if enabled)
    if config.enable_user_skills:
        _scan_user_skills(registry)
    
    return registry

def _discover_entrypoint_skills(registry: SkillRegistry) -> None:
    """Discover skills via entry points."""
    from importlib.metadata import entry_points
    
    eps = entry_points(group="ag.skills")
    for ep in eps:
        skill_class = ep.load()
        registry.register_v2(skill_class())
```

---

## Deliverables

- [ ] Design document: Entry points vs alternatives
- [ ] Implement entry point discovery
- [ ] Update documentation for skill authors
- [ ] Example external skill package
- [ ] Tests for plugin loading

---

## Acceptance Criteria

- [ ] External skills can be registered via entry points
- [ ] `ag skills list` shows external skills
- [ ] Documentation for creating skill plugins
- [ ] Security considerations documented

---

## Security Considerations

- Entry points only load installed packages (pip trust model)
- Directory scanning should be opt-in with warnings
- Skills should not have elevated privileges

---

## Related Items

- **AF-0069:** Skills architecture documentation
- **AF-0075:** Skills registry cleanup
- **AF-0078:** Playbooks plugin architecture
