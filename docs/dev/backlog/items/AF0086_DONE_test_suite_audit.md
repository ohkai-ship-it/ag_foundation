# BACKLOG ITEM — AF0086 — test_suite_audit
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - CI discipline (ruff + pytest -W error + coverage)
> - Test isolation
> - Warning-clean execution

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0086
- **Type:** Architecture / Testing
- **Status:** DONE
- **Priority:** P2
- **Area:** Testing
- **Owner:** Jacob
- **Target sprint:** Sprint 09
- **Depends on:** None

---

## Problem

The test suite has grown organically across sprints and now exhibits legacy patterns, inconsistencies, and potential redundancies.

### Observed Issues

#### 1. Legacy Test Patterns

Tests written in earlier sprints may use outdated patterns:
- Old fixture styles
- Deprecated mocking approaches (e.g., `duckduckgo_search.DDGS` → `ddgs.DDGS`)
- Inconsistent setup/teardown

#### 2. Test Naming Inconsistency

| Pattern | Examples | Issue |
|---------|----------|-------|
| `test_<feature>` | `test_cli.py` | Generic |
| `test_<module>_<feature>` | `test_cli_global_options.py` | Specific |
| `test_<concern>` | `test_contracts.py` | Abstract |
| Mixed in same file | Various | Hard to navigate |

#### 3. Test Organization

Current structure:
```
tests/
├── test_artifacts.py
├── test_cli.py
├── test_cli_global_options.py
├── test_cli_truthful.py
├── test_config.py
├── test_contracts.py
├── test_delegation.py
├── test_documentation_drift.py
├── test_e2e_integration.py
├── test_providers.py
├── test_research_skills.py
├── test_runtime.py
├── test_sanity.py
├── test_schema_verifier.py
├── test_skill_framework.py
├── test_storage.py
├── test_summarize_skills.py
└── test_web_search.py
```

**Issues:**
- Flat structure — no grouping by area (CLI, core, skills)
- Some files test multiple concerns
- Unclear which tests are unit vs integration vs e2e

#### 4. Fixture Inconsistency

Different tests create similar fixtures differently:
- Some use `@pytest.fixture` with `tmp_path`
- Some create workspaces inline
- Some mock providers, others don't
- Cleanup patterns vary

#### 5. Coverage Gaps vs Redundancy

- Some areas over-tested (multiple tests for same behavior)
- Some areas under-tested (gaps in edge cases)
- No clear test matrix showing coverage by component

#### 6. Known Test Issues

| Bug | Description | Status |
|-----|-------------|--------|
| BUG-0007 | OpenAI provider test isolation failure | OPEN |
| BUG-0012 | Test workspace cleanup pollution | OPEN |

#### 7. Warning Suppression

Some tests may be suppressing warnings that should be fixed:
- `pytest.mark.filterwarnings`
- Blanket exception handling hiding issues

---

## Goal

Conduct a **comprehensive test suite audit** to:

1. **Identify legacy patterns** — What needs modernization?
2. **Establish naming conventions** — Consistent test naming
3. **Propose organization** — Logical grouping (unit/integration/e2e)
4. **Standardize fixtures** — Common patterns, shared conftest.py
5. **Map coverage** — What's tested, what's missing?
6. **Clean up redundancy** — Remove duplicate tests
7. **Fix known issues** — BUG-0007, BUG-0012

---

## Non-goals (for this AF)

- Rewriting all tests (implementation in child AFs)
- Changing test framework (pytest stays)
- 100% coverage mandate

---

## Proposed Test Organization

### Directory Structure

