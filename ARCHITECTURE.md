# ag_foundation — Architecture
# Version number: v0.4

This document defines the **core architecture** for ag_foundation: a modular, inspectable **agent network runtime** that can plan, execute, verify, and record runs.

**Near-term focus:** CLI-first developer workflow to build the core agent-network capability.  
**Later integrations:** IoT in a defined space, plus web/app interfaces. These are treated as **Interface Adapters** that plug into the same core pipeline.

---

## 1. Goals and non-goals

### Goals
- **Agent network behavior:** decomposition, delegation, multi-step execution.
- **Modular core runtime:** planner/orchestrator/executor/verifier/recorder are swappable modules behind stable interfaces.
- **Modular skills/plugins:** tools/connectors added without touching core.
- **Truthful observability:** user-visible labels derive from **run traces**, not assumptions.
- **Safety hooks:** permission + confirmation points exist even before IoT.
- **Interface-agnostic core:** CLI now; internal API and event ingestion later, without core rewrites.
- **Optional intelligence modules:** RAG + MLP are **interfaces-first**; implementations later.

### Non-goals (for now)
- Implementing IoT hardware integrations, device SDKs
- Providing a public/stable external API
- Multi-tenant SaaS deployment, billing, enterprise governance suite
- Full policy engine (we define hook points + minimal gating only)

---

## 2. System model (core concepts)

- **Workspace**: isolated project boundary for runs, artifacts, memory, configs.
- **TaskSpec**: normalized representation of a request (input → structured task).
- **Run**: one execution instance of a TaskSpec.
- **RunTrace**: record of what happened (steps, tool calls, evidence, errors, retries).
- **Artifact**: produced files/objects (reports, exports, structured outputs).
- **Skill**: pluggable capability (tool wrapper, connector, transformer, generator).
- **Agent (role)**: a responsibility bundle used by playbooks (planner/researcher/writer/critic/operator).
- **Playbook**: declarative orchestration recipe specifying roles, step graph, reasoning modes, budgets.
- **Policy hooks**: decision points for permissions, confirmations, redaction, rate limits.

### Runtime modes
- **LLM mode (default end-user behavior)**: planning/execution uses LLM(s).
- **Manual mode (dev/test only)**: LLM calls disabled; execution uses mocks/stubs or constrained scaffolding for speed/cost control.

> Manual mode must remain dev/test-only. End-user behavior is LLM-first.

---

## 3. Layered architecture

### 3.1 Interface Layer (Adapters)
Adapters accept requests/events and **normalize** them into `TaskSpec`.

- **CLI Adapter** (now)
- **Internal API Adapter** (planned; mirrors CLI semantics)
- **Event Adapter** (planned; for IoT/sensors/streams)
- **UI Adapter** (planned; web/app)

**Contract:** adapters do not contain business logic; they produce `TaskSpec` + `RequestContext`.

### 3.2 Core Runtime (Modular Pipeline)
The kernel of execution, implemented as replaceable modules.
Each module lives in its own file (AF-0114) and evolves through versioned implementations.

1) **TaskSpec Normalizer**
- input/event → `TaskSpec`
- applies workspace defaults (budgets, policies, preferred playbooks)

2) **Planner**
- decomposes into a step graph
- selects agent roles/skills
- chooses playbook + reasoning modes
- **V0Planner (current):** deterministic registry lookup, requires explicit `--playbook`
- **V1Planner (Sprint 11):** LLM analyzes task + skill catalog → composes skill sequence
- **V2Planner (Sprint 13):** LLM composes mixed skill+playbook plans; playbooks as first-class plan steps
- **V3Planner (Sprint 15, ADR-0009):** adds feasibility assessment phase before plan generation; identifies capability gaps and prevents execution of tasks that can't be performed

3) **Orchestrator**
- executes the playbook step graph (sequence first; branching/parallel later)
- enforces budgets, retries, state transitions
- emits trace events
- **V0Orchestrator (current):** linear fire-and-forget loop, verification once at end
- **V1Orchestrator (planned, AF-0117):** per-step verification loop; calls Verifier after each step

4) **Executor**
- runs one step
- calls LLM(s) and/or skills/tools
- outputs step results + evidence
- **V0Executor (current):** calls `skill.execute()` and returns result unchecked
- **V1Executor (planned, AF-0116):** validates output against `SkillInfo.output_schema`; bounded retry on schema mismatch

