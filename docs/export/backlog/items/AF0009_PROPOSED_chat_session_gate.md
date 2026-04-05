# AF-0009 — Chat Session Gate: Context Refresh at Session Boundaries
# Version number: v0.2
# Created: 2026-04-04
# Started:
# Completed:
# Status: PROPOSED
# Priority: P1
# Area: Process / Governance
# Models:

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> **CI workflow (CRITICAL):**
> - **During AF development:** no code changes — no targeted test run required
> - **Before commit (full gate):**
>   1. `ruff check src tests`
>   2. `ruff format --check src tests`
>   3. `pytest -W error`
>   4. `pytest --cov=src/ag --cov-report=term-missing`

---

## Metadata
- **ID:** AF-0009
- **Type:** Process
- **Status:** PROPOSED
- **Priority:** P1
- **Area:** Process / Governance
- **Owner:** Jeff + Kai
- **Target sprint:** Sprint 17 — skill_catalog_expansion
- **Phase:** TBD (needs design work before sequencing)

---

## Problem

Long inter-sprint planning sessions and multi-AF sprints accumulate context in the LLM's context window. This creates two documented failure modes:

1. **Recency/salience bias** — the most recently discussed subject displaces older constraints. The D11 violation in this session (new naming convention applied where old rules applied) is a confirmed instance of this failure.
2. **Degraded reasoning at high context depth** — no measurement exists yet, but the failure mode is known and the D11 incident provides direct evidence that it occurs.

Currently there is no formal mechanism in the governance system requiring or recommending a context refresh. The need for a new chat is communicated informally in conversation, which itself relies on the agent being aware enough to flag it — exactly the capacity that degrades when context is overloaded.

---

## Goal

- Decide whether a formal "chat session gate" is warranted and where it should live in the governance system
- If yes: define the trigger conditions, gate procedure, and responsibility (who initiates)
- Design **continuation prompt(s)** that give a fresh LLM session enough context to proceed without requiring the human to rebuild it manually
- Ensure the gate is low-overhead — not another ceremony, but a lightweight checkpoint that pays for itself by preventing D11-class errors

---

## Non-goals

- Automated context measurement (no tooling to measure token count)
- Changes to `src/`, `tests/`, or `scripts/`

---

## Design Questions (to be resolved before READY)

1. **Trigger conditions**: Always at sprint kickoff? After N minutes of planning? Human-discretionary only? Some combination?
2. **Gate location**: New G16 in the HITL table? Or a sub-procedure of G1 (sprint scope approval)?
3. **Who decides**: Agent self-flags when it detects likely context saturation? Human-initiated always? Or mandatory at defined checkpoints regardless?
4. **Continuation prompt format**: What does a good handoff prompt include?
   - Pointer to session summary file?
   - Pointer to governance plan?
   - Explicit list of active constraints (e.g., "this sprint runs under D11")?
   - Current git state summary?
5. **Scope**: Sprint kickoff only? Or also mid-sprint after long planning blocks?
6. **Coverage**: Does this apply to Jeff (planning), Jacob (implementation), or both?

---

## Candidate Continuation Prompt Structure

*(Draft — to be refined and formally decided in this AF)*

```
## Context Refresh — Sprint ## Kickoff

**Project:** ag_foundation
**Agent role:** [Jeff — planning / Jacob — implementation]
**Session start:** YYYY-MM-DDTHH:MM:SS

**Governance:**
- Active rules: GOVERNANCE_SIMPLIFICATION_PLAN_0.1.md (APPROVED)
- This sprint runs under: [old rules (D11) / new rules (post-S01)]
- HITL gates in effect: G1–G15 (see FOUNDATION_MANUAL §HITL)

**Active sprint:** Sprint ## — <name>
- AF files: docs/dev/backlog/items/AF####_*.md
- Sprint description: docs/dev/sprints/documentation/Sprint##_<name>/S##_DESCRIPTION.md
- Key constraints for this sprint: [list any D-numbered exceptions or special rules]

**Git state:**
- Branch: <branch>
- Uncommitted: [yes/no — describe]

**Read before proceeding:**
1. [Primary reference for this session]
2. [Secondary reference]

**First action required:** [e.g., "G1: present sprint scope for approval before any implementation"]
```

---

## Acceptance Criteria

*(to be defined once design questions are resolved)*

- [ ] Design questions answered and decisions documented
- [ ] Gate trigger conditions defined
- [ ] Gate location in governance system defined (new HITL gate, or sub-procedure of existing gate)
- [ ] Continuation prompt format finalized and documented
- [ ] FOUNDATION_MANUAL or SPRINT_MANUAL updated with gate definition and prompt template
- [ ] Docs impact checked: README / CLI_REFERENCE / ARCHITECTURE (updated or N/A)
- [ ] AI functionality check: N/A (no AI functionality)

---

## Files Touched

*(to be determined — depends on design decisions)*

- `docs/dev/foundation/FOUNDATION_MANUAL.md` (likely — new gate or sub-procedure)
- `docs/dev/foundation/SPRINT_MANUAL.md` (likely — sprint kickoff procedure)
- Possibly: `docs/dev/additional/CONTINUATION_PROMPT_TEMPLATE.md` (new — if prompt template warrants a standalone reference doc)

---

## Risks

**Low.** Documentation-only AF. The risk is under-specification — this AF needs real design work before implementation. The PROPOSED status reflects that.

---

## Decision Record (if applicable)

*(fill when decisions are made)*
