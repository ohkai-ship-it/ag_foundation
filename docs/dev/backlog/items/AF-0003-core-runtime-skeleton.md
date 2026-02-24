# AF-0003 — Core runtime skeleton (request + event driven)

## Metadata
- **ID:** AF-0003
- **Type:** Architecture
- **Status:** Proposed
- **Priority:** P0
- **Area:** Kernel/IoT
- **Owner:** Jeff/Jacob

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

## Acceptance criteria (DoD)
- [ ] Runtime flow is described clearly in the new ARCHITECTURE doc (or a dedicated section within it)
- [ ] Core interfaces/nouns are defined in a way that keeps future adapters pluggable