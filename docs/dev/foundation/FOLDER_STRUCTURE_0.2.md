# Folder Structure — /docs/dev
# Version: v0.2
# Effective date: 2026-03-04

```
/docs/dev/
│
├── additional/
│   ├── playbooks/
│   │   ├── CLI_CHANGE_PLAYBOOK.md
│   │   ├── LARGE_CHANGE_PLAYBOOK.md
│   │   ├── NEW_DEPENDENCY_PLAYBOOK.md
│   │   └── TRACE_SCHEMA_CHANGE_PLAYBOOK.md
│   │
│   └── prompts/
│       ├── templates/
│       │   ├── CONTINUATION_PROMPT_JUNDEV.md
│       │   └── CONTINUATION_PROMPT_SENDEV.md
│       ├── continuation_prompt_jeff_sprint_design.md
│       ├── continuation_prompt_sprint03_opus.md
│       └── kickoff_prompt_jacob_onboarding.md
│
├── backlog/
│   ├── items/
│   │   └── AF####_<desc>.md           (new convention: no status token)
│   │   └── AF####_<Status>_<desc>.md  (legacy: existing files keep status token)
│   ├── templates/
│   │   └── BACKLOG_ITEM_TEMPLATE.md
│   └── INDEX_BACKLOG.md
│
├── bugs/
│   ├── reports/
│   │   └── BUG####_<desc>.md           (new convention: no status token)
│   │   └── BUG####_<Status>_<desc>.md  (legacy: existing files keep status token)
│   ├── templates/
│   │   └── BUG_REPORT_TEMPLATE.md
│   └── INDEX_BUGS.md
│
├── decisions/
│   ├── files/
│   │   └── ADR###_<desc>.md
│   ├── templates/
│   │   └── ADR_TEMPLATE.md
│   └── INDEX_DECISIONS.md
│
├── foundation/
│   ├── FOUNDATION_MANUAL.md       ← Canonical operating rules
│   ├── SPRINT_MANUAL.md           ← Deterministic sprint execution
│   ├── PROJECT_PLAN_0.1.md        ← Historical
│   ├── PROJECT_PLAN_0.2.md        ← Current project plan
│   └── FOLDER_STRUCTURE_0.2.md    ← This file
│
└── sprints/
    ├── documentation/
    │   ├── Sprint##_<desc>/
    │   │   ├── S##_DESCRIPTION.md
    │   │   ├── S##_REVIEW_01.md
    │   │   ├── S##_PR_01.md
    │   │   └── artifacts/
    │   └── _old/
    ├── templates/
    │   ├── SPRINT_DESCRIPTION_TEMPLATE.md
    │   ├── PULL_REQUEST_TEMPLATE.md
    │   ├── REVIEW_TEMPLATE.md
    │   └── SPRINT_PR_TEMPLATE.md
    └── INDEX_SPRINTS.md
```

---

## Canonical Documents

| Document | Purpose |
|----------|---------|
| `FOUNDATION_MANUAL.md` | All operating rules, invariants, CI discipline |
| `SPRINT_MANUAL.md` | Step-by-step sprint execution protocol |

---

## Naming Conventions

| Artifact | New convention (Sprint 01+) | Legacy convention (pre-Sprint 01) |
|----------|----------------------------|-----------------------------------|
| Backlog items | `AF####_<three_word_description>.md` | `AF####_<Status>_<three_word_description>.md` |
| Bug reports | `BUG####_<three_word_description>.md` | `BUG####_<Status>_<three_word_description>.md` |
| ADRs | `ADR###_<three_word_description>.md` | (same — ADRs never had status tokens) |
| Sprint folders | `Sprint##_<three_word_description>/` | (same) |
| Sprint files | `S##_DESCRIPTION.md`, `S##_REVIEW_01.md`, `S##_PR_01.md` | (same) |

**Both conventions coexist.** Existing files keep their current names. New files use the new convention (no status token in filename). Status is tracked in internal metadata + INDEX row only.

---

## Status Values

**Backlog:** `PROPOSED | READY | BLOCKED | DONE | DROPPED`

**Bugs:** `OPEN | FIXED | DROPPED`

**ADRs:** `PROPOSED | ACCEPTED | SUPERSEDED | DEPRECATED`

**Sprints:** `PLANNED | DONE | REJECTED`
