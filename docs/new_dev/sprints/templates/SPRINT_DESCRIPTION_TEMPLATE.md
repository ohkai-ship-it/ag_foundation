# SPRINT DESCRIPTION — Sprint## — <three_word_description>
# Version number: v0.2

> **Folder naming (required):** `/docs/new_dev/sprints/documentation/Sprint##_three_word_description/`  
> **Files (required):**
> - `S##_DESCRIPTION.md` (this file; includes plan + report)
> - `S##_REVIEW_01.md` (created by Jeff+Kai; executed by Jacob)
> - `S##_PR_01.md` (PR checklist for sprint finalization)

---

## 1) Metadata
- **Sprint:** Sprint##
- **Name:** <three_word_description>
- **Dates:** YYYY-MM-DD → YYYY-MM-DD
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **State:** Draft | Ready | In Progress | In Review | Accepted | Closed

---

## 2) Sprint goal
One sentence, outcome-focused.

---

## 3) Scope (what we intend to ship)

### Must-have (P0)
- AF#### — <title> (Owner: ...)
- AF#### — <title> (Owner: ...)

### Should-have (P1)
- AF#### — <title> (Owner: ...)

### Nice-to-have (P2)
- AF#### — <title> (Owner: ...)

---

## 4) Sprint start checklist (ritual)
### Jeff + Kai
- [ ] Create AFs (Status = Ready)
- [ ] Create this sprint description file
- [ ] Define sprint ID + sprint name

### Jacob
- [ ] Read sprint description
- [ ] Check AFs in `/docs/new_dev/backlog/items/`
- [ ] Ask clarifying questions in chat (no writing required)
- [ ] Create branch
- [ ] Create sprint folder
- [ ] Update INDEX files (ritual at sprint start):  
  - `/docs/new_dev/backlog/INDEX_BACKLOG.md`  
  - `/docs/new_dev/bugs/INDEX_BUGS.md`  
  - `/docs/new_dev/decisions/INDEX_DECISIONS.md`  
  - `/docs/new_dev/sprints/INDEX_SPRINTS.md`
- [ ] Confirm with Kai before starting implementation

> **INDEX update rule (strict):**  
> 1) Update when any AF/BUG/ADR/SPRINT status changes  
> 2) Also update as a ritual at sprint start

---

## 5) PR plan (expected slices)
> Rule: **1 PR = 1 primary AF item.**

- PR1: AF#### — <title> — branch `chore/...` / `feat/...` / `fix/...`
- PR2: AF#### — <title> — branch `...`

---

## 6) Definition of Done (Sprint-level)
- [ ] All P0 items are merged
- [ ] Each merged AF has its completion section filled
- [ ] Evidence captured for behavior changes (tests + RunTrace ID(s))
- [ ] Review completed (ACCEPT or ACCEPT WITH FOLLOW-UPS)
- [ ] Repo hygiene executed (per checklist)
- [ ] Indices updated and consistent

---

## 7) Risks & mitigations
- Risk: ...
  - Mitigation: ...

---

## 8) Dependencies
- Internal: ...
- External: ...

---

# Sprint report section (fill at sprint end)

## 9) Outcome summary
- Shipped:
  - ...
- Not shipped:
  - ...

---

## 10) Completed work
- ✅ AF#### — <title> (PR #...)
- ✅ AF#### — <title> (PR #...)

---

## 11) Not completed / carried over
- ⏭️ AF#### — <title> (reason + next step)

---

## 12) Evidence
- Review file(s):
  - `S##_REVIEW_01.md`
- Representative RunTrace IDs:
  - `run_...`
- Test summary:
  - `pytest ...` (PASS/FAIL)

---

## 13) Learnings
- What worked:
- What to improve:

---

## 14) Next sprint candidate slice
- P0:
- P1:
- P2:
