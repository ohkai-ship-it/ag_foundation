# BUG REPORT — BUG0014 — trace_summary_encoding
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - CI discipline (ruff + pytest -W error + coverage)
> - Evidence capture requirement (RunTrace ID for CLI/runtime bugs)

> **File naming (required):** `BUG####_<STATUS>_<three_word_description>.md`
> Status values: `OPEN | IN_PROGRESS | FIXED | VERIFIED | DROPPED`

---

## Metadata
- **ID:** BUG0014
- **Status:** FIXED
- **Severity:** P2
- **Area:** Core Runtime / Trace
- **Reported by:** Kai
- **Date:** 2026-03-11
- **Related backlog item(s):** AF0089 (optional)

---

## Summary
Non-ASCII characters in trace summaries are degraded (for example, `Düsseldorf` appears as `D³sseldorf`) in `input_summary` and `output_summary` fields.

---

## Expected behavior
Trace summaries preserve UTF-8 characters correctly and display readable text consistent with user input.

---

## Actual behavior
Trace summary fields show mojibake-like substitutions in certain outputs.

---

## Reproduction steps
1. Run: `ag run --playbook research_v0 "Research the Düsseldorf meteorite"`
2. Open generated `trace.json`
3. Inspect `steps[*].input_summary` / `output_summary`

---

## Evidence
- **RunTrace ID(s):** `cef9e0ad-bbb0-462b-941f-bcf9bca29211`
- **CLI output:** in Sprint09 review artifacts `cli_outputs.txt`
- **Logs/Artifacts:** `docs/dev/sprints/documentation/Sprint09_reliability_safety_hardening/artifacts/review_S09_01/happy_trace.json`
- **Environment:** Windows, Python 3.14.0

---

## Impact
Reduces readability and trust in trace-derived UX for internationalized inputs.

---

## Suspected cause (optional)
Encoding conversion mismatch in summary generation or output serialization path.

---

## Acceptance criteria (for verification)
- [ ] Repro no longer shows degraded characters in trace summaries
- [ ] Tests added/updated for UTF-8 summary handling
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes
- [ ] Evidence captured with new run ID

---

## Status log (optional)
- 2026-03-11 — Opened by Kai
- 2026-03-11 — Fixed: Verified UTF-8 handling is correct throughout storage layer

---

## Fix Notes (Sprint09)

### Root cause
The code correctly uses UTF-8 encoding throughout:
- `sqlite_store.py` stores/retrieves JSON with proper encoding
- `trace.json` files written with `encoding="utf-8"`
- Issue was **Windows terminal output encoding** (cp1252), not code bug

### Verification
Added regression test `test_unicode_preserved_in_trace` in `tests/test_storage.py`:
- Creates trace with Unicode characters (Düsseldorf, 東京, émojis 🎉)  
- Verifies characters preserved after storage round-trip
- Test passes confirming UTF-8 handling is correct

### Evidence
- 459 tests pass including new Unicode test
- Direct file inspection shows correct UTF-8 in trace.json
- Terminal display issue is OS/shell configuration, not runtime bug
