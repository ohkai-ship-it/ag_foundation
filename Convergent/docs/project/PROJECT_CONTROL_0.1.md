# PROJECT CONTROL
#### Description: Consumer-specific rules for ag_foundation that extend the generic Governance Standard. Defines project invariants, CI commands, coverage thresholds, and PR type taxonomy.
#### Convergent: v1.3.2
#### File version: 0.1
#### governs: ag_foundation

---

## GS:PO01 Non-Negotiable Invariants

**Truthful UX:**
- Any user-visible label MUST be derivable from persisted `RunTrace` data.
- Labels are not invented, assumed, or approximated.
- Proof requirement: `ag runs show <run_id>` must demonstrate the exact trace fields backing any printed label.

**Workspace Isolation:**
- The runtime MUST NOT read or write outside active workspace boundaries.
- No cross-workspace data leakage.
- No implicit workspace creation.
- Workspace paths are strict; violations are blocking bugs.

**Manual Mode Gating:**
- Manual mode is **dev/test-only**.
- If manual mode is touched, enforce a dev gate (`AG_DEV=1` or equivalent).
- Print an explicit banner when manual mode is active.
- Manual mode must never be silently enabled.

**Layer Separation:**
- CLI/API/Event adapters parse inputs and call core pipeline only.
- No business logic in adapters.
- Planner/Orchestrator/Executor/Verifier/Recorder must remain independently replaceable.
- Prefer small, composable modules.

---

## GS:PO05 Architectural Layering

**Module Structure:**
```
ag/cli/       — CLI adapter only (Typer). No business logic.
ag/core/      — Core runtime modules and interfaces:
                runtime.py (composition root)
                interfaces.py (Protocols)
                task_spec.py, run_trace.py (schemas)
                execution_plan.py, playbook.py
                planner.py, orchestrator.py,
                executor.py, verifier.py, recorder.py
                schema_verifier.py
ag/playbooks/ — Playbook registry + playbook implementations (plugin entry point)
ag/skills/    — Skill registry + skill implementations (plugin entry point)
ag/storage/   — Persistence (sqlite, artifacts, workspace)
ag/providers/ — LLM provider adapters (OpenAI, stubs)
```
**Layer separation must be preserved.** New top-level packages require an ADR.

**Interface-First Development:**

When adding behavior:
1. Define or extend an interface
2. Implement behind that interface
3. Add tests
4. Add trace fields (if behavior is user-visible)

**Trace Instrumentation Rules:**

Any behavior that affects outputs or execution decisions MUST be traceable.
Every step emits:
- `step_id`, `role`, `reasoning_mode`, `status`, `timing_ms`
- tool/skill calls with outcomes
- evidence refs (if used)
- errors + retries

Trace schema changes are **P1+** and require:
- ARCHITECTURE.md doc update
- Migration/compat note (if needed)

**Error Handling Rules:**
- Fail fast on invalid inputs (adapter/normalizer level).
- Inside the runtime: capture exceptions into trace step `errors`, return a controlled failure status with next-action hints.
- **Never swallow errors silently.**

**Configuration Rules:**

Config resolution order is fixed:
1. Environment variables (`AG_WORKSPACE`, `AG_WORKSPACE_DIR`, `AG_LLM_API_KEY`, etc.)
2. Config file (`AG_CONFIG_PATH` or `~/.ag/config.yaml`) — not yet implemented in v0
3. Hardcoded defaults

Persisted default workspace via `ag ws use <workspace>` → `~/.ag/state.json`.

Config must be:
- Explicit and discoverable (`ag ws config ...` — stubbed, not yet implemented)
- Recorded in trace (what defaults/overrides were applied)

**Performance / Overhead Rules:**
- Keep the "happy path" minimal; avoid heavy frameworks until thresholds are reached.
- If introducing a dependency (LangGraph/LlamaIndex/etc.), include:
  - Why now (threshold)
  - What interface it implements
  - How to disable or bypass for dev/test

---

## GS:PO02 Testing Requirements

**Coverage Thresholds:**

| Module | Minimum Coverage | Enforced |
|--------|-----------------|----------|
| Overall | ≥70% | Yes (`--cov-fail-under=70` in CI) |
| CLI (`src/ag/cli/`) | ≥72% | No (aspirational) |
| Providers (`src/ag/providers/`) | ≥95% | No (aspirational) |
| Storage (`src/ag/storage/`) | ≥95% | No (aspirational) |
| Core (`src/ag/core/`) | ≥85% | No (aspirational) |

