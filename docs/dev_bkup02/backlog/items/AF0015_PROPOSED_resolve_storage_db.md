# AF0015 — Resolve storage DB filename mismatch (docs vs code): ag.db vs db.sqlite
# Version number: v0.2

## Metadata
- **ID:** AF-0015
- **Type:** Quality
- **Status:** PROPOSED
- **Priority:** P2
- **Area:** Storage
- **Owner:** Jacob
- **Target sprint:** TBD
- **Related:** AF0058 (overlapping scope)

## Problem
Contract inventory describes workspace SQLite file as `ag.db`, while other docs/plans reference `db.sqlite`. This may be (a) docs mismatch, or (b) inconsistent naming across code paths.

## Goal
Standardize on a single canonical workspace DB filename and ensure all references (code, tests, docs) use the same constant/behavior.

## Non-goals
- Changing SQLite schema.
- Switching DB backend.
- Complex migration work (dev-only; optional backward-compat if trivial).

## Acceptance criteria (Definition of Done)
- [ ] Audit: confirm actual filename(s) created on disk for at least two workspaces.
- [ ] Choose canonical filename (prefer existing implementation unless strong reason).
- [ ] Unify code to a single constant (e.g., `DB_FILENAME`) referenced everywhere.
- [ ] Update docs (CONTRACT_INVENTORY, ARCHITECTURE, CLI_REFERENCE if needed) to match canonical filename.
- [ ] Update tests to assert the canonical filename.
- [ ] Optional: if trivial, accept both names with deprecation note.

## Implementation notes
- Search for hardcoded strings and unify.
- Add a test that creates a workspace and asserts DB file exists at expected path.

## Risks
Low: mainly naming; mitigate by updating tests and running full suite.

## PR plan
1. PR (chore/storage-db-filename): Audit + unify DB filename constant + update docs/tests.

---
# Completion section (fill when done)

Pending completion.

