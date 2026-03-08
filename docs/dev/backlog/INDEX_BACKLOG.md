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
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

## Status legend
PROPOSED → READY → IN_PROGRESS → DONE (or BLOCKED / DROPPED)

---

## Active backlog (current)

### Sprint 06 Scope
| Order | ID | Priority | Status | Title | Area | Owner | Filename |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF-0058 | P0 | DONE | Workspace folder restructure (+DB filename) | Storage | Jacob | `AF0058_DONE_workspace_folder_restructure.md` |
| 2 | AF-0061 | P2 | DONE | Status CAPS convention | Docs/Process | Kai | `AF0061_DONE_status_caps_convention.md` |
| 3 | AF-0060 | P0 | DONE | Skill definition framework | Skills | Kai | `AF0060_DONE_skill_definition_framework.md` |
| 4 | AF-0063 | P1 | DONE | Schema inventory documentation | Docs/Core | Kai | `AF0063_DONE_schema_inventory_documentation.md` |
| 5 | AF-0013 | P1 | DONE | Contract inventory hardening | Contracts | Jacob | `AF0013_DONE_contract_inventory_hardening.md` |

### Sprint 07 Scope (planned)
| Order | ID | Priority | Status | Title | Area | Owner | Filename |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF-0065 | P0 | READY | First skill set (summarize_v0) | Skills | Kai | `AF0065_READY_first_skill_set.md` |
| 2 | AF-0068 | P1 | READY | Skills/playbooks folder restructure | Skills/Playbooks | Kai | `AF0068_READY_skills_playbooks_folder_restructure.md` |
| 3 | AF-0066 | P1 | DONE | E2E integration test | Testing | Kai | `AF0066_DONE_e2e_integration_test.md` |
| 4 | AF-0062 | P1 | READY | Trace LLM model tracking | Core | Kai | `AF0062_READY_trace_llm_model_tracking.md` |
| 5 | AF-0067 | P2 | READY | Skill code documentation | Skills/Docs | Kai | `AF0067_READY_skill_code_documentation.md` |

### Backlog (unprioritized)
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0015 | P2 | PROPOSED | Resolve storage DB filename mismatch | Storage | Jacob | `AF0015_PROPOSED_resolve_storage_db.md` |
| AF-0046 | P1 | READY | Test isolation framework (+BUG-0007) | Testing | Jacob | `AF0046_READY_test_isolation_framework.md` |
| AF-0056 | P0 | PROPOSED | Direct skill runs through verifier | CLI/Core/Verifier | Jacob | `AF0056_PROPOSED_direct_skill_runs_verifier.md` |
| AF-0057 | P0 | PROPOSED | Skill emits trace artifacts evidence | Core/Recorder/Skills | Jacob | `AF0057_PROPOSED_skill_emits_trace_artifacts_evidence.md` |
| AF-0059 | P2 | PROPOSED | Implement playbooks list | CLI | Jacob | `AF0059_PROPOSED_implement_playbooks_list.md` |
| AF-0064 | P1 | PROPOSED | Process documentation hardening | Process/Docs | Kai | `AF0064_PROPOSED_process_documentation_hardening.md` |
| AF-0012 | P2 | PROPOSED | CLI_REFERENCE surface parity (+playbooks list) | CLI | Jacob | `AF0012_PROPOSED_cli_reference_surface.md` |
| AF-0036 | P1 | PROPOSED | Remove global CLI flags (needs design) | CLI | Jacob | `AF0036_PROPOSED_remove_global_cli.md` |

---

## Sprint 05 items — completed (follow-ups)
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0047 | P0 | DONE | Foundation consolidation refactor | Docs/Process | Jacob | `AF0047_DONE_foundation_consolidation.md` |
| AF-0052 | P0 | DONE | Restore coverage threshold | Testing | Jacob | `AF0052_DONE_restore_coverage_threshold.md` |
| AF-0053 | P0 | DONE | Provider test stability | Testing | Jacob | `AF0053_DONE_provider_test_stability.md` |
| AF-0054 | P1 | DONE | Citation model unification | Core | Jacob | `AF0054_DONE_citation_model_unification.md` |
| AF-0055 | P1 | DONE | Verifier loop bounding | Verifier | Jacob | `AF0055_DONE_verifier_loop_bounding.md` |

