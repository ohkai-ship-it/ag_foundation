# BACKLOG ITEM — AF0072 — playbook_validation_error
# Version number: v0.2

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - CLI discipline

> **File naming (required):** `AF####_<Status>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0072
- **Type:** Bug Fix / CLI
- **Status:** DONE
- **Priority:** P2
- **Area:** CLI
- **Owner:** Jacob
- **Target sprint:** Sprint 09 (completed)
- **Depends on:** None

---

## Problem

When an invalid playbook name is specified via `--playbook`, the CLI silently falls back to `default_v0` instead of failing with a clear error.

**Observed behavior:**
```
$ ag run --workspace s07-review --playbook nonexistent_playbook "Test"

Run completed
  Run ID: 0326b35b-5cbb-4018-bad0-10aaf54b145c
  Playbook: default_v0@1.0.0   ← Silent fallback!
```

**Expected behavior:**
```
Error: Playbook 'nonexistent_playbook' not found.
Available playbooks: default_v0, delegate_v0, summarize_v0
Run 'ag playbooks list' to see all available playbooks.
```

This violates the **Truthful UX** principle: the user requested a specific playbook and got a different one without explicit feedback.

---

## Evidence

From S07_REVIEW_01 cli_outputs.txt:
```
### Scenario A: Invalid Playbook Name
Command: ag run --workspace s07-review --playbook nonexistent_playbook "Test invalid"
Result: FELL BACK to default_v0 (not failed)
**Finding:** Unknown playbook falls back to default - may want to fail instead
```

---

## Acceptance Criteria

1. **Invalid playbook name fails with clear error** — ✅ Exit code 1, descriptive message
2. **Error suggests available playbooks** — ✅ Either inline list or `ag playbooks list`
3. **No silent fallback** — ✅ User must explicitly specify a valid playbook
4. **Backward compatibility** — ✅ If no `--playbook` specified, default_v0 is still used (this is fine)

---

## Proposed Solution

In `src/ag/cli/main.py`, the `run` command:

```python
# Before runtime execution
if playbook_name:
    playbook = get_playbook(playbook_name)
    if playbook is None:
        available = list_playbooks()
        err_console.print(f"[bold red]Error:[/bold red] Playbook '{playbook_name}' not found.")
        err_console.print(f"Available: {', '.join(available)}")
        raise typer.Exit(code=1)
```

---

## Test Cases

1. `ag run --playbook unknown "test"` → Error, exit 1
2. `ag run --playbook summarize "test"` → Works (alias)
3. `ag run --playbook summarize_v0 "test"` → Works (canonical)
4. `ag run "test"` → Works with default_v0 (no explicit playbook)

---

## References
- S07_REVIEW_01: `/docs/dev/sprints/documentation/Sprint07_summarize_playbook/S07_REVIEW_01.md`
- cli_outputs: `artifacts/review_S07_01/cli_outputs.txt`
- bug_triage: `artifacts/review_S07_01/bug_triage.md`

---

## Completion Section

**Completed:** Sprint 09 (2026-03-11)

### Solution Implemented

Added playbook validation in CLI's `run` command (line ~374) before runtime execution:

```python
# Validate playbook if specified (AF-0072: no silent fallback)
if playbook:
    from ag.playbooks import get_playbook, list_playbooks

    if get_playbook(playbook) is None:
        available = list_playbooks()
        err_console.print(
            f"[bold red]Error:[/bold red] Playbook '{playbook}' not found."
        )
        err_console.print(f"Available playbooks: {', '.join(available)}")
        err_console.print("Run [cyan]ag playbooks list[/cyan] for details.")
        raise typer.Exit(code=1)
```

### Files Changed

- `src/ag/cli/main.py`: Added playbook validation after manual mode check
- `tests/test_cli.py`: Updated `test_run_with_playbook_option` to use valid playbook
- `tests/test_cli.py`: Added `test_run_with_invalid_playbook_fails` test

### Test Evidence

```bash
# Invalid playbook now fails:
$ ag run --playbook nonexistent "Test" --workspace test-audit
Error: Playbook 'nonexistent' not found.
Available playbooks: default_v0, delegate_v0, research_v0, summarize_v0
Run ag playbooks list for details.

# Valid playbooks still work:
$ ag run --playbook default_v0 "Test"    # canonical name
$ ag run --playbook summarize "Test"     # alias
$ ag run "Test"                          # default (no --playbook)
```

### Run Evidence

- pytest -W error: 434 passed, 3 deselected
- Coverage: 86% maintained
