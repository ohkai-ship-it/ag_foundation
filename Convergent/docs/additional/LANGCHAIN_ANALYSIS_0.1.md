# LangChain Integration Analysis
#### Description: Point-in-time analysis of LangChain as a skill source and component library for ag_foundation. Covers skill comparison, viable integrations, and what does not fit.
#### Convergent: v1.3.2
#### File version: 0.1
#### governs: ag_foundation
#### Date: 2026-03-23

---

## 1) LangChain as Skill Source

LangChain (`langchain-community`) is the most mature external skill catalog.
The integration model: wrap a LangChain tool behind the ag skill interface.
LangChain does the implementation; our pipeline handles schema validation,
retry, LLM repair, trace recording, and auditability.

### Skill Comparison

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

### Integration Approach

```python
class LangChainSkillAdapter(Skill[LCInput, LCOutput]):
    """Wraps any langchain_core.tools.BaseTool as an ag skill."""

    def __init__(self, tool: BaseTool):
        self.tool = tool

    def execute(self, input: LCInput, ctx: SkillContext) -> LCOutput:
        result = self.tool.run(input.prompt)
        return LCOutput(success=True, summary=result)
```

LangChain tools return unstructured strings. The adapter normalizes
their output into the declared output_schema. V2Executor's LLM repair
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

---

## 2) Core Components and Advanced Usage

Beyond the skill adapter layer, `langchain-core` and companion packages expose
components that integrate naturally into the existing pipeline architecture.
Analysis is based on V3Planner / V2Verifier / V2Executor internals
(chat message lists, raw f-string prompts, manual JSON parsing, no text splitting).

### Viable Integrations (ordered by priority)

**1. `PydanticOutputParser` / `JsonOutputParser` — high value**

V2Executor repair currently does `json.loads()` → `model_validate()` manually.
`PydanticOutputParser` wraps exactly this pattern and adds one critical extra: it
generates **format instructions** that can be prepended to the repair prompt,
telling the LLM the target JSON schema _before_ it responds. This closes the most
common repair failure mode (LLM doesn't know the expected structure).

Drop-in replacement for the manual JSON extraction in V2Executor repair logic.
Zero architecture change. High repair success rate improvement for low effort.

**2. `RecursiveCharacterTextSplitter` — high value (RAG prerequisite)**

`load_documents` loads entire files with no chunking. Any file over ~6K tokens
silently overflows the LLM context window downstream in `synthesize_research`.
`RecursiveCharacterTextSplitter` chunks at paragraph → sentence → word boundaries.

Two benefits: (1) fixes the silent large-doc overflow problem immediately;
(2) mandatory prerequisite for the Phase 3 RAG layer — vector stores require
chunked documents. Self-contained change to `load_documents`. Ships as
`langchain-text-splitters` (separate lightweight package, no community dependency).

**3. Rich Document Loaders**

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

**4. `BaseCallbackHandler` — post AF-0126 refactor candidate**

LC callbacks fire automatically on every LLM call: `on_llm_start(prompt)`,
`on_llm_end(response, token_counts)`, `on_tool_start/end`. A single
`TraceCallbackHandler` registered with the provider would auto-capture token
counts for planner, executor repair, and verifier calls in one place —
instead of each component tracking its own tokens (which is what AF-0126 required).

Cleanest long-term architecture for trace token aggregation. Tradeoff:
`LLMProvider` protocol must wire callbacks through, which touches the
provider layer. Worth evaluating after AF-0126 ships.

**5. `ChatPromptTemplate` — code quality, not functional**

All three pipeline components build prompts via raw f-strings in
`_build_prompt()` / `_get_system_prompt()`. LC prompt templates add
variable declaration, render-and-inspect testing, and reusable template instances.
No functional improvement — a code quality and testability gain. Low urgency.

**6. Embeddings + Local Vector Stores — RAG foundation**

`OpenAIEmbeddings` reuses the existing `OpenAIProvider` API key with zero new auth.
`Chroma` is a local, file-based vector store: no server, naturally workspace-scoped,
trivially mapped to the run-centered storage layout. `FAISS` is an alternative if
Chroma is too heavy. These are Phase 3 / RAG work, but the path is low-friction
given the existing OpenAI provider wiring.

### What Does Not Integrate

| Component | Why not |
|---|---|
| LCEL / Runnable chains | Our orchestrator IS our pipeline chain. Two competing chain abstractions would conflict with V1Orchestrator. |
| LC Agents (ReAct, OpenAI Functions) | Conflicts with V3Planner architecture. We have our own plan-execute-verify loop. |
| LangSmith tracing | External SaaS dependency; we have a rigorous local trace contract (AF-0126). Not a fit. |
| Conversation memory | We use run-based storage, not multi-turn session memory. No current use case. |
| `ShellTool` / `PythonREPLTool` | Sandbox isolation prerequisite unmet. High risk without workspace scoping. |

### Roadmap Placement

| Component | Package | Target |
|---|---|---|
| `PydanticOutputParser` | `langchain-core` | V2Executor hardening |
| `RecursiveCharacterTextSplitter` | `langchain-text-splitters` | RAG prerequisite sprint |
| Rich document loaders (PDF, CSV, DOCX) | `langchain-community` | Companion to text splitting |
| `BaseCallbackHandler` trace integration | `langchain-core` | Post AF-0126 refactor |
| `ChatPromptTemplate` | `langchain-core` | Low priority / code quality |
| `OpenAIEmbeddings` + `Chroma` | `langchain-community`, `chromadb` | Phase 3 / RAG foundation |