5) **Verifier/Evaluator**
- checks acceptance criteria / quality thresholds
- can trigger repair loops within limits
- **V0Verifier (current):** end-of-run error scan only; no step awareness (BUG-0017)
- **V1Verifier (planned, AF-0115):** step-aware; respects required/optional; per-step pass/fail evidence

6) **Recorder**
- persists run trace + artifacts + summaries
- produces artifact index for CLI/API/UI retrieval
- **V0Recorder (current):** persists trace + artifacts to SQLite/filesystem
- **V1Recorder (planned, AF-0118):** adds structured verification evidence, retry history, per-step breakdown

> **Pipeline Manifest (AF-0120):** Every `RunTrace` includes a `pipeline` block recording which component versions executed the run (e.g., `V3Planner → V1Orchestrator → V0Executor → V1Verifier → V0Recorder`). This enables reproducibility — given a trace, you know the exact component mix.

#### 3.2.1 Implementation Map

All pipeline components have Protocol interfaces in `interfaces.py` and versioned implementations:

| Component | Protocol | V0 Implementation | V1+ Implementation | Primary File |
|-----------|----------|-------------------|-------------------|-------------|
| TaskSpec | — (schema) | `TaskSpec` | — | `task_spec.py` |
| Planner | `Planner` | `V0Planner` | `V1Planner` ✅, `V2Planner` ✅, `V3Planner` ✅ (AF-0121) | `planner.py` |
| Orchestrator | `Orchestrator` | `V0Orchestrator` | `V1Orchestrator` ✅ | `orchestrator.py` |
| Executor | `Executor` | `V0Executor` | `V1Executor` ✅ (AF-0116), `V2Executor` ✅ (AF-0124) | `executor.py` |
| Verifier | `Verifier` | `V0Verifier` | `V1Verifier` ✅ (AF-0115), `V2Verifier` ✅ (AF-0123) | `verifier.py` |
| Recorder | `Recorder` | `V0Recorder` | — | `recorder.py` |

> **Current state:** V0 Orchestrator, Executor, Verifier, and Recorder all live in `runtime.py`.
> AF-0114 extracts them to dedicated files. `runtime.py` becomes the composition root (assembly/wiring only).

#### 3.2.2 Target File Structure

```
src/ag/core/
├── interfaces.py        # Protocols (stable contracts)
├── task_spec.py         # TaskSpec schema
├── planner.py           # V0Planner + V1Planner + V2Planner + V3Planner
├── orchestrator.py      # V0/V1 Orchestrator
├── executor.py          # V0/V1/V2 Executor
├── verifier.py          # V0/V1/V2 Verifier
├── recorder.py          # V0/V1 Recorder
├── runtime.py           # Composition root: wire dependencies, create_runtime()
├── run_trace.py         # RunTrace, Step, VerifierStatus, etc.
├── playbook.py          # Playbook, PlaybookStep
├── execution_plan.py    # ExecutionPlan
└── schema_verifier.py   # SchemaValidator (repair loop engine)
```

**Dependency graph:**
```
executor.py      (depends on: skills/registry, interfaces)
verifier.py      (depends on: run_trace, interfaces)
recorder.py      (depends on: storage, run_trace, interfaces)
     ↑ ↑ ↑
orchestrator.py  (depends on: executor, verifier, recorder, planner)
     ↑
runtime.py       (imports all, wires together, exports create_runtime())
```

### 3.3 Skills & Tooling Layer (Plugins)

**Core principle: Skills are CAPABILITIES, Playbooks are PROCEDURES.**

| Concept | Role | Example |
|---------|------|--------|
| **Skill** | Atomic capability — does ONE thing | `load_documents` (file I/O), `summarize_docs` (LLM call) |
| **Playbook** | Orchestration — sequences capabilities | `summarize_v0` chains load → summarize → emit |

A registry of skills that declare:
- input/output schemas (Pydantic models)
- tool dependencies
- required permissions (for future safety gating)
- test harness expectations

#### Current Skill Inventory

| Skill | Type | Capability | Used By |
|-------|------|------------|--------|
| `load_documents` | File I/O | Read documents from workspace | summarize_v0 |
| `summarize_docs` | LLM | Generate summary from documents | summarize_v0 |
| `web_search` | Search API | Discover URLs from research query | research_v0 |
| `fetch_web_content` | HTTP | Fetch and extract text from URLs | research_v0 |
| `synthesize_research` | LLM | Synthesize research report | research_v0 |
| `emit_result` | Output | Emit structured result to trace | V1Planner plans |
| `zero_skill` | Test | No-op skill (testing) | test_skill |
| `fail_skill` | Test | Always fails (testing) | tests |
| `error_skill` | Test | Always raises exception (testing) | tests |

