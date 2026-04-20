# PROJECT ROADMAP — <project_name>
#### Description: Template for project roadmaps. A project roadmap is a strategic planning document defining long-term phases, milestones, and priorities. Updated at phase boundaries and major scope shifts. Copy into the consumer's docs/project/ folder, rename, and fill all sections.
#### Convergent: v1.3.2
#### File version: 0.1
#### governs: <project_name>

---

> **FOUNDATION GOVERNANCE**
> This file is governed by: `foundation/SPRINT_PLAYBOOK.md`
> This is a strategic planning document. Update at phase boundaries and major scope shifts.

---

## 1) Executive Summary

One paragraph: what the project is, why it exists now, and what this roadmap covers (and doesn't cover).

---

## 2) Vision

What does success look like when this project is "done" (or mature)? Frame the capabilities, not the implementation.

**Design principle:** <one sentence that constrains all design choices>

---

## 3) Current State

Where is the project today? Summarize components, their maturity, and known gaps.

| Component | Location / Status | Version |
|-----------|-------------------|---------|
| <component> | <path or status> | <version> |
| <component> | <path or status> | <version> |

**Known issues at time of writing:**
- ...
- ...

---

## 4) Architecture

### 4.1 High-Level Model

Describe the system's structural model. Use whatever abstraction fits: server/client, layers, pipeline stages, plugin model, etc.

### 4.2 Key Boundaries

What are the hard boundaries the architecture enforces? (Examples: layer separation, workspace isolation, interface-first, no cross-component leakage.)

### 4.3 Consumer Model

If this project is consumed by other projects: how do consumers adopt it? What do they get vs. what do they provide?

*(Remove §4.3 if not applicable.)*

---

## 5) Phased Roadmap

### Phase 0 — <name>
**Theme:** ...
**Deliverables:**
- [ ] ...
- [ ] ...

### Phase 1 — <name>
**Theme:** ...
**Deliverables:**
- [ ] ...
- [ ] ...

### Phase 2 — <name>
**Theme:** ...
**Deliverables:**
- [ ] ...
- [ ] ...

### Phase 3 — <name> (Future)
**Theme:** ...
**Deliverables:**
- [ ] ...
- [ ] ...

*(Add or remove phases as needed. Each phase should have a clear theme and concrete deliverables.)*

---

## 6) Success Criteria

How do you know the roadmap is progressing? Define measurable or verifiable criteria per phase.

| Phase | Criterion | Target | Status |
|-------|-----------|--------|--------|
| 0 | <what to measure> | <target value> | NOT STARTED / MET |
| 1 | <what to measure> | <target value> | NOT STARTED / MET |
| 2 | <what to measure> | <target value> | NOT STARTED / MET |

---

## 7) Open Decisions

Strategic decisions not yet made. Track them here; convert to ADRs when resolved.

| # | Question | Impact | Status |
|---|----------|--------|--------|
| 1 | <decision question> | <what it affects> | OPEN / DECIDED |
| 2 | <decision question> | <what it affects> | OPEN / DECIDED |

---

## 8) Immediate Next Steps

Ordered list of what happens next. Keep this short — details live in sprint descriptions.

1. ...
2. ...
3. ...

---

## References

- Project control: `docs/project/PROJECT_CONTROL.md` <!-- generic name — use highest version on disk -->
