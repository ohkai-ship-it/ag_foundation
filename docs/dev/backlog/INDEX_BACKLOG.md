# INDEX_BACKLOG
# Version number: v0.2

> **Location (new):** `/docs/dev/backlog/INDEX_BACKLOG.md`  
> **Naming (required):** `AF####_<Status>_<three_word_description>.md` in `/docs/dev/backlog/items/`  
> Status values: `Proposed | Ready | In progress | Blocked | Done | Dropped`

## Status legend
Proposed → Ready → In progress → Done (or Blocked / Dropped)

---

## Active backlog (current)
| ID | Priority | Status | Title | Area | Owner | New file (target path) |
|---:|:--:|:--|---|---|---|---|
| AF-0046 | P1 | Proposed | Test isolation framework for providers | Testing | Jacob | `/docs/dev/backlog/items/AF0046_Proposed_test_isolation_framework.md` |
| AF-0034 | P0 | Ready | Workspace error message hardening (no identifier leakage) | CLI | Jacob | `/docs/dev/backlog/items/AF0034_Ready_workspace_error_message.md` |
| AF-0037 | P1 | Ready | Standardize workspace error messages | CLI | Jacob | `/docs/dev/backlog/items/AF0037_Ready_standardize_workspace_error.md` |
| AF-0038 | P1 | Ready | JSON error path consistency | CLI | Jacob | `/docs/dev/backlog/items/AF0038_Ready_json_error_path.md` |
| AF-0012 | P2 | Ready | CLI_REFERENCE surface parity v0.1 (partial — if capacity) | CLI | Jacob | `/docs/dev/backlog/items/AF0012_Ready_cli_reference_surface.md` |
| AF-0013 | P1 | Ready | Contract inventory hardening: reconcile docs ↔ implementation | Contracts | Jacob | `/docs/dev/backlog/items/AF0013_Ready_contract_inventory_hardening.md` |
| AF-0015 | P2 | Ready | Resolve storage DB filename mismatch (docs vs code) | Storage | Jacob | `/docs/dev/backlog/items/AF0015_Ready_resolve_storage_db.md` |
| AF-0035 | P2 | Ready | Clarify --workspace flag help text | CLI | Jacob | `/docs/dev/backlog/items/AF0035_Ready_clarify_workspace_flag.md` |
| AF-0036 | P1 | Proposed | Remove global CLI flags (needs design) | CLI | Jacob | `/docs/dev/backlog/items/AF0036_Proposed_remove_global_cli.md` |

---

## Sprint 03 items — completed
| ID | Priority | Status | Title | Area | Owner | New file (target path) |
|---:|:--:|:--|---|---|---|---|
| AF-0027 | P0 | Done | Default workspace policy (intuitive precedence) | CLI/Core/Storage | Jacob | `/docs/dev/backlog/items/AF0027_Done_default_workspace_policy.md` |
| AF-0028 | P0 | Done | Run ID truncation fix | CLI | Jacob | `/docs/dev/backlog/items/AF0028_Done_run_id_truncation.md` |
| AF-0029 | P0 | Done | RunTrace verification hardening | Core/Storage | Jacob | `/docs/dev/backlog/items/AF0029_Done_runtrace_verification_hardening.md` |
| AF-0030 | P0 | Done | RunTrace metadata completeness (workspace_source) | Core/Storage | Jacob | `/docs/dev/backlog/items/AF0030_Done_runtrace_metadata_completeness.md` |
| AF-0031 | P0 | Done | CLI truthfulness enforcement | CLI | Jacob | `/docs/dev/backlog/items/AF0031_Done_cli_truthfulness_enforcement.md` |
| AF-0032 | P0 | Done | Observability command expansion | CLI | Jacob | `/docs/dev/backlog/items/AF0032_Done_observability_command_expansion.md` |
| AF-0033 | P0 | Done | Early .env loading + manual mode gate fix | CLI | Jacob | `/docs/dev/backlog/items/AF0033_Done_early_env_loading.md` |

---

## Sprint 02 items — completed
| ID | Priority | Status | Title | Area | Owner | New file (target path) |
|---:|:--:|:--|---|---|---|---|
| AF-0017 | P0 | Done | OpenAI API integration (provider adapter) + config wiring | Providers | Jacob | `/docs/dev/backlog/items/AF0017_Done_openai_api_integration.md` |
| AF-0019 | P0 | Done | Agent network playbook v0: delegation with multi-step trace | Kernel | Jacob | `/docs/dev/backlog/items/AF0019_Done_agent_network_playbook.md` |
| AF-0011 | P1 | Done | CLI global options: --workspace/--json/--quiet/--verbose truly global | CLI | Jacob | `/docs/dev/backlog/items/AF0011_Done_cli_global_options.md` |
| AF-0014 | P1 | Done | Resolve Recorder interface discrepancy (docs vs implementation) | Kernel | Jacob | `/docs/dev/backlog/items/AF0014_Done_resolve_recorder_interface.md` |
| AF-0018 | P1 | Done | Provider abstraction + Claude/local stubs | Providers | Jacob | `/docs/dev/backlog/items/AF0018_Done_provider_abstraction_claude.md` |
| AF-0016 | P2 | Done | Resolve contract drift: ReasoningMode enum vs examples; Artifact semantics | Contracts | Jacob | `/docs/dev/backlog/items/AF0016_Done_resolve_contract_drift.md` |

