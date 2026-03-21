# Pass 1 — Scope verification
# Date: 2026-03-21
# Executor: Jacob

## AF files existence check (after Pass 0.5 corrections)

| ID | File | Status | Exists |
|---|---|---|---|
| AF-0094 | AF0094_DONE_trace_full_io_enrichment.md | DONE | ✓ |
| AF-0097 | AF0097_DONE_runs_default_workspace.md | DONE | ✓ |
| AF-0098 | AF0098_DONE_plan_preview_command.md | DONE | ✓ |
| AF-0099 | AF0099_DONE_plan_approval_workflow.md | DONE | ✓ |
| AF-0100 | AF0100_DONE_step_confirmation_hooks.md | DONE | ✓ |
| AF-0101 | AF0101_DONE_autonomy_level_display.md | DONE | ✓ |
| AF-0102 | AF0102_DONE_llm_planner_v1_skills.md | DONE | ✓ |
| BUG-0015 | BUG0015_FIXED_runs_list_count_mismatch.md | FIXED | ✓ |

## Index verification

| Index | Updated |
|---|---|
| INDEX_BACKLOG.md | ✓ Sprint 11 items all DONE/FIXED |
| INDEX_BUGS.md | ✓ BUG-0015 shows FIXED |

## CLI_REFERENCE.md updates

- [x] Added `ag run --plan <plan_id>` to synopsis
- [x] Added "Plan execution mode" section
- [x] Added full `ag plan` command group documentation:
  - `ag plan generate`
  - `ag plan show`
  - `ag plan list`
  - `ag plan delete`
- [x] Added V1Planner description
- [x] Added examples

## Verification summary
All scope items verified. Documentation updated to match implementation.
