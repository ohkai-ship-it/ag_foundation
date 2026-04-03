# LinkedIn Campaign — Technical Deep Dive Input
# Prepared by: Jeff (via Kai)
# Requested by: Simon (campaign manager)
# Date: 2026-04-01
# Version: 0.1

> Context: Simon and Kai are planning a LinkedIn campaign about ag_foundation across
> two content streams: governance/process and technical architecture. This document
> is Jeff's technical input for the technical stream. All observations are grounded
> in the actual codebase as of Sprint 15.

---

## 1. Vision and Purpose

### What problem does ag_foundation solve that LangChain/CrewAI/AutoGen don't?

The honest answer is: it solves a different problem at a different layer. LangChain
is a toolkit — it gives you components and you assemble them. CrewAI and AutoGen are
agent collaboration frameworks — they coordinate multiple agents toward a shared goal.
ag_foundation is closer to an _auditable runtime_. The primary concern isn't "how do
multiple agents collaborate?" but "how do we know what actually happened, whether the
output was valid, and whether the system told the user the truth about it?"

The design decision that makes this concrete is the Truthful UX invariant: every
label the CLI shows must be derivable from the RunTrace. No "Success" because the
code reached the end of a function. Success because the RunTrace says
`FinalStatus.SUCCESS`. LangChain has no equivalent concept — it delegates that
entirely to the application layer.

### Who is the intended user?

Right now: developers building agents and testing agent behavior. The CLI is the only
interface, manual mode exists explicitly for dev/test, and the governance
documentation (FOUNDATION_MANUAL, SPRINT_MANUAL) is much more developed than any
end-user onboarding material. The architecture explicitly plans for a UI adapter and
IoT event adapter — so the longer-term intended user is anyone consuming agent output
through an interface that isn't the terminal. But that user doesn't exist in the
product yet.

### Two-sentence pitch to a senior engineer

ag_foundation is a modular agent runtime where every component — planner, executor,
verifier, recorder — is a swappable protocol implementation, and every run produces a
typed evidence log that the CLI is contractually prohibited from misrepresenting. It's
not trying to replace LangChain's tool library; it's the layer beneath that ensures
what runs is auditable, recoverable, and honest about what it did.

### 12 months out

If the capability expansion goes as planned — LangChain adapter, MCP bridge,
credentials management, file ops, Wikipedia, then RAG — the system becomes genuinely
useful for personal productivity tasks: research and emit a report, find a document
and summarize it, draft an email. The pipeline intelligence (V3Planner feasibility
assessment, V2Verifier semantic scoring) is already ahead of the skill set. The
bottleneck is breadth of what it can do, not quality of how it reasons. In 12 months
the interesting question is whether the RAG layer is in place to make it useful as a
personal knowledge assistant.

---

## 2. Architecture Observations

### The 3–5 most distinctive architectural decisions

**1. Structural subtyping via `Protocol`, explicitly documented.**

`src/ag/core/interfaces.py` opens with this comment: *"We use typing.Protocol for
structural subtyping (duck typing) rather than abc.ABC for nominal subtyping. This
allows more flexibility and better integration with testing (any object matching the
interface works)."* This isn't incidental — it's a stated design choice. The practical
effect: any object that implements `.plan()`, `.run()`, or `.execute()` with the right
signature works, without inheriting from anything. Test doubles are plain classes with
matching signatures. No mocking framework required for basic substitution.

**2. Additive-only trace schema with per-field attribution.**

Every `Step` model field that was added after the initial schema has an AF reference
comment in the source: `# AF-0049: Evidence references`, `# AF-0094: Full step I/O`,
`# AF-0100: Confirmation status`. And every model has `model_config = {"extra":
"forbid"}`. Combined effect: the schema never silently accepts unknown fields (so
drift shows up as validation errors), and you can trace every field's origin to the
sprint that introduced it. `src/ag/core/run_trace.py` is a living archaeology of the
project's evolution.

**3. Loop bounding as an explicit safety invariant with exported constants.**

`src/ag/core/schema_verifier.py` exports `DEFAULT_MAX_VALIDATION_ATTEMPTS = 3` and
`MAX_VALIDATION_ATTEMPTS_CEILING = 10`, and the docstring says: *"Infinite retry
scenarios are impossible."* The tests import these constants and assert against them.
An infinite loop in an LLM repair cycle is a real operational risk — most systems
just set a `max_retries` variable and hope nobody changes it. Here it's an exported
API with an architectural ceiling and tests that would fail if you raised it past 10.

