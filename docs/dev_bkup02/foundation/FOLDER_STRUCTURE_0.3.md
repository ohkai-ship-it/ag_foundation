# Folder Structure — /docs/dev
# Convergent version: v1.3.1
# File version: v1.3
# Effective date: 2026-04-04
# Supersedes: FOLDER_STRUCTURE_0.2.md

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
│   ├── prompts/
│   │   ├── templates/
│   │   │   ├── CONTINUATION_PROMPT_JUNDEV.md
│   │   │   └── CONTINUATION_PROMPT_SENDEV.md
│   │   ├── continuation_prompt_jeff_sprint_design.md
│   │   ├── continuation_prompt_sprint03_opus.md
│   │   └── kickoff_prompt_jacob_onboarding.md
│   │
│   ├── ARCHITECTURAL_FINDINGS_0_2.md
│   ├── CONTRACT_INVENTORY.md
│   ├── GOVERNANCE_SIMPLIFICATION_PLAN_0.1.md
│   ├── SCHEMA_INVENTORY.md
│   ├── SKILLS_ARCHITECTURE_0.1.md
│   └── SPRINT_VELOCITY_ANALYSIS_0.*.md
│
├── backlog/
│   ├── items/
│   │   ├── AF####_<desc>.md              (new convention: immutable filename, no status token)
│   │   └── AF####_<Status>_<desc>.md     (legacy: existing files keep status token)
│   ├── templates/
│   │   └── BACKLOG_ITEM_TEMPLATE.md
│   └── INDEX_BACKLOG.md
│
├── bugs/
│   ├── reports/
│   │   ├── BUG####_<desc>.md              (new convention: immutable filename, no status token)
│   │   └── BUG####_<Status>_<desc>.md     (legacy: existing files keep status token)
│   ├── templates/
│   │   └── BUG_REPORT_TEMPLATE.md
│   └── INDEX_BUGS.md
│
├── decisions/
│   ├── files/
│   │   └── ADR###_<desc>.md              (ADRs never had status tokens — unchanged)
│   ├── templates/
│   │   └── ADR_TEMPLATE.md
│   └── INDEX_DECISIONS.md
│
├── foundation/
│   ├── FOUNDATION_MANUAL.md              ← Canonical operating rules
│   ├── SPRINT_MANUAL.md                  ← Deterministic sprint execution
│   ├── FOLDER_STRUCTURE_0.3.md           ← This file (current)
│   ├── FOLDER_STRUCTURE_0.2.md           ← Superseded
│   ├── FOLDER_STRUCTURE_0.1.md           ← Historical
│   ├── PROJECT_PLAN_0.1.md               ← Historical
│   └── PROJECT_PLAN_0.2.md               ← Current project plan
│
└── sprints/
    ├── documentation/
    │   └── Sprint##_<three_word_description>/
    │       ├── S##_DESCRIPTION.md        (planning artifact)
    │       ├── S##_REVIEW.md             (outcomes artifact, written at sprint close)
    │       └── artifacts/                (review outputs, traces, logs)
    ├── templates/
    │   ├── SPRINT_DESCRIPTION_TEMPLATE.md
    │   ├── SPRINT_REVIEW_TEMPLATE.md
    │   ├── PULL_REQUEST_TEMPLATE.md      (kept for reference; GitHub PR is canonical)
    │   └── archived/
    │       ├── REVIEW_TEMPLATE.md        (superseded by SPRINT_REVIEW_TEMPLATE)
    │       └── SPRINT_PR_TEMPLATE.md     (superseded by GitHub PR workflow)
    └── INDEX_SPRINTS.md
```

---

## Canonical Documents

| Document | Purpose |
|----------|---------|
| `FOUNDATION_MANUAL.md` | All operating rules, invariants, CI discipline, HITL framework |
| `SPRINT_MANUAL.md` | Step-by-step sprint execution protocol |
| `FOLDER_STRUCTURE_0.3.md` | This file — current folder layout |

---

## Naming Conventions

Two naming conventions coexist. New files use immutable filenames (no status token). Legacy files keep their original names (status token in filename). Both are valid.

| Artifact | New convention (Sprint 01+) | Legacy convention (pre-Sprint 01) |
|----------|----------------------------|-----------------------------------|
| Backlog items | `AF####_<three_word_description>.md` | `AF####_<Status>_<three_word_description>.md` |
| Bug reports | `BUG####_<three_word_description>.md` | `BUG####_<Status>_<three_word_description>.md` |
| ADRs | `ADR###_<three_word_description>.md` | (same — ADRs never had status tokens) |
| Sprint folders | `Sprint##_<three_word_description>/` | (same) |

**Status tracking (new convention):** Status lives in exactly **2 places**: internal file metadata + INDEX row. Status changes require exactly **2 edits**, zero renames.

**Status tracking (legacy convention):** Status in **3 places**: filename token + internal metadata + INDEX row. All three must match.

> Historical files and entries are immutable — see FOUNDATION_MANUAL §7.7.

---

## Sprint Folder Structure

Each sprint has one folder under `documentation/` containing:
- `S##_DESCRIPTION.md` — planning artifact (scope, sequence, checklist)
- `S##_REVIEW.md` — outcomes artifact (review decision, cognitive health, learnings)
- `artifacts/` — supplementary files (traces, logs, screenshots)

**Deprecated artifacts:** `S##_PR_01.md` and `S##_REVIEW_01.md` no longer created. GitHub PR is the canonical PR artifact. Historical sprint folders may still contain these files.

---

## Status Values

> Canonical status values are defined in FOUNDATION_MANUAL §7.6. The values below must match.

**Backlog:** `PROPOSED | READY | BLOCKED | DONE | DROPPED`

**Bugs:** `OPEN | FIXED | DROPPED`

**ADRs:** `PROPOSED | ACCEPTED | SUPERSEDED | DEPRECATED`

**Sprints:** `PLANNED | DONE | REJECTED`

---

## Governance System Version

All governance INDEX files and templates carry **Governance System Version (GSV) v1.3** as of Sprint 01. See ADR-0001.
