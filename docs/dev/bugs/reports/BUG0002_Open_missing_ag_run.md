# BUG-0002 — Missing ag run options per CLI reference
# Version number: v0.1

## Metadata
- **ID:** BUG-0002
- **Status:** OPEN
- **Severity:** P2
- **Area:** CLI
- **Reported by:** Jacob
- **Date:** 2026-02-24
- **Related backlog item(s):** AF-0008, AF-0012, AF-0085 (audit)
- **Related PR(s):** —

## Summary
The `ag run` command is missing several options documented in CLI_REFERENCE.md. While the core functionality works, the command lacks input flexibility (`--file`, `--task`) and safety controls (`--confirm`).

## Expected behavior
Per CLI_REFERENCE.md § "ag run — execute a task > Synopsis":
```
ag run "<prompt>"
ag run --file <path>          # treat file as input prompt/content
ag run --task <task.json>     # explicit TaskSpec payload; dev-oriented
ag run --playbook <name>      # ✅ implemented
ag run --reasoning <mode>     # ✅ implemented  
ag run --allow-web            # (planned; default true)
ag run --confirm / --no-confirm  # confirmation behavior; safety hook
```

## Actual behavior
Running `ag run --help` shows:
```
--workspace  -w      TEXT   ✅
--mode       -m      TEXT   ✅
--playbook   -p      TEXT   ✅
--reasoning  -r      TEXT   ✅
--json                      ✅
--quiet      -q             ✅
--verbose    -v             ✅
```

**Added since Sprint 08:**
- `--skill -s` — Run a specific skill directly (bypasses playbook) ✅

Still missing:
| Option | Purpose | Status |
|--------|---------|--------|
| `--file <path>` | Read prompt from file | ❌ Missing |
| `--task <task.json>` | Explicit TaskSpec payload | ❌ Missing |
| `--confirm / --no-confirm` | Safety confirmation hook | ❌ Missing |
| `--allow-web` | Web access flag | ❌ Missing (noted as "planned") |

**Planned fix:** AF-0012 (Sprint 10 scope)

## Reproduction steps
1. Run `ag run --help`
2. Try `ag run --file myfile.txt`
3. Observe: `Error: No such option: --file`

## Evidence
- **CLI_REFERENCE.md:** Lines 19-27 document the full synopsis
- **main.py:** Lines 157-176 show implemented options

## Impact
- Cannot easily pass long prompts via file input
- Cannot use TaskSpec directly for programmatic/dev workflows
- No safety confirmation for potentially destructive tasks

## Suspected cause
These options were likely deferred during AF-0008 to keep v0 scope minimal. The --playbook and --reasoning options demonstrate the pattern, so adding more is straightforward.

## Proposed fix
1. Add `--file` option that reads content and passes as prompt:
   ```python
   file: Optional[Path] = typer.Option(None, "--file", "-f", help="Read prompt from file.")
   # If --file provided, read content as prompt
   if file:
       prompt = file.read_text()
   ```

2. Add `--task` option for TaskSpec JSON:
   ```python
   task: Optional[Path] = typer.Option(None, "--task", "-t", help="TaskSpec JSON file.")
   # Parse and use TaskSpec instead of building from prompt
   ```

3. Add `--confirm / --no-confirm` flag:
   ```python
   confirm: Optional[bool] = typer.Option(None, "--confirm/--no-confirm", help="Confirmation behavior.")
   # If confirm is True, prompt user before execution
   ```

4. Optionally add `--allow-web` stub (marked as not yet functional).

## Acceptance criteria (for verification)
- [ ] `ag run --file prompt.txt` reads file and executes task
- [ ] `ag run --task spec.json` parses TaskSpec and executes
- [ ] `ag run --confirm "do something"` prompts for confirmation
- [ ] `ag run --no-confirm "do something"` skips confirmation
- [ ] Tests exist for each new option
- [ ] Help text matches CLI_REFERENCE.md

## Notes
- `--allow-web` may remain a stub/flag until web skills are implemented
- `--task` is primarily for dev/test workflows; may require `AG_DEV=1` gate like manual mode