**4. Pipeline manifest in RunTrace.**

Every trace records which component versions executed it:
`V3Planner → V1Orchestrator → V2Executor → V2Verifier → V0Recorder`. This means you
can look at a trace from three sprints ago and know the exact component mix. Most
frameworks have no equivalent — you know what the code does _now_, not what it did
when this run was recorded. This matters when you're debugging a regression.

**5. Documentation drift as a failing test.**

`tests/test_documentation_drift.py` uses `inspect.getmembers()` to enumerate the
live Protocol classes in `src/ag/core/interfaces.py` and `storage/interfaces.py`,
then asserts each name appears in `CONTRACT_INVENTORY.md`. Same for Pydantic models
vs `SCHEMA_INVENTORY.md`. Documentation going stale is a CI failure here, not a
social norm.

### Component I'm most proud of technically

`src/ag/core/schema_verifier.py` / `src/ag/core/run_trace.py` together. The schema
verifier is unremarkable on the surface — validate, attempt repair if invalid, loop.
What's notable is how the failure evidence is structured: `ValidationAttempt` records
the input data, whether it was valid, what the errors were, and whether repair was
attempted, for every single attempt. When the loop finishes, `ValidationResult` has
the full history. Not just the final verdict — the entire repair narrative. That feeds
directly into the trace, which feeds into the CLI, which can show "attempted 3
repairs, succeeded on attempt 2, field X was corrected." That chain works because the
data model was designed for it from the start.

### Most technical debt

The README. It says "173 tests, 89% coverage" — the actual count is ~783 tests. The
project structure section still describes `runtime.py` as containing "V0 runtime
implementation" but that was refactored in Sprint 13 (AF-0114). A first-time visitor
reading the README gets a picture of the system circa Sprint 08. It's the
highest-visibility surface and it's three phases out of date.

### The pipeline evolution — what broke and what it forced

V0 had two fundamental problems:

V0 _Verifier_ was end-of-run only, and it had no step awareness. BUG-0017 was: the
verifier scanned the final run state for errors, but it didn't know which steps were
required vs optional. A required step could fail, an optional step could succeed, and
the verifier would call it a pass because the final state looked clean. V1Verifier
(Sprint 13, AF-0115) added the `required: bool` field on each step and respects it.

V0 _Executor_ had no output contract. Steps executed, returned a dict, and the result
went directly into the trace. If the skill returned `{"report": "..."}` and the
downstream skill expected `{"content": "..."}`, the pipeline failed at runtime with
an opaque error. V1Executor (Sprint 14, AF-0116) introduced `output_schema`
validation per step. V2Executor (Sprint 15, AF-0124) added LLM repair when schema
validation fails — give the LLM the malformed output and the expected schema, try to
fix it.

### Has Truthful UX ever been painful? Has it caught a real problem?

It's been friction every time a new CLI feature shipped. The natural instinct is to
compute a label from local logic — "we got here, so it succeeded." The invariant
pushes back: what does the trace say?

In practice: BUG-0020 (fixed Sprint 15) is the clearest example. `ag run` reported
success on an empty plan. The pipeline technically succeeded in executing zero steps.
The Truthful UX invariant is why that was a P0 bug rather than an accepted edge case:
the CLI was saying "Success" and displaying a result count, but the RunTrace had no
steps. Fixing it required making the Orchestrator explicitly recognize an empty plan
as a failure condition and recording that in the trace — not patching the CLI output.

---

## 3. Code-Level Highlights

### Single file that best demonstrates the architecture philosophy

`src/ag/core/interfaces.py`. It's ~120 lines, has no implementation, and the opening
docstring explains the structural typing choice and why. Read the five Protocols
(`Planner`, `Orchestrator`, `Executor`, `Verifier`, `Recorder`) and you know the
entire pipeline structure, the data flow, and the design philosophy in under five
minutes. That's intentional.

### Cleanest Protocol + multiple implementations

