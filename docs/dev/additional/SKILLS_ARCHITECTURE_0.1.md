# Skills & Playbooks Architecture Proposal
# Version: 0.1
# Status: Draft
# Date: 2026-03-06
# Author: Jacob (via Kai review)

---

## Executive Summary

This document proposes a **bounded autonomy** architecture for skills and playbooks in the ag_foundation system. The core principle: **humans define WHAT, agents decide HOW**.

- **Skills** are atomic, LLM-powered capabilities with strict input/output schemas
- **Playbooks** define execution order and data flow between skills
- **Agents** have autonomy *within* skill execution, not over system structure

---

## 1. Problem Statement

### Current State
```python
# Current skill signature — tells us nothing
SkillFn = Callable[[dict[str, Any]], tuple[bool, str, dict[str, Any]]]
```

Issues:
1. No input validation — skills receive untyped dicts
2. No output schema — consumers can't trust result structure
3. No LLM integration pattern — skills can't easily call providers
4. No evidence model — skills don't produce verifiable reasoning
5. Unclear relationship between skills and playbooks

### Desired State
- Skills are well-defined, testable units with known contracts
- Playbooks compose skills predictably
- Agent autonomy is bounded and verifiable
- Evidence trail exists for every decision

---

## 2. Architecture Overview

### 2.1 The Autonomy Spectrum

```
RIGID                                                    AUTONOMOUS
(human decides everything)                    (agent decides everything)
    │                                                         │
    ▼                                                         ▼
┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
│ Script │  │Playbook│  │ Guided │  │ Goals  │  │  Full  │
│        │  │        │  │ Agent  │  │  Only  │  │ Agent  │
└────────┘  └────────┘  └────────┘  └────────┘  └────────┘
                 ▲
                 │
           WE ARE HERE
           (Phase 1)
```

**Recommendation:** Start with fixed playbooks, agent autonomy within skill execution.

### 2.2 Responsibility Matrix

| Decision | Decided By | Rationale |
|----------|------------|-----------|
| Which skills exist | Human (compile-time) | Security boundary — no runtime skill creation |
| Playbook structure | Human (definition-time) | Predictability — same playbook = same steps |
| Execution order | Playbook (static) | Testability — deterministic execution |
| Skill parameters | Agent (runtime) | Flexibility — agent interprets task |
| Retry decisions | Agent (bounded) | Adaptability — agent judges success |
| Output content | Agent (schema-bounded) | Creativity — agent generates within constraints |
| Resource limits | Human (budget) | Cost control — hard limits enforced |

### 2.3 Layer Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      USER REQUEST                           │
│                 "Review my Python code"                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    RUNTIME LAYER                            │
│  • Selects playbook (or user specifies)                     │
│  • Enforces budgets                                         │
│  • Records trace                                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   PLAYBOOK LAYER                            │
│  • Defines step sequence                                    │
│  • Maps data between steps                                  │
│  • Handles step failures                                    │
│                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                 │
│  │ Step 1  │───►│ Step 2  │───►│ Step 3  │                 │
│  │summarize│    │ review  │    │ format  │                 │
│  └─────────┘    └─────────┘    └─────────┘                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    SKILL LAYER                              │
│  • Validates input against schema                           │
│  • Calls LLM via provider                                   │
│  • Produces evidence                                        │
│  • Returns structured output                                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   PROVIDER LAYER                            │
│  • OpenAI, Claude, Local stubs                              │
│  • Token counting                                           │
│  • Rate limiting                                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Schema Definitions

### 3.1 Contract vs Schema Distinction

| Term | Definition | Enforcement |
|------|------------|-------------|
| **Schema** | Data shape (Pydantic model) | Runtime validation |
| **Contract** | Behavioral promise (docs + tests) | Test assertions |

A contract *includes* schemas but also covers preconditions, postconditions, and invariants.

### 3.2 Core Schemas

#### SkillDefinition — What a skill IS

```python
class SkillDefinition(BaseModel):
    """Metadata about a skill's interface."""
    
    name: str = Field(..., min_length=1, description="Unique skill identifier")
    version: str = Field(..., pattern=r"^\d+\.\d+$", description="Skill version")
    description: str = Field(..., description="What the skill does")
    
    # Schema references (type objects, not instances)
    input_schema: type[BaseModel]
    output_schema: type[BaseModel]
    
    # Capabilities
    requires_llm: bool = Field(default=True, description="Does skill need LLM?")
    produces_artifacts: list[str] = Field(
        default_factory=list, 
        description="Artifact types produced (e.g., ['brief.md'])"
    )
    
    # Constraints
    typical_tokens: int = Field(default=1000, description="Expected token usage")
    timeout_seconds: int = Field(default=60, description="Default timeout")
```

