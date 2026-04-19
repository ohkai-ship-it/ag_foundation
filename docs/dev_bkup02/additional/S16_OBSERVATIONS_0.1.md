# Sprint 16 Observations — Governance System Learnings
# Version number: v0.1
# Created: 2026-04-05
# Author: Kai (PM), captured by Jeff (Tech Lead)
# Context: Observations collected during Sprint 16 (governance_simplification) implementation

---

## 1) Agent Behavior Under Governance Complexity

### 1.1 Historical content edits
Jacob repeatedly attempted to rename/restructure historical entries (sprint docs, INDEX rows, AF files from closed sprints). The pattern: "rename headers for sprint 1–16, then AFs, then bugs…" — a cascading scope explosion triggered by the ambiguous goal "all governance docs internally consistent."

**Root cause:** No in-doc signal that old entries use a different layout and must stay untouched.

**Resolution:** AF-0138 (v1.3 transition brief) created mid-sprint. Tiered placement: canonical rule in FOUNDATION_MANUAL, one-sentence pointer in SPRINT_MANUAL §2, HTML comment in each INDEX file header. ~4 lines of new content total.

### 1.2 Commit discipline failure
Jacob did not commit a single AF through the first 7 completed items. All changes sat in the working tree with no git safety net. The "1 commit per AF" rule from S16_DESCRIPTION §6 was entirely unenforced.

**Root cause:** Governance system complexity overwhelms the agent — process discipline is the first thing dropped when content work is demanding.

### 1.3 AF-0136 ambiguity
The goal statement "All governance docs internally consistent with new rules" was ambiguous enough to imply normalizing historical entries. AF-0136 was rewritten to say "All **authoritative** governance docs internally consistent with new rules **(historical entries exempt — see AF-0138)**" with an explicit Non-goals line about pre-v1.3 entries.

**Lesson:** Goal statements must be unambiguous about scope boundaries. Agents interpret maximally — if a goal can be read as "touch everything," it will be.

### 1.4 Misunderstanding of approval gates

Jacob treats G4 (AF completion approval) as "I cannot initiate a commit until the user tells me to" — a passive blocker. The correct behavior is proactive: "I've completed AF-0129. Here's what changed: [summary]. All AC met. Approve for commit?"

**Consequence:** The commit discipline failure (§1.2) is partly caused by this misunderstanding. If Jacob had proactively presented each completed AF and asked for sign-off, the uncommitted backlog would never have accumulated. Instead, he waited passively, and nobody triggered the commits.

**Correct gate behavior:**
- Agent DRIVES the flow — completes work, presents result, recommends action, asks for approval
- Human DECIDES — approve, reject, or request changes
- Agent EXECUTES the approved action (commit, move to next AF, etc.)

**Wrong gate behavior:**
- Agent completes work, stops, waits silently
- Human initiates the next action ("commit now")
- Agent passively follows

**Root cause:** The HITL gate definitions (G1–G15) say "Agent MUST Stop and Wait" — Jacob reads "stop and wait" literally as "go silent until spoken to." The phrasing should be "Agent MUST present result and request approval before proceeding." The gate is a checkpoint, not a wall.

**Fix needed:** Rephrase HITL gate descriptions in SPRINT_MANUAL / FOUNDATION_MANUAL to clarify that gates are proactive agent-initiated checkpoints, not passive blockers. This is a v1.4 improvement for gvs_development.

---

## 2) Process Improvements Identified

### 2.1 Phase-anchored approval gates

**Key insight:** Approval gates should anchor to PHASES in the sprint cycle, not to git actions.

Git actions (commit, PR, merge) are consequences of phase transitions, not the gates themselves. Agents barrel through conceptual transitions at machine speed unless explicitly gated.

Current problem: gates are tied to mechanical actions → agents skip the conceptual pause entirely.

Correct model — explicit human approval required at each phase boundary:
- Implementation → Review
- Review → Close
- Close → Next sprint planning
- Within implementation: AF batch done → consolidation AF
- Last AF commit → sprint review (never start reviewing immediately after the last commit)

The commit-per-AF discipline is a *hygiene rule*, not a gate. The gate is "are we ready to move to the next phase?"

This reframing simplifies the HITL framework: fewer, more meaningful gates instead of per-action checkpoints. Agents have no concept of "take a breath" — every sprint phase boundary needs an explicit human gate, not just the obvious ones (sprint start, sprint close) but the in-between transitions too.

