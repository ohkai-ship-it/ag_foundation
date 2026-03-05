# INDEX_BACKLOG
# Version number: v0.2

> **FOUNDATION RULE**
> INDEX integrity is mandatory.
> Filename status must match internal status.
> Update required:
> - at sprint start ritual
> - whenever status changes
> See `/docs/dev/foundation/FOUNDATION_MANUAL.md` → Section 7: Index Discipline.

> **Location:** `/docs/dev/backlog/INDEX_BACKLOG.md`
> **Naming (required):** `AF####_<Status>_<three_word_description>.md` in `/docs/dev/backlog/items/`
> Status values: `Proposed | Ready | In progress | Blocked | Done | Dropped`

## Status legend
Proposed → Ready → In progress → Done (or Blocked / Dropped)

---

## Active backlog (current)
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0056 | P0 | Ready | Direct skill runs through verifier | CLI/Core/Verifier | Jacob | `AF0056_Ready_direct_skill_runs_verifier.md` |
| AF-0057 | P0 | Ready | Skill emits trace artifacts evidence | Core/Recorder/Skills | Jacob | `AF0057_Ready_skill_emits_trace_artifacts_evidence.md` |
| AF-0058 | P1 | Ready | Workspace folder restructure | Storage | Jacob | `AF0058_Ready_workspace_folder_restructure.md` |
| AF-0059 | P2 | Ready | Implement playbooks list | CLI | Jacob | `AF0059_Ready_implement_playbooks_list.md` |
| AF-0060 | P1 | Proposed | Skill definition framework | Skills | Kai | `AF0060_Proposed_skill_definition_framework.md` |
| AF-0061 | P2 | Proposed | Status CAPS convention | Docs/Process | Kai | `AF0061_Proposed_status_caps_convention.md` |
| AF-0062 | P1 | Proposed | Trace LLM model tracking | Core | Kai | `AF0062_Proposed_trace_llm_model_tracking.md` |
| AF-0063 | P2 | Proposed | Schema inventory documentation | Docs/Core | Kai | `AF0063_Proposed_schema_inventory_documentation.md` |
| AF-0064 | P1 | Proposed | Sprint PR timing clarification | Process/Docs | Kai | `AF0064_Proposed_sprint_pr_timing_clarification.md` |
| AF-0046 | P1 | Proposed | Test isolation framework for providers | Testing | Jacob | `AF0046_Proposed_test_isolation_framework.md` |
| AF-0012 | P2 | Ready | CLI_REFERENCE surface parity v0.1 (partial — if capacity) | CLI | Jacob | `AF0012_Ready_cli_reference_surface.md` |
| AF-0013 | P1 | Ready | Contract inventory hardening: reconcile docs ↔ implementation | Contracts | Jacob | `AF0013_Ready_contract_inventory_hardening.md` |
| AF-0015 | P2 | Ready | Resolve storage DB filename mismatch (docs vs code) | Storage | Jacob | `AF0015_Ready_resolve_storage_db.md` |
| AF-0036 | P1 | Proposed | Remove global CLI flags (needs design) | CLI | Jacob | `AF0036_Proposed_remove_global_cli.md` |

---

## Sprint 05 items — completed (follow-ups)
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0047 | P0 | Done | Foundation consolidation refactor | Docs/Process | Jacob | `AF0047_Done_foundation_consolidation.md` |
| AF-0052 | P0 | Done | Restore coverage threshold | Testing | Jacob | `AF0052_Done_restore_coverage_threshold.md` |
| AF-0053 | P0 | Done | Provider test stability | Testing | Jacob | `AF0053_Done_provider_test_stability.md` |
| AF-0054 | P1 | Done | Citation model unification | Core | Jacob | `AF0054_Done_citation_model_unification.md` |
| AF-0055 | P1 | Done | Verifier loop bounding | Verifier | Jacob | `AF0055_Done_verifier_loop_bounding.md` |

