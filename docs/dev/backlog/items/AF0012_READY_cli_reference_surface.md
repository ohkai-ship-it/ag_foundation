# AF0012 — CLI_REFERENCE surface parity v0.1: missing subcommand stubs (+ config tests)
# Version number: v0.3

## Metadata
- **ID:** AF-0012
- **Type:** Feature
- **Status:** READY
- **Priority:** P2
- **Area:** CLI
- **Owner:** Jacob
- **Target sprint:** TBD (needs discussion)

## Problem
The CLI implements core commands, but several subcommands documented in CLI_REFERENCE are missing (BUG-0003 subcommands). This creates spec drift and blocks API-parity planning. Additionally, config.py has low coverage (~46%); adding CLI surface for config should include config tests.

## Goal
Establish CLI surface parity for v0.1 by stubbing missing subcommands with clear behavior, while increasing confidence via focused CLI + config tests.

## Non-goals
- Implementing full behavior for every stubbed subcommand (OK to stub).
- Enabling real web access (`--allow-web`) (can be stubbed as always-false).
- Adding LLM provider integration (separate items).
- Advanced `ag run` options (`--file`, `--task`, `--confirm`) — deferred to future iteration.

## Acceptance criteria (Definition of Done)
- [ ] Add stubs for missing subcommands (minimum): `ag runs tail`, `ag ws config get/set`, `ag artifacts open/export`, `ag skills test/enable/disable`, `ag playbooks validate/set-default`.
- [ ] **`ag playbooks list` implemented** (from AF0059):
  - [ ] Lists all available playbooks with metadata
  - [ ] `--json` flag outputs structured JSON
  - [ ] Default playbook marked in output
- [ ] Stub semantics are consistent: non-zero exit code + message `Not implemented in v0`; with `--json`, return structured JSON error.
- [ ] Tests added/updated (CLI surface)
- [ ] Config tests added (config.py coverage focus)
- [ ] After merge, config.py coverage increases measurably (target: +30pp or more for that file; exact % depends on implementation).
- [ ] BUG-0003 can be closed or reclassified with evidence.

## Implementation notes
- Centralize stub helper (e.g., `not_implemented(cmd_name, json_mode)`), so all stubs behave the same.
- For config tests: create temp config files in tests; avoid relying on user home directory; prefer env var override to point at temp.
- **Per ADR008:** `--json`, `--quiet`, `--verbose` must be declared as command-level options (not global). `--workspace` remains the only global flag.

## Risks
Low: adding stubs is straightforward. Main risk is forgetting to update stubs when real implementations land.

## Related
- **AF0059 (Dropped)** — Playbooks list (absorbed into this AF)
- **AF0036 (Done)** — Global CLI flags decision
- **ADR008** — CLI global flags (hybrid approach)
- BUG-0002, BUG-0003 — CLI surface gaps

## PR plan
1. PR (chore/cli-stub-surface): Add missing subcommand stubs + JSON error semantics + tests.
2. PR (test/config-coverage): Add focused config tests (path resolution, missing/invalid config) and wire into CI.

---
# Completion section (fill when done)

Pending completion.

