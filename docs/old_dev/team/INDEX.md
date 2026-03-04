# Team (ag_foundation) — Index

This folder defines **how we work together** on ag_foundation (roles, collaboration rules, Git workflow, and repo hygiene).

## Files
1. **collaboration_manifest.md** — roles, responsibilities, comms norms, and “how we ship”
2. **github_flow.md** — branching, PR sizing, reviews, and merge rules
3. **repo_hygiene_checklist.md** — day-to-day repo health checks and conventions

## Roles (quick reference)
- **Kai (PM / human-in-the-loop):** prioritization, acceptance criteria, release decisions
- **Jeff (Senior Engineer/Architect — GPT-5.2 Thinking):** architecture invariants, PR review gatekeeper, technical decisions
- **Jacob (Junior Engineer — VS Code + Copilot/Opus):** implementation in PR-sized chunks, tests, completion notes

## Ground rules (fast)
- Default runtime behavior is **LLM-first**; manual mode is **dev/test-only**.
- Truthful UX: outputs and labels must be provable from `RunTrace`.
- Prefer small PRs with evidence (tests, traces, review notes).
