# BACKLOG ITEM — AF#### — <three_word_description>
# Version number: v0.2

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - 1 PR = 1 primary AF
> - INDEX update rule (status ↔ filename integrity)

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF####
- **Type:** Foundation | Docs | Architecture | Feature | Refactor | Process
- **Status:** PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED
- **Priority:** P0 | P1 | P2
- **Area:** Docs | CLI | Kernel | Skills | Storage | Process | Testing | CI
- **Owner:** Kai | Jeff | Jacob
- **Target sprint:** Sprint## — <sprint_name>

---

## Problem
What’s missing / unclear? Why does it matter now?

---

## Goal
Concrete outcome(s). Must be verifiable.

---

## Non-goals
Explicitly out of scope.

---

## Acceptance criteria (Definition of Done)
- [ ] Deliverable exists in the correct folder (per `/docs/dev` structure)
- [ ] Naming conventions applied (file name + internal Status match)
- [ ] INDEX file(s) updated (ritual at sprint start AND on status change)
- [ ] CI/local checks pass (as applicable):  
  - [ ] `ruff check src tests`  
  - [ ] `ruff format --check src tests` (or `ruff format src tests`)  
  - [ ] `pytest -W error`  
  - [ ] coverage thresholds met (see TESTING_GUIDELINES)
- [ ] Evidence included (as applicable): tests + RunTrace ID(s)
- [ ] Completion section filled below (mandatory when Status = Done)

---

## Implementation notes
Be specific: files/folders touched, rename/move steps, invariants to keep true.

---

## Risks
What could go wrong? How to mitigate?

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF####
- **PR:** #<number>
- **Author:** <name>
- **Date:** YYYY-MM-DD
- **Branch:** <feat/... | fix/... | chore/...>
- **Risk level:** P0 | P1 | P2
- **Runtime mode used for verification:** llm | manual (dev/test-only)

---

## 2) Acceptance criteria verification
Copy the AC list from above and mark it.

- [ ] ...
- [ ] ...

---

## 3) What changed (file-level)
List each file changed and what changed in 1 line.

- `<path/to/file>` — ...
- `<path/to/file>` — ...

---

## 4) Architecture alignment (mandatory)
- **Layering:** where the logic lives and why (adapter vs core vs skill vs storage)
- **Interfaces touched:** TaskSpec / RunTrace / Planner / Orchestrator / Executor / Verifier / Recorder / Skill (specify)
- **Backward compatibility:** any contract/schema change? (yes/no + details)

---

## 5) Truthful UX check (mandatory when user-visible)
- **User-visible labels affected:** <list>
- **Trace fields backing them:** <exact fields>
- **Proof:** point to `ag runs show <run_id>` fields demonstrating truthfulness

---

## 6) Tests executed (mandatory unless docs-only)
Provide exact commands and results summary.

- Command: `...`
  - Result: PASS/FAIL (include failing test names if any)

---

## 7) Run evidence (mandatory for behavior changes)
- **RunTrace ID(s):** `run_...`
- **How to reproduce:** exact command(s)
  - `ag run ...`
- **Expected trace outcomes:** bullet list of fields/values a reviewer should see

---

## 8) Artifacts (if applicable)
- **Artifact IDs/URIs:** `artifact://...`
- **What they contain:** ...

---

## 9) Risks, tradeoffs, follow-ups
- **Risks introduced:** ...
- **Tradeoffs made:** ...
- **Follow-up items to create:** AF-____ / BUG-____ / ADR-___

---

## 10) Reviewer checklist (copy/paste)
- [ ] I can map PR → AF item and see acceptance criteria satisfied
- [ ] I can verify truthful labels from RunTrace
- [ ] I can reproduce a run (or it’s docs-only)
- [ ] Tests were run and results are documented
- [ ] Any contract changes are documented in cornerstone docs
