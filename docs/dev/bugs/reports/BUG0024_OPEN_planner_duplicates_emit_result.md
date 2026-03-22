# BUG REPORT — BUG-0024 — Planner duplicates emit_result
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - INDEX update rule (status ↔ filename integrity)
> - Evidence capture requirement (RunTrace ID for CLI/runtime bugs)

> **File naming (required):** `BUG####_<STATUS>_<three_word_description>.md`
> Status values: `OPEN | IN_PROGRESS | FIXED | VERIFIED | DROPPED`

---

## Metadata
- **ID:** BUG-0024
- **Status:** OPEN
- **Severity:** P2
- **Area:** Core Runtime / Planner
- **Reported by:** Kai
- **Date:** 2026-03-22
- **Related backlog item(s):** AF-0103 (V2Planner playbooks as plan steps), AF-0121 (V3Planner)
- **Related ADR(s):** —
- **Related PR(s):** —

---

## Summary

When the V2Planner or V3Planner selects a PLAYBOOK step (e.g. `research_v0`) as part
of a plan, it sometimes also adds a standalone `emit_result` skill step after it.
This results in two output artifacts being produced: one from the playbook's own
internal `emit_result` step (executed during playbook expansion by V1Orchestrator)
and a second from the planner-added standalone step. The user receives duplicate
output artifacts for a single run.

---

## Expected behavior

When a plan contains a PLAYBOOK step, no standalone `emit_result` step should be
added after it. A playbook is a self-contained, tested skill sequence that already
produces its own output. Adding an extra `emit_result` after a playbook is redundant
and produces a confusing duplicate artifact.

---

## Actual behavior

The LLM-generated plan contains both a `research_v0` playbook step and a trailing
`emit_result` skill step:

```
Proposed execution:
┏━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ #   ┃ Skill       ┃ Est. Tokens ┃ ...   ┃
┡━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1   │ research_v0 │        ~500 │ ...   │
│ 2   │ emit_result │        ~500 │ ...   │
└─────┴─────────────┴─────────────┴───────┘
```

After execution, two artifacts are created:
1. `research_report.md` (from `research_v0`'s internal `emit_result` step)
2. A second artifact from the planner-added `emit_result` step

---

## Reproduction steps

1. Run a task that causes the planner to select `research_v0`:
   `ag run "Wetterbericht Düsseldorf from web. Only use playbooks. Create an md file"`
2. Approve the plan
3. Observe: the plan table shows `research_v0` followed by `emit_result`
4. After completion, check artifacts: `ag artifacts list --workspace ws01`
5. Observe: two output artifacts for the single run

---

## Evidence

- **RunTrace ID:** `9bfab745-0152-4178-8ceb-af28e0c20d1c`
- **CLI output:** See "Actual behavior" above
- **Environment:** Windows 11, Python 3.14.0a6, Sprint 15 branch

---

## Impact

Users receive duplicate output artifacts and may be confused about which result to
use. In cases where `emit_result` is destructive (e.g. overwrites a previous file),
the second write may corrupt or overwrite the playbook's correctly-produced output.
Token budget is also wasted on a redundant step.

---

## Root cause

The V2Planner and V3Planner system prompts instruct the LLM to prefer playbooks when
they match the task, and to mix playbooks and individual skills. However, neither
prompt contains any instruction about the internal structure of playbooks. The LLM
has no way to know that `research_v0` (and `summarize_v0`) already contain an
`emit_result` step as their final internal step. When the user's prompt explicitly
asks for output ("Create an md file"), the LLM correctly infers that output should be
produced and adds `emit_result` — not knowing this is already handled within the
chosen playbook.

The planner has no post-generation validation step that checks for this redundancy.

---

## Acceptance criteria

- [ ] A plan containing a PLAYBOOK step does not include a trailing standalone
  `emit_result` step
- [ ] Plans with only skill steps (no PLAYBOOK steps) are unaffected and may still
  include `emit_result`
- [ ] `ag artifacts list` after a playbook-based run shows exactly one output artifact
  per run (not two)
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes

---

## Notes

This bug is specific to plans that mix PLAYBOOK steps with post-hoc skill steps. It
does not affect plans composed entirely of individual skills (where `emit_result` is
the correct and only way to produce output).

The set of playbooks that contain internal `emit_result` steps currently includes:
- `research_v0` (step 4: `emit_result`)
- `summarize_v0` (step 2: `emit_result`)

Any new playbooks that follow the same pattern would be subject to the same issue.

---

## Status log
- 2026-03-22 — Opened by Kai (reproduced with run `9bfab745`)
