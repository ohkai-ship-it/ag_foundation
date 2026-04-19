# Sprint 10 Scope Links
# Generated: 2026-03-12

## Completed AFs (Sprint 10)

| ID | Status | Filename | Link |
|---|---|---|---|
| AF-0090 | DONE | AF0090_DONE_artifact_evidence_deepdive.md | [🔗](../../../../../backlog/items/AF0090_DONE_artifact_evidence_deepdive.md) |
| AF-0091 | DONE | AF0091_DONE_verifier_failure_path_maturity.md | [🔗](../../../../../backlog/items/AF0091_DONE_verifier_failure_path_maturity.md) |
| AF-0093 | DONE | AF0093_DONE_skills_test_coverage_hardening.md | [🔗](../../../../../backlog/items/AF0093_DONE_skills_test_coverage_hardening.md) |
| AF-0012 | DONE | AF0012_DONE_cli_reference_surface.md | [🔗](../../../../../backlog/items/AF0012_DONE_cli_reference_surface.md) |
| AF-0036 | DONE | AF0036_DONE_remove_global_cli.md | [🔗](../../../../../backlog/items/AF0036_DONE_remove_global_cli.md) |
| AF-0081 | DONE | AF0081_DONE_inventory_sync_discipline.md | [🔗](../../../../../backlog/items/AF0081_DONE_inventory_sync_discipline.md) |
| AF-0082 | DONE | AF0082_DONE_human_readable_result.md | [🔗](../../../../../backlog/items/AF0082_DONE_human_readable_result.md) |
| AF-0084 | DONE | AF0084_DONE_index_link_emoji_fix.md | [🔗](../../../../../backlog/items/AF0084_DONE_index_link_emoji_fix.md) |
| AF-0077 | DONE | AF0077_DONE_skills_plugin_architecture.md | [🔗](../../../../../backlog/items/AF0077_DONE_skills_plugin_architecture.md) |
| AF-0078 | DONE | AF0078_DONE_playbooks_plugin_architecture.md | [🔗](../../../../../backlog/items/AF0078_DONE_playbooks_plugin_architecture.md) |

## ADR Created

| ID | Status | Filename | Link |
|---|---|---|---|
| ADR-0008 | ACCEPTED | ADR008_ACCEPTED_cli_global_flags.md | [🔗](../../../../../decisions/files/ADR008_ACCEPTED_cli_global_flags.md) |

## Dropped

| ID | Status | Filename | Reason |
|---|---|---|---|
| AF-0092 | DROPPED | AF0092_DROPPED_evidence_cli_commands.md | Separate evidence concept rejected; `ag artifacts` suffices |

## New Items (discovered during sprint)

| ID | Type | Status | Filename |
|---|---|---|---|
| AF-0094 | Backlog | PROPOSED | AF0094_PROPOSED_trace_full_io_enrichment.md |
| AF-0095 | Backlog | PROPOSED | AF0095_PROPOSED_research_v0_skill_output_audit.md |
| BUG-0015 | Bug | OPEN | BUG0015_OPEN_runs_list_count_mismatch.md |

## Indices Updated

- `/docs/dev/backlog/INDEX_BACKLOG.md` (v0.8)
- `/docs/dev/decisions/INDEX_DECISIONS.md` (v0.4)
- `/docs/dev/bugs/INDEX_BUGS.md` (check pending)
- `CLI_REFERENCE.md` (v0.4)

## Key Changes Summary

### CLI Architecture (ADR008)
- `--workspace` remains the only global flag
- `--json`, `--quiet`, `--verbose` moved to command-level
- Hybrid approach chosen over full removal or full retention

### Plugin Architecture
- Skills: Entry points mechanism via `ag.skills` group
- Playbooks: YAML loading from `~/.ag/playbooks/` (Option A chosen)

### Inventory Sync
- Registry-based drift detection in `test_documentation_drift.py`
- Automated enforcement via CI (blocks merge if schemas undocumented)

---

## Pass 1 Verification (S10_REVIEW_01)
Date: 2026-03-12

### Files Verified
- [x] All 10 sprint AF files exist with DONE status
- [x] ADR-0008 exists with ACCEPTED status
- [x] AF-0092 exists with DROPPED status
- [x] AF-0094, AF-0095 exist with PROPOSED status
- [x] BUG-0015 exists with OPEN status

### Issues Found
Stale files with old statuses (need cleanup post-review):
- AF0077_READY_skills_plugin_architecture.md
- AF0078_READY_playbooks_plugin_architecture.md
- AF0081_IN_PROGRESS_inventory_sync_discipline.md
- AF0082_IN_PROGRESS_human_readable_result.md
- AF0084_READY_index_link_emoji_fix.md

### Checklist
- [x] Confirm each AF file exists in /docs/dev/backlog/items/
- [x] Confirm filename Status matches internal Status field
- [x] Confirm indices include all new/changed items
- [x] Confirm ADR008 is in INDEX_DECISIONS.md
