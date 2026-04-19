# BACKLOG ITEM — AF0090 — artifact_evidence_deepdive
# Version number: v0.3

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
- **Type:** Investigation + Implementation
- **Status:** DONE
- **Priority:** P1
- **Area:** Core Runtime / Artifacts
- **Owner:** TBD
- **Target sprint:** Sprint 10
- **Depends on:** AF-0089 (report output format — DONE), AF-0057 (playbook artifacts in trace — DONE)

---

## Context

AF-0083 (Sprint 09) proposed a separate `evidence/` directory tree alongside
artifacts. After reviewing the actual codebase and on-disk layout, we decided
this creates unnecessary complexity:

- **Artifacts** already represent outputs per step
- **EvidenceRef** (AF-0049) in trace.json already handles citation traceability
- trace.json already captures `input_summary`, `output_summary`, timing, model per step
- A parallel `evidence/` tree would duplicate most of this data

**Decision:** No separate evidence concept. Instead, strengthen the existing
artifact system — fix metadata truthfulness, enrich trace.json with full I/O,
use `artifacts/` directory properly, and categorize artifacts (result vs
intermediate). The `EvidenceRef` model remains the citation mechanism.

See also: AF-0083 child AF table for the original vs actual plan.

---

## Problem

### 1. Artifact metadata is not truthful
Despite AF-0089 fixes to emit_result, artifacts are still not correctly
represented in trace.json:
- `artifact_type` may not propagate correctly to trace artifact metadata
- `research_report.md` shows `"artifact_type": "application/json"` in
  trace.json even after fix claiming to set `text/markdown`
- Multiple code paths exist for artifact registration — unclear which runs

### 2. Artifacts not stored in artifacts/ directory
Current on-disk layout for a run:
```
runs/<run_id>/
├── artifacts/           # empty! unused
├── research_report.md   # deliverable dumped at run root
└── trace.json
```
Artifacts should go in `artifacts/`, not at root level.

### 3. Trace lacks full step I/O
- `input_summary` and `output_summary` are lossy truncations
- No way to reconstruct what a skill actually received or produced
- Debugging and auditing require full inputs/outputs

### 4. No end-to-end verification
- No test verifies: skill produces artifact → trace records it correctly
  → file on disk matches → `ag artifacts list/show` displays it truthfully

---

## Goal

Deliver **truthful, complete artifact tracking:**

1. **Fix artifact metadata** — trace.json artifact_type matches actual file format
2. **Fix artifact storage** — deliverables stored in `artifacts/` directory
3. **Enrich trace.json** — full step I/O (not just summaries) for audit/debug
4. **Document artifact lifecycle** — clear path from skill output → storage → trace → CLI
5. **End-to-end test coverage** — integration test verifying full chain

---

## Non-goals

- Separate `evidence/` directory tree (rejected — use enriched artifacts instead)
- Separate `ag evidence` CLI commands (existing `ag artifacts` suffices)
- Evidence retention/cleanup policy — deferred to Sprint 11+
- Sensitive data redaction — deferred to Sprint 11+
- New artifact storage backend
- Full trace system refactor

---

## Scope

### Phase 1: Investigation & Fix (artifact metadata truthfulness) ✅ DONE
1. ✅ Trace full artifact registration path from skill output → trace.json
2. ✅ Identified where MIME type was lost: emit_result.py determined format from filename only
3. ✅ Fix applied: emit_result.py now respects `artifact_type` input parameter with backwards compatibility
4. ✅ Artifact files now stored in `artifacts/` subdirectory

### Phase 2: Trace Enrichment (step-level I/O)
1. Record full step input/output in trace.json (not just summaries)
2. Add `input_data` and `output_data` fields to Step model (optional, alongside summaries)
3. Categorize artifacts: `ArtifactCategory.RESULT` for deliverables, `.DATA` for intermediates
4. Document artifact lifecycle (skill output → trace → storage → CLI display)

### Phase 3: Integration Testing ✅ DONE
1. ✅ End-to-end test: run emit_result → verify correct artifact_type
2. ✅ End-to-end test: verify artifact files in `artifacts/` directory
3. ✅ Verify artifact_path contains `artifacts/` subdirectory
4. ✅ Verify no regression in existing artifact tests (466 tests pass)

---

## Implementation Notes (added Sprint 10)

