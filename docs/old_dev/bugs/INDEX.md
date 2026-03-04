# Bugs — Index

> **⚠️ DEPRECATED (2026-03-03):** This index is archived. The canonical bug tracker is now at `/docs/dev/bugs/INDEX_BUGS.md`. Bug files have been migrated with the new naming convention.

This folder contains bug reports and bug templates.

## Structure
- `templates/` — bug report template
- `reports/` — bug reports (create as needed)

## Open Bugs

| ID | Title | Severity | Area | Status |
|----|-------|----------|------|--------|
| [BUG-0002](reports/BUG-0002-missing-run-options.md) | Missing ag run options per CLI reference | P2 | CLI | Open |
| [BUG-0003](reports/BUG-0003-missing-cli-subcommands.md) | Missing CLI subcommands per reference spec | P2 | CLI | Open |

## Fixed Bugs

| ID | Title | Severity | Area | Status |
|----|-------|----------|------|--------|
| [BUG-0001](reports/BUG-0001-global-options-not-global.md) | Global CLI options not implemented as global | P1 | CLI | Fixed |
| [BUG-0004](reports/BUG-0004-sqlite-connection-leak.md) | SQLite connections not closed → ResourceWarning | P1 | Storage | Fixed |
| [BUG-0005](reports/BUG-0005-implicit-workspace-creation.md) | Implicit workspace creation on ag run | P0 | CLI/Storage | Fixed |
| [BUG-0006](reports/BUG-0006.md) | Manual mode ignores .env AG_DEV | P1 | CLI | Fixed |

## How to use
1. Create a new file in `/docs/dev/bugs/reports/BUG-000x-<title>.md` from the template.
2. Link the bug from the relevant PR and/or backlog item.
3. Update status as the bug progresses (Open → In progress → Fixed → Verified).
