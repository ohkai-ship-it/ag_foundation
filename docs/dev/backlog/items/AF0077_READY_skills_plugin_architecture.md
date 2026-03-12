# BACKLOG ITEM — AF0077 — skills_plugin_architecture
# Version number: v0.2

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - CI discipline (ruff + pytest -W error + coverage)
> - INDEX update rule (status ↔ filename integrity)

> **File naming (required):** `AF0077_<Status>_skills_plugin_architecture.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0077
- **Type:** Architecture / Feature
- **Status:** DONE
- **Priority:** P3
- **Area:** Skills / Architecture
- **Owner:** Jacob
- **Target sprint:** Sprint 10
- **Depends on:** AF-0079 (V1 removal — DONE)

---

## Context

After AF-0079 unified skills around the Pydantic-based `Skill` ABC, all
skill registration is hardcoded in `create_default_registry()` in
[registry.py](../../../../src/ag/skills/registry.py). Adding a new skill
requires modifying that function, importing the class, and adding a
`registry.register(...)` call.

This AF adds entry-point-based skill discovery so that external packages
can register skills by declaring them in `pyproject.toml` — the standard
Python mechanism for plugin systems.

---

## Problem

1. **Closed registry:** Adding a skill requires modifying core source code
2. **No external skills:** Users cannot install a skill package and have it auto-discovered
3. **Monolithic coupling:** All skills must live inside `src/ag/skills/`

---

## Goal

Enable external skill packages to register skills via Python entry points.
After `pip install ag-skill-foo`, `ag skills list` shows `foo` without
any code changes to `ag_foundation`.

---

## Non-goals

- Directory scanning (`~/.ag/skills/`) — security concerns, deferred
- Config-based skill registration — unnecessary complexity
- Dynamic runtime skill loading/unloading
- Skill marketplace or distribution system
- Changes to the Skill ABC or SkillContext interface

---

## Design: Entry Points

### How it works

Python entry points allow installed packages to advertise objects under
a named group. The host application discovers them at runtime via
`importlib.metadata.entry_points()`.

**External skill package declares in its `pyproject.toml`:**
```toml
[project.entry-points."ag.skills"]
my_skill = "my_package.skills:MySkill"
```

**ag_foundation discovers at startup:**
```python
from importlib.metadata import entry_points

for ep in entry_points(group="ag.skills"):
    skill_class = ep.load()    # imports my_package.skills.MySkill
    registry.register(skill_class())
```

### Why entry points

| Criterion | Entry Points | Dir Scanning | Config File |
|-----------|:---:|:---:|:---:|
| Standard Python mechanism | ✅ | ❌ | ❌ |
| Works with pip install | ✅ | ❌ | ❌ |
| No arbitrary code execution risk | ✅ | ❌ | ❌ |
| No extra config to manage | ✅ | ✅ | ❌ |
| Auto-discovery | ✅ | ✅ | ❌ |

Entry points are the standard, secure, zero-config approach. Directory
scanning and config-based registration can be added later if needed.

---

## Scope

### 1. Entry point discovery in registry

Modify `create_default_registry()` to discover and register entry-point
skills after registering built-in skills:

```python
def create_default_registry() -> SkillRegistry:
    registry = SkillRegistry()

    # 1. Register built-in skills (unchanged)
    registry.register(LoadDocumentsSkill())
    registry.register(SummarizeDocsSkill())
    # ... existing registrations ...

    # 2. Discover entry-point skills (NEW)
    _discover_entrypoint_skills(registry)

    return registry


def _discover_entrypoint_skills(registry: SkillRegistry) -> None:
    """Discover and register skills from installed entry points."""
    from importlib.metadata import entry_points

    for ep in entry_points(group="ag.skills"):
        try:
            skill_class = ep.load()
            skill = skill_class()
            # Validate it implements the Skill protocol
            if not isinstance(skill, Skill):
                logger.warning(
                    "Entry point %s does not implement Skill protocol, skipping",
                    ep.name,
                )
                continue
            # Don't overwrite built-in skills
            if registry.has(skill.name):
                logger.warning(
                    "Entry point skill %r conflicts with built-in skill, skipping",
                    skill.name,
                )
                continue
            registry.register(skill)
        except Exception:
            logger.warning("Failed to load skill entry point %s", ep.name, exc_info=True)
```

### 2. Register ag_foundation's own skills as entry points

Move ag_foundation's built-in skills to entry points too, so the
pattern is dogfooded:

```toml
# pyproject.toml
[project.entry-points."ag.skills"]
load_documents = "ag.skills.load_documents:LoadDocumentsSkill"
summarize_docs = "ag.skills.summarize_docs:SummarizeDocsSkill"
emit_result = "ag.skills.emit_result:EmitResultSkill"
fetch_web_content = "ag.skills.fetch_web_content:FetchWebContentSkill"
synthesize_research = "ag.skills.synthesize_research:SynthesizeResearchSkill"
web_search = "ag.skills.web_search:WebSearchSkill"
```

Then `create_default_registry()` becomes simply:

```python
def create_default_registry() -> SkillRegistry:
    registry = SkillRegistry()
    _discover_entrypoint_skills(registry)  # discovers built-in + external
    # Test stubs registered separately (not entry points)
    registry.register(EchoSkill())
    registry.register(FailSkill())
    registry.register(ErrorSkill())
    return registry
