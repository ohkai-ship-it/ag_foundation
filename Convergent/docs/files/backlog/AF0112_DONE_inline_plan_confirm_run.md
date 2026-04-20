# AF-0112 — Inline plan preview and confirm in ag run
# Version number: v0.1
# Created: 2026-03-21
# Status: DONE
# Priority: P1
# Area: CLI/Runtime/Planner

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

---

## Summary

Make `ag run "prompt"` the single entry point for guided autonomy. The command generates a plan, displays it inline, and asks the user to confirm before executing — all in one step. No more copy-pasting plan IDs.

---

## Problem

The current guided autonomy workflow requires three steps:

```
ag plan generate --task "Research Tokyo trends"   # step 1: generate
# user reads output, copies plan_abc123            # step 2: copy
ag run --plan plan_abc123                          # step 3: run
```

This is clumsy: the user must context-switch between commands, manually copy a plan ID, and the "guided" experience feels like a developer workflow rather than an intuitive approval gate.

**Principle:** Guided autonomy should feel like one decision point, not a multi-command ceremony.

---

## Proposed UX

### Default flow (single command):
```
> ag run "Research Tokyo population trends"

Planning...

  Plan: plan_7f3a2b1c
  Steps (4):
    1. web_search        → search for "Tokyo population trends"
    2. fetch_web_content  → retrieve top results
    3. synthesize_research → compile findings
    4. emit_result        → write report (Markdown)

  Confidence: 0.85
  Estimated tokens: ~5500

  Execute this plan? [Y/n] _
```

- **Y / Enter** → executes immediately, plan stored under run artifacts
- **n** → aborts, plan discarded (or optionally saved)

### Flags:
| Flag | Behavior |
|------|----------|
| `--yes` / `-y` | Auto-approve, skip confirmation (scripting/CI) |
| `--dry-run` | Show plan summary and exit (replaces `ag plan generate` for quick inspection) |
| `--plan <id>` | Existing behavior: execute a previously saved plan (unchanged) |

### Power-user flow preserved:
```
ag plan generate --task "..."    # save plan for later (still works)
ag plan list                      # browse saved plans
ag run --plan plan_abc123         # run a saved plan (still works)
```

---

## Scope

### Must change
- [x] `ag run` default path: call V1Planner → display plan summary → prompt for confirmation → execute
- [x] Add `--yes` / `-y` flag to `ag run` (auto-approve)
- [x] Add `--dry-run` flag to `ag run` (show plan, exit)
- [x] Plan display formatting: steps table, confidence, estimated tokens
- [x] Plan stored under run artifacts on execution (consistent with AF-0110 layout)

### Must preserve
- [x] `ag run --plan <id>` path unchanged (backward compatible)
- [x] `ag plan generate` still works for save-now-run-later
- [x] `--playbook` flag still works for V0Planner / explicit playbook selection
- [x] Non-interactive mode: `--yes` must not hang on missing stdin

### Out of scope
- Step-level confirmation during execution (already in AF-0100)
- Plan editing / step modification before approval
- Fuzzy plan matching or plan history search

---

## Acceptance criteria

- [x] `ag run "prompt"` shows plan and prompts for confirmation
- [x] Pressing Enter or Y executes the plan
- [x] Pressing n aborts without execution
- [x] `ag run -y "prompt"` executes without prompting
- [x] `ag run --dry-run "prompt"` prints plan and exits with code 0
- [x] `ag run --plan <id>` works exactly as before
- [x] Plan summary includes: step count, skill names, confidence, estimated tokens
- [x] Plan is persisted under run artifacts after execution
- [x] `--json` mode outputs plan as JSON (no interactive prompt)
- [x] Tests cover: confirm path, reject path, --yes path, --dry-run path, --plan path

---

## Implementation notes

- Modified `src/ag/cli/main.py`: added inline plan flow in the default `ag run` path
- `--mode manual` bypasses V1Planner (no LLM needed in manual mode)
- `--dry-run` + `--plan` are mutually exclusive
- `--json` mode auto-approves (no interactive prompt), outputs plan JSON for dry-run or trace JSON for execution
- Plan stored as `plan.json` artifact under run (AF-0110 layout)
- Autonomy metadata set to `GUIDED` with inline plan ID
- 7 contract tests in `tests/test_contracts.py::TestInlinePlanConfirmRun`
- 697 tests pass, ruff clean
