# AF0041 — Backlog migration: merge templates + embed completion notes + rename/move AF items
# Version number: v0.1

## Metadata
- **ID:** AF0041
- **Type:** Docs | Refactor
- **Status:** DONE
- **Priority:** P0
- **Area:** Docs/Backlog
- **Owner:** Jacob
- **Target sprint:** Sprint04
- **Completion date:** 2026-03-03

## Problem
Backlog items and completion notes are split across `/docs/dev/backlog/items` and `/docs/dev/backlog/completion`, with inconsistent naming and duplicated templates. This creates drift and makes review difficult.

## Goal
Create a single canonical backlog system in `/docs/dev/backlog/` where each AF file contains both the item definition and its completion section, with strict filename conventions and a renamed INDEX_BACKLOG.

## Non-goals
No changes to AF content semantics beyond embedding completion notes and updating paths. No rewriting historical completion content.

## Renaming / naming conventions (template first)
**AF item filename template**
- `AF####_STATUS_three_word_description.md`
  - `####` = zero-padded numeric id (e.g., 0034)
  - `STATUS` ∈ `Proposed | Ready | In_progress | Blocked | Done | Dropped`
  - `three_word_description` = snake_case slug derived from the AF title (first ~3 meaningful words)

**Template merge**
- `docs/dev/backlog/templates/BACKLOG_ITEM_TEMPLATE.md` + `docs/dev/backlog/templates/COMPLETION_NOTE_TEMPLATE.md`
  → `docs/dev/backlog/templates/BACKLOG_ITEM_TEMPLATE.md` (includes “Completion” section)

**Completion folder deprecation**
- `docs/dev/backlog/completion/*` is deprecated; completion content is migrated into the corresponding AF item file (Completion section).


## Files that change

### Legacy (`/docs/dev/`)
- `docs/dev/backlog/INDEX.md`
- `docs/dev/backlog/templates/BACKLOG_ITEM_TEMPLATE.md`
- `docs/dev/backlog/templates/COMPLETION_NOTE_TEMPLATE.md`
- `docs/dev/backlog/items/AF-0001.md`
- `docs/dev/backlog/items/AF-0002.md`
- `docs/dev/backlog/items/AF-0003.md`
- `docs/dev/backlog/items/AF-0004.md`
- `docs/dev/backlog/items/AF-0005.md`
- `docs/dev/backlog/items/AF-0006.md`
- `docs/dev/backlog/items/AF-0007.md`
- `docs/dev/backlog/items/AF-0008.md`
- `docs/dev/backlog/items/AF-0009.md`
- `docs/dev/backlog/items/AF-0010.md`
- `docs/dev/backlog/items/AF-0011.md`
- `docs/dev/backlog/items/AF-0012.md`
- `docs/dev/backlog/items/AF-0013.md`
- `docs/dev/backlog/items/AF-0014.md`
- `docs/dev/backlog/items/AF-0015.md`
- `docs/dev/backlog/items/AF-0016.md`
- `docs/dev/backlog/items/AF-0017.md`
- `docs/dev/backlog/items/AF-0018.md`
- `docs/dev/backlog/items/AF-0019.md`
- `docs/dev/backlog/items/AF-0021-storage-lifecycle-hardening.md`
- `docs/dev/backlog/items/AF-0022-provider-coverage-hardening.md`
- `docs/dev/backlog/items/AF-0023-environment-configuration-hardening.md`
- `docs/dev/backlog/items/AF-0024-workspace-lifecycle-correction.md`
- `docs/dev/backlog/items/AF-0025-test-discipline-enforcement.md`
- `docs/dev/backlog/items/AF-0026-workspace-selection-policy-enforcement.md`
- `docs/dev/backlog/items/AF-0027.md`
- `docs/dev/backlog/items/AF-0028.md`
- `docs/dev/backlog/items/AF-0029.md`
- `docs/dev/backlog/items/AF-0030.md`
- `docs/dev/backlog/items/AF-0031.md`
- `docs/dev/backlog/items/AF-0032.md`
- `docs/dev/backlog/items/AF-0033.md`
- `docs/dev/backlog/items/AF-0034-workspace-error-hardening.md`
- `docs/dev/backlog/items/AF-0035-clarify-workspace-flag-help.md`
- `docs/dev/backlog/items/AF-0036-remove-global-cli-flags.md`
- `docs/dev/backlog/items/AF-0037-standardize-workspace-errors.md`
- `docs/dev/backlog/items/AF-0038-json-error-path-consistency.md`
- `docs/dev/backlog/completion/2026-02-24_AF-0004_sprint-os-hygiene.md`
- `docs/dev/backlog/completion/2026-02-24_AF-0005_contracts.md`
- `docs/dev/backlog/completion/2026-02-24_AF-0006_storage-baseline.md`
- `docs/dev/backlog/completion/2026-02-24_AF-0007_runtime-skeleton.md`
- `docs/dev/backlog/completion/2026-02-24_AF-0008_cli-v0-truthful.md`
- `docs/dev/backlog/completion/2026-02-24_AF-0009_artifacts-v0.md`
- `docs/dev/backlog/completion/2026-02-24_AF-0010_python-bootstrap.md`
- `docs/dev/backlog/completion/2026-02-26_AF-0011_cli-global-options.md`
- `docs/dev/backlog/completion/2026-02-26_AF-0014_recorder-protocol.md`
- `docs/dev/backlog/completion/2026-02-26_AF-0016_reasoning-mode-fix.md`
- `docs/dev/backlog/completion/2026-02-26_AF-0017_openai-adapter.md`
- `docs/dev/backlog/completion/2026-02-26_AF-0018_provider-abstraction.md`
- `docs/dev/backlog/completion/2026-02-26_AF-0019_delegation-playbook.md`
- `docs/dev/backlog/completion/2026-02-26_AF-0021_storage-lifecycle-hardening.md`
- `docs/dev/backlog/completion/2026-02-26_AF-0022_provider-coverage-hardening.md`
- `docs/dev/backlog/completion/2026-02-26_AF-0023_environment-configuration-hardening.md`
- `docs/dev/backlog/completion/2026-02-26_AF-0024_workspace-lifecycle-correction.md`
- `docs/dev/backlog/completion/2026-02-26_AF-0025_test-discipline-enforcement.md`
- `docs/dev/backlog/completion/2026-02-26_AF-0026_workspace-selection-policy.md`
- `docs/dev/backlog/completion/2026-02-27_AF-0027_default-workspace-policy.md`
- `docs/dev/backlog/completion/2026-02-27_AF-0028_run-id-formatting.md`
- `docs/dev/backlog/completion/2026-02-27_AF-0029_runtrace-verification-hardening.md`
- `docs/dev/backlog/completion/2026-02-27_AF-0030_runtrace-metadata-completeness.md`
- `docs/dev/backlog/completion/2026-02-27_AF-0031_cli-truthfulness-enforcement.md`
- `docs/dev/backlog/completion/2026-02-27_AF-0032_observability-command-expansion.md`
- `docs/dev/backlog/completion/2026-02-27_AF-0033_dotenv-loading.md`
- `docs/dev/backlog/completion/ONBOARDING_SUMMARY_JACOB.md`
- `docs/dev/backlog/completion/README.md`