### 2.2 Test scheduling and reduction
Full test suite is painful during per-AF commit gates. Need to reduce the number of tests or make test runs smarter.

Options to explore:
- Targeted test selection per AF (already in copilot-instructions, but not enforced)
- Test suite pruning — are all tests still needed?
- Parallelization (pytest-xdist)
- Tiered CI: fast smoke tests per commit, full suite only at PR merge
- Docs-only AFs should skip runtime tests entirely

### 2.3 Commit checkpoint enforcement
Need a mechanism beyond documentation to enforce commit discipline. Jacob consistently forgets.

Options:
- Copilot-instructions rule (currently exists but ignored under pressure)
- HITL gate at AF completion (explicit human approval before moving on)
- AF completion ritual checklist baked into the template
- Future `gov.py check` detecting uncommitted DONE AFs

### 2.4 AF-0135 (gov.py) deferred
Decision: consolidate first (AF-0136), automate later. Rationale:
- Don't automate conventions that might still shift
- Let the system prove usable for a sprint or two before building tooling
- Validation/debugging belongs in test files, not a separate script
- AF-0135 moved to unprioritized backlog; may be dropped if tests cover it

---

## 3) Versioning Conventions (Uncodified)

Emerging rules identified but not yet formalized anywhere in governance docs:

1. **INDEX-linked files** (AFs, bugs, ADRs, sprint docs): NO version in filename; version in file metadata header only
2. **`docs/dev/additional/` files**: version number IN filename; new version = new file (e.g., `GOVERNANCE_SIMPLIFICATION_PLAN_0.1.md` → `..._0.2.md`)
3. **All governance files**: should carry metadata for (a) GSV they were created under, (b) file's own version number
4. **Standalone reference docs** (FOLDER_STRUCTURE, PROJECT_PLAN, etc.): version in filename, same convention as `additional/`
5. **Files in `docs/dev/additional/`** with old version numbers weren't updated in S16 — no AF scoped them

These conventions need to be codified in FOUNDATION_MANUAL or FOLDER_STRUCTURE_0.3. Candidate for AF-0136 scope or a follow-up AF.

---

## 4) Governance System Deployability (Future Phase)

The governance system (docs, templates, INDEX files, validation, tests) is reaching complexity where it warrants its own standalone project. These observations inform the eventual deployability phase.

### 4.1 Migration strategy
- Create a new VS Code folder/project with its own git repo
- Seed it by copying existing `docs/dev/` as the starting point
- ag_foundation becomes the first "consumer" AND the reference implementation
  - If governance works well here (change logs current, versions traceable, scope changes governed, gates respected), that's live proof the system delivers
  - ag_foundation's documentation becomes dual-purpose: source of truth for the project AND validation that the governance system works
  - Every stale entry, missed commit, or ungoverned scope change is a governance system bug — not just a project hygiene issue
- Open design questions:
  - Consumer ↔ governance relationship model (git submodule? template repo? copy-and-diverge?)
  - How governance updates propagate to consumers
  - What stays in the consumer project vs. what lives in the governance repo
  - The consumer ↔ governance relationship is itself a candidate for automation — one of the most interesting design problems

### 4.2 Folder structure redesign
Current `docs/dev/` is flat — templates, foundation rules, and user-facing files all mixed together. Proposed separation:

- **System/config layer:** templates, foundation docs (FOUNDATION_MANUAL, SPRINT_MANUAL) — the "framework"
- **User content layer:** INDEX files, item files (AFs, bugs, ADRs, sprint docs) — the "project data"

This separation clarifies what's "governance system" vs. "project content" — the framework-vs-application boundary.

### 4.3 Consumer-specific hooks
The governance system currently touches project-level files (README.md, ARCHITECTURE.md) via the living reference sweep checklist. This works for ag_foundation but won't work for other consumers who have their own ideas for these files.

The system needs:
- Configurable sweep list (not hardcoded to 6 specific files)
- Optional hooks ("sweep these files if they exist")
- A governance-specific status file instead of borrowing the project's README
- Consumer project defines which files are in the living reference sweep
- Generic or configurable governance tests (test_documentation_drift.py is ag_foundation-specific — governance tests must be portable)

