# SPRINT DESCRIPTION — Sprint04 — Process Hardening
# Version number: v0.2

> **Folder:** `/docs/dev/sprints/documentation/Sprint04_process_hardening/`

---

## 1) Metadata
- **Sprint:** Sprint04
- **Name:** process_hardening
- **Dates:** 2026-03-04 → 2026-03-10
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **State:** In Progress

---

## 2) Sprint goal
Migrate from `/docs/dev/` to `/docs/dev/` and enforce a deterministic sprint + artifact workflow (folder structure, naming conventions, templates, CI/ruff enforcement).

---

## 3) Scope (what we intend to ship)

### Must-have (P0)
- AF0039 — Create new `/docs/dev` structure + move ARCHITECTURE/CLI_REFERENCE to repo root + rename indexes (Done: prep)
- AF0041 — Backlog migration: merge templates + embed completion notes into AF items + rename/move AF items + update INDEX_BACKLOG (Owner: Jacob)
- AF0043 — Sprint system migration: per-sprint folder, combined templates, new sprint state machine, deprecate SPRINT_LOG (Owner: Jacob)
- AF0045 — CI enforcement: ruff + pytest -W error + coverage thresholds enforced via pre-commit + GitHub Actions (Owner: Jacob)

### Should-have (P1)
- AF0040 — Merge WORKFLOW/PROCESS into canonical foundation docs + eliminate duplicates + update references (Done: prep)
- AF0042 — Bugs + ADR migration: rename/move files + update templates + update INDEX files (Owner: Jacob)
- AF0044 — Review artifact migration: new review location under sprint folders; archive old `/docs/dev/reviews` (Done: prep)

### Nice-to-have (P2)
- Migrate older sprint reports (S00–S03) into the new per-sprint folder convention (as "archived")
- Add a simple "migration checklist" to the sprint folder

---

## 4) Sprint start checklist (ritual)
### Jeff + Kai
- [x] Create AFs (Status = Ready)
- [x] Create this sprint description file
- [x] Define sprint ID + sprint name

### Jacob
- [x] Read sprint description
- [x] Check AFs in `/docs/dev/backlog/items/`
- [x] Ask clarifying questions in chat
- [x] Create branch (not required — docs-only sprint)
- [x] Create sprint folder
- [x] Update INDEX files

---

## 5) PR plan (expected slices)
- PR1: AF0039 — Create `/docs/dev` skeleton + root doc moves + index renames (Done: prep)
- PR2: AF0041 — Backlog migration — branch `chore/backlog-migration`
- PR3: AF0043 — Sprint system migration — branch `chore/sprint-system`
- PR4: AF0045 — CI enforcement — branch `chore/ci-enforcement`
- PR5–PR7: AF0040/AF0042/AF0044 — Docs harmonization (Done: prep or during sprint)

---

## 6) Definition of Done (Sprint-level)
- [ ] All P0 items are merged
- [ ] Each merged AF has its completion section filled
- [ ] Evidence captured for behavior changes (tests + RunTrace ID(s))
- [ ] Review completed (ACCEPT or ACCEPT WITH FOLLOW-UPS)
- [ ] Repo hygiene executed (per checklist)

---

# Sprint Report (fill at sprint end)

## Delivered
(TBD — fill after completion)

## Not delivered / follow-ups
(TBD)

## Metrics
- Tests: TBD
- Coverage: TBD
- Ruff: TBD
