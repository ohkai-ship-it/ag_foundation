# Observation Triage — _old/ Files vs v1.3.2
#### Description: Point-in-time audit of all files in `Convergent/docs/additional/_old/` against the current v1.3.2 governance standard. Tracks which observations were addressed, which remain open, and which files are fully consumed.
#### Convergent: v1.3.2
#### File version: 0.1
#### governs: ag_foundation
#### Date: 2026-04-20

---

## 1) File Inventory

| File | Type | Status |
|------|------|--------|
| `S01_OBSERVATIONS_0.1.md` | Sprint observations (Sprint 01 numbering) | Duplicate of S16 — see §2 |
| `S16_OBSERVATIONS_0.1.md` | Sprint observations (Sprint 16 numbering) | Primary observations doc — see §2 |
| `GVS_FEEDBACK_NOTES.md` | Consumer → governance feedback (7 notes) | See §3 |
| `GOVERNANCE_SIMPLIFICATION_PLAN_0.1.md` | Design doc for Sprint 16 | Fully consumed — see §4 |
| `GVS_PROJECT_PLAN_0.1.md` | Original Convergent extraction plan | Largely superseded — see §5 |
| `ARCHITECTURAL_FINDINGS_0_2.md` | Component version history (LinkedIn campaign) | Historical reference — see §6 |
| `SPRINT_VELOCITY_ANALYSIS_0.1.md` | Velocity analytics (LinkedIn campaign) | Historical reference — see §6 |
| `SPRINT_VELOCITY_ANALYSIS_0.2.md` | Velocity analytics v0.2 (LinkedIn campaign) | Historical reference — see §6 |
| `sprint_velocity_charts.html` | Chart visualizations (LinkedIn campaign) | Historical reference — see §6 |
| `LINKEDIN_CAMPAIGN_TECHNICAL_INPUT_0.1.md` | Marketing content for LinkedIn | No governance relevance — see §6 |
| `SKILLS_ARCHITECTURE_0.1.md` | Skill framework proposal (Sprint 06 era) | Stale as spec; key content inlined into ARCHITECTURE.md — see §7 |

---

## 2) Sprint Observations (S01 / S16)

S01_OBSERVATIONS and S16_OBSERVATIONS are **the same document** with different AF numbers substituted (S01 references AF-0007/0008/0010; S16 references AF-0129/0135/0136/0138). S16 is the canonical version — S01 appears to be an earlier draft or renumbered copy.

### Observation resolution against v1.3.2

| § | Observation | v1.3.2 Status | Resolution |
|---|---|---|---|
| §1.1 | Historical content edits — agents cascade-restructure old entries | **✅ Fully addressed** | §IM02 Historical Record Immutability. Explicit rule with legacy naming subsection (§IM02.1). |
| §1.2 | Commit discipline failure — 7 AFs uncommitted | **⚠️ Partially** | Copilot-instructions have commit rule + HITL gate G4. Enforcement is documentation-based only; no tooling. |
| §1.3 | Goal ambiguity → scope explosion | **✅ Addressed** | Learned behavior. AF templates emphasize Non-goals. No structural template mandate. |
| §1.4 | Passive gate behavior — "stop and wait" misread | **✅ Fully addressed** | §IM04 Gate Behavior at Runtime: agents must "present result and request approval." Copilot-instructions reinforce proactive gates. Primary fix from this doc. |
| §2.1 | Phase-anchored approval gates | **✅ Fully addressed** | LIFECYCLE_REGISTRY defines 6 phases with explicit gate boundaries. SP operationalizes phase transitions. |
| §2.2 | Test scheduling and reduction | **✅ Addressed** | Copilot-instructions: targeted tests per AF, full suite before commit only. §PO07 C1 vs C2/C3 split. |
| §2.3 | Commit checkpoint enforcement | **⚠️ Partially** | Still documentation-only. No `gov.py` or automated enforcement. Template lacks completion checklist. |
| §2.4 | gov.py deferred | **Intentionally deferred** | "Don't automate conventions that might still shift" — still valid rationale. |
| §3 | Versioning conventions uncodified | **✅ Fully addressed** | §DS01 → FOLDER_STRUCTURE.md codifies all naming conventions. File metadata headers standardized. |
| §4.1 | Migration strategy — standalone project | **✅ Fully addressed** | Convergent exists. Server/client model live. ag_foundation is the reference consumer. |
| §4.2 | Folder structure redesign — system vs user split | **✅ Fully addressed** | `foundation/` (system) vs `docs/` (user content) — the v1.3.2 architecture. |
| §4.3 | Consumer-specific hooks — configurable sweep list | **✅ Fully addressed** | §PO08 Living Docs is a PC-override table. Each consumer defines their own files. |
| §4.4 | Roadmap as first-class artifact | **✅ Fully addressed** | PROJECT_ROADMAP_TEMPLATE.md exists in foundation/templates/. ag_foundation roadmap rewritten 2026-04-20. |
| §4.5 | Governance system scaffold | **✅ Fully addressed** | Convergent IS this scaffold. |
| §4.6 | Bootstrap paradox / workspace role flag | **⚠️ Not addressed** | No formal `consumer` vs `framework-dev` mode in v1.3.2. GS applies identically regardless of context. Open design question for Convergent's own development. |
| §4.7 | Consumer → governance feedback channel | **⚠️ Partially** | No `external_inputs/` folder. No formal feedback template. GVS_FEEDBACK_NOTES.md was the ad-hoc attempt. |
| §4.8 | Project-type assumptions — docs-only projects | **⚠️ Not addressed** | §PO07 hardcodes pytest/ruff. No pluggable verification pass concept. |
| §5 | Mid-sprint scope change protocol | **⚠️ Not addressed** | No formal scope change procedure in SP or GS. Still ad-hoc when it happens. |
| §7.1 | Approval gates are mandatory | **✅ Fully addressed** | §IM04 + §IM06. |
| §7.2 | Templates immutable at runtime | **✅ Fully addressed** | §IM08.4 Server Boundary — foundation/ is read-only to the consumer. |

