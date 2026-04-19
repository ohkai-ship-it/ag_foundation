# ag_foundation Pre-Migration Cleanup Prompt

> **Context:** This prompt is produced by convergent (AF-0045, Step B) for Jeff (ag_foundation agent) to execute. It cleans up ag_foundation's `docs/dev/` folder BEFORE the v1.3.2 governance migration begins. All steps operate on `docs/dev/` inside the ag_foundation workspace.
>
> **Date:** 2026-04-18
> **Produced by:** Conny (convergent agent), AF-0045

---

## Overview

ag_foundation's `docs/dev/` folder has accumulated 33 OneDrive sync-conflict files (`-DESKTOP-FR9RV0G` suffix), 16 leftover old-status duplicate files, and 3 bugs whose filenames don't match their actual status. This prompt walks through all cleanup steps in order.

**Execution rules:**
- Execute steps in the order listed (Phase 1 → Phase 2 → Phase 3 → Phase 4).
- Within each phase, work item by item. Show Kai what you're doing before each delete/rename.
- Do NOT batch deletes silently — confirm each group with Kai.
- Do NOT modify file content unless explicitly instructed.
- Commit after each phase (not after each file).

---

## Phase 1: Resolve 33 OneDrive Conflict Files

OneDrive created `-DESKTOP-FR9RV0G` copies when files were edited on two machines. Analysis shows two categories:

### Phase 1A: Delete 12 line-ending-only DESKTOP files

These 12 files are textually identical to their originals — the only difference is CRLF vs LF line endings. The originals are correct. **Delete the DESKTOP copies.**

| # | File to DELETE | Location |
|---|---|---|
| 1 | `AF0039_DONE_new_dev_skeleton-DESKTOP-FR9RV0G.md` | `backlog/items/` |
| 2 | `AF0041_DONE_backlog_migration-DESKTOP-FR9RV0G.md` | `backlog/items/` |
| 3 | `AF0042_DONE_bugs_decisions_migration-DESKTOP-FR9RV0G.md` | `backlog/items/` |
| 4 | `AF0043_DONE_sprint_system_migration-DESKTOP-FR9RV0G.md` | `backlog/items/` |
| 5 | `AF0044_DONE_review_migration-DESKTOP-FR9RV0G.md` | `backlog/items/` |
| 6 | `AF0045_DONE_ci_enforcement-DESKTOP-FR9RV0G.md` | `backlog/items/` |
| 7 | `BUG0004_FIXED_sqlite_connections_not-DESKTOP-FR9RV0G.md` | `bugs/reports/` |
| 8 | `BUG0005_FIXED_implicit_workspace_creation-DESKTOP-FR9RV0G.md` | `bugs/reports/` |
| 9 | `BUG0006_FIXED_manual_mode_ignores-DESKTOP-FR9RV0G.md` | `bugs/reports/` |
| 10 | `ADR001_ACCEPTED_architecture_baseline-DESKTOP-FR9RV0G.md` | `decisions/files/` |
| 11 | `ADR002_ACCEPTED_trace_versioning_strategy-DESKTOP-FR9RV0G.md` | `decisions/files/` |
| 12 | `ADR003_ACCEPTED_manual_mode_gating-DESKTOP-FR9RV0G.md` | `decisions/files/` |
| 13 | `ADR004_ACCEPTED_storage_baseline-DESKTOP-FR9RV0G.md` | `decisions/files/` |
| 14 | `ADR005_ACCEPTED_orchestrator_threshold-DESKTOP-FR9RV0G.md` | `decisions/files/` |

**Action:** Delete all 14 files listed above. (Note: the ADR count is 5, bringing the total to 14 not 12 — the 5 ADRs were originally grouped as "3" in the analysis but there are 5 individual files.)

### Phase 1B: Replace 19 originals with their DESKTOP versions

These 19 files have real content differences. In every case, the DESKTOP version is the newer, more complete version. The original is a stale snapshot.

**Action for each:** Delete the original → rename the DESKTOP file to the original's name.

#### 1B-1: INDEX files (4 files)

