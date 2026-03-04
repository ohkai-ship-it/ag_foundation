# AF0033 — Early .env Loading + Manual Mode Gate Fix
# Version number: v1.0

## Metadata
- **ID:** AF-0033
- **Type:** Foundation
- **Status:** Done
- **Priority:** P0
- **Area:** CLI | Core | Storage
- **Owner:** Jacob
- **Completed in:** Sprint 03
- **Completion date:** 2026-02-27

## Problem
Manual mode fails despite AG_DEV=1 in .env.

## Goal
Load .env at CLI entrypoint before mode validation; add regression tests.

## Non-goals
N/A

## Acceptance criteria (Definition of Done)
- [x] Implementation complete
- [x] Tests added/updated
- [x] No regression
- [x] Evidence captured (tests + trace)

## Implementation notes
N/A

## Risks
- Regression in CLI behavior
- Workspace state inconsistencies

## PR plan
N/A

---
# Completion section (fill when done)

**Completion date:** 2026-02-27  
**Author:** Jacob

**Related:** BUG-0006 (Manual mode ignores .env AG_DEV)

**Summary:**
Load .env at CLI entrypoint before mode validation. Manual mode now works when AG_DEV=1 is in .env file.

**What Changed:**
- `src/ag/cli/main.py` — Added early load_dotenv() at lines 10-12, before all other imports
- `src/ag/cli/main.py` — Added `# noqa: E402` comments for imports after load_dotenv()
- `tests/test_cli.py` — Added subprocess test for .env loading behavior

**Architecture Alignment:**
- CLI adapter (entrypoint)
- Bug fix, no breaking changes

**Tests Executed:**
- pytest tests/test_cli.py -k "dotenv": PASS (subprocess test)
- pytest -W error: PASS (188 tests)
- ruff check: PASS

**Run Evidence:**
1. Create `.env` with `AG_DEV=1`
2. Run `ag run --mode manual "test"`
3. Previously failed, now succeeds

**Status:** BUG-0006 fully resolved
