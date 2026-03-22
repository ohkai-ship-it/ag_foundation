# BUG REPORT — BUG-0019 — V1Orchestrator drops required flag on expansion
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - INDEX update rule (status ↔ filename integrity)
> - Evidence capture requirement (RunTrace ID for CLI/runtime bugs)

> **File naming (required):** `BUG####_<STATUS>_<three_word_description>.md`
> Status values: `OPEN | IN_PROGRESS | FIXED | VERIFIED | DROPPED`

---

## Metadata
- **ID:** BUG-0019
- **Status:** OPEN
- **Severity:** P1
- **Area:** Core Runtime / Orchestrator
- **Reported by:** Kai
- **Date:** 2026-03-22
- **Related backlog item(s):** AF-0117 (V1 Orchestrator), AF-0115 (V1 Verifier)
- **Related ADR(s):** —
- **Related PR(s):** —

---

## Summary

When V1Orchestrator expands a PLAYBOOK step into individual skill steps, it does not propagate the `required` flag from the original `PlaybookStep` definition. All expanded steps default to `required=True`, causing V1Verifier to fail the run when an originally-optional step (like `load_documents` in `research_v0`) encounters an error.

---

## Expected behavior

When `research_v0` playbook defines `load_documents` as `required=False`:
- V1Orchestrator expands the playbook into skill steps
- The expanded `load_documents` step should have `required=False`
- V1Verifier should report `passed` because only optional steps failed

---

## Actual behavior

- V1Orchestrator expands `research_v0` into skill steps
- All expanded steps get `required=True` (the default)
- `load_documents` fails with `No files found matching patterns: ['**/*.md']`
- V1Verifier correctly fails the run because a "required" step failed
- Error: `Required step 'research_v0/load_local' failed: No files found matching patterns: ['**/*.md']`

---

## Reproduction steps

1. Ensure workspace `ws01` has no `.md` files in `inputs/`
2. Run: `ag run -y "Wetterbericht Düsseldorf"`
3. V2Planner selects `research_v0` as a PLAYBOOK step
4. V1Orchestrator expands it — `load_documents` becomes required
5. Run fails on the optional step

---

## Evidence

- **RunTrace ID:** `19eb2092-c433-4727-ab6f-80accdaa565c`
- **CLI output:**
  ```
  Run completed
  Plan ID: plan_7a91e086617c
  Run ID: 19eb2092-c433-4727-ab6f-80accdaa565c
  Workspace: ws01
  Autonomy: guided (inline plan)
  Status: failure
  Verifier: failed
  Duration: unknown
  Playbook: v2plan_423de579@1.0.0

  Error: Required step 'research_v0/load_local' failed: No files found matching patterns: ['**/*.md']
  ```
- **Environment:** Windows 11, Python 3.14.0a6, commit `04b1e9e` on `feat/sprint13-intelligent-pipeline`

---

## Root cause

V1Orchestrator's `_expand_steps()` method creates new `Step` objects from `PlaybookStep` entries but does not copy `PlaybookStep.required` into `Step.required`. The `Step` model defaults `required=True`, so all expanded steps are treated as mandatory.

---

## Proposed fix

**Decision (2026-03-22, Kai):** Use AND logic — the sub-step is required only if *both* the parent step and the playbook author agree.

In V1Orchestrator `_expand_steps()`, change the `required` assignment:

```python
inlined = PlaybookStep(
    ...
    required=step.required and sub_step.required,  # AND logic
)
```

Rationale: The playbook author knows which steps are optional (e.g., `load_documents` is `required=False` in `research_v0`). A parent step cannot promote an author-declared-optional sub-step to required — that overrides domain knowledge. AND is the conservative choice.

One-line fix in the orchestrator expansion code.

---

## Acceptance criteria

- [ ] Expanded playbook steps preserve `required` flag from PlaybookStep
- [ ] `ag run -y "Wetterbericht Düsseldorf"` with no local docs: Status=success, Verifier=passed
- [ ] Optional step failure recorded in trace but does not cause verifier failure
- [ ] Required step failure still causes verifier failure (regression check)
- [ ] New test: expanded optional PlaybookStep produces optional Step
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes

---

## Relationship to BUG-0017

BUG-0017 (FIXED in Sprint 13): V0Verifier had no concept of required/optional at all — it failed on any step error.

BUG-0019 (this): V1Verifier correctly respects `required`, but V1Orchestrator doesn't propagate it during playbook expansion. Different component, same symptom.

---

## Status log
- 2026-03-22 — Opened by Kai (reproduced with run `19eb2092-c433-4727-ab6f-80accdaa565c`)
