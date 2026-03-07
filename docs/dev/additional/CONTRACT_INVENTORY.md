# CONTRACT_INVENTORY — Protocol Interface Reference
# Version number: v0.1
# Created: 2026-03-06 (AF0013)

> **Purpose:** Canonical reference for all Protocol interfaces in ag_foundation.
> 
> **Complementary document:** [SCHEMA_INVENTORY.md](SCHEMA_INVENTORY.md) documents Pydantic schemas.
> 
> For schema vs contract distinction, see [SKILLS_ARCHITECTURE_0.1.md](SKILLS_ARCHITECTURE_0.1.md) Section 3.1.

---

## Contract vs Schema Distinction

| Term | Definition | Location | Enforcement |
|------|------------|----------|-------------|
| **Contract** | Behavioral promise (Protocol interface) | This document | Test assertions + type checking |
| **Schema** | Data shape (Pydantic model) | SCHEMA_INVENTORY.md | Runtime validation |

A contract *includes* method signatures but also covers preconditions, postconditions, and invariants documented in docstrings.

---

## Protocol Groups

### 1. Core Runtime Protocols (`src/ag/core/interfaces.py`)

| Protocol | Purpose | Methods |
|----------|---------|---------|
| `Normalizer` | Normalizes and validates incoming task requests | `normalize(prompt, **options) -> TaskSpec` |
| `Planner` | Selects and configures the execution playbook | `plan(task) -> Playbook` |
| `Orchestrator` | Coordinates execution of playbook steps | `run(task, playbook) -> RunTrace` |
| `Executor` | Executes individual skills/tools | `execute(skill_name, parameters) -> (bool, str, dict)` |
| `Verifier` | Verifies execution results | `verify(trace) -> (status, message)` |
| `Recorder` | Records run traces and artifacts | `record(trace)`, `register_artifact(...)` |

#### Normalizer
```python
class Normalizer(Protocol):
    def normalize(self, prompt: str, **options: object) -> TaskSpec:
        """Normalize user input into a TaskSpec.
        
        Responsibilities:
        - Parse and validate user input
        - Resolve defaults (workspace, mode, etc.)
        - Produce a validated TaskSpec
        """
```

#### Planner
```python
class Planner(Protocol):
    def plan(self, task: TaskSpec) -> Playbook:
        """Select playbook for task execution.
        
        Responsibilities:
        - Match task to appropriate playbook
        - Apply budget/constraint overrides
        - Return execution-ready playbook
        """
```

#### Orchestrator
```python
class Orchestrator(Protocol):
    def run(self, task: TaskSpec, playbook: Playbook) -> RunTrace:
        """Execute a playbook for the given task.
        
        Responsibilities:
        - Execute steps in sequence (v0: linear only)
        - Track step results and timing
        - Handle errors and early termination
        - Delegate to Executor for skill calls
        """
```

#### Executor
```python
class Executor(Protocol):
    def execute(
        self, skill_name: str, parameters: dict[str, object]
    ) -> tuple[bool, str, dict[str, object]]:
        """Execute a skill.
        
        Responsibilities:
        - Resolve skill by name from registry
        - Execute skill with parameters
        - Capture output and errors
        
        Returns:
            Tuple of (success, output_summary, result_data)
        """
```

#### Verifier
```python
class Verifier(Protocol):
    def verify(self, trace: RunTrace) -> tuple[str, str | None]:
        """Verify a run's results.
        
        Responsibilities:
        - Check step outputs against expectations
        - Run validation rules
        - Produce verification status
        
        Returns:
            Tuple of (status: 'passed'|'failed'|'skipped', message)
        """
```

#### Recorder
```python
class Recorder(Protocol):
    def record(self, trace: RunTrace) -> None:
        """Persist a RunTrace."""
        
    def register_artifact(
        self, trace: RunTrace, artifact_id: str, path: str, content: bytes
    ) -> str:
        """Register an artifact for a run.
        
        Returns:
            Storage path/URI for the artifact
        """
```

---

### 2. Storage Protocols (`src/ag/storage/interfaces.py`)

| Protocol | Purpose | Methods |
|----------|---------|---------|
| `RunStore` | Run storage operations | `save`, `get`, `list`, `delete` |
| `ArtifactStore` | Artifact storage operations | `save`, `get`, `list` |

