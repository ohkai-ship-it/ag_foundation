# AF0003 — Core runtime skeleton (request + event driven)
# Version number: v0.2

## Metadata
- **ID:** AF-0003
- **Type:** Architecture
- **Status:** Done
- **Priority:** P0
- **Area:** Kernel/IoT
- **Owner:** Jeff/Jacob
- **Completed in:** Sprint 00

## Problem
The new vision requires the system to handle both:
1) user requests (CLI/API)
2) environment events (IoT sensor streams)

We need a minimal runtime model that supports both without overbuilding.

## Goal
Define (doc-first) the minimal runtime model:
- Space (bounded environment)
- Device/Sensor (event source)
- Actuator (action sink)
- Event ingestion → TaskSpec normalization → Planner → Executor → Skill
- Safety gate pattern for actuator actions (confirmations/policies)

Deliverable can be either:
- docs only (preferred for AF-0003), or
- small code skeleton + docs (if you want code started now)

## Non-goals
- Real hardware integration
- Vendor-specific IoT SDKs
- Complex policy engines

## Acceptance criteria (Definition of Done)
- [x] Runtime flow is described clearly in the new ARCHITECTURE doc (or a dedicated section within it)
- [x] Core interfaces/nouns are defined in a way that keeps future adapters pluggable

## Implementation notes
N/A

## Risks
N/A

## PR plan
N/A

---
# Completion section (fill when done)

**Completion date:** Sprint 00 (kick-off)

**Summary:**
Defined the minimal runtime model in the ARCHITECTURE doc. The core interfaces and nouns are established to support future adapters and both request-driven and event-driven flows.

**Key outcomes:**
- Runtime flow documented in ARCHITECTURE.md
- Core interfaces defined (Normalizer, Planner, Orchestrator, Executor, Verifier, Recorder)
- Pluggable adapter pattern established
