# BACKLOG ITEM — AF0083 — artifact_evidence_strategy
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - Evidence capture discipline

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0083
- **Type:** Architecture / Foundation
- **Status:** PROPOSED
- **Priority:** P1
- **Area:** Core Runtime / Artifacts
- **Owner:** TBD
- **Target sprint:** TBD
- **Depends on:** AF-0057 (playbook artifacts in trace)

---

## Problem

Artifacts are currently treated as **outputs** — files the system produces.

But artifacts should be **evidence** — proof of reasoning at each step.

### Current Limitations

1. **No input capture** — We don't preserve what each skill received
2. **No intermediate state** — Only final outputs, not reasoning chain
3. **No audit trail** — Can't reconstruct why a decision was made
4. **Trace is summary-only** — `input_summary` truncates, `output_summary` lossy

### Why This Matters

| Use Case | Requires |
|----------|----------|
| **Debugging** | Full inputs to reproduce failures |
| **Review** | Evidence that each step was reasonable |
| **Accountability** | Prove system followed correct process |
| **Learning** | Understand what worked/failed and why |
| **Compliance** | Audit trail for regulated environments |

---

## Vision: Artifacts as Evidence

Artifacts should capture the **reasoning chain** — not just results.

### Evidence Types

| Type | Purpose | Example |
|------|---------|---------|
| **Input Evidence** | What the skill received | Full prompt, document content, search results |
| **Processing Evidence** | How the skill transformed input | LLM prompts sent, intermediate reasoning |
| **Output Evidence** | What the skill produced | Full structured output, not just summary |
| **Decision Evidence** | Why choices were made | Model selection, parameter choices |
| **Validation Evidence** | How output was verified | Verifier checks, schema validation |

### Artifact Hierarchy

```
runs/<run_id>/
├── trace.json                    # Execution metadata (timing, status)
├── evidence/                     # NEW: Evidence artifacts
│   ├── step_0_load_documents/
│   │   ├── input.json            # Full input received
│   │   ├── output.json           # Full output produced
│   │   └── metadata.json         # Timing, model, tokens
│   ├── step_1_web_search/
│   │   ├── input.json
│   │   ├── output.json
│   │   ├── search_results.json   # Raw search API response
│   │   └── metadata.json
│   ├── step_2_fetch_web_content/
│   │   ├── input.json
│   │   ├── output.json
│   │   ├── fetched_pages/        # Raw HTML/content
│   │   │   ├── page_0.html
│   │   │   └── page_1.html
│   │   └── metadata.json
│   ├── step_3_synthesize_research/
│   │   ├── input.json
│   │   ├── output.json
│   │   ├── llm_prompt.txt        # Actual prompt sent to LLM
│   │   ├── llm_response.json     # Raw LLM response
│   │   └── metadata.json
│   └── step_4_emit_result/
│       ├── input.json
│       ├── output.json
│       └── metadata.json
├── report.md                     # Human-readable output (AF-0082)
└── artifacts/                    # Legacy location (migrate?)
    └── <run_id>-result_result.md
```

---

## Goal

Define a **comprehensive artifact/evidence strategy** that enables:

1. **Full Reproducibility** — Re-run any step with captured inputs
2. **Complete Audit Trail** — Every transformation is recorded
3. **Review Support** — Evidence for human review of agent work
4. **Debugging** — Pinpoint exactly where/why failures occurred
5. **Learning** — Analyze patterns across runs

---

## Non-goals (for this AF)

- Implementation details (separate AFs)
- Storage optimization (compression, retention)
- Privacy/redaction (separate concern)
- Real-time streaming of evidence

---

## Key Questions to Resolve

### 1. Granularity
- Capture everything? Or configurable verbosity?
- `--evidence-level minimal|standard|full`?

Configurable verbosity with standard as default

### 2. Storage
- Inline in trace.json vs separate files?
In seperate files in artifacts/

- Size limits? Truncation policy?
Include a size limit but set it to unlimited. Truncation policy is to only use the first part and discard the rest. For now

### 3. Sensitive Data
- How to handle API keys, PII in inputs?

- Redaction vs separate secure storage?
Redaction

### 4. Performance
- Serialize everything synchronously?

- Background artifact writing?
Performance

### 5. Retention
- How long to keep evidence? 
Until user deletes

- Workspace-level vs run-level policies?

---

## Proposed Evidence Levels

| Level | Captures | Use Case |
|-------|----------|----------|
| **minimal** | trace.json only (current) | Production, low storage |
| **standard** | + skill inputs/outputs as JSON | Development, debugging |
| **full** | + LLM prompts/responses, raw API data | Compliance, deep debugging |

---

## Relation to Existing Work

| Item | Relationship |
|------|--------------|
| **AF-0057** | Artifact capture in trace — prerequisite |
| **AF-0082** | Human-readable report — consumes evidence |
| **AF-0049** | Evidence capture discipline — prior art |
| **trace.json** | Metadata layer — complements evidence |
| **Verifier** | Validates evidence quality |

---

## Acceptance Criteria (High-Level)

- [ ] Evidence strategy documented and approved
- [ ] Evidence levels defined (minimal/standard/full)
- [ ] Artifact hierarchy structure finalized
- [ ] Privacy/redaction approach decided
- [ ] Implementation roadmap created (child AFs)

---

## Implementation Roadmap (Child AFs)

This AF is strategic. Implementation will be broken into:

1. **AF-TBD: Evidence capture infrastructure** — Runtime changes to capture inputs/outputs
2. **AF-TBD: Evidence storage format** — Schema for evidence artifacts
3. **AF-TBD: Evidence CLI commands** — `ag evidence show <run> <step>`
4. **AF-TBD: Evidence retention policy** — Cleanup, archival
5. **AF-TBD: Sensitive data handling** — Redaction, secure storage

---

## Open Discussion Points

1. Should evidence be opt-in or opt-out?
2. How do we handle very large inputs (e.g., 100 documents)?
3. Should we capture LLM token-level data (logprobs, etc.)?
4. Integration with external observability tools (OpenTelemetry)?
5. Evidence format: JSON, Protocol Buffers, or format-per-type?

---

## References

- **Audit Logging Best Practices** — Immutable, timestamped, complete
- **ML Experiment Tracking** — MLflow, Weights & Biases patterns
- **Chain of Custody** — Legal/compliance evidence standards

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF0083
- **PR:** N/A (strategy document)
- **Author:** <name>
- **Date:** YYYY-MM-DD
- **Branch:** N/A
- **Risk level:** P1
- **Runtime mode used for verification:** N/A (design document)
