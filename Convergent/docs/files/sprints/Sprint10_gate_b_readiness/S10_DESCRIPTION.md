# SPRINT DESCRIPTION — Sprint10 — gate_b_readiness
# Version number: v0.4

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

> **Folder naming (required):** `/docs/dev/sprints/documentation/Sprint10_gate_b_readiness/`
> **Files (required):**
> - `S10_DESCRIPTION.md` (this file; includes plan + report)
> - `S10_REVIEW_01.md` (created after implementation)
> - `S10_PR_01.md` (PR checklist for sprint finalization)

---

## 1) Metadata
- **Sprint:** Sprint10
- **Name:** gate_b_readiness
- **Dates:** 2026-03-12 → 2026-03-12
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **State:** Closed

---

## 2) Sprint goal

Achieve Gate B (Guided Autonomy) readiness through four parallel tracks:
1. Artifact truthfulness & verification maturity (artifact metadata fix, trace enrichment, verifier failure-path consistency)
2. CLI completeness (surface parity with CLI_REFERENCE, global flags decision)
3. Documentation hygiene (inventory sync, report polish, index link consistency)
4. Plugin architecture foundation (skills entry points, YAML playbook loading)

---

## 3) Scope (what we intend to ship)

### Group 1: Artifact Truthfulness, Verification & Test Maturity (Gate B track)
| Order | ID | Title | Owner |
|:--:|--|--|--|
| 1 | AF-0090 | Artifact truthfulness + trace enrichment | TBD |
| 2 | AF-0091 | Verifier failure-path maturity | TBD |
| 3 | AF-0093 | Skills test coverage hardening | TBD |

### Group 2: CLI Completeness
| Order | ID | Title | Owner |
|:--:|--|--|--|
| 4 | AF-0036 | Remove global CLI flags (ADR + implementation) | TBD |
| 5 | AF-0012 | CLI_REFERENCE surface parity (+BUG-0002, BUG-0003, BUG-0011) | Jacob |

### Group 3: Documentation Hygiene
| Order | ID | Title | Owner |
|:--:|--|--|--|
| 6 | AF-0081 | Inventory sync discipline | TBD |
| 7 | AF-0082 | Report polish (rescoped after AF-0089) | TBD |
| 8 | AF-0084 | Index link emoji fix | TBD |

### Group 4: Plugin Architecture Foundation (stretch)
| Order | ID | Title | Owner |
|:--:|--|--|--|
| 9 | AF-0077 | Skills plugin architecture (Phase 1: entry points) | TBD |
| 10 | AF-0078 | Playbooks plugin architecture (Phase 1: YAML playbooks) | TBD |

### Dropped during planning
| ID | Title | Reason |
|--|--|--|
| AF-0092 | Evidence CLI commands | Separate evidence concept rejected — `ag artifacts` suffices |

### Bundled bug fixes
| Bug | Addressed by |
|-----|-------------|
| BUG-0002 | AF-0012 |
| BUG-0003 | AF-0012 |
| BUG-0011 | AF-0012 |

---

## 4) Sprint start checklist (ritual)

### Kai (PM)
- [x] Create sprint description file
- [x] Update INDEX_SPRINTS to Active
- [x] Update INDEX_BACKLOG with Sprint 10 scope table
- [x] Verify OPEN bugs triaged and linked

### Jacob (implementer)
- [x] Read sprint description
- [x] Review AF items in scope
- [x] Confirm scope feasibility
- [x] Create feature branch: `feat/sprint10-gate-b-readiness`

---

## 5) Dependencies and ordering

```
Group 1 (Evidence/Verifier) ─── parallel ─── Group 3 (Docs Hygiene)
                                              │
Group 2: AF-0036 ──blocks──> AF-0012         Group 4 (Plugin Arch)
                                              │ parallel with all
```

- Groups 1, 3, 4 are fully independent
- AF-0036 (global flags decision) should precede AF-0012 (CLI surface parity)
- AF-0077 and AF-0078 are independent of each other

