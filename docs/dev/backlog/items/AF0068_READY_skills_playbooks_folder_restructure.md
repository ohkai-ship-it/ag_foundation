# BACKLOG ITEM — AF0068 — skills_playbooks_folder_restructure
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

> **File naming (required):** `AF0068_READY_skills_playbooks_folder_restructure.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0068
- **Type:** Refactor / Docs
- **Status:** READY
- **Priority:** P1
- **Area:** Skills / Playbooks / Structure
- **Owner:** Kai
- **Target sprint:** Sprint07

---

## Problem
The current codebase structure conflates playbooks with core runtime code:

**Current structure:**
```
src/ag/
├── skills/           # ✓ Dedicated folder, one file per skill
│   ├── base.py       # Skill ABC + context
│   ├── registry.py   # Skill registry functions
│   └── strategic_brief.py  # Concrete skill
└── core/
    ├── playbook.py   # Playbook SCHEMA (fine here)
    └── playbooks.py  # Playbook INSTANCES (wrong location)
```

Issues:
1. **Inconsistent organization:** Skills have their own folder, but playbooks live in `core/`
2. **Single file for all playbooks:** `playbooks.py` contains all hardcoded playbooks (DEFAULT_V0, DELEGATE_V0) in one file
3. **Scalability:** As we add more skills and playbooks, current structure doesn't scale
4. **Discoverability:** New contributors can't easily find where to add new playbooks

---

## Goal
Create a parallel folder structure where:
1. **Skills** stay in `src/ag/skills/` (already correct)
2. **Playbooks** get their own `src/ag/playbooks/` folder
3. **One file per playbook** — each playbook in a separate file
4. **One file per skill** — enforced convention for new skills

**Target structure:**
```
src/ag/
├── skills/                    # ✓ Already exists
│   ├── __init__.py
│   ├── base.py               # Skill ABC, SkillContext, SkillInput/Output
│   ├── registry.py           # get_skill(), list_skills()
│   └── strategic_brief.py    # One skill per file
└── playbooks/                 # NEW folder
    ├── __init__.py           # Exports all playbooks
    ├── registry.py           # get_playbook(), list_playbooks()
    ├── default_v0.py         # DEFAULT_V0 playbook
    └── delegate_v0.py        # DELEGATE_V0 playbook
```

---

## Non-goals
- Moving `playbook.py` (schema) from `core/` — it's correctly placed as a schema
- Creating YAML/JSON playbook loading (future work)
- Changing skill or playbook logic

---

## Scope

### Code changes
1. **Create `src/ag/playbooks/` folder**
2. **Move playbook instances:**
   - `core/playbooks.py` → Split into `playbooks/default_v0.py` + `playbooks/delegate_v0.py`
3. **Create `playbooks/registry.py`:**
   - Move `get_playbook()` and `list_playbooks()` functions
   - Auto-register playbooks from the folder
4. **Create `playbooks/__init__.py`:**
   - Export all public playbooks and registry functions
5. **Delete or deprecate `core/playbooks.py`:**
   - Update all imports

### Documentation updates
1. **ARCHITECTURE.md:**
   - Update folder structure section
   - Document skills/ and playbooks/ parallel structure
2. **FOLDER_STRUCTURE_0.2.md:**
   - Update module tree
3. **SCHEMA_INVENTORY.md:**
   - Update schema locations if needed
4. **CONTRACT_INVENTORY.md:**
   - Update implementation references

### Tests
1. **Update imports** in all test files referencing `core.playbooks`
2. **Add test for playbook registry** (discover playbooks from folder)
3. **Add test for skill registry** consistency check

---

## Acceptance criteria
- [ ] `src/ag/playbooks/` folder exists with proper structure
- [ ] Each playbook is in its own file (`default_v0.py`, `delegate_v0.py`)
- [ ] `get_playbook()` and `list_playbooks()` work from new location
- [ ] All imports updated, no references to `core.playbooks` remain
- [ ] All existing tests pass
- [ ] Documentation updated to reflect new structure
- [ ] CI green (ruff + pytest + coverage)

---

## Implementation notes

### Playbook file template
Each playbook file should follow this pattern:
```python
"""<playbook_name> playbook — <brief description>.

AF-00XX reference if applicable.
"""
from ag.core.playbook import (
    Budgets,
    Playbook,
    PlaybookStep,
    PlaybookStepType,
    ReasoningMode,
)

<PLAYBOOK_NAME> = Playbook(
    playbook_version="0.1",
    name="<playbook_name>",
    version="1.0.0",
    # ... rest of definition
)
```

### Registry pattern
Follow the same pattern as `skills/registry.py`:
```python
# playbooks/registry.py
from ag.playbooks.default_v0 import DEFAULT_V0
from ag.playbooks.delegate_v0 import DELEGATE_V0

_REGISTRY: dict[str, Playbook] = {
    "default_v0": DEFAULT_V0,
    "default": DEFAULT_V0,  # alias
    "delegate_v0": DELEGATE_V0,
    "delegate": DELEGATE_V0,  # alias
}

def get_playbook(name: str) -> Playbook | None:
    return _REGISTRY.get(name)

def list_playbooks() -> list[str]:
    return ["default_v0", "delegate_v0"]
```

---

## Related items
- **AF0060:** Skill definition framework (established skills/ pattern)
- **AF0065:** First skill set (will add more skills following this pattern)
- **AF0067:** Skill code documentation (add inline docs to skills/)

---

## Risks
- **Import churn:** Many files may reference `core.playbooks` — need thorough grep
- **CI breakage:** Ensure all tests updated before merge

---

## Open questions
1. Should we add auto-discovery of playbooks in the folder? (vs. explicit registry)
2. Should playbook filename match playbook name exactly? (e.g., `delegate_v0.py` → `delegate_v0`)
