# DEPRECATED — see FOUNDATION_MANUAL.md

> **This document is deprecated.**
> All rules have been consolidated into:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> This file is retained for historical reference only.
> Do not update this file. Update the operating manual instead.

---

# GitHub Workflow (ag_foundation)
# Version number: v0.2 (DEPRECATED)
# Effective date: 2026-03-03

## Branching model
- `main`: always releasable, protected
- Feature branches:
  - `feat/<short-name>`
  - `fix/<short-name>`
  - `chore/<short-name>`

## Work items
Every PR references:
- exactly one **primary** backlog item: `AF-####`
- optional secondary AFs / BUGs / ADRs

## PR requirements (minimum)
- Clear summary + non-goals
- File list (important paths)
- Evidence:
  - tests run (commands + results), and/or
  - RunTrace ID(s) for behavior changes
- Docs updated if contracts or workflow changed

## Merge strategy
- Squash merge preferred
- PR title should be a good changelog line

## CI expectations
- Ruff passes
- Tests pass with warnings treated as errors
- Coverage thresholds maintained
- No external network dependency unless explicitly allowed
