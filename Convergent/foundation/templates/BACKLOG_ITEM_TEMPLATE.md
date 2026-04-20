# BACKLOG ITEM — AF#### — <three_word_description>
#### Description: Template for backlog items (AFs — Action Focuses). An AF represents a discrete, atomic unit of work with clear acceptance criteria and bounded scope. Each AF progresses through the status lifecycle (PROPOSED → READY → DONE) and is tracked in INDEX_BACKLOG. Copy, rename per naming conventions (SP Appendix C.3), and fill all sections including cognitive observations.
#### Convergent: v1.3.2
#### governs: <project_name>

---

> **FOUNDATION GOVERNANCE**
> This file is governed by: `foundation/SPRINT_PLAYBOOK.md`

---

## Metadata
- **AF:** AF####
- **Type:** Foundation | Docs | Architecture | Feature | Refactor | Process
- **Owner:** <name>

- **Status:** PROPOSED | READY | BLOCKED | DONE | DEPRECATED
- **PRIORITY:** P0 | P1 | P2
- **Area:** CLI | Core Runtime | Orchestrator | Skills | Storage | Docs | Process | CI

- **PROPOSED:** DD-MM-YYYY, hh:mm
- **Started implementation:** DD-MM-YYYY, hh:mm
- **DONE:** DD-MM-YYYY, hh:mm

- **Related backlog item(s):** AF#### (optional)
- **Related bug(s):** BUG#### (optional)
- **Related PR(s):** #<number> (optional)

- **Models:**
- **Description:** (1-3 sentences)

---

## Problem
What’s missing / unclear? Why does it matter now?

---

## Goal
Concrete outcome(s). Must be verifiable.

---

## Non-goals
Explicitly out of scope.

---

## Acceptance criteria (Definition of Done)
- [ ] Deliverable exists in the correct folder
- [ ] Naming conventions applied (see FOLDER_STRUCTURE)
- [ ] INDEX file(s) updated
- [ ] C1 checks pass
- [ ] Evidence included (as applicable)
- [ ] Docs impact checked (updated or N/A)
- [ ] Completion section filled below (mandatory when Status = DONE)
- [ ] Cognitive Observations filled below (mandatory when Status = DONE)

---

## Implementation notes
Be specific: files/folders touched, rename/move steps, invariants to keep true.

---

## Risks
What could go wrong? How to mitigate?

---

# Completion section (fill when done)

## 1) Completion details
- **PR:** #<number>
- **Branch:** <feat/... | fix/... | chore/...>
- **Risk level:** P0 | P1 | P2
- **Runtime mode used for verification:** 

---

## 2) Acceptance criteria verification
Copy the AC list from above and mark it.

- [ ] ...
- [ ] ...

---

## 3) What changed (file-level)
List each file changed and what changed in 1 line.

- `<path/to/file>` — ...
- `<path/to/file>` — ...

---

## 4) Architecture alignment (mandatory) 
- **Layering:** where the logic lives and why 
- **Interfaces touched:** 
- **Backward compatibility:** any contract/schema change? (yes/no + details)

---

## 9) Risks, tradeoffs, follow-ups
- **Risks introduced:** ...
- **Tradeoffs made:** ...
- **Follow-up items to create:** AF-____ / BUG-____ / ADR-___

---


## Decision Record (if applicable)
- **Decision:** What was decided?
- **Alternatives considered:** What else was possible?
- **Rationale:** Why this choice?

---

## Cognitive Observations (mandatory before DONE)

- **Collapse events** (incomplete implementation carried forward): [count + description, or "none"]
- **Drift events** (spec changed mid-implementation): [yes/no + what changed, or "none"]
- **Repair events:** [description, or "none"]
- **LLM avoidance events:** [yes/no + description, or "none"]
- **Other observations:** [free text]

> **Type hints** (optional, use if applicable):
> data error · process skip · misinterpretation · scope violation · stale input · validation gap

---

## References

- Sprint execution: `foundation/SPRINT_PLAYBOOK.md`
