# S17_DESCRIPTION — Sprint17 — gvs_migration
# Version number: v1.3
# Status: PLANNED

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
> `/docs/dev/foundation/SPRINT_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - 1 PR = 1 sprint
> - INDEX update rule

> **Folder naming (required):** `/docs/dev/sprints/documentation/Sprint17_gvs_migration/`
> **Files (required):**
> - `S17_DESCRIPTION.md` (this file — planning artifact, stable during sprint)
> - `S17_REVIEW_01.md` (outcomes artifact, written at sprint close)

> **NOTE:** This is the first sprint executing under GVS v1.3 rules.
> It is a docs-only migration sprint — no code changes, no runtime tests required.
> Pre-sprint dependency: AF-0143 (HITL active approval gates) must be completed before sprint start.

---

## 1) Metadata
- **Sprint:** Sprint17
- **Name:** gvs_migration
- **Dates:** TBD → TBD
- **Branch:** feat/sprint17-gvs-migration
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **Status:** PLANNED
- **Models:**
- **Started:**
- **Completed:**

---

## 2) Sprint goal

Complete the GVS extraction from ag_foundation: produce a clean, renumbered v1.3 export and add handoff markers throughout ag_foundation's governance docs so future agents know governance now lives in the standalone convergent/ project.

---

## 3) Scope (what we intend to ship)

### Must-have (P0)
- AF-0141 — GVS v1.3 export clean: strip runtime content, renumber all IDs from 1, produce `docs/export/` (Owner: Jacob)

### Should-have (P1)
- AF-0142 — ag_foundation GVS handoff docs: add extraction notices to FOUNDATION_MANUAL, SPRINT_MANUAL, PROJECT_PLAN, 4 INDEX files, README (Owner: Jacob)

---

## 4) Execution sequence

1. **AF-0141** — Export must be done first (AF-0142 references the export)
2. **AF-0142** — Handoff docs reference the completed export

---

## 5) Sprint start checklist (ritual)

### Jeff + Kai (pre-sprint)
- [ ] AF-0143 completed (HITL active approval gates)
- [ ] BUG-0025, BUG-0026 carried over to convergent/GVS as starting material
- [ ] Kai manually copies AF-0141 export output → `convergent/gvs_version_fixed/version1.3/`

### Jacob (sprint start)
- [ ] Read this sprint description
- [ ] Read AF-0141 and AF-0142
- [ ] Ask clarifying questions in chat
- [ ] Create branch: `feat/sprint17-gvs-migration`
- [ ] Update INDEX files (ritual at sprint start):
  - `/docs/dev/backlog/INDEX_BACKLOG.md`
  - `/docs/dev/bugs/INDEX_BUGS.md`
  - `/docs/dev/decisions/INDEX_DECISIONS.md`
  - `/docs/dev/sprints/INDEX_SPRINTS.md` (Sprint 17 → In Progress)

---

## 6) Notes

- **Docs-only sprint:** No code changes. Runtime tests not required per-AF. Full suite run at end is optional (no code touched).
- **Post-sprint manual step:** Kai copies `docs/export/` output to `convergent/gvs_version_fixed/version1.3/`, replacing the raw copy from AF-0140.
- **BUG-0025 / BUG-0026:** Not fixed in this sprint — carried to convergent/GVS as starting material for GVS Sprint 1.
