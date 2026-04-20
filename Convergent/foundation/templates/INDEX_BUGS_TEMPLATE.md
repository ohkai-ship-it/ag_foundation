# INDEX_BUGS
#### Description: Template for the bug index file. INDEX_BUGS is the master registry tracking all BUGs by status, priority, sprint assignment, and ownership. INDEX row status must always match the internal Status field in the corresponding BUG file. Update points are defined in the Sprint Playbook.
#### Convergent: v1.3.2
#### governs: <project_name>

> **FOUNDATION RULE**
> INDEX integrity is mandatory.
> Status must match between internal file metadata and INDEX row.
> SP defines update points per phase.

---

## How to use
1. Create bug report from `foundation/templates/BUG_REPORT_TEMPLATE.md`
2. Link bug from PR and/or AF item
3. Update status below

---

## Proposed
| ID | Priority | Status | Name (short) | Area | Owner | Link |
|---:|:--:|:--|---|---|---|---|
| BUG#### | P# | PROPOSED | <name> | <area> | <owner> | [🔗](files/bugs/<filename>.md) |

---

## Ready
| ID | Priority | Status | Name (short) | Area | Owner | Link |
|---:|:--:|:--|---|---|---|---|
| BUG#### | P# | READY | <name> | <area> | <owner> | [🔗](files/bugs/<filename>.md) |

---

## Done
| ID | Priority | Status | Name (short) | Area | Owner | Link |
|---:|:--:|:--|---|---|---|---|
| BUG#### | P# | DONE | <name> | <area> | <owner> | [🔗](files/bugs/<filename>.md) |

---

## Blocked
| ID | Priority | Status | Name (short) | Area | Owner | Link |
|---:|:--:|:--|---|---|---|---|
| BUG#### | P# | BLOCKED | <name> | <area> | <owner> | [🔗](files/bugs/<filename>.md) |

---

## Deprecated *KEEP ALWAYS AT BOTTOM*
| ID | Priority | Status | Name (short) | Area | Owner | Link |
|---:|:--:|:--|---|---|---|---|
| BUG#### | P# | DEPRECATED | <name> | <area> | <owner> | [🔗](files/bugs/<filename>.md) |

---

## References

- Sprint execution: `foundation/SPRINT_PLAYBOOK.md`

