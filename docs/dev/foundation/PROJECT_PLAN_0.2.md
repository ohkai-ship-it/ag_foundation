# ag_foundation --- Project Plan
# Version number: v1.0
# Updated: 2026-03-21

------------------------------------------------------------------------

## Purpose

ag_foundation builds a modular agent network core that can plan,
execute, verify, and learn from runs.
IoT integration, web/app UI, and other sensors/data sources are later
integrations; the foundation must make those easy to attach.

The current phase prioritizes reliability and safety hardening for
bounded autonomy. Skills are established, but autonomy expansion now
depends on enforcement, resilience, and governance quality gates.

------------------------------------------------------------------------

# Current State Summary (after Sprint 12)

The system has:

-  Modular runtime with clear layered architecture
-  Trace-contract enforcement and truthful UX discipline
-  Workspace isolation and explicit workspace selection policy
-  CI discipline (ruff + pytest -W error + coverage)
-  Skill framework v2 and working playbooks (`summarize_v0`, `research_v0`)
-  Architecture and inventory documentation synchronized (schemas/contracts)
-  Policy hooks with enforcement (AF-0087)
-  Plugin architecture foundation (skills entry points, YAML playbooks)
-  Gate A (Reliability) PASSED
-  Gate B (Guided Autonomy) PASSED
-  Guided autonomy with plan preview and approval (`ag plan`, `ag run --plan`)
-  V1Planner with multi-output plans and accumulated chaining
-  Run-centered storage layout (runs/<id>/result.md, trace.json, artifacts/*)
-  Unified summarization pipeline (synthesize_research)
-  Strict content emission validation (emit_result)
-  Autonomy mode visibility in CLI and trace

Canonical governance documents:

- `/docs/dev/foundation/FOUNDATION_MANUAL.md`
- `/docs/dev/foundation/SPRINT_MANUAL.md`

Key shift:
Guided autonomy is operational and hardened. Next priority: LLM-powered
pipeline intelligence (smarter plans, semantic verification, output repair)
to maximize agent quality for end users.

------------------------------------------------------------------------

# Strategic Focus (Post-Sprint 12)

We are transitioning from:

> Guided autonomy hardening (output quality + storage boundaries)

to:

> Intelligent pipeline: LLM-powered planning, verification, and repair

Key rule going forward:

- Maximize LLM impact for end users: smarter plans, better output quality
- Pipeline V1 components enable V2 LLM intelligence layer
- Gate C prerequisites drive sprint scope (replanning, feasibility, evidence)
- Keep truthful UX and workspace isolation non-negotiable
- Preserve bounded autonomy: humans define WHAT, agents decide HOW

------------------------------------------------------------------------

# Phase 0 --- Foundation Build (Completed)

## Sprint 00 --- Project Bootstrap (Closed)

## Sprint 01 --- Core Runtime Skeleton (Closed)

## Sprint 02 --- Agent Network Behavior (Closed)

## Sprint 03 --- Observability & Truthful UX (Closed)

## Sprint 04 --- Safety & Process Hardening (Closed)

## Sprint 05 --- High-Pressure Skills (Closed)

Exit status of Phase 0:
 Modular runtime
 Delegation pattern
 Trace contract
 Truthful CLI
 CI enforcement
 Governance consolidation
 Schema verifier with repair loop

------------------------------------------------------------------------

# Phase 1 --- Skill & Playbook Foundation (Completed)

## Sprint 06 --- Skill Foundation (Closed)

## Sprint 07 --- First Real Skills (Closed)

## Sprint 08 --- Skill Ecosystem Expansion (Closed)

Exit status of Phase 1:
 Skills have defined contracts and schemas
 LLM-powered skills and playbooks validated
 Sprint-level architecture documentation completed
 Autonomy-enabling reliability and policy maturity still required

------------------------------------------------------------------------

# Phase 2 --- Autonomy Readiness Hardening (Completed)

This phase operationalizes bounded autonomy with strong enforcement,
resilience, and deterministic review gates.

------------------------------------------------------------------------

## Sprint 09 --- Reliability + Safety Hardening (Closed)

Goal: Eliminate known reliability blockers before autonomy expansion.

Exit status:
 Test isolation framework implemented (AF-0046)
 Warning-clean test discipline enforced (AF-0071)
 CLI consistency audit completed (AF-0085)
 Policy hook enforcement baseline established (AF-0087)
 Failure-path coverage hardened

------------------------------------------------------------------------

## Sprint 10 --- Gate B Readiness (Closed)

Goal: Achieve Gate B (Guided Autonomy) readiness through evidence
maturity, CLI completeness, documentation hygiene, and plugin
architecture foundation.

Exit status:
 Gate B achieved (2026-03-12)
 Artifact metadata truthful end-to-end (AF-0090)
 Verifier failure-path consistency (AF-0091)
 Skills test coverage thresholds met (AF-0093)
 CLI surface parity with CLI_REFERENCE (AF-0012)
 Global CLI flags ADR accepted (ADR008)
 Plugin architecture foundation (AF-0077, AF-0078)
 Documentation hygiene enforced (AF-0081, AF-0084)

------------------------------------------------------------------------

## Sprint 11 --- Guided Autonomy Enablement (Closed)

Goal: Enable guided autonomy mode where users can preview, approve, and
control agent execution plans before they run.

This sprint transitions from Gate B readiness to operating IN guided
autonomy mode:

```
Playbook → [Guided Agent] → Goals Only → Full Agent
           ^^^^^^^^^^^^^^
           THIS SPRINT
```

Scope focus (3 parallel tracks):

**Track 1: LLM Planner + Plan Workflow (P1 — core autonomy)**
- AF-0102 V1Planner — LLM composes plans from skill catalog
- AF-0098 Plan preview command (`ag plan --task "..."`)
- AF-0099 Plan approval workflow (`ag run --plan <id>`)
- AF-0100 Step confirmation hooks for high-impact actions

**Track 2: Observability for Autonomy (P2 — audit support)**
- AF-0094 Trace full I/O enrichment (LLM tokens, step data)
- BUG-0015 Runs list count mismatch fix (truthful UX)

**Track 3: UX Polish (P3 — quality of life)**
- AF-0097 runs commands default workspace
- AF-0101 Autonomy level display in CLI and trace

Exit criteria:
- V1Planner composes skill sequences from LLM analysis
- `ag plan --task "..."` generates reviewable execution plan
- `ag run --plan <id>` executes approved plan
- Step confirmation policy configurable per workspace
- Trace records full step I/O and LLM usage
- Autonomy mode visible in CLI and trace
- Truthful UX maintained (BUG-0015)

Key milestone (2026-03-21):
V1Planner produces multi-output plans (multiple `emit_result` calls) with
accumulated chaining. Earlier step outputs flow through to all subsequent
steps, enabling plans that emit both Markdown and JSON from a single run.
(BUG-0016c fix, plan `plan_486286485e3b`)

------------------------------------------------------------------------

## Sprint 12 --- Autonomy Boundaries (Closed)

Goal: Stabilize guided autonomy output quality and storage boundaries by
unifying summarization, hardening content emission, and standardizing
run-centered artifact/plan layout.

Scope focus:
- AF-0110 Run layout and plan artifacts refactor (P1)
- AF-0108 Unify summarization skill (P1)
- AF-0109 emit_result strict content validation (P1)
- AF-0107 load_documents MD inputs reliability (P1)
- AF-0105 CLI defaults fix (P2)
- AF-0106 V1Planner file pattern defaults (P2)
- AF-0111 --workspace flag must never create workspace (P1)

Exit status:
✓ Unified summarization pipeline — synthesize_research (AF-0108)
✓ Strict emit_result content validation enforced (AF-0109)
✓ Run-centered storage layout standardized (AF-0110)
✓ load_documents reliability hardened (AF-0107)
✓ CLI defaults fixed (AF-0105)
✓ V1Planner file pattern defaults (AF-0106)
✓ --workspace rejects non-existent names (AF-0111)

Exit status of Phase 2:
✓ Gate A and Gate B achieved
✓ Guided autonomy operational with plan preview and approval
✓ Output quality stabilized with strict content validation
✓ Storage layout unified under run-centered model
✓ Ready for intelligent pipeline development (Gate C track)

------------------------------------------------------------------------

# Phase 2b --- Intelligent Pipeline (Gate C Track)

This phase upgrades the mechanical runtime pipeline with LLM intelligence,
progressing from structural foundations through smart verification to
full semantic quality assurance. Sprint ordering prioritizes maximum LLM
impact for end users.

------------------------------------------------------------------------

## Sprint 13 --- LLM Planner Intelligence + Pipeline Foundation

Goal: Deliver smarter LLM-composed plans with playbook awareness, inline
approval UX, and a V1 Orchestrator for mixed plans, while extracting
the monolithic runtime and fixing the verifier bug.

Scope focus (2 parallel tracks):

**Track 1: LLM Planner Impact (P1 — user-facing intelligence)**
- AF-0103 V2 Planner: playbooks as first-class plan steps
- AF-0112 Inline plan preview and confirm in `ag run`
- AF-0117 (partial) V1 Orchestrator: mixed skill+playbook plan support

**Track 2: Pipeline Architecture (P1 — structural prerequisite)**
- AF-0114 Extract pipeline V0s to dedicated files
- AF-0115 V1 Verifier: step-aware verification (fixes BUG-0017)

Exit criteria:
- V2Planner composes plans using playbooks as macro steps
- V1Orchestrator handles mixed skill+playbook plans natively
- `ag run "task"` shows inline plan preview with [Y/n] confirmation
- `--yes` and `--dry-run` flags operational
- V0 components extracted to own files (orchestrator.py, executor.py, verifier.py, recorder.py)
- V1Verifier respects required/optional step flags
- BUG-0017 resolved

------------------------------------------------------------------------

## Sprint 14 --- Smart Verification Pipeline

Goal: Complete per-step verification with output schema enforcement;
every skill invocation is validated and retried on failure.

Scope focus:
- AF-0116 V1 Executor: output schema validation + bounded retry (P1)
- AF-0117 (remainder) V1 Orchestrator: per-step verification wiring (P1)
- AF-0118 V1 Recorder: verification evidence persistence (P2)
- AF-0096 Test workspace cleanup pollution (P2)

Note: V1Orchestrator was created in Sprint 13 for mixed plan support.
Sprint 14 extends it with per-step verification wiring (V1Executor +
V1Verifier integration, VERIFICATION steps in trace).

Exit criteria:
- Skill output validated against declared output_schema
- Failed validation triggers bounded retry (max 3 attempts)
- Verification runs after each step, not just end-of-run
- StepType.VERIFICATION steps emitted in trace
- `ag runs show` displays per-step verification evidence
- Test workspace pollution eliminated

------------------------------------------------------------------------

## Sprint 15 --- LLM Intelligence Layer (Gate C Target)

Goal: Add LLM-powered semantic verification, output repair, and
feasibility judgment. Fix the empty-plan-as-success bug. Achieve Gate C
readiness.

Scope focus:
- BUG-0020 Empty plan reports success (P0)
- AF-0121 V3Planner: feasibility assessment (P1)
- AF-0123 V2Verifier: LLM semantic quality checks (P1)
- AF-0124 V2Executor: LLM output repair (P2)
- AF-0122 CLI planning and pipeline display (P2)

Exit criteria:
- Empty plan no longer reports success (BUG-0020)
- Planner emits feasibility judgment (FULLY / MOSTLY / NOT_FEASIBLE)
- Planner reports capability gaps and suggests workarounds
- V2Verifier evaluates output relevance, completeness, consistency via LLM
- V2Executor attempts LLM repair before full skill re-invocation
- CLI displays planning tokens and pipeline manifest
- Gate C conditions substantially met (see Gate table)

Gate C target items addressed across Sprint 13-15:
- (2) Replanning on step failure: AF-0117 (mixed plans in S13, per-step verification in S14)
- (3) Feasibility judgment: AF-0121
- (4) Strategy justification in trace: AF-0118 + AF-0123 V2Verifier evidence
- (5) V2Planner composition: AF-0103 + AF-0117 partial (playbooks + V1Orchestrator)
- (1) Policy engine: deferred (not LLM-dependent)

Exit status:
✓ Gate C achieved (2026-03-22)
✓ BUG-0020 fixed (empty plan no longer reports success)
✓ V3Planner: feasibility judgment (FULLY / MOSTLY / PARTIALLY / NOT_FEASIBLE)
✓ V2Verifier: LLM semantic quality checks (relevance, completeness, consistency)
✓ V2Executor: LLM output repair on schema validation failure
✓ AF-0125: Deterministic test provider (FakeLLMProvider)
✓ AF-0126: Executor / verifier LLM trace enrichment
✓ CLI: planning tokens, pipeline manifest, full audit trail

------------------------------------------------------------------------

## Sprint 16 --- Skill Catalog Expansion (Phase 3 Start)

Goal: Bridge the gap between pipeline intelligence and task reachability by
adding the `LangChainSkillAdapter` infrastructure and the first batch of
external tools. The planner, verifier, and executor are now more capable
than the skills they route to — this sprint closes that gap.

Scope focus:
- AF-0127 LangChain skill adapter infrastructure (P1)
- AF-0128 First LangChain tool batch: file ops + Wikipedia (P1)

**Track 1: Adapter infrastructure (AF-0127 — prerequisite)**
- `LangChainSkillAdapter` class: generic bridge for any `langchain_core.tools.BaseTool`
- YAML-driven loader: new tools through config alone, zero per-tool Python code
- `FakeTool` test stub: deterministic testing without network or community packages
- Skill registry integration: adapters registered identically to native skills
- `langchain-core` added to dependencies (lightweight, base classes only)

**Track 2: First tool batch (AF-0128 — builds on AF-0127)**
- `write_file` (`WriteFileTool`) — write files within the active workspace
- `read_file` (`ReadFileTool`) — read files within the active workspace
- `list_directory` (`ListDirectoryTool`) — list directory contents
- `delete_file` (`DeleteFileTool`) — delete files within the active workspace
- `wikipedia` (`WikipediaQueryRun`) — factual lookup with structured output
- Workspace isolation enforced for all file tools (`root_dir` scoping)
- `langchain-community`, `wikipedia` added as optional extras

Exit criteria:
- `LangChainSkillAdapter` wraps any `BaseTool` and produces a valid ag skill
- YAML loader resolves tool names to adapters; missing tools raise `SkillConfigError`
- All 5 new skills appear in `ag skills` listing
- File tools reject paths outside the active workspace (isolation invariant preserved)
- `ag run -y "Look up Little Tokyo on Wikipedia and write a summary to output.md"` succeeds
- All adapter tests pass without LLM or network calls (FakeTool isolation)
- Full CI gate passes

------------------------------------------------------------------------

# Autonomy Phase Gates (Required)

| Gate | Purpose | Required Conditions | Status |
|------|---------|---------------------|--------|
| Gate A: Reliability | Move from foundation to autonomy-ready execution | warning-clean tests, isolation stability, failure-path coverage, deterministic cleanup | ✅ Passed (Sprint 09) |
| Gate B: Guided Autonomy | Enable guided planning behavior | policy enforcement present, verifier/failure rigor, trace-derived labels for all new behavior | ✅ Passed (Sprint 10) |
| Gate C: Goals-Only Preparation | Prepare for dynamic composition | (1) mature policy engine (budgets, risk scoring, scope boundaries), (2) replanning on step failure (adaptive recovery), (3) feasibility judgment (partial plans, "can't do this" reporting), (4) strategy justification in trace (evidence model), (5) controlled skill/playbook extensibility (V2Planner composition) | ✅ Passed (Sprint 15) |
| Gate D: Full Agent | Autonomous end-to-end execution | mature policy engine (budgets, risk scoring), adaptive mid-run replanning, broad skill catalog, RAG/retrieval interface, internal API layer | ⏳ Not started |

Gate rule:
No sprint may claim autonomy progression while a P0 gate condition is unmet.

------------------------------------------------------------------------

# Phase 3 --- Capability Expansion (Gate C Passed — Active)

These areas were deferred until Gate C. Gate C passed in Sprint 15 (2026-03-22).
Phase 3 is now active, starting with skill catalog expansion in Sprint 16.

## Retrieval Interface Layer (RAG)
- Retriever interface definition
- Workspace-bound indexing model
- Evidence bundle capture in trace
- Citation linking in trace contract

## Internal API Readiness
- Internal adapter interface definition
- CLI -> service layer mapping
- Future endpoint definitions

## Integration Phase (IoT/Web)
- IoT adapters
- Web/app adapters
- Multi-interface orchestration

------------------------------------------------------------------------

# Phase 4 --- Autonomy Evolution (Future)

## Autonomy Spectrum

```
RIGID                                                    AUTONOMOUS
(human decides everything)                    (agent decides everything)
    |                                                         |
    v                                                         v
+--------+  +--------+  +--------+  +--------+  +--------+
| Script |  |Playbook|  | Guided |  | Goals  |  |  Full  |
|        |  |        |  | Agent  |  |  Only  |  | Agent  |
+--------+  +--------+  +--------+  +--------+  +--------+
```

Current operational mode:
Guided autonomy hardened; building intelligent pipeline (Sprint 13).

Progression status:
- ✅ Playbook: established and validated
- ✅ Guided Agent: operational (Sprint 11; multi-output plans validated)
- ✅ Guided Agent hardening: completed (Sprint 12)
- ✅ Intelligent Pipeline: completed (Sprint 13-15; Gate C track)
- ✅ Goals Only: achieved (Sprint 15, 2026-03-22)
- ⏳ Full Agent: long-term (policy-engine + skill catalog + RAG dependent)

Core principle:
Humans define WHAT, agents decide HOW.

------------------------------------------------------------------------

# Current Strategic Position

**Gate A (Reliability) ✅ · Gate B (Guided Autonomy) ✅ · Gate C (Goals-Only) ✅ — all passed.**
**Next: Phase 3 capability expansion (skill catalog + RAG) → Gate D (Full Agent).**

Sprint 15 completed the intelligent pipeline:
- V3Planner: feasibility judgment (FULLY / MOSTLY / PARTIALLY / NOT_FEASIBLE)
- V2Verifier: LLM semantic quality checks (relevance, completeness, consistency)
- V2Executor: LLM output repair on schema validation failure
- CLI: planning tokens, pipeline manifest, full audit trail for all LLM calls

The system reached Goals-Only level in 15 sprints (2026-03-22).

The next bottleneck is the skill catalog, not the pipeline intelligence.
The planner, verifier, and executor are now more capable than the skills
they can route to. Reachable task space is essentially: research + summarize + emit.

Prioritization principle going forward:
Broaden what the agent can DO before deepening how it reasons about doing it.

------------------------------------------------------------------------

# Post-Sprint 15 Thinking (2026-03-22)

## Immediate bottleneck: skill collection

The pipeline intelligence (V3Planner, V2Verifier, V2Executor) is now ahead
of the skill catalog. Current primitives:
  `web_search, fetch_web_content, load_documents, synthesize_research, emit_result`

Everything beyond research/summarize/emit reports PARTIALLY_FEASIBLE or
falls back to research_v0. Skill breadth directly gates task reachability.

## Candidate next skill domains (unordered, for future sprint planning)

- **File operations** — read/write/move/delete local files. Unlocks most
  personal productivity tasks; the agent can find documents but not manipulate them.
- **Code execution** — run a script or command and capture output. Turns
  the agent from an observer into an actor.
- **Structured data extraction** — parse tables, CSV, JSON from documents
  or web content into a normalized form downstream skills can reason over.
- **Calendar / task management** — create/read events or tasks via local
  APIs (iCal, etc.). Directly relevant to scheduling and email-class tasks.
- **Diff / compare** — compare two documents or code files and surface
  meaningful deltas. Useful for review workflows.

## Candidate playbook patterns (unordered)

- **Decision brief** — research topic, extract pros/cons, emit structured
  recommendation. High daily-use value.
- **Weekly digest** — aggregate multiple sources on a theme, deduplicate,
  emit summary report.
- **Code review assist** — load a diff, analyze for issues, emit findings.
- **Meeting prep** — given topic + attendees, research context, emit briefing doc.

## Open architectural questions before Phase 3

- Should skills be able to call other skills (skill composition), or
  does that remain the playbook layer's job?
- How to handle skills that require credentials (email, calendar, APIs)?
  Secrets management does not exist yet.
- Is a skill interface version discipline needed so V2 skills can coexist
  with V1 skills during transition?

## What Gate D (Full Agent) actually requires

1. **Mature policy engine** — budgets, risk scoring, scope boundaries.
   Currently only basic confirmation hooks exist.
2. **Adaptive replanning** — genuine mid-run strategy pivot when a path
   fails. Sprint 14/15 introduced bounded retry; true replanning does not exist.
3. **Skill catalog breadth** — a full agent with a narrow skill set is
   still heavily constrained in what it can decide autonomously.
4. **RAG / retrieval interface** — workspace-bound indexing, evidence
   bundles, citation linking. Listed as Phase 3 prerequisite.
5. **Internal API readiness** — CLI → service layer so the agent is
   callable programmatically, not just from the terminal.

Path: skills/playbooks → Phase 3 capability layer → policy engine → Gate D

------------------------------------------------------------------------

## LangChain as skill source (2026-03-23)

LangChain (`langchain-community`) is the most mature external skill catalog.
The integration model: wrap a LangChain tool behind the ag skill interface.
LangChain does the implementation; our pipeline handles schema validation,
retry, LLM repair, trace recording, and auditability.

### Skill comparison

| Domain | Our skill | LangChain equivalent | Assessment |
|---|---|---|---|
| Web search | `web_search` — structured (urls, results, title, body, position), configurable engine/region/safe_search | `DuckDuckGoSearchResults`, `TavilySearchResults`, `SerpAPIWrapper` | **Ours is richer.** LangChain DDG returns flat strings. Tavily structured but needs API key. |
| URL fetching | `fetch_web_content` — batch, failure tracking, configurable timeout/length | `WebBaseLoader`, `AsyncHtmlLoader`, `PlaywrightURLLoader` | **Comparable core; LC wider.** LC adds JS-rendered pages (Playwright) which ours cannot. |
| Local file read | `load_documents` — glob, workspace-scoped, text/MD only | `TextLoader`, `DirectoryLoader`, `PyPDFLoader`, `CSVLoader`, `Docx2txtLoader`, and 50+ more | **LC much wider.** Ours handles text/MD. LC supports PDF, DOCX, CSV, Excel, PowerPoint, email formats, code files. |
| LLM synthesis | `synthesize_research` — report + citations + key_findings output schema | `MapReduceDocumentsChain`, `RefineDocumentsChain` | **Ours is a complete packaged skill.** LC equivalents are lower-level chain primitives, not drop-in skills. Our output schema is more opinionated and audit-friendly. |
| Artifact output | `emit_result` — workspace artifact with content contract, artifact_id | No equivalent | **Ours is unique.** LC has no workspace-scoped artifact emission concept. |
| File write | ❌ | `WriteFileTool`, `AppendFileTool` | **Gap — easy win, no credentials needed.** |
| File operations | ❌ | `CopyFileTool`, `MoveFileTool`, `DeleteFileTool`, `ListDirectoryTool` | **Gap.** Basic filesystem manipulation missing entirely. |
| Code execution | ❌ | `PythonREPLTool`, `ShellTool`, `E2BDataAnalysisTool` | **Gap — high value, high risk.** Sandboxing required before adopting. |
| Wikipedia | ❌ | `WikipediaQueryRun` | **Gap — easy win.** No API key, clean structured output. |
| Academic search | ❌ | `ArxivQueryRun`, `PubMedQueryRun` | Gap. Useful for research workflows. |
| Email | ❌ | `GmailToolkit` (read, send, search, draft) | Gap. Requires OAuth — credentials problem. |
| Calendar | ❌ | `GoogleCalendarTool` | Gap. Same credentials problem. |
| Structured data | ❌ | `PandasDataFrameTool` | Gap. CSV/tabular extraction. |
| Database query | ❌ | `SQLDatabaseToolkit` | Gap. Phase 3 territory. |

### Verdict

Our 5 production skills are equal or better in their specific domains.
The research pipeline (web_search → fetch_web_content → synthesize_research)
is more structured and audit-capable than LangChain equivalents.
`emit_result` has no LangChain analog.

The entire gap is in breadth. File operations are the highest-value, lowest-risk
entry point — no credentials, no sandboxing concerns, immediately useful.

### Integration approach

```python
class LangChainSkillAdapter(BaseSkill):
    def __init__(self, tool: BaseTool):
        self.tool = tool

    def execute(self, context: SkillContext) -> dict:
        result = self.tool.run(context.params["input"])
        return {"output": result}
```

LangChain tools return unstructured strings. The adapter must normalize
their output into our declared output_schema. V2Executor's LLM repair
provides a safety net for schema mismatches.

### Risks

- **Output schema mismatch** — LangChain tools return strings; adapter
  normalization layer required.
- **Sandboxing** — ShellTool/PythonREPLTool conflict with workspace
  isolation invariant. Require explicit scoping before adoption.
- **Credentials** — LC tools pick up secrets from environment variables.
  Clashes with future workspace-scoped secrets model.
- **Dependency weight** — `langchain-community` is large; check if
  tool subsets can be installed independently.

------------------------------------------------------------------------

## LC Core components and advanced usage (2026-03-23)

Beyond the skill adapter layer, `langchain-core` and companion packages expose
several components that integrate naturally into our existing pipeline architecture.
Analysis is based on the current V3Planner / V2Verifier / V2Executor internals
(chat message lists, raw f-string prompts, manual JSON parsing, no text splitting).

### Viable integrations (ordered by priority)

**1. `PydanticOutputParser` / `JsonOutputParser` — high value, Sprint 16/17**

V2Executor repair currently does `json.loads()` → `model_validate()` manually.
`PydanticOutputParser` wraps exactly this pattern and adds one critical extra: it
generates **format instructions** that can be prepended to the repair prompt,
telling the LLM the target JSON schema _before_ it responds. This closes the most
common repair failure mode (LLM doesn't know the expected structure).

Drop-in replacement for the manual JSON extraction in V2Executor repair logic.
Zero architecture change. High repair success rate improvement for low effort.

**2. `RecursiveCharacterTextSplitter` — high value, Sprint 17 (RAG prerequisite)**

`load_documents` loads entire files with no chunking. Any file over ~6K tokens
silently overflows the LLM context window downstream in `synthesize_research`.
`RecursiveCharacterTextSplitter` chunks at paragraph → sentence → word boundaries.

Two benefits: (1) fixes the silent large-doc overflow problem immediately;
(2) mandatory prerequisite for the Phase 3 RAG layer — vector stores require
chunked documents. Self-contained change to `load_documents`. Ships as
`langchain-text-splitters` (separate lightweight package, no community dependency).

**3. Rich document loaders — Sprint 17 (companion to text splitting)**

`load_documents` handles `.txt` and `.md` only. LangChain community loaders follow
the same `Document` interface and slot directly into the existing skill:

| Format | Class | Extra dependency |
|---|---|---|
| PDF | `PyPDFLoader` | `pypdf` |
| DOCX | `Docx2txtLoader` | `docx2txt` |
| CSV | `CSVLoader` | none |
| HTML | `BSHTMLLoader` | `bs4` |
| Excel | `UnstructuredExcelLoader` | `unstructured` |

No new skill class required — loaders register in the existing `load_documents`
dispatch table via the YAML config pattern from AF-0127.

**4. `BaseCallbackHandler` — Sprint 17/18 (post AF-0126 refactor candidate)**

LC callbacks fire automatically on every LLM call: `on_llm_start(prompt)`,
`on_llm_end(response, token_counts)`, `on_tool_start/end`. A single
`TraceCallbackHandler` registered with the provider would auto-capture token
counts for planner, executor repair, and verifier calls in one place —
instead of each component tracking its own tokens (which is what AF-0126 required).

This is the cleanest long-term architecture for trace token aggregation. The tradeoff
is that the `LLMProvider` protocol must wire callbacks through, which touches the
provider layer. Worth evaluating after AF-0126 ships.

**5. `ChatPromptTemplate` — Sprint 17+ (code quality, not functional)**

All three pipeline components (V3Planner, V2Verifier, V2Executor) build prompts via
raw f-strings in `_build_prompt()` / `_get_system_prompt()`. LC prompt templates add
variable declaration, render-and-inspect testing, and reusable template instances.
No functional improvement — a code quality and testability gain. Low urgency.

**6. Embeddings + local vector stores — Phase 3 (RAG foundation)**

`OpenAIEmbeddings` reuses the existing `OpenAIProvider` API key with zero new auth.
`Chroma` is a local, file-based vector store: no server, naturally workspace-scoped,
trivially mapped to the run-centered storage layout. `FAISS` is an alternative if
Chroma is too heavy. These are not Sprint 16/17 work, but the path to RAG is
low-friction given the existing OpenAI provider wiring.

### What does not integrate

| Component | Why not |
|---|---|
| LCEL / Runnable chains | Our orchestrator IS our pipeline chain. Two competing chain abstractions would conflict with V1Orchestrator. |
| LC Agents (ReAct, OpenAI Functions) | Conflicts with V3Planner architecture. We have our own plan-execute-verify loop. |
| LangSmith tracing | External SaaS dependency; we have a rigorous local trace contract (AF-0126). Not a fit. |
| Conversation memory | We use run-based storage, not multi-turn session memory. No current use case. |
| `ShellTool` / `PythonREPLTool` | Sandbox isolation prerequisite unmet. High risk without workspace scoping. |

### Roadmap placement

| Component | Package | Target |
|---|---|---|
| `PydanticOutputParser` | `langchain-core` | Sprint 16 or V2Executor hardening |
| `RecursiveCharacterTextSplitter` | `langchain-text-splitters` | Sprint 17 |
| Rich document loaders (PDF, CSV, DOCX) | `langchain-community` | Sprint 17 |
| `BaseCallbackHandler` trace integration | `langchain-core` | Sprint 17/18 |
| `ChatPromptTemplate` | `langchain-core` | Sprint 17+ |
| `OpenAIEmbeddings` + `Chroma` | `langchain-community`, `chromadb` | Phase 3 / Sprint 18+ |
