# Future Contracts Roadmap — ag_foundation
# Version: v0.1 (Sprint 01)
# Generated: 2026-02-25
# Based on: ARCHITECTURE.md, PROJECT_PLAN.md, CLI_REFERENCE.md

## Summary

This document outlines contracts expected to be needed in upcoming sprints based on the architecture and project plan.

| Sprint | Focus | Estimated New Contracts |
|--------|-------|------------------------|
| Sprint 02 | Agent network behavior | 8-12 |
| Sprint 03 | Observability & trace | 4-6 |
| Sprint 04 | Safety primitives | 6-8 |
| Sprint 05 | Skills ecosystem | 10-15 |
| Sprint 06 | Workspace maturity | 8-10 |
| Sprint 07 | Interface readiness | 5-8 |

---

## Sprint 02 — Agent Network Behavior

**Goal:** Evolve from single executor to multi-agent delegation.

### Agent/Role Contracts

#### AgentRole
**Purpose:** Define agent responsibilities in a playbook

| Field | Type | Description |
|-------|------|-------------|
| role_id | str | Unique role identifier |
| name | str | Role name (planner, researcher, writer, critic) |
| capabilities | list[str] | Skills this role can invoke |
| reasoning_mode | ReasoningMode | Default reasoning mode |
| budgets | Budgets | Role-specific budgets |
| context_window | int | Max context tokens for role |

---

#### Delegation
**Purpose:** Record of task delegation between agents

| Field | Type | Description |
|-------|------|-------------|
| delegation_id | str | Unique delegation ID |
| parent_step_id | str | Step that initiated delegation |
| from_role | str | Source role |
| to_role | str | Target role |
| subtask | str | Delegated task description |
| context | dict | Passed context |
| constraints | Constraints | Delegation constraints |

---

#### SubtaskSpec
**Purpose:** Normalized subtask for delegation

| Field | Type | Description |
|-------|------|-------------|
| subtask_id | str | Unique subtask ID |
| parent_task_id | str | Parent TaskSpec ID |
| prompt | str | Subtask description |
| role | str | Assigned role |
| priority | int | Execution priority |
| dependencies | list[str] | Subtask dependencies |

---

#### StepGraph
**Purpose:** Non-linear step execution (replaces linear list)

| Field | Type | Description |
|-------|------|-------------|
| nodes | list[StepNode] | Step nodes |
| edges | list[StepEdge] | Step dependencies |
| entry_points | list[str] | Starting nodes |
| exit_points | list[str] | Terminal nodes |

---

### Context Passing Contracts

#### ContextBundle
**Purpose:** Bounded context passed between steps

| Field | Type | Description |
|-------|------|-------------|
| bundle_id | str | Unique bundle ID |
| source_step_id | str | Producing step |
| summary | str | Context summary |
| key_facts | list[str] | Important facts extracted |
| evidence_refs | list[str] | References to evidence |
| token_count | int | Approximate token size |

---

## Sprint 03 — Observability & Truthful UX

**Goal:** Rich run inspection and auditable traces.

### Enhanced Trace Contracts

#### TraceEvent
**Purpose:** Stream-friendly trace events

| Field | Type | Description |
|-------|------|-------------|
| event_id | str | Unique event ID |
| event_type | TraceEventType | Event type enum |
| timestamp | datetime | Event timestamp |
| run_id | str | Parent run ID |
| step_id | str | Related step (optional) |
| payload | dict | Event-specific data |

---

#### TraceEventType (Enum)
| Value | Description |
|-------|-------------|
| RUN_STARTED | Run began |
| STEP_STARTED | Step began |
| STEP_COMPLETED | Step finished |
| SKILL_INVOKED | Skill called |
| SKILL_RETURNED | Skill returned |
| ERROR_OCCURRED | Error happened |
| VERIFICATION_STARTED | Verifier began |
| RUN_COMPLETED | Run finished |

---

#### EvidenceBundle
**Purpose:** Collected evidence for verification

| Field | Type | Description |
|-------|------|-------------|
| bundle_id | str | Unique bundle ID |
| step_id | str | Producing step |
| evidence_type | str | Type (source, citation, output) |
| content_hash | str | Content checksum |
| uri | str | Evidence location |
| metadata | dict | Additional metadata |

---

## Sprint 04 — Safety Primitives

**Goal:** Human-in-the-loop gates and policy enforcement.

### Permission & Policy Contracts

#### Permission
**Purpose:** Workspace-scoped permission grant

| Field | Type | Description |
|-------|------|-------------|
| permission_id | str | Unique permission ID |
| workspace_id | str | Workspace scope |
| resource_type | str | Resource type (skill, path, action) |
| resource_pattern | str | Resource pattern (glob/regex) |
| access_level | AccessLevel | Read/write/execute |
| granted_by | str | Granter identity |
| expires_at | datetime | Expiration (optional) |

