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
- **Status:** DONE
- **Priority:** P3
- **Area:** Playbooks / Architecture
- **Owner:** Jacob
- **Target sprint:** Sprint 10 (stretch)

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

### Option A: YAML Playbooks (Recommended) ✅ CHOSEN

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

- [x] Entry point discovery for playbooks
- [x] `ag playbooks list` shows source column
- [x] PlaybookInfo tracks source (built-in/entry-point/yaml)
- [x] Built-in playbooks registered via pyproject.toml entry points
- [x] register_playbook() and unregister_playbook() API for tests
- [x] Unit tests for entry point discovery
- [ ] YAML playbooks load from ~/.ag/playbooks/ (infrastructure ready, needs PyYAML)
- [ ] Documentation for creating playbook files (deferred)

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

---

## Completion Summary

**Completed:** Sprint 10 (Phase 1)

### Implementation

1. **PlaybookInfo dataclass** (`src/ag/playbooks/registry.py`):
   - Added `source: str` field ("built-in", "entry-point", "yaml")
   - Added `source_path: Path | None` for YAML files
   - Added `aliases: list[str]` for alias tracking

2. **Entry point discovery**:
   - `_discover_entrypoint_playbooks()` discovers from `ag.playbooks` group
   - Invalid entry points logged and skipped (never crash)
   - Automatically derives aliases (e.g., `research_v0` → `research`)

3. **Built-in playbooks as entry points** (`pyproject.toml`):
   ```toml
   [project.entry-points."ag.playbooks"]
   default_v0 = "ag.playbooks.default_v0:DEFAULT_V0"
   delegate_v0 = "ag.playbooks.delegate_v0:DELEGATE_V0"
   research_v0 = "ag.playbooks.research_v0:RESEARCH_V0"
   summarize_v0 = "ag.playbooks.summarize_v0:SUMMARIZE_V0"
   ```

4. **YAML loading infrastructure** (ready, needs PyYAML):
   - `_load_yaml_playbook()` parses YAML and validates via Pydantic
   - `_discover_yaml_playbooks()` scans `~/.ag/playbooks/`
   - Graceful handling if PyYAML not installed

5. **Public API for tests**:
   - `register_playbook()` — programmatic registration
   - `unregister_playbook()` — cleanup (removes canonical + aliases)
   - `reset_registry()` — clear for isolation

6. **CLI updates** (`src/ag/cli/main.py`):
   - `ag playbooks list` shows Source column

### Tests Added

7 new tests in `tests/test_contracts.py::TestPlaybookPluginArchitecture`:
- PlaybookInfo source field tests (2)
- register_playbook / unregister_playbook tests (2)
- Default registry entry-point verification tests (2)
- Entry point discovery mock test (1)

1 new test in `tests/test_cli.py::TestPlaybooksListCommand`:
- test_playbooks_list_shows_source_column

### Metrics

- Tests: 582 passing (574 → 582)
- Ruff: Clean