## Sprint 05 items — completed (ACCEPT WITH FOLLOW-UPS)
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0048 | P0 | DONE | Structured brief skill | Skills | Jacob | `AF0048_DONE_structured_brief_skill.md` |
| AF-0049 | P0 | DONE | Evidence capture discipline | Core | Jacob | `AF0049_DONE_evidence_capture_discipline.md` |
| AF-0050 | P0 | DONE | Verifier schema loop | Verifier | Jacob | `AF0050_DONE_verifier_schema_loop.md` |
| AF-0051 | P1 | DONE | Artifact export hardening | Storage | Jacob | `AF0051_DONE_artifact_export_hardening.md` |

---

## Sprint 04 items — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0039 | P0 | DONE | Create canonical /docs/dev skeleton + root doc moves | Docs/Process | Kai/Jeff | `AF0039_DONE_new_dev_skeleton.md` |
| AF-0040 | P1 | DONE | Merge WORKFLOW/PROCESS into canonical foundation docs | Docs/Process | Kai/Jeff | `AF0040_DONE_workflow_docs_merge.md` |
| AF-0041 | P0 | DONE | Backlog migration: merge templates + rename/move AFs | Docs/Backlog | Jacob | `AF0041_DONE_backlog_migration.md` |
| AF-0042 | P1 | DONE | Bugs + Decisions migration: rename/move + update indexes | Docs/Bugs/Decisions | Jacob | `AF0042_DONE_bugs_decisions_migration.md` |
| AF-0043 | P0 | DONE | Sprint system migration: per-sprint folders + deprecate SPRINT_LOG | Docs/Sprints | Jacob | `AF0043_DONE_sprint_system_migration.md` |
| AF-0044 | P1 | DONE | Review artifact migration: reviews into sprint folders | Docs/Reviews | Jacob | `AF0044_DONE_review_migration.md` |
| AF-0045 | P0 | DONE | CI enforcement: ruff + pytest + coverage via pre-commit/Actions | CI/Quality | Jacob | `AF0045_DONE_ci_enforcement.md` |

---

## Sprint 03 items — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0027 | P0 | DONE | Default workspace policy (intuitive precedence) | CLI/Core/Storage | Jacob | `AF0027_DONE_default_workspace_policy.md` |
| AF-0028 | P0 | DONE | Run ID truncation fix | CLI | Jacob | `AF0028_DONE_run_id_truncation.md` |
| AF-0029 | P0 | DONE | RunTrace verification hardening | Core/Storage | Jacob | `AF0029_DONE_runtrace_verification_hardening.md` |
| AF-0030 | P0 | DONE | RunTrace metadata completeness (workspace_source) | Core/Storage | Jacob | `AF0030_DONE_runtrace_metadata_completeness.md` |
| AF-0031 | P0 | DONE | CLI truthfulness enforcement | CLI | Jacob | `AF0031_DONE_cli_truthfulness_enforcement.md` |
| AF-0032 | P0 | DONE | Observability command expansion | CLI | Jacob | `AF0032_DONE_observability_command_expansion.md` |
| AF-0033 | P0 | DONE | Early .env loading + manual mode gate fix | CLI | Jacob | `AF0033_DONE_early_env_loading.md` |
| AF-0034 | P0 | DONE | Workspace error message hardening (no name leakage) | CLI | Jacob | `AF0034_DONE_workspace_error_message.md` |
| AF-0035 | P2 | DONE | Clarify --workspace flag help text | CLI | Jacob | `AF0035_DONE_clarify_workspace_flag.md` |
| AF-0037 | P1 | DONE | Standardize workspace-required error messaging | CLI | Jacob | `AF0037_DONE_standardize_workspace_error.md` |
| AF-0038 | P1 | DONE | Ensure --json applies to error paths | CLI | Jacob | `AF0038_DONE_json_error_path.md` |

---

