# AF0012 — CLI_REFERENCE surface parity v0.1: missing subcommand stubs (+ config tests)
# Version number: v0.3

## Metadata
- **ID:** AF-0012
- **Type:** Feature
- **Status:** DONE
- **Priority:** P2
- **Area:** CLI
- **Owner:** Jacob
- **Target sprint:** Sprint 10

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
- [x] Add stubs for missing subcommands (minimum): `ag runs tail`, `ag ws config get/set`, `ag artifacts open/export`, `ag skills test/enable/disable`, `ag playbooks validate/set-default`.
- [x] **`ag playbooks list` implemented** (from AF0059):
  - [x] Lists all available playbooks with metadata
  - [x] `--json` flag outputs structured JSON
  - [x] Default playbook marked in output
- [x] Stub semantics are consistent: non-zero exit code + message `Not implemented in v0`; with `--json`, return structured JSON error.
- [x] Tests added/updated (CLI surface)
- [x] Config tests added (config.py coverage focus)
- [x] After merge, config.py coverage increases measurably (target: +30pp or more for that file; exact % depends on implementation).
- [x] BUG-0003 can be closed or reclassified with evidence.

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

## Completion Summary

**Implemented CLI stubs:**
- `ag runs tail <run-id>` — stream live output (stub)
- `ag ws config get <key>` — get workspace config (stub)
- `ag ws config set <key> <value>` — set workspace config (stub)
- `ag artifacts open <artifact-id> --run <run-id>` — open in system viewer (stub)
- `ag skills test <name>` — run skill tests (stub)
- `ag skills enable <name>` — enable skill (stub)
- `ag skills disable <name>` — disable skill (stub)
- `ag playbooks show <name>` — show playbook details (stub, updated)
- `ag playbooks validate <path>` — validate playbook syntax (stub)
- `ag playbooks set-default <name>` — set default playbook (stub)
- `ag config list` — list config values (stub, updated with --json)
- `ag config get <key>` — get config value (stub, updated with --json)
- `ag config set <key> <value>` — set config value (stub, updated with --json)

**All stubs use centralized `_not_implemented()` helper:**
- Consistent exit code 1
- Console output: "⚠ {cmd} is not implemented in v0"
- `--json` output: `{"error": "not_implemented", "command": "...", "message": "..."}`

**Test coverage:**
- Added 15 new CLI stub tests (`TestCLIStubs` class)
- Added 7 new config state tests (`TestPersistedWorkspaceState` class)
- Config.py coverage: 56% → 98% (+42pp, exceeds +30pp target)
- Total tests: 539 → 561 (+22 tests)

**Files modified:**
- `src/ag/cli/main.py` — Added `_not_implemented()` helper, 12 stub commands, ws_config_app sub-app
- `tests/test_cli.py` — Added TestCLIStubs test class
- `tests/test_config.py` — Added TestPersistedWorkspaceState test class

