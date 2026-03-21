# ag_foundation --- Project Plan
# Version number: v0.9
# Updated: 2026-03-20

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

# Current State Summary (after Sprint 10)

The system has:

-  Modular runtime with clear layered architecture
-  Trace-contract enforcement and truthful UX discipline
-  Workspace isolation and explicit workspace selection policy
-  CI discipline (ruff + pytest -W error + coverage)
-  Skill framework v2 and working playbooks (`summarize_v0`, `research_v0`)
-  Architecture and inventory documentation synchronized (schemas/contracts)
-  Policy hooks with enforcement (AF-0087)
-  Plugin architecture foundation (skills entry points, YAML playbooks)
-  Gate A (Reliability) PASSED
-  Gate B (Guided Autonomy) PASSED

Canonical governance documents:

- `/docs/dev/foundation/FOUNDATION_MANUAL.md`
- `/docs/dev/foundation/SPRINT_MANUAL.md`

Key shift:
Ready to implement guided autonomy capabilities. Sprint 11 enables plan
preview, approval workflows, and step-level confirmation.

------------------------------------------------------------------------

# Strategic Focus (Post-Sprint 10)

We are transitioning from:

> Gate B readiness (reliability + safety hardening)

to:

> Guided autonomy implementation (plan preview + approval + confirmation)

Key rule going forward:

- Guided autonomy must prove reliable before goals-only mode
- Keep truthful UX and workspace isolation non-negotiable
- Preserve bounded autonomy: humans define WHAT, agents decide HOW
- Expand planner autonomy incrementally with user control

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

## Sprint 09 --- Reliability + Safety Hardening (Closed)

Goal: Eliminate known reliability blockers before autonomy expansion.

Exit status:
 Test isolation framework implemented (AF-0046)
 Warning-clean test discipline enforced (AF-0071)
 CLI consistency audit completed (AF-0085)
 Policy hook enforcement baseline established (AF-0087)
 Failure-path coverage hardened

------------------------------------------------------------------------

## Sprint 10 --- Gate B Readiness (Closed)

Goal: Achieve Gate B (Guided Autonomy) readiness through evidence
maturity, CLI completeness, documentation hygiene, and plugin
architecture foundation.

Exit status:
 Gate B achieved (2026-03-12)
 Artifact metadata truthful end-to-end (AF-0090)
 Verifier failure-path consistency (AF-0091)
 Skills test coverage thresholds met (AF-0093)
 CLI surface parity with CLI_REFERENCE (AF-0012)
 Global CLI flags ADR accepted (ADR008)
 Plugin architecture foundation (AF-0077, AF-0078)
 Documentation hygiene enforced (AF-0081, AF-0084)

------------------------------------------------------------------------

## Sprint 11 --- Guided Autonomy Enablement (Closed)

Goal: Enable guided autonomy mode where users can preview, approve, and
control agent execution plans before they run.

This sprint transitions from Gate B readiness to operating IN guided
autonomy mode:

```
Playbook → [Guided Agent] → Goals Only → Full Agent
           ^^^^^^^^^^^^^^
           THIS SPRINT
```

Scope focus (3 parallel tracks):

**Track 1: LLM Planner + Plan Workflow (P1 — core autonomy)**
- AF-0102 V1Planner — LLM composes plans from skill catalog
- AF-0098 Plan preview command (`ag plan --task "..."`)
- AF-0099 Plan approval workflow (`ag run --plan <id>`)
- AF-0100 Step confirmation hooks for high-impact actions

**Track 2: Observability for Autonomy (P2 — audit support)**
- AF-0094 Trace full I/O enrichment (LLM tokens, step data)
- BUG-0015 Runs list count mismatch fix (truthful UX)

**Track 3: UX Polish (P3 — quality of life)**
- AF-0097 runs commands default workspace
- AF-0101 Autonomy level display in CLI and trace

