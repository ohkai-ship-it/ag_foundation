# BUG REPORT — BUG-0023 — V2 pipeline evidence hidden
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
- **ID:** BUG-0023
- **Status:** FIXED
- **Severity:** P2
- **Area:** Core Runtime / Executor / Verifier / CLI
- **Reported by:** Kai
- **Date:** 2026-03-22
- **Related backlog item(s):** AF-0122 (CLI planning and pipeline display), AF-0124 (V2Executor), AF-0123 (V2Verifier)
- **Related ADR(s):** —
- **Related PR(s):** —

---

## Summary

V2Executor and V2Verifier both produce structured evidence about their LLM-powered
operations — repair attempts and semantic quality scores respectively — but this
evidence is invisible in the human-readable CLI output. Worse, V2Executor repair
failures are emitted as raw `logging.warning()` calls that bleed directly to the
terminal as unformatted lines, disconnected from the clean `Run completed` summary
block. Users see alarming messages like "LLM-repaired output still invalid for
'load_documents'" followed immediately by "Status: success", with no explanation of
how these two things relate. V2Verifier's semantic relevance, completeness, and
consistency scores exist only in the trace JSON and are never surfaced at all.

---

## Expected behavior

**V2Executor repair failures:**
- Repair attempt outcomes (succeeded/failed, fields changed, tokens used) should appear
  in the `Run completed` summary block — either as a per-step annotation or a
  "Step warnings" section — not as raw console output
- The raw `logging.warning()` call must be suppressed or replaced with structured
  output routed through the CLI's Rich console
- If a step's optional repair failed, the summary should make clear: "Step X failed
  (optional — execution continued)"

**V2Verifier semantic evidence:**
- `ag run` post-execution summary should show semantic verification outcome for key
  steps: relevance, completeness, and consistency scores alongside the "Verifier: passed"
  line
- `ag runs show` should display a "Semantic verification" section per step when
  semantic evidence is present in the trace
- If V2Verifier degraded to V1-only (semantic: null), that should also be visible

---

## Actual behavior

**V2Executor repair failure (raw console bleed):**

```
LLM-repaired output still invalid for 'load_documents': ['Field required', 'Field required',
'Extra inputs are not permitted', 'Extra inputs are not permitted', 'Extra inputs are not permitted']

Run completed
  Status: success
  Verifier: passed
```

The raw warning line appears before the summary block with no formatting, no step
context, no explanation that this was an optional step, and no reconciliation with
the "Status: success" that follows.

**V2Verifier semantic evidence (completely absent):**

```
Run completed
  Status: success
  Verifier: passed
```

No semantic scores visible. User must run `ag runs show <id> --json` and manually
navigate the JSON to find relevance/completeness/consistency scores.

---

## Reproduction steps

**BUG-0023a (executor raw console bleed):**
1. Run any task that causes V2Executor to attempt LLM repair on a step:
   `ag run "Download and read my email"`
2. Approve the plan
3. Observe: raw `LLM-repaired output still invalid for 'X'` line appears directly in
   the terminal output, unformatted, before the `Run completed` block

**BUG-0023b (verifier semantic evidence hidden):**
1. Run any task that completes with `Status: success`
2. Observe: `Verifier: passed` line with no semantic scores
3. Compare with `ag runs show <run_id> --json` and check `verifier.evidence.semantic`
   — it contains rich data not visible in the human output

---

## Evidence

- **RunTrace IDs:**
  - `b0f76c50-60ff-4474-8d73-8466b98a0083` (executor repair failure visible)
  - `9bfab745-0152-4178-8ceb-af28e0c20d1c` (verifier semantic data hidden)
- **CLI output:** See "Actual behavior" above
- **Environment:** Windows 11, Python 3.14.0a6, Sprint 15 branch

---

## Impact

**Auditability gap.** The V2Executor and V2Verifier are the two most expensive
LLM-powered components in Sprint 15's intelligent pipeline — they consume tokens and
affect output quality — yet they are the least visible to the user. A user who sees
"LLM-repaired output still invalid" in raw console output alongside "Status: success"
has no way to understand what happened or whether to trust the result.

This is not a truthful UX violation (the status and verifier fields are correct) but
it is an observability failure: the system is doing intelligent work that users cannot
audit through normal CLI usage.

---

## Root cause

**BUG-0023a (executor):**
`V2Executor` in `src/ag/core/executor.py` uses `logging.warning()` to emit repair
failure messages. Python's logging system is not integrated with the CLI's Rich
console, so the message appears as raw text uncontrolled by the output formatting
layer. The structured `repair_result` dict is captured correctly in the trace but
the CLI never reads it from there for display.

**BUG-0023b (verifier):**
AF-0122 (CLI planning and pipeline display) added Planning and Pipeline sections to
the CLI output, but was scoped to `planning` and `pipeline` trace fields only. The
`verifier.evidence.semantic` field — added by AF-0123 (V2Verifier) — was not in
scope for AF-0122 and was never wired into the human-readable display. The data
exists in the trace; only the display is missing.

---

## Proposed fix

**BUG-0023a — Suppress raw log; surface repair outcome via trace:**
1. Remove or downgrade the `logging.warning()` call in `V2Executor` to `logging.debug()`
   so it does not surface in normal operation
2. In `src/ag/cli/main.py`, after execution, read `repair_result` evidence from step
   data in the trace and emit a structured "Step warnings" panel in the `Run completed`
   summary for any step where `repair_attempted=True`

**BUG-0023b — Surface semantic evidence in CLI:**
1. In `src/ag/cli/main.py` `_display_run_summary()`, check `trace.verifier.evidence`
   for a `semantic` field and display relevance/completeness/consistency scores
2. In `ag runs show` human output, add a "Semantic verification" section alongside
   the existing "Verifier" section when semantic evidence is present
3. If `semantic` is null (V2Verifier degraded to V1), show "Semantic checks: skipped
   (provider unavailable)" rather than silently omitting the section

---

## Acceptance criteria

- [ ] `logging.warning()` in V2Executor no longer appears as raw console output during
  normal runs
- [ ] `ag run` summary shows repair outcome for any step where repair was attempted
  (success or failure, with step name)
- [ ] `ag run` summary shows semantic verification scores (or "skipped") after
  "Verifier: passed/failed"
- [ ] `ag runs show` displays "Semantic verification" section with per-score breakdown
- [ ] Old traces without semantic evidence render gracefully (section omitted)
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes

---

## Notes

This bug covers two related auditability gaps introduced simultaneously when V2Executor
(AF-0124) and V2Verifier (AF-0123) were added. They share a fix location (CLI output
formatting in `main.py`) and should be addressed in the same commit.

The fix for BUG-0023a is partially overlapping with AF-0122 scope (CLI planning and
pipeline display). Consider extending AF-0122 to include this fix, or treating it as
a follow-on patch commit on the Sprint 15 branch.

---

## Status log
- 2026-03-22 — Opened by Kai (reproduced with runs `b0f76c50`, `9bfab745`)