`Executor` Protocol in `src/ag/core/interfaces.py` → `V0Executor`, `V1Executor`,
`V2Executor` in `executor.py`. Same `.execute(skill_name, parameters, context)`
signature, three entirely different behaviors: V0 calls and returns unchecked, V1
validates against schema with retry, V2 validates + attempts LLM repair + emits
`ExecutionMetadata` to the trace. No inheritance between them. The runtime wires in
whichever one is configured.

### What a RunTrace looks like in practice

A representative multi-step research run:

```json
{
  "run_id": "b0f76c50-...",
  "pipeline": "V3Planner → V1Orchestrator → V2Executor → V2Verifier → V0Recorder",
  "planning": {
    "planner": "V3Planner",
    "feasibility_level": "fully_feasible",
    "feasibility_score": 0.92,
    "llm_call": {"model": "gpt-4o-mini", "total_tokens": 1240},
    "feasibility_llm_call": {"model": "gpt-4o-mini", "total_tokens": 385},
    "raw_plan_steps": [...]
  },
  "steps": [
    {
      "step_number": 0, "step_type": "skill_call", "skill_name": "web_search",
      "input_data": {"query": "Little Tokyo Los Angeles", "max_results": 5},
      "output_data": {"urls": [...], "results": [...], "total_results": 5},
      "duration_ms": 1240, "required": true, "confirmation": null
    },
    {
      "step_number": 1, "step_type": "skill_call", "skill_name": "fetch_web_content",
      "input_data": {"urls": [...]}, "output_data": {"pages": [...], "failures": []},
      "required": true
    },
    {
      "step_number": 2, "step_type": "skill_call", "skill_name": "synthesize_research",
      "output_data": {
        "report": "...", "key_findings": [...], "sources_used": [...], "source_count": 3
      },
      "output_data.repair_result": {
        "repaired_output": {...}, "fields_changed": ["key_findings"],
        "repair_tokens": 1116, "repair_model": "gpt-4o-mini-2024-07-18"
      }
    }
  ],
  "verifier": {
    "status": "passed",
    "evidence": {
      "semantic": {
        "relevance_score": 0.85, "completeness_score": 0.72, "consistency_score": 0.91,
        "overall_pass": true, "llm_tokens_used": 832
      }
    }
  },
  "llm": {"call_count": 4, "total_tokens": 8099},
  "final": "success"
}
```

### Most interesting test in the suite

`tests/test_documentation_drift.py::TestContractInventoryDrift::test_core_interfaces_documented`.
It imports `ag.core.interfaces`, calls `inspect.getmembers(interfaces, inspect.isclass)`
to find all Protocol classes at runtime, then asserts every Protocol name exists as a
substring in `CONTRACT_INVENTORY.md`. If you add a Protocol to
`src/ag/core/interfaces.py` without documenting it, the test fails. Not a lint rule,
not a human review convention — a failing pytest. This is the kind of test that only
appears in a codebase where documentation hygiene is treated as a first-class
engineering concern.

---

## 4. Repository Readiness for Open Source

### Is the code in a state you'd be comfortable with strangers reading?

The core package (`src/ag`) is in good shape for a stranger to read. The layer
separation is real, the code is clean, ruff enforces style, the Protocol
documentation is honest. I wouldn't be embarrassed.

The test suite is excellent by any measure — 783 tests, 87% coverage, tests that
enforce documentation synchronization. That's unusual for a project at this stage
and it's genuinely impressive to show externally.

Rough edges:
- `runtime.py` still describes itself as a "V0 runtime implementation" in old
  docstrings even though it's now the composition root after Sprint 13's refactor
  (AF-0114)
- The sprint documentation in `docs/dev/sprints` is extensive and honest, including
  bugs, review evidence, and decision trails — that's valuable but may read as unusual
  to an outsider who expects `docs` to be user-facing guides

### README assessment

Not adequate for a first-time visitor. Three specific problems:

1. **Stale test count**: says "173 tests, 89% coverage" — the actual number is ~783
   tests, 87% coverage. This is the first thing a skeptical engineer checks.
2. **Project structure is Sprint 08**: shows `runtime.py — V0 runtime implementation`
   as the core file. The refactor in AF-0114 split that into `executor.py`,
   `verifier.py`, `orchestrator.py`, `recorder.py`.
3. **No "what is this for" narrative**: the one-liner is "Modular agent network core
   runtime with LLM provider abstraction and multi-step delegation." That describes
   the mechanism but not the value.

### Hardcoded paths, API keys, personal references

