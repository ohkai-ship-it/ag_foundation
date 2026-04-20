# AF0036 — Remove Global CLI Flags (Done)
# Version number: v1.2

## Metadata
- **ID:** AF-0036
- **Type:** Architecture
- **Status:** DONE
- **Priority:** P1
- **Area:** CLI
- **Owner:** Kai

## Problem
Global flags may create UX complexity and maintenance burden.

## Goal
Evaluate removal of global flags and migration to command-level options.

## Non-goals
N/A

## Acceptance criteria (Definition of Done)
- [x] Impact analysis complete
- [x] Migration path documented
- [x] Decision documented in ADR

## Decision Summary
**Hybrid approach adopted (ADR008):**
- Keep `--workspace` as the only global flag (context selection)
- Move `--json`, `--quiet`, `--verbose` to command-level options
- See ADR008_ACCEPTED_cli_global_flags.md for full rationale

## Implementation notes
See ADR008 for implementation details. Key changes:
1. `CLIContext` retains only `workspace`
2. Each command declares its own output formatting flags
3. Remove global/local precedence logic for output flags

## Risks
- Breaking change for existing users
- May simplify or complicate UX depending on usage patterns

## PR plan
N/A

---
# Completion section

**Completed:** 2026-03-12
**ADR:** ADR008_ACCEPTED_cli_global_flags.md
**Notes:** Chose hybrid approach after analysis. Global `--workspace` retained for context selection; output flags moved to command-level.

