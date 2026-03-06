# ADR-0001 — Architecture baseline for ag_foundation
# Version number: v0.1

## Metadata
- **ADR:** ADR-0001
- **Status:** ACCEPTED
- **Date:** 2026-02-23
- **Owners:** Kai, Jeff
- **Related backlog item(s):** AF-0002 (cornerstone docs)
- **Related PR(s):** N/A (docs baseline)
- **Reviewers:** Kai, Jeff

## Context
ag_foundation starts as a clean-slate project to build a modular agent-network core, with future readiness for internal API, UI, and IoT adapters. We need a baseline architecture to prevent drift and enable consistent implementation.

## Decision
We adopt the following baseline architecture:

- **Interface adapters** (CLI now; internal API/event adapters later) normalize input into **TaskSpec**.
- The **core runtime** is a modular pipeline with replaceable modules:
  - Normalizer → Planner → Orchestrator → Executor → Verifier → Recorder
- The system is **LLM-first** for end-user behavior.
- A **manual mode** exists for dev/test only (LLMs disabled) and must remain gated.
- **Playbooks** define orchestration as a step graph with **reasoning modes** as policies.
- **RAG** and **MLP-like predictors** are optional modules behind interfaces (`Retriever`, `Predictor`) and are not required for correctness.
- **RunTrace** is the canonical record; user-visible labels must be derived from trace facts (**truthful UX**).
- **Safety hooks** (permission/confirmation/redaction/budgets/escalation) are designed in early, even before IoT exists.

## Options considered
1) **Monolithic agent loop without modular interfaces**
   - Pros: faster initial coding
   - Cons: high coupling, hard to add API/UI/IoT later, difficult to test and observe

2) **Adopt workflow framework immediately (e.g., LangGraph)**
   - Pros: graph orchestration, streaming/persistence features
   - Cons: upfront overhead and lock-in risk before requirements are clear

## Consequences
- We will implement a minimal in-house orchestrator first (sequence execution), keeping the `Orchestrator` interface stable.
- If/when step graphs require branching/cycles/persistence/streaming, we may adopt a framework backend (e.g., LangGraph) behind the interface via a new ADR.
- Any RunTrace schema changes are treated as P1 and require documentation and evidence.

## Guardrails / invariants
- Truthful UX: labels must be provable from RunTrace
- Workspace isolation is strict
- Manual mode remains dev/test-only
- Modular boundaries must not be bypassed

## Links
- `/docs/dev/cornerstone/ARCHITECTURE.md`
- `/docs/dev/cornerstone/PROJECT_PLAN.md`

