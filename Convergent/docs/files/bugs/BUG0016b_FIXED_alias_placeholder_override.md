# BUG REPORT — BUG-0016b — alias placeholder override
# Version number: v0.1

---

## Metadata
- **ID:** BUG-0016b
- **Status:** FIXED
- **Severity:** P1
- **Area:** Skills | emit_result
- **Reported by:** Jacob (during Sprint 12 live testing)
- **Date:** 2026-03-21
- **Fixed:** 2026-03-21
- **Related backlog item(s):** AF-0109 (emit_result strict content validation)
- **Related ADR(s):** —
- **Related PR(s):** Sprint 12 branch

---

## Summary
When `emit_result` receives both a canonical field (e.g. `content`) with a `previous_step.*` placeholder value and an alias field (e.g. `report`) with real data, the alias value fails to override the placeholder. The validator accepts the placeholder string as valid content, producing empty or template-filled output files.

---

## Expected behavior
Alias fields (`report`, `key_findings`, `sources_used`) should override their canonical counterparts (`content`, etc.) when present. Placeholder strings like `previous_step.synthesize_research.report` should never survive as final content.

---

## Actual behavior
- The canonical field `content` retained the raw placeholder string `previous_step.synthesize_research.report`
- The alias field `report` (containing actual research output) was ignored
- `emit_result` wrote the placeholder string to the output file

---

## Reproduction steps
1. Generate a plan with `synthesize_research` → `emit_result` steps where `emit_result.content` is set to `previous_step.synthesize_research.report`
2. If placeholder resolution partially fails, the alias `report` field carries the real data but `content` keeps the placeholder
3. Run the plan — output file contains the placeholder string instead of research content

---

## Evidence
- **Commits:** `7af500d`, `517aba1`
- **Environment:** Windows, Python 3.14.0, Sprint 12 branch
- **Contract test:** `test_emit_result_alias_override` added

---

## Impact
- **Severity:** P1 — Multi-step plans produce garbage output when alias fields aren't prioritized
- **Users affected:** Any plan using `synthesize_research` → `emit_result` chaining

---

## Fix applied
Updated `emit_result` validator in `emit_result.py` to check alias fields first and override canonical fields when aliases contain real (non-placeholder) data. Added placeholder pattern detection to content validation.
