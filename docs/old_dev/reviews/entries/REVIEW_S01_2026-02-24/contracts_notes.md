# Pass 3 — Contracts Audit
# Date: 2026-02-24
# Reviewer: Jacob

## TaskSpec v0.1 Fields

### Required Fields (per CLI_REFERENCE.md expectations)
| Field | Present | Type | Notes |
|-------|---------|------|-------|
| task_spec_version | ✅ | str | Default "0.1" |
| prompt | ✅ | str | Required, min_length=1 |
| workspace_id | ✅ | str | Required, min_length=1 |
| mode | ✅ | ExecutionMode | Default MANUAL |
| playbook_preference | ✅ | str | Optional |
| budgets | ✅ | Budgets | max_steps, max_tokens, max_duration_seconds |
| constraints | ✅ | Constraints | allowed/blocked skills & paths |

### TaskSpec Contract Tests
- ✅ `test_version_field_present`
- ✅ `test_required_fields`
- ✅ `test_json_roundtrip`
- ✅ `test_stable_defaults`
- ✅ `test_builder_produces_valid_spec`
- ✅ `test_all_v01_fields_present` (additive evolution)

---

## RunTrace v0.1 Fields

### Required Fields
| Field | Present | Type | Notes |
|-------|---------|------|-------|
| trace_version | ✅ | str | Default "0.1" |
| run_id | ✅ | str | UUID, auto-generated |
| workspace_id | ✅ | str | Required |
| mode | ✅ | ExecutionMode | Required |
| playbook | ✅ | PlaybookMetadata | name + version |
| started_at | ✅ | datetime | Required |
| ended_at | ✅ | datetime | Optional |
| duration_ms | ✅ | int | Optional |
| steps | ✅ | list[Step] | Default [] |
| artifacts | ✅ | list[Artifact] | Default [] |
| verifier | ✅ | Verifier | status, checked_at, message, evidence |
| final | ✅ | FinalStatus | Required |
| error | ✅ | str | Optional |
| metadata | ✅ | dict | Default {} |

### RunTrace Contract Tests
- ✅ `test_version_field_present`
- ✅ `test_required_fields`
- ✅ `test_json_roundtrip`
- ✅ `test_stable_defaults`
- ✅ `test_builder_produces_valid_trace`
- ✅ `test_all_v01_fields_present` (additive evolution)

---

## Playbook v0.1 Fields

### Structure
| Field | Present | Type | Notes |
|-------|---------|------|-------|
| playbook_version | ✅ | str | Default "0.1" |
| name | ✅ | str | Required |
| version | ✅ | str | Required |
| description | ✅ | str | Default "" |
| reasoning_modes | ✅ | list[ReasoningMode] | Default [DIRECT] |
| budgets | ✅ | Budgets | Inherited from TaskSpec |
| steps | ✅ | list[PlaybookStep] | Linear sequence |
| metadata | ✅ | dict | Default {} |

### Linear Structure Confirmed
- Steps are a simple `list[PlaybookStep]` — linear execution
- Step types: SKILL, BRANCH, LOOP, GATE
- No DAG or graph structure in v0 — linear only

### Playbook Contract Tests
- ✅ `test_version_field_present`
- ✅ `test_json_roundtrip`
- ✅ `test_stable_defaults`
- ✅ `test_all_v01_fields_present` (additive evolution)

---

## Additive Evolution Guardrails

All three schemas include explicit guardrail tests:

```python
class TestTaskSpecAdditiveEvolution:
    REQUIRED_FIELDS_V01 = {...}  # Locked set

class TestRunTraceAdditiveEvolution:
    REQUIRED_FIELDS_V01 = {...}  # Locked set

class TestPlaybookAdditiveEvolution:
    REQUIRED_FIELDS_V01 = {...}  # Locked set
```

These tests ensure no v0.1 fields can be removed without breaking the test suite.

---

## JSON Round-trip Tests

All schemas have explicit JSON round-trip tests:
- `TaskSpec.to_json()` / `from_json()`
- `RunTrace.to_json()` / `from_json()`
- `Playbook.to_json()` / `from_json()`

Each test verifies lossless serialization with complex nested objects.

---

## Result
✅ PASS — All required fields present, JSON round-trip verified, additive evolution guardrails in place
