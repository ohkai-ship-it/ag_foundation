# AF-0105 — CLI defaults verification audit
# Version number: v0.1
# Created: 2026-03-21
# Status: PROPOSED
# Priority: P2
# Area: CLI/QA

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

---

## Summary

Audit and verify that all CLI commands work with sensible defaults, requiring explicit flags only when absolutely necessary. The goal is consistent UX where commands "just work" in the common case.

---

## Problem

During guided autonomy development, we encountered several cases where commands required explicit parameters that could have been inferred:

1. `--workspace` required for some commands but not others
2. Output formats defaulting to JSON instead of human-readable Markdown
3. Potential inconsistencies in default behaviors across command groups

**Principle:** Every CLI command should work with zero flags in the most common use case. Flags should modify behavior, not enable it.

---

## Scope

### Commands to verify (completeness check)

**Core execution:**
- [ ] `ag run "<prompt>"` — should use default workspace, default playbook
- [ ] `ag run --plan <id>` — should infer workspace from plan storage

**Planning:**
- [ ] `ag plan generate` — should use default workspace
- [ ] `ag plan list` — should use default workspace
- [ ] `ag plan show <id>` — should use default workspace
- [ ] `ag plan delete <id>` — should use default workspace

**Workspace management:**
- [ ] `ag ws list` — no defaults needed (lists all)
- [ ] `ag ws show` — should use default workspace
- [ ] `ag ws create <name>` — explicit name required (correct)
- [ ] `ag ws use <name>` — explicit name required (correct)

**Run inspection:**
- [ ] `ag runs list` — should use default workspace (AF-0097)
- [ ] `ag runs show <id>` — should use default workspace (AF-0097)
- [ ] `ag runs trace <id>` — should use default workspace (AF-0097)
- [ ] `ag runs stats` — should use default workspace (AF-0097)

**Artifacts:**
- [ ] `ag artifacts list` — should use default workspace, latest run
- [ ] `ag artifacts show <name>` — should use default workspace, latest run
- [ ] `ag artifacts export <name>` — should use default workspace, latest run

**Configuration:**
- [ ] `ag config show` — no defaults needed
- [ ] `ag config set <key> <value>` — explicit required (correct)

---

## Acceptance criteria

### Verification
- [ ] All commands documented in CLI_REFERENCE.md tested
- [ ] Commands without `--workspace` use `get_default_workspace()`
- [ ] Commands without `--run` against recent runs use latest run
- [ ] Error messages are clear when no default is set

### Consistency
- [ ] All error messages follow same pattern for missing defaults
- [ ] Help text documents default behavior for each flag
- [ ] `--verbose` or `-v` works consistently across all commands

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
