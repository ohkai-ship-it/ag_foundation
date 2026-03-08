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
- **Type:** Analysis / Engineering
- **Status:** PROPOSED
- **Priority:** P1
- **Area:** Skills / Architecture
- **Owner:** Kai
- **Target sprint:** Sprint08

---

## Problem

The skills registry (`src/ag/skills/registry.py`) has grown organically and needs a strategic review:

1. **Unclear skill inventory**: Mix of production skills, test stubs, and legacy wrappers
2. **Hardcoded registration**: All skills registered in `create_default_registry()` — no plugin system
3. **Missing descriptions**: V2 skills show empty descriptions in `ag skills list`
4. **Stub skills exposure**: Test stubs visible to users alongside production skills
5. **No skill categories**: Can't filter by "production", "test", "LLM-required", etc.
6. **Implementation gaps**: Many stubs need real implementations for production use

---

## Current State Analysis

### Skill Inventory (as of Sprint07)

| Skill | Version | Type | Status | Notes |
|-------|---------|------|--------|-------|
| `load_documents` | V2 | Production | ✅ Real | Loads files from workspace |
| `summarize_docs` | V2 | Production | ✅ Real | LLM-powered summarization |
| `emit_result` | V2 | Production | ✅ Real | Emits artifacts to workspace |
| `strategic_brief` | V1 | Production | ✅ Real | Non-LLM brief generation |
| `strategic_brief_v2` | V2 | Production | ✅ Real | LLM brief generation |
| `echo_tool` | V1 | Test | ⚠️ Stub | Test fixture |
| `analyze_task` | V1 | Playbook | ⚠️ Stub | default_v0 playbook |
| `execute_task` | V1 | Playbook | ⚠️ Stub | default_v0 playbook |
| `verify_result` | V1 | Playbook | ⚠️ Stub | default_v0 playbook |
| `normalize_input` | V1 | Delegation | ⚠️ Stub | agent_network playbook |
| `plan_subtasks` | V1 | Delegation | ⚠️ Stub | agent_network playbook |
| `execute_subtask` | V1 | Delegation | ⚠️ Stub | agent_network playbook |
| `verify_delegation` | V1 | Delegation | ⚠️ Stub | agent_network playbook |
| `finalize_result` | V1 | Delegation | ⚠️ Stub | agent_network playbook |
| `fail_skill` | V1 | Test | ⚠️ Stub | Test fixture |
| `error_skill` | V1 | Test | ⚠️ Stub | Test fixture |

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
   from ag.skills.strategic_brief import StrategicBriefSkillV2, strategic_brief_skill
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

### Phase 1: Analysis (this AF)
- [ ] Complete skill inventory with implementation status
- [ ] Document hardcoded vs configurable elements
- [ ] Identify bugs in current implementation
- [ ] Propose architecture improvements
- [ ] Create implementation roadmap

### Phase 2: Quick Fixes (follow-up AF)
- [ ] Fix V2 skill empty descriptions in CLI
- [ ] Add `--production` / `--all` flag to `ag skills list`
- [ ] Add skill category to registry (production/test/stub)

### Phase 3: Stub Implementation (future sprints)
- [ ] Implement real `analyze_task` skill (LLM-powered)
- [ ] Implement real `execute_task` skill (with tool use)
- [ ] Implement real delegation skills
- [ ] Remove or hide test-only stubs

### Phase 4: Plugin Architecture (v1+)
- [ ] Design skill plugin system
- [ ] Allow external skill registration
- [ ] Configuration-based skill loading

---

## Non-goals
- Implementing all stub skills in this AF (scope too large)
- Building a full plugin system (v1+ feature)
- Changing skill execution semantics

---

## Acceptance criteria (Definition of Done)
- [ ] Skill inventory documented with status for each
- [ ] Architecture analysis complete
- [ ] Implementation roadmap created
- [ ] Follow-up AFs created for implementation work
- [ ] Strategy document reviewed

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