```
tests/
├── conftest.py              # Shared fixtures
├── unit/                    # Fast, isolated unit tests
│   ├── conftest.py
│   ├── cli/
│   │   ├── test_commands.py
│   │   ├── test_global_options.py
│   │   └── test_output_formatting.py
│   ├── core/
│   │   ├── test_runtime.py
│   │   ├── test_run_trace.py
│   │   └── test_task_spec.py
│   ├── skills/
│   │   ├── test_base.py
│   │   ├── test_emit_result.py
│   │   ├── test_web_search.py
│   │   └── ...
│   ├── playbooks/
│   │   └── test_playbook_loading.py
│   └── storage/
│       ├── test_sqlite_store.py
│       └── test_workspace.py
├── integration/             # Component interaction tests
│   ├── conftest.py
│   ├── test_skill_pipeline.py
│   ├── test_playbook_execution.py
│   └── test_cli_to_runtime.py
├── e2e/                     # Full system tests
│   ├── conftest.py
│   ├── test_research_workflow.py
│   └── test_summarize_workflow.py
└── contracts/               # Contract/schema tests
    ├── test_schema_contracts.py
    ├── test_documentation_drift.py
    └── test_sanity.py
```

### Naming Convention

```python
# Unit tests: test_<behavior>_<condition>_<expected>
def test_emit_result_with_valid_input_writes_artifact():
def test_emit_result_without_workspace_returns_error():

# Integration tests: test_<component>_<interaction>
def test_research_pipeline_produces_report():

# E2E tests: test_<workflow>_<scenario>
def test_research_query_returns_formatted_result():
```

### Fixture Standards

```python
# conftest.py - shared fixtures

@pytest.fixture
def temp_workspace(tmp_path: Path) -> Path:
    """Create isolated workspace for testing."""
    ws = tmp_path / "test_workspace"
    ws.mkdir()
    (ws / "inputs").mkdir()
    (ws / "runs").mkdir()
    yield ws
    # Cleanup handled by tmp_path

@pytest.fixture
def mock_llm_provider():
    """Mock LLM provider for deterministic tests."""
    ...

@pytest.fixture
def skill_context(temp_workspace: Path) -> SkillContext:
    """Standard skill context for testing."""
    ...
```

### Test Markers

```python
@pytest.mark.unit          # Fast, isolated
@pytest.mark.integration   # Component interaction
@pytest.mark.e2e           # Full system
@pytest.mark.slow          # Long-running
@pytest.mark.network       # Requires network
@pytest.mark.llm           # Requires LLM provider
```

Usage:
```bash
pytest -m unit              # Run only unit tests
pytest -m "not slow"        # Skip slow tests
pytest -m "not network"     # Skip network tests
```

---

## Audit Checklist

### Per Test File

- [ ] Naming follows convention
- [ ] Single responsibility (one component/concern)
- [ ] Uses shared fixtures where appropriate
- [ ] No suppressed warnings without justification
- [ ] Cleanup handled properly
- [ ] Markers applied correctly

### Per Test Function

- [ ] Name describes behavior, condition, expected
- [ ] Single assertion focus (or related assertions)
- [ ] No magic numbers — use constants
- [ ] Mocks are scoped appropriately
- [ ] Edge cases covered

---

## Acceptance Criteria (High-Level)

- [x] Full test inventory documented
- [x] Legacy patterns identified with migration plan
- [x] Naming convention finalized
- [x] Directory structure proposal approved
- [x] Fixture standards documented
- [x] Coverage gaps identified
- [ ] Child AFs created for implementation (deferred to future sprint)

---

## Implementation Roadmap (Child AFs)

1. **AF-TBD: Test directory restructure** — Move to unit/integration/e2e structure
2. **AF-TBD: Fixture consolidation** — Shared conftest.py, standard fixtures
3. **AF-TBD: Test marker system** — Add markers, update CI
4. **AF-TBD: Legacy test migration** — Update old patterns
5. **AF-0071: Warning-clean test discipline** — Fix warnings (existing)
6. **AF-0046: Test isolation framework** — Fix isolation issues (existing)

---

## Related Items

| Item | Relationship |
|------|--------------|
| **AF-0046** | Test isolation framework (existing) |
| **AF-0071** | Warning-clean test discipline (existing) |
| **BUG-0007** | OpenAI provider test isolation |
| **BUG-0012** | Test workspace cleanup pollution |

---

## Open Questions

1. Should we migrate to the new structure incrementally or all-at-once?
2. How do we maintain test history (git blame) during restructure?
3. Should we add test generation for new skills (template)?
4. What's the minimum coverage threshold per component?

