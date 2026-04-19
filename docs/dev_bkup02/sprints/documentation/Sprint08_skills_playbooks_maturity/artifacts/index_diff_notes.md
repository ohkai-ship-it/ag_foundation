# Sprint 08 Review - Index Diff Notes
# Date: 2026-03-09
# Executor: Jacob

## INDEX_BACKLOG.md Changes

### Sprint 08 Scope (corrected)
| Order | AF | Status | Title | Notes |
|:--:|---:|:--:|---|---|
| 1 | AF-0073 | DONE | Index file linking | ✅ File exists |
| 2 | AF-0079 | DONE | Skills framework V1 removal | ✅ File exists |
| 3 | AF-0074 | DONE | research_v0 playbook | ✅ File exists |
| 4 | AF-0059 | DONE | Implement playbooks list | ❌ DONE file missing |
| 5 | AF-0076 | DONE | Playbooks registry cleanup | ✅ File exists |
| 6 | AF-0069 | DONE | Skills architecture documentation | ✅ File exists |
| 7 | AF-0070 | DONE | Playbooks architecture documentation | ✅ File exists |

### Issues Found

#### Issue 1: AF-0059 File Status Mismatch
- **INDEX_BACKLOG.md** references `AF0059_DONE_implement_playbooks_list.md`
- **Actual files:**
  - `AF0059_Proposed_implement_playbooks_list.md` (old)
  - `AF0059_READY_implement_playbooks_list.md` (old)
- **No DONE file exists**

**Resolution options:**
1. Create `AF0059_DONE_implement_playbooks_list.md` marking it done (if truly complete)
2. Mark AF-0059 as DROPPED (absorbed into AF-0076)
3. Fix INDEX to remove AF-0059 from Sprint 08 scope

**Recommendation:** Option 2 - AF-0059 functionality was absorbed into AF-0076.
The `ag playbooks list` command is implemented in AF-0076.

#### Issue 2: Duplicate AF Files
These old files should be deleted:
- `AF0059_Proposed_implement_playbooks_list.md`
- `AF0059_READY_implement_playbooks_list.md`
- `AF0069_PROPOSED_skills_registry_deep_dive.md`
- `AF0070_PROPOSED_playbooks_registry_deep_dive.md`
- `AF0079_IN_PROGRESS_skills_framework_v1_removal.md`

## INDEX_BUGS.md Changes
- Added BUG-0013 (research_v0 pipeline broken) to OPEN section
- Index correctly updated

## ARCHITECTURE.md Changes
- Added §3.3 skill inventory and "How to add skills"
- Added §5.3 playbook inventory and "How to add playbooks"
- Documented "Skills = Capabilities" principle