| # | Original (DELETE) | DESKTOP (RENAME to original) | What DESKTOP adds |
|---|---|---|---|
| 1 | `backlog/INDEX_BACKLOG.md` | `backlog/INDEX_BACKLOG-DESKTOP-FR9RV0G.md` | Full S00–S18 backlog (all 150 AFs), v1.3.1 header, legacy notes |
| 2 | `bugs/INDEX_BUGS.md` | `bugs/INDEX_BUGS-DESKTOP-FR9RV0G.md` | All 26 bugs, v1.3.1 header |
| 3 | `decisions/INDEX_DECISIONS.md` | `decisions/INDEX_DECISIONS-DESKTOP-FR9RV0G.md` | ADR006–010, v1.3.1 header |
| 4 | `sprints/INDEX_SPRINTS.md` | `sprints/INDEX_SPRINTS-DESKTOP-FR9RV0G.md` | Sprints 06–18, v1.3.1 header |

#### 1B-2: Foundation/system docs (4 files)

| # | Original (DELETE) | DESKTOP (RENAME to original) | What DESKTOP adds |
|---|---|---|---|
| 5 | `foundation/FOUNDATION_MANUAL.md` | `foundation/FOUNDATION_MANUAL-DESKTOP-FR9RV0G.md` | +136 lines: v1.3.1 header, §1.5 commit/PR discipline, full content |
| 6 | `foundation/SPRINT_MANUAL.md` | `foundation/SPRINT_MANUAL-DESKTOP-FR9RV0G.md` | +189 lines: v1.3.1 header, HITL framework refs |
| 7 | `foundation/PROJECT_PLAN_0.2.md` | `foundation/PROJECT_PLAN_0.2-DESKTOP-FR9RV0G.md` | +352 lines: v1.3.1 header, full project description |
| 8 | `foundation/FOLDER_STRUCTURE_0.2.md` | `foundation/FOLDER_STRUCTURE_0.2-DESKTOP-FR9RV0G.md` | Reformatted tree view |

#### 1B-3: Templates (5 files)

| # | Original (DELETE) | DESKTOP (RENAME to original) | What DESKTOP adds |
|---|---|---|---|
| 9 | `backlog/templates/BACKLOG_ITEM_TEMPLATE.md` | `backlog/templates/BACKLOG_ITEM_TEMPLATE-DESKTOP-FR9RV0G.md` | v1.3.1 header, timestamps, naming rules |
| 10 | `bugs/templates/BUG_REPORT_TEMPLATE.md` | `bugs/templates/BUG_REPORT_TEMPLATE-DESKTOP-FR9RV0G.md` | v1.3.1 header, model format, naming convention |
| 11 | `decisions/templates/ADR_TEMPLATE.md` | `decisions/templates/ADR_TEMPLATE-DESKTOP-FR9RV0G.md` | v1.3.1 header, model format, naming convention |
| 12 | `sprints/templates/PULL_REQUEST_TEMPLATE.md` | `sprints/templates/PULL_REQUEST_TEMPLATE-DESKTOP-FR9RV0G.md` | v1.3.1 header, sprint work items format |
| 13 | `sprints/templates/SPRINT_DESCRIPTION_TEMPLATE.md` | `sprints/templates/SPRINT_DESCRIPTION_TEMPLATE-DESKTOP-FR9RV0G.md` | v1.3.1 header (restructured, fewer lines but more current) |

#### 1B-4: additional/ docs (3 files)

| # | Original (DELETE) | DESKTOP (RENAME to original) | What DESKTOP adds |
|---|---|---|---|
| 14 | `additional/CONTRACT_INVENTORY.md` | `additional/CONTRACT_INVENTORY-DESKTOP-FR9RV0G.md` | PlanStore, ArtifactStore entries |
| 15 | `additional/SCHEMA_INVENTORY.md` | `additional/SCHEMA_INVENTORY-DESKTOP-FR9RV0G.md` | Step, StepConfirmation, PlanningLLMCall, PipelineManifest schemas |
| 16 | `additional/SKILLS_ARCHITECTURE_0.1.md` | `additional/SKILLS_ARCHITECTURE_0.1-DESKTOP-FR9RV0G.md` | Cross-reference links |

