# INDEX_BACKLOG
#### Description: Master registry of all backlog items (AFs) for ag_foundation. Tracks status, priority, sprint assignment, and ownership. INDEX row status must match the internal Status field in each AF file.
#### Convergent: v1.3.2
#### governs: ag_foundation

> **FOUNDATION RULE**
> INDEX integrity is mandatory.
> Status must match between internal file metadata and INDEX row.
> SP defines update points per phase.

---

## How to use
1. Create AFs from `foundation/templates/BACKLOG_ITEM_TEMPLATE.md`
2. Update status below

---

## Backlog (unprioritized) *KEEP ALWAYS ON TOP*
| ID | Priority | Status | Name (short) | Area | Owner | Link |
|---:|:--:|:--|---|---|---|---|
| AF0149 | P1 | READY | Add LICENSE file | Governance / IP | — | [🔗](files/backlog/AF0149_add_license_file.md) |
| AF0150 | P2 | READY | CLI `run()` complexity reduction | CLI / Code Quality | — | [🔗](files/backlog/AF0150_cli_run_complexity_reduction.md) |
| AF0146 | P2 | PROPOSED | `ag artifacts list --category` filter | CLI / Artifacts | — | [🔗](files/backlog/AF0146_artifacts_category_filter.md) |
| AF0148 | P2 | PROPOSED | Workspace isolation design | CLI / Storage / Architecture | — | [🔗](files/backlog/AF0148_workspace_isolation_design.md) |

---

## Done — No scope (inter-sprint)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0140 | P0 | DONE | GVS convergent folder creation | Process / Governance | Kai | [✅](files/backlog/AF0140_DONE_gvs_convergent_folder_creation.md) |
| 2 | AF0143 | P0 | DONE | HITL active approval gates | Process / Governance | Jacob | [✅](files/backlog/AF0143_READY_hitl_active_approval_gates.md) |
| 3 | AF0095 | — | DONE | research_v0 skill output audit | Core Runtime | — | [✅](files/backlog/AF0095_DONE_research_v0_skill_output_audit.md) |
| 4 | AF0036 | — | DONE | Remove global CLI flags | CLI | — | [🔗](files/backlog/AF0036_DONE_remove_global_cli.md) |

---

## Sprints *IN DESCENDING ORDER*

### Proposed

### Sprint XX Scope (skill_catalog_expansion)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0127 | P1 | READY | LangChain skill adapter | Skills / Plugin Architecture | Jacob | [🔗](files/backlog/AF0127_READY_langchain_skill_adapter.md) |
| 2 | AF0128 | P1 | READY | First LangChain tool batch | Skills / Capability Expansion | Jacob | [🔗](files/backlog/AF0128_READY_first_langchain_tool_batch.md) |


### Sprint 18 Scope (cli_ux_polish)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0147 | P2 | DONE | `ag playbooks show` command | CLI / Playbooks | Jacob | [✅](files/backlog/AF0147_playbooks_show_command.md) |
| 2 | AF0144 | P2 | DONE | `ag runs list` filter expansion | CLI / UX | Jacob | [✅](files/backlog/AF0144_runs_list_filter_expansion.md) |
| 3 | AF0145 | P2 | DONE | `ag doctor` diagnostic expansion | CLI / Diagnostics | Jacob | [✅](files/backlog/AF0145_doctor_diagnostic_expansion.md) |

### Sprint 17 Scope (gvs_migration)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0141 | P0 | DONE | GVS v1.3 export clean | Process / Governance | Jacob | [✅](files/backlog/AF0141_READY_gvs_v1_3_export_clean.md) |
| 2 | AF0142 | P1 | DONE | ag_foundation GVS handoff docs | Process / Docs | Jacob | [✅](files/backlog/AF0142_READY_ag_foundation_gvs_handoff_docs.md) |

