# BACKLOG ITEM — AF0099 — plan_approval_workflow
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
- **ID:** AF0099
- **Type:** Feature
- **Status:** READY
- **Priority:** P1
- **Area:** CLI / Core Runtime
- **Owner:** TBD
- **Target sprint:** Sprint 11 — guided_autonomy_enablement
- **Depends on:** AF-0098 (plan preview command)

---

## Problem

AF-0098 generates execution plans, but there's no way to actually run them.
The guided autonomy workflow requires:

1. Generate plan → Review → Approve → Execute

Without a plan execution path, the preview is useless.

---

## Goal

Implement `ag run --plan <plan_id>` to execute a previously generated plan:

```bash
# Step 1: Generate plan (AF-0098)
ag plan --task "Research Berlin history" --workspace demo
# Output: Plan ID: plan_abc123

# Step 2: Review plan
ag plan show plan_abc123

# Step 3: Execute approved plan
ag run --plan plan_abc123
```

Execution behavior:
- Loads saved plan from workspace
- Validates plan not expired
- Validates workspace unchanged (optional: warn if modified)
- Executes plan steps in order
- Records in trace that execution was from approved plan
- Removes plan after successful execution

---

## Non-goals

- Plan modification before execution (plans are immutable)
- Partial plan execution (all or nothing)
- Plan chaining or composition
- Plan sharing across workspaces

---

## Acceptance criteria (Definition of Done)

- [ ] `ag run --plan <plan_id>` executes saved plan
- [ ] Expired plans rejected with clear error message
- [ ] Trace includes `plan_id` field linking to original plan
- [ ] Plan removed from storage after successful execution
- [ ] Failed execution preserves plan for retry (configurable)
- [ ] `--plan` and `--task` are mutually exclusive (error if both provided)
- [ ] Tests cover: valid plan, expired plan, missing plan, execution failure
- [ ] CI passes

---

## Implementation notes

### CLI changes
- Add `--plan <plan_id>` option to `ag run`
- Mutually exclusive with `--task` and `--playbook`
- Plan ID validated before execution starts

### Runtime changes
- New execution path: load plan → validate → execute steps
- Trace metadata includes `plan_id` and `plan_approved_at`
- Plan execution uses same runtime as direct execution

### Plan lifecycle
```
PENDING → EXECUTING → COMPLETED
                   ↘ FAILED (preserved for retry)
        → EXPIRED (auto-cleanup)
        → DELETED (manual)
```

### Storage
- Plan status updated during execution
- `executed_at` timestamp recorded
- Link between run trace and plan preserved

---

## Risks

| Risk | Mitigation |
|------|------------|
| Plan state becomes inconsistent | Use transactions, validate state before execution |
| Workspace changed since plan | Add optional `--force` flag, warn by default |
| Plan execution diverges from plan | Log deviations in trace, don't allow skill substitution |

---

# Completion section (fill when done)

_To be filled upon completion_