#### How to Add a Skill

1. Create skill file: `src/ag/skills/{name}.py`
2. Define input/output schemas (Pydantic `BaseModel`)
3. Implement skill class extending `Skill` ABC
4. Implement `execute(ctx, input) -> SkillResult`
5. Register in `registry.py` → `create_default_registry()`
6. Add tests in `tests/test_skill_framework.py`

For detailed skill architecture, see [SKILLS_ARCHITECTURE_0.1.md](docs/dev/additional/SKILLS_ARCHITECTURE_0.1.md).

### 3.4 Schema Reference

All Pydantic models are documented in [SCHEMA_INVENTORY.md](docs/dev/additional/SCHEMA_INVENTORY.md) (AF-0063).

Key schema groups:
- **Task/Run:** TaskSpec, RunTrace, Step, Artifact
- **Skills:** SkillInput, SkillOutput, SkillContext (AF-0060)
- **Playbooks:** Playbook, PlaybookStep

### 3.4.1 Contract Reference

All Protocol interfaces are documented in [CONTRACT_INVENTORY.md](docs/dev/additional/CONTRACT_INVENTORY.md) (AF-0013).

Key protocol groups:
- **Core Runtime:** Normalizer, Planner, Orchestrator, Executor, Verifier, Recorder
- **Storage:** RunStore, ArtifactStore
- **Providers:** LLMProvider
- **Skills:** Skill (v2 ABC)

### 3.4.2 Concept Relationships

The four core concepts (Schemas, Contracts, Skills, Playbooks) relate as follows:

| Concept | Definition | Layer |
|---------|------------|-------|
| **Schema** | Data shape (Pydantic model) | Data |
| **Contract** | Behavioral promise (Protocol interface) | Interface |
| **Skill** | Atomic LLM-powered capability | Capability |
| **Playbook** | Workflow composing skills | Orchestration |

**Relationship Matrix:**

```
                    SCHEMAS                          CONTRACTS
                    (data shapes)                    (behavioral promises)
                         │                                  │
    ┌────────────────────┼──────────────────────────────────┼────────────────────┐
    │                    │                                  │                    │
    │  ┌─────────────────▼─────────────────┐   ┌───────────▼───────────────┐    │
    │  │ SkillInput, SkillOutput           │   │ Skill ABC (execute)       │    │
SKILLS │ LoadDocumentsInput/Output         │◄──│ SkillContext injection    │    │
    │  │ SummarizeDocsInput/Output         │   │ Executor calls skills     │    │
    │  └───────────────────────────────────┘   └───────────────────────────┘    │
    │                                                                            │
    │  ┌───────────────────────────────────┐   ┌───────────────────────────┐    │
    │  │ Playbook, PlaybookStep            │   │ Planner (selects)         │    │
PLAYBOOKS TaskSpec (input)                 │◄──│ Orchestrator (executes)   │    │
    │  │ RunTrace (output)                 │   │ Verifier (validates)      │    │
    │  └───────────────────────────────────┘   └───────────────────────────┘    │
    │                                                                            │
    └────────────────────────────────────────────────────────────────────────────┘
```

**Key Relationships:**

| From | To | Relationship |
|------|-----|--------------|
| Skill | Schema | Consumes input schemas, produces output schemas |
| Skill | Contract | Implements `Skill` ABC, invoked by `Executor` contract |
| Playbook | Schema | Defined by `Playbook` schema, produces `RunTrace` |
| Playbook | Contract | Selected by `Planner`, executed by `Orchestrator` |
| Contract | Schema | Methods take/return schema instances |

**Execution Flow:**

```
TaskSpec (schema)
     │
     ▼
Planner (contract) ──► selects ──► Playbook (schema)
     │
     ▼
Orchestrator (contract) ──► executes steps ──► calls Executor (contract)
     │                                              │
     │                                              ▼
     │                                         Skill (contract)
     │                                              │
     │                                         SkillInput/Output (schemas)
     │                                              │
     │                                              ▼
     │                                         Verifier (contract)
     │                                              │
     │                                         pass / fail (repair?)
     │
     ▼
RunTrace (schema) ──► persisted by ──► Recorder (contract)
```

### 3.5 Knowledge & Intelligence (Optional modules)
- **Retriever (RAG option)**: `retrieve(query, ctx) -> EvidenceBundle`
- **MemoryStore (optional)**: workspace-bounded state, summaries, embeddings
- **Predictor (MLP option)**: `predict(ctx) -> ranked hints` (routing/tool ranking/classification)
  - must never be required for correctness

