# Coding Guidelines (ag_foundation)
# Version number: v0.2

These guidelines keep the codebase modular, testable, and ready for future interfaces (API/UI/IoT) without rewrites.

## 0) Code Quality Enforcement (MANDATORY)

### Ruff Linting
All code must pass Ruff checks before merge:
```bash
# Check for linting issues
ruff check src tests

# Auto-fix issues where possible
ruff check --fix src tests
```

### Ruff Formatting
All code must be formatted with Ruff:
```bash
# Check formatting
ruff format --check src tests

# Apply formatting
ruff format src tests
```

### Pre-commit Hook (Recommended)
Set up pre-commit to run Ruff automatically:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## 1) Golden rules (non-negotiable)
1. **No business logic in adapters.**
   - CLI/API/Event adapters only parse inputs and call the core pipeline.
2. **Truthful UX is trace-derived.**
   - Any label printed must be provable from persisted `RunTrace`.
3. **Workspace isolation is strict.**
   - Never read/write outside the active workspace boundaries.
4. **Manual mode is dev/test-only.**
   - If manual mode is touched, enforce a dev gate and print an explicit banner.
5. **Prefer small, composable modules.**
   - Planner/Orchestrator/Executor/Verifier/Recorder must remain replaceable.

## 2) Code organization (recommended)
Use a clear layering so responsibilities don’t bleed.

- `ag/cli/` — CLI adapter only (Typer/Click)
- `ag/core/` — core runtime modules and interfaces
  - `task_spec.py`, `run_trace.py` (schemas)
  - `normalizer.py`, `planner.py`, `orchestrator.py`, `executor.py`, `verifier.py`, `recorder.py`
- `ag/skills/` — skill registry + skill implementations
- `ag/storage/` — persistence (sqlite, artifacts, configs)
- `ag/telemetry/` — trace export (optional; OTel/Langfuse)
- `ag/policy/` — safety hook interfaces and minimal implementations

> If your repo uses different folder names, keep the same *layer separation*.

## 3) Interface-first development
When adding behavior, prefer:
1) define or extend an interface
2) implement behind that interface
3) add tests
4) add trace fields (if behavior is user-visible)

### Examples
- Adding retrieval: add `Retriever` interface + stub; do not embed retrieval into Planner directly.
- Adding a new workflow backend: keep `Orchestrator` interface stable; swap backend implementation.

## 4) Trace instrumentation rules
Any behavior that affects outputs or execution decisions must be traceable:
- Every step emits:
  - `step_id`, `role`, `reasoning_mode`, `status`, `timing_ms`
  - tool/skill calls with outcomes
  - evidence refs (if used)
  - errors + retries
- Trace schema changes are **P1** and require:
  - doc update (ARCHITECTURE)
  - migration/compat note (if needed)

## 5) Error handling rules
- Fail fast on invalid inputs (adapter/normalizer level).
- Inside the runtime:
  - capture exceptions into trace step `errors`
  - return a controlled failure status with next-action hints
- Never swallow errors silently.

## 6) Configuration rules
Config resolution order must remain:
1) TaskSpec overrides
2) Workspace config
3) System defaults

Config must be:
- explicit and discoverable (`ag ws config ...`)
- recorded in trace (what defaults/overrides were applied)

## 7) Performance / overhead rules
- Keep the “happy path” minimal:
  - avoid heavy frameworks until thresholds are reached
- If introducing a dependency (LangGraph/LlamaIndex/etc.), include:
  - why now (threshold)
  - what interface it implements
  - how to disable or bypass for dev/test
