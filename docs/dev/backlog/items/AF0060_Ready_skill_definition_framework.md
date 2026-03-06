# BACKLOG ITEM — AF0060 — skill_definition_framework
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

> **File naming (required):** `AF####_<Status>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0060
- **Type:** Architecture
- **Status:** READY
- **Priority:** P0
- **Area:** Skills
- **Owner:** Kai
- **Target sprint:** Sprint06

---

## Problem
Current skill implementation is inadequate:

1. **No clear definition:** Skills are just `Callable[[dict], tuple[bool, str, dict]]` with no schema
2. **No LLM integration:** Skills cannot call the LLM — `strategic_brief` just lists files
3. **Stub-only:** 11 of 12 skills are stubs returning hardcoded values
4. **No validation:** Input/output schemas are informal at best
5. **Unclear purpose:** What distinguishes a skill from a playbook step?

Current skill signature:
```python
SkillFn = Callable[[dict[str, Any]], tuple[bool, str, dict[str, Any]]]
```

This tells us nothing about:
- What parameters are expected
- What the output structure should be
- Whether the skill needs LLM access
- What evidence/citations it should produce

---

## Goal
Define a clear skill framework that answers:

1. **What is a skill?** — A reusable, LLM-powered capability with defined I/O
2. **Skill contract** — Schema for inputs, outputs, and configuration
3. **LLM access** — How skills invoke the model (provider injection? context passing?)
4. **Evidence model** — How skills produce citations and artifacts
5. **Composability** — How skills can be used in playbooks and direct execution

### Bounded Autonomy Principle

This framework implements **Phase 1 (Playbook-driven)** of the autonomy spectrum:
- Humans define WHAT (skills exist, playbook structure, budgets)
- Agents decide HOW (skill parameters, retry decisions, output content within schema)

Future phases (Guided Agent, Goals Only, Full Agent) will evolve FROM this foundation.
See: `SKILLS_ARCHITECTURE_0.1.md` Section 2.1 for the full spectrum.

Deliverables:
- [ ] Skill definition spec (this document, refined)
- [ ] Base skill class or protocol
- [ ] At least one "real" skill implementation (strategic_brief v2 or new)
- [ ] Updated registry with schema awareness

---

## Non-goals
- Dynamic skill loading from files (future)
- User-defined skills (future)  
- Skill marketplace/sharing (future)
- Async skill execution (v1+)

---

## Design questions (to resolve during refinement)

### Q1: Skill vs Playbook distinction
Options:
- **A)** Skills are atomic LLM calls; playbooks compose skills
- **B)** Skills can have internal multi-step logic; playbooks only sequence skills
- **C)** Merge concepts — playbooks ARE skill compositions

### Q2: LLM access pattern
Options:
- **A)** Skills receive provider instance in params
- **B)** Skills receive a `context` object with provider + workspace + config
- **C)** Skills declare LLM needs; runtime injects via decorator

### Q3: Schema enforcement
Options:
- **A)** Pydantic models for input/output (like StrategicBrief)
- **B)** JSON Schema declarations
- **C)** Runtime validation only (current, basically none)

### Q4: Evidence production
Options:
- **A)** Skills return Citation objects (current strategic_brief approach)
- **B)** Skills return EvidenceRef directly  
- **C)** Skills return raw data; caller converts to evidence

---

## Proposed skill contract (strawman)

```python
from pydantic import BaseModel
from typing import Protocol

class SkillInput(BaseModel):
    """Base class for skill inputs."""
    prompt: str  # Common to all skills
    
class SkillOutput(BaseModel):
    """Base class for skill outputs."""
    success: bool
    summary: str
    
class SkillContext:
    """Runtime context passed to skills."""
    provider: LLMProvider
    workspace_path: Path | None
    config: dict[str, Any]
    
class Skill(Protocol):
    """Skill protocol."""
    name: str
    description: str
    input_schema: type[SkillInput]
    output_schema: type[SkillOutput]
    
    def execute(self, input: SkillInput, context: SkillContext) -> SkillOutput:
        ...
