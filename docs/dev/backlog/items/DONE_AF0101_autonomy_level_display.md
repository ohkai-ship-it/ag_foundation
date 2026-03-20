# BACKLOG ITEM — AF0101 — autonomy_level_display
# Version number: v0.1

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
- **ID:** AF0101
- **Type:** Feature
- **Status:** READY
- **Priority:** P3
- **Area:** CLI / Core Runtime / Trace
- **Owner:** TBD
- **Target sprint:** Sprint 11 — guided_autonomy_enablement
- **Depends on:** —

---

## Problem

As we introduce guided autonomy (AF-0098, AF-0099, AF-0100), users need to
understand what autonomy mode they're operating in. Currently there's no
visibility into:

1. Whether a run used a pre-approved plan or direct execution
2. What confirmation policies were active
3. The "autonomy level" of the execution

This violates truthful UX — users should know HOW the system is operating.

---

## Goal

Display autonomy mode in CLI output and record in trace:

**CLI output:**
```
ag run --task "Research Berlin" --workspace demo

╭─────────────────────────────────────────────────────────╮
│ Run: run_abc123                                         │
│ Mode: guided (plan approval required)                   │
│ Confirmation: enabled (external_api, llm_call_large)    │
╰─────────────────────────────────────────────────────────╯

Executing step 1/4: web_search...
```

**Trace recording:**
```json
{
  "run_id": "run_abc123",
  "autonomy": {
    "mode": "guided",
    "plan_id": "plan_xyz789",
    "confirmation_policy": {
      "enabled": true,
      "flags": ["external_api", "llm_call_large"]
    }
  }
}
```

---

## Non-goals

- Autonomy mode switching during execution
- User-selectable autonomy levels (determined by config/workflow)
- Detailed policy explanations in CLI (keep it concise)

---

## Acceptance criteria (Definition of Done)

- [ ] CLI run output shows autonomy mode in header
- [ ] Autonomy modes defined: `playbook`, `guided`, `direct`
- [ ] `ag run --plan` shows "guided" mode
- [ ] `ag run --task` shows "direct" mode (or "playbook" if using playbook)
- [ ] Confirmation policy summary shown when enabled
- [ ] Trace includes `autonomy` object with mode and policy
- [ ] `ag runs show <id>` displays autonomy info
- [ ] Tests verify autonomy metadata in trace
- [ ] CI passes

---

## Implementation notes

### Autonomy modes

| Mode | Description | Trigger |
|------|-------------|---------|
| `playbook` | Executing predefined playbook | `--playbook` flag or playbook-routed task |
| `guided` | Executing pre-approved plan | `--plan` flag |
| `direct` | Immediate execution, no plan | `--task` without plan |

### CLI display
- Header box shows mode and key policy info
- Keep concise — details available via `ag runs show`
- Color coding: guided=yellow, direct=default, playbook=blue

### Trace schema addition
```python
class AutonomyMetadata(TypedDict):
    mode: Literal["playbook", "guided", "direct"]
    plan_id: str | None  # if guided mode
    confirmation_policy: ConfirmationPolicySnapshot | None
```

### Backwards compatibility
- `autonomy` field is additive (old traces won't have it)
- Default to `direct` mode for legacy runs

---

## Risks

| Risk | Mitigation |
|------|------------|
| Mode confusion | Clear documentation, consistent terminology |
| Display clutters output | Keep header minimal, details in `runs show` |

---

# Completion section (fill when done)

_To be filled upon completion_