---

#### AccessLevel (Enum)
| Value | Description |
|-------|-------------|
| DENY | Explicitly denied |
| READ | Read-only access |
| WRITE | Read/write access |
| EXECUTE | Can invoke/execute |
| ADMIN | Full control |

---

#### ConfirmationRequest
**Purpose:** Human confirmation request

| Field | Type | Description |
|-------|------|-------------|
| request_id | str | Unique request ID |
| run_id | str | Related run |
| step_id | str | Related step |
| action_type | str | Action requiring confirmation |
| action_summary | str | Human-readable summary |
| risk_level | RiskLevel | Assessed risk |
| timeout_seconds | int | Confirmation timeout |
| default_action | str | Action if timeout (deny/allow) |

---

#### RiskLevel (Enum)
| Value | Description |
|-------|-------------|
| LOW | Informational only |
| MEDIUM | Reversible changes |
| HIGH | Potentially destructive |
| CRITICAL | Irreversible actions |

---

#### PolicyRule
**Purpose:** Declarative policy rule

| Field | Type | Description |
|-------|------|-------------|
| rule_id | str | Unique rule ID |
| name | str | Rule name |
| description | str | Rule description |
| condition | str | Condition expression |
| action | PolicyAction | Action to take |
| priority | int | Rule priority |

---

#### RedactionRule
**Purpose:** Data redaction policy

| Field | Type | Description |
|-------|------|-------------|
| rule_id | str | Unique rule ID |
| pattern | str | Pattern to match |
| redaction_type | str | full/partial/hash |
| applies_to | list[str] | Contexts (log/trace/artifact) |

---

## Sprint 05 — Skills Ecosystem

**Goal:** Real tools with proper contracts.

### Skill Contracts

#### SkillSpec
**Purpose:** Full skill definition

| Field | Type | Description |
|-------|------|-------------|
| skill_id | str | Unique skill ID |
| name | str | Skill name |
| version | str | Skill version |
| description | str | Skill description |
| input_schema | dict | JSON Schema for input |
| output_schema | dict | JSON Schema for output |
| permissions_required | list[str] | Required permissions |
| tool_dependencies | list[str] | External tool dependencies |
| timeout_default | int | Default timeout |
| retry_policy | RetryPolicy | Retry configuration |
| tags | list[str] | Categorization tags |

---

#### SkillInvocation
**Purpose:** Record of skill call

| Field | Type | Description |
|-------|------|-------------|
| invocation_id | str | Unique invocation ID |
| skill_id | str | Skill invoked |
| step_id | str | Parent step |
| input | dict | Input parameters |
| output | dict | Output data |
| started_at | datetime | Start time |
| ended_at | datetime | End time |
| status | InvocationStatus | Success/failure |
| error | str | Error if failed |
| metrics | SkillMetrics | Performance metrics |

---

#### SkillMetrics
**Purpose:** Performance metrics for skill call

| Field | Type | Description |
|-------|------|-------------|
| duration_ms | int | Execution time |
| tokens_used | int | Tokens consumed |
| api_calls | int | External API calls |
| bytes_processed | int | Data processed |

---

#### RetryPolicy
**Purpose:** Retry configuration

| Field | Type | Description |
|-------|------|-------------|
| max_attempts | int | Maximum retry attempts |
| backoff_type | str | none/linear/exponential |
| base_delay_ms | int | Initial delay |
| max_delay_ms | int | Maximum delay |
| retryable_errors | list[str] | Errors to retry |

---

#### ToolAdapter
**Purpose:** External tool wrapper contract

| Field | Type | Description |
|-------|------|-------------|
| adapter_id | str | Unique adapter ID |
| tool_name | str | External tool name |
| protocol | str | Communication protocol |
| endpoint | str | Connection endpoint |
| auth_type | str | Authentication type |
| rate_limits | RateLimits | Rate limiting config |

---

## Sprint 06 — Workspace Maturity

**Goal:** Durable state and artifact management.

### Workspace Contracts

#### WorkspaceConfig
**Purpose:** Workspace-level configuration

| Field | Type | Description |
|-------|------|-------------|
| workspace_id | str | Workspace identifier |
| name | str | Display name |
| description | str | Description |
| default_playbook | str | Default playbook name |
| default_budgets | Budgets | Default budgets |
| default_constraints | Constraints | Default constraints |
| memory_enabled | bool | Memory store enabled |
| rag_enabled | bool | RAG enabled |
| created_at | datetime | Creation time |
| updated_at | datetime | Last update |

---

#### ArtifactIndex
**Purpose:** Artifact registry index entry

