# AF-0111 — --workspace flag must never create a workspace
# Version number: v0.1
# Created: 2026-03-21
# Status: PROPOSED
# Priority: P1
# Area: CLI/Storage

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

---

## Summary

The `--workspace` (`-w`) global flag must never implicitly create a workspace. If the user passes a workspace name that does not exist, the program must fail with a clear error. The only way to create a workspace is `ag ws create <name>`.

---

## Problem

Implicit workspace creation via `--workspace` is dangerous:

- Typos silently create empty workspaces (e.g. `ag run -w taks02` instead of `tasks02`)
- The user loses track of which workspaces exist
- Orphan workspaces accumulate with no data

The current code has a guard in `main.py` that checks `ws.exists()` before proceeding, but this behavior is not covered by a dedicated contract test. Any refactor could silently remove the guard.

---

## Scope

1. **Verify guard exists** — confirm `--workspace` resolution rejects non-existent names on all code paths
2. **Add contract test** — explicit test: passing `--workspace nonexistent` to any command must exit with error and must NOT create the workspace directory
3. **Error message contract** — error must include the bad name and suggest `ag ws create <name>`

### Out of scope
- Changing `ag ws create` behavior (already correct)
- Fuzzy matching / "did you mean?" suggestions (future enhancement)

---

## Acceptance criteria

- [ ] `ag run -w nonexistent "prompt"` exits with non-zero code and no directory created
- [ ] `ag plan list -w nonexistent` exits with non-zero code and no directory created
- [ ] `ag runs list -w nonexistent` exits with non-zero code and no directory created
- [ ] Error message includes the workspace name and `ag ws create` hint
- [ ] Contract test added to `test_contracts.py` or equivalent
- [ ] No code path bypasses the existence check
