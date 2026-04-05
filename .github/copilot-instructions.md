# Copilot Instructions — ag_foundation

## ToDo List Discipline

When working on an AF (Action Feature), always create a ToDo checklist:

1. **Title format:** `AF-####: <AF Title>` — the AF ID must be clearly visible
2. **Granularity:** Break the AF into concrete, actionable sub-tasks (3–8 items typical)
3. **Status tracking:**
   - Mark a task as **in-progress** before starting work on it
   - Mark it as **completed** immediately after finishing
   - Only **one** task should be in-progress at a time
4. **Persistence:** The ToDo list should be maintained throughout the AF implementation
5. **Sprint-level tracking:** At sprint start, create a high-level ToDo with all AFs in scope

## Testing Workflow

- During AF development: run only the specific test file related to the change
  - Example: `pytest tests/test_runtime.py -x -q` — not the full suite
- Full suite (`pytest -W error`) only before each commit (full CI gate)
- Keep test runs targeted and fast

## Governance References

- Foundation rules: `/docs/dev/foundation/FOUNDATION_MANUAL.md`
- Sprint execution: `/docs/dev/foundation/SPRINT_MANUAL.md`
- HITL Framework: FOUNDATION_MANUAL §10
