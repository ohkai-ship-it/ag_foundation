# CLI Change Playbook (P1/P2) — ag_foundation
# Version number: v0.1

Use this playbook when changing CLI commands, flags, defaults, or output formatting.

## 1) Define the CLI contract change
- What command/flag/output changes?
- What is the user impact?
- Is this a breaking change?

## 2) Ensure trace-first truthfulness
- If adding a label, specify the exact RunTrace field(s) that back it.
- Do not introduce “truthy” output that is not trace-derived.

## 3) Update docs
- `/docs/dev/cornerstone/CLI_REFERENCE.md` (mandatory)
- If it affects execution semantics: `/docs/dev/cornerstone/ARCHITECTURE.md`

## 4) Implement safely
- Prefer additive changes (new flags) over breaking changes.
- If breaking:
  - keep backward compat alias for one sprint (if feasible)
  - provide clear error message with replacement usage

## 5) Tests + evidence
- Unit tests for parsing/flag logic (if non-trivial)
- Integration test for `ag run` / `ag runs show --json`
- Capture run trace ID demonstrating:
  - correct mode/playbook selection
  - correct label derivation from trace

## 6) Done criteria
- CLI reference updated
- Tests/evidence included
- Truthful UX preserved
