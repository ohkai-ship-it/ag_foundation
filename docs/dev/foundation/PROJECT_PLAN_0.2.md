# ag_foundation --- Project Plan

# Version number: v0.3

# Updated: 2026-03-04

------------------------------------------------------------------------

## Purpose

ag_foundation builds a **modular agent network core** that can plan,
execute, verify, and learn from runs.\
IoT integration, web/app UI, and other sensors/data sources are **later
integrations**; the foundation must make those easy to attach.

The foundation phase is complete. The next phase prioritizes **impact
and capability pressure**, not structural hardening.

------------------------------------------------------------------------

# Current State Summary (after Sprint 04)

The system is now:

-   Architecturally modular
-   Trace-contract enforced
-   Workspace-isolated
-   CI disciplined (ruff + pytest -W error + coverage thresholds)
-   Governance consolidated
-   Execution protocol deterministic

Canonical governance documents:

-   `/docs/dev/foundation/FOUNDATION_OPERATING_MANUAL.md`
-   `/docs/dev/foundation/SPRINT_EXECUTION_PLAYBOOK.md`

This marks the end of structural ambiguity.

We are ready to push for functional impact.

------------------------------------------------------------------------

# Strategic Shift (Post-Sprint 04)

We are transitioning from:

> Architecture hardening

to:

> Capability expansion under real pressure

Key rule going forward:

-   No more "infrastructure for infrastructure's sake"
-   Every sprint must create visible system capability
-   Architecture must be validated by use, not by theory

------------------------------------------------------------------------

# Phase 0 --- Foundation Build & Hardening (Completed)

## Sprint 00 --- Project Bootstrap (Closed)

## Sprint 01 --- Core Runtime Skeleton (Closed)

## Sprint 02 --- Agent Network Behavior (Closed)

## Sprint 03 --- Observability & Truthful UX (Closed)

## Sprint 04 --- Safety & Process Hardening (Closed)

Exit status of Phase 0: ✔ Modular runtime\
✔ Delegation\
✔ Trace contract\
✔ Truthful CLI\
✔ CI enforcement\
✔ Governance consolidation\
✔ Deterministic sprint execution model

Foundation maturity achieved.

------------------------------------------------------------------------

# Phase 1 --- Capability Expansion

Future sprints are now impact-driven.

------------------------------------------------------------------------

## Sprint 05 --- High-Pressure Skills (Impact Sprint)

Goal: Force the architecture to prove itself through a real multi-file,
multi-step scenario.

Proposed target scenario:

> Given a workspace with 20+ markdown files, generate a structured
> strategic brief with: - evidence citations - structured output
> (schema-enforced) - artifact export - multi-step delegation - verifier
> loop - trace-backed justification

Why this matters: - Validates skill contracts - Validates trace depth
under load - Forces artifact lifecycle discipline - Exposes weaknesses
in planner/orchestrator - Creates real utility

Exit criteria: - End-to-end scenario reproducible - Structured output
validated - Evidence traceable - No workspace bleed - No invariant
violations

------------------------------------------------------------------------

## Sprint 06 --- Retrieval Interface Layer (RAG Interface)

Goal: Introduce retrieval as a pluggable interface (not necessarily full
production RAG).

Scope: - Retriever interface definition - Workspace-bound indexing
model - Evidence bundle capture in trace - Citation linking in trace
contract - Retrieval fully disable-able for deterministic test mode

Why earlier than previously planned: Retrieval introduces complexity
pressure: - Storage strain - Trace expansion - Evidence verification -
Planner decision branching

Better to surface architectural cracks earlier.

Exit criteria: - Retrieval does not violate layering - Retrieval
trace-observable - Retrieval isolation enforced

------------------------------------------------------------------------

## Sprint 07 --- Workspace & Artifact Maturity

Goal: Strengthen durable state and artifact lifecycle.

Scope: - Artifact registry formalization - Export/import boundaries -
Artifact reproducibility guarantees - Workspace migration model - Memory
boundary enforcement

Exit criteria: - Artifacts reproducible - Cross-workspace bleed
impossible - Clear artifact lifecycle documentation

------------------------------------------------------------------------

## Sprint 08 --- Internal API Readiness (Deferred Priority)

API is **not** top priority.

However, readiness must be preserved.

Goal: Prepare core runtime for future API exposure without freezing
immature contracts.

Scope: - Internal adapter interface definition - Mapping CLI semantics →
internal service layer - Ensure no CLI-only logic leaks into core -
Define future endpoints (not public-stable): - POST /tasks - GET
/runs/{id} - GET /runs/{id}/trace - GET /runs/{id}/artifacts

Important constraint: API implementation should follow real capability
maturity --- not precede it.

Exit criteria: - Core callable via internal interface - No architectural
refactor required when API implemented later

------------------------------------------------------------------------

## Sprint 09 --- Policy & Budget Engine

Goal: Formalize guardrails and execution governance.

Scope: - Budget enforcement hooks - Retry/backoff formalization -
Structured reasoning mode policy - Safe-action classification model -
Verifier escalation strategy

This is expected to be one of the most complex sprints.

Exit criteria: - High-impact steps require explicit policy path - Policy
behavior testable via unit tests - Trace captures policy decisions

------------------------------------------------------------------------

## Sprint 10 --- Integration Phase (Later)

Goal: Attach real-world I/O.

Scope: - IoT adapters - Web/app adapters - Deployment model -
Multi-interface orchestration

Exit criteria: - Sensor event → plan → action (with safety gates) - UI
can inspect traces

------------------------------------------------------------------------

# Architectural Trajectory Summary

We have completed structural maturity.

We now optimize for:

1.  Real capability pressure
2.  Trace depth validation
3.  Skill ecosystem usefulness
4.  Retrieval & evidence rigor
5.  Guardrail formalization

API remains strategically important --- but must follow maturity, not
drive it.

------------------------------------------------------------------------

# Current Strategic Position

The foundation is stable.

The next failure mode is not structural.

It is:

> Building too much architecture without forcing it through real use.

The focus from Sprint 05 onward must be:

-   High-signal capability
-   Realistic workloads
-   Architectural stress testing
-   Invariant preservation under load

That is the path to impact.
