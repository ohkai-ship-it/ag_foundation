# BACKLOG ITEM — AF0089 — report_output_format
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
- **ID:** AF0089
- **Type:** Feature
- **Status:** DONE
- **Priority:** P1
- **Area:** Core Runtime / CLI
- **Owner:** Jacob
- **Target sprint:** Sprint09
- **Depends on:** AF-0082 (human-readable result format)

---

## Problem
`research_report.md` is emitted as JSON payload despite `.md` filename and does not provide clear user-facing report value.

---

## Goal
Make report output truthful and user-readable:
- format aligns with extension
- JSON and markdown outputs are clearly separated/named
- runtime output references correct artifact type

---

## Non-goals
- New report templating system
- Full redesign of artifact registry

---

## Acceptance criteria (Definition of Done)
- [ ] Markdown report file contains markdown (not JSON string payload)
- [ ] JSON payload (if retained) uses explicit `.json` filename
- [ ] Trace/artifact metadata MIME type matches output format
- [ ] CLI output references correct artifact path/type
- [ ] Tests verify format and naming consistency
- [ ] `ruff check src tests` passes
- [ ] `pytest -W error` passes

---

## Implementation notes
Likely touchpoints:
- `src/ag/skills/stubs.py` / emit result handling
- `src/ag/core/runtime.py` artifact recording path/type
- playbook/report related tests under `tests/`

---

## Risks
- Existing consumers may depend on current `research_report.md` JSON behavior
- Migration may require compatibility period

---

## Completion (Sprint09)

### Files changed
- `src/ag/skills/emit_result.py` — added `_format_markdown()` method, detects `.md` extension and writes proper markdown format; added `artifact_type` field to output schema with correct MIME type based on extension

### Tests added
- `tests/test_summarize_skills.py`:
  - `test_markdown_output_format` — verifies `.md` files get markdown headers/content
  - `test_json_output_for_json_extension` — verifies `.json` files still get JSON format
  - `test_artifact_type_mime_for_markdown` — verifies artifact_type is `text/markdown` for .md
  - `test_artifact_type_mime_for_json` — verifies artifact_type is `application/json` for .json

### Behavior
- Files with `.md` extension now emit markdown with `# Title`, date, content sections
- Files with `.json` or other extensions still emit JSON as before
- MIME type in artifact metadata matches actual output format (fixes trace.json artifact listing)

### Evidence
- All 461 tests pass
- `ruff check src tests` clean
- Coverage: 86%
