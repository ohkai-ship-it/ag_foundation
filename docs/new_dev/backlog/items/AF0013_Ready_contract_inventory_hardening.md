# AF0013 — Contract inventory hardening: reconcile docs ↔ implementation and add consistency checks
# Version number: v0.2

## Metadata
- **ID:** AF-0013
- **Type:** Docs/Quality
- **Status:** Ready
- **Priority:** P1
- **Area:** Contracts
- **Owner:** Jacob
- **Target sprint:** Sprint 02

## Problem
The contract inventory is becoming a system-of-record, but it currently contains discrepancies (missing interfaces, naming mismatches, enum/example drift). This can cause reviewer distrust and mis-implementation.

## Goal
Make contract documentation reliably reflect reality by (1) reconciling discrepancies via a small audit, and (2) adding lightweight automated checks that prevent future drift.

## Non-goals
- Introducing new runtime features unrelated to contract consistency.
- Large refactors of core modules.
- Heavy doc generation frameworks.

## Acceptance criteria (Definition of Done)
- [ ] An audit note is added describing for each discrepancy whether it was (a) implemented but undocumented, or (b) not implemented.
- [ ] CONTRACT_INVENTORY.md is updated to reflect actual implementation (or explicitly marked TODO with a follow-up AF id).
- [ ] At least one automated guard is added (test or script) to catch obvious drifts, e.g.:
  - enum values referenced in examples must exist
  - required core Protocols count matches architecture (or explicit rationale if not)
  - storage file name in docs matches code constant/config
- [ ] Guard runs in CI and fails on drift.
- [ ] Review entry references the updated inventory as canonical for Sprint 02 onward.

## Implementation notes
- Start with grep + quick code inspection. Treat docs as untrusted until verified.
- Prefer `tests/test_docs_consistency.py` with small assertions.
- Keep AF-0013 docs/consistency focused; code fixes go to AF-0014..0016.

## Risks
Low/Medium: risk of scope creep. Mitigate by limiting to the known drifts (Recorder, DB filename, enum/example, artifact field semantics).

## PR plan
1. PR (chore/contracts-inventory): Audit discrepancies, update CONTRACT_INVENTORY.md, add minimal consistency tests.

---
# Completion section (fill when done)

Pending completion.
