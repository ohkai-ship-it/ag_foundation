# AF-0118 — V1 Recorder: verification evidence persistence
# Version number: v0.2
# Created: 2026-03-21
# Status: DONE
# Priority: P2
# Area: Core Runtime / Recorder / Storage

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

---

## Summary

Upgrade V0Recorder to persist verification evidence alongside run traces and artifacts. V0Recorder stores traces and artifacts but ignores verification results beyond the top-level `Verifier.status`. V1Recorder makes per-step verification history, schema validation results, and retry evidence inspectable via `ag runs show`.

---

## Problem

V0Recorder (`runtime.py:253`) persists `RunTrace` to SQLite and artifacts to filesystem. However:

1. **Verification evidence is empty.** The `Verifier.evidence` dict in RunTrace is always `{}`. Even after V1Verifier (AF-0115) populates it, this data is stored but never surfaced in a structured way.
2. **VERIFICATION steps are opaque.** After AF-0117, traces will contain `VERIFICATION` steps, but `ag runs show` doesn't format them distinctly from `SKILL_CALL` steps.
3. **No retry history.** When V1Executor (AF-0116) retries a skill, each attempt is recorded but there's no structured summary ("attempt 1: failed schema validation, attempt 2: passed").
4. **No verification artifact.** For complex runs, a separate verification report artifact would be useful for auditing.

---

## Goal

- Verification evidence persisted in structured form (queryable, displayable)
- `ag runs show` displays verification results distinctly
- Retry history visible per step
- Optional: verification summary artifact for complex runs

---

## Non-goals

- LLM-generated verification summaries (future)
- New database schema (SQLite) — work within existing RunTrace JSON
- New CLI commands — enhance existing `ag runs show` output

---

## Design

### Structured verification evidence in RunTrace

V1Recorder ensures the `Verifier.evidence` dict uses a consistent schema:

```python
verifier = Verifier(
    status=verify_status,
    checked_at=now,
    message=verify_message,
    evidence={
        "version": "v1",
        "total_steps": 10,
        "skill_steps": 5,
        "verification_steps": 5,
        "required_passed": 4,
        "required_failed": 0,
        "optional_passed": 0,
        "optional_skipped": 1,
        "retries": {
            "step_2": {"attempts": 2, "reason": "output schema mismatch"},
        },
        "per_step": [
            {"step": 0, "skill": "load_documents", "required": False, "verified": "skipped", "reason": "No files found"},
            {"step": 2, "skill": "web_search", "required": False, "verified": "passed"},
            # ...
        ]
    }
)
```

### Enhanced `ag runs show` output

```
Verifier: passed ✓ (4/4 required ok, 1 optional skipped)
  Step 0: load_documents (optional) — skipped: No files found
  Step 1: web_search — passed
  Step 2: fetch_web_content — passed (2 attempts)
  Step 3: synthesize_research — passed
  Step 4: emit_result — passed
```

### Files touched

| File | Change |
|------|--------|
| `src/ag/core/recorder.py` | V1Recorder with structured evidence assembly (assumes AF-0114 done) |
| `src/ag/cli/main.py` | `ag runs show` formats VERIFICATION steps and evidence summary |
| `tests/test_runtime.py` | Tests: evidence dict populated, retry history captured |

---

## Acceptance criteria

- [ ] `Verifier.evidence` populated with structured per-step verification data
- [ ] `ag runs show` displays per-step verification results (passed/failed/skipped)
- [ ] Retry attempts visible per step (e.g. "2 attempts")
- [ ] Optional step skips clearly labeled in output
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Evidence dict size for large runs | JSON bloat in SQLite | Cap per_step detail to last N steps or summarize |
| CLI formatting complexity | Verbose output | Default to summary; `--verbose` for per-step detail |

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF-0118
- **PR:** #<number>
- **Author:** <name>
- **Date:** YYYY-MM-DD
- **Branch:** feat/v1-recorder
- **Risk level:** P2
- **Runtime mode used for verification:** llm + manual

## 2–10) (fill when done per template)
