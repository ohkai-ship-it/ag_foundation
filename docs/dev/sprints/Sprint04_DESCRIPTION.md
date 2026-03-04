# Sprint04 — Process Hardening
# Version number: v0.1 (new sprint system)

## Metadata
- **Sprint:** Sprint04 — process_hardening
- **Dates:** 2026-03-04 → 2026-03-10 (proposal; adjust in repo if needed)
- **Owner:** Kai (PM)
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **Primary goal:** Migrate from `/docs/dev/` to `/docs/new_dev/` and enforce a deterministic sprint + artifact workflow (folder structure, naming conventions, templates, CI/ruff enforcement).

---

## Context / why this sprint exists
Current docs and process are fragmented across multiple folders (`/cornerstone`, `/team`, `/engineering`, `/sprints`, `/backlog`) and are not consistently enforced. The target is a *single coherent operating system* with:
- one place per artifact type,
- strict naming + status conventions,
- sprint folders with description+review+PR evidence,
- CI enforcement (ruff, pytest -W error, coverage thresholds),
- clean separation between legacy `/docs/dev/` and the new canonical `/docs/new_dev/`.

**Important migration rule:** During this sprint, `/docs/dev/` remains the “legacy baseline”. `/docs/new_dev/` becomes the “new baseline”. We do not delete `/docs/dev/` until the sprint review accepts the migration.

---

## Scope (what we intend to ship)

### Must-have (P0)
- **AF0039** — Create new `/docs/new_dev` structure + move ARCHITECTURE/CLI_REFERENCE to repo root + rename indexes
- **AF0041** — Backlog migration: merge templates + embed completion notes into AF items + rename/move AF items + update INDEX_BACKLOG
- **AF0043** — Sprint system migration: per-sprint folder, combined templates, new sprint state machine, deprecate SPRINT_LOG
- **AF0045** — CI enforcement: ruff + pytest -W error + coverage thresholds enforced via pre-commit + GitHub Actions

### Should-have (P1)
- **AF0040** — Merge WORKFLOW/PROCESS into canonical foundation docs + eliminate duplicates + update references
- **AF0042** — Bugs + ADR migration: rename/move files + update templates + update INDEX files
- **AF0044** — Review artifact migration: new review location under sprint folders; archive old `/docs/dev/reviews`

### Nice-to-have (P2)
- Migrate older sprint reports (S00–S03) into the new per-sprint folder convention (as “archived”)
- Add a simple “migration checklist” to the sprint folder (`artifacts/migration_checklist.txt`)

---

## Sprint-level Definition of Done
- [ ] All P0 AF items are **Done**
- [ ] Sprint review decision recorded as **ACCEPT** or **ACCEPT WITH FOLLOW-UPS**
- [ ] New canonical structure exists under `/docs/new_dev/` and is internally consistent
- [ ] No broken references from root docs (README, ARCHITECTURE, CLI_REFERENCE) to new docs locations
- [ ] CI passes and blocks merges when:
  - ruff check fails
  - ruff format --check fails
  - pytest emits warnings (pytest -W error)
  - coverage drops below thresholds
- [ ] INDEX files updated (ritual at sprint start + on every status change)

---

## Operating rules (this sprint)
### Dual-structure rule (explicit)
- **Legacy:** `/docs/dev/` (read-only baseline; changes only as needed to add deprecation pointers)
- **Canonical:** `/docs/new_dev/` (all new work lands here)
- Deletions in `/docs/dev/` happen only after review acceptance.

### PR rule (still strict)
- One PR = one primary AF item.
- Docs-only PRs allowed; they still require template + evidence (commands may be N/A).

---

## Sprint phases (new workflow)

### Sprint start (agreed final version)
Jeff + Kai:
- Create AFs (status = Ready)
- Create sprint description file
- Define sprint ID + name

Jacob:
- Clarify questions (chat only; no writing needed)
- Create branch
- Create sprint folder
- Update INDEX files (ritual check; Jeff/Kai may have added AFs/BUGs/ADRs)

### Sprint execution
Jacob:
- Implement AFs in order (P0 then P1)
- One PR per AF
- No shortcuts: ask before quick+dirty solutions
- Update statuses in:
  1) file name
  2) internal Metadata field
  3) INDEX file

### Sprint end / review cycle
Jeff + Kai:
- Create `S04_REVIEW_01.md` in sprint folder

Jacob:
- Execute review tasks + attach evidence under `artifacts/`

Jeff + Kai:
- Decide: ACCEPT / ACCEPT WITH FOLLOW-UPS / REJECT

### Finalize sprint (only after accept)
Jacob:
- Repo hygiene
- Final index updates
- Create `S04_PR_01.md`
- Open PR for final merge (if any “meta PR” is used for docs-only consolidation)

---

## PR plan (expected slices)
- PR1 (AF0039): Create `/docs/new_dev` skeleton + root doc moves + index renames
- PR2 (AF0041): Backlog migration (templates + AF files + completion note merge)
- PR3 (AF0043): Sprint system migration (templates + new folder + deprecations)
- PR4 (AF0045): CI enforcement (pre-commit + GitHub Actions)
- PR5–PR7 (AF0040/AF0042/AF0044): Docs harmonization + bug/ADR + review migration

---

## Risks & mitigations
- **Risk:** breaking links/references during moves  
  **Mitigation:** add deprecation stubs in `/docs/dev/` pointing to new locations, and include a “link audit” checklist in review.

- **Risk:** too-large PRs due to many renamed docs  
  **Mitigation:** keep migration PRs docs-only; do not mix code changes unless CI enforcement requires it.

- **Risk:** index drift  
  **Mitigation:** index update ritual at sprint start + update on every status change.

---

## Deliverables in repo (paths)
All deliverables for this sprint live in:

- Sprint folder (canonical):
  - `docs/new_dev/sprints/documentation/Sprint04_process_hardening/S04_DESCRIPTION.md`
  - `docs/new_dev/sprints/documentation/Sprint04_process_hardening/S04_REVIEW_01.md`
  - `docs/new_dev/sprints/documentation/Sprint04_process_hardening/S04_PR_01.md`
  - `docs/new_dev/sprints/documentation/Sprint04_process_hardening/artifacts/`

- AF items (canonical):
  - `docs/new_dev/backlog/items/AF0039_Ready_...md` etc.
