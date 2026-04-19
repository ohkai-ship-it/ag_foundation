# AF0005 — Contracts: TaskSpec + RunTrace + Playbook schemas v0.1 + builders + contract tests
# Version number: v0.3

## Metadata
- **ID:** AF-0005
- **Type:** Foundation
- **Status:** DONE
- **Priority:** P0
- **Area:** Kernel
- **Owner:** Jeff
- **Completed in:** Sprint 01
- **Completion date:** 2026-02-24

## Problem
Truthful UX and evidence rules require explicit contracts. Prior wording didn't lock down required fields (e.g., playbook preference) or the contract-test strategy (evolution, serialization, stability).

## Goal
Define v0.1 schemas for TaskSpec, RunTrace, and a minimal Playbook; add builders and contract tests so runtime/CLI are unambiguous and forward-compatible.

## Non-goals
- Full workflow engine schema.
- Retrieval/RAG evidence bundle.
- Telemetry export.

## Acceptance criteria (Definition of Done)
- [x] TaskSpec v0.1 includes at minimum: `task_spec_version`, `prompt`, `workspace_id`, `mode`, `playbook_preference`, `budgets`, `constraints`.
- [x] RunTrace v0.1 includes at minimum: `trace_version`, `run_id`, timestamps, `workspace_id`, `mode`, playbook metadata, `steps[]`, `artifacts[]`, `verifier`, `final`.
- [x] Playbook v0.1 schema exists (minimal): `name`, `version`, `reasoning_modes`, `budgets`, `steps[]` (linear sequence).
- [x] Contract tests cover: JSON round-trip, version fields present, additive evolution guardrails (no removals/renames within v0), and stable defaults.
- [x] Schema versioning strategy is documented (or ADR referenced) and enforced by tests.

## Implementation notes
- Use Pydantic (or equivalent).
- Additive-only policy for v0.
- Align fields with CLI truthful labels (mode, verifier.status, timings).

## Risks
P1: schema churn. Mitigate with explicit v0.1 scope + ADR-0002 + contract tests.

## PR plan
1. PR (feat/contracts): Implement schemas + builders + contract tests; update docs/examples if needed.

---
# Completion section (fill when done)

**Completion date:** 2026-02-24  
**Author:** Jacob (Junior Engineer)

**Summary:**
Implemented v0.1 schemas for TaskSpec, RunTrace, and Playbook with Pydantic models, builders for fluent construction, and comprehensive contract tests ensuring JSON round-trip stability and additive evolution guardrails.

**What Was Done:**

1. **TaskSpec v0.1** (`src/ag/core/task_spec.py`)
   - TaskSpec model with required fields: `prompt`, `workspace_id`
   - `task_spec_version` field (default "0.1")
   - ExecutionMode enum: `manual`, `supervised`, `autonomous`
   - Budgets and Constraints models
   - TaskSpecBuilder for fluent construction
   - JSON serialization

2. **RunTrace v0.1** (`src/ag/core/run_trace.py`)
   - RunTrace model with required fields: `run_id`, `workspace_id`, `started_at`
   - `trace_version` field (default "0.1")
   - Supporting models: Step, Artifact, PlaybookMetadata, Verifier, FinalStatus
   - RunTraceBuilder for fluent construction

3. **Playbook v0.1** (`src/ag/core/playbook.py`)
   - Playbook model: `name`, `version`, `reasoning_modes`, `budgets`, `steps[]`
   - PlaybookStep model, PlaybookStepType enum, ReasoningMode enum
   - PlaybookBuilder for fluent construction

4. **Contract Tests** (`tests/test_contracts.py`)
   - 21 tests covering version fields, required fields, JSON round-trip, stable defaults, builders, additive evolution

**Test Results:** 21 passed

