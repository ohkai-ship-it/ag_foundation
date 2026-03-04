# Completion Note — AF-000x — <short title>
# Version number: v0.1

> Strict template. Fill every section. If something is not applicable, write **N/A** (do not delete sections).

## 1) Metadata
- **Backlog item (primary):** AF-000x
- **PR:** #<number>
- **Author:** <name>
- **Date:** YYYY-MM-DD
- **Branch:** <feat/... | fix/... | chore/...>
- **Risk level:** P0 | P1 | P2
- **Runtime mode used for verification:** llm | manual (dev/test-only)

## 2) Goal and acceptance criteria
### Goal (from backlog item)
<copy/paste the goal>

### Acceptance criteria (from backlog item)
- [ ] <AC1>
- [ ] <AC2>
- [ ] <AC3>

## 3) What changed (file-level)
List each file changed and what changed in 1 line.

- `path/to/file.py` — ...
- `path/to/file.md` — ...

## 4) Architecture alignment (mandatory)
- **Layering:** where the logic lives and why (adapter vs core vs skill)
- **Interfaces touched:** TaskSpec / RunTrace / Planner / Orchestrator / Executor / Verifier / Recorder / Skill (specify)
- **Backward compatibility:** any contract/schema change? (yes/no + details)

## 5) Truthful UX check (mandatory)
- **User-visible labels affected:** <list>
- **Trace fields backing them:** <exact fields>
- **Proof:** point to `ag runs show <run_id>` fields that demonstrate truthfulness

## 6) Tests executed (mandatory)
Provide exact commands and results summary.

- Command: `pytest ...`
  - Result: PASS/FAIL (include failing test names if any)

## 7) Run evidence (mandatory for behavior changes)
- **RunTrace ID(s):** `run_...`
- **How to reproduce the run:** exact command(s)
  - `ag run ...`
- **Expected trace outcomes:** bullet list of fields/values a reviewer should see

## 8) Artifacts (if applicable)
- **Artifact IDs/URIs:** `artifact://...`
- **What they contain:** ...

## 9) Risks, tradeoffs, and follow-ups
- **Risks introduced:** ...
- **Tradeoffs made:** ...
- **Follow-up backlog items or bugs to create:** AF-____ / BUG-____

## 10) Reviewer checklist (copy/paste)
- [ ] I can map PR → AF item and see acceptance criteria satisfied
- [ ] I can verify truthful labels from RunTrace
- [ ] I can reproduce a run (or it’s docs-only)
- [ ] Tests were run and results are documented
- [ ] Any contract changes are documented in cornerstone docs
