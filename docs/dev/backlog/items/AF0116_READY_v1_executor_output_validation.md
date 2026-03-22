# AF-0116 — V1 Executor: output schema validation with retry
# Version number: v0.1
# Created: 2026-03-21
# Status: READY
# Priority: P1
# Area: Core Runtime / Executor / Skills

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

---

## Summary

Upgrade V0Executor to validate skill outputs against `SkillInfo.output_schema` after each execution, with bounded retry on schema mismatch. This completes the input/output validation symmetry (input validation already exists in `registry.py:136-139`) and catches malformed LLM outputs before they chain to the next step. Includes a V2 roadmap for LLM-powered output repair.

---

## Problem

### Input validation exists, output validation doesn't

```
registry.py:
  Input:  skill_info.input_schema.model_validate(params)   ✅ enforced
  Output: output = skill.execute(input, ctx)                ❌ returned unchecked
                    return output.to_legacy_tuple()
```

Every skill declares an `output_schema` (stored in `SkillInfo.output_schema`), but it's never validated at runtime. If an LLM skill returns malformed data, it chains forward silently.

### Consequences

1. **Garbage-in for next step.** A malformed `web_search` output (e.g. missing `urls` field) gets passed to `fetch_web_content`, which fails with an opaque error rather than a clear "web_search output didn't match schema."
2. **Root cause obscured.** The failure surfaces 2-3 steps later, making debugging hard.
3. **SchemaValidator exists but is orphaned.** `schema_verifier.py` has a full repair-loop engine with bounded retries and evidence recording — never called by the runtime.

---

## Goal

- Every skill output is validated against its declared `output_schema`
- Failed validation triggers bounded retry (re-invoke skill, same input)
- Each validation attempt records a `VERIFICATION` step in the trace using `StepType.VERIFICATION`
- Clear V2 extension point for LLM-powered output repair

---

## Non-goals

- LLM-powered output repair (V2 scope — see Future section)
- Semantic quality checks ("is this summary good?") — that's V2 Verifier (AF-0115 roadmap)
- Per-step verification loop in orchestrator — that's AF-0117
- Changing the Skill ABC or SkillOutput base class

---

## Design

### Integration point: V1Executor.execute()

V0Executor calls `registry.execute(skill_name, params, ctx)` and returns the result. V1Executor adds output validation between skill execution and result return.

```python
class V1Executor:
    def execute(self, skill_name, params, ctx):
        skill_info = self._registry.get_skill_info(skill_name)

        for attempt in range(1, self._max_attempts + 1):
            output = self._registry.execute_raw(skill_name, params, ctx)

            # Validate against declared output schema
            is_valid, errors, validated = self._validate_output(
                output, skill_info.output_schema
            )

            if is_valid:
                self._record_verification(attempt, skill_name, passed=True)
                return validated.to_legacy_tuple()

            # Log validation failure
            self._record_verification(attempt, skill_name, passed=False, errors=errors)

            if attempt < self._max_attempts:
                continue  # retry

        # All attempts exhausted
        return False, f"Output validation failed after {self._max_attempts} attempts", {...}
```

### Key design decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Validation engine | Pydantic `model_validate` (direct) | Simpler than wiring SchemaValidator for V1; SchemaValidator used for V2+ repair loops |
| Retry strategy | Re-invoke skill with same input | Idempotent retry; LLM calls are non-deterministic, so retry may produce valid output |
| Max attempts | 2 retries (3 total, matching `DEFAULT_MAX_VALIDATION_ATTEMPTS`) | Conservative; bounded by existing constant |
| Where to validate | In Executor, before returning | Keeps validation coupled to execution; orchestrator doesn't need to know |
| Trace recording | `StepType.VERIFICATION` step per attempt | Uses existing enum value that's currently unused |

### Registry change

Add `execute_raw()` to `SkillRegistry` — returns `SkillOutput` object directly instead of `to_legacy_tuple()`. This preserves the typed output for validation. Existing `execute()` remains for backward compatibility.

Add `get_skill_info(name)` public method if not already exposed.

### Files touched

| File | Change |
|------|--------|
| `src/ag/core/executor.py` | **New** V1Executor with output validation (assumes AF-0114 done) |
| `src/ag/skills/registry.py` | Add `execute_raw()` returning SkillOutput; add `get_skill_info()` |
| `tests/test_runtime.py` | V1Executor tests: valid output passes, invalid triggers retry, exhausted retries fail |
| `tests/test_skill_framework.py` | Test `execute_raw()` returns typed SkillOutput |

---

## V2 roadmap: LLM-powered output repair

V1 retries blindly (re-invoke skill, hope for better output). V2 adds **intelligent repair**:

| V2 Capability | How it works | Benefit |
|---|---|---|
| **LLM repair prompt** | On schema validation failure, send the malformed output + schema + error messages to LLM with "fix this JSON to match the schema" | Cheaper than full skill re-invocation (no tool calls, just JSON fixing). Handles common LLM mistakes: missing field, wrong type, extra comma. |
| **Targeted field repair** | Only the failing fields are repaired, rest preserved | Minimal change to otherwise-correct output |
| **Repair evidence in trace** | Original output + repair prompt + repaired output all recorded | Full auditability for what the LLM changed |

**V2 design principle:** LLM repair is a **fallback between retry and failure**. Flow: `validate → fail → retry skill → fail → LLM repair → fail → give up`. The LLM call is bounded by token budget.

**V2 integration point:** `V2Executor` extends V1Executor's loop with an LLM repair step between the last retry and final failure. The `SchemaValidator.validate_with_repair()` method already supports a `repair_fn` callback — V2 provides an LLM-backed `repair_fn`.

---

## Acceptance criteria

- [ ] Skill output validated against `SkillInfo.output_schema` after each execution
- [ ] Valid output: passes through unchanged
- [ ] Invalid output: skill re-invoked (up to 2 retries)
- [ ] Exhausted retries: step marked failed with validation error details
- [ ] `VERIFICATION` steps recorded in trace for each validation attempt
- [ ] `execute_raw()` added to SkillRegistry, returning typed SkillOutput
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes
- [ ] Tests: valid output passes, invalid triggers retry, retries exhausted, verification steps in trace

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Existing skill outputs don't match declared schemas | All runs fail | Pre-flight test: run all skills through output schema validation before merging |
| LLM skills produce different output each retry (cost) | Extra API calls | 2 retries is conservative; token budgets limit cost |
| `to_legacy_tuple()` discards type info | V1Executor needs typed output | `execute_raw()` provides this |

---

## Supersedes

This AF, combined with AF-0115 and AF-0117, supersedes **AF-0113** (per-step skill output verification). AF-0113 proposed a monolithic wiring approach; these three AFs decompose it into focused, individually testable components.

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF-0116
- **PR:** #<number>
- **Author:** <name>
- **Date:** YYYY-MM-DD
- **Branch:** feat/v1-executor
- **Risk level:** P1
- **Runtime mode used for verification:** llm + manual

## 2–10) (fill when done per template)