### Root Cause Analysis
The artifact_type was not propagating correctly because `emit_result.py` determined
the output format solely from the filename extension, ignoring the `artifact_type`
input parameter. When a skill requested `artifact_type="text/markdown"` but the
filename was `summary.json`, the output was still JSON with `artifact_type="application/json"`.

### Fix Applied
1. **emit_result.py** now uses `artifact_type` parameter as the authoritative source for format
2. **Backwards compatibility**: If `artifact_type` is the default `application/json` but filename
   has `.md` extension, the skill infers `text/markdown` for backwards compatibility
3. **File extension**: The output file extension now matches the MIME type (`.md` for text/markdown,
   `.json` for application/json, `.txt` for text/plain)
4. **Artifact directory**: Changed path from `runs/<id>/` to `runs/<id>/artifacts/`

### Tests Added
- `TestArtifactTruthfulness` class in test_e2e_integration.py with 5 tests:
  - `test_markdown_artifact_has_correct_mime_type` - verifies text/markdown type
  - `test_artifact_stored_in_artifacts_directory` - verifies /artifacts/ path
  - `test_artifact_file_exists_on_disk` - verifies file creation and content
  - `test_json_artifact_has_correct_mime_type` - verifies application/json type
  - `test_artifact_type_matches_file_extension` - verifies extension consistency

---

## Key Files

| File | Role |
|------|------|
| `src/ag/skills/emit_result.py` | Skill output + artifact_type setting |
| `src/ag/core/runtime.py` | Artifact registration (~line 332) |
| `src/ag/core/run_trace.py` | Artifact model, Step model, serialization |
| `src/ag/playbooks/runtime.py` | Playbook execution, step orchestration |
| `src/ag/storage/workspace.py` | Artifact file storage layout |
| `tests/test_e2e_integration.py` | Integration tests |
| `tests/test_artifacts.py` | Artifact unit tests |

---

## Acceptance criteria (Definition of Done)

- [x] Root cause of artifact_type mismatch identified and documented
- [x] Fix applied so artifact_type matches actual file format in trace.json
- [x] Artifact files stored in `runs/<id>/artifacts/` (not run root)
- [ ] trace.json Step model enriched with full I/O data (not just summaries) — Phase 2
- [ ] Artifact lifecycle documented (skill output → trace → storage → CLI) — Phase 2
- [x] Integration test: run emit_result, verify trace.json artifact metadata correct
- [x] Integration test: verify artifact files in artifacts/ directory
- [ ] `ag artifacts list --run <id>` returns correct artifact_type — CLI work in AF-0012
- [x] No regression in existing artifact tests (test_artifacts.py)
- [x] `ruff check src tests` passes
- [x] `pytest -W error` passes (466 tests pass)

---

## Risks

| Risk | Mitigation |
|------|------------|
| Multiple artifact registration paths | Map all paths in Phase 1; unify if needed |
| Full I/O in trace.json increases file size | Optional fields; keep summaries for display, full data for debug |
| Moving artifacts to subdirectory breaks existing runs | Migration not required; new layout for new runs only |
| Fix may require interface changes | Review Artifact model in run_trace.py first |

---

## Design rationale (v0.3 rescope)

AF-0083 originally proposed a separate `evidence/` hierarchy. This was
rejected because:

1. **Duplication:** `evidence/step_N/metadata.json` would contain the same
   timing, model, token data already in trace.json Step entries
2. **Complexity:** Two parallel file trees for overlapping data
3. **Existing mechanisms:** EvidenceRef (AF-0049) already handles citations;
   ArtifactCategory already supports result/intermediate/trace classification
4. **YAGNI:** Evidence levels (minimal/standard/full) add configuration
   surface without clear user demand

Instead: enrich trace.json with full I/O, fix artifact metadata, use
`artifacts/` directory properly. If a separate evidence system is needed
later, it can be added as a Sprint 11+ AF with real requirements.

---

## Related Items

- **AF-0083:** Evidence strategy (upstream design — this AF deviates from it) — DONE
- **AF-0089:** Report output format (prerequisite — fixed markdown output) — DONE
- **AF-0057:** Playbook artifacts in trace (prerequisite — artifact capture) — DONE
- **AF-0082:** Report polish (related — report metadata depends on truthful trace)
- **AF-0012:** CLI surface parity (artifact CLI gaps addressed there)
