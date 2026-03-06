# BACKLOG ITEM --- AF0051 --- Artifact export hardening

## Metadata

-   **ID:** AF0051
-   **Type:** Feature
-   **Status:** Done
-   **Priority:** P1
-   **Area:** Storage
-   **Owner:** Jacob
-   **Target sprint:** Sprint05 --- High_Pressure_Skills

------------------------------------------------------------------------

## Problem

Current architecture has not been forced through a realistic, multi-file
structured-output scenario.

------------------------------------------------------------------------

## Goal

Improve artifact registry with typed artifacts and deterministic export
command.

------------------------------------------------------------------------

## Non-goals

-   No API layer
-   No full RAG implementation
-   No policy engine formalization

------------------------------------------------------------------------

## Acceptance criteria

-   [x] Implementation complete
-   [x] Naming conventions applied
-   [x] INDEX updated
-   [x] CI passes (ruff + pytest -W error + coverage)
-   [ ] Evidence captured (RunTrace ID)
-   [ ] Completion section filled when done

------------------------------------------------------------------------

## Risks

-   Architectural stress may expose hidden contract weaknesses

------------------------------------------------------------------------

# Completion section (to fill when done)

## Implementation summary

Added **typed artifacts** with `ArtifactCategory` enum and **deterministic export** CLI command.

### Typed Artifacts (ArtifactCategory enum in run_trace.py)

Categories:
- `RESULT` - Primary run outputs (e.g., result.md)
- `LOG` - Execution logs
- `TRACE` - RunTrace JSON
- `CONFIG` - Configuration files
- `DOCUMENT` - Markdown, text documents
- `DATA` - JSON, YAML structured data
- `CODE` - Source code files
- `IMAGE` - Images, charts, diagrams
- `BINARY` - Generic binary content
- `UNKNOWN` - Fallback for untyped

### Category Inference

`infer_artifact_category(artifact_type, path)` infers category from MIME type and file path:
- Code files (.py, .js, .ts, etc.) → CODE
- result in path → RESULT
- trace in path → TRACE
- .log files → LOG
- config/settings files → CONFIG
- text/* MIME → DOCUMENT
- image/* MIME → IMAGE
- application/octet-stream → BINARY

### CLI Commands

1. **ag artifacts show** - Displays artifact details and content preview
   - Shows category, type, size, checksum, timestamps
   - Previews first 20 lines of text-based artifacts
   - Supports --json output

2. **ag artifacts export** - Exports artifact to local file
   - `ag artifacts export <id> --run <run> --workspace <ws> --to <path>`
   - Creates parent directories automatically
   - Supports --force to overwrite existing files

## Files changed

- `src/ag/core/run_trace.py` - Added ArtifactCategory enum, category field, infer_artifact_category()
- `src/ag/core/__init__.py` - Export new types
- `src/ag/cli/main.py` - Implemented artifacts show and export commands
- `tests/test_artifacts.py` - Added 21 new tests for categories and CLI

## Test results

- 32 tests in test_artifacts.py (21 new), all passing
- 276 tests total (excluding provider tests), all passing
- Coverage: 79% overall, 100% on run_trace.py

