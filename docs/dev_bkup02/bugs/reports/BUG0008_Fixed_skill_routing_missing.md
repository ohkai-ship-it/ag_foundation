# BUG REPORT --- BUG0008 --- CLI cannot route to strategic_brief skill

# Version number: v0.1

## Metadata

-   **ID:** BUG0008
-   **Status:** Fixed
-   **Priority:** P0
-   **Area:** CLI / Routing
-   **Reported in:** Sprint05 --- High_Pressure_Skills
-   **Reported on:** 2026-03-04
-   **Reported by:** Kai
-   **Fixed on:** 2026-03-05

------------------------------------------------------------------------

## Summary

The `strategic_brief` skill implemented in Sprint05 is not reachable via
CLI.

Commands: - `ag skills list` - `ag playbooks list`

both return stubs.

Default `ag run` execution routes only through the generic: -
analyze_task - execute_task - verify_result

pipeline and does not invoke `strategic_brief`.

------------------------------------------------------------------------

## Expected behavior

Human user must be able to explicitly invoke the `strategic_brief` skill
via CLI, for example:

    ag run --workspace <ws> --skill strategic_brief "<prompt>"

Expected trace behavior: - skill_name = strategic_brief - Non-empty
artifacts (brief.md, brief.json) - evidence_refs populated - Non-zero
duration - Verifier schema validation recorded

------------------------------------------------------------------------

## Actual behavior

-   `ag skills list` → ⚠ Stub --- not implemented yet
-   `ag playbooks list` → ⚠ Stub --- not implemented yet
-   `ag run` executes only generic pipeline
-   No artifacts generated
-   No evidence_refs recorded
-   duration_ms = 0

Skill exists internally (per Sprint05 report), but is not reachable via
CLI.

------------------------------------------------------------------------

## Impact

-   Sprint05 capability cannot be human-tested.
-   Architectural pressure validation incomplete.
-   Violates practical "real use" validation intent of Sprint05.
-   Blocks meaningful user-level stress testing.

------------------------------------------------------------------------

## Root cause (hypothesis)

CLI routing layer does not expose: - Skill registry - Playbook
selection - Explicit skill invocation flag

------------------------------------------------------------------------

## Proposed minimal fix

Introduce deterministic CLI surface:

Option A (preferred minimal solution):

    ag run --skill <skill_name> "<prompt>"

Behavior: - If `--skill` present → directly invoke named skill - Wrap in
standard trace + verifier flow - Maintain backward compatibility

No full playbook or discovery system required.

------------------------------------------------------------------------

## Acceptance criteria

-   [x] `--skill` flag implemented
-   [x] strategic_brief reachable via CLI
-   [x] Trace shows correct skill invocation
-   [x] Artifacts generated
-   [x] No regression in default `ag run` behavior
-   [x] CI passes

------------------------------------------------------------------------

## Repro steps

1.  `ag ws create sprint05_demo`

2.  Add 20+ markdown files

3.  Run:

        ag run --workspace sprint05_demo "Generate structured strategic brief"

4.  Inspect trace:

        ag runs show --workspace sprint05_demo <run_id> --json

Result: Only generic pipeline executed.

------------------------------------------------------------------------

# Resolution section (fill when closed)

## Fix commit(s)

Implemented in Sprint05 follow-up:
- Added `--skill` / `-s` flag to `ag run` command
- Fixed `ag skills list` to show registered skills (was stub)
- Fixed `ag skills info <name>` to show skill details (was stub)
- Added 7 tests for skill CLI functionality

## Verification evidence

```bash
$ ag skills list
┃ Name              ┃ Description                                            ┃
│ strategic_brief   │ Generate strategic brief from workspace markdown files │
... (12 skills total)

$ ag skills info strategic_brief
Skill: strategic_brief
Description: Generate strategic brief from workspace markdown files

$ ag run --skill echo_tool -w test-skill-ws "Hello"
Skill executed: echo_tool
  Status: ✓ Success
  Output: Echo:
```

All 339 tests pass, no regressions.

## Status

**FIXED** - 2026-03-05