#### 1B-5: Bug reports (3 files)

| # | Original (DELETE) | DESKTOP (RENAME to original) | What DESKTOP adds |
|---|---|---|---|
| 17 | `bugs/reports/BUG0002_OPEN_missing_ag_run.md` | `bugs/reports/BUG0002_OPEN_missing_ag_run-DESKTOP-FR9RV0G.md` | Related items (AF-0085 audit), Sprint 08 progress |
| 18 | `bugs/reports/BUG0003_OPEN_missing_cli_subcommands.md` | `bugs/reports/BUG0003_OPEN_missing_cli_subcommands-DESKTOP-FR9RV0G.md` | Related items, Sprint 09 status table |
| 19 | `bugs/reports/BUG0011_OPEN_default_workspace_name_leaked.md` | `bugs/reports/BUG0011_OPEN_default_workspace_name_leaked-DESKTOP-FR9RV0G.md` | DROPPED status, drop reason, link to AF-0148 |

**Commit after Phase 1:** `cleanup: resolve 33 OneDrive conflict files`

---

## Phase 2: Delete 16 Leftover Old-Status Duplicate Files

When AFs transition from PROPOSED → READY → DONE (or DROPPED), the old-status file should have been deleted. These 16 files are stale copies — the current-status version is the one that matches INDEX_BACKLOG.

**Rule:** For each AF/BUG below, KEEP the file whose status matches the INDEX entry. DELETE all others.

### Backlog duplicates (15 files to delete)

| AF | INDEX status | KEEP | DELETE |
|----|-------------|------|--------|
| AF-0012 | DONE | `AF0012_DONE_cli_reference_surface.md` | `AF0012_PROPOSED_cli_reference_surface.md` |
| AF-0015 | DONE | `AF0015_DONE_resolve_storage_db.md` | `AF0015_PROPOSED_resolve_storage_db.md`, `AF0015_READY_resolve_storage_db.md` |
| AF-0036 | DONE | `AF0036_DONE_remove_global_cli.md` | `AF0036_PROPOSED_remove_global_cli.md` |
| AF-0046 | DONE | `AF0046_DONE_test_isolation_framework.md` | `AF0046_PROPOSED_test_isolation_framework.md`, `AF0046_READY_test_isolation_framework.md` |
| AF-0056 | DROPPED | `AF0056_DROPPED_direct_skill_runs_verifier.md` | `AF0056_PROPOSED_direct_skill_runs_verifier.md` |
| AF-0057 | DONE | `AF0057_DONE_playbook_artifacts_in_trace.md` | `AF0057_PROPOSED_skill_emits_trace_artifacts_evidence.md` |
| AF-0059 | DROPPED | `AF0059_DROPPED_implement_playbooks_list.md` | `AF0059_PROPOSED_implement_playbooks_list.md`, `AF0059_READY_implement_playbooks_list.md` |
| AF-0062 | DONE | `AF0062_DONE_trace_llm_model_tracking.md` | `AF0062_PROPOSED_trace_llm_model_tracking.md` |
| AF-0064 | DONE | `AF0064_DONE_process_documentation_hardening.md` | `AF0064_PROPOSED_process_documentation_hardening.md` |
| AF-0065 | DONE | `AF0065_DONE_first_skill_set.md` | `AF0065_PROPOSED_first_skill_set.md` |
| AF-0066 | DONE | `AF0066_DONE_e2e_integration_test.md` | `AF0066_PROPOSED_e2e_integration_test.md` |
| AF-0138 | DONE | `AF0138_DONE_v1_3_transition_brief.md` | `AF0138_READY_v1_3_transition_brief.md` |

### Bug duplicate (1 file to delete)

| BUG | INDEX status | KEEP | DELETE |
|-----|-------------|------|--------|
| BUG-0007 | FIXED | `BUG0007_FIXED_openai_test_isolation.md` | `BUG0007_OPEN_openai_test_isolation.md` |

**Total:** 16 files to delete.

**Commit after Phase 2:** `cleanup: delete 16 leftover old-status duplicate files`