None found in `src`. API keys are read from environment variables only
(`os.environ.get(OPENAI_API_KEY_ENV)`), with no fallback values. `.env.example` is
present and clean. `pyproject.toml` author is `"ag_foundation team"` — no personal
name.

**One flag**: the `htmlcov` directory is present in the workspace and listed in
`.gitignore`. Needs verification that it's not currently committed.

**Missing**: no `LICENSE` file at the repo root. The license is declared as `"MIT"`
in `pyproject.toml`, but PyPI and GitHub both look for a `LICENSE` file. This must be
created before going public.

### Ranked "repo polish" list before publication

1. **Add `LICENSE` file** — MIT text, required for open source
2. **Fix README** — update test count, update project structure to post-Sprint 13
   reality, add a "why does this exist" paragraph
3. **Verify `htmlcov` is not committed** — remove from tree if it is
4. **README Quick Start** — clarify what "manual mode" means for a newcomer
5. **`ARCHITECTURE.md`** — some "current state" boxes reference Sprint 08 reality
   despite V1Orchestrator shipping in Sprint 14

### Dependencies and licenses

`typer`, `pydantic`, `rich`, `python-dotenv`, `httpx`, `ddgs` — all MIT-compatible.
`openai` in optional extras. No dependencies with viral licenses (GPL, AGPL). Clean.

---

## 5. The ag_foundation Story

### Most interesting technical turning point

Sprint 13, AF-0114: extracting the monolithic `runtime.py` into separate files. On
the surface it looks like a boring refactor. In practice it was the moment the
architecture became real. Before that, V0Planner, V0Orchestrator, V0Executor,
V0Verifier, and V0Recorder all lived in `runtime.py` together — the "modular
pipeline" was a conceptual claim, not a structural one.

AF-0114 forced every component to define its inputs and outputs cleanly because they
now lived in separate files with explicit imports. The Protocol interfaces in
`src/ag/core/interfaces.py` went from aspirational documentation to the actual
contracts those files enforced. The V1/V2 upgrade path became credible because each
component was now genuinely replaceable. Every subsequent sprint (V2Executor's LLM
repair, V2Verifier's semantic checks, V3Planner's feasibility assessment) was only
clean to ship because that extraction happened.

### Three blog post takeaways: "What I learned building an agent runtime from scratch"

**1. "The trace is the source of truth, not the code."**
The decision to make CLI labels derive from RunTrace rather than from local variables
seems pedantic until the first time you catch a bug where the code reaches success but
the agent didn't actually do what you asked. Building the discipline early is cheap.
Retrofitting it is expensive.

**2. "Versioned components beat feature flags."**
Every pipeline component evolves through V0 → V1 → V2, and old versions stay in the
code. V0Orchestrator runs in tests. V1Orchestrator runs in production. When V2 ships,
you don't delete V0 — you just update the composition root to wire in V2. This means
you can reproduce any historical run by spinning up the exact component mix that
executed it. You can't do that with feature flags.

**3. "Loop bounding is an architecture decision, not a parameter."**
The first time a repair loop in an LLM pipeline runs 47 times and burns $3 in tokens,
you add a retry limit. But where? In the calling code? In a config file?
ag_foundation puts it in a module-level constant (`DEFAULT_MAX_VALIDATION_ATTEMPTS =
3`, `MAX_VALIDATION_ATTEMPTS_CEILING = 10`), exports both constants from the module's
public API, and tests assert against them. If someone changes the ceiling, the test
fails, and the commit author has to justify why. That's a different level of
seriousness than a config value.

### What's underappreciated

The `model_config = {"extra": "forbid"}` on every Pydantic model. It's five words
per class and it doesn't appear in any documentation. What it does: if any code tries
to pass a field that isn't declared in the schema, Pydantic raises a `ValidationError`
immediately. In a pipeline where data flows between components as dicts, this is the
difference between silent field loss and a loud failure at the boundary.

It means you can't accidentally introduce a field in V2Executor's output that
V1Verifier silently ignores — one of them will reject it. This constraint is why the
additive-only schema evolution works. Without it, adding fields would be safe but
deleting or renaming them would be invisible. The combination of `extra = "forbid"` +
additive-only policy means the schema is honest — every field that exists is declared,
and every declared field is meaningful.

---

*Jeff — 2026-04-01*