---

## 6) Exit criteria

1. Artifact metadata in trace.json is truthful end-to-end (AF-0090)
2. Trace enriched with full step I/O data (AF-0090)
3. Artifact files stored in `runs/<id>/artifacts/` directory (AF-0090)
4. Verifier outcomes consistent across happy/failure paths (AF-0091)
5. Skills test coverage: fetch_web_content ≥80%, web_search ≥80%, synthesize_research ≥90% (AF-0093)
6. CLI surface matches CLI_REFERENCE for implemented commands (AF-0012)
7. Global CLI flags architecture decision documented as ADR (AF-0036)
8. Schema and contract inventories current (AF-0081)
9. Report includes polished metadata/sources/execution (AF-0082)
10. Index link emoji consistency fixed (AF-0084)
11. Skills entry points mechanism works (AF-0077)
12. YAML playbook loading + validation works (AF-0078)
13. `ruff check src tests` clean
14. `pytest -W error` passes
15. Gate B conditions assessable at sprint review

---

## 7) Gate B assessment criteria

At Sprint 10 review, evaluate:
| Gate B Condition | Evidence Source |
|------------------|----------------|
| Policy enforcement present | AF-0087 (Sprint 09) ✅ |
| Verifier/failure rigor | AF-0091 (this sprint) |
| Trace-derived labels for all new behavior | Review pass 2.5 |

---

## 8) Risk register

| Risk | Impact | Mitigation |
|------|--------|------------|
| AF-0036 decision blocks AF-0012 | CLI surface delayed | Parallelize analysis; decision can be quick |
| Plugin architecture scope creep | Sprint overload | Limit to Phase 1 only |
| AF-0090 reveals deep artifact issues | Extra work | Timeboxed investigation; create follow-up AFs if needed |
| 10 AFs is ambitious | Incomplete sprint | Groups 1+2 are must-have; Groups 3+4 can slip to Sprint 11 |

---

## 9) Report (filled at sprint close)

### What shipped
All 9 planned AFs completed plus 1 ADR:

| ID | Title | Status |
|---|---|---|
| AF-0090 | Artifact truthfulness (Phase 1+3) | ✅ DONE |
| AF-0091 | Verifier failure-path maturity | ✅ DONE |
| AF-0093 | Skills test coverage hardening | ✅ DONE |
| AF-0012 | CLI_REFERENCE surface parity | ✅ DONE |
| AF-0036 | Remove global CLI flags | ✅ DONE (planning) |
| AF-0081 | Inventory sync discipline | ✅ DONE |
| AF-0082 | Report polish | ✅ DONE |
| AF-0084 | Index link emoji fix | ✅ DONE |
| AF-0077 | Skills plugin architecture (Phase 1) | ✅ DONE |
| AF-0078 | Playbooks plugin architecture (Phase 1) | ✅ DONE |
| ADR008 | CLI global flags (hybrid approach) | ✅ ACCEPTED |

### What didn't ship (deferred)
- AF-0090 Phase 2 → AF-0094 (trace full I/O enrichment)

### New items discovered
| ID | Type | Title | Status |
|---|---|---|---|
| AF-0094 | Backlog | Trace full I/O enrichment | PROPOSED |
| AF-0095 | Backlog | research_v0 skill output audit | DONE |
| BUG-0015 | Bug | Runs list count mismatch | OPEN |

### Lessons learned
- Decisions during planning (AF-0036 → ADR008) can accelerate dependent work
- Manual testing reveals issues that automated tests miss (BUG-0015, AF-0095)
- Plugin architecture foundation enables future extensibility
- Registry-based drift detection is more reliable than manual checklists

---

## 10) PR plan
| PR | Primary AF | Branch | Status |
|--|--|--|--|
| PR-01 | Sprint 10 scope | feat/sprint10-gate-b-readiness | Merged |
