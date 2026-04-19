# BACKLOG ITEM — AF0143 — hitl_active_approval_gates
# Version number: v1.3
# Created: 2026-04-05
# Started:
# Completed:
# Status: READY
# Priority: P0
# Area: Process / Governance
# Models:

---

## Metadata
- **ID:** AF-0143
- **Type:** Process
- **Status:** READY
- **Priority:** P0
- **Area:** Process / Governance
- **Owner:** Jacob
- **Target sprint:** Pre-Sprint 17 (standalone, must complete before S17 starts)

---

## Goal

Rephrase all HITL gate definitions in FOUNDATION_MANUAL and SPRINT_MANUAL so that gates describe **proactive agent-initiated checkpoints**, not passive blockers.

**Problem:** The current phrasing "Agent MUST Stop and Wait" causes the agent to go silent and wait for the user to initiate the next action. The agent interprets "stop and wait" as "become passive until spoken to."

**Correct behavior:** At each gate, the agent MUST:
1. Present a summary of what was completed
2. State readiness for the next action
3. Explicitly ask for approval to proceed

A gate is a **checkpoint where the agent drives the conversation**, not a wall where the agent goes silent.

## Scope

1. **FOUNDATION_MANUAL.md §10 (HITL Framework)** — Rephrase every gate (G1–G15 or however many exist) from "Agent MUST Stop and Wait" to "Agent MUST present result and request approval before proceeding." Each gate should specify what the agent presents and what approval it asks for.

2. **SPRINT_MANUAL.md** — Update any gate references to match the new phrasing.

3. **copilot-instructions.md** — Add a rule: "At every HITL gate, you MUST proactively present your result and ask for approval. Never go silent and wait."

## Non-Goals

- Do NOT add new gates — only rephrase existing ones
- Do NOT change gate triggers or conditions — only the agent behavior description
- Do NOT restructure the HITL framework

## Acceptance Criteria

- [ ] Every HITL gate definition uses active phrasing ("present result and request approval")
- [ ] No gate uses passive phrasing ("stop and wait", "wait for user", "do not proceed")
- [ ] copilot-instructions.md includes active approval-seeking rule
- [ ] All changes are consistent across FOUNDATION_MANUAL, SPRINT_MANUAL, and copilot-instructions

## References

- S16_OBSERVATIONS_0.1.md §1.4 (Misunderstanding of approval gates)
- S16_OBSERVATIONS_0.1.md §1.2 (Commit discipline failure — same root cause)
- S16_OBSERVATIONS_0.1.md §2.1 (Phase-anchored approval gates)