Per-module thresholds are targets; only the overall threshold is CI-enforced.

**What to Assert in Tests:**
- `run.status` and `verifier.status` expectations
- Presence and correctness of step fields: `role`, `reasoning_mode`, `status`, `timing_ms`
- Correctness of "truthful label" derivation from trace facts
- Workspace isolation (paths, DB, artifacts)

**Warnings Policy:**

All tests MUST pass with warnings treated as errors. This catches:
- ResourceWarning (unclosed files/connections)
- DeprecationWarning (deprecated APIs)
- UserWarning (potential issues)

**Network Restrictions:**
- No external network calls in CI tests unless explicitly allowed
- No hidden LLM provider dependencies
- Non-deterministic tests require explicit controls

---

## GS:PO06 Autonomy Gate

This gate is mandatory when sprint scope touches planner, orchestrator,
verifier, skill chaining, policy hooks, or user-visible execution labels.

**Start Gate (Sprint Planning):**
- [ ] Scope identifies autonomy-affecting AF/BUG items explicitly
- [ ] Policy impact identified (permission, confirmation, budget, escalation)
- [ ] Trace impact identified (new/changed labels and required trace fields)
- [ ] Failure-path scenarios identified up front
- [ ] Workspace-boundary risks identified

**Close Gate (Sprint Review/Closure):**
- [ ] User-visible labels verified as trace-derived
- [ ] Policy checks verified in touched behavior paths
- [ ] Retry/timeout/failure behavior verified and trace-aligned
- [ ] Workspace isolation verified in happy and failure paths
- [ ] `pytest -W error` evidence captured
- [ ] Open autonomy blockers converted to AF/BUG items with index updates

**Decision Rule:**
- If any P0 Autonomy Gate item is unchecked: sprint cannot be closed.
- If only P1/P2 items remain: `ACCEPT WITH FOLLOW-UPS` is allowed only if
  follow-up AF/BUG items are created and indexed.

---

## GS:PO03 Violations & Escalation

---

## GS:PO04 ADR Creation Criteria

---

## GS:PO07 CI Commands

CI commands for ag_foundation.

**C1 — Targeted CI (per AF commit):**
```bash
pytest tests/test_<relevant>.py -W error
```
Run only the tests relevant to the current AF. Do NOT run the full suite per commit.

**C2 — Full CI + evidence (review):**
```bash
ruff check src tests
ruff format --check src tests
AG_DEV=1 pytest -W error
AG_DEV=1 pytest --cov=src/ag --cov-report=term-missing --cov-fail-under=70
```

**C3 — Full CI (pre-merge):**

| Check | Command | Success Criteria |
|-------|---------|------------------|
| Linting | `ruff check src tests` | No errors |
| Formatting | `ruff format --check src tests` | No files need reformatting |
| Tests | `AG_DEV=1 pytest -W error` | All pass, no warnings |
| Coverage | `AG_DEV=1 pytest --cov=src/ag --cov-report=term-missing --cov-fail-under=70` | ≥70% overall (see GS:PO02) |

---

## GS:PO08 Living Docs

Project-specific living documents for ag_foundation.

| Document | Update if sprint changed... |
|----------|----------------------------|
| `README.md` | Test count, coverage, project structure |
| `ARCHITECTURE.md` | Implementation map, pipeline components |
| `CLI_REFERENCE.md` | CLI commands, flags, output format |
| `Convergent/docs/additional/CONTRACT_INVENTORY.md` | Protocol interfaces (Normalizer, Planner, etc.) |
| `Convergent/docs/additional/SCHEMA_INVENTORY.md` | Pydantic schemas (RunTrace, TaskSpec, Step, etc.) |

These are checked during the sprint review living docs sweep.

---

## GS:PO09 PR Type Taxonomy

Evidence requirements by PR type for ag_foundation.

| PR Type | Tests Required | RunTrace Required |
|---------|---------------|-------------------|
| CLI adapter | Unit + Integration | Yes (if labels change) |
| Core runtime | Unit + Integration | Yes |
| Skill/plugin | Unit + Integration | Yes |
| Storage | Unit + Integration | No (unless visible) |
| Trace schema | Contract tests | Yes |

---

## References

- Project roadmap: `docs/project/PROJECT_ROADMAP.md` <!-- generic name — use highest version on disk -->