```

### 3. `ag skills list` shows source

Add a `source` field to `SkillInfo` to distinguish built-in from external:

```python
@dataclass
class SkillInfo:
    name: str
    description: str
    skill: Skill
    input_schema: type[SkillInput]
    output_schema: type[SkillOutput]
    requires_llm: bool = False
    source: str = "built-in"  # NEW: "built-in" | "entry-point" | "test-stub"
```

CLI output:
```
$ ag skills list
NAME                  SOURCE        REQUIRES_LLM
load_documents        built-in      No
summarize_docs        built-in      Yes
my_custom_skill       entry-point   No
```

### 4. Tests

- Unit test: mock entry points, verify discovery and registration
- Unit test: entry point that fails to load → logs warning, doesn't crash
- Unit test: entry point with name conflict → skipped with warning
- Unit test: entry point that doesn't implement Skill → skipped
- Integration test: `ag skills list` shows entry-point skills

---

## Key Files

| File | Change |
|------|--------|
| `src/ag/skills/registry.py` | Add `_discover_entrypoint_skills()`, update `create_default_registry()` |
| `src/ag/skills/registry.py` | Add `source` field to `SkillInfo` |
| `pyproject.toml` | Add `[project.entry-points."ag.skills"]` section |
| `tests/test_skill_framework.py` | Tests for entry point discovery |
| `src/ag/cli/` | Update `ag skills list` to show source column |

---

## Acceptance criteria (Definition of Done)

- [x] `_discover_entrypoint_skills()` discovers skills from `ag.skills` entry point group
- [x] ag_foundation's built-in skills registered as entry points in pyproject.toml
- [x] `create_default_registry()` uses entry point discovery (dogfooding)
- [x] `SkillInfo.source` field distinguishes built-in / entry-point / test-stub
- [x] `ag skills list` displays source column
- [x] Invalid entry points log warning and don't crash
- [x] Name conflicts with built-in skills are rejected with warning
- [x] Unit tests cover: discovery, load failure, name conflict, protocol check
- [x] `ruff check src tests` passes
- [x] `pytest -W error` passes

---

## Risks

| Risk | Mitigation |
|------|------------|
| Entry point discovery slow at startup | Only runs once; benchmark in tests |
| External skill breaks at import time | try/except with logging, never crash |
| Test stubs accidentally exposed as entry points | Register stubs directly, not via entry points |
| Entry point cache stale after pip install | Known Python issue; documented as "re-run pip install -e .") |

---

## Related Items

- **AF-0079:** Skills framework V1 removal (prerequisite — unified Skill ABC) — DONE
- **AF-0069:** Skills architecture documentation — DONE
- **AF-0078:** Playbooks plugin architecture (parallel — same pattern for playbooks)

---

## Completion Summary

**Completed:** Sprint 10

### Implementation

1. **Entry point discovery** (`src/ag/skills/registry.py`):
   - Added `_discover_entrypoint_skills()` function
   - Discovers skills from `ag.skills` entry point group
   - Invalid entry points logged and skipped (never crash)
   - Name conflicts with existing skills rejected with warning

2. **SkillInfo.source field**:
   - Added `source: str = "built-in"` to SkillInfo dataclass
   - Values: `"built-in"`, `"entry-point"`, `"test-stub"`
   - Included in `get_info()` return dict

3. **Built-in skills as entry points** (`pyproject.toml`):
   ```toml
   [project.entry-points."ag.skills"]
   load_documents = "ag.skills.load_documents:LoadDocumentsSkill"
   summarize_docs = "ag.skills.summarize_docs:SummarizeDocsSkill"
   emit_result = "ag.skills.emit_result:EmitResultSkill"
   fetch_web_content = "ag.skills.fetch_web_content:FetchWebContentSkill"
   synthesize_research = "ag.skills.synthesize_research:SynthesizeResearchSkill"
   web_search = "ag.skills.web_search:WebSearchSkill"
   ```

4. **CLI updates** (`src/ag/cli/main.py`):
   - `ag skills list` shows Source column
   - `ag skills info` shows Source field

### Tests Added

9 new tests in `tests/test_skill_framework.py::TestEntryPointDiscovery`:
- Source field tests (3)
- Mock entry point discovery test
- Load failure handling test
- Non-Skill protocol rejection test
- Name conflict handling test
- Default registry integration test
- Skills list integration test

### Metrics

- Tests: 574 passing (565 → 574)
- Ruff: Clean
