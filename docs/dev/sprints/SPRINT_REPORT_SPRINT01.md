# Sprint Report — Sprint 01: Core runtime skeleton v0
# Version number: v0.1

## Metadata
- **Sprint:** Sprint 01 — Core runtime skeleton v0
- **Dates:** 2026-03-02 → 2026-03-15 (completed early: 2026-02-24)

## Outcome summary
- Shipped complete end-to-end runtime: `ag run "<prompt>"` produces a persisted `RunTrace`
- Workspace isolation with SQLite + filesystem storage fully implemented
- CLI with truthful labels derived from actual trace data
- Artifact registry automatically generates `result.md` for every run
- 103 tests passing across all modules

## Completed work
- ✅ AF-0004 — Sprint OS hygiene: sprint log + docs/dev pointers + handoff rules
- ✅ AF-0010 — Python project bootstrap (packaging + CLI stub + pytest)
- ✅ AF-0005 — Contracts: TaskSpec + RunTrace + Playbook schemas v0.1 (feat/contracts)
- ✅ AF-0006 — Workspace + storage baseline (sqlite + filesystem) (feat/storage-baseline)
- ✅ AF-0007 — Core runtime skeleton v0 (interfaces + playbook + stub skills) (feat/runtime-skeleton)
- ✅ AF-0008 — CLI v0: ag run + runs show --json, truthful labels, manual gate (feat/cli-v0)
- ✅ AF-0009 — Artifact registry v0 + ag artifacts list (feat/artifacts-v0)

## Not completed / carried over
- None — all Sprint 01 items completed

## Evidence
- Handoff notes:
  - [2026-02-24_AF-0006_storage-baseline.md](../handoff/2026-02-24_AF-0006_storage-baseline.md)
  - [2026-02-24_AF-0007_runtime-skeleton.md](../handoff/2026-02-24_AF-0007_runtime-skeleton.md)
  - [2026-02-24_AF-0008_cli-v0-truthful.md](../handoff/2026-02-24_AF-0008_cli-v0-truthful.md)
  - [2026-02-24_AF-0009_artifacts-v0.md](../handoff/2026-02-24_AF-0009_artifacts-v0.md)
- Branches pushed:
  - feat/contracts
  - feat/storage-baseline
  - feat/runtime-skeleton
  - feat/cli-v0
  - feat/artifacts-v0

## Metrics
- PR count: 5 feature branches
- Test count: 103 tests (all passing)
  - test_sanity.py: 6 tests
  - test_cli.py: 13 tests
  - test_cli_truthful.py: 14 tests
  - test_contracts.py: 21 tests
  - test_runtime.py: 19 tests
  - test_storage.py: 19 tests
  - test_artifacts.py: 11 tests

## Learnings
- **What worked:**
  - Explicit isolation tests caught workspace boundary issues early
  - Truthful UX design (labels from trace) prevented display/data mismatch bugs
  - Protocol-based interfaces (`typing.Protocol`) enabled clean dependency injection for tests
  - Building incrementally (storage → runtime → CLI → artifacts) reduced integration surprises

- **What to improve next sprint:**
  - Consider adding type checking (mypy) to CI
  - Banner/JSON output conflict showed need for earlier integration testing
  - Windows path handling in tests needed workarounds

## Next sprint candidate slice
- P0: LLM provider integration (OpenAI/Anthropic adapter)
- P0: Real skill execution (beyond echo_tool stubs)
- P1: Playbook YAML/JSON loading (move beyond hardcoded default_v0)
- P1: Verifier improvements (actual code verification)
