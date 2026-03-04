# RunTrace Schema Change Playbook (P1+) — ag_foundation
# Version number: v0.1

Use this playbook any time the `RunTrace` contract changes.

## 1) Define the change
- Which fields are added/removed/renamed?
- Why is the change needed?
- What features depend on it?

## 2) Decide compatibility strategy
Choose one:
- **Additive only (preferred):** add new fields, keep old ones
- **Version bump:** introduce `run_trace_version` and handle both
- **Migration:** provide a migration script/tool (avoid unless necessary)

## 3) Update docs (mandatory)
- Update `/docs/dev/cornerstone/ARCHITECTURE.md` trace section
- If CLI output labels change: update `/docs/dev/cornerstone/CLI_REFERENCE.md`

## 4) Implement in safe slices
1) PR1: Add new fields + populate them (keep old)
2) PR2: Switch readers/labels to new fields
3) PR3: Remove old fields only if versioned/migrated and explicitly approved

## 5) Tests (mandatory)
- Contract tests for schema presence and types
- Integration test: `ag run ...` produces trace with new fields
- Assertion: CLI labels are derived from the new fields (truthful UX)

## 6) Evidence (mandatory)
- Capture at least 1 run trace ID showing the new fields populated
- Add a review entry summarizing the verification steps

## 7) Done criteria
- Trace schema documented and tested
- No hardcoded CLI claims introduced
- Backwards compatibility addressed explicitly
