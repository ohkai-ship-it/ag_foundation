# INDEX_BUGS
# Version number: v0.3

> **FOUNDATION RULE**
> INDEX integrity is mandatory.
> Filename status must match internal status.
> Update required:
> - at sprint start ritual
> - whenever status changes
> See `/docs/dev/foundation/FOUNDATION_MANUAL.md` → Section 7: Index Discipline.

> **Location:** `/docs/dev/bugs/INDEX_BUGS.md`
> **Naming (required):** `BUG####_<Status>_<three_word_description>.md` in `/docs/dev/bugs/reports/`
> Status values: `OPEN | IN_PROGRESS | FIXED | VERIFIED | DROPPED`
> **Linking convention:** Filename column uses clickable links: `[filename](reports/filename)`

---

## OPEN bugs
| ID | Severity | Status | Title | Area | Filename |
|---:|:--:|:--|---|---|---|
| BUG-0012 | P2 | OPEN | Test workspace cleanup pollution | Testing/Storage | [](reports/BUG0012_OPEN_test_workspace_cleanup.md) |
| BUG-0007 | P1 | FIXED | OpenAI provider test isolation failure | Testing | [](reports/BUG0007_FIXED_openai_test_isolation.md) |
| BUG-0002 | P2 | OPEN | Missing ag run options per CLI reference | CLI | [](reports/BUG0002_OPEN_missing_ag_run.md) |
| BUG-0003 | P2 | OPEN | Missing CLI subcommands per reference spec | CLI | [](reports/BUG0003_OPEN_missing_cli_subcommands.md) |
| BUG-0011 | P2 | OPEN | Default workspace name leaked in error | CLI | [](reports/BUG0011_OPEN_default_workspace_name_leaked.md) |

---

## FIXED bugs
| ID | Severity | Status | Title | Area | Filename |
|---:|:--:|:--|---|---|---|
| BUG-0013 | P1 | FIXED | research_v0 playbook pipeline broken | Playbooks/Runtime | [](reports/BUG0013_FIXED_research_v0_pipeline_broken.md) |
| BUG-0009 | P0 | FIXED | Direct skill skips verifier | CLI/Core/Verifier | [](reports/BUG0009_FIXED_direct_skill_skips_verifier.md) |
| BUG-0010 | P0 | FIXED | Skill trace missing artifacts evidence | Core/Recorder/Skills | [](reports/BUG0010_FIXED_skill_trace_missing_artifacts.md) |
| BUG-0008 | P0 | FIXED | CLI cannot route to strategic_brief skill | CLI / Routing | [](reports/BUG0008_FIXED_skill_routing_missing.md) |
| BUG-0001 | P1 | FIXED | Global CLI options not implemented as global | CLI | [](reports/BUG0001_FIXED_global_cli_options.md) |
| BUG-0004 | P1 | FIXED | SQLite connections not closed → ResourceWarning | Storage | [](reports/BUG0004_FIXED_sqlite_connections_not.md) |
| BUG-0005 | P0 | FIXED | Implicit workspace creation on ag run | CLI/Storage | [](reports/BUG0005_FIXED_implicit_workspace_creation.md) |
| BUG-0006 | P1 | FIXED | Manual mode ignores .env AG_DEV | CLI | [](reports/BUG0006_FIXED_manual_mode_ignores.md) |

---

## How to use
1. Create bug report from `/docs/dev/bugs/templates/BUG_REPORT_TEMPLATE.md`
2. Link bug from PR and/or AF item
3. Update status in:
   - bug filename
   - bug metadata
   - this index