**Score: 12 of 18 fully addressed, 5 partially, 1 intentionally deferred.**

---

## 3) GVS Feedback Notes

7 consumer feedback notes filed by ag_foundation team (Jeff/Kai) dated 2026-04-06.

| Note | Topic | v1.3.2 Status | Resolution |
|---|---|---|---|
| Note 1 | Out-of-sprint items have no clean backlog section | **✅ Addressed** | INDEX_BACKLOG now has "Done — No scope (inter-sprint)" section with documented convention. |
| Note 2 | New AFs skip PROPOSED status — missing PM approval gate | **⚠️ Partially** | §IM07 defines PROPOSED→READY transition. No explicit rule preventing agents from creating AFs as READY directly. The human gate is implicit, not enforced. |
| Note 3 | AF date fields missing time component | **⚠️ Not addressed** | Templates don't enforce ISO 8601 with time. `Created:` fields still commonly date-only. |
| Note 4 | Inter-sprint phase is unstructured — no preparation checklist | **⚠️ Partially** | LIFECYCLE_REGISTRY defines phases. But no explicit "copy templates, create folder, create AFs as PROPOSED" ritual documented in SP. |
| Note 5 | AF scoping without codebase verification | **Not addressed** | No "Premises" section in AF template. No rule requiring code verification before AF finalization. |
| Note 6 | Bug triage depth — symptom vs root cause | **Not addressed** | No "Root cause / Symptom / Unknown" field in BUG template. No triage depth requirement. |
| Note 7 | CI full gate runs pytest twice (redundant) | **✅ Addressed** | §PO07 C2 combines flags into a single command. C3 still lists them separately but the duplication is documented. |

**Score: 2 of 7 fully addressed, 3 partially, 2 not addressed.**

---

## 4) Governance Simplification Plan

`GOVERNANCE_SIMPLIFICATION_PLAN_0.1.md` was the design blueprint for Sprint 16 (governance_simplification). **Fully consumed.**

All 8 AFs (AF-0001 through AF-0008, later renumbered AF-0129 through AF-0136) were delivered:
- Filename-status coupling eliminated (AF-0129)
- Redundant sprint artifacts dropped (AF-0130)
- Template enhancements (AF-0131)
- HITL framework codified (AF-0132)
- Copilot ToDo discipline (AF-0133)
- INDEX streamlining (AF-0134)
- v1.3 transition brief (AF-0138)
- Governance docs consolidation (AF-0136)

The HITL framework (§2 of the plan) is now §IM03–§IM06 in the Governance Standard. The gate table, escalation procedure, human rights, constitutional principle, and review decisions all shipped as designed.

**Status: Historical. No residual action items.**

---

## 5) GVS Project Plan

`GVS_PROJECT_PLAN_0.1.md` was the original Convergent extraction plan (2026-04-05). **Largely superseded.**

