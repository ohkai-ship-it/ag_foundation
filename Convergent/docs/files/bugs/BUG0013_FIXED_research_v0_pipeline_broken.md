# BUG-0013 — research_v0 playbook pipeline cannot run autonomously
# Version number: v0.2

## Metadata
- **ID:** BUG-0013
- **Status:** FIXED
- **Severity:** P1
- **Area:** Playbooks / Skills
- **Reported by:** Kai
- **Date:** 2026-03-09
- **Fixed date:** 2026-03-10
- **Related backlog item(s):** AF-0074, AF-0080
- **Related PR(s):** Sprint08 PR

## Summary
The `research_v0` playbook cannot run autonomously because no skill produces URLs from the user's research query. The `fetch_web_content` skill requires URLs as input, but the pipeline has no mechanism to discover relevant URLs — it relies on manual curation via `urls.txt`.

**This is an architectural gap, not a data flow bug.**

## Expected behavior
```bash
ag run --playbook research_v0 --workspace skills01 "Research the Düsseldorf meteorite"
```
Should:
1. **Convert query to search terms** (implicit or explicit)
2. **Search the web for relevant URLs** ← MISSING CAPABILITY
3. Fetch content from those URLs (fetch_web_content skill)
4. Pass fetched documents to synthesize_research skill
5. Produce a research synthesis output

## Actual behavior
The playbook requires manual URL curation:
- User must create `inputs/urls.txt` with URLs beforehand
- Without this file, `fetch_web_content` has no URLs to fetch
- Pipeline produces "No URLs provided" or empty results

## Root cause analysis

### Root Cause: Missing `web_search` Skill

The pipeline has a conceptual gap:

```
Current Pipeline:
┌──────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│  load_documents  │ ──► │  fetch_web_content  │ ──► │ synthesize_research │
│  (local files)   │     │  Input: urls=???    │     │                     │
└──────────────────┘     └─────────────────────┘     └─────────────────────┘
                                    ▲
                                    │
                         WHERE DO URLs COME FROM?
                         (Currently: manual urls.txt)
```

**The `fetch_web_content` skill is a pure HTTP capability** — it fetches content from given URLs. It does not (and should not) perform web searches. A separate `web_search` skill is needed to convert the user's query into relevant URLs.

### Previous Hypotheses (Invalidated)

The original bug report hypothesized data flow issues:
- ~~Hypothesis 1: Runtime merge logic~~ — Verified working correctly
- ~~Hypothesis 2: Pydantic serialization~~ — Conversion logic exists and works
- ~~Hypothesis 3: Output format~~ — Pipeline chaining works when data exists

**The real issue is that there's no data to pass** — `fetch_web_content` receives no URLs because no skill produces them.

## Evidence
- `fetch_web_content.py`: Expects `urls` from input or `urls_file` (manual)
- No skill in the pipeline produces URLs from the user's query
- `synthesize_research.py`: Works correctly when documents are provided
- Runtime pipeline chaining (`previous_result` merge) works as designed

## Proposed Solution: AF-0080

Add a `web_search` skill that:
1. Takes the user's research query
2. Calls a search engine API (DuckDuckGo, Serper, Google, Bing)
3. Returns a list of URLs

This creates a complete autonomous pipeline:

```
Fixed Pipeline:
┌──────────────┐     ┌─────────────────────┐     ┌─────────────────────┐     ┌───────────────┐
│  web_search  │ ──► │  fetch_web_content  │ ──► │ synthesize_research │ ──► │  emit_result  │
│  query→urls  │     │  urls→documents     │     │  documents→report   │     │  report→file  │
└──────────────┘     └─────────────────────┘     └─────────────────────┘     └───────────────┘
```

**See [AF-0080](../../backlog/items/AF0080_PROPOSED_web_search_skill.md) for full specification.**

## Files involved
- `src/ag/skills/web_search.py` — **NEW** skill to implement
- `src/ag/skills/fetch_web_content.py` — No changes needed (works correctly)
- `src/ag/skills/synthesize_research.py` — No changes needed (works correctly)
- `src/ag/playbooks/research_v0.py` — Update to include `web_search` as step 0

## Impact
- **Blocker**: The flagship playbook demonstrating multi-step skill pipelines cannot run autonomously
- **Sprint 8**: Cannot demonstrate skills_playbooks_maturity milestone without manual URL curation
- **User Experience**: Requires manual setup that defeats the purpose of an autonomous research agent

## Resolution Path

1. ✅ Root cause identified (missing skill, not data flow bug)
2. ✅ Solution designed (AF-0080: web_search skill)
3. ⬜ Implement `web_search` skill with DuckDuckGo/Serper backends
4. ⬜ Update `research_v0` playbook with `web_search` as step 0
5. ⬜ Verify end-to-end autonomous research pipeline

## Notes
The original diagnosis focused on pipeline data flow mechanics, but the actual issue is architectural — the pipeline is missing a capability (web search). The existing skills (`fetch_web_content`, `synthesize_research`) work correctly; they just need a URL source upstream.
