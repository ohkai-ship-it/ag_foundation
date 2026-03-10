# BACKLOG ITEM - AF0059 - implement_playbooks_list
# Version number: v0.5

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - 1 PR = 1 primary AF
> - INDEX update rule (status <-> filename integrity)

> **File naming (required):** `AF####_<Status>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0059
- **Type:** Feature
- **Status:** DROPPED
- **Priority:** P2
- **Area:** CLI
- **Owner:** Jacob
- **Target sprint:** Sprint08
- **Absorbed by:** AF0076 (Playbooks registry cleanup)

---

## Problem

`ag playbooks list` was originally tracked as a standalone CLI feature.

---

## Resolution

This item was absorbed into **AF0076** during Sprint08.
The intended behavior is implemented via playbooks registry cleanup and list derivation.

---

## Reason for drop

To preserve the 1-primary-AF implementation trail and avoid duplicate tracking for the same shipped behavior.

---

## Notes

- Historical READY/PROPOSED file variants were removed as part of index integrity cleanup.
- Sprint08 review recorded this consolidation as a follow-up action.
