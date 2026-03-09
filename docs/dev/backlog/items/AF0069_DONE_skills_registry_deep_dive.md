# BACKLOG ITEM — AF0069 — skills_registry_deep_dive
# Version number: v0.2

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

> **File naming (required):** `AF0069_DONE_skills_registry_deep_dive.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0069
- **Type:** Documentation
- **Status:** DONE
- **Priority:** P1
- **Area:** Skills / Architecture
- **Owner:** Kai
- **Target sprint:** Sprint08
- **Completed:** Sprint08

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

### Skill Inventory (as of Sprint08)

> **UPDATE (Sprint08):** V1 framework removed (AF-0079). All process-oriented stubs removed.
> Only capability-oriented V2 skills remain.

| Skill | Status | Capability | Used By |
|-------|--------|------------|--------|
| `load_documents` | ✅ Real | File I/O: read from workspace | summarize_v0 |
| `summarize_docs` | ✅ Real | LLM: generate summary | summarize_v0 |
| `fetch_web_content` | ✅ Real | HTTP: fetch and extract text from URLs | research_v0 |
| `synthesize_research` | ✅ Real | LLM: synthesize research report | research_v0 |
| `fail_skill` | 🧪 Test | Always fails (testing) | tests |
| `error_skill` | 🧪 Test | Always raises exception (testing) | tests |

### Removed Skills (AF-0079)

| Skill | Reason for Removal |
|-------|-------------------|
| `emit_result` | Redundant — skills can write output directly |
| `echo_tool` | V1 stub — replaced by V2 test skills |
| `analyze_task` | Process-oriented, not a capability |
| `execute_task` | Process-oriented, not a capability |
| `verify_result` | Process-oriented, not a capability |
| `normalize_input` | Process-oriented, not a capability |
| `plan_subtasks` | Orchestration (runtime job, not skill) |
| `execute_subtask` | Process-oriented, not a capability |
| `verify_delegation` | Process-oriented, not a capability |
| `finalize_result` | Redundant with emit_result |

### Hardcoded Elements

1. **Skill registration** (`create_default_registry()`):
   ```python
   def create_default_registry() -> SkillRegistry:
       registry = SkillRegistry()
       registry.register("load_documents", LoadDocumentsSkill())
       registry.register("summarize_docs", SummarizeDocsSkill())
       registry.register("fetch_web_content", FetchWebContentSkill())
       registry.register("synthesize_research", SynthesizeResearchSkill())
       registry.register("fail_skill", FailSkill())
       registry.register("error_skill", ErrorSkill())
       return registry
   ```

2. **Skill imports** — all V2 Pydantic-based skills:
   ```python
   from ag.skills.load_documents import LoadDocumentsSkill
   from ag.skills.summarize_docs import SummarizeDocsSkill
   from ag.skills.fetch_web_content import FetchWebContentSkill
   from ag.skills.synthesize_research import SynthesizeResearchSkill
   from ag.skills.stubs import FailSkill, ErrorSkill
   ```

3. **Singleton pattern** (lines 467-473):
   ```python
   _default_registry: SkillRegistry | None = None
   def get_default_registry() -> SkillRegistry:
       # Lazy singleton — no way to reset or customize
   ```

### CLI Integration

`ag skills list` (as of Sprint08):
- ✅ Shows all registered skills with descriptions
- ✅ V2 skills show proper descriptions from `describe()` method
- ⚠️ No indication of LLM requirement (future enhancement)

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

- [x] Document architectural principle (Skills = Capabilities) — ARCHITECTURE.md §3.3
- [x] Update ARCHITECTURE.md with skills section — ARCHITECTURE.md §3.3
- [x] Create "How to add skills" guide — ARCHITECTURE.md §3.3
- [x] Document skill inventory with status — ARCHITECTURE.md §3.3 + this AF
- [x] Document versioning convention — Skills use bare names (no `_v0` suffix)

**Note:** The architectural principle "Skills = Capabilities" drove AF-0079 (V1 removal).
All process-oriented stubs were removed; only capability-oriented skills remain.

---

## Related Implementation AFs

| AF | Title | Scope | Status |
|----|-------|-------|--------|
| AF-0079 | Skills framework V1 removal | Remove V1 framework, stubs, simplify registry | ✅ DONE |
| AF-0077 | Skills plugin architecture | Entry points, external registration (v1+) | PROPOSED |
| AF-0074 | research_v0 playbook | New capability-oriented skills | ✅ DONE |

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
