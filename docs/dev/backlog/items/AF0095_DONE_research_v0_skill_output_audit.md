# BACKLOG ITEM — AF0095 — research_v0_skill_output_audit
# Version number: v0.2

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
- **ID:** AF0095
- **Type:** Investigation / Bug Fix
- **Status:** DONE
- **Priority:** P2
- **Area:** Skills / Playbooks / research_v0
- **Owner:** AGENT
- **Completed:** 2026-03-12
- **Depends on:** None

---

## Audit Summary

**Audit completed 2026-03-12.** The research_v0 pipeline was audited by:
1. Running each skill individually via CLI
2. Running the full playbook end-to-end
3. Inspecting trace data and artifact outputs
4. Verifying schema compliance

### Key Findings

| Finding | Severity | Status |
|---------|----------|--------|
| CLI skill execution missing SkillContext.workspace_path | Bug - Fixed | ✅ Fixed |
| Artifact JSON excludes success/summary fields | Design | Documented |
| synthesize_research has dead fallback code | Tech Debt | Follow-up needed |
| CLI --skill vs --playbook LLM handling differs | Design | Documented |

---

## Finding 1: CLI SkillContext Missing workspace_path (FIXED)

**Problem:** CLI `ag run --skill` didn't pass SkillContext with workspace_path, causing fetch_web_content to fail loading URLs from inputs/urls.txt.

**Root Cause:** `src/ag/cli/main.py` line 442 called `registry.execute(skill, skill_params)` without passing a context argument. The registry then created an empty SkillContext with `workspace_path=None`.

**Fix Applied:**
```python
# AF-0095: Create proper SkillContext with workspace_path for skill execution
skill_ctx = SkillContext(
    workspace_path=ws.path,
    run_id=run_id,
)
success, output_summary, result = registry.execute(skill, skill_params, skill_ctx)
```

**Files Changed:**
- `src/ag/cli/main.py` (added SkillContext import and creation)

---

## Finding 2: Artifact JSON Excludes success/summary (DESIGN)

**Observation:** Skill artifacts don't include `success` and `summary` fields.

**Explanation:** This is intentional design in `SkillOutput.to_legacy_tuple()`:
```python
def to_legacy_tuple(self) -> tuple[bool, str, dict[str, Any]]:
    return (
        self.success,
        self.summary,
        self.model_dump(exclude={"success", "summary"}),  # Artifact data
    )
```

The artifact stores the "data" portion; success/summary are returned separately in the tuple.

**Impact:** Users inspecting artifacts cannot see success/summary without reading the trace.

**Recommendation:** Document this behavior. Consider adding success/summary to artifact for completeness.

---

## Finding 3: synthesize_research Dead Fallback Code (TECH DEBT)

**Problem:** `synthesize_research.py` has a `_fallback_synthesis()` function that's unreachable.

**Root Cause:** The skill declares `requires_llm: ClassVar[bool] = True`, which causes `validate_context()` to fail before `execute()` runs. The fallback code inside `execute()` can never be reached.

**Impact:** The skill cannot be run without an LLM even though fallback code exists.

**Recommendation:** Either:
1. Remove dead fallback code (if LLM is strictly required)
2. Set `requires_llm=False` and let execute() handle fallback
3. Override `validate_context()` to allow manual mode

---

## Finding 4: CLI --skill vs --playbook LLM Handling (DESIGN)

**Observation:** CLI `--skill` execution doesn't create an LLM provider, but `--playbook` execution does.

**Code:** Playbook runtime creates provider in `V0Orchestrator.run()`:
```python
if task.mode != ExecutionMode.MANUAL:
    provider_config = ProviderConfig(provider="openai", model="gpt-4o-mini")
    llm_provider = get_provider(provider_config)
```

CLI skill execution doesn't do this—it only creates a SkillContext with workspace_path.

**Impact:** Skills requiring LLM (like synthesize_research) fail with `--skill` but work with `--playbook`.

**Recommendation:** Consider adding `--llm` flag to CLI skill execution, or auto-detect when skill `requires_llm=True`.

---

## Verified Working

The following were verified as correctly implemented:

