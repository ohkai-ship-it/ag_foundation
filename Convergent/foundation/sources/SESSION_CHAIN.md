# SESSION CHAIN
#### Description: Continuity model for agent chat sessions across the project lifecycle. Delegated by GS §DS02. Covers the handoff protocol (outgoing agent produces a continuation prompt), onboarding protocol (incoming agent reads governance docs and verifies state), and inter-agent handoff procedures. Session chains are independent of sprints and may span multiple lifecycle phases. Ensures no context is lost when sessions end.
#### Convergent: v1.3.2
#### governs: ag_foundation

---

## 1. Purpose

Define what happens when a chat session ends and a new one begins. Session changes are discretionary (not mandatory) and can occur at any lifecycle phase. This model ensures no state is lost and the incoming agent can resume work without requiring the HITL to manually reconstruct context.

---

## 2. Core Concepts

**Session:** A single continuous agent chat window. Ends when context fills, the platform crashes, or the HITL chooses to start fresh.

**Session chain:** An ordered sequence of sessions that share a continuity thread. Session chains are not tied to sprints — they may span multiple sprints, cover non-sprint work, or end mid-sprint. HITL assigns human-readable names and numbering at their discretion.

**Handoff:** The outgoing agent's final act — producing a structured state snapshot, triggered by the HITL.

**Onboarding:** The incoming agent's first act — reading governance docs + handoff artifact + verifying workspace state.

**Continuity artifact:** The file that bridges sessions. Written by the outgoing agent, read by the incoming agent. Stored in `docs/additional/prompts/`.

---

## 3. Handoff Protocol

When the HITL decides to end a session, they prompt the outgoing agent to produce a **continuation prompt** before the session closes.

> **Note:** The agent does not know a priori when the session will end. The HITL is responsible for triggering the handoff.

### 3.1 Continuation Prompt Format

The continuation prompt is a structured document containing:

| Section | Required | Content |
|---------|:--------:|---------|
| Sprint state | Yes | Sprint ID, branch name, which AFs are DONE / in-progress / not started |
| Current position | Yes | Which lifecycle phase (P1–P6), which step in SP, which AF (if in P3 loop) |
| In-progress work | If applicable | What's done within the current AF, what remains, any partial file changes |
| Decisions made | Yes | Escalation outcomes, convention choices, HITL approvals received this session |
| Git state | Yes | Last commit hash, working tree status (clean/dirty), uncommitted changes |
| Known issues | If applicable | Warnings, blockers, things that surprised the agent |
| Next action | Yes | The exact next step the incoming agent should take |

### 3.2 Timing

- **Normal end:** HITL prompts the agent. Agent produces the continuation prompt as the last action before session close.
- **Crash/forced end:** HITL reconstructs from commit history, INDEX state, and git status. The model degrades gracefully — it's designed for normal handoffs, not crash recovery.
- **Mid-AF end:** The continuation prompt includes partial AF state (files changed but not committed, decisions in flight).

### 3.3 Storage

Continuation prompts are stored in `docs/additional/prompts/` inside the governed repository.

| Location | When to use |
|----------|-------------|
| `docs/additional/prompts/` | Default — committed to the repo for traceability |
| Chat message to HITL | Fallback — paste into the next session if prompt file wasn't created |
| Session memory (if available) | Platform-specific — may not persist |

### 3.4 Inter-Agent Handoff

GVS supports multiple agent roles: Agent-I (implementation) and Agent-C (conceptual). When work passes between different agents within a sprint:

1. **HITL decides routing.** HITL assigns AFs to agents based on problem category. The assignment is explicit — in the sprint description or at gate O2.
2. **Outgoing agent** completes current AF (or reaches a clean stopping point) and commits.
3. **HITL** provides incoming agent with: sprint description, relevant AF files, continuation prompt (if available), and any session-specific context.
4. **Incoming agent** reads governance docs and sprint scope before proceeding.
5. **Handoff artifact:** The git history + AF completion sections + continuation prompt are the handoff record.

> Agents do not communicate directly. HITL mediates all inter-agent handoffs.

**Same-agent session switch vs. agent switch:**

| Scenario | Handoff source | Onboarding scope |
|----------|---------------|-----------------|
| Same agent, new session | Continuation prompt | Verify state, resume at recorded position |
| Different agent, same sprint | Continuation prompt + HITL briefing | Full governance reads + sprint scope |
| Different agent, new sprint | No continuation prompt needed | Standard sprint start (SP Phase 2) |

---

## 4. Onboarding Protocol

<!-- Kai: later we need to see if we can optimize here -->

When a new session begins mid-sprint, the incoming agent follows this sequence:

### 4.1 Mandatory Reads (extended SP Step 2.2.1)

1. All governance docs per SP Step 2.2.1 (GS, SP, sprint description, AF files, INDEX files)
2. **Continuation prompt** from the previous session (if one exists)
3. Design context documents (if referenced in sprint description)

### 4.2 State Verification

After reading, the incoming agent verifies:

- [ ] Git branch matches the continuation prompt's branch name
- [ ] Last commit hash matches (or is a known successor)
- [ ] Working tree status matches (clean/dirty as expected)
- [ ] INDEX file statuses match AF completion state described in the continuation prompt
- [ ] No unexpected files or changes in the workspace

### 4.3 Confirmation Gate

The incoming agent presents a verification summary to the HITL:
- "I've read the governance docs and continuation prompt"
- "Sprint state: X AFs done, Y remaining"
- "Current position: Phase PX, next action is Z"
- "Git state: branch B, last commit C, working tree clean/dirty"

**This is a P2-equivalent check, NOT a P2 restart.** The incoming agent resumes at the lifecycle position recorded in the continuation prompt — it does not restart from Phase 2. The P2 gate rigor (Critical severity, HITL approval required) applies to ensure the agent's understanding is correct before proceeding.

---

## 5. Cross-Cutting Nature

Session changes can occur at any lifecycle phase. The model applies uniformly:

| Phase | Session change impact | Continuation prompt includes |
|-------|----------------------|------------------------------|
| P1 (Planning) | Common — natural breakpoint between planning and execution | Sprint scope, planning decisions |
| P2 (Start) | Possible — large read phases can fill context | Read progress, questions asked/answered |
| P3 (Implementation) | Most common — AF work fills context fastest | Per-AF status, partial work state, commit history |
| P4 (Review) | Uncommon — reviews are relatively short | Review document state, HITL decision if given |
| P5 (Sprint End) | Uncommon — close ritual is mostly mechanical | Checklist progress, PR state |
| P6 (Inter-Sprint) | Rare — short phase | Grooming decisions |

---

## 6. Design Decisions

### 6.1 Why not make session changes mandatory?

Mandatory session boundaries add ceremony without proven benefit. The current evidence (Sprint 01) shows that single-session sprints work for small scope. Mandatory cadence can be evaluated after more sprints provide data.

### 6.2 Why P2-equivalent rigor for re-onboarding?

The incoming agent is in the same position as a sprint-start agent — it needs HITL confirmation that its understanding is correct before proceeding. Applying P2-level rigor (Critical, HITL approval) ensures the same quality bar without inventing a new gate. However, the agent resumes at the recorded lifecycle position, not at P2 Step 2.1.

---

## References

- Sibling source: `foundation/sources/LIFECYCLE_REGISTRY.md`
- Sibling source: `foundation/sources/FOLDER_STRUCTURE.md`

