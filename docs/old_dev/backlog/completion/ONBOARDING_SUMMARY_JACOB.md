# Onboarding Summary — Jacob (Junior Engineer)
## ag_foundation Pre-Sprint 001

**Date:** 2026-02-23  
**Reader:** Jacob  
**Status:** Ready for Sprint 001 implementation

---

## 1. Onboarding Summary (What I Read + Key Invariants)

### A. Architecture Pipeline Modules (Normalizer → Recorder)

The core runtime is a **modular pipeline** where each module is behind a stable interface and can be replaced independently:

1. **TaskSpec Normalizer**
   - Accepts: raw input (prompt, file, or event) + workspace context
   - Produces: standardized `TaskSpec` with applied defaults (budgets, policies, playbook preference)
   - Rule: validates inputs; applies workspace isolation boundaries

2. **Planner**
   - Accepts: normalized `TaskSpec`
   - Produces: decomposed step graph + selected playbook + agent role assignments + reasoning modes per role
   - Rule: no execution happens here; only planning/decomposition

3. **Orchestrator**
   - Accepts: `Playbook` + step graph (from Planner)
   - Orchestrates: manages step execution order, retries, budget enforcement, state transitions
   - Emits to Recorder: step metadata (start/end, inputs/outputs summary)
   - Rule: sequence-first (branching/parallel come later); must remain swappable (eventually to LangGraph)

4. **Executor**
   - Accepts: one `StepSpec` (role, reasoning_mode, constraints)
   - Executes: LLM calls and/or skill invocations (via tools/functions)
   - Returns: step result (outputs, tool calls, evidence refs, errors, timing)
   - Rule: pure execution; no planning; emits all decision-making to trace

5. **Verifier/Evaluator**
   - Accepts: candidate output + acceptance criteria (from task + playbook)
   - Checks: does output meet quality threshold?
   - Returns: `pass | fail` + optional repair suggestion (bounded retries only)
   - Rule: can trigger repair loops within budget; no silent failures

6. **Recorder**
   - Accepts: events from all steps (via SDK/logging)
   - Persists: complete `RunTrace` + artifacts + metadata to storage (SQLite + filesystem)
   - Provides: queryable run history + artifact registry
   - Rule: single source of truth; all CLI/API outputs derive from here

**Key Invariant:** Each module logs to the trace. **Observability is a contract**, not optional.

---

### B. RunTrace Minimum Fields & CLI Display

The **RunTrace** is the canonical record of what happened. Every claim the CLI makes must be provable from the trace.

**RunTrace minimum structure:**
```json
{
  "run_id": "run_2026_02_23_180512_9f3a",
  "workspace_id": "ws_home",
  "mode": "llm" | "manual",
  "interface": "cli" | "api" | "event",
  "playbook": { "name": "...", "version": "0.1", "reasoning_modes": {...} },
  "budgets": { "max_steps": N, "max_retries": N, "max_tool_calls": N, "max_tokens_estimate": N },
  "timestamps": { "started_at": "ISO8601", "finished_at": "ISO8601" },
  "task": { /* normalized TaskSpec */ },
  "steps": [
    {
      "step_id": "s1",
      "role": "planner|writer|critic|...",
      "reasoning_mode": "fast|balanced|deep|structured|safe-action",
      "status": "ok|error|skipped",
      "inputs_summary": "...",
      "outputs_summary": "...",
      "tool_calls": [{ "tool": "...", "status": "ok|error", ... }],
      "skill_calls": [{ "skill": "...", "status": "ok|error", ... }],
      "evidence_refs": [],
      "errors": [],
      "timing_ms": 420
    }
  ],
  "artifacts": [
    { "artifact_id": "a1", "type": "markdown|json|...", "uri": "artifact://...", "created_by_step": "s2" }
  ],
  "verifier": {
    "status": "pass|fail",
    "checks": [{ "name": "...", "result": "pass|fail" }],
    "notes": "..."
  },
  "final": {
    "status": "success|failure",
    "summary": "...",
    "user_visible_output_ref": "artifact://..."
  }
}
```

**CLI Display (truthful labels from trace):**

When you print to the user, derive from trace:
- `mode: llm | manual` → from `trace.mode`
- `verified: pass | fail` → from `trace.verifier.status`
- `retrieval: used | not_used` → check if any step invoked `Retriever`
- `repairs: N` → count of steps where role=="repair"
- `duration: ...` → `finished_at - started_at`
- Artifacts listed → from `trace.artifacts`

