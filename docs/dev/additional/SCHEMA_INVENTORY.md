# SCHEMA_INVENTORY — Pydantic Model Reference
# Version number: v0.1
# Created: 2026-03-06 (AF0063)

> **Purpose:** Canonical reference for all Pydantic schemas in ag_foundation.
> 
> **Complementary document:** [CONTRACT_INVENTORY.md](CONTRACT_INVENTORY.md) documents Protocol interfaces.
> 
> For schema vs contract distinction, see [SKILLS_ARCHITECTURE_0.1.md](SKILLS_ARCHITECTURE_0.1.md) Section 3.1.

---

## Schema Groups

### 1. Core Runtime Schemas (`src/ag/core/`)

#### Task Specification

| Model | Module | Purpose | Version |
|-------|--------|---------|---------|
| `TaskSpec` | task_spec.py | Input contract for agent runs — prompt, workspace, mode, budgets, constraints | 0.1 |
| `Budgets` | task_spec.py | Resource limits (max_tokens, max_time_seconds, max_cost_usd) | 0.1 |
| `Constraints` | task_spec.py | Run constraints (allow_network, allow_fs, output_format) | 0.1 |

#### Run Trace

| Model | Module | Purpose | Version |
|-------|--------|---------|---------|
| `RunTrace` | run_trace.py | Complete execution record — run_id, task, steps, artifacts, timing | 0.1 |
| `Step` | run_trace.py | Single reasoning/action step in execution (input_data, output_data added AF-0094) | 0.1 |
| `StepConfirmation` | run_trace.py | Confirmation status for steps requiring approval (AF-0100) | 0.1 |
| `Artifact` | run_trace.py | Output file metadata (id, path, type, hash) | 0.1 |
| `Subtask` | run_trace.py | Delegated subtask reference | 0.1 |
| `EvidenceRef` | run_trace.py | Reference to evidence supporting a step | 0.1 |
| `PlaybookMetadata` | run_trace.py | Playbook info captured in trace (name, version) | 0.1 |
| `Verifier` | run_trace.py | Verification result stored in trace (status, message) | 0.1 |
| `LLMExecution` | run_trace.py | LLM provider/model info with token tracking (AF-0062, AF-0094) | 0.1 |
| `AutonomyMetadata` | run_trace.py | Autonomy mode for run (mode, plan_id, confirmation_enabled) (AF-0101) | 0.1 |

#### Playbook

| Model | Module | Purpose | Version |
|-------|--------|---------|---------|
| `Playbook` | playbook.py | Workflow definition — name, version, steps, reasoning modes, budgets | 0.1 |
| `PlaybookStep` | playbook.py | Single step in playbook (skill invocation, branch, loop, gate) | 0.1 |

#### Schema Verifier

| Model | Module | Purpose | Version |
|-------|--------|---------|---------|
| `ValidationAttempt` | schema_verifier.py | Record of single validation attempt | 0.1 |
| `ValidationResult` | schema_verifier.py | Final validation loop result with attempts | 0.1 |

---

### 2. Skill Schemas (`src/ag/skills/`)

#### Base Framework (AF0060)

| Model | Module | Purpose | Version |
|-------|--------|---------|---------|
| `SkillInput` | base.py | Base input schema for v2 skills (prompt) | 0.1 |
| `SkillOutput` | base.py | Base output schema for v2 skills (success, summary, error) | 0.1 |
| `StubSkillOutput` | base.py | Extension of SkillOutput for stub responses (stub=True, stub_data) | 0.1 |

#### load_documents

| Model | Module | Purpose | Version |
|-------|--------|---------|---------|
| `LoadDocumentsInput` | load_documents.py | Input for document loading (paths, include_patterns, exclude_patterns) | 0.1 |
| `LoadDocumentsOutput` | load_documents.py | Loaded documents output (documents, loaded_count, failed_paths) | 0.1 |

#### summarize_docs

| Model | Module | Purpose | Version |
|-------|--------|---------|---------|
| `SummarizableDocument` | summarize_docs.py | Unified document schema for any source (local/web) | 0.1 |
| `SummarizeDocsInput` | summarize_docs.py | Input for document summarization (documents, max_tokens) | 0.1 |
| `SummarizeDocsOutput` | summarize_docs.py | Summarized output (summary) | 0.1 |

#### emit_result

| Model | Module | Purpose | Version |
|-------|--------|---------|---------|
| `EmitResultInput` | emit_result.py | Input for result emission (report, format) | 0.1 |
| `EmitResultOutput` | emit_result.py | Result emission output (artifact_path, format) | 0.1 |

#### echo/stub skills (test utilities)

| Model | Module | Purpose | Version |
|-------|--------|---------|---------|
| `EchoInput` | stubs.py | Echo skill input (message) | 0.1 |
| `EchoOutput` | stubs.py | Echo skill output (echoed) | 0.1 |

#### fetch_web_content (AF0074)

