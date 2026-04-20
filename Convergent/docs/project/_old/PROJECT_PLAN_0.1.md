# ag_foundation — Project Plan
# Version number: v0.1

## Purpose
ag_foundation builds a **modular agent network core** that can plan, execute, verify, and learn from runs.  
IoT integration, web/app UI, and other sensors/data sources are **later** integrations; the foundation must make those easy to attach.

## Scope boundaries
### In scope (foundation)
- Agent-network runtime: request → plan → execute → verify → record
- Modular Skill/Plugin architecture + contracts
- Modular Core runtime architecture + contracts
- Observability & “truthful outputs” (trace-driven labels)
- Safety primitives (permissions, confirmations, policy hooks)
- Knowledge options: **RAG** (retrieval-augmented generation) and **MLP** (learned/predictive components) as pluggable modules
- CLI-first developer experience

### Out of scope (for now)
- Real IoT hardware integrations, home automation SDKs
- Web UI / mobile app
- Multi-tenant SaaS packaging and billing
- Full enterprise policy engine / governance suite

## Guiding principles
- End-user behavior is **LLM-first**. Manual mode exists for **dev/test only** (LLMs disabled).
- **Truthfulness > prettiness**: UI output claims come from traces.
- **Pluggable everything**: skills, retrieval, memory, planning, verification are modules behind stable interfaces.
- **Safety by design**: every action channel has gating points.

---

## Core concept: agent network
The system behaves as a **network of cooperating agents**:
- A planner/router decomposes work and selects roles/skills.
- Specialized agents execute subtasks (research, structuring, writing, tool use).
- A verifier/evaluator checks outputs against acceptance criteria and captured evidence.
- A recorder stores run traces, artifacts, and workspace-bounded state.

---

## Architectural options (planned, not mandatory)

## Future API surface (planned)
While CLI is the primary interface early on, we will keep the core runtime **interface-agnostic**.
We plan a thin internal API (not public/stable until later sprints) that mirrors CLI semantics:

- **POST /tasks** → submit a TaskSpec (same payload CLI normalizes to)
- **GET /runs/{run_id}** → run metadata + status
- **GET /runs/{run_id}/trace** → full trace contract (steps, tool calls, evidence)
- **GET /runs/{run_id}/artifacts** → artifact index + download links/paths
- **GET /runs/{run_id}/events** (stream) → live run events for future UI

This API is treated as an additional Input Adapter; the execution pipeline remains unchanged.

### RAG (Retrieval Augmented Generation) — Option
RAG is a **replaceable Retrieval module** that can be enabled per workspace/task:
- sources: local workspace docs, curated knowledge packs; later web sources
- outputs: citations/evidence bundles stored with the run trace

### MLP (Learned / Predictive Components) — Option
MLP here means “learned model components” (not necessarily a literal MLP network):
- routing/policy recommendations
- tool selection ranking
- task classification
- memory relevance scoring

Both are **interfaces-first**: define contracts now so implementations later don’t force rewrites.

---

## Modular core runtime (like Skills/Plugins)
We treat the **core runtime as a pipeline of pluggable modules**.

### Core Runtime Modules (proposed)
1) **Input Adapter** (CLI now; later web/app; later event ingestion)
2) **TaskSpec Normalizer** (standardize input/events into TaskSpec + constraints)
3) **Planner** (decompose; select agents/skills; choose reasoning mode)
4) **Orchestrator** (runs a playbook step graph; manages state, retries, budgets)
5) **Executor** (runs steps: LLM calls, skill calls, transformations)
6) **Verifier/Evaluator** (checks acceptance criteria; triggers repair loops)
7) **Recorder** (run trace, artifacts, evidence, summaries)
8) **Memory/Retrieval** (optional RAG + memory store modules)
9) **Safety/Policy Hooks** (permissions, confirmations, redaction, rate limits)

Each module must log to the trace (observability is a contract).

---