### Sprint 16 Scope (governance_simplification)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0129 | P0 | DONE | Eliminate filename-status coupling | Process / Docs | Jacob | [✅](files/backlog/AF0129_DONE_eliminate_filename_status.md) |
| 2 | AF0130 | P1 | DONE | Drop redundant sprint artifacts | Process / Docs | Jacob | [✅](files/backlog/AF0130_DONE_drop_sprint_artifacts.md) |
| 3 | AF0131 | P1 | DONE | Template enhancements: time, model, docs impact | Process / Docs | Jacob | [✅](files/backlog/AF0131_DONE_template_enhancements.md) |
| 4 | AF0132 | P1 | DONE | HITL framework in governance docs | Process / Governance | Jacob | [✅](files/backlog/AF0132_DONE_hitl_framework_docs.md) |
| 5 | AF0133 | P1 | DONE | Copilot instructions: ToDo discipline | Process / Tooling | Jacob | [✅](files/backlog/AF0133_DONE_copilot_todo_discipline.md) |
| 6 | AF0134 | P1 | DONE | Streamline INDEX files | Process / Docs | Jacob | [✅](files/backlog/AF0134_DONE_streamline_index_files.md) |
| 7 | AF0138 | P1 | DONE | v1.3 transition brief | Process / Docs | Jacob | [✅](files/backlog/AF0138_DONE_v1_3_transition_brief.md) |
| 8 | AF0136 | P1 | DONE | Governance docs consolidation | Process / Docs | Jacob | [✅](files/backlog/AF0136_DONE_governance_docs_consolidation.md) |

### Sprint 15 Scope (llm_intelligence_layer)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | BUG0020 | P0 | DONE | Empty plan reports success | Core Runtime / Orchestrator / Verifier / CLI | Jacob | [✅](files/bugs/BUG0020_FIXED_empty_plan_reports_success.md) |
| 2 | AF0121 | P1 | DONE | V3Planner: feasibility assessment | Core Runtime / Planner | Jacob | [✅](files/backlog/AF0121_DONE_v3planner_feasibility_assessment.md) |
| 3 | AF0123 | P1 | DONE | V2Verifier: LLM semantic quality checks | Core Runtime / Verifier | Jacob | [✅](files/backlog/AF0123_DONE_v2_verifier_semantic_checks.md) |
| 4 | AF0124 | P2 | DONE | V2Executor: LLM output repair | Core Runtime / Executor | Jacob | [✅](files/backlog/AF0124_DONE_v2_executor_llm_repair.md) |
| 5 | AF0122 | P2 | DONE | CLI planning and pipeline display | CLI | Jacob | [✅](files/backlog/AF0122_DONE_cli_planning_pipeline_display.md) |
| 6 | AF0125 | P1 | DONE | Deterministic test provider | Testing / CI | Jacob | [✅](files/backlog/AF0125_DONE_deterministic_test_provider.md) |
| 7 | BUG0021 | P2 | DONE | ddgs/primp SSL socket GC noise in tests | Testing / CI | Jacob | [✅](files/bugs/BUG0021_FIXED_ddgs_primp_ssl_noise.md) |
| 8 | BUG0022 | P2 | DONE | V3Planner CLI test flakiness | Testing / CI | Jacob | [✅](files/bugs/BUG0022_FIXED_v3planner_cli_test_flakiness.md) |
| 9 | BUG0024 | P2 | DONE | Planner duplicates emit_result | Core Runtime / Planner | Jacob | [✅](files/bugs/BUG0024_FIXED_planner_duplicates_emit_result.md) |
| 10 | AF0126 | P1 | DONE | Executor / verifier LLM trace | Core Runtime / Trace / CLI | Jacob | [✅](files/backlog/AF0126_DONE_executor_verifier_llm_trace.md) |
| 11 | BUG0023 | P2 | DONE | V2 pipeline evidence hidden | Core Runtime / Executor / Verifier / CLI | Jacob | [✅](files/bugs/BUG0023_FIXED_v2_pipeline_evidence_hidden.md) |

