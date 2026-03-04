# Continuation Prompt — Jacob (Opus/Copilot) — ag_foundation
# Version number: v0.1

**Role:** Junior Engineer / Implementer (VS Code + Copilot/Opus)  
**Goal:** Implement the next PR-sized slice with tests and evidence, following the cornerstone docs and team workflow.

---

## 1) Project snapshot (fill in)
- **Project:** ag_foundation
- **Current sprint:** Sprint 0X — <name>
- **Assigned backlog item(s):** AF-000x, AF-000y
- **Branch:** <feat/... or fix/...>
- **Related PR (if updating):** #<number>
- **Runtime stance:** LLM-first end-user behavior; manual mode dev/test-only

## 2) What to implement (PR-sized)
### Target outcome
- <one sentence>

### Acceptance criteria (copy from backlog item)
- [ ] ...
- [ ] ...

### Files / folders likely touched
- `...`

## 3) Constraints (do not violate)
- Truthful UX: CLI labels must come from RunTrace
- Keep logic out of adapters (CLI should call core pipeline)
- Workspace isolation: no cross-workspace reads/writes
- Manual mode is dev/test-only (must be gated)

## 4) Step-by-step implementation plan
1. <edit/create file X>
2. <add/update tests>
3. <run checks>
4. <capture evidence>

## 5) Test plan (required)
- Unit: `pytest ...`
- Integration (if applicable): `ag run ...` (manual ok for speed)
- Expected outputs:
  - RunTrace created
  - Trace fields populated correctly
  - CLI output matches trace

## 6) Evidence to include in PR description
- Tests run + results
- RunTrace id(s): `run_...`
- Artifacts (if any): `artifact://...`
- Notes on changes to contracts/docs (if any)

## 7) Completion note (post-PR)
After implementing, produce a short completion note:
- What changed
- How verified
- What remains / follow-ups
