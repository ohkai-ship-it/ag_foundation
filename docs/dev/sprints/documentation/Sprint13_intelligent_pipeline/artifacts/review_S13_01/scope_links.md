# Sprint 13 Review - Scope Links

## AF Files Status

| AF | Title | Status | Location |
|----|-------|--------|----------|
| AF-0114 | Extract V0 / V1 classes as stable API | DONE | [🔗](../../../../../backlog/items/AF0114_DONE_extract_v0_classes.md) |
| AF-0115 | V1Verifier (evidence-based acceptance) | DONE | [🔗](../../../../../backlog/items/AF0115_DONE_v1_verifier.md) |
| AF-0103 | V2Planner (playbook-aware LLM planner) | DONE | [🔗](../../../../../backlog/items/AF0103_DONE_v2_planner.md) |
| AF-0117 | V1Orchestrator (plan-driven execution) | DONE | [🔗](../../../../../backlog/items/AF0117_DONE_v1_orchestrator.md) |

## Implementation Locations

| Component | File | Purpose |
|-----------|------|---------|
| V0Planner | [planner.py](../../../../../../../src/ag/core/planner.py) | Original LLM planner (extracted) |
| V1Planner | [planner.py](../../../../../../../src/ag/core/planner.py) | Validation-based planner (extracted) |
| V2Planner | [planner.py](../../../../../../../src/ag/core/planner.py) | Playbook-aware planner (new in Sprint 13) |
| V0Orchestrator | [orchestrator.py](../../../../../../../src/ag/core/orchestrator.py) | Original step executor (extracted) |
| V1Orchestrator | [orchestrator.py](../../../../../../../src/ag/core/orchestrator.py) | Mixed plan executor (new in Sprint 13) |
| V0Verifier | [verifier.py](../../../../../../../src/ag/core/verifier.py) | Original pass/fail verifier (extracted) |
| V1Verifier | [verifier.py](../../../../../../../src/ag/core/verifier.py) | Evidence-based verifier (new in Sprint 13) |
| PlaybookStepType.PLAYBOOK | [playbook.py](../../../../../../../src/ag/core/playbook.py) | New step type for playbook refs |

## Test Locations

| Test Class | File | Coverage |
|------------|------|----------|
| TestV2PlannerPlaybookAwareness | [test_planner.py](../../../../../../../tests/test_planner.py) | 7 tests for V2Planner |
| TestV1OrchestratorMixedPlans | [test_planner.py](../../../../../../../tests/test_planner.py) | 6 tests for V1Orchestrator |
| TestV1VerifierEvidenceCollection | [test_runtime.py](../../../../../../../tests/test_runtime.py) | V1Verifier evidence tests |

## INDEX File
- [INDEX_AF.md](../../../../../backlog/INDEX_AF.md) - Updated with all DONE statuses