#### SkillContext — What skills have access to

```python
@dataclass
class SkillContext:
    """Dependencies injected into skill execution."""
    
    provider: BaseProvider      # LLM access
    workspace: Workspace        # File I/O (inputs/, runs/)
    recorder: Recorder          # Evidence capture
    run_id: str                 # Current run identifier
    parameters: dict[str, Any]  # Runtime config overrides
```

#### SkillResult — What skills return

```python
class Evidence(BaseModel):
    """A piece of reasoning evidence."""
    type: str = Field(..., description="Evidence type: citation, reasoning, observation")
    content: str = Field(..., description="Evidence content")
    source: str | None = Field(default=None, description="Source reference")

class ArtifactRef(BaseModel):
    """Reference to a produced artifact."""
    name: str = Field(..., description="Artifact filename")
    path: str = Field(..., description="Relative path in workspace")
    mime_type: str = Field(default="application/json", description="Content type")

class SkillResult(BaseModel):
    """Standard skill output structure."""
    
    success: bool = Field(..., description="Did skill complete successfully?")
    output: BaseModel = Field(..., description="Skill-specific output (validated)")
    summary: str = Field(..., description="Human-readable summary")
    
    evidence: list[Evidence] = Field(default_factory=list, description="Reasoning trail")
    artifacts: list[ArtifactRef] = Field(default_factory=list, description="Produced files")
    
    tokens_used: int = Field(default=0, description="LLM tokens consumed")
    duration_ms: int = Field(default=0, description="Execution time")
```

#### Skill Protocol — The contract

```python
class Skill(Protocol):
    """Contract: What every skill must implement."""
    
    @property
    def definition(self) -> SkillDefinition:
        """Return skill metadata and schemas."""
        ...
    
    def execute(
        self, 
        input: BaseModel,      # Validated against definition.input_schema
        context: SkillContext  # Injected dependencies
    ) -> SkillResult:          # Must contain output matching definition.output_schema
        """Execute the skill."""
        ...
```

### 3.3 Playbook Schemas

#### PlaybookStep — Single step definition

```python
class InputMapping(BaseModel):
    """Maps playbook context to skill input fields."""
    field: str = Field(..., description="Skill input field name")
    source: str = Field(..., description="JSONPath in playbook context")
    # Example: source="$.steps.summarize.output.summary"

class PlaybookStep(BaseModel):
    """A single step in playbook execution."""
    
    step_id: str = Field(..., description="Unique step identifier")
    skill_name: str = Field(..., description="Skill to invoke")
    
    input_mapping: list[InputMapping] = Field(
        default_factory=list,
        description="How to populate skill input from context"
    )
    output_key: str = Field(..., description="Key to store result in context")
    
    # Control flow
    required: bool = Field(default=True, description="Fail playbook if step fails?")
    retry_count: int = Field(default=0, ge=0, description="Max retries")
    on_failure: str | None = Field(default=None, description="Step to jump to on failure")
```

#### Playbook — Workflow definition

```python
class Playbook(BaseModel):
    """A workflow composing multiple skills."""
    
    playbook_version: str = Field(default="0.2", pattern=r"^\d+\.\d+$")
    name: str = Field(..., min_length=1, description="Playbook identifier")
    version: str = Field(..., description="Playbook version")
    description: str = Field(default="", description="What this playbook does")
    
    # Execution
    steps: list[PlaybookStep] = Field(..., min_length=1, description="Ordered steps")
    
    # Budgets
    max_tokens: int = Field(default=10000, description="Total token budget")
    max_duration_seconds: int = Field(default=300, description="Total time budget")
    
    # Metadata
    tags: list[str] = Field(default_factory=list, description="Categorization tags")
```

---

## 4. Execution Model

### 4.1 Playbook Execution Flow