| Field | Type | Description |
|-------|------|-------------|
| artifact_id | str | Unique artifact ID |
| run_id | str | Producing run |
| workspace_id | str | Workspace scope |
| artifact_type | str | MIME type |
| path | str | Storage path |
| uri | str | artifact:// URI |
| size_bytes | int | File size |
| checksum | str | SHA256 |
| created_at | datetime | Creation time |
| tags | list[str] | User tags |
| metadata | dict | Additional metadata |

---

### Memory Contracts (Optional Module)

#### MemoryEntry
**Purpose:** Workspace-bounded memory entry

| Field | Type | Description |
|-------|------|-------------|
| entry_id | str | Unique entry ID |
| workspace_id | str | Workspace scope |
| entry_type | str | fact/summary/embedding |
| content | str | Memory content |
| source_run_id | str | Source run (optional) |
| relevance_score | float | Computed relevance |
| created_at | datetime | Creation time |
| expires_at | datetime | Expiration (optional) |

---

#### RetrievalQuery
**Purpose:** RAG retrieval query

| Field | Type | Description |
|-------|------|-------------|
| query_id | str | Unique query ID |
| workspace_id | str | Workspace scope |
| query_text | str | Query string |
| filters | dict | Metadata filters |
| top_k | int | Max results |
| min_score | float | Minimum relevance |

---

#### RetrievalResult
**Purpose:** RAG retrieval result

| Field | Type | Description |
|-------|------|-------------|
| result_id | str | Unique result ID |
| query_id | str | Source query |
| entries | list[MemoryEntry] | Retrieved entries |
| scores | list[float] | Relevance scores |
| latency_ms | int | Query latency |

---

## Sprint 07 — Interface Readiness

**Goal:** Stable internal API surface.

### API Contracts

#### APIRequest
**Purpose:** Normalized API request

| Field | Type | Description |
|-------|------|-------------|
| request_id | str | Unique request ID |
| method | str | HTTP method equivalent |
| path | str | Resource path |
| headers | dict | Request headers |
| body | dict | Request body |
| auth_context | AuthContext | Authentication context |

---

#### APIResponse
**Purpose:** Normalized API response

| Field | Type | Description |
|-------|------|-------------|
| request_id | str | Original request ID |
| status_code | int | HTTP status equivalent |
| headers | dict | Response headers |
| body | dict | Response body |
| latency_ms | int | Processing time |

---

#### EventSpec
**Purpose:** Incoming event (IoT/sensor/stream)

| Field | Type | Description |
|-------|------|-------------|
| event_id | str | Unique event ID |
| source_type | str | Source type |
| source_id | str | Source identifier |
| event_type | str | Event type |
| timestamp | datetime | Event timestamp |
| payload | dict | Event data |
| priority | int | Processing priority |

---

#### AuthContext
**Purpose:** Authentication context

| Field | Type | Description |
|-------|------|-------------|
| identity | str | User/service identity |
| auth_method | str | Authentication method |
| permissions | list[str] | Granted permissions |
| workspace_access | list[str] | Accessible workspaces |
| expires_at | datetime | Token expiration |

---

## Contract Dependencies

```
                    ┌─────────────────────────────────────┐
                    │           Sprint 07                 │
                    │   APIRequest, EventSpec, AuthCtx    │
                    └──────────────┬──────────────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────┐
│    Sprint 05    │    │      Sprint 06      │    │    Sprint 04    │
│   SkillSpec     │    │   WorkspaceConfig   │    │   Permission    │
│   ToolAdapter   │    │   MemoryEntry       │    │   PolicyRule    │
└────────┬────────┘    └──────────┬──────────┘    └────────┬────────┘
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │        Sprint 03          │
                    │   TraceEvent, Evidence    │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │        Sprint 02          │
                    │   AgentRole, Delegation   │
                    │   SubtaskSpec, StepGraph  │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │        Sprint 01          │
                    │   TaskSpec, RunTrace      │
                    │   Playbook (current)      │
                    └───────────────────────────┘
```

---

## Evolution Notes

### Backward Compatibility Strategy

| When | Strategy |
|------|----------|
| New optional fields | Add with defaults |
| New required fields | Version bump (0.1 → 0.2) |
| Schema changes | Create new version, deprecate old |
| Breaking changes | Major version only |

### Testing Strategy for New Contracts

Each new contract should have:
1. **Schema test** — Required fields, types, defaults
2. **Round-trip test** — JSON serialization lossless
3. **Evolution test** — Guardrail against field removal
4. **Integration test** — Works with existing contracts
5. **Builder test** — Builder pattern works

---

## Notes

- All future contracts follow the same patterns as Sprint 01
- Pydantic v2 with `extra="forbid"` policy
- Protocol interfaces for pluggable implementations
- Builder patterns for complex construction
- UTC timestamps, UUID identifiers
