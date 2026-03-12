# ag_foundation --- Project Plan
# Version number: v0.7
# Updated: 2026-03-11

------------------------------------------------------------------------

## Purpose

ag_foundation builds a modular agent network core that can plan,
execute, verify, and learn from runs.
IoT integration, web/app UI, and other sensors/data sources are later
integrations; the foundation must make those easy to attach.

The current phase prioritizes reliability and safety hardening for
bounded autonomy. Skills are established, but autonomy expansion now
depends on enforcement, resilience, and governance quality gates.

------------------------------------------------------------------------

# Current State Summary (after Sprint 08)

The system has:

-  Modular runtime with clear layered architecture
-  Trace-contract enforcement and truthful UX discipline
-  Workspace isolation and explicit workspace selection policy
-  CI discipline (ruff + pytest -W error + coverage)
-  Skill framework v2 and working playbooks (`summarize_v0`, `research_v0`)
-  Architecture and inventory documentation synchronized (schemas/contracts)
-  Policy hooks exist but enforcement depth is still maturing
-  Reliability debt remains (warning-clean tests, isolation hardening)
-  Autonomy remains playbook-driven; dynamic composition is future work

Canonical governance documents:

- `/docs/dev/foundation/FOUNDATION_MANUAL.md`
- `/docs/dev/foundation/SPRINT_MANUAL.md`

Key shift:
The highest risk is no longer missing skills; it is scaling autonomy
without sufficiently hardened reliability and policy enforcement.

------------------------------------------------------------------------

# Strategic Focus (Post-Sprint 08)

We are transitioning from:

> Skill architecture establishment

to:

> Reliability + safety hardening for bounded autonomy

Key rule going forward:

- Reliability and policy enforcement before deeper autonomy
- Keep truthful UX and workspace isolation non-negotiable
- Preserve bounded autonomy: humans define WHAT, agents decide HOW
- Expand planner autonomy only behind explicit quality gates

------------------------------------------------------------------------

# Phase 0 --- Foundation Build (Completed)

## Sprint 00 --- Project Bootstrap (Closed)

## Sprint 01 --- Core Runtime Skeleton (Closed)

## Sprint 02 --- Agent Network Behavior (Closed)

## Sprint 03 --- Observability & Truthful UX (Closed)

## Sprint 04 --- Safety & Process Hardening (Closed)

## Sprint 05 --- High-Pressure Skills (Closed)

Exit status of Phase 0:
 Modular runtime
 Delegation pattern
 Trace contract
 Truthful CLI
 CI enforcement
 Governance consolidation
 Schema verifier with repair loop

------------------------------------------------------------------------

# Phase 1 --- Skill & Playbook Foundation (Completed)

## Sprint 06 --- Skill Foundation (Closed)

## Sprint 07 --- First Real Skills (Closed)

## Sprint 08 --- Skill Ecosystem Expansion (Closed)

Exit status of Phase 1:
 Skills have defined contracts and schemas
 LLM-powered skills and playbooks validated
 Sprint-level architecture documentation completed
 Autonomy-enabling reliability and policy maturity still required

------------------------------------------------------------------------

# Phase 2 --- Autonomy Readiness Hardening (Current)

This phase operationalizes bounded autonomy with strong enforcement,
resilience, and deterministic review gates.

------------------------------------------------------------------------

## Sprint 09 --- Reliability + Safety Hardening

Goal: Eliminate known reliability blockers before autonomy expansion.

Scope focus:
- Test isolation framework and warning-clean discipline
- CLI consistency audit and reference parity follow-ups
- Policy hook enforcement baseline in runtime paths
- Failure-path coverage and deterministic cleanup behavior

Planned high-priority items (from current backlog state):
- AF-0046 (READY) test isolation framework
- AF-0071 warning-clean test discipline
- AF-0085 CLI consistency audit
- AF-0086 test suite audit

Exit criteria:
- `pytest -W error` passes without known warning exceptions
- Isolation regressions addressed (workspace/provider cleanup)
- CLI behavior and docs parity gaps triaged and scheduled
- Policy checks explicitly validated on touched behavior

------------------------------------------------------------------------

## Sprint 10 --- Gate B Readiness

Goal: Achieve Gate B (Guided Autonomy) readiness through evidence
maturity, CLI completeness, documentation hygiene, and plugin
architecture foundation.

Note: Original Sprint 10 scope (AF-0072, AF-0057, AF-0083) was
completed in Sprint 09 via aggressive mode. Sprint 10 now targets
the remaining Gate B prerequisites.

Scope focus (4 parallel tracks):
- Artifact truthfulness, verification & test maturity (AF-0090, AF-0091, AF-0093)
- CLI completeness (AF-0036 decision, AF-0012 surface parity + BUG-0002/0003/0011)
- Documentation hygiene (AF-0081, AF-0082 rescoped, AF-0084)
- Plugin architecture foundation (AF-0077 Phase 1, AF-0078 Phase 1)