**Non-negotiable:** Never hardcode "verified", "used retrieval", or "balanced mode" in the CLI. All labels must be computed from the persisted trace.

---

### C. Non-Negotiable Rules (5 Core Principles)

1. **One PR = One Primary Backlog Item (AF-000x)**
   - Each PR targets a single AF item and satisfies its acceptance criteria (fully or as a split PR).

2. **Truthful UX from RunTrace**
   - Any label shown in CLI must be derivable from persisted RunTrace. Check the trace; don't assume.

3. **No Business Logic in Adapters**
   - CLI/API/Event adapters **only** parse input → call core pipeline → render output from trace.
   - All decision-making, skill selection, planning happens in core runtime.

4. **Workspace Isolation is Strict**
   - Read/write operations must respect workspace boundaries (designated directories, database rows, artifact storage).
   - Never access files or data outside the active workspace without explicit permission.

5. **Manual Mode is Dev/Test-Only**
   - Must be gated (`AG_DEV=1` env var or similar).
   - Must print a prominent banner: `DEV MODE: manual (LLMs disabled)`.
   - End-user behavior is **LLM-first**; manual mode is for developers to debug/test fast.

---

### D. Key Architectural Insights

- **Interface-agnostic core:** Planner/Orchestrator/Executor remain unchanged whether called from CLI, API, or event ingestion. Adapters are thin.
- **Playbook-driven orchestration:** Playbooks specify step graphs, reasoning modes, budgets, verification requirements. They're config, not code.
- **Modular knowledge:** RAG (retrieval) and MLP (learned models) are optional, pluggable modules behind stable interfaces. No LLM is required for correctness.
- **Safety by default:** Confirmation/permission hooks exist even in v0 (simulated today but architecture-ready for real IoT later).
- **Trace-driven truthfulness:** Every user-visible claim is auditable by inspecting the RunTrace. This is the foundation of trust and review.

---

## 2. Dev Environment Readiness

### Current State (as of 2026-02-23)

**What exists:**
- ✅ Cornerstone docs (PROJECT_PLAN, ARCHITECTURE, CLI_REFERENCE, REVIEW_GUIDE)
- ✅ Backlog structure (`/docs/dev/backlog/items/AF-000x`)
- ✅ Testing guidelines (`/docs/dev/engineering/TESTING_GUIDELINES.md`)
- ✅ Coding guidelines (`/docs/dev/engineering/CODING_GUIDELINES.md`)
- ✅ Review guide (`/docs/dev/dev/cornerstone/REVIEW_GUIDE.md`)
- ✅ PR template placeholder (`/docs/dev/repo/templates/PULL_REQUEST_TEMPLATE.md`)
- ✅ Completion note template (`/docs/dev/backlog/templates/COMPLETION_NOTE_TEMPLATE.md`)

**What does NOT exist yet:**
- ❌ Python project structure (no `src/`, `ag/`, `pyproject.toml`, `setup.py`)
- ❌ Any code files (`.py`)
- ❌ Tests (no `tests/`, no `pytest.ini`)
- ❌ CLI entrypoint (no `ag` command)
- ❌ Package config (`pyproject.toml`, `requirements.txt`)
- ❌ Git repo or version control (implied but not confirmed)

### What You Need to Confirm / Build

**Immediate (before first PR):**
1. ✅ Read the cornerstone docs (YOU ARE HERE) → see above summary
2. ⚠️ **Confirm Python environment** → see "Local Dev Setup" below
3. ⚠️ **Set up project skeleton** → likely first implementation task (AF-0004 or similar)

**Local Dev Setup (Next Steps):**
- Confirm Python 3.9+ is available
- Create a `pyproject.toml` or `requirements.txt` with baseline dependencies:
  - `typer` (CLI framework)
  - `pydantic` (schemas: TaskSpec, RunTrace)
  - `pytest` (testing)
  - `sqlalchemy` (optional; start with sqlite3 direct if lightweight)
- Create folder structure:
  ```
  ag/
    __init__.py
    cli/
      __init__.py
      main.py          # typer app
    core/
      __init__.py
      task_spec.py     # TaskSpec schema
      run_trace.py     # RunTrace schema
      normalizer.py    # TaskSpec normalization
      planner.py       # Planner stub
      orchestrator.py  # Orchestrator stub
      executor.py      # Executor stub
      verifier.py      # Verifier stub
      recorder.py      # Recorder stub
    storage/
      __init__.py
      run_store.py     # Run/trace persistence
  tests/
    __init__.py
    test_task_spec.py
    test_run_trace.py
  ```
