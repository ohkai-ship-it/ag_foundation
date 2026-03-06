# SPRINT DESCRIPTION — Sprint06 — skill_foundation
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
> `/docs/dev/foundation/SPRINT_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - 1 PR = 1 primary AF
> - INDEX update rule (status ↔ filename integrity)

> **Folder naming (required):** `/docs/dev/sprints/documentation/Sprint06_skill_foundation/`
> **Files (required):**
> - `S06_DESCRIPTION.md` (this file; includes plan + report)
> - `S06_REVIEW_01.md` (created by Jeff+Kai; executed by Jacob)
> - `S06_PR_01.md` (PR checklist for sprint finalization)

---

## 1) Metadata
- **Sprint:** Sprint06
- **Name:** skill_foundation
- **Dates:** 2026-03-06 → TBD
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **State:** In Progress

---

## 2) Sprint goal
Establish the skill architecture foundation that enables real LLM-powered capabilities.

GitHub clean with branching and PRs

---

## 3) Scope (what we intend to ship)

### Must-have (P0)
- AF0058 — Workspace folder restructure (inputs/, runs/<id>/) (Owner: Jacob)
- AF0060 — Skill definition framework (schemas, protocols) (Owner: Kai)

### Should-have (P1)
- AF0063 — Schema inventory documentation (Owner: Kai)
- AF0013 — Contract inventory hardening (Owner: Jacob)

### Nice-to-have (P2)
- AF0061 — Status CAPS convention (Owner: Kai)

---

## 4) Sprint start checklist (ritual)
### Jeff + Kai
- [x] Create AFs (Status = Ready)
- [x] Create this sprint description file
- [x] Define sprint ID + sprint name

### Jacob
- [x] Read sprint description
- [x] Check AFs in `/docs/dev/backlog/items/`
- [x] Ask clarifying questions in chat (no writing required)
- [x] Create branch
- [x] Create sprint folder
- [x] Update INDEX files (ritual at sprint start):  
  - `/docs/dev/backlog/INDEX_BACKLOG.md`  
  - `/docs/dev/bugs/INDEX_BUGS.md`  
  - `/docs/dev/decisions/INDEX_DECISIONS.md`  
  - `/docs/dev/sprints/INDEX_SPRINTS.md`
- [ ] Confirm with Kai before starting implementation

> **INDEX update rule (strict):**  
> 1) Update when any AF/BUG/ADR/SPRINT status changes  
> 2) Also update as a ritual at sprint start

---

## 5) PR plan (expected slices)
> Rule: **1 PR = 1 primary AF item.**

- PR1: AF0058 — Workspace folder restructure — branch `feat/workspace-restructure`
- PR2: AF0060 — Skill definition framework — branch `feat/skill-framework`
- PR3: AF0063 — Schema inventory documentation — branch `docs/schema-inventory`
- PR4: AF0013 — Contract inventory hardening — branch `docs/contract-inventory`
- PR5: AF0061 — Status CAPS convention — branch `chore/status-caps`

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
- Risk: AF0060 (skill framework) scope creep — many schemas proposed in SKILLS_ARCHITECTURE_0.1.md
  - Mitigation: Focus on core schemas only (SkillDefinition, SkillContext, SkillResult, Skill protocol). Playbook updates deferred to Sprint 07.

- Risk: AF0058 workspace restructure may break existing tests
  - Mitigation: Run all tests after implementation. Strict testing workflow documented in AF.

- Risk: Documentation AFs (AF0063, AF0013) may feel low-value
  - Mitigation: These establish the schema/contract discipline needed for Sprint 07's real skills.

---

## 8) Dependencies
- Internal:
  - AF0060 depends on AF0058 (workspace structure needed for skill I/O)
  - AF0013 should follow AF0063 (contract inventory references schema inventory)

- External:
  - Reference: `SKILLS_ARCHITECTURE_0.1.md` in `/docs/dev/additional/`

---

## 9) Key references
- [SKILLS_ARCHITECTURE_0.1.md](../../additional/SKILLS_ARCHITECTURE_0.1.md) — Architecture proposal
- [PROJECT_PLAN_0.2.md](../../foundation/PROJECT_PLAN_0.2.md) — Sprint 06 context
- [ARCHITECTURE.md](../../../../ARCHITECTURE.md) — System architecture (v0.2)

---

## 10) Autonomy context
This sprint implements **Phase 1 (Playbook-driven)** of the autonomy spectrum:
- Humans define WHAT (skills, playbooks, budgets)
- Agents decide HOW (parameters, retry, output content)

See SKILLS_ARCHITECTURE_0.1.md Section 2.1 for the full spectrum.

---

# Sprint report section (fill at sprint end)

## 11) Outcome summary
- Shipped:
  - (pending)
- Not shipped:
  - (pending)

---

## 12) Completed work
- (pending)

---

## 13) Not completed / carried over
- (pending)

---

## 14) Evidence
- Review file(s):
  - `S06_REVIEW_01.md` (pending)
- Representative RunTrace IDs:
  - (pending)
- Test summary:
  - (pending)

---

## 15) Learnings
- What worked:
  - (pending)
- What to improve:
  - (pending)

---

## 16) Next sprint candidate slice
Sprint 07 (planned):
- P0: AF0065 — First skill set (from scratch)
- P1: AF0066 — E2E integration test
- P1: AF0062 — Trace LLM model tracking