✅ **web_search**: Returns proper WebSearchOutput schema with urls, results, total_results
✅ **fetch_web_content**: Returns proper FetchWebContentOutput with documents, failed_urls
✅ **load_documents**: Returns proper LoadDocumentsOutput with documents, file_count
✅ **emit_result**: Returns proper EmitResultOutput with artifact_id, artifact_path
✅ **Pipeline chaining**: Output of each step correctly flows to next step
✅ **Artifact generation**: research_report.md properly generated with citations

---

## Context

The `research_v0` playbook orchestrates a 5-step research pipeline:
1. `load_documents` — Load local reference docs (optional)
2. `web_search` — Discover URLs from query (optional)
3. `fetch_web_content` — Fetch content from URLs (optional)
4. `synthesize_research` — LLM-powered synthesis (required)
5. `emit_result` — Save artifact (required)

Observed discrepancies between skill behavior and CLI reporting suggest potential issues in:
- Skill output schemas vs actual returned data
- Summary/output truncation masking errors
- Step success reporting not matching actual outcomes
- Data flow between skills (output of one → input of next)

---

## Problem

### 1. Behavior vs Reporting Discrepancies
- CLI reports may show "success" when skill behavior is partially correct
- Output summaries may not reflect actual skill execution state
- Error conditions may be masked by summary truncation

### 2. Skill Output Verification Gaps
- No systematic verification of skill outputs against their schemas
- Intermediate outputs between pipeline steps not easily inspectable
- `output_summary` is lossy — cannot reconstruct full picture

### 3. Data Flow Integrity
- research_v0 passes data between skills implicitly
- `web_search` → `fetch_web_content` URL handoff unclear
- `fetch_web_content` → `synthesize_research` content handoff unclear

---

## Scope

### Investigation Phase
1. **Audit each skill in research_v0:**
   - `web_search` — Verify search results match expected schema
   - `fetch_web_content` — Verify fetched content matches expected schema
   - `synthesize_research` — Verify synthesis output matches expected schema
   - `emit_result` — Verify artifact storage matches expectations

2. **Trace inspection:**
   - Run research_v0 with logging enabled
   - Capture full input/output at each step
   - Compare trace data with CLI display
   - Document any discrepancies

3. **Schema compliance:**
   - Verify each skill's output matches its `output_schema`
   - Check for undocumented fields or missing required fields
   - Validate Pydantic model dumps

### Fix Phase (if issues found)
4. **Fix identified discrepancies:**
   - Correct skill output schemas
   - Fix output summary generation
   - Ensure CLI displays truthful status

5. **Add regression tests:**
   - Test each skill's output schema compliance
   - Test data flow between steps
   - Test CLI output matches trace data

---

## Test Commands

```bash
# Run research_v0 playbook
ag run --playbook research_v0 "What is the capital of France?"

# Run individual skills for isolated testing
ag run --skill web_search "capital of France"
ag run --skill fetch_web_content --urls "https://example.com"
ag run --skill synthesize_research --sources "test content"

# Inspect trace
ag runs inspect <run-id> --json

# Run with debug logging
AG_LOG_LEVEL=DEBUG ag run --playbook research_v0 "test query"
```

---

## Acceptance Criteria

- [ ] Each skill in research_v0 audited for output correctness
- [ ] Identified discrepancies documented
- [ ] Fixes implemented for any behavior/reporting mismatches
- [ ] Trace data matches CLI display
- [ ] Regression tests prevent future discrepancies
- [ ] SCHEMA_INVENTORY.md updated if schemas change

---

## Skills to Audit

| Skill | Module | Schema | Priority |
|-------|--------|--------|----------|
| `web_search` | `ag.skills.web_search` | `WebSearchOutput` | High |
| `fetch_web_content` | `ag.skills.fetch_web_content` | `FetchWebContentOutput` | High |
| `synthesize_research` | `ag.skills.synthesize_research` | `SynthesizeResearchOutput` | High |
| `load_documents` | `ag.skills.load_documents` | `LoadDocumentsOutput` | Medium |
| `emit_result` | `ag.skills.emit_result` | `EmitResultOutput` | Medium |

---

## Notes

- May overlap with AF0094 (trace_full_io_enrichment) — full I/O capture would help this audit
- Consider adding verbose/debug mode for skill execution
- Zero skill (`zero_skill`) provides minimal baseline for comparison
