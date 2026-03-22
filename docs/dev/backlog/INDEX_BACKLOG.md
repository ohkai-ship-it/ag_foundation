# INDEX_BACKLOG
# Version number: v1.2

> **FOUNDATION RULE**
> INDEX integrity is mandatory.
> Filename status must match internal status.
> Update required:
> - at sprint start ritual
> - whenever status changes
> See `/docs/dev/foundation/FOUNDATION_MANUAL.md` → Section 7: Index Discipline.

> **Location:** `/docs/dev/backlog/INDEX_BACKLOG.md`
> **Naming (required):** `AF####_<STATUS>_<three_word_description>.md` in `/docs/dev/backlog/items/`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`
> **Linking convention:** Filename column uses clickable links: `[🔗](items/filename)`

## Status legend
PROPOSED → READY → IN_PROGRESS → DONE (or BLOCKED / DROPPED)

---

## Active backlog (current)

### Backlog (unprioritized) *KEEP ALWAYS ON TOP*
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| *(empty)* | | | | | | |


---
## Sprints *IN DESCENDING ORDER*

### Sprint 15 Scope (llm_intelligence_layer)
| Order | ID | Priority | Status | Title | Area | Owner | Filename |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | BUG-0020 | P0 | IN_PROGRESS | Empty plan reports success | Core Runtime / Orchestrator / Verifier / CLI | Jacob | [🔗](../bugs/reports/BUG0020_OPEN_empty_plan_reports_success.md) |
| 2 | AF-0121 | P1 | IN_PROGRESS | V3Planner: feasibility assessment | Core Runtime / Planner | Jacob | [🔗](items/AF0121_READY_v3planner_feasibility_assessment.md) |
| 3 | AF-0123 | P1 | IN_PROGRESS | V2Verifier: LLM semantic quality checks | Core Runtime / Verifier | Jacob | [🔗](items/AF0123_READY_v2_verifier_semantic_checks.md) |
| 4 | AF-0124 | P2 | IN_PROGRESS | V2Executor: LLM output repair | Core Runtime / Executor | Jacob | [🔗](items/AF0124_IN_PROGRESS_v2_executor_llm_repair.md) |
| 5 | AF-0122 | P2 | READY | CLI planning and pipeline display | CLI | Jacob | [🔗](items/AF0122_READY_cli_planning_pipeline_display.md) |

### Sprint 14 Scope (pipeline_trace_hardening)
| Order | ID | Priority | Status | Title | Area | Owner | Filename |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | BUG-0019 | P1 | FIXED | V1Orchestrator drops required flag on expansion | Core Runtime/Orchestrator | Jacob | [✅](../bugs/reports/BUG0019_FIXED_orchestrator_drops_required_flag.md) |
| 2 | BUG-0018 | P1 | FIXED | V2Planner misclassifies playbook as skill | Core Runtime/Planner | Jacob | [✅](../bugs/reports/BUG0018_FIXED_v2planner_misclassifies_playbook.md) |
| 3 | AF-0116 | P1 | DONE | V1 Executor: output schema validation | Core Runtime/Executor | S14 | [✅](items/AF0116_DONE_v1_executor_output_validation.md) |
| 4 | AF-0117 | P1 | DONE | V1 Orchestrator: per-step verification (remainder) | Core Runtime/Orchestrator | S14 | [✅](items/AF0117_DONE_v1_orchestrator_perstep_loop.md) |
| 5 | AF-0118 | P1 | DONE | V1 Recorder: verification evidence | Core Runtime/Recorder | S14 | [✅](items/AF0118_DONE_v1_recorder_verification_evidence.md) |
| 6 | AF-0119 | P1 | DONE | Planner trace + per-step LLM attribution | Core Runtime/Planner/Recorder | S14 | [✅](items/AF0119_DONE_planner_trace_llm_attribution.md) |
| 7 | AF-0113 | P1 | DONE | Per-step output verification | Core Runtime/Verifier/Skills | S14 | [✅](items/AF0113_DONE_per_step_output_verification.md) |
| 8 | AF-0096 | P2 | DONE | Test workspace cleanup pollution | Testing/Storage | S14 | [✅](items/AF0096_DONE_test_workspace_cleanup.md) |
| 9 | AF-0104 | P2 | DONE | LLM Planner V3 (feasibility) | Core Runtime/Planner | Jacob | [✅](items/AF0104_DONE_llm_planner_v3_feasibility.md) |
| 10 | AF-0120 | P2 | DONE | Component manifest in RunTrace | Core Runtime/Recorder | S14 | [✅](items/AF0120_DONE_component_manifest_trace.md) |

### Sprint 13 Scope (Closed)
| Order | ID | Priority | Status | Title | Area | Owner | Filename |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF-0103 | P1 | DONE | V2 Planner: playbooks as plan steps | Core Runtime/Planner | S13 | [✅](items/AF0103_DONE_llm_planner_v2_playbooks.md) |
| 2 | AF-0112 | P1 | DONE | Inline plan preview and confirm in ag run | CLI/Runtime/Planner | Jacob | [✅](items/AF0112_DONE_inline_plan_confirm_run.md) |
| 3 | AF-0114 | P1 | DONE | Extract pipeline V0s to own files | Core Runtime/Refactor | S13 | [✅](items/AF0114_DONE_extract_pipeline_v0_files.md) |
| 4 | AF-0115 | P1 | DONE | V1 Verifier: step-aware verification | Core Runtime/Verifier | S13 | [✅](items/AF0115_DONE_v1_verifier_step_aware.md) |
| 5 | AF-0117 | P1 | DONE | V1 Orchestrator: mixed plan support (partial) | Core Runtime/Orchestrator | S13 | [✅](items/AF0117_DONE_v1_orchestrator_perstep_loop.md) |

### Sprint 12 Scope (Closed)
| Order | ID | Priority | Status | Title | Area | Owner | Filename |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF-0110 | P1 | DONE | Run layout and plan artifacts refactor | Runtime/Storage/CLI | Jacob | [✅](items/AF0110_DONE_run_layout_plan_artifacts.md) |
| 2 | AF-0108 | P1 | DONE | Unify summarization skill | Skills/Playbooks | Jacob | [✅](items/AF0108_DONE_unify_summarization_skill.md) |
| 3 | AF-0109 | P1 | DONE | emit_result strict content validation | Skills/Artifacts | Jacob | [✅](items/AF0109_DONE_emit_result_strict_content.md) |
| 4 | AF-0107 | P1 | DONE | load_documents MD inputs reliability | Skills/Storage | Jacob | [✅](items/AF0107_DONE_load_documents_md_inputs.md) |
| 5 | AF-0105 | P2 | DONE | CLI defaults fix | CLI/QA | Jacob | [✅](items/AF0105_DONE_cli_defaults_fix.md) |
| 6 | AF-0106 | P2 | DONE | V1Planner file pattern defaults | Planner/Skills | Jacob | [✅](items/AF0106_DONE_planner_file_pattern_defaults.md) |
| 7 | AF-0111 | P1 | DONE | --workspace flag must never create | CLI/Storage | Jacob | [✅](items/AF0111_DONE_workspace_flag_no_create.md) |

### Sprint 11 Scope (Closed)
| Order | ID | Priority | Status | Title | Area | Owner | Filename |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF-0102 | P1 | DONE | LLM Planner V1 (skills) | Core Runtime/Planner | Jacob | [✅](items/AF0102_DONE_llm_planner_v1_skills.md) |
| 2 | AF-0098 | P1 | DONE | Plan preview command | CLI/Planner | Jacob | [✅](items/AF0098_DONE_plan_preview_command.md) |
| 3 | AF-0099 | P1 | DONE | Plan approval workflow | CLI/Runtime | Jacob | [✅](items/AF0099_DONE_plan_approval_workflow.md) |
| 4 | AF-0100 | P1 | DONE | Step confirmation hooks | Runtime/Policy | Jacob | [✅](items/AF0100_DONE_step_confirmation_hooks.md) |
| 5 | AF-0094 | P2 | DONE | Trace full I/O enrichment | Core Runtime/Trace | Jacob | [✅](items/AF0094_DONE_trace_full_io_enrichment.md) |
| 6 | BUG-0015 | P2 | FIXED | Runs list count mismatch fix | Storage/CLI | Jacob | [✅](../bugs/reports/BUG0015_FIXED_runs_list_count_mismatch.md) |
| 7 | AF-0097 | P3 | DONE | runs commands default workspace | CLI/UX | Jacob | [✅](items/AF0097_DONE_runs_default_workspace.md) |
| 8 | AF-0101 | P3 | DONE | Autonomy level display | CLI/Trace | Jacob | [✅](items/AF0101_DONE_autonomy_level_display.md) |

### Done after Sprint 10
| ID | Status | Title | Notes | Filename |
|---:|:--|---|---|---|
| AF-0095 | DONE | research_v0 skill output audit | Audit completed, CLI fix applied | [✅](items/AF0095_DONE_research_v0_skill_output_audit.md) |

### Sprint 10 Scope (closed)
| Order | ID | Priority | Status | Title | Area | Owner | Filename |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF-0090 | P1 | DONE | Artifact truthfulness (Phase 1+3) | Core Runtime/Artifacts | Jacob | [🔗](items/AF0090_DONE_artifact_evidence_deepdive.md) |
| 2 | AF-0091 | P1 | DONE | Verifier failure-path maturity | Core Runtime/Verifier | Jacob | [🔗](items/AF0091_DONE_verifier_failure_path_maturity.md) |
| 3 | AF-0093 | P2 | DONE | Skills test coverage hardening | Skills/Testing | TBD | [🔗](items/AF0093_DONE_skills_test_coverage_hardening.md) |
| 4 | AF-0012 | P2 | DONE | CLI_REFERENCE surface parity (+BUG-0003) | CLI | Jacob | [🔗](items/AF0012_DONE_cli_reference_surface.md) |
| 5 | AF-0081 | P2 | DONE | Inventory sync discipline | Docs/Process | Jacob | [🔗](items/AF0081_DONE_inventory_sync_discipline.md) |
| 6 | AF-0082 | P2 | DONE | Report polish (rescoped) | Core Runtime/CLI | Jacob | [✅](items/AF0082_DONE_human_readable_result.md) |
| 7 | AF-0084 | P3 | DONE | Index link emoji fix | Docs/Process | Jacob | [✅](items/AF0084_DONE_index_link_emoji_fix.md) |
| 8 | AF-0077 | P3 | DONE | Skills plugin architecture (Phase 1) | Skills/Architecture | Jacob | [✅](items/AF0077_DONE_skills_plugin_architecture.md) |
| 9 | AF-0078 | P3 | DONE | Playbooks plugin architecture (Phase 1) | Playbooks/Architecture | Jacob | [✅](items/AF0078_DONE_playbooks_plugin_architecture.md) |

### Done during Sprint 10 planning
| ID | Status | Title | Notes | Filename |
|---:|:--|---|---|---|
| AF-0036 | DONE | Remove global CLI flags | ADR008 accepted (hybrid approach) | [🔗](items/AF0036_DONE_remove_global_cli.md) |

### Dropped (Sprint 10 planning)
| ID | Status | Title | Drop Reason | Filename |
|---:|:--|---|---|---|
| AF-0092 | DROPPED | Evidence CLI commands | Separate evidence concept rejected; `ag artifacts` suffices | [🔗](items/AF0092_DROPPED_evidence_cli_commands.md) |

### Sprint 09 Scope (closed)
| Order | ID | Priority | Status | Title | Area | Owner | Filename |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF-0046 | P1 | DONE | Test isolation framework (+BUG-0007) | Testing | Jacob | [🔗](items/AF0046_DONE_test_isolation_framework.md) |
| 2 | AF-0071 | P1 | DONE | Warning-clean test discipline (+BUG-0012) | Testing/Storage | Jacob | [🔗](items/AF0071_DONE_warning_clean_test_discipline.md) |
| 3 | AF-0085 | P1 | DONE | CLI consistency audit | CLI | Jacob | [🔗](items/AF0085_DONE_cli_consistency_audit.md) |
| 4 | AF-0087 | P1 | DONE | Policy hook runtime validation baseline | Core Runtime/Policy | Jacob | [🔗](items/AF0087_DONE_policy_hook_validation.md) |
| 5 | AF-0086 | P2 | DONE | Test suite audit | Testing | Jacob | [🔗](items/AF0086_DONE_test_suite_audit.md) |
| 6 | AF-0072 | P2 | DONE | Playbook validation error | CLI | Jacob | [🔗](items/AF0072_DONE_playbook_validation_error.md) |
| 7 | AF-0015 | P2 | DONE | Resolve storage DB filename mismatch | Storage | Jacob | [🔗](items/AF0015_DONE_resolve_storage_db.md) |
| 8 | AF-0083 | P1 | DONE | Artifact evidence strategy | Core Runtime | Jacob | [🔗](items/AF0083_DONE_artifact_evidence_strategy.md) |
| 9 | AF-0057 | P1 | DONE | Playbook artifacts in trace | Core Runtime | Jacob | [🔗](items/AF0057_DONE_playbook_artifacts_in_trace.md) |
| 10 | AF-0064 | P1 | DONE | Process documentation hardening | Process/Docs | Kai | [🔗](items/AF0064_DONE_process_documentation_hardening.md) |
| 11 | AF-0088 | P2 | DONE | Runs list pagination (+BUG-0014) | CLI | Jacob | [🔗](items/AF0088_DONE_runs_list_pagination.md) |
| 12 | AF-0089 | P1 | DONE | Report output format | Core Runtime/CLI | Jacob | [🔗](items/AF0089_DONE_report_output_format.md) |

### Sprint 08 Scope (closed)
| Order | ID | Priority | Status | Title | Area | Owner | Filename |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF-0073 | P2 | DONE | Index file linking convention | Docs/Process | Jacob | [🔗](items/AF0073_DONE_index_file_linking.md) |
| 2 | AF-0079 | P1 | DONE | Skills framework V1 removal | Skills/Framework | Jacob | [🔗](items/AF0079_DONE_skills_framework_v1_removal.md) |
| 3 | AF-0074 | P1 | DONE | research_v0 playbook | Playbooks/Skills | Kai | [🔗](items/AF0074_DONE_research_v0_playbook.md) |
| 4 | AF-0059 | P2 | DROPPED | Implement playbooks list | CLI | Jacob | [🔗](items/AF0059_DROPPED_implement_playbooks_list.md) |
| 5 | AF-0076 | P2 | DONE | Playbooks registry cleanup | Playbooks/Registry | TBD | [🔗](items/AF0076_DONE_playbooks_registry_cleanup.md) |
| 6 | AF-0069 | P1 | DONE | Skills architecture documentation | Skills/Architecture | Kai | [🔗](items/AF0069_DONE_skills_registry_deep_dive.md) |
| 7 | AF-0070 | P1 | DONE | Playbooks architecture documentation | Playbooks/Architecture | Kai | [🔗](items/AF0070_DONE_playbooks_registry_deep_dive.md) |
| 8 | AF-0080 | P1 | DONE | Web search skill (+BUG-0013 fix) | Skills/Playbooks | Jacob | [🔗](items/AF0080_DONE_web_search_skill.md) |


### Sprint 07 Scope (completed)
| Order | ID | Priority | Status | Title | Area | Owner | Filename |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF-0065 | P0 | DONE | First skill set (summarize_v0) | Skills | Kai | [🔗](items/AF0065_DONE_first_skill_set.md) |
| 2 | AF-0068 | P1 | DONE | Skills/playbooks folder restructure | Skills/Playbooks | Kai | [🔗](items/AF0068_DONE_skills_playbooks_folder_restructure.md) |
| 3 | AF-0066 | P1 | DONE | E2E integration test | Testing | Kai | [🔗](items/AF0066_DONE_e2e_integration_test.md) |
| 4 | AF-0062 | P1 | DONE | Trace LLM model tracking | Core | Kai | [🔗](items/AF0062_DONE_trace_llm_model_tracking.md) |
| 5 | AF-0067 | P2 | DONE | Skill code documentation | Skills/Docs | Kai | [🔗](items/AF0067_DONE_skill_code_documentation.md) |

### Sprint 06 Scope
| Order | ID | Priority | Status | Title | Area | Owner | Filename |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF-0058 | P0 | DONE | Workspace folder restructure (+DB filename) | Storage | Jacob | [🔗](items/AF0058_DONE_workspace_folder_restructure.md) |
| 2 | AF-0061 | P2 | DONE | Status CAPS convention | Docs/Process | Kai | [🔗](items/AF0061_DONE_status_caps_convention.md) |
| 3 | AF-0060 | P0 | DONE | Skill definition framework | Skills | Kai | [🔗](items/AF0060_DONE_skill_definition_framework.md) |
| 4 | AF-0063 | P1 | DONE | Schema inventory documentation | Docs/Core | Kai | [🔗](items/AF0063_DONE_schema_inventory_documentation.md) |
| 5 | AF-0013 | P1 | DONE | Contract inventory hardening | Contracts | Jacob | [🔗](items/AF0013_DONE_contract_inventory_hardening.md) |

## Sprint 05 items — completed (follow-ups)
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0047 | P0 | DONE | Foundation consolidation refactor | Docs/Process | Jacob | [🔗](items/AF0047_DONE_foundation_consolidation.md) |
| AF-0052 | P0 | DONE | Restore coverage threshold | Testing | Jacob | [🔗](items/AF0052_DONE_restore_coverage_threshold.md) |
| AF-0053 | P0 | DONE | Provider test stability | Testing | Jacob | [🔗](items/AF0053_DONE_provider_test_stability.md) |
| AF-0054 | P1 | DONE | Citation model unification | Core | Jacob | [🔗](items/AF0054_DONE_citation_model_unification.md) |
| AF-0055 | P1 | DONE | Verifier loop bounding | Verifier | Jacob | [🔗](items/AF0055_DONE_verifier_loop_bounding.md) |

## Sprint 05 items — completed (ACCEPT WITH FOLLOW-UPS)
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0048 | P0 | DONE | Structured brief skill | Skills | Jacob | [🔗](items/AF0048_DONE_structured_brief_skill.md) |
| AF-0049 | P0 | DONE | Evidence capture discipline | Core | Jacob | [🔗](items/AF0049_DONE_evidence_capture_discipline.md) |
| AF-0050 | P0 | DONE | Verifier schema loop | Verifier | Jacob | [🔗](items/AF0050_DONE_verifier_schema_loop.md) |
| AF-0051 | P1 | DONE | Artifact export hardening | Storage | Jacob | [🔗](items/AF0051_DONE_artifact_export_hardening.md) |

---

## Sprint 04 items — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0039 | P0 | DONE | Create canonical /docs/dev skeleton + root doc moves | Docs/Process | Kai/Jeff | [🔗](items/AF0039_DONE_new_dev_skeleton.md) |
| AF-0040 | P1 | DONE | Merge WORKFLOW/PROCESS into canonical foundation docs | Docs/Process | Kai/Jeff | [🔗](items/AF0040_DONE_workflow_docs_merge.md) |
| AF-0041 | P0 | DONE | Backlog migration: merge templates + rename/move AFs | Docs/Backlog | Jacob | [🔗](items/AF0041_DONE_backlog_migration.md) |
| AF-0042 | P1 | DONE | Bugs + Decisions migration: rename/move + update indexes | Docs/Bugs/Decisions | Jacob | [🔗](items/AF0042_DONE_bugs_decisions_migration.md) |
| AF-0043 | P0 | DONE | Sprint system migration: per-sprint folders + deprecate SPRINT_LOG | Docs/Sprints | Jacob | [🔗](items/AF0043_DONE_sprint_system_migration.md) |
| AF-0044 | P1 | DONE | Review artifact migration: reviews into sprint folders | Docs/Reviews | Jacob | [🔗](items/AF0044_DONE_review_migration.md) |
| AF-0045 | P0 | DONE | CI enforcement: ruff + pytest + coverage via pre-commit/Actions | CI/Quality | Jacob | [🔗](items/AF0045_DONE_ci_enforcement.md) |

---

## Sprint 03 items — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0027 | P0 | DONE | Default workspace policy (intuitive precedence) | CLI/Core/Storage | Jacob | [🔗](items/AF0027_DONE_default_workspace_policy.md) |
| AF-0028 | P0 | DONE | Run ID truncation fix | CLI | Jacob | [🔗](items/AF0028_DONE_run_id_truncation.md) |
| AF-0029 | P0 | DONE | RunTrace verification hardening | Core/Storage | Jacob | [🔗](items/AF0029_DONE_runtrace_verification_hardening.md) |
| AF-0030 | P0 | DONE | RunTrace metadata completeness (workspace_source) | Core/Storage | Jacob | [🔗](items/AF0030_DONE_runtrace_metadata_completeness.md) |
| AF-0031 | P0 | DONE | CLI truthfulness enforcement | CLI | Jacob | [🔗](items/AF0031_DONE_cli_truthfulness_enforcement.md) |
| AF-0032 | P0 | DONE | Observability command expansion | CLI | Jacob | [🔗](items/AF0032_DONE_observability_command_expansion.md) |
| AF-0033 | P0 | DONE | Early .env loading + manual mode gate fix | CLI | Jacob | [🔗](items/AF0033_DONE_early_env_loading.md) |
| AF-0034 | P0 | DONE | Workspace error message hardening (no name leakage) | CLI | Jacob | [🔗](items/AF0034_DONE_workspace_error_message.md) |
| AF-0035 | P2 | DONE | Clarify --workspace flag help text | CLI | Jacob | [🔗](items/AF0035_DONE_clarify_workspace_flag.md) |
| AF-0037 | P1 | DONE | Standardize workspace-required error messaging | CLI | Jacob | [🔗](items/AF0037_DONE_standardize_workspace_error.md) |
| AF-0038 | P1 | DONE | Ensure --json applies to error paths | CLI | Jacob | [🔗](items/AF0038_DONE_json_error_path.md) |

---

## Sprint 02 items — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0017 | P0 | DONE | OpenAI API integration (provider adapter) + config wiring | Providers | Jacob | [🔗](items/AF0017_DONE_openai_api_integration.md) |
| AF-0019 | P0 | DONE | Agent network playbook v0: delegation with multi-step trace | Kernel | Jacob | [🔗](items/AF0019_DONE_agent_network_playbook.md) |
| AF-0011 | P1 | DONE | CLI global options: --workspace/--json/--quiet/--verbose truly global | CLI | Jacob | [🔗](items/AF0011_DONE_cli_global_options.md) |
| AF-0014 | P1 | DONE | Resolve Recorder interface discrepancy (docs vs implementation) | Kernel | Jacob | [🔗](items/AF0014_DONE_resolve_recorder_interface.md) |
| AF-0018 | P1 | DONE | Provider abstraction + Claude/local stubs | Providers | Jacob | [🔗](items/AF0018_DONE_provider_abstraction_claude.md) |
| AF-0016 | P2 | DONE | Resolve contract drift: ReasoningMode enum vs examples; Artifact semantics | Contracts | Jacob | [🔗](items/AF0016_DONE_resolve_contract_drift.md) |

---

## Sprint 02 hardening extension — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0021 | P1 | DONE | Storage lifecycle hardening (SQLite deterministic closure) | Storage | Jacob | [🔗](items/AF0021_DONE_storage_lifecycle_hardening.md) |
| AF-0022 | P1 | DONE | Provider coverage hardening (≥95% target) | Providers | Jacob | [🔗](items/AF0022_DONE_provider_coverage_hardening.md) |
| AF-0023 | P1 | DONE | Environment & configuration hardening | Config | Jacob | [🔗](items/AF0023_DONE_environment_configuration_hardening.md) |
| AF-0024 | P1 | DONE | Workspace lifecycle correction (ag ws create/list) | CLI | Jacob | [🔗](items/AF0024_DONE_workspace_lifecycle_correction.md) |
| AF-0025 | P1 | DONE | Test discipline enforcement (Ruff + docs) | Testing | Jacob | [🔗](items/AF0025_DONE_test_discipline_enforcement.md) |
| AF-0026 | P0 | DONE | Workspace selection policy enforcement | CLI/Runtime | Jacob | [🔗](items/AF0026_DONE_workspace_selection_policy.md) |

---

## Sprint 01 items — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0004 | P0 | DONE | Sprint OS hygiene: sprint log + docs/dev pointers + handoff rules | Docs | Jeff | [🔗](items/AF0004_DONE_sprint_os_hygiene.md) |
| AF-0010 | P0 | DONE | Python project bootstrap (packaging + CLI stub + pytest) | Repo | Jacob | [🔗](items/AF0010_DONE_python_project_bootstrap.md) |
| AF-0005 | P0 | DONE | Contracts: TaskSpec + RunTrace + Playbook schemas v0.1 | Kernel | Jeff | [🔗](items/AF0005_DONE_contracts_taskspec_runtrace.md) |
| AF-0006 | P0 | DONE | Workspace + storage baseline (sqlite + filesystem) | Storage | Jacob | [🔗](items/AF0006_DONE_workspace_storage_baseline.md) |
| AF-0007 | P0 | DONE | Core runtime skeleton v0 (interfaces + playbook + stub skills) | Kernel | Jacob | [🔗](items/AF0007_DONE_core_runtime_skeleton.md) |
| AF-0008 | P0 | DONE | CLI v0: ag run + runs show --json, truthful labels, manual gate | CLI | Jacob | [🔗](items/AF0008_DONE_cli_ag_run.md) |
| AF-0009 | P1 | DONE | Artifact registry v0 + ag artifacts list | Storage | Jacob | [🔗](items/AF0009_DONE_artifact_registry_ag.md) |

---

## Sprint 00 items — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0001 | P0 | DONE | Kick-off: establish new docs/dev foundation | Docs/Process | Kai/Jeff | [🔗](items/AF0001_DONE_kick_off_establish.md) |
| AF-0002 | P0 | DONE | New cornerstone docs (IoT-in-space vision) | Docs/Architecture | Jeff | [🔗](items/AF0002_DONE_new_cornerstone_docs.md) |
| AF-0003 | P0 | DONE | Core runtime skeleton (request + event driven) — docs only | Architecture/Kernel | Jeff/Jacob | [🔗](items/AF0003_DONE_core_runtime_skeleton.md) |

---

## Dropped items
| ID | Status | Title | Reason | Filename |
|---:|:--|---|---|---|
| AF-0075 | DROPPED | Skills registry cleanup | Superseded by AF-0079 (V1 removal) | [🔗](items/AF0075_DROPPED_skills_registry_cleanup.md) |
| AF-0056 | DROPPED | Direct skill runs through verifier | Already fixed via BUG-0009 | [🔗](items/AF0056_DROPPED_direct_skill_runs_verifier.md) |
| AF-0059 | DROPPED | Implement playbooks list | Absorbed into AF-0076 | [🔗](items/AF0059_DROPPED_implement_playbooks_list.md) |

---

## Notes
- Bugs are tracked in `/docs/dev/bugs/INDEX_BUGS.md` (not mixed into this backlog index).
- During migration, keep IDs stable (AF-#### in content), but filenames follow the new convention above.