Planned high-priority items:
- AF-0090 artifact truthfulness + trace enrichment (rescoped v0.3)
- AF-0091 verifier failure-path maturity
- AF-0093 skills test coverage hardening
- AF-0036 global CLI flags decision (ADR)
- AF-0012 CLI_REFERENCE surface parity
- AF-0081 inventory sync discipline
- AF-0082 report polish (rescoped after AF-0089)
- AF-0084 index link emoji fix
- AF-0077 skills plugin architecture (Phase 1)
- AF-0078 playbooks plugin architecture (Phase 1)

Dropped: AF-0092 (evidence CLI) — separate evidence concept rejected;
existing `ag artifacts` commands suffice once metadata is truthful.

Exit criteria:
- Artifact metadata in trace.json is truthful end-to-end
- Trace enriched with full step I/O data
- Artifact files stored in runs/<id>/artifacts/ directory
- Verifier outcomes consistent across happy and failure paths
- Skills test coverage: fetch_web_content ≥80%, web_search ≥80%, synthesize_research ≥90%
- CLI surface matches CLI_REFERENCE for implemented commands
- Global CLI flags architecture decision documented as ADR
- Schema/contract inventories current
- Report includes polished metadata/sources/execution details
- Index link emoji consistency fixed
- Skills entry points mechanism works
- YAML playbook loading and validation works
- Gate B conditions assessable at sprint review

------------------------------------------------------------------------

## Sprint 11 --- Controlled Autonomy Enablement

Goal: Prepare the system for Guided Agent evolution behind explicit gates.

Scope focus:
- Controlled planner evolution (suggestions, not unconstrained autonomy)
- Policy/confirmation escalation discipline for higher-impact actions
- Operational quality gates integrated into sprint close ritual

Candidate follow-up themes:
- AF-0077 skills plugin architecture (if gate-ready)
- AF-0078 playbooks plugin architecture (if gate-ready)
- AF-0064 process documentation hardening

Exit criteria:
- Guided autonomy scope is explicitly bounded and documented
- Safety and policy checks are enforced, not only declared
- Review/autonomy gates are integrated in sprint templates and closure

------------------------------------------------------------------------

# Autonomy Phase Gates (Required)

| Gate | Purpose | Required Conditions |
|------|---------|---------------------|
| Gate A: Reliability | Move from foundation to autonomy-ready execution | warning-clean tests, isolation stability, failure-path coverage, deterministic cleanup |
| Gate B: Guided Autonomy | Enable guided planning behavior | policy enforcement present, verifier/failure rigor, trace-derived labels for all new behavior |
| Gate C: Goals-Only Preparation | Prepare for dynamic composition | mature policy engine, stronger evidence model, controlled playbook/skill extensibility |

Gate rule:
No sprint may claim autonomy progression while a P0 gate condition is unmet.

------------------------------------------------------------------------

# Phase 3 --- Capability Expansion (Deferred Until Gate B)

These areas remain deferred until autonomy readiness gates are satisfied.

## Retrieval Interface Layer (RAG)
- Retriever interface definition
- Workspace-bound indexing model
- Evidence bundle capture in trace
- Citation linking in trace contract

## Internal API Readiness
- Internal adapter interface definition
- CLI -> service layer mapping
- Future endpoint definitions

## Integration Phase (IoT/Web)
- IoT adapters
- Web/app adapters
- Multi-interface orchestration

------------------------------------------------------------------------

# Phase 4 --- Autonomy Evolution (Future)

## Autonomy Spectrum

```
RIGID                                                    AUTONOMOUS
(human decides everything)                    (agent decides everything)
    |                                                         |
    v                                                         v
+--------+  +--------+  +--------+  +--------+  +--------+
| Script |  |Playbook|  | Guided |  | Goals  |  |  Full  |
|        |  |        |  | Agent  |  |  Only  |  | Agent  |
+--------+  +--------+  +--------+  +--------+  +--------+
```

Current operational mode:
Playbook-driven bounded autonomy.

Future progression:
- Guided Agent: planner suggestions with human approval
- Goals Only: constrained autonomous composition
- Full Agent: long-term and policy-engine dependent

Core principle:
Humans define WHAT, agents decide HOW.

------------------------------------------------------------------------

# Current Strategic Position

The runtime and skill foundations are now strong enough to shift focus to
reliability and safety enforcement for autonomy scaling.

The next failure mode is:

> Expanding planner autonomy without hardened policy and reliability gates.

Near-term focus from Sprint 09 onward must be:

- Reliability and warning-clean test discipline
- Policy enforcement in runtime behavior
- Failure-path and verifier maturity
- Explicit autonomy gates in sprint planning and review

That is the path to trustworthy bounded agentic autonomy.
