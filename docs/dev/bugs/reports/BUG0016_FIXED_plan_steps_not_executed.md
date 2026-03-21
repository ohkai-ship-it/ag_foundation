# BUG REPORT — BUG-0016 — plan steps not executed
# Version number: v0.2

---

## Metadata
- **ID:** BUG-0016
- **Status:** FIXED
- **Severity:** P1
- **Area:** Core Runtime | Orchestrator
- **Reported by:** Kai
- **Date:** 2026-03-20
- **Fixed:** 2026-03-21
- **Related backlog item(s):** AF-0099 (--plan execution)
- **Related ADR(s):** —
- **Related PR(s):** —

---

## Summary
When executing a pre-generated plan via `ag run --plan`, the runtime ignores the plan's `planned_steps` and instead executes the default playbook (echo skill only). The plan generation correctly identifies the needed skills (web_search, fetch_web_content, summarize_docs, emit_result), but execution bypasses them entirely.

---

## Expected behavior
`ag run --plan plan_5a5575893295 -w tasks02` should:
1. Load the plan's `planned_steps` array
2. Execute each step in sequence (web_search → fetch_web_content → summarize_docs → emit_result)
3. Produce actual weather information output

---

## Actual behavior
- Only the `echo` skill from the default playbook is executed
- No web search, no fetch, no summarization occurs
- Run completes as "success" with no meaningful output
- Plan status updated to EXECUTED despite not executing plan steps

---

## Reproduction steps
1. Generate a plan: `ag plan generate --task "Weather düsseldorf today" --workspace tasks02`
2. Observe planned steps: web_search, fetch_web_content, summarize_docs, emit_result
3. Execute: `ag run --plan plan_5a5575893295 -w tasks02`
4. Check trace: only echo skill was called

---

## Evidence
- **RunTrace ID(s):** `eb43f355-2532-4f0a-abe0-ffbb3a54aa3a`
- **CLI output:**
```
Executing plan: plan_5a5575893295
Task: Weather düsseldorf today...
Steps: 4

Plan executed
  Plan ID: plan_5a5575893295
  Run ID: eb43f355-2532-4f0a-abe0-ffbb3a54aa3a
  Workspace: tasks02
  Mode: guided (pre-approved plan)
  Status: success
  Verifier: passed
  Duration: unknown
  Playbook: default_v0@1.0.0  <-- Should be research_v0 or plan-derived
```
- **Environment:** Windows, Python 3.14.0, Sprint 11 branch

---

## Impact
- **Severity:** P1 — Core AF-0099 feature is non-functional
- **Users affected:** Anyone using guided autonomy workflow
- **Workaround:** None (--plan flag is unusable)

---

## Suspected cause
The CLI loads the plan and extracts `loaded_plan.playbook.name` but passes it to `runtime.execute()` which then goes through `V0Planner.plan()` which ignores the passed playbook name and returns its own selection. The `planned_steps` from the ExecutionPlan are never converted into actual skill invocations.

Relevant code path (main.py ~785-790):
```python
trace = runtime.execute(
    prompt=loaded_plan.task_prompt,
    workspace=resolved_workspace,
    mode=mode,
    playbook=loaded_plan.playbook.name,  # <-- This is ignored
    workspace_source=workspace_source,
)
```

The runtime's `V0Planner` doesn't use the `playbook` parameter to select the right playbook, and even if it did, the `planned_steps` contain specific skill sequences that differ from static playbook definitions.

---

## Proposed fix
1. **Short-term:** Modify `V0Planner.plan()` to respect the `playbook` parameter when provided
2. **Long-term:** Create a dynamic playbook from `ExecutionPlan.planned_steps` that the orchestrator can execute

The fix requires either:
- A new code path that converts `PlannedStep[]` → `PlaybookStep[]` for execution, OR
- A runtime mode that directly executes planned steps without going through static playbook lookup

---

## Acceptance criteria (for verification)
- [ ] `ag run --plan <id>` executes the skills listed in `planned_steps`
- [ ] Trace shows web_search, fetch_web_content, summarize_docs, emit_result steps
- [ ] Output contains actual fetched/synthesized content
- [ ] Test coverage for plan step execution
