# AF-0002 — New cornerstone docs (IoT-in-space vision)

## Metadata
- **ID:** AF-0002
- **Type:** Docs | Architecture
- **Status:** Proposed
- **Priority:** P0
- **Area:** Docs/Architecture/CLI/Review
- **Owner:** Jeff

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

## Acceptance criteria (DoD)
- [ ] New cornerstone docs exist and reference the new “IoT-in-space” vision
- [ ] Mode rules are stated consistently inside the docs (no separate mode contract doc)
- [ ] Cornerstone INDEX explains scope boundaries and what is “v0 foundation”