# BACKLOG ITEM — AF0065 — first_skill_set
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
- **ID:** AF0065
- **Type:** Feature
- **Status:** DONE
- **Priority:** P0
- **Area:** Skills
- **Owner:** Kai
- **Target sprint:** Sprint07
- **Depends on:** AF0060 (skill definition framework), AF0058 (workspace restructure)

---

## Problem
The current codebase has no production-ready skills:

1. **strategic_brief is deprecated** — It doesn't use LLM, just lists files. Not a model for future skills.
2. **All other skills are stubs** — 11 of 12 skills return hardcoded values
3. **No playbook composition** — No example of skills chaining together in a pipeline
4. **No LLM integration pattern** — No reference implementation for provider injection

We need a complete skill set and playbook to validate the framework from AF0060.

---

## Goal
Implement the **summarize_v0** playbook with **three individual skills**:

| Order | Skill | Purpose |
|:--:|---|---|
| 1 | `load_documents` | Read files from workspace matching glob patterns |
| 2 | `summarize_docs` | Call LLM to summarize document contents |
| 3 | `emit_result` | Store structured output as artifact |

This provides:
- **Playbook composition** — Three skills chained in sequence
- **LLM integration** — Real provider call in `summarize_docs`
- **Reference implementation** — Pattern for future skill development

**Important:** This work starts fresh. The existing `strategic_brief` skill is NOT a template.

---

## Non-goals
- Migrating or reusing `strategic_brief` code
- Complex multi-agent orchestration
- External tool integration (web search, etc.)
- Streaming responses

---

## Acceptance criteria (Definition of Done)
- [ ] 3 skills implemented: `load_documents`, `summarize_docs`, `emit_result`
- [ ] `summarize_docs` calls LLM via provider abstraction
- [ ] Skills produce proper evidence/citations
- [ ] `emit_result` stores artifact to workspace
- [ ] `summarize_v0` playbook chains all 3 skills
- [ ] All skills registered in skill registry
- [ ] Unit tests for each skill (mocked provider)
- [ ] Integration test with real provider (manual)
- [ ] `ruff check src tests` passes
- [ ] `pytest -W error` passes
- [ ] Coverage threshold maintained

---

## Skill definitions

### Skill 1: `load_documents`
**Purpose:** Read files from workspace matching glob patterns.

```python
# Input schema
class LoadDocumentsInput(SkillInput):
    patterns: list[str] = ["**/*.md"]  # Glob patterns
    max_files: int = 10

# Output schema
class LoadDocumentsOutput(SkillOutput):
    documents: list[Document]  # List of {path, content}
    file_count: int
    total_bytes: int
```

**Logic:**
1. Resolve workspace inputs path
2. Match files using glob patterns
3. Read file contents (respect max_files limit)
4. Return structured document list

### Skill 2: `summarize_docs`
**Purpose:** Call LLM to summarize document contents.

```python
# Input schema
class SummarizeDocsInput(SkillInput):
    documents: list[Document]  # From load_documents
    prompt: str  # User's summarization request
    max_tokens: int = 2000

# Output schema
class SummarizeDocsOutput(SkillOutput):
    summary: str
    key_points: list[str]
    source_count: int
    sources: list[str]  # File paths used
```

**Logic:**
1. Build LLM prompt with document contents
2. Call LLM via `context.provider.complete()`
3. Parse response into structured output
4. Include source file references as citations

### Skill 3: `emit_result`
**Purpose:** Store structured output as workspace artifact.

```python
# Input schema
class EmitResultInput(SkillInput):
    data: dict  # The result to store
    artifact_name: str = "summary.json"
    artifact_type: str = "application/json"

# Output schema
class EmitResultOutput(SkillOutput):
    artifact_id: str
    artifact_path: str
    bytes_written: int
```

**Logic:**
1. Serialize data to JSON
2. Create artifact via `context.recorder.record_artifact()`
3. Return artifact reference

---

## Playbook definition