---

# Completion section

## 1) Metadata
- **Backlog item (primary):** AF0086
- **PR:** N/A (audit document)
- **Author:** Jacob
- **Date:** 2026-03-11
- **Branch:** feat/sprint09-reliability-safety-hardening
- **Risk level:** P2
- **Runtime mode used for verification:** N/A (audit document)

## 2) Test Suite Inventory (Sprint 09 Audit)

### Summary Statistics

| Metric | Value |
|--------|-------|
| Total tests | 448 |
| Test files | 18 |
| Test classes | 108 |
| Overall coverage | 86% |

### Tests Per File

| File | Tests | Classes | Fixtures |
|------|------:|--------:|---------:|
| test_schema_verifier.py | 44 | 8 | 0 |
| test_providers.py | 42 | 14 | 0 |
| test_cli.py | 40 | 8 | 0 |
| test_artifacts.py | 35 | 11 | 0 |
| test_contracts.py | 34 | 8 | 0 |
| test_runtime.py | 32 | 10 | 5 |
| test_research_skills.py | 31 | 5 | 0 |
| test_web_search.py | 29 | 0 | 0 |
| test_summarize_skills.py | 29 | 5 | 0 |
| test_skill_framework.py | 24 | 6 | 0 |
| test_storage.py | 23 | 5 | 4 |
| test_cli_truthful.py | 19 | 6 | 5 |
| test_config.py | 18 | 6 | 0 |
| test_cli_global_options.py | 13 | 6 | 0 |
| test_e2e_integration.py | 12 | 5 | 7 |
| test_delegation.py | 11 | 3 | 0 |
| test_documentation_drift.py | 8 | 2 | 2 |
| test_sanity.py | 6 | 0 | 0 |

### Coverage Gaps (< 90%)

| Module | Coverage | Gap Reason |
|--------|----------|------------|
| fetch_web_content.py | 54% | Network-dependent code paths |
| web_search.py | 61% | Network-dependent code paths |
| synthesize_research.py | 82% | LLM-dependent code paths |

### Findings

#### Positive Patterns ✅
1. **Good class organization** — 108 test classes across 18 files
2. **No warning suppressions** — Tests run cleanly with `-W error`
3. **High coverage** — 86% overall, most modules > 90%
4. **Consistent naming** — `test_<file>.py` pattern followed

#### Areas for Improvement 🔧
1. **No shared conftest.py** — Fixtures duplicated across files
2. **Minimal pytest markers** — Only 3 markers used (manual, parametrize, integration)
3. **Flat structure** — No unit/integration/e2e separation
4. **Fixture duplication** — 23 fixtures across 5 files, many similar

### Marker Usage (Current)

| Marker | Count | Files |
|--------|------:|-------|
| `@pytest.mark.manual` | 1 | test_e2e_integration.py |
| `@pytest.mark.parametrize` | 1 | test_e2e_integration.py |
| `@pytest.mark.integration` | 1 | test_providers.py |

### Recommendations

1. **Create shared conftest.py** with common fixtures:
   - `temp_workspace`
   - `mock_llm_provider`
   - `skill_context`

2. **Add markers systematically**:
   - `@pytest.mark.unit` — pure logic tests
   - `@pytest.mark.integration` — multi-component tests
   - `@pytest.mark.network` — requires internet (skip in CI)

3. **Consider directory restructure** (low priority):
   - Current flat structure is manageable at 18 files
   - Revisit when test count exceeds 600

4. **Improve network-dependent coverage**:
   - Add mocked tests for fetch_web_content.py
   - Add mocked tests for web_search.py

## 3) Resolved Related Items

| Item | Status | Relationship |
|------|--------|--------------|
| AF-0046 | ✅ DONE | Test isolation framework |
| AF-0071 | ✅ DONE | Warning-clean test discipline |
| BUG-0007 | ✅ FIXED | OpenAI provider test isolation |

## 4) Decision: Incremental Migration

**Approach:** Incremental improvements over restructure
- Current structure is workable
- Focus on conftest.py and markers first
- Full restructure deferred until test count grows