### 3.5.1 LLM Intelligence in the Pipeline

Not all pipeline components benefit equally from LLM calls. This table summarizes
where intelligence adds value and where mechanical processing suffices:

| Component | LLM in V0/V1? | LLM in V2+? | What LLM adds |
|-----------|:-:|:-:|---|
| **Planner** | **Yes** (V1) | Yes | Compose skill sequences, judge feasibility |
| **Verifier** | No | **Yes (strongest candidate)** | Semantic quality: relevance, completeness, consistency |
| **Executor** | No | Yes (targeted) | Output repair: fix malformed JSON without full re-invocation |
| **Orchestrator** | No | Indirect only | Triggers Planner for replanning; decision logic stays mechanical |
| **Recorder** | No | Low value | Auto-generated summaries (nice-to-have, not essential) |
| **TaskSpec** | No | No | Pure data schema; no intelligence needed |

**Design principle:** LLM calls in pipeline components are always **additive**.
Mechanical validation runs first; LLM adds intelligence on top. If the LLM is
unavailable, the pipeline degrades gracefully to mechanical-only behavior.

### 3.6 Storage Layer

**Workspace directory structure (AF0058):**
```
<workspace_id>/
├── db.sqlite              # SQLite index for runs/artifacts
├── inputs/                # User content (read by skills)
│   └── *.md, *.txt, etc.
└── runs/                  # System outputs (per-run folders)
    └── <run_id>/
        ├── trace.json     # RunTrace JSON
        └── artifacts/     # Artifacts for this run
            └── <filename>
```

Storage components:
- Workspace state (db.sqlite)
- Runs + traces (runs/<id>/trace.json)
- Artifacts registry (runs/<id>/artifacts/)
- Optional memory store
- Config store

---

## 4. Execution flows

### 4.1 Request-driven flow (CLI/API)
1. Adapter receives a request
2. Normalizer produces `TaskSpec` (workspace defaults applied)
3. Planner creates execution plan:
   - **V0 (current):** lookup playbook by `--playbook <name>`
   - **V1 (Sprint 11):** LLM composes skill sequence from task + catalog
4. (V1 only) User previews and approves plan via `ag plan` / `ag run --plan`
5. Orchestrator executes steps:
   - Executor runs each step (LLM + skills/tools)
   - Verifier checks; may repair within limits
6. Recorder persists trace + artifacts
7. Adapter renders output strictly derived from trace (truthful UX)

### 4.2 Event-driven flow (planned; IoT later)
1. Event Adapter receives an event (sensor reading, trigger)
2. Normalizer maps `EventSpec -> TaskSpec` (policy + constraints)
3. Same pipeline as above
4. Safety hooks apply stricter gating for actuator-like actions

---

## 5. Playbooks and reasoning modes

### 5.0 Autonomy Spectrum

The system's autonomy evolves through phases:

```
RIGID                                                    AUTONOMOUS
(human decides everything)                    (agent decides everything)
    │                                                         │
    ▼                                                         ▼
┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
│ Script │  │Playbook│  │ Guided │  │ Goals  │  │  Full  │
│        │  │        │  │ Agent  │  │  Only  │  │ Agent  │
└────────┘  └────────┘  └────────┘  └────────┘  └────────┘
              ✅ Done     🔄 S11      ⏳         ⏳
```

**Current design:** Operating in guided autonomy mode (Sprint 11+).
V1Planner composes multi-step, multi-output plans from the skill catalog.
Accumulated chaining allows earlier step outputs to flow through to all
subsequent steps (validated 2026-03-21 with multi-emit plans).

### Pipeline Component Evolution

Each pipeline component evolves through versioned implementations aligned with the autonomy spectrum.

#### Planner Evolution

| Version | Behavior | LLM? | Sprint |
|---------|----------|:---:|--------|
| V0Planner | Deterministic registry lookup; requires `--playbook <name>` | No | Current |
| V1Planner | LLM composes skill sequences from catalog; returns `ExecutionPlan`. Supports multi-output plans (multiple `emit_result` steps) with accumulated chaining. | **Yes** | Sprint 11 ✅ |
| V2Planner | LLM uses skills AND playbooks as building blocks | **Yes** | Sprint 13 ✅ |
| V3Planner | Judges feasibility, identifies capability gaps, offers partial plans | **Yes** | Sprint 15 ✅ (ADR-0009) |

#### Executor Evolution

