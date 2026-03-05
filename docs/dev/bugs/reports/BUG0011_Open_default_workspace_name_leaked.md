# BUG REPORT — BUG0011 — default_workspace_name_leaked
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - INDEX update rule (status ↔ filename integrity)
> - Evidence capture requirement (RunTrace ID for CLI/runtime bugs)

> **File naming (required):** `BUG####_<Status>_<three_word_description>.md`
> Status values: `Open | In progress | Fixed | Verified | Dropped`

---

## Metadata
- **ID:** BUG0011
- **Status:** Open
- **Severity:** P2
- **Area:** CLI
- **Reported by:** Kai
- **Date:** 2026-03-05
- **Related backlog item(s):** (none)
- **Related ADR(s):** (none)
- **Related PR(s):** (none)

---

## Summary
When a command fails due to a missing workspace, the error message reveals the workspace name even when it was resolved implicitly from config/environment. This leaks internal state that the user may not be aware of, causing confusion about where the name came from.

---

## Expected behavior
When workspace is resolved implicitly (from default/config):
```
Error: Default workspace does not exist or is not configured.
Set one with: ag ws use <name>
```

When workspace is explicitly provided by user:
```
Error: Workspace 'dev01' does not exist.
Create it first: ag ws create dev01
```

---

## Actual behavior
Both cases show the workspace name:
```
Error: Workspace 'dev01' does not exist.
Create it first: ag ws create dev01
```

This is confusing when the user never typed "dev01" — they don't know where this name came from.

---

## Reproduction steps
1. Set a default workspace that doesn't exist (or was deleted):
   - `ag ws use dev01` (when dev01 existed)
   - Delete workspace folder manually or via other means
2. Run any command that uses implicit workspace resolution:
   - `ag run --skill strategic_brief "Generate brief"`
3. Observe error message shows "dev01" even though user never specified it

---

## Evidence
- **CLI output:**
```
(.venv) PS> ag run --skill strategic_brief "Generate brief"
Error: Workspace 'dev01' does not exist.
Create it first: ag ws create dev01

(.venv) PS> ag ws use dev02
Error: Workspace 'dev02' does not exist.
Create it first: ag ws create dev02
```
- **Environment:** Windows, Python 3.14.0, commit 13c247b (feat/sprint05-skills)

---

## Impact
- **User confusion:** User sees a workspace name they didn't type and doesn't know its origin
- **Minor security concern:** Leaks configured state that user may not want visible
- **UX quality:** Violates principle of least surprise

---

## Suspected cause
The error handling code uses the resolved workspace name regardless of how it was resolved (implicit vs explicit). There's no tracking of whether workspace was user-provided or config-derived.

---

## Proposed fix
1. Track in workspace resolution whether the value came from:
   - `--workspace` flag (explicit)
   - Environment variable (semi-explicit)
   - Config file default (implicit)
2. Tailor error messages based on resolution source:
   - Explicit: Show the name (user typed it)
   - Implicit: Don't show the name, explain how to configure

---

## Acceptance criteria (for verification)
- [ ] Implicit workspace errors don't reveal workspace name
- [ ] Explicit workspace errors still show the name
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes

---

## Notes
Consider also improving the `ag ws use <name>` error — while the name is explicit, the suggestion to create might be inappropriate if user just mistyped.

---

## Status log
- 2026-03-05 — Opened by Kai