## Sprint 05 items — completed (ACCEPT WITH FOLLOW-UPS)
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0048 | P0 | Done | Structured brief skill | Skills | Jacob | `AF0048_Done_structured_brief_skill.md` |
| AF-0049 | P0 | Done | Evidence capture discipline | Core | Jacob | `AF0049_Done_evidence_capture_discipline.md` |
| AF-0050 | P0 | Done | Verifier schema loop | Verifier | Jacob | `AF0050_Done_verifier_schema_loop.md` |
| AF-0051 | P1 | Done | Artifact export hardening | Storage | Jacob | `AF0051_Done_artifact_export_hardening.md` |

---

## Sprint 04 items — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0039 | P0 | Done | Create canonical /docs/dev skeleton + root doc moves | Docs/Process | Kai/Jeff | `AF0039_Done_new_dev_skeleton.md` |
| AF-0040 | P1 | Done | Merge WORKFLOW/PROCESS into canonical foundation docs | Docs/Process | Kai/Jeff | `AF0040_Done_workflow_docs_merge.md` |
| AF-0041 | P0 | Done | Backlog migration: merge templates + rename/move AFs | Docs/Backlog | Jacob | `AF0041_Done_backlog_migration.md` |
| AF-0042 | P1 | Done | Bugs + Decisions migration: rename/move + update indexes | Docs/Bugs/Decisions | Jacob | `AF0042_Done_bugs_decisions_migration.md` |
| AF-0043 | P0 | Done | Sprint system migration: per-sprint folders + deprecate SPRINT_LOG | Docs/Sprints | Jacob | `AF0043_Done_sprint_system_migration.md` |
| AF-0044 | P1 | Done | Review artifact migration: reviews into sprint folders | Docs/Reviews | Jacob | `AF0044_Done_review_migration.md` |
| AF-0045 | P0 | Done | CI enforcement: ruff + pytest + coverage via pre-commit/Actions | CI/Quality | Jacob | `AF0045_Done_ci_enforcement.md` |

---

## Sprint 03 items — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0027 | P0 | Done | Default workspace policy (intuitive precedence) | CLI/Core/Storage | Jacob | `AF0027_Done_default_workspace_policy.md` |
| AF-0028 | P0 | Done | Run ID truncation fix | CLI | Jacob | `AF0028_Done_run_id_truncation.md` |
| AF-0029 | P0 | Done | RunTrace verification hardening | Core/Storage | Jacob | `AF0029_Done_runtrace_verification_hardening.md` |
| AF-0030 | P0 | Done | RunTrace metadata completeness (workspace_source) | Core/Storage | Jacob | `AF0030_Done_runtrace_metadata_completeness.md` |
| AF-0031 | P0 | Done | CLI truthfulness enforcement | CLI | Jacob | `AF0031_Done_cli_truthfulness_enforcement.md` |
| AF-0032 | P0 | Done | Observability command expansion | CLI | Jacob | `AF0032_Done_observability_command_expansion.md` |
| AF-0033 | P0 | Done | Early .env loading + manual mode gate fix | CLI | Jacob | `AF0033_Done_early_env_loading.md` |
| AF-0034 | P0 | Done | Workspace error message hardening (no name leakage) | CLI | Jacob | `AF0034_Done_workspace_error_message.md` |
| AF-0035 | P2 | Done | Clarify --workspace flag help text | CLI | Jacob | `AF0035_Done_clarify_workspace_flag.md` |
| AF-0037 | P1 | Done | Standardize workspace-required error messaging | CLI | Jacob | `AF0037_Done_standardize_workspace_error.md` |
| AF-0038 | P1 | Done | Ensure --json applies to error paths | CLI | Jacob | `AF0038_Done_json_error_path.md` |

---

