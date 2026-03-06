# ag_foundation --- Project Plan

# Version number: v0.4

# Updated: 2026-03-06

------------------------------------------------------------------------

## Purpose

ag_foundation builds a **modular agent network core** that can plan,
execute, verify, and learn from runs.\
IoT integration, web/app UI, and other sensors/data sources are **later
integrations**; the foundation must make those easy to attach.

The current phase prioritizes **skill architecture hardening**. Skills are
the core unit of capability — everything else (RAG, API, IoT) depends on
skills working correctly first.

------------------------------------------------------------------------

# Current State Summary (after Sprint 05)

The system has:

-   ✅ Architecturally modular runtime
-   ✅ Trace-contract enforced
-   ✅ Workspace-isolated
-   ✅ CI disciplined (ruff + pytest -W error + coverage thresholds)
-   ✅ Governance consolidated
-   ✅ Deterministic sprint execution model
-   ⚠️ **Skills are stub-only** — no LLM integration
-   ⚠️ **Skill contracts undefined** — no input/output schemas
-   ⚠️ **Workspace structure incomplete** — no `inputs/` folder convention

Canonical governance documents:

-   `/docs/dev/foundation/FOUNDATION_MANUAL.md`
-   `/docs/dev/foundation/SPRINT_MANUAL.md`

**Key gap:** The skill layer is the weakest part of the architecture.
Until skills have proper contracts, LLM integration, and evidence capture,
the system cannot deliver real capability.

------------------------------------------------------------------------

# Strategic Focus (Post-Sprint 05)

We are transitioning from:

> Runtime architecture hardening

to:

> Skill architecture hardening

Key rule going forward:

-   **Skills first** — everything else depends on working skills
-   No RAG, API, or IoT until skills are solid
-   Architecture must be validated by real LLM-calling skills

------------------------------------------------------------------------

# Phase 0 --- Foundation Build (Completed)

## Sprint 00 --- Project Bootstrap (Closed)

## Sprint 01 --- Core Runtime Skeleton (Closed)

## Sprint 02 --- Agent Network Behavior (Closed)

## Sprint 03 --- Observability & Truthful UX (Closed)

## Sprint 04 --- Safety & Process Hardening (Closed)

## Sprint 05 --- High-Pressure Skills (Closed)

Exit status of Phase 0:
✔ Modular runtime
✔ Delegation pattern
✔ Trace contract
✔ Truthful CLI
✔ CI enforcement
✔ Governance consolidation
✔ Schema verifier with repair loop
⚠️ Skills remain stubs (no LLM calls)

------------------------------------------------------------------------

# Phase 1 --- Skill Architecture Hardening

This phase makes skills the foundation for all future capability.

------------------------------------------------------------------------

## Sprint 06 --- Skill Foundation (Current)

Goal: Establish the skill architecture that enables real LLM-powered capabilities.

Scope (per INDEX_BACKLOG):

| Order | AF | Title |
|-------|-----|-------|
| 1 | AF-0058 | Workspace folder restructure (inputs/, runs/<id>/) |
| 2 | AF-0060 | Skill definition framework (schemas, protocols) |
| 3 | AF-0063 | Schema inventory documentation |
| 4 | AF-0013 | Contract inventory hardening |

Why this matters:
- AF-0058 establishes the workspace interface skills depend on
- AF-0060 defines how skills declare inputs/outputs and call LLMs
- AF-0063 documents what schemas exist (prerequisite for contracts)
- AF-0013 reconciles documentation with implementation

Exit criteria:
- Workspace has `inputs/` and `runs/<id>/` structure
- Skill protocol defined with input/output schemas
- SkillContext provides LLM access pattern
- Schema inventory complete
- No undocumented contract drift

Reference: `/docs/dev/additional/SKILLS_ARCHITECTURE_0.1.md`

------------------------------------------------------------------------

## Sprint 07 --- First Real Skills

Goal: Prove the skill framework by implementing real LLM-calling skills.

Scope (per INDEX_BACKLOG):

| Order | AF | Title |
|-------|-----|-------|
| 1 | AF-0065 | First skill set (from scratch, not strategic_brief) |
| 2 | AF-0066 | E2E integration test (skill → verifier → trace → artifact) |
| 3 | AF-0062 | Trace LLM model tracking |

Why this matters:
- AF-0065 validates that the framework actually works
- AF-0066 proves the full pipeline end-to-end
- AF-0062 ensures LLM usage is observable