### Sprint 14 Scope (pipeline_trace_hardening)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | BUG0019 | P1 | FIXED | V1Orchestrator drops required flag on expansion | Core Runtime / Orchestrator | Jacob | [✅](files/bugs/BUG0019_FIXED_orchestrator_drops_required_flag.md) |
| 2 | BUG0018 | P1 | FIXED | V2Planner misclassifies playbook as skill | Core Runtime / Planner | Jacob | [✅](files/bugs/BUG0018_FIXED_v2planner_misclassifies_playbook.md) |
| 3 | AF0116 | P1 | DONE | V1 Executor: output schema validation | Core Runtime / Executor | S14 | [✅](files/backlog/AF0116_DONE_v1_executor_output_validation.md) |
| 4 | AF0117 | P1 | DONE | V1 Orchestrator: per-step verification (remainder) | Core Runtime / Orchestrator | S14 | [✅](files/backlog/AF0117_DONE_v1_orchestrator_perstep_loop.md) |
| 5 | AF0118 | P1 | DONE | V1 Recorder: verification evidence | Core Runtime / Recorder | S14 | [✅](files/backlog/AF0118_DONE_v1_recorder_verification_evidence.md) |
| 6 | AF0119 | P1 | DONE | Planner trace + per-step LLM attribution | Core Runtime / Planner / Recorder | S14 | [✅](files/backlog/AF0119_DONE_planner_trace_llm_attribution.md) |
| 7 | AF0113 | P1 | DONE | Per-step output verification | Core Runtime / Verifier / Skills | S14 | [✅](files/backlog/AF0113_DONE_per_step_output_verification.md) |
| 8 | AF0096 | P2 | DONE | Test workspace cleanup pollution | Testing / Storage | S14 | [✅](files/backlog/AF0096_DONE_test_workspace_cleanup.md) |
| 9 | AF0104 | P2 | DONE | LLM Planner V3 (feasibility) | Core Runtime / Planner | Jacob | [✅](files/backlog/AF0104_DONE_llm_planner_v3_feasibility.md) |
| 10 | AF0120 | P2 | DONE | Component manifest in RunTrace | Core Runtime / Recorder | S14 | [✅](files/backlog/AF0120_DONE_component_manifest_trace.md) |

### Sprint 13 Scope (intelligent_pipeline)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0103 | P1 | DONE | V2 Planner: playbooks as plan steps | Core Runtime / Planner | S13 | [✅](files/backlog/AF0103_DONE_llm_planner_v2_playbooks.md) |
| 2 | AF0112 | P1 | DONE | Inline plan preview and confirm in ag run | CLI / Runtime / Planner | Jacob | [✅](files/backlog/AF0112_DONE_inline_plan_confirm_run.md) |
| 3 | AF0114 | P1 | DONE | Extract pipeline V0s to own files | Core Runtime / Refactor | S13 | [✅](files/backlog/AF0114_DONE_extract_pipeline_v0_files.md) |
| 4 | AF0115 | P1 | DONE | V1 Verifier: step-aware verification | Core Runtime / Verifier | S13 | [✅](files/backlog/AF0115_DONE_v1_verifier_step_aware.md) |
| 5 | AF0117 | P1 | DONE | V1 Orchestrator: mixed plan support (partial) | Core Runtime / Orchestrator | S13 | [✅](files/backlog/AF0117_DONE_v1_orchestrator_perstep_loop.md) |

### Sprint 12 Scope (autonomy_boundaries)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0110 | P1 | DONE | Run layout and plan artifacts refactor | Runtime / Storage / CLI | Jacob | [✅](files/backlog/AF0110_DONE_run_layout_plan_artifacts.md) |
| 2 | AF0108 | P1 | DONE | Unify summarization skill | Skills / Playbooks | Jacob | [✅](files/backlog/AF0108_DONE_unify_summarization_skill.md) |
| 3 | AF0109 | P1 | DONE | emit_result strict content validation | Skills / Artifacts | Jacob | [✅](files/backlog/AF0109_DONE_emit_result_strict_content.md) |
| 4 | AF0107 | P1 | DONE | load_documents MD inputs reliability | Skills / Storage | Jacob | [✅](files/backlog/AF0107_DONE_load_documents_md_inputs.md) |
| 5 | AF0105 | P2 | DONE | CLI defaults fix | CLI / QA | Jacob | [✅](files/backlog/AF0105_DONE_cli_defaults_fix.md) |
| 6 | AF0106 | P2 | DONE | V1Planner file pattern defaults | Planner / Skills | Jacob | [✅](files/backlog/AF0106_DONE_planner_file_pattern_defaults.md) |
| 7 | AF0111 | P1 | DONE | --workspace flag must never create | CLI / Storage | Jacob | [✅](files/backlog/AF0111_DONE_workspace_flag_no_create.md) |

