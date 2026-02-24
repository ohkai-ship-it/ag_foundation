# Repo Hygiene Checklist (ag_foundation)
# Version number: v0.1

Use this checklist to keep the repository consistent, reviewable, and low-drag.

## Daily / per-PR
- [ ] Branch name follows convention: `feat/`, `fix/`, `chore/`
- [ ] PR references AF/BUG ids
- [ ] Tests run locally (or explained why not)
- [ ] RunTrace captured for behavior changes (especially CLI labels / planner/orchestrator changes)
- [ ] No large unrelated diffs (split PR if needed)

## Docs hygiene
- [ ] Cornerstone docs live in `/docs/dev/cornerstone/`
- [ ] Changes to contracts update the relevant cornerstone doc
- [ ] New process docs go to the correct folder and include an `INDEX.md` update if needed

## Code hygiene
- [ ] Interfaces are explicit (no adapter logic leaking into core)
- [ ] Workspace boundaries respected (paths, storage, artifacts)
- [ ] Trace logging included for new behaviors

## Naming conventions
- [ ] IDs: `AF-000x` backlog, `BUG-000x` bugs, `run_<...>` run ids
- [ ] Core nouns: TaskSpec, RunTrace, Playbook, Skill, Workspace

## Before merging
- [ ] PR description includes evidence
- [ ] Reviewer can reproduce or validate via trace
- [ ] No “truthy” UI claims without trace support
