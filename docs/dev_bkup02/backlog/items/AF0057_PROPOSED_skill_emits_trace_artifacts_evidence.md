# BACKLOG ITEM --- AF0057 --- skill_emits_trace_artifacts_evidence

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

-   **ID:** AF0057
-   **Type:** Foundation
-   **Status:** Ready
-   **Priority:** P0
-   **Area:** Core Runtime / Recorder / Skills
-   **Owner:** Jacob
-   **Target sprint:** TBD (needs discussion)

------------------------------------------------------------------------

## Problem

Human run outputs show the strategic brief markdown + structured JSON
were produced, but the RunTrace contains: - `artifacts: []` at step and
run level - `evidence_refs: null`

This breaks trace/audit expectations and makes outputs non-discoverable
via trace-derived UX.

------------------------------------------------------------------------

## Goal

Ensure skill execution records: - produced artifacts into the artifact
registry and RunTrace (`artifacts` populated) - evidence references into
RunTrace (`evidence_refs` populated where applicable)

This must work for direct skill execution (`--skill`) and default
playbook execution.

------------------------------------------------------------------------

## Non-goals

-   No full artifact export/import redesign
-   No retrieval/indexing changes

------------------------------------------------------------------------

## Acceptance criteria (Definition of Done)

-   [ ] After `ag run --skill strategic_brief ...`, RunTrace step
    includes artifact references (non-empty)
-   [ ] RunTrace run-level `artifacts` is non-empty and includes brief
    outputs (md + json)
-   [ ] `evidence_refs` populated for the synthesis/brief step (or
    explicitly "none used" if truly none)
-   [ ] Artifacts are discoverable via CLI
    (`ag artifacts list --run <id>`) and match trace
-   [ ] Tests added/updated:
    -   [ ] Integration test asserts `artifacts` and `evidence_refs`
        fields are populated as expected
-   [ ] CI/local checks pass (ruff + pytest -W error + coverage
    thresholds)
-   [ ] Evidence included: RunTrace ID(s) captured in PR

------------------------------------------------------------------------

## Implementation notes

-   Ensure skills return a structured result that includes:
    -   artifact descriptors (type, path, id)
    -   evidence refs (file path + line ranges or excerpt IDs)
-   Recorder must persist these into trace consistently (step-level and
    run-level aggregation).
-   Keep backward compatibility: additive fields only.

------------------------------------------------------------------------

## Risks

-   Trace schema expansion: if new fields required, treat as P1+ and
    update ARCHITECTURE + compat notes.
    -   Prefer using existing `artifacts` and `evidence_refs` fields
        first.

------------------------------------------------------------------------

# Completion section (fill when done)

## 1) Metadata

-   **Backlog item (primary):** AF0057
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
-   **Interfaces touched:** Recorder / Skill contract / Artifact
    registry
-   **Backward compatibility:** yes/no + details

------------------------------------------------------------------------

