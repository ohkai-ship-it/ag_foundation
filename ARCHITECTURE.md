# ag_foundation — Architecture
# Version number: v0.2

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
The kernel of execution, implemented as replaceable modules:

1) **TaskSpec Normalizer**
- input/event → `TaskSpec`
- applies workspace defaults (budgets, policies, preferred playbooks)

2) **Planner**
- decomposes into a step graph
- selects agent roles/skills
- chooses playbook + reasoning modes

3) **Orchestrator**
- executes the playbook step graph (sequence first; branching/parallel later)
- enforces budgets, retries, state transitions
- emits trace events

4) **Executor**
- runs one step
- calls LLM(s) and/or skills/tools
- outputs step results + evidence

5) **Verifier/Evaluator**
- checks acceptance criteria / quality thresholds
- can trigger repair loops within limits

6) **Recorder**
- persists run trace + artifacts + summaries
- produces artifact index for CLI/API/UI retrieval

### 3.3 Skills & Tooling Layer (Plugins)
A registry of skills that declare:
- input/output schemas
- tool dependencies
- required permissions (for future safety gating)
- test harness expectations

For detailed skill architecture, see [SKILLS_ARCHITECTURE_0.1.md](docs/dev/additional/SKILLS_ARCHITECTURE_0.1.md).

### 3.4 Schema Reference

All Pydantic models are documented in [SCHEMA_INVENTORY.md](docs/dev/additional/SCHEMA_INVENTORY.md) (AF-0063).

Key schema groups:
- **Task/Run:** TaskSpec, RunTrace, Step, Artifact
- **Skills:** SkillDefinition, SkillContext, SkillResult (AF-0060)
- **Playbooks:** Playbook, PlaybookStep, InputMapping

### 3.5 Knowledge & Intelligence (Optional modules)
- **Retriever (RAG option)**: `retrieve(query, ctx) -> EvidenceBundle`
- **MemoryStore (optional)**: workspace-bounded state, summaries, embeddings
- **Predictor (MLP option)**: `predict(ctx) -> ranked hints` (routing/tool ranking/classification)
  - must never be required for correctness

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
3. Planner selects Playbook + step graph
4. Orchestrator executes steps:
   - Executor runs each step (LLM + skills/tools)
   - Verifier checks; may repair within limits
5. Recorder persists trace + artifacts
6. Adapter renders output strictly derived from trace (truthful UX)

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
                 ▲
                 │
           CURRENT PHASE
```

**Current design:** Playbook-driven with bounded agent autonomy.

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
| `Citation` | Skill | e.g., `strategic_brief.py` | Skill output artifact schema |

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
