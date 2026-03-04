# GitHub Flow (ag_foundation)
# Version number: v0.1

This document defines the branching and PR process for ag_foundation.

## 1) Branching model
- `main`: always releasable, protected
- Feature branches: `feat/<short-name>` or `chore/<short-name>` or `fix/<short-name>`

## 2) Work items
Every PR should reference at least one:
- backlog item: `AF-000x`
- bug report: `BUG-000x`

## 3) PR requirements (minimum)
- Clear description (what/why)
- Scope boundaries (what not included)
- Evidence:
  - tests run (and results), and/or
  - run trace id(s) showing behavior
- Doc updates if any public contract changed (cornerstone docs / CLI reference)

## 4) Review rules
- Jeff reviews architecture-meaningful changes (core runtime, trace schema, safety hooks).
- Kai reviews product-facing behavior and UX changes.
- Jacob requests review only after self-checks.

## 5) Merge strategy
- Squash merge preferred (clean history).
- PR title should be a good changelog line.

## 6) CI expectations
- Tests must pass.
- No external network dependency unless explicitly allowed (and documented).
- Manual mode can be used to speed up local tests (dev/test only).

## 7) Release notes (lightweight)
- Keep a short “what changed” in PR description.
- Optionally add a sprint report entry at sprint end.
