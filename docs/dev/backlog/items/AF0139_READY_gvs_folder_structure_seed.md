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
- **Owner:** Jacob (GVS agent)
- **Target sprint:** GVS Sprint 1 (executed in convergent/ workspace, NOT ag_foundation)

> **NOTE:** This AF originated in ag_foundation during Sprint 16 planning. It is carried over to the convergent/GVS workspace for execution. The copy here is retained as historical record.

---

## Goal

Clean up the `gvs_development/version1.4/` folder structure — which already exists as a raw template copy — into a proper governed workspace ready for its first sprint.

**Specifically:**

1. **`hidden_layer/`** — Verify v1.3 system files (manuals, templates, folder structure specs) are present and correct. Clean any ag_foundation-specific content that was carried over from the template.
2. **`user/`** — Create clean, empty INDEX files (backlog, bugs, decisions, sprints) with correct v1.3 headers but NO ag_foundation-specific content. Zero rows in all tables.
3. **`user/foundation/`** — Write a GVS-specific PROJECT_PLAN (seed from GVS_PROJECT_PLAN_0.1.md carried over from ag_foundation).
4. **Copilot instructions** — Write `.github/copilot-instructions.md` pointing the agent at `gvs_version_fixed/version1.3/` as the governance source.

## Non-Goals

- Do NOT modify ag_foundation files (this AF runs in convergent/)
- Do NOT modify `gvs_version_fixed/version1.3/` (read-only server)
- Do NOT write sprint descriptions — that's a separate step
- Do NOT start developing v1.4 changes (hidden_layer/user split spec, external_inputs spec) — that's later GVS sprint scope

## Acceptance Criteria

- [ ] `hidden_layer/foundation/` contains FOUNDATION_MANUAL.md, SPRINT_MANUAL.md, FOLDER_STRUCTURE_0.3.md, PROJECT_PLAN_0.2.md — clean of ag_foundation-specific content
- [ ] `hidden_layer/backlog/templates/`, `bugs/templates/`, `decisions/templates/`, `sprints/templates/` each contain the correct template file from v1.3 server
- [ ] `user/backlog/INDEX_BACKLOG.md` exists with correct v1.3 header, empty sprint table
- [ ] `user/bugs/INDEX_BUGS.md` exists with correct v1.3 header, empty table
- [ ] `user/decisions/INDEX_DECISIONS.md` exists with correct v1.3 header, empty table
- [ ] `user/sprints/INDEX_SPRINTS.md` exists with correct v1.3 header, empty table
- [ ] `user/foundation/` contains GVS project plan
- [ ] `.github/copilot-instructions.md` exists with governance source reference
- [ ] No ag_foundation-specific content in any file

## Dependencies

- AF-0140 (DONE): Kai created convergent/ folder structure and populated gvs_version_fixed/version1.3/
- AF-0141: v1.3 export clean provides the cleaned server content

## References

- `docs/dev/additional/GVS_PROJECT_PLAN_0.1.md` §6.3 (bootstrap sequence)
- `docs/dev/additional/GVS_PROJECT_PLAN_0.1.md` §4.3 (folder structure)
