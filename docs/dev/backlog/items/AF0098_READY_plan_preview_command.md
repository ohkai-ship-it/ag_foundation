# BACKLOG ITEM — AF0098 — plan_preview_command
# Version number: v0.3

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
- **ID:** AF0098
- **Type:** Feature
- **Status:** READY
- **Priority:** P1
- **Area:** CLI / Core Runtime / Planner
- **Owner:** TBD
- **Target sprint:** Sprint 11 — guided_autonomy_enablement
- **Depends on:** AF-0102 (V1Planner — LLM-based skill composition)

---

## Problem

Currently, `ag run` immediately executes tasks without allowing users to preview
what the system intends to do. This is a barrier to guided autonomy because:

1. Users cannot review proposed execution plans before committing
2. No opportunity to catch suboptimal skill selections
3. No cost/token estimates before LLM calls
4. Cannot identify policy-flagged steps in advance

For guided autonomy, users need to see WHAT the system proposes before it does it.

---

## Goal

Implement `ag plan` command that generates and displays a proposed execution
plan without executing it:

```bash
ag plan --task "Research the history of Berlin" --workspace demo
```

Output:
```
Plan ID: plan_abc123
Task: Research the history of Berlin
Workspace: demo
Generated: 2026-03-13T10:30:00Z
Expires: 2026-03-13T11:30:00Z (1 hour)

Proposed execution:
┌────┬──────────────────────┬─────────────┬──────────────┬─────────┐
│ #  │ Skill                │ Est. Tokens │ Policy Flags │ Status  │
├────┼──────────────────────┼─────────────┼──────────────┼─────────┤
│ 1  │ web_search           │ ~500        │ external_api │ pending │
│ 2  │ fetch_web_content    │ ~2000       │ external_api │ pending │
│ 3  │ synthesize_research  │ ~3000       │ llm_call     │ pending │
│ 4  │ emit_result          │ ~100        │ —            │ pending │
└────┴──────────────────────┴─────────────┴──────────────┴─────────┘

Estimated total: ~5600 tokens
Policy warnings: 2 steps require external API access

To execute: ag run --plan plan_abc123
To discard: ag plan delete plan_abc123
```

---

## Non-goals

- Actual execution (that's AF-0099)
- Dynamic plan modification after generation
- Multi-plan comparison
- Cost estimation in currency (just tokens)

---

## Acceptance criteria (Definition of Done)

- [ ] `ag plan --task "..." --workspace <ws>` generates plan without executing
- [ ] Plan includes: proposed skills, order, estimated tokens, policy flags
- [ ] Plan saved to workspace with unique ID and expiration time
- [ ] `ag plan show <plan_id>` displays saved plan details
- [ ] `ag plan delete <plan_id>` removes saved plan
- [ ] `ag plans list --workspace <ws>` shows pending plans
- [ ] Plan schema documented
- [ ] Tests cover happy path and edge cases
- [ ] CI passes (`ruff check`, `pytest -W error`)

---

## Implementation notes

### CLI additions
- `ag plan --task "..." --workspace <ws>` — generate plan
- `ag plan show <plan_id>` — display plan details
- `ag plan delete <plan_id>` — remove plan
- `ag plans list --workspace <ws>` — list pending plans

### Storage
- Plans stored in `<workspace>/plans/<plan_id>/plan.json`
- Plan schema includes: task, proposed_steps, estimated_tokens, policy_flags, expires_at
- Plans auto-expire after TTL (default 1 hour, configurable)

### Integration with V1Planner (AF-0102)
- V1Planner is pure: `plan(task) -> Playbook` (no disk I/O)
- AF-0098 calls V1Planner to generate Playbook
- AF-0098 handles persistence: saves Playbook to `<workspace>/plans/`
- Separation of concerns: planner plans, storage stores

### Policy integration
- Each step annotated with policy flags (external_api, file_write, llm_call, etc.)
- Flags derived from skill metadata

---

## Risks

| Risk | Mitigation |
|------|------------|
| Plan format not extensible | Include version field, design for additive changes |
| Token estimates inaccurate | Label as "estimated", track actual vs estimate over time |
| Plans become stale | Enforce TTL, warn if workspace changed since plan |

---

# Completion section (fill when done)

_To be filled upon completion_
