# INDEX_BACKLOG
#### Description: Template for the backlog index file. INDEX_BACKLOG is the master registry tracking all AFs by status, priority, sprint assignment, and ownership. INDEX row status must always match the internal Status field in the corresponding AF file. Update points are defined in the Sprint Playbook.
#### Convergent: v1.3.2
#### governs: <project_name>

> **FOUNDATION RULE**
> INDEX integrity is mandatory.
> Status must match between internal file metadata and INDEX row.
> SP defines update points per phase.

---

## How to use
1. Create AFs from `foundation/templates/BACKLOG_ITEM_TEMPLATE.md`
2. Update status below

---

## Backlog (unprioritized) *KEEP ALWAYS ON TOP*
| ID | Priority | Status | Name (short) | Area | Owner | Link |
|---:|:--:|:--|---|---|---|---|
| AF#### | P# | PROPOSED | <name> | <area> | <owner> | [🔗](files/backlog/<filename>.md) |

---

## Done — No scope (inter-sprint)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF#### | P# | PROPOSED | <name> | <area> | <owner> | [🔗](files/backlog/<filename>.md) |

---

## Sprints *IN DESCENDING ORDER*

### Proposed

### Sprint XX Scope (<sprint_name>)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|

### Sprint ## Scope (<sprint_name>)
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF#### | P# | PROPOSED | <name> | <area> | <owner> | [🔗](files/backlog/<filename>.md) |

---

## Blocked
| Order | ID | Priority | Status | Name (short) | Area | Owner | Link |
|:--:|---:|:--:|:--|---|---|---|---|
| 1 | AF#### | P# | PROPOSED | <name> | <area> | <owner> | [🔗](files/backlog/<filename>.md) |

---

## Deprecated *KEEP ALWAYS AT BOTTOM*
| ID | Priority | Status | Name (short) | Area | Owner | Link |
|---:|:--:|:--|---|---|---|---|
| AF#### | P# | DEPRECATED | <name> | <area> | <owner> | [🔗](files/backlog/<filename>.md) |

---

## References

- Sprint execution: `foundation/SPRINT_PLAYBOOK.md`