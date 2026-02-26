# Test Inventory — ag_foundation
# Version: v0.1 (Sprint 01)
# Generated: 2026-02-25

## Summary

| Metric | Value |
|--------|-------|
| **Total Tests** | 103 |
| **Test Files** | 7 |
| **Test Classes** | 25 |
| **All Passing** | ✅ Yes |

---

## Test Files Overview

| File | Tests | Focus Area |
|------|-------|------------|
| test_sanity.py | 6 | Import health checks |
| test_contracts.py | 21 | Schema validation & evolution guardrails |
| test_storage.py | 19 | Persistence & workspace isolation |
| test_runtime.py | 19 | Orchestrator & execution pipeline |
| test_cli.py | 13 | CLI commands & options |
| test_cli_truthful.py | 14 | Truthful UX labels |
| test_artifacts.py | 11 | Artifact creation & listing |

---

## Detailed Test Inventory

### test_sanity.py (6 tests)
Basic import health checks ensuring package structure is correct.

| Test | Description |
|------|-------------|
| `test_import_ag` | Verify `ag` package imports |
| `test_import_cli` | Verify `ag.cli` module imports |
| `test_import_core` | Verify `ag.core` module imports |
| `test_import_storage` | Verify `ag.storage` module imports |
| `test_import_skills` | Verify `ag.skills` module imports |
| `test_import_config` | Verify `ag.config` module imports |

---

### test_contracts.py (21 tests)
Schema validation ensuring contracts remain stable across versions.

#### TestTaskSpecContract (5 tests)
| Test | Description |
|------|-------------|
| `test_version_field_present` | TaskSpec has version "0.1" |
| `test_required_fields` | prompt, workspace_id are required |
| `test_json_roundtrip` | Lossless JSON serialization |
| `test_stable_defaults` | Default values are stable |
| `test_builder_produces_valid_spec` | Builder pattern works |

#### TestTaskSpecAdditiveEvolution (1 test)
| Test | Description |
|------|-------------|
| `test_all_v01_fields_present` | All v0.1 fields exist (no removals) |

#### TestRunTraceContract (5 tests)
| Test | Description |
|------|-------------|
| `test_version_field_present` | RunTrace has version "0.1" |
| `test_required_fields` | Required fields validated |
| `test_json_roundtrip` | Lossless JSON serialization |
| `test_stable_defaults` | Default values are stable |
| `test_builder_produces_valid_trace` | Builder pattern works |

#### TestRunTraceAdditiveEvolution (1 test)
| Test | Description |
|------|-------------|
| `test_all_v01_fields_present` | All v0.1 fields exist (no removals) |

#### TestPlaybookContract (5 tests)
| Test | Description |
|------|-------------|
| `test_version_field_present` | Playbook has version "0.1" |
| `test_required_fields` | name, version are required |
| `test_json_roundtrip` | Lossless JSON serialization |
| `test_stable_defaults` | Default values are stable |
| `test_builder_produces_valid_playbook` | Builder pattern works |

#### TestPlaybookAdditiveEvolution (1 test)
| Test | Description |
|------|-------------|
| `test_all_v01_fields_present` | All v0.1 fields exist (no removals) |

#### TestSchemaIntegration (3 tests)
| Test | Description |
|------|-------------|
| `test_taskspec_mode_matches_runtrace_mode` | ExecutionMode shared between schemas |
| `test_budgets_shared_between_taskspec_and_playbook` | Budgets model shared |
| `test_full_workflow_schemas` | End-to-end schema integration |

---

### test_storage.py (19 tests)
Persistence layer and workspace isolation verification.

#### TestWorkspace (4 tests)
| Test | Description |
|------|-------------|
| `test_ensure_exists_creates_structure` | Workspace directories created |
| `test_path_safety_rejects_traversal` | Path traversal attacks blocked |
| `test_path_safety_rejects_empty` | Empty paths rejected |
| `test_artifact_path_creates_run_dir` | Artifact directories created |

