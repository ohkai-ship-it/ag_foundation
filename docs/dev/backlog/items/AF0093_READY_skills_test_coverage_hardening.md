# BACKLOG ITEM — AF0093 — skills_test_coverage_hardening
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - CI discipline (ruff + pytest -W error + coverage)
> - INDEX update rule (status ↔ filename integrity)

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0093
- **Type:** Quality / Testing
- **Status:** READY
- **Priority:** P2
- **Area:** Skills / Testing
- **Owner:** TBD
- **Target sprint:** Sprint 10
- **Depends on:** AF-0086 (test suite audit — DONE)

---

## Context

AF-0086 (Sprint 09) audited the test suite and found significant coverage
gaps in network-dependent skill modules:

| Module | Coverage | Gap |
|--------|----------|-----|
| `fetch_web_content` | 54% | Error paths, timeout, content extraction |
| `web_search` | 61% | Provider fallback, rate limiting, result parsing |
| `synthesize_research` | 82% | Edge cases, multi-source synthesis |

These are the three lowest-coverage modules in the codebase (overall 86%).
All three are network-dependent skills that require careful mocking to test.

AF-0086 proposed child AFs for test restructuring but none were created.
This AF addresses the most critical gap: skill test coverage.

---

## Problem

Network-dependent skills have the lowest test coverage in the codebase.
These skills handle external data and are most likely to fail in production.
Low coverage means:
- Bugs in error handling go undetected
- Refactoring these skills is risky
- Gate B readiness requires confidence in skill reliability

---

## Goal

Raise test coverage for the three weakest skill modules to ≥80% each,
focusing on error paths, edge cases, and network failure scenarios.

---

## Non-goals

- Test directory restructuring (AF-0086 child AF, not urgent)
- Test fixture consolidation (AF-0086 child AF, not urgent)
- Test marker system (nice-to-have, not blocking)
- Coverage for non-skill modules (already adequate)

---

## Scope

### 1. `fetch_web_content` (54% → ≥80%)
- Mock HTTP responses for success, error, timeout
- Test content extraction from HTML (various structures)
- Test encoding detection edge cases
- Test URL validation and sanitization

### 2. `web_search` (61% → ≥80%)
- Mock search provider responses
- Test provider fallback behavior
- Test rate limiting / retry logic
- Test result parsing and ranking

### 3. `synthesize_research` (82% → ≥90%)
- Test multi-source synthesis with conflicting data
- Test empty source handling
- Test maximum context handling
- Test output format consistency

### 4. Test Infrastructure
- Ensure all new tests use proper mocking (no real network calls)
- Add `@pytest.mark.unit` markers where appropriate
- All tests must pass with `pytest -W error`

---

## Key Files

| File | Role |
|------|------|
| `src/ag/skills/fetch_web_content.py` | Web fetch skill |
| `src/ag/skills/web_search.py` | Web search skill |
| `src/ag/skills/synthesize_research.py` | Research synthesis skill |
| `tests/test_research_skills.py` | Existing skill tests |
| `tests/test_skill_framework.py` | Skill framework tests |

---

## Acceptance criteria (Definition of Done)

- [ ] `fetch_web_content` coverage ≥ 80%
- [ ] `web_search` coverage ≥ 80%
- [ ] `synthesize_research` coverage ≥ 90%
- [ ] All new tests use mocking (no network calls)
- [ ] No regression in existing tests
- [ ] `ruff check src tests` passes
- [ ] `pytest -W error` passes
- [ ] Coverage report generated and reviewed

---

## Risks

| Risk | Mitigation |
|------|------------|
| Complex mock setup needed | Use existing mock patterns from test_research_skills.py |
| Skill internals may change during sprint | Coordinate with AF-0090 if skills are refactored |
| Coverage % targets too ambitious | 80% is reasonable floor; adjust if blocked |

---

## Related Items

- **AF-0086:** Test suite audit (parent audit — identified these gaps) — DONE
- **AF-0090:** Evidence capture (may touch skill execution paths)
- **AF-0084:** Research framework refactor (may change skill interfaces)
