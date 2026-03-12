# BACKLOG ITEM — AF0092 — evidence_cli_commands
# Version number: v0.2

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0092
- **Type:** Feature
- **Status:** DROPPED
- **Priority:** —
- **Area:** CLI / Evidence
- **Owner:** —
- **Target sprint:** —
- **Depends on:** —

---

## Drop reason

Dropped before implementation. AF-0090 (v0.3) concluded that a separate
`evidence/` directory tree is unnecessary — the existing artifact system
and enriched trace.json cover all audit/debug needs. Therefore dedicated
`ag evidence list/show` CLI commands have no data to operate on.

Existing `ag artifacts list/show` commands (part of AF-0012 CLI surface
parity) serve the same purpose once artifact metadata is truthful.

---

## Original scope (for reference)

Would have added `ag evidence list <run_id>` and `ag evidence show <run_id> <step>`
to display step-level evidence files. Superseded by the decision to enrich
trace.json and use the artifacts system instead of a parallel evidence hierarchy.
