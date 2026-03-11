# SPRINT DESCRIPTION — Sprint09 — reliability_safety_hardening
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

> **Folder naming (required):** `/docs/dev/sprints/documentation/Sprint09_reliability_safety_hardening/`
> **Files (required):**
> - `S09_DESCRIPTION.md` (this file; includes plan + report)
> - `S09_REVIEW_01.md` (created after implementation)
> - `S09_PR_01.md` (PR checklist for sprint finalization)

---

## 1) Metadata
- **Sprint:** Sprint09
- **Name:** reliability_safety_hardening
- **Dates:** 2026-03-11 → TBD
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **State:** Active

---

## 2) Sprint goal

Harden bounded autonomy reliability and safety so Gate A conditions are provably met:
1. isolate tests and remove flakiness
2. enforce warning-clean execution (`pytest -W error`)
3. close high-impact CLI consistency gaps
4. establish policy/failure-path validation evidence

---

## 3) Scope (what we intend to ship)

### Must-have (P0/P1)
| Order | ID | Title | Owner |
|:--:|--|--|--|
| 1 | AF-0046 | Test isolation framework (+BUG-0007) | Jacob |
| 2 | AF-0071 | Warning-clean test discipline (+BUG-0012) | TBD |
| 3 | AF-0085 | CLI consistency audit | TBD |
| 4 | AF-0087 | Policy hook runtime validation baseline | TBD |

### Aggressive additions (carryover reduction)
| Order | ID | Title | Owner |
|:--:|--|--|--|
| 5 | AF-0086 | Test suite audit | TBD |
| 6 | AF-0072 | Playbook validation error | TBD |
| 7 | AF-0015 | Resolve storage DB filename mismatch | Jacob |
| 8 | AF-0083 | Artifact evidence strategy | TBD |
| 9 | AF-0057 | Playbook artifacts in trace | TBD |
| 10 | AF-0064 | Process documentation hardening | Kai |

---

## 4) Sprint start checklist (ritual)

### Kai (PM)
- [x] Create sprint description file
- [x] Create sprint folder
- [x] Define sprint ID + sprint name
- [x] Create/confirm AFs for Sprint09 scope

### Jacob (Implementer)
- [ ] Read sprint description
- [ ] Review AF files in `/docs/dev/backlog/items/`
- [ ] Create branch
- [ ] Update index files at sprint start ritual:
  - [ ] `/docs/dev/backlog/INDEX_BACKLOG.md`
  - [ ] `/docs/dev/bugs/INDEX_BUGS.md`
  - [ ] `/docs/dev/decisions/INDEX_DECISIONS.md`
  - [ ] `/docs/dev/sprints/INDEX_SPRINTS.md`
- [ ] Confirm implementation sequence with Kai

---

## 5) Technical notes

### Critical path
1. `AF-0046` must land before `AF-0071`
2. `AF-0085` runs in parallel to define scoped CLI fixes
3. `AF-0087` validates policy behavior for touched runtime paths

### Gate A alignment
- warning-clean test evidence must be captured
- isolation must hold under both happy and failure paths
- user-visible labels remain trace-derived
- workspace isolation must remain intact in failure handling

---

## 6) Exit criteria

- [ ] `pytest -W error` passes cleanly
- [ ] isolation regressions for providers/workspace resolved
- [ ] CLI consistency findings triaged with explicit follow-up mapping
- [ ] policy checks validated on touched behavior paths
- [ ] failure-path behavior is explicit and trace-aligned
- [ ] no open P0 Autonomy Gate failures at sprint close

---

## 7) Sprint report (filled at close)

### Shipped items
| ID | Status | Title |
|--|--|--|
| TBD | TBD | TBD |

### Not shipped (with reasons)
| ID | Status | Title | Reason |
|--|--|--|--|
| TBD | TBD | TBD | TBD |

### Evidence
- TBD

### Learnings
- TBD

---

## 8) PR plan
| PR | Primary AF | Branch | Status |
|--|--|--|--|
| PR-01 | Sprint09 scope | feat/sprint09-reliability-safety-hardening | Open |