## Sprint 02 items — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0017 | P0 | DONE | OpenAI API integration (provider adapter) + config wiring | Providers | Jacob | `AF0017_DONE_openai_api_integration.md` |
| AF-0019 | P0 | DONE | Agent network playbook v0: delegation with multi-step trace | Kernel | Jacob | `AF0019_DONE_agent_network_playbook.md` |
| AF-0011 | P1 | DONE | CLI global options: --workspace/--json/--quiet/--verbose truly global | CLI | Jacob | `AF0011_DONE_cli_global_options.md` |
| AF-0014 | P1 | DONE | Resolve Recorder interface discrepancy (docs vs implementation) | Kernel | Jacob | `AF0014_DONE_resolve_recorder_interface.md` |
| AF-0018 | P1 | DONE | Provider abstraction + Claude/local stubs | Providers | Jacob | `AF0018_DONE_provider_abstraction_claude.md` |
| AF-0016 | P2 | DONE | Resolve contract drift: ReasoningMode enum vs examples; Artifact semantics | Contracts | Jacob | `AF0016_DONE_resolve_contract_drift.md` |

---

## Sprint 02 hardening extension — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0021 | P1 | DONE | Storage lifecycle hardening (SQLite deterministic closure) | Storage | Jacob | `AF0021_DONE_storage_lifecycle_hardening.md` |
| AF-0022 | P1 | DONE | Provider coverage hardening (≥95% target) | Providers | Jacob | `AF0022_DONE_provider_coverage_hardening.md` |
| AF-0023 | P1 | DONE | Environment & configuration hardening | Config | Jacob | `AF0023_DONE_environment_configuration_hardening.md` |
| AF-0024 | P1 | DONE | Workspace lifecycle correction (ag ws create/list) | CLI | Jacob | `AF0024_DONE_workspace_lifecycle_correction.md` |
| AF-0025 | P1 | DONE | Test discipline enforcement (Ruff + docs) | Testing | Jacob | `AF0025_DONE_test_discipline_enforcement.md` |
| AF-0026 | P0 | DONE | Workspace selection policy enforcement | CLI/Runtime | Jacob | `AF0026_DONE_workspace_selection_policy.md` |

---

## Sprint 01 items — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0004 | P0 | DONE | Sprint OS hygiene: sprint log + docs/dev pointers + handoff rules | Docs | Jeff | `AF0004_DONE_sprint_os_hygiene.md` |
| AF-0010 | P0 | DONE | Python project bootstrap (packaging + CLI stub + pytest) | Repo | Jacob | `AF0010_DONE_python_project_bootstrap.md` |
| AF-0005 | P0 | DONE | Contracts: TaskSpec + RunTrace + Playbook schemas v0.1 | Kernel | Jeff | `AF0005_DONE_contracts_taskspec_runtrace.md` |
| AF-0006 | P0 | DONE | Workspace + storage baseline (sqlite + filesystem) | Storage | Jacob | `AF0006_DONE_workspace_storage_baseline.md` |
| AF-0007 | P0 | DONE | Core runtime skeleton v0 (interfaces + playbook + stub skills) | Kernel | Jacob | `AF0007_DONE_core_runtime_skeleton.md` |
| AF-0008 | P0 | DONE | CLI v0: ag run + runs show --json, truthful labels, manual gate | CLI | Jacob | `AF0008_DONE_cli_ag_run.md` |
| AF-0009 | P1 | DONE | Artifact registry v0 + ag artifacts list | Storage | Jacob | `AF0009_DONE_artifact_registry_ag.md` |

---

## Sprint 00 items — completed
| ID | Priority | Status | Title | Area | Owner | Filename |
|---:|:--:|:--|---|---|---|---|
| AF-0001 | P0 | DONE | Kick-off: establish new docs/dev foundation | Docs/Process | Kai/Jeff | `AF0001_DONE_kick_off_establish.md` |
| AF-0002 | P0 | DONE | New cornerstone docs (IoT-in-space vision) | Docs/Architecture | Jeff | `AF0002_DONE_new_cornerstone_docs.md` |
| AF-0003 | P0 | DONE | Core runtime skeleton (request + event driven) — docs only | Architecture/Kernel | Jeff/Jacob | `AF0003_DONE_core_runtime_skeleton.md` |

---

## Notes
- Bugs are tracked in `/docs/dev/bugs/INDEX_BUGS.md` (not mixed into this backlog index).
- During migration, keep IDs stable (AF-#### in content), but filenames follow the new convention above.