### 4.4 Roadmap as first-class artifact
PROJECT_PLAN_0.2.md does triple duty: roadmap, sprint history, and strategic analysis. It has no governance discipline — no INDEX, no template, no status tracking. Examples of drift:
- Sprint 16 description in PROJECT_PLAN still says "Skill Catalog Expansion" — factually stale
- LangChain analysis (2026-03-23) is embedded in the project plan rather than in `docs/dev/additional/`
- Phase transitions, gate achievements, and strategic pivots are documented inline rather than tracked as governance events

For the standalone governance system, roadmap should be a first-class artifact:
- Governed by a template
- Version-tracked
- INDEX-linked (or its own section in a master INDEX)
- Clear separation: roadmap (forward-looking phases/gates) vs. sprint history (backward-looking log)
- The governance system provides the roadmap structure; consumers fill in their phases, gates, and priorities
- This is critical for most projects, yet it's currently the least governed document in the system

### 4.5 Governance system scaffold
The governance system's own development (templates, INDEX files, validation rules, tests) is complex enough to warrant its own dedicated scaffold:
- Dedicated folder structure within the standalone repo
- Its own test suite (generic, not ag_foundation-specific)
- Possibly a standalone package or installable tool
- Keep this in mind for the deployability phase — not Sprint 16 scope

### 4.6 Bootstrap paradox — governance governs itself
When the governance system becomes standalone, it uses itself to manage its own development. This creates a self-referential loop that will confuse both agents and humans:

**Concrete confusion risks:**
1. **Template edits are product work, not violations.** In a consumer project, editing a template is forbidden (§7.2). In the governance repo, editing a template *is the work* — it's the product being built.
2. **INDEX files track AFs that modify INDEX files.** The AF that changes the INDEX format is itself tracked in the INDEX it's changing.
3. **FOUNDATION_MANUAL edits are constitutional amendments.** In a consumer project, you never touch it. In the governance repo, updating the manual is a regular AF.
4. **Sprint conventions change mid-sprint.** Just like Sprint 16's D11 — the sprint delivers new conventions that could retroactively apply to itself.

**Proposed solution: workspace role flag.**
A single, unmissable declaration that tells every participant (human and agent) which mode they're operating in:

- **`consumer`** (default): templates, FOUNDATION_MANUAL, INDEX schemas are protected — current rules apply
- **`framework-dev`**: those same files are editable under AF governance — they are the product being built

The flag lives somewhere visible — workspace config, repo root marker file, or copilot-instructions. Every gate and rule checks the mode before enforcing.

This also solves the "D11 problem" from Sprint 16: you're always building the next version while running under the current one. In `framework-dev` mode, that's the standard operating pattern, not an exception.

**This is a critical deployability design decision — must be resolved before standalone launch.**

### 4.7 Consumer → Governance feedback loop

**Timing decision:** Kai decided to outsource the governance system immediately after Sprint 16 close — not wait for a validation sprint. Rationale: the governance system will iterate faster without ag_foundation's runtime overhead, and the feedback loop design problem exists regardless of timing.

**The immediate use case:** ag_foundation Sprint 17 will generate governance feedback (bugs, improvement requests, convention gaps) while the governance repo is simultaneously improving the system. Both projects proceed independently; feedback flows through a defined channel.

**Feedback channels (consumer → governance):**

1. **Governance Bug Reports** — consumer discovers a rule that's broken, ambiguous, or missing (e.g., S16's historical edits problem). Filed as a bug *in the governance repo*, tagged with the consumer project that surfaced it.
2. **Governance Feature Requests** — consumer needs a new convention, template, gate type, or artifact type. Filed as an AF *in the governance repo*.
3. **Observations artifacts** — structured field experience artifacts (exactly what this file is). Could become a formal artifact type with its own template. Consumer writes them locally, then files the actionable items into the governance repo.
4. **Version upgrade notes** — when governance bumps a version, consumers need to know what changed and what to do. The change log (see §3, "Governance version change log") serves this purpose.

**Feedback channels (governance → consumer):**

1. **Version releases** — governance repo tags a new GSV; consumer pulls or copies updated templates, manuals, INDEX schemas
2. **Migration guides** — when a version introduces breaking changes, a migration guide explains what to update in the consumer project
3. **Change log** — the governance CHANGELOG tells consumers what's new without reading every AF