#### RunStore
```python
class RunStore(Protocol):
    def save(self, trace: RunTrace) -> None:
        """Persist a RunTrace."""
        
    def get(self, workspace_id: str, run_id: str) -> RunTrace | None:
        """Retrieve a RunTrace by ID."""
        
    def list(self, workspace_id: str, limit: int = 100) -> list[RunTrace]:
        """List runs in a workspace, most recent first."""
        
    def delete(self, workspace_id: str, run_id: str) -> bool:
        """Delete a run. Returns True if deleted."""
```

#### ArtifactStore
```python
class ArtifactStore(Protocol):
    def save(
        self, workspace_id: str, run_id: str, artifact: Artifact, content: bytes
    ) -> str:
        """Store an artifact. Returns storage path/URI."""
        
    def get(
        self, workspace_id: str, run_id: str, artifact_id: str
    ) -> tuple[Artifact, bytes] | None:
        """Retrieve an artifact and its content."""
        
    def list(self, workspace_id: str, run_id: str) -> list[Artifact]:
        """List artifacts for a run."""
```

---

### 3. Provider Protocols (`src/ag/providers/base.py`)

| Protocol | Purpose | Methods |
|----------|---------|---------|
| `LLMProvider` | LLM provider interface | `chat`, `validate_config`, `name`, `is_stub` |

#### LLMProvider
```python
@runtime_checkable
class LLMProvider(Protocol):
    @property
    def name(self) -> str:
        """Provider name (e.g., 'openai', 'anthropic', 'local')."""
        
    @property
    def is_stub(self) -> bool:
        """Whether this provider is a stub (fails fast with structured error)."""
        
    def chat(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        """Send a chat completion request.
        
        Raises:
            ProviderError: On provider errors (auth, timeout, rate limit, etc.)
            ProviderNotImplementedError: If provider is a stub
        """
        
    def validate_config(self) -> bool:
        """Validate provider configuration. Returns True if valid."""
```

---

### 4. Skill Protocols (`src/ag/skills/base.py`)

| Protocol | Purpose | Methods |
|----------|---------|---------|
| `Skill` | V2 skill interface (ABC) | `execute`, `validate_context` |

#### Skill (Abstract Base Class)
```python
class Skill(ABC, Generic[InputT, OutputT]):
    """V2 skill with typed input/output and context injection."""
    
    # Class attributes
    name: ClassVar[str]
    description: ClassVar[str]
    input_schema: ClassVar[type[SkillInput]]
    output_schema: ClassVar[type[SkillOutput]]
    requires_llm: ClassVar[bool] = False
    
    @abstractmethod
    def execute(self, input: InputT, ctx: SkillContext) -> OutputT:
        """Execute the skill with validated input and runtime context."""
        
    def validate_context(self, ctx: SkillContext) -> None:
        """Validate runtime context. Raises ValueError if invalid."""
```

---

## Implementation Status

| Protocol | Implementations | Status |
|----------|-----------------|--------|
| Normalizer | `runtime.py` (inline) | ✅ Implemented |
| Planner | `runtime.py` (inline) | ✅ Implemented |
| Orchestrator | `runtime.py` (inline) | ✅ Implemented |
| Executor | `runtime.py` (inline) | ✅ Implemented |
| Verifier | `schema_verifier.py` | ✅ Implemented |
| Recorder | `runtime.py` (inline) | ✅ Implemented |
| RunStore | `sqlite_store.py` | ✅ Implemented |
| ArtifactStore | `sqlite_store.py` | ✅ Implemented |
| LLMProvider | `openai.py`, `stubs.py` | ✅ Implemented |
| Skill | `strategic_brief.py` (V2) | ✅ Implemented |

---

## Drift Detection

This inventory is validated by `tests/test_contracts.py` which:
1. Ensures all Protocols in interface modules are documented here
2. Verifies method signatures match documented signatures
3. Fails CI if protocols are added without documentation

---

## Related Documents
- [SCHEMA_INVENTORY.md](SCHEMA_INVENTORY.md) — Pydantic schemas
- [SKILLS_ARCHITECTURE_0.1.md](SKILLS_ARCHITECTURE_0.1.md) — Skill/playbook design
- [ARCHITECTURE.md](../../ARCHITECTURE.md) — System architecture
- [ARCHITECTURE.md Section 3.4.2](../../ARCHITECTURE.md#342-concept-relationships) — How contracts relate to schemas, skills, and playbooks

## Related AFs
- **AF0013:** This document
- **AF0060:** Skill protocol definition
- **AF0063:** Schema inventory (complementary)
