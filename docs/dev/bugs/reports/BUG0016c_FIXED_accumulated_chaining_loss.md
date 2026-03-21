# BUG REPORT — BUG-0016c — accumulated chaining loss
# Version number: v0.1

---

## Metadata
- **ID:** BUG-0016c
- **Status:** FIXED
- **Severity:** P1
- **Area:** Core Runtime | Orchestrator
- **Reported by:** Kai (during Sprint 12 live testing)
- **Date:** 2026-03-21
- **Fixed:** 2026-03-21
- **Related backlog item(s):** AF-0109 (emit_result strict content validation)
- **Related ADR(s):** —
- **Related PR(s):** Sprint 12 branch

---

## Summary
When a plan has two consecutive `emit_result` steps (e.g. MD output + JSON output), the second `emit_result` only sees the first `emit_result`'s artifact metadata (`artifact_id`, `bytes_written`) instead of the original `synthesize_research` output (`report`, `key_findings`, `sources_used`). Earlier step data is lost because the runtime replaces `previous_result` after each step instead of accumulating results.

---

## Expected behavior
All step outputs should accumulate so that later steps can access data from any earlier step. A second `emit_result` should still have access to the `synthesize_research` fields (`report`, `key_findings`, `sources_used`).

---

## Actual behavior
- `previous_result` was set to the output of only the immediately preceding step
- After the first `emit_result`, `previous_result` contained only `{"artifact_id": "...", "bytes_written": 1234}`
- The second `emit_result` could not access research data, producing empty/placeholder output

---

## Reproduction steps
1. Generate a plan: `ag plan generate --task "Report on X"` that produces steps: `web_search` → `fetch_web_content` → `synthesize_research` → `emit_result` (MD) → `emit_result` (JSON)
2. Execute: `ag run --plan <id>`
3. Second `emit_result` output file is empty or contains placeholder data

---

## Evidence
- **RunTrace ID:** `plan_486286485e3b` (post-fix verification)
- **Commit:** `4066240`
- **Environment:** Windows, Python 3.14.0, Sprint 12 branch
- **Contract test:** `test_accumulated_chaining` added (BUG-0016c)

---

## Impact
- **Severity:** P1 — Multi-output plans (the new autonomy milestone) are broken without this fix
- **Users affected:** Any plan with more than one `emit_result` step

---

## Fix applied
Introduced `accumulated_result` dict in `runtime.py` that merges all step outputs via `.update()`. Each step's result is merged into the accumulator so earlier data (research fields) persists through intermediate steps. `chained_result` now uses `accumulated_result` instead of just `previous_result`.