```python
SUMMARIZE_V0 = Playbook(
    playbook_version="0.1",
    name="summarize_v0",
    version="1.0.0",
    description="Summarize documents from workspace using LLM",
    reasoning_modes=[ReasoningMode.DIRECT],
    budgets=Budgets(
        max_steps=5,
        max_tokens=None,
        max_duration_seconds=120,
    ),
    steps=[
        PlaybookStep(
            step_id="step_0",
            name="load_docs",
            step_type=PlaybookStepType.SKILL,
            skill_name="load_documents",
            description="Read files matching patterns from workspace",
            required=True,
            retry_count=0,
        ),
        PlaybookStep(
            step_id="step_1",
            name="summarize",
            step_type=PlaybookStepType.SKILL,
            skill_name="summarize_docs",
            description="Call LLM to summarize document contents",
            required=True,
            retry_count=1,
        ),
        PlaybookStep(
            step_id="step_2",
            name="emit",
            step_type=PlaybookStepType.SKILL,
            skill_name="emit_result",
            description="Store summary as workspace artifact",
            required=True,
            retry_count=0,
        ),
    ],
    metadata={
        "author": "ag_foundation",
        "stability": "experimental",
        "af_item": "AF-0065",
    },
)
```

---

## Runtime pipeline flow

### High-level execution
```
┌─────────────────────────────────────────────────────────────────┐
│                     SUMMARIZE_V0 PLAYBOOK                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  step_0: load_docs                                              │
│    ├── skill: load_documents                                    │
│    ├── action: Read files matching patterns from workspace      │
│    └── output: documents[]                                      │
│                         │                                       │
│                         ▼                                       │
│  step_1: summarize                                              │
│    ├── skill: summarize_docs                                    │
│    ├── action: Single LLM call to summarize all documents       │
│    └── output: summary, key_points[], sources[]                 │
│                         │                                       │
│                         ▼                                       │
│  step_2: emit                                                   │
│    ├── skill: emit_result                                       │
│    ├── action: Store summary as artifact                        │
│    └── output: artifact_id                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Detailed runtime flow with all components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  USER INPUT                                                                 │
│  > ag run --workspace myproject --playbook summarize_v0                     │
│    "Summarize all markdown files in docs/"                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1: NORMALIZER (V0Normalizer.normalize)                                │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Input:  prompt="Summarize all markdown files in docs/"                     │
│          workspace="myproject", playbook="summarize_v0"                     │
│                                                                             │
│  Actions:                                                                   │
│    • Validate prompt is non-empty                                           │
│    • Validate workspace exists (required, no implicit creation)             │
│    • Parse execution mode (default: supervised)                             │
│    • Store playbook preference                                              │
│                                                                             │
│  Output: TaskSpec                                                           │
│    {                                                                        │
│      prompt: "Summarize all markdown files in docs/",                       │
│      workspace_id: "myproject",                                             │
│      mode: ExecutionMode.SUPERVISED,                                        │
│      playbook_preference: "summarize_v0",                                   │
│      budgets: Budgets(max_steps=10, max_duration_seconds=300),              │
│      constraints: Constraints()                                             │
│    }                                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 2: PLANNER (V0Planner.plan)                                           │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Input:  TaskSpec (from normalizer)                                         │
│                                                                             │
│  Actions:                                                                   │
│    • Check playbook_preference: "summarize_v0"                              │
│    • Look up in registry: get_playbook("summarize_v0")                      │
│    • Found → return SUMMARIZE_V0 playbook                                   │
│    • (If not found, would fall back to DEFAULT_V0)                          │
│                                                                             │
│  Output: Playbook (SUMMARIZE_V0)                                            │
│    {                                                                        │
│      name: "summarize_v0",                                                  │
│      version: "1.0.0",                                                      │
│      budgets: Budgets(max_steps=5, max_duration_seconds=120),               │
│      steps: [                                                               │
│        { step_id: "step_0", skill_name: "load_documents" },                 │
│        { step_id: "step_1", skill_name: "summarize_docs" },                 │
│        { step_id: "step_2", skill_name: "emit_result" }                     │
│      ]                                                                      │
│    }                                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 3: ORCHESTRATOR (V0Orchestrator.run)                                  │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Input:  TaskSpec + Playbook                                                │
│                                                                             │
│  Actions:                                                                   │
│    • Initialize RunTrace with new run_id                                    │
│    • Create WorkspaceSource reference                                       │
│    • Iterate through playbook.steps in order                                │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  STEP 3a: Execute "step_0" (load_documents)                         │    │
│  │  ─────────────────────────────────────────────────────────────────  │    │
│  │                                                                     │    │
│  │  → EXECUTOR (V0Executor.execute)                                    │    │
│  │    • Resolve skill: get_skill("load_documents")                     │    │
│  │    • Build SkillContext with workspace path                         │    │
│  │    • Build LoadDocumentsInput from task prompt (parse patterns)     │    │
│  │    • Call skill.execute(context, input)                             │    │
│  │                                                                     │    │
│  │    ┌─────────────────────────────────────────────────────────────┐  │    │
│  │    │  SKILL: load_documents.execute()                            │  │    │
│  │    │  ─────────────────────────────────────────────────────────  │  │    │
│  │    │  1. Parse glob patterns: ["docs/**/*.md"]                   │  │    │
│  │    │  2. Resolve workspace inputs path                           │  │    │
│  │    │  3. Match files using glob                                  │  │    │
│  │    │  4. Read file contents (up to max_files)                    │  │    │
│  │    │  5. Return LoadDocumentsOutput                              │  │    │
│  │    │     {                                                       │  │    │
│  │    │       documents: [{path: "docs/README.md", content: "..."}],│  │    │
│  │    │       file_count: 5,                                        │  │    │
│  │    │       total_bytes: 12480                                    │  │    │
│  │    │     }                                                       │  │    │
│  │    └─────────────────────────────────────────────────────────────┘  │    │
│  │                                                                     │    │
│  │  → VERIFIER: Validate LoadDocumentsOutput schema                    │    │
│  │  → RECORDER: Record step_0 in RunTrace                              │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                         │                                                   │
│                         ▼                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  STEP 3b: Execute "step_1" (summarize_docs)                         │    │
│  │  ─────────────────────────────────────────────────────────────────  │    │
│  │                                                                     │    │
│  │  → EXECUTOR (V0Executor.execute)                                    │    │
│  │    • Resolve skill: get_skill("summarize_docs")                     │    │
│  │    • Build SkillContext with LLM provider                           │    │
│  │    • Build SummarizeDocsInput from step_0 output + task prompt      │    │
│  │    • Call skill.execute(context, input)                             │    │
│  │                                                                     │    │
│  │    ┌─────────────────────────────────────────────────────────────┐  │    │
│  │    │  SKILL: summarize_docs.execute()                            │  │    │
│  │    │  ─────────────────────────────────────────────────────────  │  │    │
│  │    │  1. Build LLM prompt with document contents                 │  │    │
│  │    │  2. Call LLM: context.provider.complete(prompt)             │  │    │
│  │    │  3. Parse LLM response into structured output               │  │    │
│  │    │  4. Return SummarizeDocsOutput                              │  │    │
│  │    │     {                                                       │  │    │
│  │    │       summary: "The docs folder contains architecture...",  │  │    │
│  │    │       key_points: ["Point 1", "Point 2", ...],              │  │    │
│  │    │       source_count: 5,                                      │  │    │
│  │    │       sources: ["docs/README.md", "docs/ARCH.md", ...]      │  │    │
│  │    │     }                                                       │  │    │
│  │    └─────────────────────────────────────────────────────────────┘  │    │
│  │                                                                     │    │
│  │  → VERIFIER: Validate SummarizeDocsOutput schema                    │    │
│  │  → RECORDER: Record step_1 in RunTrace                              │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                         │                                                   │
│                         ▼                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  STEP 3c: Execute "step_2" (emit_result)                            │    │
│  │  ─────────────────────────────────────────────────────────────────  │    │
│  │                                                                     │    │
│  │  → EXECUTOR (V0Executor.execute)                                    │    │
│  │    • Resolve skill: get_skill("emit_result")                        │    │
│  │    • Build SkillContext with recorder                               │    │
│  │    • Build EmitResultInput from step_1 output                       │    │
│  │    • Call skill.execute(context, input)                             │    │
│  │                                                                     │    │
│  │    ┌─────────────────────────────────────────────────────────────┐  │    │
│  │    │  SKILL: emit_result.execute()                               │  │    │
│  │    │  ─────────────────────────────────────────────────────────  │  │    │
│  │    │  1. Serialize data to JSON                                  │  │    │
│  │    │  2. Call context.recorder.record_artifact()                 │  │    │
│  │    │  3. Return EmitResultOutput                                 │  │    │
│  │    │     {                                                       │  │    │
│  │    │       artifact_id: "art-abc123",                            │  │    │
│  │    │       artifact_path: "summary.json",                        │  │    │
│  │    │       bytes_written: 1248                                   │  │    │
│  │    │     }                                                       │  │    │
│  │    └─────────────────────────────────────────────────────────────┘  │    │
│  │                                                                     │    │
│  │  → VERIFIER: Validate EmitResultOutput schema                       │    │
│  │  → RECORDER: Record step_2 in RunTrace, store artifact              │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  • All steps completed successfully                                         │
│  • Set FinalStatus.SUCCESS                                                  │
│  • Finalize RunTrace                                                        │
│                                                                             │
│  Output: RunTrace                                                           │
│    {                                                                        │
│      run_id: "abc-123-...",                                                 │
│      status: "success",                                                     │
│      steps: [                                                               │
│        Step(step_id="step_0", skill="load_documents", status="success"),    │
│        Step(step_id="step_1", skill="summarize_docs", status="success"),    │
│        Step(step_id="step_2", skill="emit_result", status="success")        │
│      ],                                                                     │
│      artifacts: [ Artifact(name="summary.json", ...) ]                      │
│    }                                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  OUTPUT TO USER                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Run completed: abc-123-... (success)                                       │
│  Workspace: myproject                                                       │
│  Artifact: summary.json (1.2 KB)                                            │
│                                                                             │
│  > ag artifact show abc-123-... summary.json                                │
│  {                                                                          │
│    "summary": "The docs folder contains architecture documentation...",     │
│    "key_points": [                                                          │
│      "System uses Protocol-based interfaces",                               │
│      "Playbooks define execution workflows",                                │
│      "Skills implement atomic capabilities"                                 │
│    ],                                                                       │
│    "source_count": 5,                                                       │
│    "sources": ["docs/README.md", "docs/ARCHITECTURE.md", ...]               │
│  }                                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component responsibilities

| Component | Protocol | Role | Summarize Playbook Example |
|---|---|---|---|
| **Normalizer** | `Normalizer` | Validate input, create TaskSpec | Ensures workspace exists, stores "summarize_v0" preference |
| **Planner** | `Planner` | Select playbook | Looks up `SUMMARIZE_V0` from registry |
| **Orchestrator** | `Orchestrator` | Coordinate step execution | Loops through 3 steps, calls Executor for each |
| **Executor** | `Executor` | Run individual skills | Invokes `load_documents`, `summarize_docs`, `emit_result` |
| **Verifier** | `Verifier` | Validate outputs | Checks each skill output against Pydantic schema |
| **Recorder** | `Recorder` | Persist traces/artifacts | Writes to `~/.ag/workspaces/myproject/db.sqlite` |

---

## File structure after implementation

```
src/ag/skills/
├── __init__.py
├── base.py               # Skill ABC, SkillContext (from AF0060)
├── registry.py           # get_skill(), list_skills()
├── load_documents.py     # NEW: load_documents skill
├── summarize_docs.py     # NEW: summarize_docs skill
└── emit_result.py        # NEW: emit_result skill
```

Note: Playbook file goes to `src/ag/playbooks/summarize_v0.py` per AF0068.

---

## Risks

| Risk | Mitigation |
|------|------------|
| AF0060 design changes | AF0060 is DONE — framework is stable |
| Provider abstraction gaps | Validate provider interface during implementation |
| Step output chaining | Define clear input/output contracts between skills |

---

## Related
- **AF0060** (Skill definition framework) — **prerequisite, DONE**
- **AF0058** (Workspace folder restructure) — **prerequisite, DONE**
- **AF0068** (Skills/playbooks folder restructure) — implements new folder structure
- **AF0066** (E2E integration test) — validates this work

---

## Documentation impact

> **NOTE:** After implementation, the following documentation MUST be updated:

1. **ARCHITECTURE.md**
   - Add Section 3.5: "Runtime Pipeline Flow"
   - Include the detailed execution diagram from this AF
   - Document component responsibilities table

2. **SKILLS_ARCHITECTURE_0.1.md**
   - Add `load_documents`, `summarize_docs`, `emit_result` to skill catalog
   - Include skill input/output schema examples

3. **docs/dev/additional/SCHEMA_INVENTORY.md**
   - Add new schemas: `LoadDocumentsInput`, `LoadDocumentsOutput`, etc.

4. **docs/dev/additional/CONTRACT_INVENTORY.md**
   - Verify Skill protocol implementation references

5. **CLI_REFERENCE.md**
   - Add `summarize_v0` playbook to playbook list
   - Add usage example

---

# Completion section (fill when done)

Pending completion.

