# AF-0132 — HITL Framework in Governance Docs
# Version number: v0.2
# Created: 2026-04-04
# Started:
# Completed:
# Status: READY
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
- **ID:** AF-0132
- **Type:** Process / Governance
- **Status:** READY
- **Priority:** P1
- **Area:** Process / Governance
- **Owner:** Jacob
- **Target sprint:** Sprint 16 — governance_simplification
- **Phase:** 5 (no dependencies)

---

## Problem

Human decision points and rights are implicit, scattered across SPRINT_MANUAL sections. There is no single authoritative reference for:
- When the agent **must** stop and wait for human input
- What the human can override and how
- How ad hoc chat decisions interact with documented governance rules
- What the three possible review outcomes are and what each triggers

An agent operating without a clear HITL contract defaults to either excessive escalation (slowing work) or insufficient escalation (autonomy violations). Neither is acceptable.

---

## Goal

- Single HITL Framework section in FOUNDATION_MANUAL as the authoritative reference
- All 15 mandatory gates documented and numbered (G1–G15) for traceability
- Constitutional principle formalized: chat = temporary amendment, not permanent change
- Review decision outcomes explicitly defined with consequences
- Quickfix budget rule documented (prevents scope creep on follow-ups)

---

## Non-goals

- Changing any existing gate thresholds or autonomy levels
- Changes to `src/`, `tests/`, or `scripts/`
- Genericizing gates for deployable template kit (deferred per D12)

---

## Acceptance Criteria
- [ ] FOUNDATION_MANUAL contains a dedicated HITL Framework section
- [ ] All 15 mandatory gates documented (G1–G15) in a numbered table with trigger condition
- [ ] Escalation procedure documented (document → propose options → recommend → wait)
- [ ] All four human rights documented (can override, can scope-reduce, can defer, can cancel)
- [ ] Constitutional principle stated: *"A chat instruction is a temporary amendment to the current session. It does not change the documented governance. To make a permanent change, open an AF."*
- [ ] Review decision table with all three outcomes and consequences:
  - ACCEPTED → merge, close sprint
  - ACCEPT WITH FOLLOW-UPS → merge, auto-create follow-up AFs
  - REJECTED → do not merge, reopen sprint
- [ ] Quickfix budget rule: ≤30 min cumulative per sprint review, human-overridable
- [ ] SPRINT_MANUAL references HITL Framework section at each relevant decision point
- [ ] Docs impact checked: README / CLI_REFERENCE / ARCHITECTURE (updated or N/A)
- [ ] AI functionality check: N/A (no AI functionality)

---

## Implementation Notes

### 15 Mandatory Gates (G1–G15)

| Gate | Trigger |
|---|---|
| G1 | Sprint kickoff — scope confirmed before any implementation |
| G2 | AF dependency conflict detected |
| G3 | AF acceptance criterion ambiguity |
| G4 | Proposed change touches `src/ag/core/` with no test coverage |
| G5 | New external dependency (library, service) |
| G6 | Schema breaking change |
| G7 | Contract drift detected |
| G8 | CI gate failure not resolved within 3 attempts |
| G9 | AF scope expansion beyond original spec |
| G10 | Destructive file operation (delete, overwrite without backup) |
| G11 | Credentials or secrets involved |
| G12 | PR ready for review |
| G13 | Sprint close — review decision |
| G14 | REJECTED decision — reopen criteria |
| G15 | Any action the agent assesses as irreversible |

The FOUNDATION_MANUAL section should present these in a readable table with trigger condition, agent action (stop), and expected human response.

---

## Files Touched
- `docs/dev/foundation/FOUNDATION_MANUAL.md` (new HITL Framework section)
- `docs/dev/foundation/SPRINT_MANUAL.md` (add cross-references to HITL section)

---

## Risks

**Low.** Additive documentation section. Formalizes existing implicit practice. No code changes.

---

## Completion

*(fill when Status = DONE)*
- **Review decision:**
- **Rationale:**
- **Follow-ups:**
- **PR link:**
