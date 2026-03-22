# AF-0124 — V2Executor: LLM output repair
# Version number: v0.1
# Created: 2026-03-22
# Status: IN_PROGRESS
# Priority: P2
# Area: Core Runtime / Executor

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI workflow (two-phase — see template)
> - 1 PR = 1 sprint
> - INDEX update rule (status ↔ filename integrity)
>
> **CI workflow (CRITICAL):**
> - **During AF development:** run targeted tests only
>   `pytest tests/test_<relevant>.py -W error`
> - **Before commit (full gate):** run the complete CI gate
>   1. `ruff check src tests`
>   2. `ruff format --check src tests`
>   3. `pytest -W error`
>   4. `pytest --cov=src/ag --cov-report=term-missing`
>
> Do NOT run the full suite on every save. Targeted tests keep feedback fast.
> The full gate runs once, right before `git commit`.

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF-0124
- **Type:** Feature
- **Status:** IN_PROGRESS
- **Priority:** P2
- **Area:** Core Runtime / Executor
- **Owner:** —
- **Target sprint:** Sprint 15 — llm_intelligence_layer

---

## Problem

V1Executor retries skill execution on schema validation failure using the same parameters. This is effective when the LLM produces non-deterministic output that sometimes validates and sometimes doesn't, but wasteful when the output is *structurally close* — e.g., a missing field, wrong type, or trailing comma in JSON.

Full skill re-invocation is expensive: it repeats tool calls, LLM inference, and network I/O. For common structural mistakes, a targeted LLM repair is cheaper and more reliable than retrying the entire skill.

---

## Goal

- V2Executor adds an LLM output repair step between retry exhaustion and final failure
- Repair targets structural/schema issues only (missing field, wrong type, extra comma)
- Full evidence trail: original output → repair prompt → repaired output
- Flow: validate → fail → retry skill → fail → **LLM repair** → fail → give up

---

## Non-goals

