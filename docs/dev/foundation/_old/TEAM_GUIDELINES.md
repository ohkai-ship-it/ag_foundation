# DEPRECATED — see FOUNDATION_OPERATING_MANUAL.md

> **This document is deprecated.**
> All rules have been consolidated into:
> `/docs/dev/foundation/FOUNDATION_OPERATING_MANUAL.md`
>
> This file is retained for historical reference only.
> Do not update this file. Update the operating manual instead.

---

# Team Guidelines (ag_foundation)
# Version number: v0.2 (DEPRECATED)
# Effective date: 2026-03-03

> **See also:**
> - `/docs/dev/foundation/FOUNDATION_OPERATING_MANUAL.md` — unified operating rules
> - `/docs/dev/foundation/SPRINT_EXECUTION_PLAYBOOK.md` — step-by-step sprint execution

This document consolidates collaboration norms and role responsibilities.

## Roles
### Kai — Product Manager (human-in-the-loop)
- Owns: priorities, scope, acceptance criteria, release decisions
- Reviews: product-facing behavior, UX, scope boundaries

### Jeff — Senior Engineer / Architect
- Owns: architecture invariants, interface contracts, risk identification
- Reviews: P1+ changes, trace truthfulness, modularity, safety hooks

### Jacob — Implementer
- Owns: PR-sized implementation, tests, evidence, index updates
- Responsibilities:
  - self-checks before PR
  - keep docs current when touched
  - escalate early when blocked

## Communication norms
- Keep decisions explicit (PR notes, ADRs, or sprint review).
- No “quick & dirty” implementation shortcuts without asking Kai/Jeff first.
- When uncertain: propose options + recommend one.

## Review expectations
- One PR maps to exactly one primary AF item.
- Behavior changes require evidence (tests + RunTrace ID).
- Jeff must review architecture-meaningful changes.
- Kai must review product-facing behavior and workflow changes.
