# BACKLOG ITEM — AF0069 — skills_registry_deep_dive
# Version number: v0.1

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

> **File naming (required):** `AF0069_PROPOSED_skills_registry_deep_dive.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0069
- **Type:** Documentation
- **Status:** PROPOSED
- **Priority:** P1
- **Area:** Skills / Architecture
- **Owner:** Kai
- **Target sprint:** Sprint08

---

## Problem

The skills registry (`src/ag/skills/registry.py`) needs documentation after the V1 framework removal (AF-0079):

1. **Document final architecture**: Single skill pattern (Pydantic schemas + ABC)
2. **Hardcoded registration**: All skills registered in `create_default_registry()` — no plugin system
3. **No plugin system yet**: Future AF-0077 for external skill registration
4. **Testing strategy**: How to test skills without polluting user environment

---

## Key Architectural Insight

**Skills are CAPABILITIES, Playbooks are PROCEDURES.**

| Concept | Role | Example |
|---------|------|---------|
| **Skill** | Atomic capability — does ONE thing | `load_documents` (file I/O), `summarize_docs` (LLM call) |
| **Playbook** | Orchestration — sequences capabilities | `summarize_v0` chains load → summarize → emit |

The current stub skills violate this principle. They are **process-oriented** ("analyze", "execute", "verify") rather than **capability-oriented**. This makes them impossible to implement meaningfully.

### Design Smell: Process-Oriented Stubs

| Stub Skill | Problem | Should Be |
|------------|---------|----------|
| `analyze_task` | What does "analyze" mean? | A playbook, or concrete skills like `extract_entities`, `classify_intent` |
| `execute_task` | Execute what, how? | A playbook, or concrete skills like `call_api`, `transform_data` |
| `verify_result` | Verify against what? | A playbook, or concrete skills like `validate_schema`, `check_citations` |
| `plan_subtasks` | Planning is orchestration | A playbook responsibility, not a skill |

**Recommendation:** Stub skills should be replaced with capability-oriented skills or removed. Playbooks should handle orchestration.

---

## Current State Analysis

### Skill Inventory (as of Sprint07)

| Skill | Version | Status | Capability | Used By |
|-------|---------|--------|------------|--------|
| `load_documents` | V2 | ✅ Real | File I/O: read from workspace | summarize_v0 |
| `summarize_docs` | V2 | ✅ Real | LLM: generate summary | summarize_v0 |
| `emit_result` | V2 | ✅ Real | File I/O: write to workspace | summarize_v0 |
| `echo_tool` | V1 | ⚠️ Stub | Test fixture | tests |
| `analyze_task` | V1 | ⚠️ Stub | ❌ Process-oriented | default_v0 |
| `execute_task` | V1 | ⚠️ Stub | ❌ Process-oriented | default_v0 |
| `verify_result` | V1 | ⚠️ Stub | ❌ Process-oriented | default_v0 |
| `normalize_input` | V1 | ⚠️ Stub | ❌ Process-oriented | delegate_v0 |
| `plan_subtasks` | V1 | ⚠️ Stub | ❌ Orchestration (not a skill) | delegate_v0 |
| `execute_subtask` | V1 | ⚠️ Stub | ❌ Process-oriented | delegate_v0 |
| `verify_delegation` | V1 | ⚠️ Stub | ❌ Process-oriented | delegate_v0 |
| `finalize_result` | V1 | ⚠️ Stub | ❌ Duplicate of emit_result? | delegate_v0 |
| `fail_skill` | V1 | ⚠️ Stub | Test fixture | tests |
| `error_skill` | V1 | ⚠️ Stub | Test fixture | tests |

### Hardcoded Elements

1. **Skill registration** (lines 400-460):
   ```python
   def create_default_registry() -> SkillRegistry:
       registry = SkillRegistry()
       registry.register("echo_tool", ...)
       registry.register("analyze_task", ...)
       # ... 15+ hardcoded registrations
   ```

2. **Skill imports** (lines 52-55):
   ```python
   from ag.skills.emit_result import EmitResultSkill
   from ag.skills.load_documents import LoadDocumentsSkill
   from ag.skills.summarize_docs import SummarizeDocsSkill
   ```

3. **Singleton pattern** (lines 467-473):
   ```python
   _default_registry: SkillRegistry | None = None
   def get_default_registry() -> SkillRegistry:
       # Lazy singleton — no way to reset or customize
   ```

### CLI Integration Issues

`ag skills list` in `main.py`:
- Shows all skills (no filtering)
- V2 skills have empty descriptions (bug)
- No indication of stub vs production
- No indication of LLM requirement

---

## Goal

Produce a skills strategy document and implementation plan addressing:

1. **Inventory audit**: Complete list of skills with status and next steps
2. **Architecture review**: Plugin system vs hardcoded registration trade-offs
3. **UI improvements**: Fix empty descriptions, add skill categories to CLI
4. **Stub implementation plan**: Which stubs to implement, which to remove
5. **Testing strategy**: How to test skills without polluting user environment

---

## Deliverables

- [ ] Document architectural principle (Skills = Capabilities)
- [ ] Update ARCHITECTURE.md with skills section
- [ ] Create "How to add skills" guide
- [ ] Document skill inventory with status
- [ ] Document versioning convention (no `_v0` suffix for skills)

---

## Related Implementation AFs

| AF | Title | Scope |
|----|-------|-------|
| AF-0079 | Skills framework V1 removal | Remove V1 framework, stubs, simplify registry |
| AF-0077 | Skills plugin architecture | Entry points, external registration (v1+) |
| AF-0074 | research_v0 playbook | New capability-oriented skills |

---

## Non-goals

- Implementing new skills (see AF-0074)
- Framework refactoring (see AF-0079)
- Plugin architecture (see AF-0077)

---

## Acceptance Criteria

- [ ] Skills architecture section added to ARCHITECTURE.md
- [ ] "How to add a skill" documented
- [ ] Skill inventory table complete and accurate
- [ ] V2 skill patterns documented with examples

---

## Implementation Notes

### Questions to Answer

1. **Which stubs are needed?**
   - `default_v0` playbook uses: `analyze_task`, `execute_task`, `verify_result`
   - `agent_network` playbook uses: `normalize_input`, `plan_subtasks`, `execute_subtask`, `verify_delegation`, `finalize_result`
   - Test skills: `echo_tool`, `fail_skill`, `error_skill`

2. **Should test stubs be visible?**
   - Option A: Hide from `ag skills list` by default
   - Option B: Add category column showing "test" vs "production"
   - Option C: Move to separate test registry

3. **Why are V2 descriptions empty?**
   - CLI likely using `SkillInfo.description` not `Skill.description`
   - Need to check `main.py` skills_list command

4. **Plugin system complexity?**
   - Current: ~50 lines of registration code
   - Simple plugin: Entry points in pyproject.toml
   - Full plugin: Directory scanning + config files

### Proposed Skill Categories

```python
class SkillCategory(str, Enum):
    PRODUCTION = "production"  # Real skills for users
    PLAYBOOK = "playbook"      # Playbook infrastructure (may be stubs)
    TEST = "test"              # Test fixtures only
    DEPRECATED = "deprecated"  # Scheduled for removal
```

### Files to Analyze

| File | Lines | Purpose |
|------|-------|---------|
| `src/ag/skills/registry.py` | 473 | Registry class + all registrations |
| `src/ag/skills/base.py` | ~220 | Skill ABC and schemas |
| `src/ag/cli/main.py` | skills_list | CLI integration |
| `src/ag/playbooks/*.py` | varies | Playbook skill references |

---

## Risks
- Scope creep: Analysis could lead to large implementation backlog
- Breaking changes: Modifying registry could break playbooks

Mitigation:
- Keep this AF focused on analysis and planning
- Create separate AFs for implementation work
- Ensure backward compatibility in any changes

---

## Related Items
- **AF-0060:** Skill definition framework (V2 skills)
- **AF-0065:** First skill set (summarize_v0)
- **AF-0067:** Skill code documentation
- **AF-0019:** Agent network playbook (delegation stubs)

---

# Completion Section (fill when done)

Pending analysis.