Exit criteria:
- At least 2 working skills that call LLM
- Skills produce evidence and artifacts
- E2E test passes in CI (mock provider)
- E2E test passes manually (real provider)
- Trace shows model used

------------------------------------------------------------------------

## Sprint 08 --- Skill Ecosystem Expansion

Goal: Build out the skill library and playbook composition.

Scope:
- Additional skills: code_review, generate_tests, refactor
- Playbook library with multiple workflows
- Default playbook selection logic

Exit criteria:
- 5+ working skills
- Multiple playbooks demonstrating composition
- Playbook selection documented

------------------------------------------------------------------------

# Phase 2 --- Capability Expansion (Deferred)

These sprints are deferred until skill architecture is proven.

------------------------------------------------------------------------

## Sprint 09+ --- Retrieval Interface Layer (RAG)

Goal: Introduce retrieval as a pluggable interface.

Scope:
- Retriever interface definition
- Workspace-bound indexing model
- Evidence bundle capture in trace
- Citation linking in trace contract

Prerequisite: Sprint 07 complete (skills must work first)

------------------------------------------------------------------------

## Sprint 10+ --- Workspace & Artifact Maturity

Goal: Strengthen durable state and artifact lifecycle.

Scope:
- Artifact registry formalization
- Export/import boundaries
- Artifact reproducibility guarantees
- Workspace migration model

------------------------------------------------------------------------

## Sprint 11+ --- Internal API Readiness

Goal: Prepare core runtime for API exposure.

Scope:
- Internal adapter interface definition
- CLI → service layer mapping
- Future endpoint definitions

Prerequisite: Skills work, RAG works, then API.

------------------------------------------------------------------------

## Sprint 12+ --- Policy & Budget Engine

Goal: Formalize guardrails and execution governance.

Scope:
- Budget enforcement hooks
- Retry/backoff formalization
- Safe-action classification

------------------------------------------------------------------------

## Sprint 13+ --- Integration Phase (IoT/Web)

Goal: Attach real-world I/O.

Scope:
- IoT adapters
- Web/app adapters
- Multi-interface orchestration

Prerequisite: Everything above works first.

------------------------------------------------------------------------

# Phase 3 --- Autonomy Evolution (Future)

The system's autonomy level will evolve over time.

## Autonomy Spectrum

```
RIGID                                                    AUTONOMOUS
(human decides everything)                    (agent decides everything)
    │                                                         │
    ▼                                                         ▼
┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
│ Script │  │Playbook│  │ Guided │  │ Goals  │  │  Full  │
│        │  │        │  │ Agent  │  │  Only  │  │ Agent  │
└────────┘  └────────┘  └────────┘  └────────┘  └────────┘
     │           │           │           │           │
     │      PHASE 1     PHASE 3     PHASE 4     PHASE 5
     │      (now)       (future)    (future)    (future)
```

### Phase 1: Playbook-Driven (Current Focus)

- Humans define playbooks (skill sequence, data mapping)
- Agents have autonomy WITHIN skill execution
- Predictable, testable, debuggable

### Phase 3: Guided Agent (Future)

- Agent can suggest playbook modifications
- Human approves before execution
- Semi-autonomous planning

### Phase 4: Goals Only (Future)

- Human provides goal, agent selects playbook
- Agent composes skills dynamically
- Monitoring and guardrails required

### Phase 5: Full Agent (Long-term)

- Agent defines its own skills
- Minimal human oversight
- Requires robust safety/policy engine

**Key principle:** Humans define WHAT, agents decide HOW.

------------------------------------------------------------------------

# Architectural Trajectory Summary

We have NOT completed structural maturity.

The skill layer is the critical gap. Until skills:
- Have defined input/output schemas
- Can call LLMs via provider injection
- Produce evidence and artifacts
- Are testable in isolation

...the system cannot deliver real capability.

Current optimization targets:

1.  **Skill architecture** — most urgent
2.  **Schema discipline** — enables verification
3.  **Evidence model** — enables trust
4.  **Workspace structure** — enables skill I/O

Deferred until skills work:

1.  RAG/Retrieval
2.  Internal API
3.  Policy engine
4.  IoT/Web integration

------------------------------------------------------------------------

# Current Strategic Position

The runtime is stable but the skill layer is immature.

The next failure mode is:

> Building features (RAG, API, IoT) on top of broken skill foundations.

The focus from Sprint 06 onward must be:

-   Skill contracts first
-   Real LLM integration
-   Evidence and artifact discipline
-   Verifiable, testable skills

That is the path to capability.