### Canonical (`/docs/dev/`)
- `docs/dev/backlog/INDEX_BACKLOG.md`
- `docs/dev/backlog/templates/BACKLOG_ITEM_TEMPLATE.md`
- `docs/dev/backlog/items/AF0001_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0002_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0003_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0004_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0005_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0006_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0007_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0008_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0009_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0010_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0011_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0012_Ready_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0013_Ready_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0014_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0015_Ready_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0016_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0017_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0018_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0019_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0021_Done_storage_lifecycle_hardening.md`
- `docs/dev/backlog/items/AF0022_Done_provider_coverage_hardening.md`
- `docs/dev/backlog/items/AF0023_Done_environment_configuration_hardening.md`
- `docs/dev/backlog/items/AF0024_Done_workspace_lifecycle_correction.md`
- `docs/dev/backlog/items/AF0025_Done_test_discipline_enforcement.md`
- `docs/dev/backlog/items/AF0026_Done_workspace_selection_policy.md`
- `docs/dev/backlog/items/AF0027_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0028_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0029_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0030_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0031_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0032_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0033_Done_title_slug_tbd.md`
- `docs/dev/backlog/items/AF0034_Ready_workspace_error_hardening.md`
- `docs/dev/backlog/items/AF0035_Ready_clarify_workspace_flag.md`
- `docs/dev/backlog/items/AF0036_Ready_remove_global_cli.md`
- `docs/dev/backlog/items/AF0037_Ready_standardize_workspace_errors.md`
- `docs/dev/backlog/items/AF0038_Ready_json_error_path.md`

## Acceptance criteria (Definition of Done)
- [ ] `docs/dev/backlog/templates/BACKLOG_ITEM_TEMPLATE.md` exists and includes the Completion section
- [ ] All AF items from `/docs/dev/backlog/items/` are migrated into `/docs/dev/backlog/items/` with the new filename convention
- [ ] All completion notes from `/docs/dev/backlog/completion/` are copied into the corresponding AF item’s Completion section, then the legacy completion notes are marked deprecated (or removed only after sprint acceptance)
- [ ] `docs/dev/backlog/INDEX_BACKLOG.md` exists and links to the canonical AF files
- [ ] Statuses are consistent across: filename STATUS ↔ internal Metadata Status ↔ INDEX_BACKLOG status column

## Implementation notes
For historical items without a slug in filename, derive `three_word_description` from the AF title inside the file. Keep a deterministic slugging rule and apply consistently.

## Risks
Large rename diff may be noisy; mitigate by doing it as a docs-only PR and keeping the mapping list explicit in the PR description.

## PR plan (PR-sized)
1. PR: Create merged BACKLOG_ITEM_TEMPLATE in `/docs/dev/backlog/templates/`
2. PR: Migrate AF items (rename + move) + embed completion notes + create/update INDEX_BACKLOG