```python
def execute_playbook(
    playbook: Playbook, 
    initial_inputs: dict,
    context: RuntimeContext
) -> RunTrace:
    """Execute a playbook, returning full trace."""
    
    # Initialize execution context
    exec_context = {
        "inputs": initial_inputs,
        "steps": {},
        "metadata": {"playbook": playbook.name, "start_time": now()}
    }
    
    tokens_used = 0
    
    for step in playbook.steps:
        # Check budgets
        if tokens_used >= playbook.max_tokens:
            raise BudgetExceededError("Token budget exhausted")
        
        # Get skill
        skill = registry.get(step.skill_name)
        if skill is None:
            raise SkillNotFoundError(step.skill_name)
        
        # Map inputs from context
        skill_input_dict = resolve_input_mapping(step.input_mapping, exec_context)
        
        # Validate input against skill's schema
        validated_input = skill.definition.input_schema(**skill_input_dict)
        
        # Execute with retries
        result = execute_with_retry(
            skill=skill,
            input=validated_input,
            context=build_skill_context(context),
            max_retries=step.retry_count
        )
        
        # Validate output
        if not isinstance(result.output, skill.definition.output_schema):
            raise SchemaViolationError("Skill output doesn't match schema")
        
        # Store in context
        exec_context["steps"][step.output_key] = result
        tokens_used += result.tokens_used
        
        # Handle failure
        if not result.success and step.required:
            if step.on_failure:
                # Jump to failure handler step
                continue
            raise StepFailedError(step.step_id)
    
    return build_trace(exec_context)
```

### 4.2 Skill Execution Flow

```python
class SummarizeSkill:
    """Example skill implementation."""
    
    @property
    def definition(self) -> SkillDefinition:
        return SkillDefinition(
            name="summarize",
            version="1.0",
            description="Summarize documents or code",
            input_schema=SummarizeInput,
            output_schema=SummarizeOutput,
            requires_llm=True,
            produces_artifacts=["summary.md"]
        )
    
    def execute(self, input: SummarizeInput, context: SkillContext) -> SkillResult:
        # 1. Read files from workspace
        files_content = self._read_files(input.files, context.workspace)
        
        # 2. Build prompt
        prompt = self._build_prompt(files_content, input.focus_areas)
        
        # 3. Call LLM
        response = context.provider.complete(prompt)
        
        # 4. Parse response into output schema
        output = SummarizeOutput(
            summary=response.content,
            key_points=self._extract_points(response.content)
        )
        
        # 5. Write artifact
        artifact_path = self._write_artifact(output, context)
        
        # 6. Record evidence
        evidence = [
            Evidence(type="reasoning", content=f"Analyzed {len(input.files)} files"),
            Evidence(type="citation", content=response.content[:200], source="llm")
        ]
        
        # 7. Return structured result
        return SkillResult(
            success=True,
            output=output,
            summary=f"Summarized {len(input.files)} files",
            evidence=evidence,
            artifacts=[ArtifactRef(name="summary.md", path=artifact_path)],
            tokens_used=response.usage.total_tokens
        )
```

---

## 5. Rationale

### 5.1 Why Bounded Autonomy?

| Alternative | Problem |
|-------------|---------|
| Full scripting | No AI benefit — just automation |
| Full autonomy | Unpredictable, expensive, hard to debug |
| **Bounded autonomy** | Predictable structure, flexible execution |

### 5.2 Why Strict Schemas?

| Benefit | Explanation |
|---------|-------------|
| **Testability** | Can generate test cases from schemas |
| **Verifiability** | Output can be validated automatically |
| **Documentation** | Schemas are self-documenting |
| **Composability** | Step N's output type-checks against Step N+1's input |
| **Debugging** | Know exactly what went in and came out |

### 5.3 Why Separate Skills from Playbooks?

| Concern | Skills Handle | Playbooks Handle |
|---------|---------------|------------------|
| Single responsibility | ✓ One task | Composition |
| Reusability | ✓ Used in multiple playbooks | Workflow-specific |
| Testing | ✓ Unit testable | Integration testable |
| LLM interaction | ✓ Direct | Indirect |

### 5.4 Why Evidence Required?

Every agent decision must be traceable:
- **Debugging:** Why did it produce X?
- **Auditing:** What information did it use?
- **Improvement:** Where did it go wrong?
- **Trust:** Users can verify reasoning

---

## 6. Implementation Plan

### 6.1 Phase 1: Foundation (Sprint 06)

**AF-0058: Workspace folder restructure**
- Create `inputs/` and `runs/<id>/` structure
- Skills read from `inputs/`, write to `runs/<id>/artifacts/`

