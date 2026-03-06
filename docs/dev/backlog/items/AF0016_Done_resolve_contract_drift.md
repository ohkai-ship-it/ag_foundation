# AF0016 — Resolve contract drift: ReasoningMode enum vs examples; Artifact path vs uri semantics
# Version number: v0.2

## Metadata
- **ID:** AF-0016
- **Type:** Quality
- **Status:** DONE
- **Priority:** P2
- **Area:** Contracts
- **Owner:** Jacob
- **Completed in:** Sprint 02
- **Completion date:** 2026-02-26

## Problem
Contract inventory contains internal inconsistencies: examples reference `ReasoningMode.BALANCED` but enum lists other values; artifact reference is described as `path` but elsewhere as `uri`. These drifts create ambiguity and can leak into CLI truth labels and future APIs.

## Goal
Determine the implemented truth (enum values and artifact field semantics) and reconcile docs + code to a single canonical contract.

## Non-goals
- Expanding reasoning system beyond v0 needs.
- Remote artifact storage.
- Complex URI resolvers.

## Acceptance criteria (Definition of Done)
- [x] Audit: confirm actual `ReasoningMode` enum values in code and usage sites (playbooks/tests).
- [x] If BALANCED is intended/used: add it to enum and make docs/tests consistent.
- [x] If BALANCED is not intended: remove/replace in docs/examples and ensure defaults match enum.
- [x] Audit artifact reference: confirm whether field is `path`, `uri`, or both; define canonical meaning (local path vs artifact:// URI).
- [x] Update models and CLI rendering to use canonical field(s).
- [x] Add/adjust contract tests asserting canonical enum values and artifact reference field naming.
- [x] Update CONTRACT_INVENTORY.md so no example references non-existent enum values.

## Implementation notes
- Keep v0 simple: one default mode is OK.
- If adopting `uri`, use `artifact://` workspace-relative scheme.
- Prefer additive changes within v0.1.

## Risks
Low/Medium: contract changes ripple into tests. Mitigate by updating contract tests first and keeping changes additive where possible.

## PR plan
1. PR (chore/contracts-reconcile): Audit enum + artifact fields; update code/docs/tests to consistent contracts.

---
# Completion section (fill when done)

**Completion date:** 2026-02-26  
**Author:** Jacob

**Summary:**
Audit confirmed ReasoningMode enum has values: NONE, MINIMAL, DIRECT, EXTENDED (no BALANCED). Fixed documentation to match actual implementation.

**Audit Results:**
- ReasoningMode enum: NONE, MINIMAL, DIRECT, EXTENDED — no BALANCED exists
- Artifact reference: uses `path` field (local path semantics)

**What Changed:**
- `docs/dev/reviews/entries/REVIEW_S01_2026-02-24/CONTRACT_INVENTORY.md` — Fixed example from `ReasoningMode.BALANCED` to `ReasoningMode.DIRECT`

**Architecture Alignment:**
- Documentation only; no code changes
- ReasoningMode enum documented, not changed

**Tests Executed:**
- pytest tests/test_schemas.py -k ReasoningMode: PASS
- pytest tests/: PASS (173 passed)