- Run `pytest --collect-only` to confirm test discovery works
- Create a simple `ag run --help` stub to confirm CLI bootstraps

---

## 3. Proposed First PR Slice (Sprint 001 Start)

Based on the architecture and backlog, here's the **smallest viable slice** for AF-0003 or a new AF-0004:

### PR Title
`feat/core-runtime-skeleton-schemas-and-run-creation`

### Acceptance Criteria (this PR)
- [x] TaskSpec Pydantic schema defined and tested (minimal fields: prompt, workspace_id, mode)
- [x] RunTrace Pydantic schema defined and tested (minimum fields per ARCHITECTURE.md)
- [x] `ag run "<prompt>"` creates a run record with run_id and returns run record (human + JSON)
- [x] `ag runs show <run_id> --json` retrieves and displays RunTrace as JSON
- [x] Basic persistence (SQLite) stores runs + traces
- [x] Tests pass; at least one manual-mode capture showing trace structure

### Files to Touch

**Schema definitions:**
- `ag/core/task_spec.py` — TaskSpec (Pydantic)
- `ag/core/run_trace.py` — RunTrace (Pydantic)

**CLI adapter:**
- `ag/cli/main.py` — Typer app with `ag run` and `ag runs` commands
- `ag/cli/run_handlers.py` — CLI logic for `ag run` and `ag runs show`

**Core runtime (stubs):**
- `ag/core/normalizer.py` — TaskSpec normalizer (stub; just pass through for now)
- `ag/core/plannerpy` — Planner (stub; return minimal playbook)
- `ag/core/orchestrator.py` — Orchestrator (stub; run one "execute_user_request" step)
- `ag/core/executor.py` — Executor (stub; return mock output for now)
- `ag/core/verifier.py` — Verifier (stub; always pass; record in trace)
- `ag/core/recorder.py` — Recorder (real; persist to SQLite)

**Storage:**
- `ag/storage/run_store.py` — SQLite adapter for runs + traces

**Tests:**
- `tests/test_task_spec.py` — unit tests for TaskSpec schema
- `tests/test_run_trace.py` — unit tests for RunTrace schema
- `tests/test_run_creation.py` — integration test: `ag run` end-to-end

**Config:**
- `pyproject.toml` — Python package config
- `.gitignore` — ignore `*.db`, `__pycache__`, `.pytest_cache`

### Expected Evidence

1. **Test results:**
   ```
   pytest tests/ -v
   # Output: 15 tests passed, 0 failed
   ```

2. **Manual run capture (LLM-free mode):**
   ```bash
   export AG_DEV=1
   ag run --mode manual "What is 2+2?"
   # Run ID: run_2026_02_23_123456_abcd
   # Trace endpoint: ag runs show run_2026_02_23_123456_abcd --json
   ```

3. **JSON trace output:**
   ```bash
   ag runs show run_2026_02_23_123456_abcd --json
   # Returns valid RunTrace JSON (with steps, verifier.status, final.status, etc.)
   ```

4. **Completion note:**
   - Documents which acceptance criteria were met
   - Links to test evidence
   - Links to run trace IDs
   - Lists files added/modified

---

## 4. Summary: Ready to Begin

**You're ready to:**
1. Set up the Python project skeleton (`pyproject.toml`, folder structure)
2. Define TaskSpec and RunTrace schemas (Pydantic)
3. Implement minimal CLI scaffolding (`ag run`, `ag runs show --json`)
4. Implement storage layer (SQLite run/trace persistence)
5. Wire up the core runtime stubs (normalizer → planner → orchestrator → executor → verifier → recorder)
6. Write tests + capture at least one trace as evidence
7. Open a PR against AF-0003 or AF-0004 with this slice

**Key attitudes as you code:**
- **Truthfulness first:** every label in the CLI must come from the trace
- **Interface-agnostic:** core runtime is independent of CLI; keep them loosely coupled
- **Tests + evidence:** ship with test results and at least one captured run trace
- **Review-ready:** every PR should be reviewable end-to-end (docs ↔ code ↔ evidence)

**Next step:** Confirm your Python setup and begin AF-0004 implementation (or whichever item is assigned) with this slice as your scope.

---

**Document prepared:** 2026-02-23  
**Prepared by:** Onboarding summary (automated review of cornerstone docs)