Exit criteria:
- V1Planner composes skill sequences from LLM analysis
- `ag plan --task "..."` generates reviewable execution plan
- `ag run --plan <id>` executes approved plan
- Step confirmation policy configurable per workspace
- Trace records full step I/O and LLM usage
- Autonomy mode visible in CLI and trace
- Truthful UX maintained (BUG-0015)

Key milestone (2026-03-21):
V1Planner produces multi-output plans (multiple `emit_result` calls) with
accumulated chaining. Earlier step outputs flow through to all subsequent
steps, enabling plans that emit both Markdown and JSON from a single run.
(BUG-0016c fix, plan `plan_486286485e3b`)

------------------------------------------------------------------------

## Sprint 12 --- Autonomy Boundaries (Current)

Goal: Stabilize guided autonomy output quality and storage boundaries by
unifying summarization, hardening content emission, and standardizing
run-centered artifact/plan layout.

Scope focus:
- AF-0110 Run layout and plan artifacts refactor (P1)
- AF-0108 Unify summarization skill (P1)
- AF-0109 emit_result strict content validation (P1)
- AF-0107 load_documents MD inputs reliability (P1)
- AF-0105 CLI defaults fix (P2)
- AF-0106 V1Planner file pattern defaults (P2)
- AF-0096 Test workspace cleanup pollution (P2)
- AF-0111 --workspace flag must never create workspace (P1)

Explicitly excluded:
- AF-0103 LLM Planner V2 (skills+playbooks)
- AF-0104 LLM Planner V3 (feasibility)

Exit criteria:
- Single summarization skill path (synthesize_research)
- Strict emit_result content validation (no stub/empty output)
- Run-centered layout (runs/<id>/result.md, trace.json, artifacts/*)
- Plan stored under run artifacts, workspace /plans deprecated
- CLI commands work with sensible defaults
- --workspace rejects non-existent names (contract tested)

------------------------------------------------------------------------

# Autonomy Phase Gates (Required)

| Gate | Purpose | Required Conditions | Status |
|------|---------|---------------------|--------|
| Gate A: Reliability | Move from foundation to autonomy-ready execution | warning-clean tests, isolation stability, failure-path coverage, deterministic cleanup | ✅ Passed (Sprint 09) |
| Gate B: Guided Autonomy | Enable guided planning behavior | policy enforcement present, verifier/failure rigor, trace-derived labels for all new behavior | ✅ Passed (Sprint 10) |
| Gate C: Goals-Only Preparation | Prepare for dynamic composition | mature policy engine, stronger evidence model, controlled playbook/skill extensibility | Future |

Gate rule:
No sprint may claim autonomy progression while a P0 gate condition is unmet.

------------------------------------------------------------------------

# Phase 3 --- Capability Expansion (Deferred Until Gate C)

These areas remain deferred until guided autonomy proves reliable and
Gate C prerequisites are met.

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
Transitioning from playbook-driven to guided autonomy (Sprint 11).

Progression status:
- ✅ Playbook: established and validated
- ✅ Guided Agent: operational (Sprint 11 closed; multi-output plans validated)
- 🔄 Guided Agent hardening: Sprint 12 in progress
- ⏳ Goals Only: future (requires Gate C)
- ⏳ Full Agent: long-term (policy-engine dependent)

Core principle:
Humans define WHAT, agents decide HOW.

------------------------------------------------------------------------

# Current Strategic Position

**Gate A (Reliability) and Gate B (Guided Autonomy) are now PASSED.**

Sprint 11 delivered guided autonomy capabilities:
- Plan preview before execution (`ag plan`)
- Plan approval workflow (`ag run --plan`)
- Step-level confirmation for high-impact actions
- Autonomy mode visibility in CLI and trace
- Multi-output plan support with accumulated chaining (2026-03-21)

The next failure mode is:

> Shipping unreliable output quality or fragmented storage while
> guided autonomy appears to work.

Near-term focus for Sprint 12:
- Unify summarization and harden content emission
- Standardize run-centered storage layout
- CLI defaults and workspace safety

The path forward is incremental autonomy expansion with explicit gates.
Guided autonomy must prove reliable before advancing to goals-only mode.
