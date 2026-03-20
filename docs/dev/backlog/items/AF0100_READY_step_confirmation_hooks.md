# BACKLOG ITEM — AF0100 — step_confirmation_hooks
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
- **ID:** AF0100
- **Type:** Feature
- **Status:** READY
- **Priority:** P1
- **Area:** Core Runtime / Policy
- **Owner:** TBD
- **Target sprint:** Sprint 11 — guided_autonomy_enablement
- **Depends on:** AF-0087 (policy hook validation baseline — DONE in Sprint 09)

---

## Problem

Even with plan preview (AF-0098), users may want fine-grained control over
individual high-impact steps during execution. Current policy hooks (AF-0087)
exist but don't support interactive confirmation.

For guided autonomy, certain actions should require explicit user approval:
- External API calls (cost, privacy)
- File writes (data integrity)
- LLM calls above token threshold (cost control)

Without step-level confirmation, autonomy is all-or-nothing.

---

## Goal

Implement configurable step-level confirmation hooks:

```yaml
# workspace config or global config
confirmation_policy:
  enabled: true
  require_confirmation_for:
    - external_api      # web_search, fetch_web_content
    - file_write        # any file system modification
    - llm_call_large    # LLM calls > 1000 tokens
  
  # Behavior when confirmation required
  interactive_mode: prompt  # prompt | fail | skip
  non_interactive_mode: fail  # fail | skip | allow
```

Runtime behavior:
```
Executing step 2/4: fetch_web_content
⚠️  This step requires confirmation (external_api)
   Action: Fetch content from 5 URLs
   Estimated tokens: ~2000
   
   [Y]es / [N]o / [A]ll / [Q]uit: _
```

---

## Non-goals

- Per-URL or per-file granular confirmation (too noisy)
- Confirmation for read-only operations
- Retroactive confirmation (must be before execution)
- Custom confirmation prompts per skill

---

## Acceptance criteria (Definition of Done)

- [ ] Confirmation policy configurable per workspace
- [ ] Steps flagged with policy categories (external_api, file_write, llm_call_large)
- [ ] Interactive mode prompts user before flagged steps
- [ ] Non-interactive mode fails or allows based on config
- [ ] `--yes` flag bypasses all confirmations
- [ ] Confirmation decisions logged in trace
- [ ] `[A]ll` option confirms all remaining flagged steps
- [ ] `[Q]uit` option aborts execution cleanly
- [ ] Tests cover all confirmation paths
- [ ] CI passes

---

## Implementation notes

### Skill metadata
Each skill declares its policy flags:
```python
@skill(
    name="web_search",
    policy_flags=["external_api"]
)
def web_search(...):
    ...
```

### Policy engine
- Load confirmation policy from workspace config
- Before each step, check if any policy flags require confirmation
- Route to appropriate handler (prompt/fail/skip/allow)

### CLI integration
- `--yes` / `-y` flag: bypass all confirmations
- Interactive detection: check if stdin is TTY
- Non-interactive behavior configurable

### Trace recording
```json
{
  "steps": [{
    "skill_name": "fetch_web_content",
    "confirmation": {
      "required": true,
      "policy_flags": ["external_api"],
      "decision": "approved",
      "decided_at": "2026-03-13T10:31:00Z",
      "decided_by": "user_interactive"
    }
  }]
}
```

---

## Risks

| Risk | Mitigation |
|------|------------|
| Confirmation fatigue | Provide `[A]ll` option, tune defaults |
| Breaks automation | Clear non-interactive behavior, `--yes` flag |
| Inconsistent policy across steps | Centralize policy evaluation in runtime |

---

# Completion section (fill when done)

_To be filled upon completion_