**AF-0060: Skill definition framework**
- Implement `SkillDefinition`, `SkillContext`, `SkillResult` schemas
- Implement `Skill` protocol
- Update `SkillRegistry` to use new definitions
- Create `BaseSkill` helper class

**AF-0063: Schema inventory**
- Document all 19+ existing Pydantic models
- Identify overlaps and gaps

**AF-0013: Contract inventory hardening**
- Reconcile docs with implementation
- Add automated drift detection

### 6.2 Phase 2: First Skills (Sprint 07)

**AF-0065: First skill set**
- Implement 2 real skills using new framework:
  - `summarize` — summarize documents
  - `explain_code` — explain what code does
- Create default playbook chaining them

**AF-0066: E2E integration test**
- Test full flow: skill → verifier → trace → artifact
- Mock provider for CI, real provider for manual testing

**AF-0062: Trace LLM model tracking**
- Record which model was used
- Track token usage per step

### 6.3 Phase 3: Expansion (Sprint 08+)

- Additional skills: `code_review`, `generate_tests`, `refactor`
- Playbook library with multiple workflows
- Agent-assisted playbook selection (Phase 2 autonomy)

---

## 7. AF Slicing Recommendation

### Revised Sprint 06 Scope

| Order | AF | Deliverable | Risk |
|-------|-----|-------------|------|
| 1 | AF-0058 | Workspace restructure | Low — isolated change |
| 2 | AF-0060 | Skill framework schemas | Medium — core abstraction |
| 3 | AF-0063 | Schema inventory doc | Low — documentation |
| 4 | AF-0013 | Contract hardening | Low — reconciliation |

### New AF Suggestions

| ID | Title | Scope | Sprint |
|----|-------|-------|--------|
| AF-0067 | Playbook v0.2 schema | Update Playbook with InputMapping, budgets | 06 (if time) |
| AF-0068 | BaseSkill helper class | Reduce boilerplate for skill implementations | 07 |
| AF-0069 | Skill testing utilities | Mock provider, fixtures for skill tests | 07 |

### Dependencies

```
AF-0058 (workspace)
    │
    ├──► AF-0060 (skill framework)
    │        │
    │        ├──► AF-0065 (first skills)
    │        │        │
    │        │        └──► AF-0066 (E2E test)
    │        │
    │        └──► AF-0067 (playbook v0.2)
    │
    └──► AF-0063 (schema inventory)
             │
             └──► AF-0013 (contract hardening)
```

---

## 8. Open Questions

1. **Playbook storage:** Files (YAML/JSON) or code (Python)?
   - Recommendation: Start with Python, add YAML later for user-defined playbooks

2. **Skill versioning:** How to handle breaking changes?
   - Recommendation: Additive-only within major version, new skill name for breaking changes

3. **Error recovery:** How detailed should `on_failure` handling be?
   - Recommendation: Simple step jumps for v1, more sophisticated for v2

4. **Provider selection:** Per-skill or per-playbook?
   - Recommendation: Per-playbook default, per-step override possible

---

## 9. Success Criteria

This architecture is successful if:

1. **New skills take < 1 hour to implement** — framework handles boilerplate
2. **All skill outputs are verifiable** — schema validation catches errors
3. **Playbook changes don't require code changes** — composition is declarative
4. **Every decision has evidence** — traces are auditable
5. **Tests are deterministic** — mock provider enables CI

---

## 10. References

- [ARCHITECTURE.md](../../../ARCHITECTURE.md) — System overview
- [ARCHITECTURE.md Section 3.4.2](../../../ARCHITECTURE.md#342-concept-relationships) — Concept relationship matrix (schemas ↔ contracts ↔ skills ↔ playbooks)
- [SCHEMA_INVENTORY.md](SCHEMA_INVENTORY.md) — Complete Pydantic model inventory (AF-0063)
- [CONTRACT_INVENTORY.md](CONTRACT_INVENTORY.md) — Protocol interface inventory (AF-0013)
- [AF-0060](../backlog/items/AF0060_DONE_skill_definition_framework.md) — Skill framework AF
- [AF-0065](../backlog/items/AF0065_PROPOSED_first_skill_set.md) — First skills AF
- [interfaces.py](../../../src/ag/core/interfaces.py) — Current protocols
- [playbook.py](../../../src/ag/core/playbook.py) — Current playbook schema

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-03-06 | Initial draft |