### Sprint 11 Scope (guided_autonomy_enablement)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0102 | P1 | DONE | LLM Planner V1 (skills) | Core Runtime / Planner | Jacob | [✅](files/backlog/AF0102_DONE_llm_planner_v1_skills.md) |
| 2 | AF0098 | P1 | DONE | Plan preview command | CLI / Planner | Jacob | [✅](files/backlog/AF0098_DONE_plan_preview_command.md) |
| 3 | AF0099 | P1 | DONE | Plan approval workflow | CLI / Runtime | Jacob | [✅](files/backlog/AF0099_DONE_plan_approval_workflow.md) |
| 4 | AF0100 | P1 | DONE | Step confirmation hooks | Runtime / Policy | Jacob | [✅](files/backlog/AF0100_DONE_step_confirmation_hooks.md) |
| 5 | AF0094 | P2 | DONE | Trace full I/O enrichment | Core Runtime / Trace | Jacob | [✅](files/backlog/AF0094_DONE_trace_full_io_enrichment.md) |
| 6 | BUG0015 | P2 | FIXED | Runs list count mismatch fix | Storage / CLI | Jacob | [✅](files/bugs/BUG0015_FIXED_runs_list_count_mismatch.md) |
| 7 | AF0097 | P3 | DONE | runs commands default workspace | CLI / UX | Jacob | [✅](files/backlog/AF0097_DONE_runs_default_workspace.md) |
| 8 | AF0101 | P3 | DONE | Autonomy level display | CLI / Trace | Jacob | [✅](files/backlog/AF0101_DONE_autonomy_level_display.md) |

### Sprint 10 Scope (gate_b_readiness)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0090 | P1 | DONE | Artifact truthfulness (Phase 1+3) | Core Runtime / Artifacts | Jacob | [🔗](files/backlog/AF0090_DONE_artifact_evidence_deepdive.md) |
| 2 | AF0091 | P1 | DONE | Verifier failure-path maturity | Core Runtime / Verifier | Jacob | [🔗](files/backlog/AF0091_DONE_verifier_failure_path_maturity.md) |
| 3 | AF0093 | P2 | DONE | Skills test coverage hardening | Skills / Testing | TBD | [🔗](files/backlog/AF0093_DONE_skills_test_coverage_hardening.md) |
| 4 | AF0012 | P2 | DONE | CLI_REFERENCE surface parity (+BUG-0003) | CLI | Jacob | [🔗](files/backlog/AF0012_DONE_cli_reference_surface.md) |
| 5 | AF0081 | P2 | DONE | Inventory sync discipline | Docs / Process | Jacob | [🔗](files/backlog/AF0081_DONE_inventory_sync_discipline.md) |
| 6 | AF0082 | P2 | DONE | Report polish (rescoped) | Core Runtime / CLI | Jacob | [✅](files/backlog/AF0082_DONE_human_readable_result.md) |
| 7 | AF0084 | P3 | DONE | Index link emoji fix | Docs / Process | Jacob | [✅](files/backlog/AF0084_DONE_index_link_emoji_fix.md) |
| 8 | AF0077 | P3 | DONE | Skills plugin architecture (Phase 1) | Skills / Architecture | Jacob | [✅](files/backlog/AF0077_DONE_skills_plugin_architecture.md) |
| 9 | AF0078 | P3 | DONE | Playbooks plugin architecture (Phase 1) | Playbooks / Architecture | Jacob | [✅](files/backlog/AF0078_DONE_playbooks_plugin_architecture.md) |

