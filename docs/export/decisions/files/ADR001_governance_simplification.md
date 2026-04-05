# ADR-0001 — Governance Simplification
# Version number: v0.1

## Status
ACCEPTED

## Date
2026-04-04

## Context

After 15 sprints of development, governance ceremony overhead had grown to 30–50 minutes per sprint. Key pain points:

1. **Filename-status coupling:** Every status change required renaming the file, updating internal metadata, AND updating the INDEX — three edits for one logical change. Renames also broke links.
2. **Redundant sprint artifacts:** Each sprint produced up to 4 files (description, PR doc, review doc, PR template). The PR and review docs duplicated information already captured in the GitHub PR.
3. **Template gaps:** Templates lacked fields for time/model tracking, docs impact, and decision capture — information that was repeatedly needed but never formalized.
4. **No HITL framework:** Human-in-the-loop gates existed informally but were not codified. Ambiguity about when Jacob should escalate vs. proceed.
5. **Inconsistent versioning:** INDEX files carried disparate version numbers (INDEX_BACKLOG v1.2, INDEX_SPRINTS v0.5, templates v0.2). No way to know if two governance files belonged to the same generation.

See `docs/dev/additional/GOVERNANCE_SIMPLIFICATION_PLAN_0.1.md` for the full analysis (deliverables D1–D20).

---

## Decision

Implement governance simplification across Sprint 01 (8 AFs) to achieve ~10 min/sprint ceremony target:

1. **Eliminate filename-status coupling (AF-0001):** New files use immutable filenames without status tokens. Status tracked in exactly 2 places: internal metadata + INDEX row. Legacy files keep their names.

2. **Drop redundant sprint artifacts (AF-0002):** Replace 4-file sprint structure with MECE pair: `S##_DESCRIPTION.md` (planning) + `S##_REVIEW.md` (outcomes). GitHub PR is the canonical PR artifact.

3. **Enhance templates (AF-0003):** Add time/model logging, docs impact checklist, inline decision record to all templates.

4. **Codify HITL framework (AF-0004):** 15 named gates (G1–G15) in FOUNDATION_MANUAL §10. Constitutional principle: "Jacob may always escalate; Kai may always override."

5. **Streamline INDEX files (AF-0006):** Add Link column as sole file reference. No row moves on status change — update in place. Historical entries exempt.

6. **Historical record immutability (AF-0010):** Pre-v1.3 entries are immutable. No renames, restructuring, or normalization of historical records.

7. **Unify Governance System Version (AF-0008):** All governance docs bumped to GSV v1.3. Single version number answers "what governance system is running?"

8. **Governance automation deferred (AF-0007):** `gov.py` validation script deferred to backlog. Consolidate first, automate after the system proves usable.

---

## Alternatives considered

### A) Keep per-file versioning
Each INDEX and template keeps its own version number (e.g., INDEX_BACKLOG v1.2, templates v0.2).
**Rejected:** Impossible to know if a template and an INDEX belong to the same governance generation. A single GSV number makes this unambiguous.

### B) Full migration of historical records
Rename all legacy files to new convention, rewrite INDEX tables.
**Rejected:** High risk of broken links, git blame pollution, and no functional benefit. Historical records are read-only references.

### C) Incremental ceremony reduction without structural changes
Keep filename-status coupling but reduce the number of required files.
**Rejected:** Filename-status coupling is the root cause of most ceremony overhead. Without removing it, the other simplifications have limited impact.

---

## Consequences

**Pros:**
- ~10 min/sprint ceremony target (down from 30–50 min)
- Status changes require exactly 2 edits instead of 3
- No more broken links from file renames
- Single GSV v1.3 makes governance generation unambiguous
- HITL gates provide clear escalation/override boundaries
- Historical records preserved intact

**Cons:**
- Two naming conventions coexist indefinitely (legacy + new)
- Governance docs must explicitly document both conventions
- `gov.py` deferred — manual verification until automation is built
