# Large Change Playbook (P1+) — ag_foundation
# Version number: v0.1

Use this playbook for architecture or runtime changes that span multiple PRs.

## 1) Frame the change (1 page max)
Create a short proposal in the relevant AF item:
- Problem / motivation
- Desired outcomes (definition of done)
- Non-goals
- Constraints/invariants (truthful UX, workspace isolation, modularity, safety hooks)
- Risks
- Migration/compat implications (if any)

## 2) Record the decision (ADR)
If the change is P1+:
- Create/Update an ADR in `/docs/dev/decisions/`
- Keep it short: context → decision → options → consequences → guardrails

## 3) Plan PR slicing (strict)
Rules:
- Keep each PR reviewable (~15–30 minutes).
- Prefer: **Scaffold PR → Behavior PR → Cleanup PR**

Recommended slices:
1) **Scaffold PR**
   - add interfaces, empty modules, schema additions (behind flags if needed)
   - no behavior change (or minimal)
2) **Behavior PR**
   - enable new behavior behind the interfaces
   - includes tests + evidence trace(s)
3) **Cleanup PR**
   - remove dead code
   - docs finalization, refactors

## 4) Evidence plan
Define upfront:
- Required unit tests
- Required integration tests
- RunTrace IDs to capture (manual ok for speed)
- Required review entry (P1)

## 5) Execution checklist
- [ ] AF epic + slices created
- [ ] ADR created/updated (P1+)
- [ ] PR1 opened with clear scope and no behavior change if possible
- [ ] PR2 adds behavior + tests + trace evidence
- [ ] PR3 cleanup and doc alignment
- [ ] Sprint report references completed slices

## 6) Done criteria
- Acceptance criteria of all slices complete
- No truthful UX regressions
- Trace schema stable and documented
- Workspace isolation and safety hooks preserved
