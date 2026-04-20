# S##_DESCRIPTION — Sprint## — <sprint_name>
#### Description: Template for sprint descriptions. A sprint description defines sprint scope, execution sequence, success criteria, risks, and dependencies. Created during Phase 1 (Sprint Planning) and maintained throughout the sprint. Copy into the sprint folder, rename per naming conventions (SP Appendix C.3), and fill all sections.
#### Convergent: v1.3.2
#### governs: <project_name>

---

> **FOUNDATION GOVERNANCE**
> This file is governed by: `foundation/SPRINT_PLAYBOOK.md`

---

## 1) Metadata
- **Sprint:** Sprint##
- **Branch:**

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

## Work Items

| ID | Title | Status | Notes |
|---:|---|:--:|---|
| AF-#### | <title> | PROPOSED / READY / DONE / BLOCKED / DEPRECATED | |
| AF-#### | <title> | PROPOSED / READY / DONE / BLOCKED / DEPRECATED | |

---

## 2) Sprint goal

One sentence, outcome-focused.

---

## 3) Scope (what we intend to ship)

### Must-have (P0)
- AF#### — <title> (Owner: ...)

### Should-have (P1)
- AF#### — <title> (Owner: ...)

### Nice-to-have (P2)
- AF#### — <title> (Owner: ...)

---

## 4) Execution sequence

*(Optional: dependency diagram or ordered list showing AF execution order)*

---

## 5) Sprint start checklist

> See SP Phase 2 for the full sprint start procedure.

### HITL
- [ ] Create AFs (Status = READY)
- [ ] Create this sprint description file
- [ ] Define sprint ID + sprint name

### Agent
- [ ] Read this sprint description
- [ ] Read all AF files in scope
- [ ] Ask clarifying questions (Gate O1)
- [ ] Create branch (Gate G2)
- [ ] Update INDEX files
- [ ] Confirm with HITL before starting implementation

---

## 6) PR plan

> See SP Phase 4 (Review) and Phase 5 (Sprint End) for PR and merge rules.

- Branch: `<type>/sprint##-<description>`
- Commit plan (in execution order):
  - AF#### — <title>
  - AF#### — <title>

---

## 7) Definition of Done (Sprint-level)
- [ ] All P0 items merged and CI passes
- [ ] All shipped AFs have completion sections filled
- [ ] Review completed (`S##_REVIEW.md` filled, decision recorded)
- [ ] Repo hygiene executed
- [ ] INDEX files updated and consistent

---

## 8) Risks & mitigations
- Risk: ...
  - Mitigation: ...

---

## 9) Dependencies
- Internal: ...
- External: ...

---

## References

- Sprint execution: `foundation/SPRINT_PLAYBOOK.md`
