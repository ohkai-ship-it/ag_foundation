# SPRINT DESCRIPTION — Sprint08 — skills_playbooks_maturity
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
> `/docs/dev/foundation/SPRINT_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - 1 PR = 1 primary AF
> - INDEX update rule (status ↔ filename integrity)

> **Folder naming (required):** `/docs/dev/sprints/documentation/Sprint08_skills_playbooks_maturity/`
> **Files (required):**
> - `S08_DESCRIPTION.md` (this file; includes plan + report)
> - `S08_REVIEW_01.md` (created after implementation)
> - `S08_PR_01.md` (PR checklist for sprint finalization)

---

## 1) Metadata
- **Sprint:** Sprint08
- **Name:** skills_playbooks_maturity
- **Dates:** 2026-03-09 → TBD
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **State:** Active

---

## 2) Sprint goal

Mature the skills and playbooks framework by:
1. Removing the deprecated V1 skill framework
2. Implementing the `research_v0` playbook with new skills
3. Completing CLI list commands
4. Cleaning up the playbooks registry

This sprint validates the architectural principle: **Skills = Capabilities, Playbooks = Procedures**.

---

## 3) Scope (what we intend to ship)

### Must-have (P0/P1)
| Order | ID | Title | Owner |
|:--:|--|--|--|
| 1 | AF-0073 | Index file linking convention | TBD |
| 2 | AF-0079 | Skills framework V1 removal | TBD |
| 3 | AF-0074 | research_v0 playbook | Kai |
| 4 | AF-0059 | Implement playbooks list | Jacob |
| 5 | AF-0076 | Playbooks registry cleanup | TBD |

### CHECKPOINT after item 5
Review scope of AF-0069 and AF-0070 before continuing.

### Conditional (P1, post-checkpoint)
| Order | ID | Title | Owner |
|:--:|--|--|--|
| 6 | AF-0069 | Skills architecture documentation | Kai |
| 7 | AF-0070 | Playbooks architecture documentation | Kai |

---

## 4) Sprint start checklist (ritual)

### Kai (PM)
- [x] Create AFs (Status = Ready) for items 1-5
- [x] Create this sprint description file
- [x] Define sprint ID + sprint name
- [x] Create sprint folder

### Jacob (Implementer)
- [ ] Read sprint description
- [ ] Check AFs in `/docs/dev/backlog/items/`
- [ ] Ask clarifying questions in chat (no writing required)
- [ ] Create branch
- [ ] Update INDEX files (ritual at sprint start):  
  - [ ] `/docs/dev/backlog/INDEX_BACKLOG.md`  
  - [ ] `/docs/dev/bugs/INDEX_BUGS.md`  
  - [ ] `/docs/dev/decisions/INDEX_DECISIONS.md`  
  - [ ] `/docs/dev/sprints/INDEX_SPRINTS.md`
- [ ] Confirm with Kai before starting implementation

> **INDEX update rule (strict):**  
> 1) Update when any AF/BUG/ADR/SPRINT status changes  
> 2) Also update as a ritual at sprint start

---

## 5) Technical notes

### AF-0079: V1 Framework Removal
**Breaking change:** Remove all V1 skill registration patterns.

Remove:
- `SkillFn` type alias
- `SkillInfo` dataclass (V1)
- `register()` method (V1)
- All V1 stub skills (analyze_task, execute_task, verify_result, etc.)

Rename:
- `SkillV2Info` → `SkillInfo`
- `register_v2()` → `register()`
- `list_v2_skills()` → `list_skills()`

After this, only Pydantic-based skills exist.

### AF-0074: research_v0 Playbook

**Pipeline:**
```
load_documents → fetch_web_content → synthesize_research → emit_result
```

**New skills:**
- `fetch_web_content` — HTTP fetch from user-provided URLs
- `synthesize_research` — LLM synthesis of multiple sources

### AF-0059: Playbooks List CLI
Implement `ag playbooks list` command:
- Show all playbooks with descriptions
- Support `--json` output
- Mark default playbook

### AF-0076: Playbooks Registry Cleanup
- Auto-generate `list_playbooks()` from registry
- Add stability markers (production/experimental)
- Warn on experimental playbook usage

### Versioning Convention
- **Skills:** No `_v0` suffix (atomic capabilities)
- **Playbooks:** Use `_v0` suffix (user-facing API versions)

---

## 6) Exit criteria

### Phase 1 (items 1-5)
- [ ] V1 skill framework completely removed
- [ ] `ag skills list` shows only: load_documents, summarize_docs, emit_result, fetch_web_content, synthesize_research
- [ ] `ag run --playbook research_v0` works end-to-end
- [ ] `ag playbooks list` shows all playbooks with descriptions
- [ ] Playbooks registry derives list from dict
- [ ] All tests pass, coverage ≥95%

### Phase 2 (items 6-7, conditional)
- [ ] Skills architecture documented in ARCHITECTURE.md
- [ ] Playbooks architecture documented in ARCHITECTURE.md
- [ ] "How to add skills/playbooks" guides complete

---

## 7) Sprint report (filled at close)

### Shipped items
| ID | Status | Title |
|--|--|--|
| | | |

### Not shipped (with reasons)
| ID | Status | Title | Reason |
|--|--|--|--|
| | | | |

### Evidence
- RunTrace IDs: (to be filled)
- Test summary: (to be filled)

### Learnings
- (to be filled)

---

## 8) PR plan
| PR | Primary AF | Branch | Status |
|--|--|--|--|
| PR-01 | AF-0073 | chore/index-linking | Planned |
| PR-02 | AF-0079 | refactor/v1-removal | Planned |
| PR-03 | AF-0074 | feat/research-v0 | Planned |
| PR-04 | AF-0059 | feat/playbooks-list | Planned |
| PR-05 | AF-0076 | chore/playbooks-cleanup | Planned |
