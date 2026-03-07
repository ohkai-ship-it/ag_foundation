# BACKLOG ITEM — AF0067 — skill_code_documentation
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

> **File naming (required):** `AF0067_PROPOSED_skill_code_documentation.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0067
- **Type:** Docs
- **Status:** PROPOSED
- **Priority:** P2
- **Area:** Skills / Docs
- **Owner:** Kai
- **Target sprint:** Sprint07

---

## Problem
The skill layer code (`src/ag/skills/`) lacks inline documentation that:
1. **Schema references:** Which schemas (Pydantic models) each file uses/produces
2. **Contract references:** Which protocols/contracts each file implements or depends on
3. **Extension guide:** How developers add new skills (currently undocumented in code)

After AF0060 (skill framework) and AF0063/AF0013 (inventories), we have the reference docs but the code doesn't point to them. New contributors reading skill code can't easily understand:
- What data shapes flow through the skill
- What behavioral contracts the skill implements
- How to create a new skill following the pattern

---

## Goal
Update skill code with comprehensive inline documentation:

1. **Module docstrings** linking to SCHEMA_INVENTORY.md and CONTRACT_INVENTORY.md
2. **Schema annotations** in each file showing which models are used
3. **Extension guide** as a module-level docstring in `base.py` explaining how to create new skills
4. **Cross-references** between related files (base.py ↔ registry.py ↔ strategic_brief.py)

---

## Non-goals
- Rewriting skill logic (code stays the same)
- Creating external documentation (we have SKILLS_ARCHITECTURE_0.1.md)
- Auto-generating docs from code

---

## Acceptance criteria (Definition of Done)
- [ ] `src/ag/skills/base.py` has module docstring with:
  - [ ] Link to SCHEMA_INVENTORY.md for SkillInput/SkillOutput/SkillContext
  - [ ] Link to CONTRACT_INVENTORY.md for Skill ABC
  - [ ] "How to create a new skill" section with step-by-step guide
- [ ] `src/ag/skills/registry.py` has module docstring with:
  - [ ] Schema references (SkillV2Info)
  - [ ] Contract references (explains v1 vs v2 distinction)
  - [ ] How to register skills
- [ ] `src/ag/skills/strategic_brief.py` has:
  - [ ] Module docstring listing all schemas it defines/uses
  - [ ] Example of a complete v2 skill implementation
- [ ] All docstrings follow Google style (existing convention)
- [ ] CI passes (ruff check, pytest)

---

## Implementation notes

### Module docstring template for base.py

```python
"""Skill framework base classes (AF0060).

Schemas defined here (see SCHEMA_INVENTORY.md):
- SkillInput: Base input schema for v2 skills
- SkillOutput: Base output schema for v2 skills  
- StubSkillOutput: Extension for stub responses
- SkillContext: Runtime context (dataclass, not Pydantic)

Contracts implemented (see CONTRACT_INVENTORY.md):
- Skill[InputT, OutputT]: ABC for typed skills

How to create a new skill:
1. Define input schema (subclass SkillInput)
2. Define output schema (subclass SkillOutput)
3. Create skill class (subclass Skill[YourInput, YourOutput])
4. Implement execute(input, ctx) -> output
5. Register with registry.register_v2(YourSkill())

Example:
    class MyInput(SkillInput):
        topic: str = Field(default="general")
    
    class MyOutput(SkillOutput):
        result: str = ""
    
    class MySkill(Skill[MyInput, MyOutput]):
        name = "my_skill"
        description = "Does something useful"
        input_schema = MyInput
        output_schema = MyOutput
        
        def execute(self, input: MyInput, ctx: SkillContext) -> MyOutput:
            # Use ctx.provider for LLM calls
            # Use ctx.workspace_path for file access
            return MyOutput(success=True, summary="Done", result="...")
"""
```

### Files to update

| File | Changes |
|------|---------|
| `src/ag/skills/__init__.py` | Add package-level docstring |
| `src/ag/skills/base.py` | Extension guide + schema/contract refs |
| `src/ag/skills/registry.py` | Registration guide + v1/v2 distinction |
| `src/ag/skills/strategic_brief.py` | Schema list + "example implementation" note |

---

## Risks
- Low: Documentation-only change
- Risk of docstrings getting stale → mitigated by drift tests (AF0063/AF0013)

---

## Related items
- **AF0060:** Skill definition framework (implemented the code being documented)
- **AF0063:** SCHEMA_INVENTORY.md (external reference)
- **AF0013:** CONTRACT_INVENTORY.md (external reference)
- **SKILLS_ARCHITECTURE_0.1.md:** High-level design reference

---

# Completion section (fill when done)

Pending completion.
