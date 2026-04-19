# BACKLOG ITEM — AF0142 — ag_foundation_gvs_handoff_docs
# Version number: v1.3
# Created: 2026-04-05
# Started: 2026-04-05
# Completed: 2026-04-05
# Status: DONE
# Priority: P1
# Area: Process / Docs
# Models: Claude Opus 4.6 (Copilot)

---

## Metadata
- **ID:** AF-0142
- **Type:** Docs
- **Status:** DONE
- **Priority:** P1
- **Area:** Process / Docs
- **Owner:** Jacob
- **Target sprint:** ag_foundation Sprint 17

---

## Goal

Document the GVS extraction milestone in ag_foundation's records. Mark clearly that governance was outsourced to the standalone convergent/GVS project after Sprint 16. Preserve all historical governance content in place — no deletions — but add clear markers so future agents and humans know the governance system no longer lives here.

## Scope

### 1. FOUNDATION_MANUAL.md — Add GVS extraction notice

Add a prominent notice near the top (after the header block, before §1) stating:

> **Governance System Extraction (effective after Sprint 16)**
> The governance system (GVS) was extracted into a standalone project (`convergent/`) after Sprint 16. From Sprint 17 onwards, ag_foundation consumes GVS as a fixed-version dependency. The authoritative governance rules live in `gvs_version_fixed/version1.3/`. This file is retained as historical record.

### 2. SPRINT_MANUAL.md — Add GVS extraction notice

Same pattern — prominent notice after header:

> **Governance System Extraction (effective after Sprint 16)**
> This manual was extracted into the standalone GVS project after Sprint 16. The authoritative version lives in `convergent/gvs_version_fixed/`. This copy is retained as historical record.

### 3. PROJECT_PLAN_0.2.md — Add GVS milestone entry

Add a new section or entry under the current state summary noting:

- Sprint 16: Governance simplification completed (8 AFs)
- Post-Sprint 16: GVS extracted to standalone project (`convergent/`)
- ag_foundation now consumes GVS v1.3 as external governance dependency
- Reference: `docs/dev/additional/GVS_PROJECT_PLAN_0.1.md`

### 4. INDEX_BACKLOG.md — Add extraction marker

Add a visible marker row or comment between Sprint 16 and Sprint 17 scope sections:

> `<!-- GVS EXTRACTION POINT: Governance AFs (AF-0129–AF-0141) migrated to convergent/GVS. See GVS_PROJECT_PLAN_0.1.md -->`

### 5. INDEX_BUGS.md — Add extraction marker

Same pattern for BUG-0025 and BUG-0026:

> `<!-- GVS EXTRACTION POINT: BUG-0025, BUG-0026 migrated to convergent/GVS as BUG-0001, BUG-0002 -->`

### 6. INDEX_DECISIONS.md — Add extraction marker

Same pattern for ADR-0010:

> `<!-- GVS EXTRACTION POINT: ADR-0010 migrated to convergent/GVS as ADR-0001 -->`

### 7. INDEX_SPRINTS.md — Add extraction marker

Add marker after Sprint 16 entry:

> `<!-- GVS EXTRACTION POINT: Sprint 16 governance work migrated to convergent/GVS as Sprint 01 -->`

### 8. README.md (root) — Add GVS reference

Add a brief section or line in the project README noting:

- ag_foundation uses the GVS governance framework
- Governance rules: `convergent/gvs_version_fixed/version1.3/`
- Governance development: `convergent/gvs_development/`

## Non-Goals

- Do NOT delete any historical files (AFs, bugs, ADRs, sprint docs stay in ag_foundation)
- Do NOT modify the content of historical AF/BUG/ADR/Sprint files
- Do NOT modify `docs/export/` — that's AF-0141's output
- Do NOT change copilot-instructions.md — that will be updated when ag_foundation adopts the GVS server folder

## Acceptance Criteria

- [ ] FOUNDATION_MANUAL.md has GVS extraction notice
- [ ] SPRINT_MANUAL.md has GVS extraction notice
- [ ] PROJECT_PLAN_0.2.md has Sprint 16 / GVS extraction milestone
- [ ] All 4 INDEX files have GVS extraction marker comments
- [ ] README.md references GVS
- [ ] All historical governance files remain untouched
- [ ] No functional changes to ag_foundation codebase

## Dependencies

- AF-0141 (GVS v1.3 export clean) — should be done first so the extraction is real
- Sprint 16 must be closed

## References

- `docs/dev/additional/GVS_PROJECT_PLAN_0.1.md`
- `docs/dev/additional/S16_OBSERVATIONS_0.1.md`
