# BACKLOG ITEM — AF0059 — implement_playbooks_list
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

> **File naming (required):** `AF####_<Status>_<three_word_description>.md`
> Status values: `Proposed | Ready | In progress | Blocked | Done | Dropped`

---

## Metadata
- **ID:** AF0059
- **Type:** Feature
- **Status:** Ready
- **Priority:** P2
- **Area:** CLI
- **Owner:** Jacob
- **Target sprint:** Sprint06 (tentative)

---

## Problem
The `ag playbooks list` command is currently a stub that prints "⚠ Stub — not implemented yet". Users cannot discover available playbooks through the CLI.

Current state:
- `list_playbooks()` in `playbooks.py` returns hardcoded `["default_v0", "delegate_v0"]`
- CLI command does nothing useful

---

## Goal
Implement a working `ag playbooks list` command that:
1. Lists all available playbooks with useful metadata
2. Supports `--json` output for scripting
3. Indicates which playbook is the default (if applicable)

---

## Non-goals
- Playbook creation/editing (future feature)
- Custom playbook loading from workspace (future feature)
- Playbook validation

---

## Acceptance criteria (Definition of Done)
- [ ] `ag playbooks list` shows all available playbooks
- [ ] Each playbook displays: name, description (if available)
- [ ] `--json` flag outputs structured JSON
- [ ] Default playbook is marked (e.g., `[default]` suffix or similar)
- [ ] Tests cover the new functionality
- [ ] CI/local checks pass:  
  - [ ] `ruff check src tests`  
  - [ ] `ruff format --check src tests`  
  - [ ] `pytest -W error`  
  - [ ] coverage thresholds met

---

## Implementation notes

### Changes required

1. **`src/ag/core/playbooks.py`**
   - Enhance `list_playbooks()` to return more than just names
   - Consider returning a list of dicts or dataclass instances with metadata:
     ```python
     @dataclass
     class PlaybookInfo:
         name: str
         description: str
         is_default: bool
     ```

2. **`src/ag/cli/main.py`**
   - Implement `playbooks_list()` to:
     - Call the core function
     - Format output with Rich table
     - Support `--json` flag

### Example output (table format)
```
Available playbooks:

  NAME          DESCRIPTION
  default_v0    Default single-response playbook [default]
  delegate_v0   Delegation playbook for multi-agent tasks
```

### Example output (JSON format)
```json
{
  "playbooks": [
    {"name": "default_v0", "description": "Default single-response playbook", "is_default": true},
    {"name": "delegate_v0", "description": "Delegation playbook for multi-agent tasks", "is_default": false}
  ]
}
```

---

## Risks
- **Low:** Simple implementation with no external dependencies
- If playbook registry is refactored later, this may need updates

---

## Related
- Consider also implementing `ag playbooks show <name>` in same PR for completeness
- AF0060 (Skill definition framework) — playbook/skill relationship needs clarity

---

## Documentation impact
This change may require:
- **ADR:** Potentially, if playbook metadata model decisions are made
- **CLI_REFERENCE.md:** Update `ag playbooks list` documentation from stub to implemented
- **README.md:** Add playbook discovery to quick-start if appropriate

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF0059
- **PR:** #<number>
- **Author:** <name>
- **Date:** YYYY-MM-DD
- **Branch:** <feat/... | fix/... | chore/...>
- **Risk level:** P2
- **Runtime mode used for verification:** manual

---

## 2) Acceptance criteria verification
(Copy AC list and mark when done)

---

## 3) What changed (file-level)
(Fill when done)

---

## 4) Architecture alignment (mandatory)
- **Layering:** CLI layer calls core playbooks module for data, formats for display