## Playbooks + reasoning modes (between agents)
A **Playbook** describes *how* the agent network coordinates:
- roles involved (Planner, Researcher, Writer, Critic, etc.)
- step graph (sequence/branch/parallel)
- reasoning mode per step (policy-based)
- budgets (time/tool calls/tokens/cost)
- evidence + verification requirements
- failure policy (retry/repair/escalate)

### Reasoning modes (examples)
- **Fast** (low cost, minimal verification)
- **Balanced** (default)
- **Deep** (extra verification loops, higher evidence bar)
- **Structured** (schema + validators)
- **Safe-action** (extra confirmations/policy checks; important later for IoT)

---

# Sprint plan (old milestones, renamed to sprints)

## Sprint 00 — Project bootstrap (Docs + repo operating system)
**Goal:** Establish a clean documentation baseline and workflow.
- `/docs/dev` structure + indexes
- backlog + bug reporting system
- contribution workflow (PR sizing, review gates)

**Exit criteria**
- consistent docs/dev taxonomy in place
- AF-0001 done (kick-off tracked + review entry created)

---

## Sprint 01 — Core runtime skeleton (single-request execution)
**Goal:** A minimal runtime that can execute one request end-to-end.
- CLI input → TaskSpec → Planner → Executor → Result
- basic “skill invocation” model (mock skills ok)
- minimal persistence for runs (run id, timestamps, outputs)

**Exit criteria**
- one command produces a run record with a trace
- failures captured with actionable diagnostics

---

## Sprint 02 — Agent network behavior (multi-step + delegation)
**Goal:** From “one executor” to “agent network”.
- subtask decomposition and delegation to sub-agents or skills
- bounded context passing between steps
- deterministic orchestration *structure* (not deterministic outputs)

**Exit criteria**
- complex tasks produce multi-step traces showing delegation
- clear boundaries between planner, orchestrator, executor, skills

---

## Sprint 03 — Observability and truthful UX (trace contract)
**Goal:** Make runs inspectable and auditable.
- run trace schema: steps, tool calls, evidence, errors, retries
- CLI output labels derived from trace (no hardcoded claims)
- review workflow: how to validate a run

**Exit criteria**
- every run reviewable using the review guide
- CLI/logs reflect actual behavior consistently

---

## Sprint 04 — Safety primitives (human-in-the-loop gates)
**Goal:** Guardrails critical for future IoT/actuators.
- permission model hooks (workspace-scoped)
- confirmation steps for “high-impact” actions (even if simulated)
- policy points in the execution pipeline

**Exit criteria**
- risky action requires explicit confirmation path
- safe defaults + clear audit trail

---

## Sprint 05 — Skills ecosystem (real tools, still CLI-first)
**Goal:** Useful skills without committing to UI/IoT.
- file ops, knowledge mgmt, structured outputs
- external connectors (optional, behind adapters)
- skills packaged with metadata + tests

**Exit criteria**
- skills add/remove without changing core runtime
- skill contracts documented + tested

---

## Sprint 06 — Workspace maturity (projects, artifacts, memory)
**Goal:** Durable state and artifact management.
- workspace isolation
- artifact registry (outputs, exports)
- memory: what is stored, where, and retrieval boundaries
- RAG + MLP remain optional interfaces (implement later)

**Exit criteria**
- multiple workspaces don’t bleed state
- artifacts discoverable and reproducible

---

## Sprint 07 — Interface readiness (pre-IoT, pre-UI)
**Goal:** Make the core callable from future interfaces.
- stable internal API surface mirroring CLI semantics
- event ingestion model placeholder (no IoT implementation yet)
- strict separation: interface layer vs core runtime

**Exit criteria**
- future web/app or IoT adapter can call the same execution pipeline
- adapter contracts documented

---

## Sprint 08 — Integration phase (later): IoT + web/app
**Goal:** Attach real-world I/O.
- IoT sensor/actuator adapters
- web/app frontend
- deployment concerns

**Exit criteria**
- end-to-end: sensor event → plan → action (with safety gates)
- UI supports task submission and run inspection

---

## Immediate next steps
- AF-0001 (kick-off structure) → AF-0002 (new cornerstone docs) → AF-0003 (core runtime skeleton model)
