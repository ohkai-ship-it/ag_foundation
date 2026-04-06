# GVS Feedback Notes for Convergent
# Convergent version: v1.3.1
# Purpose: Structured observations from ag_foundation (consumer) to convergent (GVS development)
# Format: Each note is a self-contained observation that Conny can triage into AFs or bugs

---

## Note 1 — Backlog doesn't handle out-of-sprint items well

**Observed by:** Jeff (Tech Lead, ag_foundation)
**Date:** 2026-04-06
**Context:** AF-0140 and AF-0143 were completed as pre-sprint standalone tasks (outside any numbered sprint). After completion, they sat in the unprioritized backlog with DONE status — cluttering the active backlog and confusing the index.

**Problem:** The INDEX_BACKLOG schema assumes items flow through sprints: unprioritized → sprint scope → DONE within that sprint. There's no clean place for:
- Pre-sprint standalone tasks (completed outside a sprint)
- Items completed between sprints (housekeeping, urgent fixes)
- Items that were created and completed within the same planning session

**Workaround applied:** Created a "Pre-Sprint 17 (standalone)" section in INDEX_BACKLOG. This works but is ad hoc — the section naming convention isn't documented, and future agents won't know to use it.

**Suggested fix directions:**
1. Add a documented "standalone / inter-sprint" section convention to the INDEX schema
2. Define a lifecycle for items that bypass sprint scope (created → done without sprint assignment)
3. Consider whether the backlog should have a permanent "completed standalone" section at a fixed location

---

## Note 2 — New AFs skip PROPOSED status (missing human approval gate)

**Observed by:** Kai (PM, ag_foundation)
**Date:** 2026-04-06
**Context:** During Sprint 18 planning, Jeff created AF-0144 through AF-0147 with status READY. Kai had approved the sprint plan conceptually but had not reviewed or approved the individual AF files before they were marked READY.

**Problem:** The backlog lifecycle is `PROPOSED → READY → DONE`. The PROPOSED → READY transition is a critical human gate — the PM must review and approve each work item before it becomes eligible for sprint execution. By skipping PROPOSED and going straight to READY, the agent bypasses this approval checkpoint entirely.

This is a governance violation: the agent assumed that plan-level approval ("thumbs up for the AFs") implied item-level approval. It does not. The PM needs to review the actual AF file content (scope, acceptance criteria, non-goals) before promoting to READY.

**Impact:** High. If an AF has incorrect scope, missing non-goals, or wrong acceptance criteria, the implementer will execute it as-is — the READY status signals "approved for implementation."

**Suggested fix directions:**
1. Add an explicit rule in FOUNDATION_MANUAL or SPRINT_MANUAL: "New AFs MUST be created with status PROPOSED. Only the PM (or designated reviewer) may promote to READY."
2. Consider making the PROPOSED → READY transition a named HITL gate (e.g., G0: AF Approval)
3. The agent creating AFs should state: "Created as PROPOSED — awaiting your review and approval to promote to READY"

---

## Note 3 — AF date fields missing time component

**Observed by:** Kai (PM, ag_foundation)
**Date:** 2026-04-06
**Context:** AF-0144 through AF-0147 were created with `Created: 2026-04-06` (date only). The backlog item template expects date and time (e.g., `2026-04-06T14:30`).

**Problem:** The governance templates define date fields that include a time component, but agents consistently write date-only values. This loses temporal ordering within a single day — when multiple AFs are created in the same session, the creation order becomes ambiguous.

**Impact:** Low individually, but compounds over time. Sprint forensics and audit trails rely on precise timestamps. When reviewing "what happened on April 6," date-only entries collapse the entire day into one moment.

**Suggested fix directions:**
1. Clarify the expected date format in the template explicitly (e.g., `# Created: YYYY-MM-DDTHH:MM`)
2. Add a format example in the template header comment so agents copy the pattern
3. Consider whether ISO 8601 with timezone (`2026-04-06T14:30+02:00`) is worth the complexity

---

## Note 4 — Inter-sprint phase is unstructured (governance gap)

**Observed by:** Kai (PM, ag_foundation) + Jeff (Tech Lead, ag_foundation)
**Date:** 2026-04-06
**Context:** Sprint 18 planning session. After sprint scope was finalized and AFs written, the PM asked "please prepare the sprint docs." The agent required 4 successive prompts to complete what should have been a single checklist-driven task.

