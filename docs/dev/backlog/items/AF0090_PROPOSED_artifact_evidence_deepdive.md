# BACKLOG ITEM — AF0090 — artifact_evidence_deepdive
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - CI discipline (ruff + pytest -W error + coverage)
> - INDEX update rule (status ↔ filename integrity)

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0090
- **Type:** Investigation / Fix
- **Status:** PROPOSED
- **Priority:** P1
- **Area:** Core Runtime / Artifacts
- **Owner:** TBD
- **Target sprint:** TBD
- **Depends on:** AF-0089 (report output format)

---

## Problem
Despite AF-0089 fixes to emit_result, artifacts are still not correctly listed in trace.json:
1. `artifact_type` may not propagate correctly to trace artifact metadata
2. Runtime artifact registration flow unclear — multiple code paths exist
3. Evidence capture requirements (per FOUNDATION_MANUAL) not consistently enforced
4. Discrepancy between what emit_result outputs and what trace.json records

Observed behavior: `research_report.md` shows `"artifact_type": "application/json"` in trace.json even after fix claiming to set `text/markdown`.

---

## Goal
Deep investigation of artifact and evidence flow:
1. Trace full artifact registration path from skill output → trace.json
2. Identify where MIME type gets lost or overwritten
3. Fix root cause so artifact metadata is truthful
4. Document artifact lifecycle for future maintainners
5. Add integration test that verifies end-to-end artifact metadata

---

## Non-goals
- New artifact storage backend
- Breaking existing artifact APIs
- Full refactor of trace system

---

## Investigation scope
1. **emit_result.py**: Verify `artifact_type` in EmitResultOutput
2. **runtime.py**: Check `_record_artifact()` and skill result handling (line ~332)
3. **run_trace.py**: Artifact model and serialization
4. **Playbook execution**: Does artifact get registered twice? Different paths?
5. **Test coverage**: Why didn't tests catch this?

---

## Acceptance criteria (Definition of Done)
- [ ] Root cause identified and documented
- [ ] Fix applied so artifact_type matches actual file format
- [ ] Integration test: run research_v0, verify trace.json has correct artifact_type
- [ ] No regression in existing artifact tests
- [ ] `ruff check src tests` passes
- [ ] `pytest -W error` passes

---

## Implementation notes
Key files to investigate:
- `src/ag/skills/emit_result.py` — skill output
- `src/ag/core/runtime.py` — artifact registration (~line 332)
- `src/ag/core/run_trace.py` — Artifact model
- `src/ag/playbooks/runtime.py` — playbook execution
- `tests/test_e2e_integration.py` — may need new test

---

## Risks
- Multiple artifact registration paths may exist
- Fix may require interface changes