| Plan section | v1.3.2 reality |
|---|---|
| §1-3 Vision, current state | Superseded by PROJECT_ROADMAP_0.1.md (rewritten 2026-04-20) |
| §4.1 Server/client model | **Concept preserved**, simpler implementation. Plan assumed `gvs_version_fixed/version1.3/` + `gvs_development/version1.4/`. Reality: single `Convergent/` folder with `foundation/` + `docs/` |
| §4.2 Two-layer split (`hidden_layer/` + `user/`) | **Implemented differently** as `foundation/` + `docs/`. Same separation, different naming |
| §4.3 Folder structure | **Significantly different** from actual layout. The elaborate nested structure (gvs_version_fixed, gvs_development, hidden_layer, user, external_inputs) was simplified |
| §4.4 Server governs clients | **Concept preserved** in §IM08 |
| §4.5 Version lifecycle (N built under N-1) | **Concept preserved**. Not formally exercised yet (no v1.4 exists) |
| §5 Consumer model | **Concept preserved** in §IM08.5 |
| §7 Phase 0 (extraction) | ✅ Done |
| §7 Phase 1 (v1.4 development) | Never happened as planned; v1.3.2 was the target |
| §7 Phases 2-3 | Remain future |

**Status: Historical. The architectural concepts survived but the implementation diverged significantly. The new PROJECT_ROADMAP replaces this as the forward-looking document.**

---

## 6) Analytics and Marketing Content

Three files were produced for a LinkedIn campaign (Simon/Kai, 2026-04-01):

- **ARCHITECTURAL_FINDINGS_0_2.md** — Component version history with git-verified timestamps. Protocol stability analysis (unchanged signatures across 15 sprints, 13 implementations). Still factually accurate through S18. Valuable as technical reference.
- **SPRINT_VELOCITY_ANALYSIS_0.1.md / 0.2.md** — Git-derived velocity data (S00–S15). Wall-clock times, merge timelines, ceremony overhead analysis. Not updated for S16–S18.
- **sprint_velocity_charts.html** — Chart visualizations accompanying the velocity analysis.
- **LINKEDIN_CAMPAIGN_TECHNICAL_INPUT_0.1.md** — Technical pitch content. Two-sentence pitch, competitive positioning vs LangChain/CrewAI/AutoGen, architecture explainers.

**Status: All historical reference. No governance relevance. No action items.**

---

## 7) Skills Architecture

`SKILLS_ARCHITECTURE_0.1.md` — Draft proposal from Sprint 06 era (2026-03-06). Assessed in a prior session. Code has substantially diverged (SkillDefinition → class attributes; SkillResult/Evidence/ArtifactRef → simplified SkillOutput; Protocol → ABC). Core principles preserved (bounded autonomy, humans define WHAT / agents decide HOW).

Key content was inlined into `ARCHITECTURE.md` Section 3.3 on 2026-04-19.

**Status: Stale as specification. Historical value only. Content transferred.**

---

## 8) Open Items Summary

Items from _old/ files that v1.3.2 has **not yet addressed**. These are candidates for Convergent backlog:

### High impact

| # | Source | Issue | Notes |
|---|---|---|---|
| 1 | Obs §4.6 | **Bootstrap paradox / workspace role flag** — no `consumer` vs `framework-dev` mode | Critical for Convergent's own development. Agents editing templates in framework-dev mode vs consumers where templates are immutable. |
| 2 | Obs §5 | **Mid-sprint scope change protocol** — no SP section | Scope changes happen regularly. Currently ad-hoc with manual multi-file updates. |
| 3 | Feedback Note 2 | **PROPOSED→READY enforcement** — agents skip PM review gate | Agents create AFs as READY directly, bypassing the item-level approval checkpoint. |

### Medium impact

| # | Source | Issue | Notes |
|---|---|---|---|
| 4 | Feedback Note 4 | **Inter-sprint preparation checklist** — phase structure exists but no explicit creation ritual | Agents don't know to copy templates, create folders, create AFs as PROPOSED without prompting. |
| 5 | Feedback Note 5 | **AF codebase verification rule** — no "Premises" section | Scope claims about existing functionality go unverified until implementation. |
| 6 | Feedback Note 6 | **Bug triage depth field** — no root-cause classification | Symptom-level bugs enter sprints without root-cause analysis. |
| 7 | Obs §4.8 | **Docs-only project verification** — §PO07 hardcodes pytest/ruff | Blocks governance for non-coding projects. |

### Low impact

| # | Source | Issue | Notes |
|---|---|---|---|
| 8 | Feedback Note 3 | **Date/time format enforcement** — templates don't enforce ISO 8601 with time | Loses temporal ordering within a single day. |
| 9 | Obs §1.2/§2.3 | **Commit checkpoint enforcement** — documentation-only | Agents still forget under pressure. No tooling. |