**Problem:** The inter-sprint phase (period between sprint close and next sprint start) has no structured procedure. The sprint manual covers sprint execution (§1–§9) and has a brief §10 on inter-sprint commits, but there is no equivalent of the sprint start ritual for the **planning/preparation** phase that precedes it.

Specific gaps:
1. **No "sprint preparation checklist"** — The sprint manual's §0.2 has a pre-sprint checklist focused on *reading* (verify scope, confirm statuses). There is no checklist for *creating* sprint artifacts: description from template, review from template, PR template, artifacts folder.
2. **Template usage not mandated** — Templates exist in `docs/dev/sprints/templates/` but nothing in the manual says "copy these templates to create S##_DESCRIPTION.md, S##_REVIEW.md, S##_PULL_REQUEST.md." The connection between templates and sprint artifacts is implicit.
3. **AF creation lifecycle unclear** — When the PM approves a sprint plan, what is the exact sequence? Create AFs as PROPOSED → PM reviews → promote to READY → create sprint description → create review/PR templates → create artifacts folder? This sequence is not documented.

**Impact:** High. During Sprint 18 planning, the agent: (a) created a sprint description freehand instead of from template (missing 4 sections), (b) did not create review or PR files until explicitly asked, (c) did not create the artifacts folder. Each omission required a separate correction prompt. A documented checklist would have prevented all of these.

**Suggested fix directions:**
1. Add a "Sprint Preparation Protocol" section to SPRINT_MANUAL (or expand §0/§10) with an explicit checklist: create folder → copy templates → fill description → create AFs as PROPOSED → PM review gate → promote to READY
2. Add a "Files required" list in the sprint description template header that links to the other templates (making the connection explicit)
3. Consider a pre-sprint HITL gate: "Sprint preparation complete — present folder contents to PM for verification before sprint start"

---

## Note 5 — AF scoping without codebase verification

**Observed by:** Jeff (Tech Lead, ag_foundation)
**Date:** 2026-04-06
**Context:** AF-0146 (`ag artifacts list --category` filter) was created with the claim that "categories are already inferred internally." This was false — no category taxonomy exists in the codebase.

**Problem:** The governance framework has no rule requiring that AF scope claims be verified against the actual codebase before the AF is finalized. The agent wrote acceptance criteria that depended on functionality that didn't exist, which would have caused the implementer to either (a) discover the gap mid-sprint and escalate, or (b) silently expand scope to build the missing prerequisite.

**Impact:** Medium. The PM caught this during review and deferred AF-0146. Without that review, a sprint could contain an AF whose scope is based on false premises — a common cause of mid-sprint blowups.

**Suggested fix directions:**
1. Add a rule to AF creation: "Scope claims about existing functionality must cite the specific file/function/line. If the claim cannot be verified, mark the AF as needing a spike/investigation step."
2. Consider a "Premises" section in the AF template where the author lists assumed preconditions (e.g., "Assumes category inference exists in artifact_store.py") that can be verified during PM review.

---

## Note 6 — Bug triage depth at sprint planning

**Observed by:** Kai (PM, ag_foundation)
**Date:** 2026-04-06
**Context:** BUG-0011 (default workspace name leaked in error) was included in Sprint 18 as a simple error message fix. The PM immediately recognized it as a symptom of a deeper design issue (cross-workspace leakage) and reframed it as a conceptual AF (AF-0148).

**Problem:** The governance framework treats bug triage as a status change (OPEN → sprint scope), not as an analysis step. There is no requirement to assess whether a bug report describes a root cause or a symptom before including it in a sprint. The agent took BUG-0011 at face value; the PM had to provide the architectural insight.

**Impact:** Medium. Including symptom-level bugs in sprints leads to shallow fixes that don't address the underlying issue, creating recurring bugs or technical debt.

**Suggested fix directions:**
1. Add a "Triage depth" field to the bug report template: `Root cause | Symptom | Unknown`
2. If a bug is marked `Symptom` or `Unknown`, require a brief root-cause note before it enters sprint scope — either confirming the fix is sufficient or recommending a conceptual AF
3. Sprint planning review should include a triage pass: "For each bug in scope, is this a root cause fix or a symptom patch?"

---
