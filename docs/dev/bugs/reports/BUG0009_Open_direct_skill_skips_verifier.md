# BUG REPORT --- BUG0009 --- direct_skill_skips_verifier

# Version number: v0.1

> **FOUNDATION GOVERNANCE** This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context: - Truthful UX (trace-derived
> labels) - Workspace isolation - CI discipline (ruff + pytest -W
> error + coverage) - INDEX update rule (status ↔ filename integrity) -
> Evidence capture requirement (RunTrace ID for CLI/runtime bugs)

> **File naming (required):**
> `BUG####_<Status>_<three_word_description>.md` Status values:
> `Open | In progress | Fixed | Verified | Dropped`

------------------------------------------------------------------------

## Metadata

-   **ID:** BUG0009
-   **Status:** Open
-   **Severity:** P0
-   **Area:** CLI \| Core Runtime \| Verifier
-   **Reported by:** Kai
-   **Date:** 2026-03-05
-   **Related backlog item(s):** AF0056 (proposed)
-   **Related ADR(s):** (optional)
-   **Related PR(s):** (optional)

------------------------------------------------------------------------

## Summary

Direct skill execution path (playbook `skill:<name>` or
`ag run --skill ...`) skips verifier, producing
`verifier.status = skipped` while still reporting run `final = success`.

------------------------------------------------------------------------

## Expected behavior

Verifier should run by default for direct skill execution and record
validation results (including schema validation / repair loop outcomes)
in RunTrace.

------------------------------------------------------------------------

## Actual behavior

RunTrace contains: - `verifier.status: "skipped"` -
`verifier.message: "Direct skill execution - verifier skipped"`

------------------------------------------------------------------------

## Reproduction steps

1.  Create / use a workspace with markdown files (e.g., `sprint05_demo`)
2.  Run (after CLI routing bug fix):
    -   `ag run --workspace sprint05_demo --skill strategic_brief "Generate a structured strategic brief ..."`
3.  Inspect trace:
    -   `ag runs show --workspace sprint05_demo <run_id> --json`
4.  Observe verifier skipped.

------------------------------------------------------------------------

## Evidence

-   **RunTrace ID(s):** `21971e86-6e45-4986-b996-da8e01487e2d`
-   **CLI output:** run reports `success` while verifier skipped (see
    RunTrace).
-   **Artifacts:** brief + result JSON produced externally.
-   **Environment:** Windows, PowerShell, venv; commit hash: (fill)

------------------------------------------------------------------------

## Impact

-   Breaks "truthful UX" invariant: user sees success without
    verification.
-   Sprint05 exit criteria (verifier loop) not validated in the human
    path.
-   Reduces trust in structured outputs.

------------------------------------------------------------------------

## Suspected cause (optional)

Direct skill path bypasses orchestrator/verifier stage and finalizes run
immediately after skill completion.

------------------------------------------------------------------------

## Proposed fix (optional)

Route direct skill execution through verifier by default; add
`--no-verify` if needed.

------------------------------------------------------------------------

## Acceptance criteria (for verification)

-   [ ] Repro steps no longer trigger the issue
-   [ ] Tests added/updated (integration test for `--skill` path)
-   [ ] `pytest -W error` passes
-   [ ] `ruff check src tests` passes
-   [ ] Evidence captured (new RunTrace ID showing verifier ran)

------------------------------------------------------------------------

## Notes

Ensure verifier results are trace-derived and user-visible via
`ag runs show`.

------------------------------------------------------------------------

## Status log (optional)

-   2026-03-05 --- Opened by Kai
