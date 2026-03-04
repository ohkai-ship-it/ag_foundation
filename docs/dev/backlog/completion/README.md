# Completion Notes — Index

> **⚠️ DEPRECATED (2026-03-03):** This folder is archived. Completion notes are now embedded directly in AF item files under `/docs/new_dev/backlog/items/`. See [INDEX_BACKLOG](/docs/new_dev/backlog/INDEX_BACKLOG.md) for the canonical location.

This folder contains **completion notes** for finished backlog items. Each note documents what was implemented, test results, and acceptance criteria verification.

## File Naming Convention
```
YYYY-MM-DD_AF-XXXX_<slug>.md
```

## Template
See [../templates/COMPLETION_NOTE_TEMPLATE.md](../templates/COMPLETION_NOTE_TEMPLATE.md)

## Sprint 01 Completions

| Date | AF Item | File | Description |
|------|---------|------|-------------|
| 2026-02-24 | AF-0004 | [2026-02-24_AF-0004_sprint-os-hygiene.md](2026-02-24_AF-0004_sprint-os-hygiene.md) | Sprint OS hygiene (docs/pointers) |
| 2026-02-24 | AF-0005 | [2026-02-24_AF-0005_contracts.md](2026-02-24_AF-0005_contracts.md) | Contracts: TaskSpec + RunTrace + Playbook |
| 2026-02-24 | AF-0006 | [2026-02-24_AF-0006_storage-baseline.md](2026-02-24_AF-0006_storage-baseline.md) | Workspace + storage baseline |
| 2026-02-24 | AF-0007 | [2026-02-24_AF-0007_runtime-skeleton.md](2026-02-24_AF-0007_runtime-skeleton.md) | Core runtime skeleton v0 |
| 2026-02-24 | AF-0008 | [2026-02-24_AF-0008_cli-v0-truthful.md](2026-02-24_AF-0008_cli-v0-truthful.md) | CLI v0 truthful labels |
| 2026-02-24 | AF-0009 | [2026-02-24_AF-0009_artifacts-v0.md](2026-02-24_AF-0009_artifacts-v0.md) | Artifact registry v0 |
| 2026-02-24 | AF-0010 | [2026-02-24_AF-0010_python-bootstrap.md](2026-02-24_AF-0010_python-bootstrap.md) | Python project bootstrap |

## Sprint 02 Completions

| Date | AF Item | File | Description |
|------|---------|------|-------------|
| 2026-02-26 | AF-0011 | [2026-02-26_AF-0011_cli-global-options.md](2026-02-26_AF-0011_cli-global-options.md) | CLI global options truly global |
| 2026-02-26 | AF-0014 | [2026-02-26_AF-0014_recorder-protocol.md](2026-02-26_AF-0014_recorder-protocol.md) | Recorder interface discrepancy |
| 2026-02-26 | AF-0016 | [2026-02-26_AF-0016_reasoning-mode-fix.md](2026-02-26_AF-0016_reasoning-mode-fix.md) | ReasoningMode enum + Artifact fix |
| 2026-02-26 | AF-0017 | [2026-02-26_AF-0017_openai-adapter.md](2026-02-26_AF-0017_openai-adapter.md) | OpenAI API integration |
| 2026-02-26 | AF-0018 | [2026-02-26_AF-0018_provider-abstraction.md](2026-02-26_AF-0018_provider-abstraction.md) | Provider abstraction + stubs |
| 2026-02-26 | AF-0019 | [2026-02-26_AF-0019_delegation-playbook.md](2026-02-26_AF-0019_delegation-playbook.md) | Delegation playbook v0 |

## Sprint 02 Hardening Completions

| Date | AF/BUG Item | File | Description |
|------|-------------|------|-------------|
| 2026-02-26 | AF-0021 / BUG-0004 | [2026-02-26_AF-0021_storage-lifecycle-hardening.md](2026-02-26_AF-0021_storage-lifecycle-hardening.md) | Storage lifecycle (SQLite connection fix) |
| 2026-02-26 | AF-0022 | [2026-02-26_AF-0022_provider-coverage-hardening.md](2026-02-26_AF-0022_provider-coverage-hardening.md) | Provider coverage hardening |
| 2026-02-26 | AF-0023 | [2026-02-26_AF-0023_environment-configuration-hardening.md](2026-02-26_AF-0023_environment-configuration-hardening.md) | Environment & configuration hardening |
| 2026-02-26 | AF-0024 | [2026-02-26_AF-0024_workspace-lifecycle-correction.md](2026-02-26_AF-0024_workspace-lifecycle-correction.md) | Workspace lifecycle (ws create/list) |
| 2026-02-26 | AF-0025 | [2026-02-26_AF-0025_test-discipline-enforcement.md](2026-02-26_AF-0025_test-discipline-enforcement.md) | Test discipline (Ruff + docs) |
| 2026-02-26 | AF-0026 / BUG-0005 | [2026-02-26_AF-0026_workspace-selection-policy.md](2026-02-26_AF-0026_workspace-selection-policy.md) | Workspace selection policy enforcement |
