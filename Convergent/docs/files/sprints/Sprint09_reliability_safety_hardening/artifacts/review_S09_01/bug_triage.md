# Bug Triage - Sprint09 Review

## Candidate issues discovered during review

1. P1: Lint/format gate fails in Pass 2
- Evidence: `ruff_summary.txt`
- Details: `ruff check` reports import-order and unused import errors in `tests/test_artifacts.py`; `ruff format --check` reports `src/ag/cli/main.py` would be reformatted.
- Impact: Authoritative quality gate not green.

2. P2: Runs list appears truncated to 10 rows without explicit pagination indicator
- Evidence: `cli_outputs.txt`
- Command: `ag runs list --workspace test-meta-ws`
- Impact: Reduced observability/discoverability during run-history review.

3. P1: research_v0 output appears unchanged from pre-sprint baseline
- Evidence: `cli_outputs.txt`, `happy_trace.json`, user-provided run artifacts
- Impact: Sprint value not clearly visible in user-facing output.

4. P2: Prompt encoding appears degraded in trace summaries
- Evidence: `happy_trace.json`
- Example: `Düsseldorf` represented as `D³sseldorf` in `input_summary` and `output_summary`.
- Impact: Truthful UX/readability concern.

## Follow-up placeholders
- AF____ (runs list pagination/total indicator)
- AF____ (human-readable report output path/format)
- BUG____ (encoding degradation in trace summaries)