---

## Phase 3: Fix 3 DROPPED Bug Filenames

INDEX_BUGS shows BUG-0002, BUG-0003, and BUG-0011 as DROPPED, but the files on disk still have `_OPEN_` in the filename. Rename to match the INDEX status.

| Current filename | New filename |
|---|---|
| `BUG0002_OPEN_missing_ag_run.md` | `BUG0002_DROPPED_missing_ag_run.md` |
| `BUG0003_OPEN_missing_cli_subcommands.md` | `BUG0003_DROPPED_missing_cli_subcommands.md` |
| `BUG0011_OPEN_default_workspace_name_leaked.md` | `BUG0011_DROPPED_default_workspace_name_leaked.md` |

**Important:** BUG-0002 and BUG-0003 also need their internal metadata updated to match:
- Change `- **Status:** OPEN` → `- **Status:** DROPPED` inside the file
- Add DROPPED date and reason if not already present (check the DESKTOP version content that was installed in Phase 1B-5 — BUG-0011 already has this from the DESKTOP version)

**Verify:** After renaming, confirm that INDEX_BUGS rows and file metadata both say DROPPED for all three.

**Commit after Phase 3:** `cleanup: rename 3 DROPPED bugs from OPEN to DROPPED filenames`

---

## Phase 4: Delete Sprint 13 Duplicate PR File

Sprint 13 has both an old-convention and new-convention PR file:
- `S13_PR_01.md` (old naming)
- `S13_PULL_REQUEST.md` (new naming)

Both exist in `sprints/documentation/S13/` (or equivalent S13 folder).

**Action:** Keep `S13_PULL_REQUEST.md` (current convention). Delete `S13_PR_01.md`.

**Verify:** Check that INDEX_SPRINTS links to the correct file, or that no explicit link exists (sprint PR files are typically not linked from the INDEX).

**Commit after Phase 4:** `cleanup: delete duplicate S13 PR file`

---

## Post-Cleanup Verification

After all 4 phases, verify:

1. **No `-DESKTOP-FR9RV0G` files remain:**
   ```
   Get-ChildItem docs/dev -Recurse -File | Where-Object Name -like "*DESKTOP*"
   ```
   Expected: 0 results.

2. **No duplicate AF files remain:**
   For each AF ID, there should be exactly one file in `backlog/items/`.
   ```
   Get-ChildItem docs/dev/backlog/items -File | Group-Object {$_.Name.Substring(0,6)} | Where-Object Count -gt 1
   ```
   Expected: 0 groups (except AF-0135, AF-0137, AF-0139 which are GVS-carried-over — ignore these for now).

3. **No duplicate BUG files remain:**
   ```
   Get-ChildItem docs/dev/bugs/reports -File | Group-Object {$_.Name.Substring(0,7)} | Where-Object Count -gt 1
   ```
   Expected: 0 groups.

4. **Bug filename status matches INDEX status:**
   BUG-0002 → DROPPED in filename and INDEX
   BUG-0003 → DROPPED in filename and INDEX
   BUG-0011 → DROPPED in filename and INDEX
   BUG-0007 → FIXED (only FIXED copy remains)

5. **File count sanity check:**
   - Before cleanup: 422 files
   - Phase 1A deletes: 14 files
   - Phase 1B replaces: 19 pairs (net 0 — delete + rename)
   - Phase 2 deletes: 16 files
   - Phase 3 renames: 3 files (net 0)
   - Phase 4 deletes: 1 file
   - Expected after cleanup: 422 - 14 - 16 - 1 = **391 files**

---

## Summary

| Phase | Action | Files affected |
|-------|--------|---------------|
| 1A | Delete 14 line-ending-only DESKTOP copies | -14 |
| 1B | Replace 19 originals with DESKTOP versions | 0 net (19 delete + 19 rename) |
| 2 | Delete 16 old-status AF/BUG duplicates | -16 |
| 3 | Rename 3 DROPPED bugs (OPEN → DROPPED filename) | 0 net |
| 4 | Delete S13 duplicate PR file | -1 |
| **Total** | | **-31 files** |