| Version | Behavior | LLM? | Sprint |
|---------|----------|:---:|--------|
| V0Executor | Calls `skill.execute()`, returns result unchecked | No | Current |
| V1Executor | Validates output against `SkillInfo.output_schema`; bounded retry (re-invoke skill) on schema mismatch | No | Sprint 14 ✅ (AF-0116) |
| V2Executor | LLM-powered output repair: on schema validation failure, asks LLM to fix malformed JSON instead of full skill re-invocation. Cheaper than retry. | **Yes** | Sprint 15 ✅ (AF-0124) |

#### Verifier Evolution

| Version | Behavior | LLM? | Sprint |
|---------|----------|:---:|--------|
| V0Verifier | End-of-run error scan; no step awareness (BUG-0017) | No | Current |
| V1Verifier | Step-aware: respects required/optional, per-step pass/fail evidence, rich verification data | No | Sprint 13 ✅ (AF-0115) |
| V2Verifier | LLM-powered semantic verification: evaluates relevance, completeness, consistency, acceptance criteria | **Yes** | Sprint 15 ✅ (AF-0123) |

**V2Verifier is the strongest LLM candidate in the pipeline.** Schema validation is mechanical;
*meaning* validation requires intelligence. Examples:
- *Relevance:* "User asked about Tokyo demographics — report covers Tokyo tourism instead"
- *Completeness:* "Report has data but no conclusion"
- *Consistency:* "Source says 14M population, synthesis says 9M"
- *Acceptance criteria:* V3Planner emits expected-output hints; V2Verifier checks against them

**Design principle:** LLM verification is always **additive** — mechanical validation (V1) runs first,
then LLM evaluation (V2) adds semantic checks. If the LLM verifier is unavailable, mechanical verification still works.

#### Orchestrator Evolution

| Version | Behavior | LLM? | Sprint |
|---------|----------|:---:|--------|
| V0Orchestrator | Linear fire-and-forget loop; verification once at end | No | Current |
| V1Orchestrator | Per-step verification loop; calls Verifier after each step; respects required/optional | No | Sprint 14 ✅ (AF-0117) |
| V2Orchestrator | Replanning on failure: Verifier failure → Planner replan → retry (Gate C) | Indirect (calls Planner) | Future |

#### Recorder Evolution

| Version | Behavior | LLM? | Sprint |
|---------|----------|:---:|--------|
| V0Recorder | Persists RunTrace + artifacts to SQLite/filesystem | No | Current |
| V1Recorder | Adds structured verification evidence, retry history, per-step breakdown | No | Planned (AF-0118) |

**V1Planner flow:**
```
User: "Research Tokyo population trends"
    │
    ▼
V1Planner receives:
- Task description
- Skill catalog (names, descriptions, I/O schemas)
    │
    ▼
LLM prompt: "Given task + skills, create execution plan..."
    │
    ▼
ExecutionPlan:
  steps: [web_search, fetch_web_content, synthesize_research, emit_result]
  confidence: 0.85
  estimated_tokens: 5500
```

**Param chaining:** Steps reference previous outputs via `{{step_N.field}}` placeholders,
resolved at runtime by a lightweight dot-access resolver.

| Decision | Decided By | Rationale |
|----------|------------|----------|
| Which skills exist | Human (compile-time) | Security boundary |
| Playbook structure | Human (definition-time) | Predictability |
| Execution order | Playbook (static) | Testability |
| Skill parameters | Agent (runtime) | Flexibility |
| Retry decisions | Agent (bounded) | Adaptability |
| Output content | Agent (schema-bounded) | Creativity within constraints |
| Resource limits | Human (budget) | Cost control |

**Future phases:**
- **Guided Agent:** Agent suggests playbook modifications, human approves
- **Goals Only:** Human provides goal, agent selects/composes playbook
- **Full Agent:** Agent defines its own skills (requires robust policy engine)

**Core principle:** Humans define WHAT, agents decide HOW.

### 5.1 Playbook responsibilities
A playbook defines:
- agent roles involved
- step graph topology (sequence; branching/parallel later)
- reasoning mode per step
- budgets (time/tool calls/tokens/cost)
- evidence + verification requirements
- failure policy (retry vs repair vs escalate)

### 5.2 Reasoning modes (policy-based)
Reasoning modes are policies affecting:
- prompt strictness/structure
- allowed tools/skills
- verification strictness
- budget allocations

Example modes:
- **Fast**
- **Balanced**
- **Deep**
- **Structured** (schema + validators)
- **Safe-action** (extra confirmations/policy checks)

### 5.3 Current Playbook Inventory

