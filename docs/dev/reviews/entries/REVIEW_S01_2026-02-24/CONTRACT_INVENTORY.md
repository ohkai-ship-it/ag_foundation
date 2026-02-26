# Contract Inventory — ag_foundation
# Version: v0.1 (Sprint 01)
# Generated: 2026-02-25

## Summary

| Metric | Value |
|--------|-------|
| **Total Contracts** | 17 |
| **Pydantic Models** | 12 |
| **Enums** | 6 |
| **Protocol Interfaces** | 6 |
| **Builders** | 3 |

---

## Contract Categories

| Category | Count | Status |
|----------|-------|--------|
| Core Schemas | 3 | ✅ Implemented |
| Supporting Models | 9 | ✅ Implemented |
| Enums | 6 | ✅ Implemented |
| Interfaces (Protocols) | 6 | ✅ Defined |
| Builders | 3 | ✅ Implemented |

---

## Core Schemas (3)

### 1. TaskSpec
**Location:** `src/ag/core/task_spec.py`  
**Version:** 0.1  
**Purpose:** Normalized representation of a task request (input to runtime)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| task_spec_version | str | No | "0.1" | Schema version |
| prompt | str | Yes | — | User's task description |
| workspace_id | str | Yes | — | Workspace identifier |
| mode | ExecutionMode | No | MANUAL | Execution mode |
| playbook_preference | str | No | None | Preferred playbook name |
| budgets | Budgets | No | Budgets() | Resource budgets |
| constraints | Constraints | No | Constraints() | Execution constraints |

**Features:**
- JSON round-trip via `to_json()` / `from_json()`
- Builder pattern via `TaskSpecBuilder`
- Pydantic validation with `extra="forbid"`

---

### 2. RunTrace
**Location:** `src/ag/core/run_trace.py`  
**Version:** 0.1  
**Purpose:** Evidence log capturing full execution history

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| trace_version | str | No | "0.1" | Schema version |
| run_id | str | No | uuid4() | Unique run identifier |
| workspace_id | str | Yes | — | Workspace identifier |
| mode | ExecutionMode | Yes | — | Execution mode used |
| playbook | PlaybookMetadata | Yes | — | Playbook used |
| started_at | datetime | Yes | — | Run start timestamp |
| ended_at | datetime | No | None | Run end timestamp |
| duration_ms | int | No | None | Total duration in ms |
| steps | list[Step] | No | [] | Execution steps |
| artifacts | list[Artifact] | No | [] | Artifacts produced |
| verifier | Verifier | Yes | — | Verification result |
| final | FinalStatus | Yes | — | Final run outcome |
| error | str | No | None | Error message if failed |
| metadata | dict | No | {} | Additional metadata |

**Features:**
- JSON round-trip via `to_json()` / `from_json()`
- Builder pattern via `RunTraceBuilder`
- Timestamps use UTC
- All fields captured for truthful UX

---

### 3. Playbook
**Location:** `src/ag/core/playbook.py`  
**Version:** 0.1  
**Purpose:** Workflow definition for task execution

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| playbook_version | str | No | "0.1" | Schema version |
| name | str | Yes | — | Playbook name |
| version | str | Yes | — | Playbook version |
| description | str | No | "" | Description |
| reasoning_modes | list[ReasoningMode] | No | [DIRECT] | Supported modes |
| budgets | Budgets | No | Budgets() | Default budgets |
| steps | list[PlaybookStep] | No | [] | Linear step sequence |
| metadata | dict | No | {} | Additional metadata |

**Features:**
- Linear step execution (v0)
- JSON round-trip via `to_json()` / `from_json()`
- Builder pattern via `PlaybookBuilder`

---

## Supporting Models (9)

### 4. Budgets
**Location:** `src/ag/core/task_spec.py`  
**Purpose:** Resource limits for execution

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| max_steps | int | None | Maximum number of steps |
| max_tokens | int | None | Maximum token budget |
| max_duration_seconds | int | None | Maximum wall-clock duration |

---

### 5. Constraints
**Location:** `src/ag/core/task_spec.py`  
**Purpose:** Execution constraints and guardrails

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| allowed_skills | list[str] | None | Whitelist of skill names |
| blocked_skills | list[str] | None | Blacklist of skill names |
| allowed_paths | list[str] | None | Filesystem path whitelist |
| blocked_paths | list[str] | None | Filesystem path blacklist |

