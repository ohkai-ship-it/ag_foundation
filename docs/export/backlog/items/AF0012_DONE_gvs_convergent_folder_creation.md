# BACKLOG ITEM — AF0012 — gvs_convergent_folder_creation
# Version number: v1.3
# Created: 2026-04-05
# Started: 2026-04-05
# Completed: 2026-04-05
# Status: DONE
# Priority: P0
# Area: Process / Governance
# Models: N/A (human task)

---

## Metadata
- **ID:** AF-0012
- **Type:** Process
- **Status:** DONE
- **Priority:** P0
- **Area:** Process / Governance
- **Owner:** Kai
- **Target sprint:** GVS Sprint 1

---

## Goal

Create the `convergent/` folder structure and populate `gvs_version_fixed/version1.3/` with a copy of ag_foundation's `docs/dev/` tree. This is the manual human prerequisite that enables AF-0011.

**Specifically:**

1. Create `convergent/gvs_version_fixed/version1.3/` — copy ag_foundation's `docs/dev/` in its entirety (monolithic, read-only server)
2. Create `convergent/gvs_development/version1.4/` — empty `hidden_layer/` and `user/` directory trees matching the v1.4 folder structure spec

## Non-Goals

- Do NOT populate files inside `gvs_development/` — that's AF-0011
- Do NOT write copilot instructions — that's AF-0011
- Do NOT start v1.4 development — that's GVS Sprint 1 scope

## Acceptance Criteria

- [x] `convergent/gvs_version_fixed/version1.3/` exists with full copy of ag_foundation `docs/dev/`
- [x] `convergent/gvs_development/version1.4/hidden_layer/` exists with correct subdirectory tree
- [x] `convergent/gvs_development/version1.4/user/` exists with correct subdirectory tree
- [x] `gvs_version_fixed/version1.3/` is treated as read-only from this point forward

## Dependencies

None — this is the first action in the GVS migration.

## References

- `docs/dev/additional/GVS_PROJECT_PLAN_0.1.md` §4.3 (folder structure)
- `docs/dev/additional/GVS_PROJECT_PLAN_0.1.md` §6.3 (bootstrap sequence, step 1–2)
