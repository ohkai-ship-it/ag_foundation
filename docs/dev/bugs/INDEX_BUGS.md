# INDEX_BUGS
# Version number: v0.2

> **Location (new):** `/docs/dev/bugs/INDEX_BUGS.md`  
> **Naming (required):** `BUG####_<Status>_<three_word_description>.md` in `/docs/dev/bugs/reports/`  
> Status values: `Open | In progress | Fixed | Verified | Dropped`

---

## Open bugs
| ID | Severity | Status | Title | Area | New file (target path) |
|---:|:--:|:--|---|---|---|
| BUG-0007 | P1 | Open | OpenAI provider test isolation failure | Testing | `/docs/dev/bugs/reports/BUG0007_Open_openai_test_isolation.md` |
| BUG-0002 | P2 | Open | Missing ag run options per CLI reference | CLI | `/docs/dev/bugs/reports/BUG0002_Open_missing_ag_run.md` |
| BUG-0003 | P2 | Open | Missing CLI subcommands per reference spec | CLI | `/docs/dev/bugs/reports/BUG0003_Open_missing_cli_subcommands.md` |

---

## Fixed bugs
| ID | Severity | Status | Title | Area | New file (target path) |
|---:|:--:|:--|---|---|---|
| BUG-0001 | P1 | Fixed | Global CLI options not implemented as global | CLI | `/docs/dev/bugs/reports/BUG0001_Fixed_global_cli_options.md` |
| BUG-0004 | P1 | Fixed | SQLite connections not closed → ResourceWarning | Storage | `/docs/dev/bugs/reports/BUG0004_Fixed_sqlite_connections_not.md` |
| BUG-0005 | P0 | Fixed | Implicit workspace creation on ag run | CLI/Storage | `/docs/dev/bugs/reports/BUG0005_Fixed_implicit_workspace_creation.md` |
| BUG-0006 | P1 | Fixed | Manual mode ignores .env AG_DEV | CLI | `/docs/dev/bugs/reports/BUG0006_Fixed_manual_mode_ignores.md` |

---

## How to use
1. Create bug report from `/docs/dev/bugs/templates/BUG_REPORT_TEMPLATE.md`
2. Link bug from PR and/or AF item
3. Update status in:
   - bug filename
   - bug metadata
   - this index