---

### 6. Step
**Location:** `src/ag/core/run_trace.py`  
**Purpose:** Single step in run trace

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| step_id | str | Yes | — | Unique step identifier |
| step_number | int | Yes | — | Sequential step number |
| step_type | StepType | Yes | — | Type of step |
| skill_name | str | No | None | Skill name if skill_call |
| input_summary | str | No | "" | Summary of step input |
| output_summary | str | No | "" | Summary of step output |
| started_at | datetime | Yes | — | Step start timestamp |
| ended_at | datetime | No | None | Step end timestamp |
| duration_ms | int | No | None | Duration in milliseconds |
| tokens_used | int | No | None | Tokens consumed |
| error | str | No | None | Error message if failed |
| artifacts | list[str] | No | [] | Artifact IDs produced |

---

### 7. Artifact
**Location:** `src/ag/core/run_trace.py`  
**Purpose:** Metadata for produced files/objects

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| artifact_id | str | Yes | — | Unique artifact identifier |
| path | str | Yes | — | Storage path or URI |
| artifact_type | str | Yes | — | MIME type or category |
| size_bytes | int | No | None | Size in bytes |
| checksum | str | No | None | SHA256 checksum |
| created_at | datetime | No | now() | Creation timestamp |
| metadata | dict | No | {} | Additional metadata |

---

### 8. Verifier
**Location:** `src/ag/core/run_trace.py`  
**Purpose:** Verification result for a run

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| status | VerifierStatus | Yes | — | Verification status |
| checked_at | datetime | No | None | Verification timestamp |
| message | str | No | None | Verifier message |
| evidence | dict | No | {} | Verification evidence |

---

### 9. PlaybookMetadata
**Location:** `src/ag/core/run_trace.py`  
**Purpose:** Reference to playbook used in a run

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | str | Yes | Playbook name |
| version | str | Yes | Playbook version |

---

### 10. PlaybookStep
**Location:** `src/ag/core/playbook.py`  
**Purpose:** Single step in playbook definition

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| step_id | str | Yes | — | Unique step identifier |
| name | str | Yes | — | Human-readable step name |
| step_type | PlaybookStepType | No | SKILL | Type of step |
| skill_name | str | No | None | Skill to invoke |
| description | str | No | "" | Step description |
| required | bool | No | True | Whether step is required |
| retry_count | int | No | 0 | Max retry attempts |
| timeout_seconds | int | No | None | Step timeout |
| parameters | dict | No | {} | Step parameters |
| on_failure | str | No | None | Step ID to jump to on failure |

---

## Enums (6)

### 11. ExecutionMode
**Location:** `src/ag/core/task_spec.py`

| Value | Description |
|-------|-------------|
| MANUAL | Dev/test mode, LLMs disabled |
| SUPERVISED | Human-in-loop mode |
| AUTONOMOUS | Full LLM mode |

---

### 12. VerifierStatus
**Location:** `src/ag/core/run_trace.py`

| Value | Description |
|-------|-------------|
| PENDING | Not yet verified |
| PASSED | Verification passed |
| FAILED | Verification failed |
| SKIPPED | Verification skipped |

---

### 13. FinalStatus
**Location:** `src/ag/core/run_trace.py`

| Value | Description |
|-------|-------------|
| SUCCESS | Run completed successfully |
| FAILURE | Run failed |
| ABORTED | Run was aborted |
| TIMEOUT | Run timed out |

---

### 14. StepType
**Location:** `src/ag/core/run_trace.py`

| Value | Description |
|-------|-------------|
| SKILL_CALL | Skill invocation |
| REASONING | LLM reasoning step |
| VERIFICATION | Verification step |
| USER_INPUT | User input step |

---

### 15. PlaybookStepType
**Location:** `src/ag/core/playbook.py`

| Value | Description |
|-------|-------------|
| SKILL | Skill execution step |
| BRANCH | Conditional branch (future) |
| LOOP | Loop construct (future) |
| GATE | Gate/checkpoint (future) |

---

### 16. ReasoningMode
**Location:** `src/ag/core/playbook.py`

| Value | Description |
|-------|-------------|
| DIRECT | Simple/fast reasoning |
| CHAIN_OF_THOUGHT | Step-by-step reasoning |
| TREE_OF_THOUGHT | Exploratory reasoning |
| REFLECTION | Self-critique reasoning |

