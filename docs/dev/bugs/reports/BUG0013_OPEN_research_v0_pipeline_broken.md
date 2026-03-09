# BUG-0013 — research_v0 playbook pipeline fails to pass documents between steps
# Version number: v0.1

## Metadata
- **ID:** BUG-0013
- **Status:** OPEN
- **Severity:** P1
- **Area:** Playbooks / Runtime
- **Reported by:** Kai
- **Date:** 2026-03-09
- **Related backlog item(s):** AF-0074
- **Related PR(s):** —

## Summary
The `research_v0` playbook fails when run end-to-end. Despite multiple fixes (URL file reading, document format conversion), the pipeline does not successfully pass fetched documents from `fetch_web_content` to `synthesize_research`. This is a fundamental issue with playbook data flow.

## Expected behavior
```bash
ag run --playbook research_v0 --workspace skills01 "Research the Düsseldorf meteorite"
```
Should:
1. Read URLs from `workspaces/skills01/inputs/urls.txt`
2. Fetch content from those URLs (fetch_web_content skill)
3. Pass fetched documents to synthesize_research skill
4. Produce a research synthesis output

## Actual behavior
The playbook fails. Either:
- "No documents provided for synthesis" error, or
- Documents are not passed correctly between pipeline steps

## Reproduction steps
1. Create `workspaces/skills01/inputs/urls.txt` with valid URLs
2. Run: `ag run --playbook research_v0 --workspace skills01 "Research topic"`
3. Observe: Pipeline fails to synthesize

## Root cause analysis (investigation needed)

### Hypothesis 1: Runtime merge logic
The runtime merges `previous_result` into next skill's parameters via spread:
```python
# In runtime.py
parameters = {**previous_result, **step_parameters}
```
But `fetch_web_content` outputs:
```python
{
    "documents": [...],  # FetchedDocument objects
    "failed_urls": [...],
    "total_fetched": int,
    "summary": str
}
```
The `documents` key must survive the merge and be recognized by `SynthesizeResearchInput`.

### Hypothesis 2: Pydantic serialization
FetchedDocument objects may not serialize correctly when passed through the pipeline. They may become dicts with unexpected structure.

### Hypothesis 3: Output format
The skill `execute()` returns `SkillResult` but the runtime extracts... what exactly? `result.output`? `result.artifacts`? The data flow is unclear.

## Evidence
- fetch_web_content.py: Outputs `FetchedDocument` list under "documents" key
- synthesize_research.py: Expects `SourceDocument` list under "documents" key
- Document conversion added (commit 8d1ff61) but still fails
- URL file reading added (commit 2bebc78) but still fails

## Files involved
- `src/ag/playbooks/runtime.py` — pipeline execution logic
- `src/ag/skills/fetch_web_content.py` — step 1 skill
- `src/ag/skills/synthesize_research.py` — step 2 skill
- `src/ag/playbooks/playbooks.py` — research_v0 definition

## Impact
- **Blocker**: The flagship playbook demonstrating multi-step skill pipelines does not work
- **Sprint 8**: Cannot demonstrate skills_playbooks_maturity milestone
- **Credibility**: Core feature (playbook data flow) is broken

## Proposed fix
1. Add debug logging to runtime.py showing exact data passed between steps
2. Trace what `SkillResult.output` contains after fetch_web_content
3. Verify Pydantic model serialization/deserialization in pipeline
4. Consider explicit `output_mapping` in playbook step definitions

## Notes
This bug is fundamental — if multi-step playbooks can't pass data between skills, the entire playbook architecture is non-functional.