### Sprint 09 Scope (reliability_safety_hardening)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0046 | P1 | DONE | Test isolation framework (+BUG-0007) | Testing | Jacob | [🔗](files/backlog/AF0046_DONE_test_isolation_framework.md) |
| 2 | AF0071 | P1 | DONE | Warning-clean test discipline (+BUG-0012) | Testing / Storage | Jacob | [🔗](files/backlog/AF0071_DONE_warning_clean_test_discipline.md) |
| 3 | AF0085 | P1 | DONE | CLI consistency audit | CLI | Jacob | [🔗](files/backlog/AF0085_DONE_cli_consistency_audit.md) |
| 4 | AF0087 | P1 | DONE | Policy hook runtime validation baseline | Core Runtime / Policy | Jacob | [🔗](files/backlog/AF0087_DONE_policy_hook_validation.md) |
| 5 | AF0086 | P2 | DONE | Test suite audit | Testing | Jacob | [🔗](files/backlog/AF0086_DONE_test_suite_audit.md) |
| 6 | AF0072 | P2 | DONE | Playbook validation error | CLI | Jacob | [🔗](files/backlog/AF0072_DONE_playbook_validation_error.md) |
| 7 | AF0015 | P2 | DONE | Resolve storage DB filename mismatch | Storage | Jacob | [🔗](files/backlog/AF0015_DONE_resolve_storage_db.md) |
| 8 | AF0083 | P1 | DONE | Artifact evidence strategy | Core Runtime | Jacob | [🔗](files/backlog/AF0083_DONE_artifact_evidence_strategy.md) |
| 9 | AF0057 | P1 | DONE | Playbook artifacts in trace | Core Runtime | Jacob | [🔗](files/backlog/AF0057_DONE_playbook_artifacts_in_trace.md) |
| 10 | AF0064 | P1 | DONE | Process documentation hardening | Process / Docs | Kai | [🔗](files/backlog/AF0064_DONE_process_documentation_hardening.md) |
| 11 | AF0088 | P2 | DONE | Runs list pagination (+BUG-0014) | CLI | Jacob | [🔗](files/backlog/AF0088_DONE_runs_list_pagination.md) |
| 12 | AF0089 | P1 | DONE | Report output format | Core Runtime / CLI | Jacob | [🔗](files/backlog/AF0089_DONE_report_output_format.md) |

### Sprint 08 Scope (skills_playbooks_maturity)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0073 | P2 | DONE | Index file linking convention | Docs / Process | Jacob | [🔗](files/backlog/AF0073_DONE_index_file_linking.md) |
| 2 | AF0079 | P1 | DONE | Skills framework V1 removal | Skills / Framework | Jacob | [🔗](files/backlog/AF0079_DONE_skills_framework_v1_removal.md) |
| 3 | AF0074 | P1 | DONE | research_v0 playbook | Playbooks / Skills | Kai | [🔗](files/backlog/AF0074_DONE_research_v0_playbook.md) |
| 4 | AF0059 | P2 | DROPPED | Implement playbooks list | CLI | Jacob | [🔗](files/backlog/AF0059_DROPPED_implement_playbooks_list.md) |
| 5 | AF0076 | P2 | DONE | Playbooks registry cleanup | Playbooks / Registry | TBD | [🔗](files/backlog/AF0076_DONE_playbooks_registry_cleanup.md) |
| 6 | AF0069 | P1 | DONE | Skills architecture documentation | Skills / Architecture | Kai | [🔗](files/backlog/AF0069_DONE_skills_registry_deep_dive.md) |
| 7 | AF0070 | P1 | DONE | Playbooks architecture documentation | Playbooks / Architecture | Kai | [🔗](files/backlog/AF0070_DONE_playbooks_registry_deep_dive.md) |
| 8 | AF0080 | P1 | DONE | Web search skill (+BUG-0013 fix) | Skills / Playbooks | Jacob | [🔗](files/backlog/AF0080_DONE_web_search_skill.md) |

### Sprint 07 Scope (summarize_playbook)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0065 | P0 | DONE | First skill set (summarize_v0) | Skills | Kai | [🔗](files/backlog/AF0065_DONE_first_skill_set.md) |
| 2 | AF0068 | P1 | DONE | Skills/playbooks folder restructure | Skills / Playbooks | Kai | [🔗](files/backlog/AF0068_DONE_skills_playbooks_folder_restructure.md) |
| 3 | AF0066 | P1 | DONE | E2E integration test | Testing | Kai | [🔗](files/backlog/AF0066_DONE_e2e_integration_test.md) |
| 4 | AF0062 | P1 | DONE | Trace LLM model tracking | Core | Kai | [🔗](files/backlog/AF0062_DONE_trace_llm_model_tracking.md) |
| 5 | AF0067 | P2 | DONE | Skill code documentation | Skills / Docs | Kai | [🔗](files/backlog/AF0067_DONE_skill_code_documentation.md) |

