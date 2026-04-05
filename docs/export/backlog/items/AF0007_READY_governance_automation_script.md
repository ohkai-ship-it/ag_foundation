# AF-0007 — Governance Automation Script (gov.py)
# Version number: v0.2
# Created: 2026-04-04
# Started:
# Completed:
# Status: READY
# Priority: P2
# Area: Process / Tooling
# Models:

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> **CI workflow (CRITICAL):**
> - **During AF development:** run targeted tests only
>   `python scripts/gov.py check`
> - **Before commit (full gate):**
>   1. `ruff check src tests scripts`
>   2. `ruff format --check src tests scripts`
>   3. `pytest -W error`
>   4. `pytest --cov=src/ag --cov-report=term-missing`

---

## Metadata
- **ID:** AF-0007
- **Type:** Tooling
- **Status:** READY
- **Priority:** P2
- **Area:** Process / Tooling
- **Owner:** Jacob
- **Target sprint:** Sprint 01 — governance_simplification
- **Phase:** 7 (depends on AF-0001 + AF-0006)

---

## Problem

Even after AF-0001 (no filename renames) and AF-0006 (streamlined INDEX), creating a new AF or updating a status still requires 2 manual edits across 2 files. Creating an AF requires: (1) copy template, (2) fill metadata, (3) add INDEX row with correct link. These are mechanical, error-prone, and account for ~5–10 min/sprint in ceremony data.

Additionally, there is no automated way to detect INDEX inconsistencies — the sprint close ritual includes a manual consistency scan that could be a command.

---

## Goal

- Optional CLI helper (`scripts/gov.py`) that automates the most common governance operations
- Provides a `check` subcommand that replaces the manual consistency scan
- Zero external dependencies — stdlib only
- Manual editing remains a valid fallback (script is a convenience, not a gate)

---

## Non-goals

- Auto-committing (git operations stay manual)
- Replacing human judgment on content (script manages structure only)
- External dependencies except stdlib
- CI enforcement (script is optional tooling)

---

## Acceptance Criteria
- [ ] `python scripts/gov.py check` passes on current repo state after S01 changes
- [ ] `python scripts/gov.py new-af <id> "<description>" --priority P1 --sprint 17` creates correct file + correct INDEX entry
- [ ] `python scripts/gov.py new-bug <id> "<description>" --severity P1` creates correct file + correct INDEX entry
- [ ] `python scripts/gov.py status af <id> DONE` updates internal `Status:` field + INDEX row; sets `Completed:` timestamp
- [ ] `python scripts/gov.py follow-up <id> "<description>"` creates follow-up AF for ACCEPT WITH FOLLOW-UPS workflow
- [ ] Script has `--help` for all subcommands
- [ ] Zero external dependencies (stdlib: pathlib, argparse, re, datetime only)
- [ ] `gov.py check` warns on cognitive health thresholds:
  - Collapse events > 2
  - Agent-initiated gates = "none" for 2 consecutive sprints
  - LLM avoidance events > 0
- [ ] `gov.py check` produces no false positives on legacy-format filenames (pre-AF-0001 convention)
- [ ] `gov.py check` produces no false positives on new-format filenames (AF-0001 convention)
- [ ] Docs impact checked: README / CLI_REFERENCE / ARCHITECTURE (updated or N/A)
- [ ] AI functionality check: N/A (no AI functionality)

---

## Implementation Notes

### Commands

| Command | Action |
|---|---|
| `gov.py new-af <id> "<desc>" --priority P1 --sprint 17` | Create AF file from template + add INDEX row; `Started:` left blank |
| `gov.py new-bug <id> "<desc>" --severity P1` | Create bug file from template + add INDEX row |
| `gov.py status af <id> DONE` | Update internal `Status:` field + INDEX row; set `Completed:` datetime if DONE |
| `gov.py check` | Validate INDEX links, status consistency, cognitive health thresholds |
| `gov.py follow-up <id> "<desc>"` | Create follow-up AF for ACCEPT WITH FOLLOW-UPS review outcome |

### Implementation constraints

- **~150–200 lines** — small, auditable, no magic
- **No auto-commit** — all git operations stay under human control
- **Stdlib only:** `pathlib`, `argparse`, `re`, `datetime` — no pip installs
- **Template-driven** — reads from existing template files in `docs/dev/*/templates/`
- **Idempotent check** — `gov.py check` is safe to run at any time

### Cognitive health check implementation

`gov.py check` reads the `Sprint Cognitive Health` section of the most recent closed sprint description and warns if any threshold is exceeded. It does not require file parsing beyond simple regex on the 7-field block.

---

## Files Touched
- `scripts/gov.py` (new — ~150–200 lines, stdlib only)

---

## Risks

**Low.** Optional tooling. Does not change any governance rules or data. If the script has bugs, manual workflow is unaffected. Validate with `gov.py check` on current repo before committing.

---

## Decision Record (if applicable)

- **Decision:** No external dependencies; stdlib only.
- **Alternatives considered:** Click / typer for CLI; PyYAML for parsing.
- **Rationale:** Zero-dependency scripts are self-contained and deployable in any environment without `pip install`. The governance script is infrastructure — it must work before the venv is set up.

---

## Completion

*(fill when Status = DONE)*
- **Review decision:**
- **Rationale:**
- **Follow-ups:**
- **PR link:**