## Sprint 02 items — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0017 | P0 | Done | OpenAI API integration (provider adapter) + config wiring | Providers | Jacob | `AF0017_Done_openai_api_integration.md` |
| AF-0019 | P0 | Done | Agent network playbook v0: delegation with multi-step trace | Kernel | Jacob | `AF0019_Done_agent_network_playbook.md` |
| AF-0011 | P1 | Done | CLI global options: --workspace/--json/--quiet/--verbose truly global | CLI | Jacob | `AF0011_Done_cli_global_options.md` |
| AF-0014 | P1 | Done | Resolve Recorder interface discrepancy (docs vs implementation) | Kernel | Jacob | `AF0014_Done_resolve_recorder_interface.md` |
| AF-0018 | P1 | Done | Provider abstraction + Claude/local stubs | Providers | Jacob | `AF0018_Done_provider_abstraction_claude.md` |
| AF-0016 | P2 | Done | Resolve contract drift: ReasoningMode enum vs examples; Artifact semantics | Contracts | Jacob | `AF0016_Done_resolve_contract_drift.md` |

---

## Sprint 02 hardening extension — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0021 | P1 | Done | Storage lifecycle hardening (SQLite deterministic closure) | Storage | Jacob | `AF0021_Done_storage_lifecycle_hardening.md` |
| AF-0022 | P1 | Done | Provider coverage hardening (≥95% target) | Providers | Jacob | `AF0022_Done_provider_coverage_hardening.md` |
| AF-0023 | P1 | Done | Environment & configuration hardening | Config | Jacob | `AF0023_Done_environment_configuration_hardening.md` |
| AF-0024 | P1 | Done | Workspace lifecycle correction (ag ws create/list) | CLI | Jacob | `AF0024_Done_workspace_lifecycle_correction.md` |
| AF-0025 | P1 | Done | Test discipline enforcement (Ruff + docs) | Testing | Jacob | `AF0025_Done_test_discipline_enforcement.md` |
| AF-0026 | P0 | Done | Workspace selection policy enforcement | CLI/Runtime | Jacob | `AF0026_Done_workspace_selection_policy.md` |

---

## Sprint 01 items — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0004 | P0 | Done | Sprint OS hygiene: sprint log + docs/dev pointers + handoff rules | Docs | Jeff | `AF0004_Done_sprint_os_hygiene.md` |
| AF-0010 | P0 | Done | Python project bootstrap (packaging + CLI stub + pytest) | Repo | Jacob | `AF0010_Done_python_project_bootstrap.md` |
| AF-0005 | P0 | Done | Contracts: TaskSpec + RunTrace + Playbook schemas v0.1 | Kernel | Jeff | `AF0005_Done_contracts_taskspec_runtrace.md` |
| AF-0006 | P0 | Done | Workspace + storage baseline (sqlite + filesystem) | Storage | Jacob | `AF0006_Done_workspace_storage_baseline.md` |
| AF-0007 | P0 | Done | Core runtime skeleton v0 (interfaces + playbook + stub skills) | Kernel | Jacob | `AF0007_Done_core_runtime_skeleton.md` |
| AF-0008 | P0 | Done | CLI v0: ag run + runs show --json, truthful labels, manual gate | CLI | Jacob | `AF0008_Done_cli_ag_run.md` |
| AF-0009 | P1 | Done | Artifact registry v0 + ag artifacts list | Storage | Jacob | `AF0009_Done_artifact_registry_ag.md` |

---

## Sprint 00 items — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0001 | P0 | Done | Kick-off: establish new docs/dev foundation | Docs/Process | Kai/Jeff | `AF0001_Done_kick_off_establish.md` |
| AF-0002 | P0 | Done | New cornerstone docs (IoT-in-space vision) | Docs/Architecture | Jeff | `AF0002_Done_new_cornerstone_docs.md` |
| AF-0003 | P0 | Done | Core runtime skeleton (request + event driven) — docs only | Architecture/Kernel | Jeff/Jacob | `AF0003_Done_core_runtime_skeleton.md` |

---

## Notes
- Bugs are tracked in `/docs/dev/bugs/INDEX_BUGS.md` (not mixed into this backlog index).
- During migration, keep IDs stable (AF-#### in content), but filenames follow the new convention above.