| Model | Module | Purpose | Version |
|-------|--------|---------|---------|
| `FetchedDocument` | fetch_web_content.py | Document fetched from URL (url, content, status_code, content_type, title, error) | 0.1 |
| `FetchWebContentInput` | fetch_web_content.py | Input for URL fetching (urls, timeout_seconds, max_content_length) | 0.1 |
| `FetchWebContentOutput` | fetch_web_content.py | Output with fetched documents (documents, failed_urls, total_fetched, total_failed) | 0.1 |

#### synthesize_research (AF0074)

| Model | Module | Purpose | Version |
|-------|--------|---------|---------|
| `SourceDocument` | synthesize_research.py | Source document for synthesis (source, content, source_type) | 0.1 |
| `SynthesizeResearchInput` | synthesize_research.py | Input for research synthesis (documents, output_format, max_tokens, include_citations) | 0.1 |
| `SynthesizeResearchOutput` | synthesize_research.py | Synthesized report output (report, key_findings, sources_used, source_count) | 0.1 |

#### zero_skill

| Model | Module | Purpose | Version |
|-------|--------|---------|--------|
| `ZeroSkillInput` | zero_skill.py | Input for zero skill (uses base SkillInput) | 0.1 |
| `ZeroSkillOutput` | zero_skill.py | Output for zero skill (uses base SkillOutput) | 0.1 |

#### web_search (AF0080)

| Model | Module | Purpose | Version |
|-------|--------|---------|---------|
| `SearchResult` | web_search.py | Single search result (url, title, snippet, position) | 0.1 |
| `WebSearchInput` | web_search.py | Input for web search (query, max_results, search_engine, region, safe_search) | 0.1 |
| `WebSearchOutput` | web_search.py | Output with search results (urls, results, search_query, search_engine, total_results) | 0.1 |

---

### 3. Provider Schemas (`src/ag/providers/`)

| Model | Module | Purpose | Version |
|-------|--------|---------|---------|
| `ChatMessage` | base.py | Single message in chat conversation (role, content) | 0.1 |
| `ChatResponse` | base.py | LLM response with content, token counts, model info (AF-0094) | 0.1 |
| `ProviderConfig` | base.py | Provider configuration (model, base_url, timeout) | 0.1 |

---

## Dependency Graph

```
TaskSpec
├── Budgets
└── Constraints

RunTrace
├── TaskSpec
├── Step[]
│   ├── Subtask[]
│   └── EvidenceRef[]
├── Artifact[]
├── PlaybookMetadata
├── Verifier
└── LLMExecution

Playbook
├── Budgets
└── PlaybookStep[]

SkillOutput ← StubSkillOutput (inheritance)
```

---

## Enums

| Enum | Module | Values |
|------|--------|--------|
| `RunStatus` | run_trace.py | `PENDING`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED` |
| `ArtifactType` | run_trace.py | `MARKDOWN`, `JSON`, `TEXT`, `BINARY`, `HTML` |
| `VerifierStatus` | run_trace.py | `PASSED`, `FAILED`, `SKIPPED`, `ERROR` |
| `ReasoningMode` | playbook.py | `DIRECT`, `CHAIN_OF_THOUGHT`, `TREE_OF_THOUGHT`, `REFLECTION` |
| `PlaybookStepType` | playbook.py | `SKILL`, `BRANCH`, `LOOP`, `GATE` |

---

## Evolution Guidelines

### Version Policy
- **0.x releases:** Additive changes only (new optional fields)
- **Breaking changes:** Bump minor version, provide migration notes in AF
- **Field deprecation:** Mark with `Deprecated` annotation, keep for 2 sprints, then remove with version bump

### Adding New Fields
```python
# Correct: new optional field with default
new_field: str | None = Field(default=None, description="...")

# Incorrect: new required field (breaks existing data)
new_field: str = Field(..., description="...")
```

### Schema Modification Checklist
When modifying schemas:
1. [ ] Is change additive (new optional field)?
2. [ ] Does field have sensible default?
3. [ ] Are existing tests still passing?
4. [ ] Is SCHEMA_INVENTORY.md updated?
5. [ ] Is version bumped if breaking?

---

## Related Documents
- [CONTRACT_INVENTORY.md](CONTRACT_INVENTORY.md) — Protocol interfaces
- [SKILLS_ARCHITECTURE_0.1.md](SKILLS_ARCHITECTURE_0.1.md) — Skill/playbook design
- [ARCHITECTURE.md](../../ARCHITECTURE.md) — System architecture
- [ARCHITECTURE.md Section 3.4.2](../../ARCHITECTURE.md#342-concept-relationships) — How schemas relate to contracts, skills, and playbooks

## Related AFs
- **AF0060:** Skill definition framework (added skill schemas)
- **AF0062:** Trace LLM model tracking (will extend RunTrace)
- **AF0063:** This document
- **AF0074:** Research playbook skills (fetch_web_content, synthesize_research)
