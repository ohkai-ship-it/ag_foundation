# ADR-0005 — Orchestrator backend threshold: sequence loop now, workflow engine later
# Version number: v0.1

## Status
Proposed (write if/when needed during Sprint 01/02)

## Date
2026-02-24

## Context
We want an interface-first design and low overhead. A workflow engine (e.g., LangGraph) can help for branching, resumability, streaming events, and complex agent graphs. But introducing it too early risks coupling, extra abstractions, and slower iteration.

## Decision
Use a custom sequence-only orchestrator loop for v0, behind the Orchestrator interface. Adopt a workflow engine only when at least two thresholds are met:

Thresholds:
1) Branching/conditional execution becomes a first-class requirement.
2) Resumability / checkpointing is required for long runs.
3) Step-level streaming/observability requires standardized event hooks.
4) Multiple planners/executors need composition and routing beyond a simple loop.

When thresholds are met, introduce a new Orchestrator implementation (engine-backed) without changing caller interfaces.

## Alternatives considered
- Adopt LangGraph immediately (rejected: premature complexity).
- Hardcode orchestration into CLI/runtime (rejected: breaks modularity).

## Consequences
- Pros: fast early iteration; preserves modularity; avoids heavy dependency.
- Cons: custom loop may need refactor when thresholds are reached.
- Implementation: ensure Orchestrator interface is expressive enough to later map to an engine.

## Related docs / links
- AF-0007 — Core runtime skeleton v0 (sequence pipeline)
- ARCHITECTURE.md (orchestrator abstractions)

