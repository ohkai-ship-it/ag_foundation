# BACKLOG ITEM --- AF0056 --- direct_skill_runs_verifier

# Version number: v0.1

> **FOUNDATION GOVERNANCE** This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context: - Truthful UX (trace-derived
> labels) - Workspace isolation - CI discipline (ruff + pytest -W
> error + coverage) - 1 PR = 1 primary AF - INDEX update rule (status ↔
> filename integrity)

> **File naming (required):**
> `AF####_<Status>_<three_word_description>.md` Status values:
> `Proposed | Ready | In progress | Blocked | Done | Dropped`

------------------------------------------------------------------------

## Metadata

-   **ID:** AF0056
-   **Type:** Foundation
-   **Status:** DROPPED
-   **Priority:** P0
-   **Area:** Core Runtime / Verifier / CLI
-   **Owner:** Jacob
-   **Target sprint:** N/A (dropped)

---

## Drop rationale

**Dropped 2026-03-08** — This AF was already fixed via BUG-0009.

The direct skill execution path (`ag run --skill`) now runs the verifier 
by default. See `src/ag/cli/main.py` lines 468-475:

```python
# BUG0009: Run verifier on step (not skipped)
from ag.core.runtime import V0Verifier
verifier = V0Verifier()
final_status = FinalStatus.SUCCESS if success else FinalStatus.FAILURE
verify_status, verify_message = verifier.verify_components([step], final_status)
```

No further work needed.

------------------------------------------------------------------------

## Problem (original)

Direct skill execution via CLI (e.g.,
`ag run --skill strategic_brief ...`) currently skips verifier
execution, yielding `verifier.status = skipped` even when Sprint05
requires schema validation + repair loop behavior.

This breaks the "truthful UX" invariant: a human run reports `success`
without running verification.

------------------------------------------------------------------------

## Goal

Ensure direct skill execution runs the verifier by default and records
verifier results in RunTrace.

Introduce an explicit opt-out (only if needed) such as: - `--no-verify`
(default verify = on)

------------------------------------------------------------------------

## Non-goals

-   No new verifier policies beyond Sprint05 scope
-   No retrieval/indexing work
-   No UI changes

------------------------------------------------------------------------

## Acceptance criteria (Definition of Done)

-   [ ] Direct skill execution runs verifier by default (no "skipped"
    unless `--no-verify` is set)
-   [ ] RunTrace `verifier` section includes schema validation summary
    and any repair attempts (if applicable)
-   [ ] CLI output remains trace-derived (no hardcoded "passed")
-   [ ] Tests added/updated:
    -   [ ] Integration test: `ag run --skill strategic_brief ...`
        produces `verifier.status != skipped`
-   [ ] CI/local checks pass (as applicable):
    -   [ ] `ruff check src tests`\
    -   [ ] `ruff format --check src tests` (or
        `ruff format src tests`)\
    -   [ ] `pytest -W error`\
    -   [ ] coverage thresholds met (see TESTING_GUIDELINES)
-   [ ] Evidence included: new RunTrace ID(s) from integration test
-   [ ] Completion section filled when Status = Done

------------------------------------------------------------------------

## Implementation notes

-   Wire direct-skill playbook path to the same verification stage as
    default orchestration.
-   If a "skill:XYZ" playbook bypasses orchestrator, either:
    -   route through orchestrator anyway, or
    -   call verifier explicitly after skill returns output and before
        finalizing run.
-   Ensure verifier evidence is persisted and rendered from RunTrace.

------------------------------------------------------------------------

## Risks

-   Tight coupling between CLI adapter and runtime stages if implemented
    in the wrong layer.
    -   Mitigation: keep `--no-verify` parsing in CLI adapter, but
        execute verification in core runtime.

------------------------------------------------------------------------

# Completion section (fill when done)

## 1) Metadata

-   **Backlog item (primary):** AF0056
-   **PR:** \#`<number>`{=html}
-   **Author:** `<name>`{=html}
-   **Date:** YYYY-MM-DD
-   **Branch:** \<feat/... \| fix/... \| chore/...\>
-   **Risk level:** P0
-   **Runtime mode used for verification:** llm \| manual
    (dev/test-only)

------------------------------------------------------------------------

## 2) Acceptance criteria verification

-   [ ] ...

------------------------------------------------------------------------

## 3) What changed (file-level)

-   `<path/to/file>` --- ...

------------------------------------------------------------------------

## 4) Architecture alignment (mandatory)

-   **Layering:** ...
-   **Interfaces touched:** CLI / Orchestrator / Verifier / Recorder
    (specify)
-   **Backward compatibility:** yes/no + details

------------------------------------------------------------------------

