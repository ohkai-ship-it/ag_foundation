# AF0009 — Artifact registry v0 + ag artifacts list
# Version number: v0.3

## Metadata
- **ID:** AF-0009
- **Type:** Feature
- **Status:** DONE
- **Priority:** P1
- **Area:** Storage
- **Owner:** Jacob
- **Completed in:** Sprint 01
- **Completion date:** 2026-02-24

## Problem
Run outputs need to be discoverable; artifact registry enables reproducibility and API/UI parity later.

## Goal
Implement artifact indexing and listing per run; Recorder registers at least one artifact when runtime produces file-like output.

## Non-goals
- Artifact open/export beyond listing.
- Remote storage.
- Complex artifact types.

## Acceptance criteria (Definition of Done)
- [x] ArtifactMetadata schema exists and an artifacts table exists in SQLite (can be minimal).
- [x] If no artifacts exist, `ag artifacts list --run <id>` returns an empty list (stable behavior).
- [x] Recorder registers a simple artifact (e.g., `result.md`) created by a step in manual mode.
- [x] `ag artifacts list --run <run_id>` supports human output and `--json`.
- [x] Integration test: run creates artifact and `ag artifacts list --run` returns it.

## Implementation notes
- Keep artifact IDs stable-ish (run_id + counter). `artifact://` URIs resolve relative to workspace.

## Risks
P1: trace/storage coupling; mitigate by keeping registry operations in storage layer and referencing via schema.

## PR plan
1. PR (feat/artifacts-v0): Implement artifact indexing + CLI list command + integration test.

---
# Completion section (fill when done)

**Completion date:** 2026-02-24  
**Author:** Jacob (Junior Engineer)

**Summary:**
Implemented artifact registry v0 with artifact indexing, automatic `result.md` generation on run completion, and `ag artifacts list` CLI command with human and JSON output support.

**What Was Done:**

1. **Artifact Registration in Runtime** (`src/ag/core/runtime.py`)
   - V0Orchestrator creates `result.md` artifact after each run
   - Artifact ID format: `{run_id}-result`
   - Type: `text/markdown`

2. **`_build_result_artifact()` Method** — Generates Markdown content with run metadata and step summaries

3. **`ag artifacts list` Command** (`src/ag/cli/main.py`)
   - Required options: `--run`, `--workspace`
   - Human output: Rich table with ID, type, size, path
   - JSON output: Array of artifact objects

4. **Test Suite** (`tests/test_artifacts.py`)
   - 11 tests: schema validation, SQLite table, artifact creation, CLI behavior, integration

**Sample result.md:**
```markdown
# Run Result: abc123-def456-...
- **Status:** success
- **Mode:** manual
## Steps
### ✓ Step 0: reasoning
### ✓ Step 1: skill_call
```

**Test Results:** 11 passed

