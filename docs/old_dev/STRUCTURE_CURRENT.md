# docs/dev/ — Directory Structure

```
docs/dev/
├───backlog/
│   │   INDEX.md
│   │   WORKFLOW.md
│   ├───completion/
│   │       2026-02-24_AF-0004_sprint-os-hygiene.md
│   │       2026-02-24_AF-0005_contracts.md
│   │       2026-02-24_AF-0006_storage-baseline.md
│   │       2026-02-24_AF-0007_runtime-skeleton.md
│   │       2026-02-24_AF-0008_cli-v0-truthful.md
│   │       2026-02-24_AF-0009_artifacts-v0.md
│   │       2026-02-24_AF-0010_python-bootstrap.md
│   │       2026-02-26_AF-0011_cli-global-options.md
│   │       2026-02-26_AF-0014_recorder-protocol.md
│   │       2026-02-26_AF-0016_reasoning-mode-fix.md
│   │       2026-02-26_AF-0017_openai-adapter.md
│   │       2026-02-26_AF-0018_provider-abstraction.md
│   │       2026-02-26_AF-0019_delegation-playbook.md
│   │       2026-02-26_AF-0021_storage-lifecycle-hardening.md
│   │       2026-02-26_AF-0022_provider-coverage-hardening.md
│   │       2026-02-26_AF-0023_environment-configuration-hardening.md
│   │       2026-02-26_AF-0024_workspace-lifecycle-correction.md
│   │       2026-02-26_AF-0025_test-discipline-enforcement.md
│   │       2026-02-26_AF-0026_workspace-selection-policy.md
│   │       2026-02-27_AF-0027_default-workspace-policy.md
│   │       2026-02-27_AF-0028_run-id-formatting.md
│   │       2026-02-27_AF-0029_runtrace-verification-hardening.md
│   │       2026-02-27_AF-0030_runtrace-metadata-completeness.md
│   │       2026-02-27_AF-0031_cli-truthfulness-enforcement.md
│   │       2026-02-27_AF-0032_observability-command-expansion.md
│   │       2026-02-27_AF-0033_dotenv-loading.md
│   │       ONBOARDING_SUMMARY_JACOB.md
│   │       README.md
│   ├───items/
│   │       AF-0001.md
│   │       AF-0002.md
│   │       AF-0003.md
│   │       AF-0004.md
│   │       AF-0005.md
│   │       AF-0006.md
│   │       AF-0007.md
│   │       AF-0008.md
│   │       AF-0009.md
│   │       AF-0010.md
│   │       AF-0011.md
│   │       AF-0012.md
│   │       AF-0013.md
│   │       AF-0014.md
│   │       AF-0015.md
│   │       AF-0016.md
│   │       AF-0017.md
│   │       AF-0018.md
│   │       AF-0019.md
│   │       AF-0021-storage-lifecycle-hardening.md
│   │       AF-0022-provider-coverage-hardening.md
│   │       AF-0023-environment-configuration-hardening.md
│   │       AF-0024-workspace-lifecycle-correction.md
│   │       AF-0025-test-discipline-enforcement.md
│   │       AF-0026-workspace-selection-policy-enforcement.md
│   │       AF-0027.md
│   │       AF-0028.md
│   │       AF-0029.md
│   │       AF-0030.md
│   │       AF-0031.md
│   │       AF-0032.md
│   │       AF-0033.md
│   │       AF-0034-workspace-error-hardening.md
│   │       AF-0035-clarify-workspace-flag-help.md
│   │       AF-0036-remove-global-cli-flags.md
│   │       AF-0037-standardize-workspace-errors.md
│   │       AF-0038-json-error-path-consistency.md
│   └───templates/
│           BACKLOG_ITEM_TEMPLATE.md
│           COMPLETION_NOTE_TEMPLATE.md
├───bugs/
│   │   INDEX.md
│   ├───reports/
│   │       BUG-0001-global-options-not-global.md
│   │       BUG-0002-missing-run-options.md
│   │       BUG-0003-missing-cli-subcommands.md
│   │       BUG-0004-sqlite-connection-leak.md
│   │       BUG-0005-implicit-workspace-creation.md
│   │       BUG-0006.md
│   └───templates/
│           BUG_REPORT_TEMPLATE.md
├───cornerstone/
│       ARCHITECTURE.md
│       CLI_REFERENCE.md
│       INDEX.md
│       PROJECT_PLAN.md
│       REVIEW_GUIDE.md
├───decisions/
│   │   ADR-0001-architecture-baseline.md
│   │   ADR-0002-trace-versioning.md
│   │   ADR-0003-manual-mode-gating.md
│   │   ADR-0004-storage-baseline.md
│   │   ADR-0005-orchestrator-threshold.md
│   │   INDEX.md
│   └───templates/
│           ADR_TEMPLATE.md
├───engineering/
│       CODING_GUIDELINES.md
│       INDEX.md
│       PR_CHECKLIST.md
│       TESTING_GUIDELINES.md
├───playbooks/
│       CLI_CHANGE_PLAYBOOK.md
│       INDEX.md
│       LARGE_CHANGE_PLAYBOOK.md
│       NEW_DEPENDENCY_PLAYBOOK.md
│       TRACE_SCHEMA_CHANGE_PLAYBOOK.md
├───prompts/
│   │   continuation_prompt_jeff_sprint_design.md
│   │   continuation_prompt_sprint03_opus.md
│   │   INDEX.md
│   │   kickoff_prompt_jacob_onboarding.md
│   └───templates/
│           CONTINUATION_PROMPT_JUNDEV.md
│           CONTINUATION_PROMPT_SENDEV.md
├───repo/
│   │   INDEX.md
│   └───templates/
│           PULL_REQUEST_TEMPLATE.md
├───reviews/
│   │   INDEX.md
│   ├───entries/
│   │   │   2026-02-23-kickoff.md
│   │   │   REVIEW_S01_2026-02-24.md
│   │   │   REVIEW_S02_2026-02-26.md
│   │   │   REVIEW_S02_2026-02-26_SIGNOFF_FINDINGS.md
│   │   │   REVIEW_TASKS_SPRINT01.md
│   │   ├───REVIEW_S01_2026-02-24/
│   │   │       artifacts_outputs.txt
│   │   │       bug_triage.md
│   │   │       cli_outputs.txt
│   │   │       contracts_notes.md
│   │   │       CONTRACT_INVENTORY.md
│   │   │       env.txt
│   │   │       failure_trace.json
│   │   │       FUTURE_CONTRACTS.md
│   │   │       happy_trace.json
│   │   │       pytest_summary.txt
│   │   │       scope_links.md
│   │   │       storage_isolation_transcript.txt
│   │   │       TEST_INVENTORY.md
│   │   ├───REVIEW_S02_2026-02-26/
│   │   │       sprint02_cli_global.txt
│   │   │       sprint02_coverage.txt
│   │   │       sprint02_delegation.txt
│   │   │       sprint02_e2e_delegation.txt
│   │   │       sprint02_integration.txt
│   │   │       sprint02_providers.txt
│   │   │       sprint02_repl_a10.txt
│   │   │       sprint02_repl_a8.txt
│   │   │       sprint02_repl_a9.txt
│   │   │       sprint02_schemas.txt
│   │   │       sprint02_test_full.txt
│   │   └───REVIEW_S03_2026-02-27/
│   │           REVIEW_S03_FINDINGS.md
│   │           REVIEW_S03_PLAN.md
│   └───templates/
│           REVIEW_TASKS_TEMPLATE.md
│           REVIEW_TEMPLATE.md
├───sprints/
│   │   INDEX.md
│   │   PROCESS.md
│   │   S03_COMPLETION_NOTE.md
│   │   SPRINT_03_CLOSURE_PROMPT_JACOB.md
│   │   SPRINT_03_PLAN.md
│   │   SPRINT_LOG.md
│   │   SPRINT_PLAN_SPRINT01.md
│   │   SPRINT_PLAN_SPRINT02.md
│   │   SPRINT_REPORT_SPRINT01.md
│   │   SPRINT_REPORT_SPRINT02.md
│   │   SPRINT_REPORT_SPRINT02_HARDENING.md
│   │   SPRINT_REPORT_SPRINT03.md
│   └───templates/
│           SPRINT_PLAN_TEMPLATE.md
│           SPRINT_REPORT_TEMPLATE.md
├───team/
│       COLLABORATION_MANIFEST.md
│       GITHUB_FLOW.md
│       INDEX.md
│       REPO_HYGIENE_LIST.md
└───STRUCTURE.md
```

---
*Generated: 2026-03-03*