| Name | Stability | Skills Used | Purpose |
|------|-----------|-------------|---------|
| `summarize_v0` | experimental | load_documents, summarize_docs | Summarize documents from workspace |
| `research_v0` | experimental | web_search, fetch_web_content, synthesize_research | Research pipeline: discover, fetch, synthesize |
| `default_v0` | test | (echo-style) | Testing playbook execution |
| `delegate_v0` | test | (echo-style) | Testing multi-step delegation |
| `test_skill` | test | zero_skill | Testing skill execution |

### 5.4 Current Autonomy Boundaries (Sprint 11)

Transitioning from playbook-driven to **guided autonomy**:

| Capability | Status | Notes |
|------------|--------|-------|
| Skill invocation | ✅ Operational | Human selects playbook, planner executes |
| Playbook-driven execution | ✅ Operational | `ag run --playbook <name>` |
| Dynamic skill composition | 🔄 Sprint 11 | V1Planner: LLM composes from skill catalog |
| Plan preview | 🔄 Sprint 11 | `ag plan --task "..."` (AF-0098) |
| Plan approval | 🔄 Sprint 11 | `ag run --plan <id>` (AF-0099) |
| Step confirmation | 🔄 Sprint 11 | Policy-driven hooks (AF-0100) |
| Dynamic playbook composition | ⏳ Future | V2Planner (AF-0103) |
| Feasibility judgment | ⏳ Future | V3Planner (AF-0104) |

**Core constraints (non-negotiable):**
- Truthful UX: all labels trace-derived
- Workspace isolation: no access outside boundaries
- Human approval required before execution (guided mode)
- Policy hooks enforce confirmation for high-impact actions

**Known limitation — workspace isolation is incomplete (AF-0148):**
The "workspace isolation" constraint is aspirational. Currently `ag ws list` exposes all workspaces globally, error messages leak implicitly-resolved workspace names (BUG-0011), and all workspaces share `~/.ag/workspaces/` with no access scoping. AF-0148 tracks the design work to address cross-workspace leakage.

#### How to Add a Playbook

1. Create playbook file: `src/ag/playbooks/{name}_v0.py`
2. Define `Playbook` instance with steps, budgets, metadata
3. Reference registered skills by name in `PlaybookStep.skill_name`
4. Register in `registry.py` → `_REGISTRY` dict
5. Add alias if desired (e.g., `"research": RESEARCH_V0`)
6. Add tests for playbook execution

**CLI commands:**
- `ag playbooks list` — Show available playbooks
- `ag run --playbook <name>` — Execute a playbook

---

## 6. Observability and truthful UX

### 6.1 Trace contract (minimum)
Every run must produce a trace with:
- run metadata: `run_id`, timestamps, workspace_id, `mode` (llm/manual), selected playbook
- step list:
  - step id, role, reasoning mode
  - inputs/outputs (summarized if needed)
  - tool/skill invocations (name + outcome)
  - evidence bundle references
  - errors + retries
- final status: success/failure + verifier result

### 6.2 Citation models (AF0054)
Two citation layers exist:

| Model | Layer | Location | Purpose |
|-------|-------|----------|---------|
| `EvidenceRef` | Core | `run_trace.py` | Trace-level evidence tracking for steps |
| Skill citations | Skill | skill output schemas | Skill output artifact schemas |

**Ownership rule**: Skills define lightweight citation models for their output artifacts.
When recording to the trace, convert to `EvidenceRef` using `to_evidence_ref()`.

### 6.3 Truthful output rule
CLI/API/UI output labels must derive from trace facts, e.g.:
- “used retrieval” only if Retriever invoked
- “verified” only if Verifier recorded pass
- “manual mode” clearly indicated in dev/test output

---

## 7. Safety and policy hook points

Safety is implemented as hook points in orchestrator/executor boundaries.

### Hook points (minimum)
- **Permission check**: before invoking skills/tools marked restricted
- **Confirmation**: before high-impact actions (even if simulated today)
- **Redaction**: before recording/exporting sensitive data
- **Budget enforcement**: token/cost/tool-call caps
- **Escalation**: when verification fails or confidence is low

### 7.1 Autonomy Readiness Constraints

Any autonomy expansion must preserve these constraints:

- **Truthful UX**: all user-visible labels remain trace-derived.
- **Workspace isolation**: no read/write outside active workspace boundaries.
- **Deterministic failure behavior**: retries/timeouts/failures are explicit and traceable.
- **Policy enforcement**: permission/confirmation/budget checks are enforced in runtime behavior, not only documented as hooks.
- **Review gate compliance**: autonomy-affecting changes pass sprint autonomy gate checks before closure.

