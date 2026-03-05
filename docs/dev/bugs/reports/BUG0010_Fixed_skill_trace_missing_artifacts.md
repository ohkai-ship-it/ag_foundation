# BUG REPORT --- BUG0010 --- skill_trace_missing_artifacts

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

-   **ID:** BUG0010
-   **Status:** Fixed
-   **Severity:** P0
-   **Area:** Core Runtime \| Recorder \| Skills \| Storage
-   **Reported by:** Kai
-   **Date:** 2026-03-05
-   **Fixed date:** 2026-03-05
-   **Related backlog item(s):** AF0057 (proposed)
-   **Related ADR(s):** (optional)
-   **Related PR(s):** (optional)

------------------------------------------------------------------------

## Summary

Direct execution of `strategic_brief` produces output files, but
RunTrace does not record artifacts or evidence refs: - `artifacts: []` -
`evidence_refs: null`

This makes outputs undiscoverable via trace-derived UX and breaks audit
expectations.

------------------------------------------------------------------------

## Expected behavior

RunTrace should include: - step-level artifacts (brief.md, brief.json,
result json, etc.) - run-level artifact aggregation - evidence refs for
cited material where applicable

------------------------------------------------------------------------

## Actual behavior

RunTrace shows empty artifacts and null evidence_refs even when outputs
include citations/excerpts.

------------------------------------------------------------------------

## Reproduction steps

1.  Run:
    -   `ag run --workspace sprint05_demo --skill strategic_brief "Generate a structured strategic brief ..."`
2.  Inspect trace:
    -   `ag runs show --workspace sprint05_demo <run_id> --json`
3.  Observe `artifacts: []` and `evidence_refs: null`.

------------------------------------------------------------------------

## Evidence

-   **RunTrace ID(s):** `21971e86-6e45-4986-b996-da8e01487e2d`
-   **Artifacts (filesystem):**
    -   `21971e86-...-strategic_brief_brief_strategic_brief_brief.md`
    -   `21971e86-...-strategic_brief_result_strategic_brief_result.json`
-   **Environment:** Windows, PowerShell, venv; commit hash: (fill)

------------------------------------------------------------------------

## Impact

-   User cannot discover outputs via `ag runs show` / trace-derived UX.
-   Breaks evidence capture invariant and weakens trust in citations.
-   Sprint05 exit criteria (evidence traceability + artifact lifecycle
    discipline) not validated in human path.

------------------------------------------------------------------------

## Suspected cause (optional)

Skill writes files directly (or returns output) without emitting
artifact descriptors into the recorder/trace pipeline.

------------------------------------------------------------------------

## Proposed fix (optional)

Standardize skill return contract to include artifact descriptors and
evidence refs; recorder persists them into trace and artifact registry.

------------------------------------------------------------------------

## Acceptance criteria (for verification)

-   [ ] Repro steps no longer trigger the issue
-   [ ] Tests added/updated (integration test asserts
    artifacts/evidence_refs in trace)
-   [ ] `pytest -W error` passes
-   [ ] `ruff check src tests` passes
-   [ ] Evidence captured (new RunTrace ID showing populated artifacts +
    evidence_refs)

------------------------------------------------------------------------

## Notes

Prefer reusing existing RunTrace fields (`artifacts`, `evidence_refs`)
with additive-only changes.

------------------------------------------------------------------------

## Status log (optional)

-   2026-03-05 --- Opened by Kai
