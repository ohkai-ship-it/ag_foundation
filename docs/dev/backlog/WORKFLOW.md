# Backlog Workflow (ag_foundation)
# Version number: v0.1

This document defines how backlog items (AF-000x) translate into PRs and evidence.

## Core rules (strict)
1) **One PR = one primary AF item.**
   - A PR may reference secondary AF items, but only one primary.
2) **Every AF item must define acceptance criteria.**
3) **Every behavior change PR must include evidence:**
   - tests results, and
   - at least one RunTrace ID (unless docs-only)
4) **Completion note is mandatory for merged PRs.**
   - Use the strict template in `/docs/dev/backlog/templates/COMPLETION_NOTE_TEMPLATE.md`.

---

## AF item lifecycle
Statuses (recommended):
- Proposed → Ready → In progress → Done
- (Optional) Blocked / Dropped

### Definition
- **Proposed:** idea exists, not yet refined
- **Ready:** scoped with clear goal + acceptance criteria + expected PR slicing
- **In progress:** at least one PR open
- **Done:** acceptance criteria met and merged, evidence captured

---

## Required fields in every AF item
- Problem
- Goal
- Non-goals
- Acceptance criteria (DoD)
- PR plan (expected slices)
- Risks

---

## PR mapping
### In the AF item
Include:
- **Expected PR:** `feat/...` (title)
- What AC each PR satisfies
- Evidence expectation (tests + run traces)

### In the PR (GitHub)
Use the PR template and include:
- Primary AF id
- Tests run
- RunTrace id(s)
- Link to completion note

---

## Evidence standards
### When to include a RunTrace ID
- Always for behavior changes (planner/orchestrator/executor/verifier/recorder/CLI output)
- Not required for docs-only PRs

### Manual mode usage
Manual mode (dev/test-only) is encouraged for fast verification runs, but:
- must be clearly labeled in the RunTrace
- must remain gated from end users

---

## Completion notes (mandatory)
After the PR is ready to merge (or immediately after merge), create a completion note MD file:
- Fill every section
- Include file-level diffs, tests, run evidence, and reviewer checklist
- Link it in the PR

---

## Multi-PR AF items
If an AF item needs multiple PRs:
- keep the AF item status as **In progress** until all AC are met
- each PR still has exactly one primary AF item (the same one)
- mark partial completion in AF item notes
