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
- **Dates:** 2026-03-11 → 2026-03-11
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **State:** Closed

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

- [x] `pytest -W error` passes cleanly
- [x] isolation regressions for providers/workspace resolved
- [x] CLI consistency findings triaged with explicit follow-up mapping
- [x] policy checks validated on touched behavior paths
- [x] failure-path behavior is explicit and trace-aligned
- [x] no open P0 Autonomy Gate failures at sprint close

---

## 7) Sprint report (filled at close)

### Shipped items
| ID | Status | Title |
|--|--|--|
| AF-0046 | DONE | Test isolation framework (+BUG-0007) |
| AF-0071 | DONE | Warning-clean test discipline (+BUG-0012) |
| AF-0085 | DONE | CLI consistency audit |
| AF-0087 | DONE | Policy hook runtime validation baseline |
| AF-0086 | DONE | Test suite audit |
| AF-0072 | DONE | Playbook validation error |
| AF-0015 | DONE | Resolve storage DB filename mismatch |
| AF-0083 | DONE | Artifact evidence strategy |
| AF-0057 | DONE | Playbook artifacts in trace |
| AF-0064 | DONE | Process documentation hardening |
| AF-0088 | DONE | Runs list pagination |
| AF-0089 | DONE | Report output format |
| BUG-0007 | FIXED | OpenAI provider test isolation failure |
| BUG-0014 | FIXED | Trace summary encoding (verified working) |

### Not shipped (with reasons)
| ID | Status | Title | Reason |
|--|--|--|--|
| (none) | — | All scope items shipped | — |

### Evidence
- **Tests:** 461 passed, 3 deselected
- **Coverage:** 86%
- **Lint:** `ruff check src tests` — All checks passed
- **Format:** `ruff format --check src tests` — 55 files already formatted
- **CI discipline:** `pytest -W error` clean

### Learnings
- Review process identified two missing scope items (AF-0088, AF-0089) which were added and completed
- UTF-8 encoding issue (BUG-0014) was Windows terminal encoding, not code bug — added regression test
- JSON output format changes require updating dependent tests across multiple files

---

## 8) PR plan
| PR | Primary AF | Branch | Status |
|--|--|--|--|
| PR-01 | Sprint09 scope | feat/sprint09-reliability-safety-hardening | Merged |