---

## Sprint 02 hardening extension — completed
| ID | Priority | Status | Title | Area | Owner | New file (target path) |
|---:|:--:|:--|---|---|---|---|
| AF-0021 | P1 | Done | Storage lifecycle hardening (SQLite deterministic closure) | Storage | Jacob | `/docs/dev/backlog/items/AF0021_Done_storage_lifecycle_hardening.md` |
| AF-0022 | P1 | Done | Provider coverage hardening (≥95% target) | Providers | Jacob | `/docs/dev/backlog/items/AF0022_Done_provider_coverage_hardening.md` |
| AF-0023 | P1 | Done | Environment & configuration hardening | Config | Jacob | `/docs/dev/backlog/items/AF0023_Done_environment_configuration_hardening.md` |
| AF-0024 | P1 | Done | Workspace lifecycle correction (ag ws create/list) | CLI | Jacob | `/docs/dev/backlog/items/AF0024_Done_workspace_lifecycle_correction.md` |
| AF-0025 | P1 | Done | Test discipline enforcement (Ruff + docs) | Testing | Jacob | `/docs/dev/backlog/items/AF0025_Done_test_discipline_enforcement.md` |
| AF-0026 | P0 | Done | Workspace selection policy enforcement | CLI/Runtime | Jacob | `/docs/dev/backlog/items/AF0026_Done_workspace_selection_policy.md` |

---

## Sprint 01 items — completed
| ID | Priority | Status | Title | Area | Owner | New file (target path) |
|---:|:--:|:--|---|---|---|---|
| AF-0004 | P0 | Done | Sprint OS hygiene: sprint log + docs/dev pointers + handoff rules | Docs | Jeff | `/docs/dev/backlog/items/AF0004_Done_sprint_os_hygiene.md` |
| AF-0010 | P0 | Done | Python project bootstrap (packaging + CLI stub + pytest) | Repo | Jacob | `/docs/dev/backlog/items/AF0010_Done_python_project_bootstrap.md` |
| AF-0005 | P0 | Done | Contracts: TaskSpec + RunTrace + Playbook schemas v0.1 | Kernel | Jeff | `/docs/dev/backlog/items/AF0005_Done_contracts_taskspec_runtrace.md` |
| AF-0006 | P0 | Done | Workspace + storage baseline (sqlite + filesystem) | Storage | Jacob | `/docs/dev/backlog/items/AF0006_Done_workspace_storage_baseline.md` |
| AF-0007 | P0 | Done | Core runtime skeleton v0 (interfaces + playbook + stub skills) | Kernel | Jacob | `/docs/dev/backlog/items/AF0007_Done_core_runtime_skeleton.md` |
| AF-0008 | P0 | Done | CLI v0: ag run + runs show --json, truthful labels, manual gate | CLI | Jacob | `/docs/dev/backlog/items/AF0008_Done_cli_ag_run.md` |
| AF-0009 | P1 | Done | Artifact registry v0 + ag artifacts list | Storage | Jacob | `/docs/dev/backlog/items/AF0009_Done_artifact_registry_ag.md` |

---

## Sprint 00 items — completed
| ID | Priority | Status | Title | Area | Owner | New file (target path) |
|---:|:--:|:--|---|---|---|---|
| AF-0001 | P0 | Done | Kick-off: establish new docs/dev foundation | Docs/Process | Kai/Jeff | `/docs/dev/backlog/items/AF0001_Done_kick_off_establish.md` |
| AF-0002 | P0 | Done | New cornerstone docs (IoT-in-space vision) | Docs/Architecture | Jeff | `/docs/dev/backlog/items/AF0002_Done_new_cornerstone_docs.md` |
| AF-0003 | P0 | Done | Core runtime skeleton (request + event driven) — docs only | Architecture/Kernel | Jeff/Jacob | `/docs/dev/backlog/items/AF0003_Done_core_runtime_skeleton.md` |

---

## Notes
- Bugs are tracked in `/docs/dev/bugs/INDEX_BUGS.md` (not mixed into this backlog index).
- During migration, keep IDs stable (AF-#### in content), but filenames follow the new convention above.