### Sprint 06 Scope (skill_foundation)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0058 | P0 | DONE | Workspace folder restructure (+DB filename) | Storage | Jacob | [🔗](files/backlog/AF0058_DONE_workspace_folder_restructure.md) |
| 2 | AF0061 | P2 | DONE | Status CAPS convention | Docs / Process | Kai | [🔗](files/backlog/AF0061_DONE_status_caps_convention.md) |
| 3 | AF0060 | P0 | DONE | Skill definition framework | Skills | Kai | [🔗](files/backlog/AF0060_DONE_skill_definition_framework.md) |
| 4 | AF0063 | P1 | DONE | Schema inventory documentation | Docs / Core | Kai | [🔗](files/backlog/AF0063_DONE_schema_inventory_documentation.md) |
| 5 | AF0013 | P1 | DONE | Contract inventory hardening | Contracts | Jacob | [🔗](files/backlog/AF0013_DONE_contract_inventory_hardening.md) |

### Sprint 05 Scope (high_pressure_skills)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0047 | P0 | DONE | Foundation consolidation refactor | Docs / Process | Jacob | [🔗](files/backlog/AF0047_DONE_foundation_consolidation.md) |
| 2 | AF0052 | P0 | DONE | Restore coverage threshold | Testing | Jacob | [🔗](files/backlog/AF0052_DONE_restore_coverage_threshold.md) |
| 3 | AF0053 | P0 | DONE | Provider test stability | Testing | Jacob | [🔗](files/backlog/AF0053_DONE_provider_test_stability.md) |
| 4 | AF0054 | P1 | DONE | Citation model unification | Core | Jacob | [🔗](files/backlog/AF0054_DONE_citation_model_unification.md) |
| 5 | AF0055 | P1 | DONE | Verifier loop bounding | Verifier | Jacob | [🔗](files/backlog/AF0055_DONE_verifier_loop_bounding.md) |
| 6 | AF0048 | P0 | DONE | Structured brief skill | Skills | Jacob | [🔗](files/backlog/AF0048_DONE_structured_brief_skill.md) |
| 7 | AF0049 | P0 | DONE | Evidence capture discipline | Core | Jacob | [🔗](files/backlog/AF0049_DONE_evidence_capture_discipline.md) |
| 8 | AF0050 | P0 | DONE | Verifier schema loop | Verifier | Jacob | [🔗](files/backlog/AF0050_DONE_verifier_schema_loop.md) |
| 9 | AF0051 | P1 | DONE | Artifact export hardening | Storage | Jacob | [🔗](files/backlog/AF0051_DONE_artifact_export_hardening.md) |

### Sprint 04 Scope (process_hardening)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0039 | P0 | DONE | Create canonical /docs/dev skeleton + root doc moves | Docs / Process | Kai/Jeff | [🔗](files/backlog/AF0039_DONE_new_dev_skeleton.md) |
| 2 | AF0040 | P1 | DONE | Merge WORKFLOW/PROCESS into canonical foundation docs | Docs / Process | Kai/Jeff | [🔗](files/backlog/AF0040_DONE_workflow_docs_merge.md) |
| 3 | AF0041 | P0 | DONE | Backlog migration: merge templates + rename/move AFs | Docs / Backlog | Jacob | [🔗](files/backlog/AF0041_DONE_backlog_migration.md) |
| 4 | AF0042 | P1 | DONE | Bugs + Decisions migration: rename/move + update indexes | Docs / Bugs / Decisions | Jacob | [🔗](files/backlog/AF0042_DONE_bugs_decisions_migration.md) |
| 5 | AF0043 | P0 | DONE | Sprint system migration: per-sprint folders + deprecate SPRINT_LOG | Docs / Sprints | Jacob | [🔗](files/backlog/AF0043_DONE_sprint_system_migration.md) |
| 6 | AF0044 | P1 | DONE | Review artifact migration: reviews into sprint folders | Docs / Reviews | Jacob | [🔗](files/backlog/AF0044_DONE_review_migration.md) |
| 7 | AF0045 | P0 | DONE | CI enforcement: ruff + pytest + coverage via pre-commit/Actions | CI / Quality | Jacob | [🔗](files/backlog/AF0045_DONE_ci_enforcement.md) |

