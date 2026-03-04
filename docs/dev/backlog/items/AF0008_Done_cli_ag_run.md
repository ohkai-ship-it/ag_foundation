# AF0008 — CLI v0: ag run + runs show --json, truthful labels tests, manual dev gate
# Version number: v0.3

## Metadata
- **ID:** AF-0008
- **Type:** Feature
- **Status:** Done
- **Priority:** P0
- **Area:** CLI
- **Owner:** Jacob
- **Completed in:** Sprint 01
- **Completion date:** 2026-02-24

## Problem
CLI must be truthful: labels derived from persisted RunTrace facts; manual mode dev-only. Must be explicitly testable.

## Goal
Implement `ag run`, `ag runs show --json`, minimal `ag runs list`, with manual-mode gating and automated tests proving CLI labels match RunTrace fields.

## Non-goals
- Real LLM mode.
- Full workspace management.
- Artifact UX beyond listing (AF-0009).

## Acceptance criteria (Definition of Done)
- [x] `--mode manual` requires `AG_DEV=1`; without it, command exits non-zero with clear error.
- [x] Manual mode prints banner: `DEV MODE: manual (LLMs disabled)` (stable wording).
- [x] RunTrace `mode` field is `manual` when the flag is used (visible via `ag runs show --json`).
- [x] Tests: manual mode without env var fails; with env var succeeds and trace.mode == manual.
- [x] Truthful label tests validate CLI labels (at minimum: mode, verifier.status, duration) against parsed RunTrace JSON.
- [x] `ag runs show <run_id> --json` outputs JSON that conforms to RunTrace schema and passes contract validation.

## Implementation notes
- CLI adapter-only; render from stored trace.
- Provide label-extraction helper; tests compare helper output to CLI output.

## Risks
P0: untruthful UX or gate bypass. Mitigate with explicit gate tests + label/trace consistency tests.

## PR plan
1. PR (feat/cli-v0): Implement run/show/list + manual gate + truthful label tests.

---
# Completion section (fill when done)

**Completion date:** 2026-02-24  
**Author:** Jacob (Junior Engineer)

**Summary:**
Implemented CLI v0 with `ag run`, `ag runs show --json`, and `ag runs list` commands. All labels are derived from persisted RunTrace data (truthful UX). Manual mode gating enforced with explicit tests.

**What Was Done:**

1. **CLI Runtime Integration** (`src/ag/cli/main.py`)
   - Updated `ag run` to use actual runtime execution
   - Integrated with SQLiteRunStore for persistence

2. **Truthful Labels** (`extract_labels()` helper)
   - All CLI labels derived from persisted RunTrace fields
   - Labels: mode, status, verifier_status, duration, playbook

3. **`ag runs show --json`** — Outputs full RunTrace as JSON

4. **`ag runs list`** — Lists runs in workspace

5. **Manual Mode Gate**
   - `--mode manual` requires AG_DEV=1
   - Banner: `DEV MODE: manual (LLMs disabled)`
   - Banner suppressed in --json mode

6. **Test Suite** (`tests/test_cli_truthful.py`)
   - 14 tests: manual mode gate, truthful labels, JSON conformance, runs list

**Truthful UX Verification:**
| CLI Label | RunTrace Field |
|-----------|---------------|
| Mode | trace.mode |
| Status | trace.final |
| Verifier | trace.verifier.status |
| Duration | trace.duration_ms |
| Playbook | trace.playbook.name@version |

**Test Results:** 14 passed