#### TestRunStore (5 tests)
| Test | Description |
|------|-------------|
| `test_save_and_get` | RunTrace persistence |
| `test_get_nonexistent_returns_none` | Missing runs return None |
| `test_list_returns_runs_ordered` | Runs ordered by timestamp |
| `test_delete` | Run deletion works |
| `test_json_file_persisted` | JSON files created on disk |

#### TestArtifactStore (4 tests)
| Test | Description |
|------|-------------|
| `test_save_and_get` | Artifact persistence |
| `test_list_empty` | Empty list for no artifacts |
| `test_list_artifacts` | Artifact listing works |
| `test_delete` | Artifact deletion works |

#### TestWorkspaceIsolation (6 tests)
| Test | Description |
|------|-------------|
| `test_runs_isolated_between_workspaces` | Runs scoped to workspace |
| `test_artifacts_isolated_between_workspaces` | Artifacts scoped to workspace |
| `test_disk_directories_separate` | Separate folders per workspace |
| `test_sqlite_databases_separate` | Separate DBs per workspace |
| `test_multiple_runs_per_workspace_isolated` | Multiple runs don't leak |
| `test_delete_in_one_workspace_does_not_affect_other` | Cross-workspace safety |

---

### test_runtime.py (19 tests)
Core execution pipeline verification.

#### TestRuntimeHappyPath (8 tests)
| Test | Description |
|------|-------------|
| `test_execute_produces_run_trace` | Execution produces trace |
| `test_trace_has_all_required_fields` | All required fields present |
| `test_manual_mode_sets_trace_mode` | Manual mode recorded correctly |
| `test_llm_mode_sets_trace_mode` | LLM mode recorded correctly |
| `test_trace_persisted_to_storage` | Trace saved to storage |
| `test_playbook_executes_all_steps` | All playbook steps run |
| `test_successful_run_has_passed_verifier` | Verifier status set |
| `test_default_playbook_selected` | Default playbook used |

#### TestRuntimeFailurePath (5 tests)
| Test | Description |
|------|-------------|
| `test_missing_skill_stops_execution` | Unknown skill fails gracefully |
| `test_skill_failure_stops_required_step` | Required step failure stops run |
| `test_failed_run_persisted` | Failed runs still saved |
| `test_error_recorded_in_step` | Errors captured in steps |
| `test_skill_exception_handled` | Exceptions don't crash runtime |

#### TestEchoTool (2 tests)
| Test | Description |
|------|-------------|
| `test_echo_tool_exists_in_registry` | Echo tool registered |
| `test_echo_tool_returns_input` | Echo tool works correctly |

#### TestDefaultPlaybook (3 tests)
| Test | Description |
|------|-------------|
| `test_default_v0_exists` | Default playbook exists |
| `test_default_v0_is_linear` | Playbook is linear (v0) |
| `test_default_v0_uses_balanced_reasoning` | Default uses balanced mode |

#### TestInterfaces (1 test)
| Test | Description |
|------|-------------|
| `test_interfaces_use_protocol` | Interfaces use Protocol pattern |

---

### test_cli.py (13 tests)
CLI command structure and options verification.

#### TestCLIHelp (7 tests)
| Test | Description |
|------|-------------|
| `test_main_help` | `ag --help` works |
| `test_version` | `ag --version` works |
| `test_run_help` | `ag run --help` works |
| `test_runs_help` | `ag runs --help` works |
| `test_ws_help` | `ag ws --help` works |
| `test_artifacts_help` | `ag artifacts --help` works |
| `test_doctor` | `ag doctor` works |

#### TestManualModeGate (3 tests)
| Test | Description |
|------|-------------|
| `test_manual_mode_without_env_var_fails` | AG_DEV required |
| `test_manual_mode_with_env_var_succeeds` | AG_DEV=1 allows manual |
| `test_llm_mode_without_env_var_succeeds` | LLM mode always works |