### 7.2 Autonomy Phase Gates

| Gate | Purpose | Required Conditions | Status |
|------|---------|---------------------|--------|
| Gate A: Reliability | Foundation to autonomy-ready | warning-clean tests, isolation stability, failure-path coverage | ✅ Passed (Sprint 09) |
| Gate B: Guided Autonomy | Enable guided planning | policy enforcement, verifier rigor, trace-derived labels | ✅ Passed (Sprint 10) |
| Gate C: Goals-Only | Enable adaptive autonomous execution | (1) mature policy engine (budgets, risk scoring, scope boundaries), (2) replanning on step failure (adaptive recovery), (3) feasibility judgment (partial plans, "can't do this" reporting), (4) strategy justification in trace (evidence model), (5) controlled skill/playbook extensibility (V2Planner composition) | Future |

**Key distinction:** Guided with `--yes` is "fire and forget with a fixed plan."
Goals Only is "fire and forget with an adaptive agent" — the agent detects
weak signals, replans around failures, and reports when goals are infeasible.

Gate rule: no sprint may claim autonomy progression while a P0 gate condition is unmet.

---

## 8. Technology choices (recommendations + adoption thresholds)

The goal is to **avoid reinventing the wheel** while also avoiding unnecessary overhead.

### Interface adapters
- **CLI (now):** Typer (or Click) for minimal ceremony.
- **Internal API (later):** FastAPI as a thin adapter around the same pipeline.
- **Event ingestion (later):** keep behind `EventAdapter`; choose MQTT/Home Assistant/etc. when IoT scope is real.

### Core runtime orchestration
- **Start simple:** implement a minimal orchestrator loop (sequence-only) behind the `Orchestrator` interface.
- **Adopt LangGraph when needed:** if/when playbooks require real graphs (branching, cycles, streaming, persistence, replay/debug), swap the orchestrator backend to LangGraph without changing your Playbook spec.
  - **Threshold:** you need branching/parallelism, resumability, or durable workflow state beyond a single process run.

### Retrieval (RAG)
- **Start with no retrieval or a trivial local retriever.**
- **Adopt LlamaIndex (or similar) when ingestion/indexing becomes a real need.**
  - **Threshold:** you have stable knowledge packs + repeated retrieval needs, and “manual retrieval” becomes a bottleneck.

### Observability
- **Canonical:** your internal `RunTrace` (always produced).
- **Export (optional):**
  - OpenTelemetry for system-level traces/metrics/log correlation.
  - Langfuse for LLM-app tracing once LLM mode is “real” (prompt/tool call visibility and analysis).

### Storage
- **Early:** SQLite for run/artifact indices + filesystem for artifacts.
- **Later:** Postgres if multi-user/server mode requires it.

### Schemas/validation/tests
- **Schemas:** Pydantic for `TaskSpec`, `RunTrace`, `ArtifactIndex`.
- **Tests:** pytest; keep manual mode usable as the fast test harness.

---

## 9. One-page sequence diagram (text-based)

### 9.1 Request-driven run (CLI/API)

Actors:
- User / Interface Adapter
- Core Runtime Modules
- Skills/Tools
- Storage

Sequence:

1) User → CLI Adapter: `ag run "<prompt>"`
2) CLI Adapter → TaskSpec Normalizer: `raw_input + workspace_ctx`
3) Normalizer → Planner: `TaskSpec (normalized, budgets, defaults)`
4) Planner → Orchestrator: `Playbook + StepGraph + policies`
5) Orchestrator → Recorder: `run_started (metadata)`
6) loop over steps:
   6.1) Orchestrator → Executor: `StepSpec(role, mode, constraints)`
   6.2) Executor → (LLM Provider / Skills): `calls`
   6.3) Skills/Tools → Executor: `results`
   6.4) Executor → Recorder: `step_result (outputs, tool_calls, evidence_refs, errors)`
   6.5) Orchestrator → Verifier: `candidate_output + acceptance_criteria`
   6.6) Verifier → Orchestrator: `pass | fail (repair?)`
   6.7) if fail and repair allowed: Orchestrator schedules repair step (bounded)
7) Orchestrator → Recorder: `run_finished (status, verifier_summary)`
8) CLI Adapter → User: render output derived from RunTrace + artifacts

### 9.2 Planned event-driven run (IoT later)
Event Adapter replaces the CLI Adapter in step (1) and emits `EventSpec -> TaskSpec`, then follows the same pipeline.

---