### Sprint 03 Scope (cli_truthfulness)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0027 | P0 | DONE | Default workspace policy (intuitive precedence) | CLI / Core / Storage | Jacob | [🔗](files/backlog/AF0027_DONE_default_workspace_policy.md) |
| 2 | AF0028 | P0 | DONE | Run ID truncation fix | CLI | Jacob | [🔗](files/backlog/AF0028_DONE_run_id_truncation.md) |
| 3 | AF0029 | P0 | DONE | RunTrace verification hardening | Core / Storage | Jacob | [🔗](files/backlog/AF0029_DONE_runtrace_verification_hardening.md) |
| 4 | AF0030 | P0 | DONE | RunTrace metadata completeness (workspace_source) | Core / Storage | Jacob | [🔗](files/backlog/AF0030_DONE_runtrace_metadata_completeness.md) |
| 5 | AF0031 | P0 | DONE | CLI truthfulness enforcement | CLI | Jacob | [🔗](files/backlog/AF0031_DONE_cli_truthfulness_enforcement.md) |
| 6 | AF0032 | P0 | DONE | Observability command expansion | CLI | Jacob | [🔗](files/backlog/AF0032_DONE_observability_command_expansion.md) |
| 7 | AF0033 | P0 | DONE | Early .env loading + manual mode gate fix | CLI | Jacob | [🔗](files/backlog/AF0033_DONE_early_env_loading.md) |
| 8 | AF0034 | P0 | DONE | Workspace error message hardening (no name leakage) | CLI | Jacob | [🔗](files/backlog/AF0034_DONE_workspace_error_message.md) |
| 9 | AF0035 | P2 | DONE | Clarify --workspace flag help text | CLI | Jacob | [🔗](files/backlog/AF0035_DONE_clarify_workspace_flag.md) |
| 10 | AF0037 | P1 | DONE | Standardize workspace-required error messaging | CLI | Jacob | [🔗](files/backlog/AF0037_DONE_standardize_workspace_error.md) |
| 11 | AF0038 | P1 | DONE | Ensure --json applies to error paths | CLI | Jacob | [🔗](files/backlog/AF0038_DONE_json_error_path.md) |

### Sprint 02 Scope (provider_integration)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0017 | P0 | DONE | OpenAI API integration (provider adapter) + config wiring | Providers | Jacob | [🔗](files/backlog/AF0017_DONE_openai_api_integration.md) |
| 2 | AF0019 | P0 | DONE | Agent network playbook v0: delegation with multi-step trace | Kernel | Jacob | [🔗](files/backlog/AF0019_DONE_agent_network_playbook.md) |
| 3 | AF0011 | P1 | DONE | CLI global options: --workspace/--json/--quiet/--verbose truly global | CLI | Jacob | [🔗](files/backlog/AF0011_DONE_cli_global_options.md) |
| 4 | AF0014 | P1 | DONE | Resolve Recorder interface discrepancy (docs vs implementation) | Kernel | Jacob | [🔗](files/backlog/AF0014_DONE_resolve_recorder_interface.md) |
| 5 | AF0018 | P1 | DONE | Provider abstraction + Claude/local stubs | Providers | Jacob | [🔗](files/backlog/AF0018_DONE_provider_abstraction_claude.md) |
| 6 | AF0016 | P2 | DONE | Resolve contract drift: ReasoningMode enum vs examples; Artifact semantics | Contracts | Jacob | [🔗](files/backlog/AF0016_DONE_resolve_contract_drift.md) |

