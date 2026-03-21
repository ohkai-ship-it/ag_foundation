# AF-0105 — CLI defaults fix
# Version number: v0.2
# Created: 2026-03-21
# Status: IN_PROGRESS
# Priority: P2
# Area: CLI/QA

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

---

## Summary

Fix all CLI commands so they work with sensible defaults out of the box. Every command should "just work" in the common case without requiring explicit flags. Flags modify behavior; they do not enable it.

---

## Problem

Several CLI commands currently require explicit parameters that should be inferred:

1. `--workspace` required for some commands but not others — should always fall back to default workspace
2. Output format inconsistencies (JSON vs human-readable Markdown)
3. Commands that should infer "latest run" still require explicit `--run`

**Principle:** Every CLI command should work with zero flags in the most common use case.

---

## Scope

### Commands to fix

**Core execution:**
- [ ] `ag run "<prompt>"` — must use default workspace, default playbook
- [ ] `ag run --plan <id>` — must infer workspace from plan storage

**Planning:**
- [ ] `ag plan generate` — must use default workspace
- [ ] `ag plan list` — must use default workspace
- [ ] `ag plan show <id>` — must use default workspace
- [ ] `ag plan delete <id>` — must use default workspace

**Run inspection:**
- [ ] `ag runs list` — must use default workspace
- [ ] `ag runs show <id>` — must use default workspace
- [ ] `ag runs trace <id>` — must use default workspace
- [ ] `ag runs stats` — must use default workspace

**Artifacts:**
- [ ] `ag artifacts list` — must use default workspace + latest run
- [ ] `ag artifacts show <name>` — must use default workspace + latest run
- [ ] `ag artifacts export <name>` — must use default workspace + latest run

### Out of scope
- `ag ws list` — no default needed (lists all)
- `ag ws create <name>` — explicit name required (correct)
- `ag ws use <name>` — explicit name required (correct)
- `ag config show` — no default needed
- `ag config set <key> <value>` — explicit required (correct)

---

## Acceptance criteria

- [ ] All commands above work without `--workspace` when a default workspace is set
- [ ] Commands against runs infer latest run when `--run` is omitted
- [ ] Error messages are clear when no default workspace is configured
- [ ] All error messages follow the same pattern for missing defaults
- [ ] Help text documents default behavior for each flag
- [ ] Tests cover each fixed command path

### Testing
- [ ] Test suite covers default workspace resolution for all commands
- [ ] Test suite covers "no config" error paths
- [ ] Integration tests verify end-to-end default workflow

---

## Implementation notes

This is primarily a verification/audit task, not new implementation. Expected work:

1. **Manual testing pass** — Run each command without optional flags
2. **Document gaps** — Create child bugs for any inconsistencies found
3. **Update tests** — Ensure test coverage for default behaviors
4. **Update docs** — Clarify defaults in CLI_REFERENCE.md

---

## Related

- AF-0097: runs commands default workspace (specific fix)
- CLI_REFERENCE.md: Command documentation
- test_cli.py: CLI test coverage