**Design decisions needed:**

- **Where does feedback live?** Filed directly in the governance repo (lightweight, immediate). Consumer keeps local observations for context but actionable items go upstream.
- **Who triages?** The governance project PM (Kai) reviews consumer feedback and prioritizes it in the governance backlog.
- **How formal?** Start lightweight — just file issues/bugs directly. Formalize the artifact type (e.g., "Governance Feedback Report" template) once there's enough volume to justify it.
- **Pull vs. push for updates?** Consumer decides when to adopt a new governance version. No forced upgrades. Consumer runs `consumer` mode, governance repo runs `framework-dev` mode (see §4.6).

**ag_foundation's role:**
ag_foundation is the first consumer AND the reference implementation. Its Sprint 17+ execution under v1.3 governance is simultaneously:
- A production use of the governance system (consumer mode)
- A source of feedback for governance v1.4+ (filed upstream)
- Living proof the system works for external consumers

---

## 5) Mid-Sprint Scope Change Handling

Sprint 16 had three scope changes mid-flight: AF-0138 added, AF-0135 deferred, AF-0136 rewritten. All three were necessary and well-reasoned — but the process for making them was entirely ad hoc. There is no governed procedure for changing sprint scope after the sprint has started.

### What happened
1. **AF-0138 created** — new P1 AF added mid-sprint to fill a gap (v1.3 transition brief)
2. **AF-0135 deferred** — P2 AF moved to unprioritized backlog (consolidate before automating)
3. **AF-0136 rewritten** — Goal, Non-goals, phase dependencies, and file references updated to reflect AF-0138 and AF-0135 changes

Each change required updates across multiple files: the AF itself, INDEX_BACKLOG, S16_DESCRIPTION (scope, execution diagram, commit plan, key references), and in AF-0136's case the review file as well. This was done correctly but only because Jeff was tracking it manually.

### What's missing
- **No formal scope change protocol.** SPRINT_MANUAL has no section for mid-sprint AF additions, deferrals, or rewrites.
- **No traceability.** The S16_DESCRIPTION was edited in place — there's no record of *when* or *why* the scope changed, only the final state. Someone reading the description after sprint close would never know AF-0138 was a mid-sprint addition.
- **No impact checklist.** When scope changes, which files must be updated? Currently this is tribal knowledge:
  - The AF file itself (create / edit / update status)
  - INDEX_BACKLOG (add/move/reorder rows)
  - S16_DESCRIPTION (scope §3, execution diagram §4, commit plan §6, references §8)
  - Any dependent AF files (update dependency references)
  - Review file (update inputs, add relevant checks)
- **No approval gate.** Scope changes should require explicit human approval — they're a phase transition ("scope is changing") not just an implementation step.

### What the governance system needs
A lightweight scope change protocol in SPRINT_MANUAL, something like:

1. **Trigger:** PM or Tech Lead identifies a scope change need
2. **Proposal:** Brief rationale — what's being added/deferred/rewritten and why
3. **Human approval:** Explicit go/no-go before any files are touched
4. **Impact checklist:** Standardized list of files to update (as above)
5. **Change log:** Append a timestamped entry to the sprint description (e.g., a "Scope Changes" section at the bottom) so the history is visible after close

This keeps scope changes fast (no heavy ceremony) but governed (traceable, approved, consistently applied).

For the standalone governance system: this protocol becomes a template-driven workflow. The framework provides the change log format and impact checklist; the consumer project fills in the details.

---

## 6) Summary of Sprint 16 Mid-Sprint Actions Taken

| Action | Detail | Status |
|---|---|---|
| AF-0138 created | v1.3 transition brief — tiered immutability rule | DONE — committed |
| AF-0136 rewritten | Historical immunity in Goal/Non-goals, AF-0135 refs removed, phase dependency updated | DONE |
| AF-0135 deferred | Moved from S16 scope to unprioritized backlog | DONE |
| INDEX_BACKLOG updated | AF-0138 added at order 7, AF-0135 moved to backlog, AF-0136 reordered to 8 | DONE |
| S16_DESCRIPTION updated | Scope §3, execution diagram §4, commit plan §6, key references §8 | DONE |
| Commits caught up | AF-0129 through AF-0138 committed in execution order | DONE |

---

## 7) Constitutional Additions

Rules that must be codified in FOUNDATION_MANUAL as inviolable governance invariants:

### 7.1 Approval gates are mandatory
Agents cannot skip, defer, or ignore approval gates unless specifically instructed by the human to do so. An agent that reaches a gate must stop and wait — even if the next step is obvious, even if the human is likely to approve. "Likely to approve" is not approval.

### 7.2 Templates are immutable at runtime
Template files (`docs/dev/*/templates/`) are governance system artifacts, not project content. Agents must never edit templates during sprint execution. Template changes require their own AF with explicit human approval.

This is also a deployability prerequisite: when the governance system is standalone, templates are part of the framework distribution. Consumer projects use them but do not modify them — modifications happen upstream in the governance repo.

### 4.8 Project-type assumptions and verification gap

**Problem:** GVS v1.3 hardcodes coding-project assumptions. The SPRINT_MANUAL's CI gate (Pass 2) mandates `pytest -W error`, `ruff check`, and coverage thresholds. For a docs-only project like gvs_development, these are meaningless — there's no source code to lint or test.

**Three verification strategies for gvs_development:**

1. **Skip CI passes** — weakens governance; the review gate loses its teeth for the project that builds the gates.
2. **Test against consumer** — ag_foundation becomes the test harness. When gvs_development changes a template or manual, validation runs against ag_foundation's sprint history to check nothing breaks. Tight coupling risk.
3. **Portable governance tests** — gvs_development ships its own test suite: INDEX schema validation, template compliance checks, folder structure verification. These tests ARE code (Python/pytest), giving gvs_development its own CI gate. This is the cleanest option.

**Abstraction question:** Should GVS support non-coding projects (design systems, hardware docs, research)? If yes, the CI gate becomes pluggable: "run the project's verification suite" instead of "run pytest." This is a product-level decision that changes GVS's target market.

**GVS runtime:** A future `gvs verify` / `gvs gate` / `gvs close` CLI tool that programmatically enforces governance gates. This would:
- Validate INDEX consistency automatically
- Check template compliance
- Enforce naming conventions
- Run project-type-appropriate verification passes

**Bootstrap note:** A GVS runtime is code, which CAN be tested with pytest. So gvs_development would have both docs AND code, giving it a real CI gate. But the runtime also governs its own development — the bootstrap paradox partially returns at the tooling layer.

---

## 8) Open Items for Sprint Review Discussion

These items need a decision during the S16 review — they are not yet resolved:

1. **Versioning conventions (§3):** Codify in AF-0136 or defer to follow-up AF?
2. **Phase-anchored gates (§2.1):** Should AF-0136 add phase gates to SPRINT_MANUAL, or is this a separate AF for Sprint 17?
3. **Test scheduling (§2.2):** When do we address this — Sprint 17 or a dedicated hardening sprint?
4. **PROJECT_PLAN staleness (§4.4):** Update as part of AF-0136's living reference sweep, or accept it as stale until the roadmap is formalized?
5. **Governance standalone project:** ~~At what point do we create the separate repo?~~ **RESOLVED** — Kai decided: immediately after Sprint 16 close. No waiting period.
6. **Scope change protocol (§5):** Codify in SPRINT_MANUAL as part of AF-0136, or create a follow-up AF?
7. **Version change log (§3):** Introduce a CHANGELOG or version history section? Retroactively document v1.0–v1.3?
8. **Feedback loop formalization (§4.7):** Start lightweight (file issues directly in governance repo). At what volume do we formalize with a "Governance Feedback Report" template?
9. **GVS project plan drafted (§4):** See `GVS_PROJECT_PLAN_0.1.md` — covers extraction, architecture, consumer model, bootstrap strategy, phased roadmap. Status: DRAFT, needs review during S16 Section B.
10. **GVS assumes coding projects (§4.8):** The SPRINT_MANUAL's CI gate (Pass 2: pytest, ruff, coverage) is meaningless for docs-only projects like gvs_development. Three options: (a) skip CI passes (weakens governance), (b) test against a consumer project (ag_foundation as test harness), (c) build portable governance tests (schema/template validation). Additionally, abstracting GVS to govern non-coding projects would require pluggable verification passes. A GVS runtime (`gvs verify`, `gvs gate`) is a longer-term possibility — and would partially re-introduce the bootstrap paradox at the tooling layer, since runtime code CAN be tested with pytest.