## 10. v0 RunTrace schema (JSON example)

> This is an example payload, not a strict JSON Schema. It shows the minimum fields we expect to persist and render from.

```json
{
  "run_id": "run_2026_02_23_180512_9f3a",
  "workspace_id": "ws_home",
  "mode": "llm",
  "interface": "cli",
  "playbook": {
    "name": "balanced_default",
    "version": "0.1",
    "reasoning_modes": {
      "planner": "balanced",
      "writer": "structured",
      "critic": "deep"
    }
  },
  "budgets": {
    "max_steps": 12,
    "max_retries": 2,
    "max_tool_calls": 40,
    "max_tokens_estimate": 60000
  },
  "timestamps": {
    "started_at": "2026-02-23T17:05:12Z",
    "finished_at": "2026-02-23T17:06:01Z"
  },
  "task": {
    "title": "Draft project plan section",
    "task_spec_version": "0.1",
    "input": {
      "prompt": "Draft the project plan for ag_foundation",
      "attachments": []
    },
    "constraints": {
      "privacy": "workspace_only",
      "allow_web": false
    }
  },
  "steps": [
    {
      "step_id": "s1",
      "role": "planner",
      "reasoning_mode": "balanced",
      "status": "ok",
      "inputs_summary": "User prompt; workspace defaults; choose playbook and outline steps.",
      "outputs_summary": "Plan: research scope, outline sections, draft, verify, finalize.",
      "tool_calls": [],
      "skill_calls": [],
      "evidence_refs": [],
      "errors": [],
      "timing_ms": 420
    },
    {
      "step_id": "s2",
      "role": "writer",
      "reasoning_mode": "structured",
      "status": "ok",
      "inputs_summary": "Outline sections and constraints.",
      "outputs_summary": "Generated draft markdown file content.",
      "tool_calls": [],
      "skill_calls": [
        {
          "skill": "artifact_writer",
          "version": "0.1",
          "input_ref": "draft_md",
          "output_ref": "artifact://docs/dev/cornerstone/PROJECT_PLAN.md",
          "status": "ok",
          "timing_ms": 38
        }
      ],
      "evidence_refs": [],
      "errors": [],
      "timing_ms": 820
    },
    {
      "step_id": "s3",
      "role": "critic",
      "reasoning_mode": "deep",
      "status": "ok",
      "inputs_summary": "Review draft for scope boundaries and sprint alignment.",
      "outputs_summary": "Found 3 issues; applied revisions; marked as ready.",
      "tool_calls": [],
      "skill_calls": [],
      "evidence_refs": [],
      "errors": [],
      "timing_ms": 510
    }
  ],
  "artifacts": [
    {
      "artifact_id": "a1",
      "type": "markdown",
      "name": "PROJECT_PLAN.md",
      "uri": "artifact://docs/dev/cornerstone/PROJECT_PLAN.md",
      "created_by_step": "s2",
      "hash": "sha256:..."
    }
  ],
  "verifier": {
    "status": "pass",
    "checks": [
      { "name": "scope_boundaries_present", "result": "pass" },
      { "name": "sprint_alignment_present", "result": "pass" },
      { "name": "truthful_mode_declared", "result": "pass" }
    ],
    "notes": "Draft meets v0 acceptance criteria."
  },
  "final": {
    "status": "success",
    "summary": "Drafted project plan and cornerstone index updates.",
    "user_visible_output_ref": "artifact://docs/dev/cornerstone/PROJECT_PLAN.md"
  }
}
```

---

## 11. Next cornerstone docs to author
- `CLI_REFERENCE.md` (trace-derived UX, LLM-first; manual dev-only)
- `REVIEW_GUIDE.md` (how to validate runs + traces + changes)

### 11.2 Known Gaps (Implementation Debt)

Post-Sprint15, remaining gaps:

- ~~**Verifier ignores optional steps (BUG-0017).**~~ Fixed: V1Verifier (AF-0115).
- ~~**Output schema validation missing.**~~ Fixed: V1Executor (AF-0116).
- ~~**Pipeline components in single file.**~~ Fixed: AF-0114 (extraction to dedicated files).
- ~~**Verification runs once at end, not per-step.**~~ Fixed: V1Orchestrator (AF-0117).
- **Verification evidence incomplete.** V1Recorder (AF-0118) not yet implemented. V0Recorder persists traces but lacks structured verification evidence and retry history.
- Policy hook depth (permission/confirmation/budget) requires stronger runtime enforcement.
- Plugin architecture for skills/playbooks is deferred until autonomy readiness gates are stable.
