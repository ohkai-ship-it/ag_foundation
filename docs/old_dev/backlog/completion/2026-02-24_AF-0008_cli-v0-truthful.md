# Handoff Note — AF-0008 — CLI v0 Truthful Labels
**Date:** 2026-02-24
**Author:** Jacob (Junior Engineer)
**Status:** Ready for review

---

## Summary
Implemented CLI v0 with `ag run`, `ag runs show --json`, and `ag runs list` commands. All labels are derived from persisted RunTrace data (truthful UX). Manual mode gating enforced with explicit tests.

## What Was Done

### 1. CLI Runtime Integration (`src/ag/cli/main.py`)
- Updated `ag run` to use actual runtime execution
- Integrated with `SQLiteRunStore` for persistence
- Added `create_runtime()` factory for test injection

### 2. Truthful Labels (`extract_labels()` helper)
- All CLI labels derived from persisted RunTrace fields
- Labels extracted: `mode`, `status`, `verifier_status`, `duration`, `playbook`
- No hardcoded or fabricated display values

### 3. `ag runs show --json` Command
- Outputs full RunTrace as JSON
- Conforms to RunTrace schema
- Parseable for programmatic verification

### 4. `ag runs list` Command
- Lists runs in workspace, most recent first
- Shows run_id, status, mode, playbook, duration
- Falls back gracefully when workspace doesn't exist

### 5. Manual Mode Gate (enhanced)
- `--mode manual` requires `AG_DEV=1` environment variable
- Clear error message on gate failure
- Banner: `DEV MODE: manual (LLMs disabled)`
- Banner suppressed when `--json` is used (to not corrupt JSON output)

### 6. Test Suite (`tests/test_cli_truthful.py`)
14 tests covering:
- Manual mode gate (with/without env var)
- Truthful label extraction
- CLI labels match trace fields
- JSON output conformance
- Runs list functionality
- Label consistency between run and show

---

## Acceptance Criteria

- [x] `--mode manual` requires `AG_DEV=1`; without it, exits non-zero with clear error
- [x] Manual mode prints banner: `DEV MODE: manual (LLMs disabled)`
- [x] RunTrace `mode` field is `manual` when the flag is used
- [x] Tests: manual mode without env var fails; with env var succeeds and trace.mode == manual
- [x] Truthful label tests validate CLI labels against parsed RunTrace JSON
- [x] `ag runs show <run_id> --json` outputs JSON that conforms to RunTrace schema

---

## Test Results

```
tests/test_cli_truthful.py::TestManualModeGateExtended::test_manual_mode_banner_printed PASSED
tests/test_cli_truthful.py::TestManualModeGateExtended::test_manual_mode_trace_has_manual_mode PASSED
tests/test_cli_truthful.py::TestManualModeGateExtended::test_without_ag_dev_manual_mode_fails PASSED
tests/test_cli_truthful.py::TestTruthfulLabels::test_extract_labels_matches_trace PASSED
tests/test_cli_truthful.py::TestTruthfulLabels::test_cli_mode_label_matches_trace PASSED
tests/test_cli_truthful.py::TestTruthfulLabels::test_cli_verifier_status_matches_trace PASSED
tests/test_cli_truthful.py::TestTruthfulLabels::test_cli_duration_matches_trace PASSED
tests/test_cli_truthful.py::TestRunsShowJsonConformance::test_runs_show_json_has_all_required_fields PASSED
tests/test_cli_truthful.py::TestRunsShowJsonConformance::test_runs_show_json_can_parse_as_runtrace PASSED
tests/test_cli_truthful.py::TestRunsShowJsonConformance::test_runs_show_json_matches_original_trace PASSED
tests/test_cli_truthful.py::TestRunsList::test_runs_list_shows_runs PASSED
tests/test_cli_truthful.py::TestRunsList::test_runs_list_empty_workspace PASSED
tests/test_cli_truthful.py::TestRunsList::test_runs_list_requires_workspace PASSED
tests/test_cli_truthful.py::TestLabelConsistency::test_run_and_show_labels_match PASSED

14 passed
```

---

## Truthful UX Verification

| CLI Label | RunTrace Field | Proof |
|-----------|---------------|-------|
| Mode | `trace.mode` | `test_cli_mode_label_matches_trace` |
| Status | `trace.final` | `test_extract_labels_matches_trace` |
| Verifier | `trace.verifier.status` | `test_cli_verifier_status_matches_trace` |
| Duration | `trace.duration_ms` | `test_cli_duration_matches_trace` |
| Playbook | `trace.playbook.name@version` | `test_extract_labels_matches_trace` |

---

## Files Changed

| File | Change |
|------|--------|
| `src/ag/cli/main.py` | Updated run command, added extract_labels(), fixed JSON+banner |
| `tests/test_cli.py` | Updated test expectations for runtime output |
| `tests/test_cli_truthful.py` | New: 14 truthful label tests |

---

## Architecture Alignment

- **Layering:** CLI adapter layer - renders from stored trace, no business logic
- **Interfaces touched:** Uses RunTrace, Verifier status from core
- **Backward compatibility:** CLI output format changed (now shows real data)

---

## Branch & PR

- **Branch:** `feat/cli-v0`
- **Pushed:** Yes (to origin)
