# Collaboration Manifest (ag_foundation)
# Version number: v0.2

This manifest defines **roles, responsibilities, and collaboration norms** for the ag_foundation project.

## 1) Mission
Build the **foundation** of an agent network: modular core runtime + skills/plugins + truthful observability + safety hooks, with future readiness for API/UI/IoT adapters.

## 2) Team and responsibilities

### Kai — Product Manager (human-in-the-loop)
- Owns: priorities, scope, acceptance criteria, release decisions
- Produces: backlog ordering, sprint goals, decision calls when tradeoffs arise
- Reviews: user experience, product scope, “is this the right thing now?”

### Jeff — Senior Engineer / Architect (GPT-5.2 Thinking)
- Owns: architecture invariants, system decomposition, interface contracts
- Produces: architecture/tech decisions, PR review guidance, risk identification
- Reviews: correctness, trace truthfulness, safety hooks, modularity

### Jacob — Junior Engineer (VS Code + Copilot/Opus)
- Owns: implementation tasks in PR-sized slices
- Produces: code changes, tests, completion notes, evidence traces
- Reviews: self-checks before PR, runs `ag doctor` / tests, updates docs if touched

## 3) Ways of working

### Sprint rhythm (lightweight)
- Sprint start: define goals + top backlog slice
- During sprint: small PRs, each tied to one backlog item
- Sprint end: short report + open issues + next slice

### PR sizing rule
- Prefer PRs that can be reviewed in ~15–30 minutes.
- If larger: split into “scaffolding PR” then “behavior PR”.

### Evidence rule
Every behavior change must include at least one of:
- tests (unit/integration)
- a captured run trace demonstrating the change
- a short review entry explaining verification steps

## 4) Communication norms
- Keep decisions explicit (record in PR notes or a review entry).
- When uncertain: propose options + recommend one; avoid long back-and-forth.
- Use consistent terminology: TaskSpec, RunTrace, Playbook, Skill, Workspace.

## 5) Invariants (non-negotiable)
- **Truthful UX:** CLI/API labels derive from RunTrace facts.
- **Workspace isolation:** no cross-workspace data leakage.
- **Modularity:** core runtime modules and skills remain swappable behind interfaces.
- **Safety hooks exist:** permission/confirmation points must not be bypassed.
- **Manual mode is dev/test-only:** never shipped as an end-user feature.
- **Code quality:** Ruff check and format must pass before merge.
- **Test discipline:** All tests must pass with `-W error` (warnings fail CI).
- **Coverage thresholds:** Overall ≥85%, CLI ≥72%, Providers ≥95%, Storage ≥95%.

## 6) Definition of Done (project-level)
A change is “done” when:
- acceptance criteria met (from backlog item)
- tests/evidence included as appropriate
- docs updated if contracts changed
- review completed and merged via GitHub flow