- Semantic repair (fixing meaning/content — that's verification, not execution)
- Replacing V1Executor retry logic (V2 extends the loop with one more step)
- Repairing non-JSON outputs (only structured outputs with declared schemas)
- Auto-retrying LLM repair (one repair attempt, then give up)

---

## Design

Based on the V2 roadmap in **AF-0116** (V1Executor, DONE).

### Execution flow (V2)

```
V2Executor.execute(skill_name, parameters, context)
  ├── attempt 1: skill.execute() → validate output
  │   └── pass → return success
  ├── attempt 2: skill.execute() → validate output  (V1 retry)
  │   └── pass → return success
  ├── attempt 3: skill.execute() → validate output  (V1 retry)
  │   └── pass → return success
  ├── LLM repair: send last output + schema + errors to LLM
  │   └── validate repaired output
  │       ├── pass → return success (repaired)
  │       └── fail → return failure
  └── give up: return failure with full evidence
```

### Repair prompt design

```python
class RepairRequest(BaseModel):
    original_output: dict          # the malformed output
    target_schema: dict            # expected JSON schema
    validation_errors: list[str]   # specific errors to fix
    instruction: str = "Fix the JSON to match the schema. Only fix the failing fields."

class RepairResult(BaseModel):
    repaired_output: dict | None   # None if repair failed
    fields_changed: list[str]      # which fields were modified
    repair_model: str              # which LLM performed repair
    repair_tokens: int             # tokens used
    repair_ms: int                 # time taken
```

### Integration point

AF-0116 notes that `SchemaValidator.validate_with_repair()` already supports a `repair_fn` callback. V2Executor provides an LLM-backed `repair_fn`:

```python
class V2Executor(V1Executor):
    def _llm_repair_fn(self, output: dict, schema: dict, errors: list[str]) -> dict | None:
        """LLM-backed repair callback for SchemaValidator."""
        # Send repair prompt to provider
        # Return repaired dict or None if repair failed
```

### Trace evidence

```python
class ExecutionEvidence(BaseModel):
    # ... existing V1 fields (attempts, validation_errors) ...
    repair_attempted: bool
    repair_result: RepairResult | None  # None if no repair attempted
```

### Files touched

| File | Change |
|------|--------|
| `src/ag/core/executor.py` | V2Executor class extending V1Executor with LLM repair step |
| `src/ag/core/run_trace.py` | `RepairResult` model, `ExecutionEvidence` extension |
| `src/ag/core/interfaces.py` | No change (same `Executor` protocol) |
| `src/ag/core/runtime.py` | **Change default from V0Executor to V2Executor(registry, provider)** |
| `src/ag/cli/main.py` | Pass provider to executor construction |
| `ARCHITECTURE.md` | Update implementation map: Executor → V2Executor |
| `tests/test_runtime.py` | V2Executor tests: repair success/failure, evidence recording |

---

## Acceptance criteria (Definition of Done)

- [ ] Deliverable exists in the correct folder
- [ ] Naming conventions applied (file name + internal Status match)
- [ ] INDEX file(s) updated
- [ ] CI/local checks pass (two-phase workflow):
  - **During development:** targeted tests run (`pytest tests/test_runtime.py -W error`)
  - **Before commit (full gate):**
    - [ ] `ruff check src tests`
    - [ ] `ruff format --check src tests`
    - [ ] `pytest -W error`
    - [ ] coverage thresholds met (`pytest --cov=src/ag --cov-report=term-missing`)
- [ ] V2Executor attempts LLM repair after V1 retry exhaustion
- [ ] Repair only runs when output has declared schema and validation failures
- [ ] `RepairResult` evidence recorded in trace (original → repaired → fields changed)
- [ ] Successful repair returns repaired output as if skill produced it
- [ ] Failed repair results in normal failure (no infinite loops)
- [ ] LLM unavailable → skip repair, fail as V1 would
- [ ] Evidence included: tests + RunTrace ID(s)
- [ ] Completion section filled below (mandatory when Status = Done)

---

## Dependencies

- AF-0116 V1Executor (DONE — Sprint 14)
- `SchemaValidator.validate_with_repair()` callback interface (AF-0116)
- LLM provider infrastructure (existing — `src/ag/providers/`)

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| LLM repair changes content meaning | Semantic drift | Targeted field repair only (failing fields, rest preserved) |
| Extra LLM call adds cost | Token budget | Repair is much cheaper than full re-invocation (no tool calls) |
| Repair succeeds but produces wrong content | Silent error | V2Verifier (AF-0123) catches semantic issues post-repair |
| Repair prompt leaks internal schema | Security | Schema is already in skill metadata, not a secret |

---

## LLM integration (CRITICAL — follow existing patterns)

V2Executor needs an `LLMProvider` injected via constructor (same pattern as V2Planner, V2Verifier):

```python
from ag.providers.base import LLMProvider, ChatMessage, MessageRole

class V2Executor(V1Executor):
    """Extends V1Executor with LLM-powered output repair."""

    def __init__(self, registry: SkillRegistry, provider: LLMProvider | None = None,
                 max_attempts: int = 3) -> None:
        super().__init__(registry, max_attempts=max_attempts)
        self._provider = provider  # None = skip repair, fail as V1 would

    def execute(self, skill_name: str, parameters: dict) -> tuple[bool, str, dict]:
        # V1 execution with retry
        success, summary, result = super().execute(skill_name, parameters)
        if success or self._provider is None:
            return success, summary, result

        # V1 failed after all retries — attempt LLM repair
        return self._attempt_llm_repair(skill_name, result)

    def _llm_repair_fn(self, output: dict, schema: dict, errors: list[str]) -> dict | None:
        """LLM-backed repair callback."""
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content="Fix the JSON to match the schema. Only fix the failing fields."),
            ChatMessage(role=MessageRole.USER, content=json.dumps({
                "output": output, "schema": schema, "errors": errors
            })),
        ]
        response = self._provider.chat(messages=messages)
        return json.loads(response.content)  # parse repaired JSON
```

**Wiring in runtime/CLI** — V2Executor receives the same provider instance:
```python
# In src/ag/core/runtime.py create_runtime() or CLI
provider = get_provider(ProviderConfig(provider="openai", model="gpt-4o-mini"))
executor = V2Executor(registry, provider)  # ← replaces V1Executor(registry)
```

**Graceful degradation:** `V2Executor(registry, provider=None)` behaves identically to `V1Executor` — tests that don't need LLM instantiate without provider.

### Default pipeline version update (CRITICAL)

- `src/ag/core/runtime.py` `create_runtime()`: currently hardcodes `V0Executor(registry)` — **change to `V2Executor(registry, provider)`**
- `ARCHITECTURE.md` implementation map: update Executor row to show V2Executor as current

---

## Implementation notes

- V2Executor extends V1Executor — do NOT duplicate retry logic
- Use existing `repair_fn` callback in `SchemaValidator` (from AF-0116)
- Repair prompt should include specific validation errors, not just "fix it"
- One repair attempt per execution — no repair retry loop
- V2Verifier (AF-0123) and V2Executor are independent code paths; no ordering dependency at implementation time

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF-0124
- **PR:** #
- **Author:**
- **Date:** YYYY-MM-DD
- **Branch:**
- **Risk level:** P2
- **Runtime mode used for verification:**

---

## 2) Acceptance criteria verification

- [ ] ...

---

## 3) What changed (file-level)

- ...

---

## 4) Architecture alignment (mandatory)
- **Layering:**
- **Interfaces touched:**
- **Backward compatibility:**

---

## 5) Truthful UX check (mandatory when user-visible)
- **User-visible labels affected:**
- **Trace fields backing them:**
- **Proof:**

---

## 6) Tests executed (mandatory unless docs-only)

- Command: `...`
  - Result:

---

## 7) Run evidence (mandatory for behavior changes)
- **RunTrace ID(s):**
- **How to reproduce:**
- **Expected trace outcomes:**

---

## 8) Artifacts (if applicable)

---

## 9) Risks, tradeoffs, follow-ups

---

## 10) Reviewer checklist (copy/paste)
- [ ] I can map PR → AF item and see acceptance criteria satisfied
- [ ] I can verify truthful labels from RunTrace
- [ ] I can reproduce a run (or it's docs-only)
- [ ] Tests were run and results are documented
- [ ] Any contract changes are documented in cornerstone docs
