# AF0002 — New cornerstone docs (IoT-in-space vision)
# Version number: v0.2

## Metadata
- **ID:** AF-0002
- **Type:** Docs | Architecture
- **Status:** Done
- **Priority:** P0
- **Area:** Docs/Architecture/CLI/Review
- **Owner:** Jeff
- **Completed in:** Sprint 00

## Problem
The cornerstone docs must be re-authored for the new vision:
An interactive agent network operating via IoT in a defined space, extensible to other sensors/data sources, spanning household chores to business strategy.

## Goal
Create fresh versions under `/docs/dev/cornerstone/`:
- ARCHITECTURE.md
- PROJECT_PLAN.md
- CLI_REFERENCE.md
- REVIEW_GUIDE.md
- plus `cornerstone/INDEX.md` that explains what is canonical.

These docs must embed the execution mode rules:
- Default: LLM mode (end user)
- Manual: dev/test only; not exposed to end users

## Non-goals
- Porting BD-first legacy scope as a primary framing
- Implementing the runtime

## Acceptance criteria (Definition of Done)
- [x] New cornerstone docs exist and reference the new "IoT-in-space" vision
- [x] Mode rules are stated consistently inside the docs (no separate mode contract doc)
- [x] Cornerstone INDEX explains scope boundaries and what is "v0 foundation"

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
Created the new cornerstone docs under `/docs/dev/cornerstone/` with the IoT-in-space vision. The docs establish the execution mode rules and define the v0 foundation scope.

**Key outcomes:**
- ARCHITECTURE.md created with new vision
- PROJECT_PLAN.md established
- CLI_REFERENCE.md defined
- REVIEW_GUIDE.md created
- cornerstone/INDEX.md explains canonical docs