#### TestRunCommand (3 tests)
| Test | Description |
|------|-------------|
| `test_run_with_prompt` | Basic run works |
| `test_run_with_workspace_option` | --workspace option works |
| `test_run_with_playbook_option` | --playbook option works |

---

### test_cli_truthful.py (14 tests)
Truthful UX verification — labels match trace data.

#### TestManualModeGateExtended (3 tests)
| Test | Description |
|------|-------------|
| `test_manual_mode_banner_printed` | DEV MODE banner shown |
| `test_manual_mode_trace_has_manual_mode` | Trace records manual mode |
| `test_without_ag_dev_manual_mode_fails` | Gate enforced |

#### TestTruthfulLabels (4 tests)
| Test | Description |
|------|-------------|
| `test_extract_labels_matches_trace` | Label extraction works |
| `test_cli_mode_label_matches_trace` | Mode label truthful |
| `test_cli_verifier_status_matches_trace` | Verifier label truthful |
| `test_cli_duration_matches_trace` | Duration label truthful |

#### TestRunsShowJsonConformance (3 tests)
| Test | Description |
|------|-------------|
| `test_runs_show_json_has_all_required_fields` | JSON has all fields |
| `test_runs_show_json_can_parse_as_runtrace` | JSON parses to RunTrace |
| `test_runs_show_json_matches_original_trace` | JSON matches stored trace |

#### TestRunsList (3 tests)
| Test | Description |
|------|-------------|
| `test_runs_list_shows_runs` | List shows runs |
| `test_runs_list_empty_workspace` | Empty workspace handled |
| `test_runs_list_requires_workspace` | --workspace required |

#### TestLabelConsistency (1 test)
| Test | Description |
|------|-------------|
| `test_run_and_show_labels_match` | Run output matches show output |

---

### test_artifacts.py (11 tests)
Artifact creation and registry verification.

#### TestArtifactSchema (2 tests)
| Test | Description |
|------|-------------|
| `test_artifact_schema_exists` | Artifact schema defined |
| `test_artifact_optional_fields` | Optional fields work |

#### TestArtifactsTable (1 test)
| Test | Description |
|------|-------------|
| `test_artifacts_table_exists` | SQLite table created |

#### TestArtifactRegistration (2 tests)
| Test | Description |
|------|-------------|
| `test_run_creates_result_artifact` | result.md created |
| `test_result_artifact_contains_step_summaries` | result.md has summaries |

#### TestArtifactsCLI (3 tests)
| Test | Description |
|------|-------------|
| `test_artifacts_list_requires_workspace` | --workspace required |
| `test_artifacts_list_empty` | Empty list handled |
| `test_artifacts_list_json_empty` | JSON empty list works |

#### TestArtifactsIntegration (3 tests)
| Test | Description |
|------|-------------|
| `test_run_then_list_artifacts` | Run → list flow works |
| `test_artifact_content_matches_run` | Content is correct |
| `test_cli_list_with_real_artifacts` | CLI lists real artifacts |

---

## Test Coverage by Feature Area

| Feature | Tests | Coverage |
|---------|-------|----------|
| TaskSpec schema | 6 | ✅ Complete |
| RunTrace schema | 6 | ✅ Complete |
| Playbook schema | 6 | ✅ Complete |
| Schema integration | 3 | ✅ Complete |
| Run storage | 5 | ✅ Complete |
| Artifact storage | 4 | ✅ Complete |
| Workspace isolation | 10 | ✅ Complete |
| Runtime happy path | 8 | ✅ Complete |
| Runtime failure path | 5 | ✅ Complete |
| CLI commands | 13 | ✅ Complete |
| Truthful UX | 14 | ✅ Complete |
| Artifact creation | 11 | ✅ Complete |
| Import sanity | 6 | ✅ Complete |

---

## Notes

- All tests use pytest fixtures for isolation
- Temporary directories used for storage tests
- CLI tests use Typer's CliRunner
- Contract tests enforce additive evolution policy
- Integration tests verify end-to-end flows
