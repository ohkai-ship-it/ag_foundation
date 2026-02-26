# Testing Guidelines (ag_foundation)
# Version number: v0.2

These guidelines define what tests are required for different change types.

## 0) Coverage Thresholds & CI Policy

### Coverage Requirements
All PRs must maintain or improve the following coverage thresholds:

| Module | Minimum Coverage |
|--------|-----------------|
| Overall | ≥85% |
| CLI (`src/ag/cli/`) | ≥72% |
| Providers (`src/ag/providers/`) | ≥95% |
| Storage (`src/ag/storage/`) | ≥95% |
| Core (`src/ag/core/`) | ≥85% |

Check coverage with:
```bash
pytest --cov=src/ag --cov-report=term-missing
```

### Warnings Policy
All tests MUST pass with warnings treated as errors:
```bash
pytest -W error
```

This catches:
- ResourceWarning (unclosed files/connections)
- DeprecationWarning (deprecated APIs)
- UserWarning (potential issues)

### CI Enforcement
The CI pipeline will fail if:
1. Coverage drops below thresholds
2. Any warning is raised during tests
3. Ruff linting fails (see PR Checklist)

## 1) Test tiers
### Unit tests (required for core logic)
- Pure functions and module logic (planner heuristics, normalizer, trace builders)
- No network calls
- Fast (< 1s per test suite chunk)

### Integration tests (required when pipeline behavior changes)
- Exercise `ag run` end-to-end (prefer manual mode for speed where allowed)
- Validate that:
  - a RunTrace is created
  - trace fields match expectations
  - CLI output labels match trace facts

### Contract tests (required for interfaces/schemas)
- Validate `TaskSpec` and `RunTrace` schema stability
- Validate skill contracts (inputs/outputs/permissions metadata)

## 2) Required tests by change type

### A) Docs-only changes
- No tests required

### B) CLI adapter changes
- Unit test parsing/flag behavior (if non-trivial)
- Integration test to confirm CLI output remains trace-derived

### C) Core runtime changes (planner/orchestrator/executor/verifier/recorder)
- Unit tests for logic
- Integration test for `ag run` pipeline
- At least one captured trace (run_id) as evidence

### D) Skill/plugin changes
- Unit test for skill logic
- Integration test showing invocation recorded in trace

### E) Storage changes
- Unit tests for storage adapters
- Integration test to confirm persistence + workspace isolation

### F) Trace schema changes (P1+)
- Contract tests for new fields
- Backwards-compat note (or migration)
- Update ARCHITECTURE doc section on trace contract

## 3) What to assert in tests
- `run.status` and `verifier.status` expectations
- presence and correctness of step fields:
  - role, reasoning_mode, status, timing_ms
- correctness of “truthful label” derivation from trace facts
- workspace isolation (paths, DB, artifacts)

## 4) Prohibited in CI tests (unless explicitly allowed)
- External network calls
- Hidden LLM provider dependencies
- Non-deterministic tests without controls

## 5) Test evidence in PRs
PR description must include:
- commands run (`pytest ...`)
- summary of results
- run_id(s) if behavior changed
