# BACKLOG ITEM — AF0139 — gvs_folder_structure_seed
# Version number: v1.3
# Created: 2026-04-05
# Started:
# Completed:
# Status: READY
# Priority: P1
# Area: Process / Governance
# Models:

---

## Metadata
- **ID:** AF-0139
- **Type:** Process
- **Status:** READY
- **Priority:** P1
- **Area:** Process / Governance
- **Owner:** Kai
- **Target sprint:** Unassigned (pre-Sprint 17, standalone task)

---

## Goal

Populate the `gvs_development/version1.4/` folder structure with correct governance files seeded from ag_foundation's `docs/dev/`. This is the first step of the GVS migration — after this AF, the convergent project is ready for its first governed sprint.

**Specifically:**

1. **`hidden_layer/`** — Seed with v1.3 system files (manuals, templates, folder structure specs) copied from ag_foundation. These are the starting point that GVS Sprint 1 will evolve into v1.4.
2. **`user/`** — Create clean, empty INDEX files (backlog, bugs, decisions, sprints) with correct v1.3 headers but NO ag_foundation-specific content. Zero rows in all tables.
3. **`user/foundation/`** — Write a GVS-specific PROJECT_PLAN (seed from GVS_PROJECT_PLAN_0.1.md in ag_foundation's additional/).
4. **Copilot instructions** — Write `.github/copilot-instructions.md` pointing the agent at `gvs_version_fixed/version1.3/` as the governance source.

## Non-Goals

- Do NOT modify ag_foundation files
- Do NOT modify `gvs_version_fixed/version1.3/` (that's already seeded by Kai)
- Do NOT write sprint descriptions — that's a separate step
- Do NOT start developing v1.4 changes (hidden_layer/user split spec, external_inputs spec) — that's GVS Sprint 1 scope

## Acceptance Criteria

- [ ] `hidden_layer/foundation/` contains FOUNDATION_MANUAL.md, SPRINT_MANUAL.md, FOLDER_STRUCTURE_0.3.md, PROJECT_PLAN_0.2.md — all copied from v1.3 server
- [ ] `hidden_layer/backlog/templates/`, `bugs/templates/`, `decisions/templates/`, `sprints/templates/` each contain the correct template file copied from v1.3 server
- [ ] `user/backlog/INDEX_BACKLOG.md` exists with correct v1.3 header, empty sprint table
- [ ] `user/bugs/INDEX_BUGS.md` exists with correct v1.3 header, empty table
- [ ] `user/decisions/INDEX_DECISIONS.md` exists with correct v1.3 header, empty table
- [ ] `user/sprints/INDEX_SPRINTS.md` exists with correct v1.3 header, empty table
- [ ] `user/foundation/` contains GVS project plan
- [ ] `.github/copilot-instructions.md` exists with governance source reference
- [ ] No ag_foundation-specific content in any user/ INDEX file

## Dependencies

- Kai must have already created the `convergent/` folder structure and populated `gvs_version_fixed/version1.3/`

## References

- `docs/dev/additional/GVS_PROJECT_PLAN_0.1.md` §6.3 (bootstrap sequence)
- `docs/dev/additional/GVS_PROJECT_PLAN_0.1.md` §4.3 (folder structure)