```

### Example: Real strategic_brief

```python
class StrategicBriefInput(SkillInput):
    title: str = "Strategic Brief"
    max_files: int = 50
    focus_areas: list[str] = []

class StrategicBriefOutput(SkillOutput):
    brief_md: str
    brief_json: dict
    sources: list[SourceFile]
    citations: list[Citation]

class StrategicBriefSkill:
    name = "strategic_brief"
    description = "Generate strategic brief from workspace files using LLM synthesis"
    input_schema = StrategicBriefInput
    output_schema = StrategicBriefOutput
    
    def execute(self, input: StrategicBriefInput, ctx: SkillContext) -> StrategicBriefOutput:
        # 1. Read files from workspace
        sources = read_markdown_files(ctx.workspace_path, input.max_files)
        
        # 2. Build LLM prompt with file contents
        prompt = build_synthesis_prompt(input.prompt, sources, input.focus_areas)
        
        # 3. Call LLM for actual synthesis
        response = ctx.provider.complete(prompt, schema=BriefSchema)
        
        # 4. Return structured output with citations
        return StrategicBriefOutput(
            success=True,
            summary=f"Generated brief from {len(sources)} sources",
            brief_md=response.markdown,
            brief_json=response.structured,
            sources=sources,
            citations=response.citations,
        )
```

---

## Acceptance criteria (Definition of Done)
- [ ] Skill contract documented and reviewed
- [ ] Base skill class/protocol implemented
- [ ] At least one skill uses LLM synthesis (not just file listing)
- [ ] Input/output schemas enforced via Pydantic
- [ ] Registry updated to support new contract
- [ ] Existing stubs marked clearly as stubs (or removed)
- [ ] Tests cover new skill execution path
- [ ] CI/local checks pass

---

## Implementation notes

### Phase 1: Contract definition
- Define `Skill` protocol/base class
- Define `SkillContext` for runtime injection
- Define input/output base schemas

### Phase 2: Migrate strategic_brief
- Add actual LLM call for synthesis
- Use Pydantic schemas throughout
- Produce proper citations with excerpts

### Phase 3: Clean up registry
- Update registry to handle new contract
- Mark stubs clearly
- Add schema introspection for `ag skills show <name>`

---

## Risks
- **Breaking change:** New skill signature won't match current registry
- **Migration burden:** Existing playbooks may need updates
- **Scope creep:** Easy to over-engineer skill system

Mitigations:
- Support both old and new signatures during transition
- Keep v0 stubs working for playbook tests
- Time-box design phase

---

## Related
- **SKILLS_ARCHITECTURE_0.1.md** — Primary design reference for this AF
- AF0048 (Strategic brief skill) — will be evolved
- AF0059 (Playbooks list) — related discovery
- BUG0011 (workspace name leak) — skills need workspace context
- AF0058 (Workspace restructure) — skills need workspace path abstraction

---

## Documentation impact
This is an **architecture-level change** that will likely require:
- **ADR (required):** Document decisions on skill contract, LLM access pattern, schema enforcement
- **ARCHITECTURE.md:** Add/update Skills section with new framework design
- **CLI_REFERENCE.md:** Update `ag skills` commands with schema information
- **FOUNDATION_MANUAL.md:** Potentially add skill development guidelines
- **README.md:** Update if skill invocation syntax changes

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF0060
- **PR:** #<number>
- **Author:** <name>
- **Date:** YYYY-MM-DD
- **Branch:** feat/skill-framework
- **Risk level:** P1
- **Runtime mode used for verification:** llm

---

## 2) Acceptance criteria verification
(Copy AC list and mark when done)

---

## 3) What changed (file-level)
(Fill when done)

---

## 4) Architecture alignment (mandatory)
- **Layering:** Skills layer sits between CLI/playbooks and providers
- Skills own their I/O schemas; core owns execution context

