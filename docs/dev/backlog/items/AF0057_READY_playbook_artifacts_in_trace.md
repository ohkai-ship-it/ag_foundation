# BACKLOG ITEM — AF0057 — playbook_artifacts_in_trace

# Version number: v0.2

> **FOUNDATION GOVERNANCE** This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - 1 PR = 1 primary AF
> - INDEX update rule (status ↔ filename integrity)

> **File naming (required):**
> `AF####_<Status>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata

- **ID:** AF-0057
- **Type:** Foundation
- **Status:** READY
- **Priority:** P1
- **Area:** Core Runtime / Skill Framework
- **Owner:** TBD
- **Target sprint:** TBD

---

## Problem

Playbook execution does not capture skill-produced artifacts in the RunTrace.

**Evidence from Sprint 07 review** (`happy_trace.json`):
```json
{
  "steps": [
    { "skill_name": "load_documents", "artifacts": [] },
    { "skill_name": "summarize_docs", "artifacts": [] },
    { "skill_name": "emit_result", "artifacts": [] }
  ],
  "artifacts": []
}
```

Yet `emit_result` successfully wrote `runs/<run_id>/summary.json` to disk.

**Root cause:**
The `Runtime._execute_playbook()` method doesn't capture artifact IDs returned 
by skills. The direct `--skill` path in CLI (main.py) does this correctly, but 
playbook execution in runtime.py does not.

---

## Goal

Skills that produce artifacts (like `emit_result`) should have those artifacts:
1. Recorded in the step's `artifacts` list
2. Aggregated to the run-level `artifacts` list
3. Discoverable via `ag artifacts list --run <id>`

---

## Non-goals

- No changes to artifact storage mechanism
- No changes to skill interface (skills already return artifact info)
- No evidence_refs implementation (separate concern)

---

## Acceptance criteria (Definition of Done)

- [ ] After `ag run --playbook research_v0 ...`, trace step for `emit_result` 
      has non-empty `artifacts` list
- [ ] Run-level `artifacts` includes skill-produced artifacts
- [ ] `ag runs show <id> --json` shows artifacts correctly
- [ ] Tests added:
  - [ ] Integration test verifies artifact capture for summarize_v0
- [ ] CI passes (ruff + pytest -W error + coverage)
- [ ] Evidence: RunTrace ID showing populated artifacts

---

## Implementation notes

**Option A: Capture from skill result**
Skills like `emit_result` return `artifact_id` and `artifact_path` in their output.
Runtime can capture these:

```python
# In runtime.py after skill execution
if result and "artifact_id" in result:
    step_artifacts.append(result["artifact_id"])
    artifacts.append(result["artifact_id"])
```

**Option B: Skill returns Artifact model**
Update skill output to include full `Artifact` object, not just ID/path strings.

**Recommendation:** Option A is minimal and non-breaking.

---

## Risks

- Low: Additive change to runtime, no schema changes needed

---

## Related

- AF-0065: First skill set (created emit_result skill)
- Sprint 07 review: Identified this gap

---

# Completion section (fill when done)

## 1) Metadata

- **Backlog item (primary):** AF-0057
- **PR:** #`<number>`
- **Author:** `<name>`
- **Date:** YYYY-MM-DD
- **Branch:** feat/playbook-artifacts-trace
- **Risk level:** P1
- **Runtime mode used for verification:** llm

---

## 2) Acceptance criteria verification

- [ ] ...

---

## 3) What changed (file-level)

- `src/ag/core/runtime.py` — Capture artifact IDs from skill results
- `tests/test_runtime.py` — Add artifact capture test

---

## 4) Architecture alignment (mandatory)

- **Layering:** Core Runtime
- **Interfaces touched:** Runtime._execute_playbook()
- **Backward compatibility:** Yes (additive only)
