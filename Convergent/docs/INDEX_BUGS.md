# INDEX_BUGS
#### Description: Master registry of all bug reports for ag_foundation. Tracks status, priority, sprint assignment, and ownership. INDEX row status must match the internal Status field in each BUG file.
#### Convergent: v1.3.2
#### governs: ag_foundation

> **FOUNDATION RULE**
> INDEX integrity is mandatory.
> Status must match between internal file metadata and INDEX row.
> SP defines update points per phase.

---

## How to use
1. Create bug report from `foundation/templates/BUG_REPORT_TEMPLATE.md`
2. Link bug from PR and/or AF item
3. Update status below

---

## Proposed
| ID | Priority | Status | Name (short) | Area | Owner | Link |
|---:|:--:|:--|---|---|---|---|
| BUG0025 | P2 | OPEN | Leftover READY duplicates (5 AF files) | Process | — | [🔗](files/bugs/BUG0025_OPEN_leftover_ready_duplicates.md) |
| BUG0026 | P2 | OPEN | PR template version gap (v0.2 → v1.3) | Docs | — | [🔗](files/bugs/BUG0026_OPEN_pr_template_version_gap.md) |

---

## Ready
| ID | Priority | Status | Name (short) | Area | Owner | Link |
|---:|:--:|:--|---|---|---|---|

---

## Done
| ID | Priority | Status | Name (short) | Area | Owner | Link |
|---:|:--:|:--|---|---|---|---|
| BUG0024 | P2 | FIXED | Planner duplicates emit_result | Core Runtime / Planner | — | [✅](files/bugs/BUG0024_FIXED_planner_duplicates_emit_result.md) |
| BUG0023 | P2 | FIXED | V2 pipeline evidence hidden | Core Runtime / Executor / Verifier / CLI | — | [✅](files/bugs/BUG0023_FIXED_v2_pipeline_evidence_hidden.md) |
| BUG0022 | P2 | FIXED | V3Planner CLI test flakiness | Testing / CI | — | [✅](files/bugs/BUG0022_FIXED_v3planner_cli_test_flakiness.md) |
| BUG0021 | P2 | FIXED | ddgs/primp SSL socket GC noise in tests | Testing / CI | — | [✅](files/bugs/BUG0021_FIXED_ddgs_primp_ssl_noise.md) |
| BUG0020 | P0 | FIXED | Empty plan reports success | Core Runtime / Orchestrator / Verifier / CLI | — | [✅](files/bugs/BUG0020_FIXED_empty_plan_reports_success.md) |
| BUG0019 | P1 | FIXED | V1Orchestrator drops required flag on expansion | Core Runtime / Orchestrator | — | [✅](files/bugs/BUG0019_FIXED_orchestrator_drops_required_flag.md) |
| BUG0018 | P1 | FIXED | V2Planner misclassifies playbook as skill | Core Runtime / Planner | — | [✅](files/bugs/BUG0018_FIXED_v2planner_misclassifies_playbook.md) |
| BUG0017 | P1 | FIXED | Verifier ignores optional step failures | Core Runtime / Verifier | — | [✅](files/bugs/BUG0017_FIXED_verifier_ignores_optional_steps.md) |
| BUG0016c | P1 | FIXED | Accumulated chaining loss (multi-emit data lost) | Core Runtime | — | [✅](files/bugs/BUG0016c_FIXED_accumulated_chaining_loss.md) |
| BUG0016b | P1 | FIXED | Alias placeholder override (emit_result) | Skills | — | [✅](files/bugs/BUG0016b_FIXED_alias_placeholder_override.md) |
| BUG0016 | P1 | FIXED | Plan steps not executed (--plan ignores planned_steps) | Core Runtime | — | [✅](files/bugs/BUG0016_FIXED_plan_steps_not_executed.md) |
| BUG0015 | P2 | FIXED | Runs list count mismatch (orphaned index) | Storage / CLI | — | [✅](files/bugs/BUG0015_FIXED_runs_list_count_mismatch.md) |
| BUG0014 | P2 | FIXED | Trace summary encoding degradation | Core Runtime / Trace | — | [✅](files/bugs/BUG0014_FIXED_trace_summary_encoding.md) |
| BUG0013 | P1 | FIXED | research_v0 playbook pipeline broken | Playbooks / Runtime | — | [✅](files/bugs/BUG0013_FIXED_research_v0_pipeline_broken.md) |
| BUG0012 | P2 | FIXED | Test workspace cleanup pollution | Testing / Storage | — | [✅](files/bugs/BUG0012_FIXED_test_workspace_cleanup.md) |
| BUG0010 | P0 | FIXED | Skill trace missing artifacts evidence | Core / Recorder / Skills | — | [✅](files/bugs/BUG0010_FIXED_skill_trace_missing_artifacts.md) |
| BUG0009 | P0 | FIXED | Direct skill skips verifier | CLI / Core / Verifier | — | [✅](files/bugs/BUG0009_FIXED_direct_skill_skips_verifier.md) |
| BUG0008 | P0 | FIXED | CLI cannot route to strategic_brief skill | CLI / Routing | — | [✅](files/bugs/BUG0008_FIXED_skill_routing_missing.md) |
| BUG0007 | P1 | FIXED | OpenAI provider test isolation failure | Testing | — | [✅](files/bugs/BUG0007_FIXED_openai_test_isolation.md) |
| BUG0006 | P1 | FIXED | Manual mode ignores .env AG_DEV | CLI | — | [✅](files/bugs/BUG0006_FIXED_manual_mode_ignores.md) |
| BUG0005 | P0 | FIXED | Implicit workspace creation on ag run | CLI / Storage | — | [✅](files/bugs/BUG0005_FIXED_implicit_workspace_creation.md) |
| BUG0004 | P1 | FIXED | SQLite connections not closed → ResourceWarning | Storage | — | [✅](files/bugs/BUG0004_FIXED_sqlite_connections_not.md) |
| BUG0001 | P1 | FIXED | Global CLI options not implemented as global | CLI | — | [✅](files/bugs/BUG0001_FIXED_global_cli_options.md) |

---

## Blocked
| ID | Priority | Status | Name (short) | Area | Owner | Link |
|---:|:--:|:--|---|---|---|---|

---

## Deprecated
| ID | Priority | Status | Name (short) | Area | Owner | Link |
|---:|:--:|:--|---|---|---|---|
| BUG0002 | P2 | DROPPED | Missing ag run options per CLI reference | CLI | — | [🔗](files/bugs/BUG0002_OPEN_missing_ag_run.md) |
| BUG0003 | P2 | DROPPED | Missing CLI subcommands per reference spec | CLI | — | [🔗](files/bugs/BUG0003_OPEN_missing_cli_subcommands.md) |
| BUG0011 | P2 | DROPPED | Default workspace name leaked in error | CLI | — | [🔗](files/bugs/BUG0011_OPEN_default_workspace_name_leaked.md) |

---

## References

- Sprint execution: `foundation/SPRINT_PLAYBOOK.md`