### Sprint 02H Scope (hardening_extension)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0021 | P1 | DONE | Storage lifecycle hardening (SQLite deterministic closure) | Storage | Jacob | [🔗](files/backlog/AF0021_DONE_storage_lifecycle_hardening.md) |
| 2 | AF0022 | P1 | DONE | Provider coverage hardening (≥95% target) | Providers | Jacob | [🔗](files/backlog/AF0022_DONE_provider_coverage_hardening.md) |
| 3 | AF0023 | P1 | DONE | Environment & configuration hardening | Config | Jacob | [🔗](files/backlog/AF0023_DONE_environment_configuration_hardening.md) |
| 4 | AF0024 | P1 | DONE | Workspace lifecycle correction (ag ws create/list) | CLI | Jacob | [🔗](files/backlog/AF0024_DONE_workspace_lifecycle_correction.md) |
| 5 | AF0025 | P1 | DONE | Test discipline enforcement (Ruff + docs) | Testing | Jacob | [🔗](files/backlog/AF0025_DONE_test_discipline_enforcement.md) |
| 6 | AF0026 | P0 | DONE | Workspace selection policy enforcement | CLI / Runtime | Jacob | [🔗](files/backlog/AF0026_DONE_workspace_selection_policy.md) |

### Sprint 01 Scope (project_bootstrap)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0004 | P0 | DONE | Sprint OS hygiene: sprint log + docs/dev pointers + handoff rules | Docs | Jeff | [🔗](files/backlog/AF0004_DONE_sprint_os_hygiene.md) |
| 2 | AF0010 | P0 | DONE | Python project bootstrap (packaging + CLI stub + pytest) | Repo | Jacob | [🔗](files/backlog/AF0010_DONE_python_project_bootstrap.md) |
| 3 | AF0005 | P0 | DONE | Contracts: TaskSpec + RunTrace + Playbook schemas v0.1 | Kernel | Jeff | [🔗](files/backlog/AF0005_DONE_contracts_taskspec_runtrace.md) |
| 4 | AF0006 | P0 | DONE | Workspace + storage baseline (sqlite + filesystem) | Storage | Jacob | [🔗](files/backlog/AF0006_DONE_workspace_storage_baseline.md) |
| 5 | AF0007 | P0 | DONE | Core runtime skeleton v0 (interfaces + playbook + stub skills) | Kernel | Jacob | [🔗](files/backlog/AF0007_DONE_core_runtime_skeleton.md) |
| 6 | AF0008 | P0 | DONE | CLI v0: ag run + runs show --json, truthful labels, manual gate | CLI | Jacob | [🔗](files/backlog/AF0008_DONE_cli_ag_run.md) |
| 7 | AF0009 | P1 | DONE | Artifact registry v0 + ag artifacts list | Storage | Jacob | [🔗](files/backlog/AF0009_DONE_artifact_registry_ag.md) |

### Sprint 00 Scope (kick_off)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF0001 | P0 | DONE | Kick-off: establish new docs/dev foundation | Docs / Process | Kai/Jeff | [🔗](files/backlog/AF0001_DONE_kick_off_establish.md) |
| 2 | AF0002 | P0 | DONE | New cornerstone docs (IoT-in-space vision) | Docs / Architecture | Jeff | [🔗](files/backlog/AF0002_DONE_new_cornerstone_docs.md) |
| 3 | AF0003 | P0 | DONE | Core runtime skeleton (request + event driven) — docs only | Architecture / Kernel | Jeff/Jacob | [🔗](files/backlog/AF0003_DONE_core_runtime_skeleton.md) |

---

## Blocked
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|

---

## Deprecated *KEEP ALWAYS AT BOTTOM*
| ID | Priority | Status | Name (short) | Area | Owner | Link |
|---:|:--:|:--|---|---|---|---|
| AF0092 | — | DROPPED | Evidence CLI commands | CLI | — | [🔗](files/backlog/AF0092_DROPPED_evidence_cli_commands.md) |
| AF0075 | — | DROPPED | Skills registry cleanup | Skills | — | [🔗](files/backlog/AF0075_DROPPED_skills_registry_cleanup.md) |
| AF0056 | — | DROPPED | Direct skill runs through verifier | Core Runtime | — | [🔗](files/backlog/AF0056_DROPPED_direct_skill_runs_verifier.md) |

---

## References

- Sprint execution: `foundation/SPRINT_PLAYBOOK.md`
