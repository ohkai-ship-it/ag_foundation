# Decisions (ADRs) — Index

This folder contains **Architecture Decision Records (ADRs)** for ag_foundation.

## What Goes Here
ADRs document significant technical decisions, especially:
- P1+ changes to architecture, schemas, or module boundaries
- Adoption of major dependencies (frameworks, libraries)
- Changes to core contracts (TaskSpec, RunTrace, CLI)

## Current ADRs

| ID | Title | Status |
|---:|---|:--:|
| ADR-0001 | [Architecture baseline](ADR-0001-architecture-baseline.md) | Accepted |
| ADR-0002 | [Trace versioning strategy](ADR-0002-trace-versioning.md) | Accepted |
| ADR-0003 | [Manual mode gating](ADR-0003-manual-mode-gating.md) | Accepted |
| ADR-0004 | [Storage baseline](ADR-0004-storage-baseline.md) | Accepted |
| ADR-0005 | [Orchestrator threshold](ADR-0005-orchestrator-threshold.md) | Accepted |

## How to Use
1. Use `templates/ADR_TEMPLATE.md` to create a new ADR.
2. Name it `ADR-XXXX-<short-title>.md` (sequential numbering).
3. Link the ADR from the relevant backlog item and PR.
4. Mark status: Proposed → Accepted → Superseded (if replaced).