---

## Protocol Interfaces (6)

### Normalizer
**Location:** `src/ag/core/interfaces.py`  
**Method:** `normalize(prompt: str, **options) -> TaskSpec`  
**Purpose:** Parse and validate user input into TaskSpec

---

### Planner
**Location:** `src/ag/core/interfaces.py`  
**Method:** `plan(task: TaskSpec) -> Playbook`  
**Purpose:** Select and configure execution playbook

---

### Orchestrator
**Location:** `src/ag/core/interfaces.py`  
**Method:** `run(task: TaskSpec, playbook: Playbook) -> RunTrace`  
**Purpose:** Coordinate execution of playbook steps

---

### Executor
**Location:** `src/ag/core/interfaces.py`  
**Method:** `execute(skill_name: str, parameters: dict) -> tuple[bool, str, dict]`  
**Purpose:** Execute individual skills/tools

---

### Verifier
**Location:** `src/ag/core/interfaces.py`  
**Method:** `verify(trace: RunTrace) -> tuple[str, str | None]`  
**Purpose:** Check acceptance criteria and quality

---

### Recorder
**Location:** `src/ag/core/interfaces.py`  
**Methods:**
- `record(trace: RunTrace) -> None`
- `register_artifact(trace: RunTrace, artifact_id: str, path: str, content: bytes) -> str`

**Purpose:** Persist run traces and register artifacts to storage

**Implementation:** `V0Recorder` in `src/ag/core/runtime.py`

---

## Builders (3)

### TaskSpecBuilder
**Location:** `src/ag/core/task_spec.py`  
**Pattern:** Fluent builder
```python
TaskSpecBuilder("prompt", "workspace")
    .mode(ExecutionMode.MANUAL)
    .playbook_preference("fast")
    .budgets(max_steps=10)
    .constraints(blocked_skills=["shell"])
    .build()
```

---

### RunTraceBuilder
**Location:** `src/ag/core/run_trace.py`  
**Pattern:** Fluent builder
```python
RunTraceBuilder("ws", ExecutionMode.MANUAL, "playbook", "1.0")
    .add_step(StepType.SKILL_CALL, skill_name="read_file")
    .add_artifact("/path", "text/plain")
    .verify(VerifierStatus.PASSED)
    .complete(FinalStatus.SUCCESS)
    .build()
```

---

### PlaybookBuilder
**Location:** `src/ag/core/playbook.py`  
**Pattern:** Fluent builder
```python
PlaybookBuilder("name", "1.0")
    .description("My playbook")
    .reasoning_mode(ReasoningMode.DIRECT)  # DIRECT, CHAIN_OF_THOUGHT, TREE_OF_THOUGHT, REFLECTION
    .add_skill_step("step-1", "analyze", "analyze_task")
    .budgets(max_steps=10)
    .build()
```

> **Note:** In v0, "balanced" is a human-friendly label stored in playbook metadata.
> The actual enum value used is `DIRECT` (`balanced = direct in v0`).

---

## Contract Evolution Policy

All v0.x contracts follow **additive-only evolution**:

| Rule | Description |
|------|-------------|
| ❌ No removals | Fields cannot be removed |
| ❌ No renames | Fields cannot be renamed |
| ✅ Additions OK | New optional fields can be added |
| ✅ Deprecation OK | Fields can be marked deprecated |

**Enforcement:** Contract tests in `test_contracts.py` validate all required fields exist.

---

## Storage Contracts

### SQLite Tables

| Table | Purpose | Columns |
|-------|---------|---------|
| runs | RunTrace storage | run_id, workspace_id, data (JSON), created_at |
| artifacts | Artifact metadata | artifact_id, run_id, workspace_id, data (JSON), created_at |

### Filesystem Structure

```
~/.ag/workspaces/
├── <workspace_id>/
│   ├── runs/
│   │   └── <run_id>.json
│   ├── artifacts/
│   │   └── <run_id>/
│   │       └── <artifact_file>
│   └── ag.db (SQLite)
```

---

## Notes

- All Pydantic models use `extra="forbid"` to reject unknown fields
- All models support JSON serialization via `to_json()` / `from_json()`
- Timestamps use UTC via `datetime(UTC)`
- UUIDs generated via `uuid4()`
- Contracts tested for round-trip stability
