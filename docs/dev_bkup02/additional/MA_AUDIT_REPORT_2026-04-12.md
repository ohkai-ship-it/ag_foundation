# M&A Technical + IP + Code Audit Report

**Subject:** ag_foundation v0.1.0 — Modular Agent Network Core Runtime  
**Repository:** `https://github.com/ohkai-ship-it/ag_foundation.git`  
**Audit Date:** 2026-04-12  
**Classification:** Confidential — M&A Diligence  
**Standard:** M&A diligence / Board reporting / Regulatory disclosure / Litigation defensibility  

---

## EXECUTIVE SUMMARY

ag_foundation is an **early-stage (Alpha)** modular agent-network runtime written in Python. It provides a CLI-first pipeline for planning, executing, verifying, and recording LLM-powered agent tasks. The codebase is **well-architected** with clean separation of concerns, Protocol-based interfaces, and a versioned component pipeline. It is authored by a single contributor, licensed as MIT (metadata only — LICENSE file missing), and has 814 tests at 86% coverage.

### Key Findings

| Area | Rating | Summary |
|------|--------|---------|
| **IP Clarity** | MEDIUM RISK | Single author, no CLA/assignment docs, missing LICENSE file |
| **Code Quality** | LOW RISK | Clean architecture, 86% coverage, 814 tests, strict linting |
| **Security** | MEDIUM RISK | .env contains live API key (local only, not in git), silent exception swallowing |
| **Architecture** | LOW RISK | Excellent modularity, protocol-based, versioned components |
| **Compliance** | LOW RISK | No PII processing, no export-controlled tech, no regulated data |
| **DevOps** | MEDIUM RISK | CI/CD exists but minimal; no staging/prod; no monitoring |
| **Dependencies** | LOW RISK | 6 runtime deps, 2 known CVEs (pip, pygments), no copyleft |

### Acquisition Readiness Score: **6.5 / 10**

Strong technical foundation. Primary gaps are governance documentation, IP formalization, operational maturity, and the pre-production development status.

---

## PART I — IP ASSET REGISTRY REVIEW

### 1. Ownership Verification

| Item | Status | Finding |
|------|--------|---------|
| **Authorship** | Single contributor | 252 commits, 2 Git identities: `ohkai-ship-it` (240), `Kai` (12) — same person (kai.voges@gmx.net) |
| **Contributor History** | Solo project | No external contributors identified in git history |
| **Assignment Agreements** | NOT FOUND | No IP assignment, contributor agreement, or employment IP clause on file |
| **Contractor IP Transfer** | N/A | No contractors identified |
| **CLAs** | NOT FOUND | No Contributor License Agreement exists |

**Risk:** Without formal IP assignment documentation, ownership chain relies solely on git authorship inference. If the author developed this under employment, employer may have claims.

### 2. Open Source Inventory — Full Dependency Tree

#### Runtime Dependencies

| Package | Version | License | Copyleft Risk | Commercial Use |
|---------|---------|---------|---------------|----------------|
| `typer` | >=0.9.0 (installed: 0.24.1) | MIT | None | Permitted |
| `pydantic` | >=2.0.0 (installed: 2.12.5) | MIT | None | Permitted |
| `rich` | >=13.0.0 (installed: 14.3.3) | MIT | None | Permitted |
| `python-dotenv` | >=1.0.0 (installed: 1.2.1) | BSD-3 | None | Permitted |
| `httpx` | >=0.27.0 (installed: 0.28.1) | BSD-3 | None | Permitted |
| `ddgs` | >=6.0.0 (installed: 9.11.2) | MIT | None | Permitted |

#### Transitive Runtime Dependencies

| Package | License | Risk |
|---------|---------|------|
| `click` (via typer) | BSD-3 | None |
| `pydantic-core` (via pydantic) | MIT | None |
| `anyio` (via httpx) | MIT | None |
| `certifi` (via httpx) | MPL-2.0 | **Low** — MPL-2.0 is file-level copyleft, but certifi is data-only (CA bundle) |
| `h11`, `httpcore` (via httpx) | MIT | None |
| `idna` (via httpx) | BSD-3 | None |
| `sniffio` (via anyio) | MIT/Apache-2.0 | None |
| `lxml` (via ddgs) | BSD-3 | None |
| `primp` (via ddgs) | MIT | None |
| `librt` (via ddgs) | MIT | None |
| `tqdm` (via ddgs) | MPL-2.0 / MIT | **None** — dual-licensed |
| `annotated-types` (via pydantic) | MIT | None |
| `jiter` (via pydantic) | MIT | None |
| `colorama` (via click) | BSD-3 | None |
| `shellingham` (via typer) | ISC | None |
| `pygments` (via rich) | BSD-2 | None |
| `markdown-it-py` (via rich) | MIT | None |

#### Optional Dependencies (dev/test/llm)

| Package | License | Risk |
|---------|---------|------|
| `openai` | Apache-2.0 | None |
| `pytest` | MIT | None (dev only) |
| `ruff` | MIT | None (dev only) |
| `mypy` | MIT | None (dev only) |

**License Risk Matrix:**

| Risk Level | Packages | Action Required |
|------------|----------|-----------------|
| **NONE** | 28/30 packages | No action needed |
| **LOW** | certifi (MPL-2.0) | Data-only; no code linking risk |
| **COPYLEFT** | None | No GPL/AGPL/LGPL contamination detected |

### 3. Proprietary Asset Mapping

| Asset Type | Finding | Value Indicator |
|------------|---------|-----------------|
| **Unique Algorithms** | V3Planner feasibility assessment, SchemaValidator repair loop, V2Verifier semantic evaluation | MEDIUM — novel LLM orchestration patterns |
| **Trade Secrets** | Playbook orchestration architecture, plugin discovery via entry points, multi-step delegation model | LOW-MEDIUM — patterns are implementable from docs |
| **Data Models** | 15+ Pydantic models (TaskSpec, RunTrace, ExecutionPlan, etc.) | MEDIUM — core domain schema |
| **ML Models** | None trained or embedded | N/A |
| **Classification Engines** | ArtifactCategory inference, feasibility classifier | LOW — rule-based, not ML |
| **Third-Party APIs** | OpenAI (optional), DuckDuckGo (via ddgs), Serper, Google Search, Bing (all optional) | Standard integrations |

### 4. Patent Landscape Check

| Potential Claim Area | Patentability | FTO Risk |
|---------------------|---------------|----------|
| Pipeline manifest (component version recording) | Weak — incremental on prior art | Low |
| Schema repair loop with LLM (bounded retry) | Weak — obvious combination | Low |
| Feasibility assessment before plan execution | Weak — prior art in agent systems | Low |
| Playbook-as-plan-step composition | Weak — workflow orchestration prior art exists | Low |

**FTO Risk Summary:** LOW. The system combines known patterns (LLM orchestration, plugin architecture, schema validation) in a clean but not patentably novel way. No identified infringement exposure.

**Trade Secret Risk Memo:** The primary proprietary value is in the **architecture composition** — the specific way pipeline components, skills, playbooks, and verification loops interact. This is well-documented in the codebase and could be duplicated from public repository access.

---

## PART II — FULL CODE AUDIT

### 1. Architecture Review

#### System Modularity: **EXCELLENT**

The codebase follows a disciplined layered architecture:

```
Interface Layer (CLI Adapter)
    ↓
Core Runtime (Modular Pipeline)
    ├── Normalizer → Planner → Orchestrator → Executor → Verifier → Recorder
    ↓
Skills & Tooling Layer (Plugins)
    ↓
Storage Layer (SQLite + Filesystem)
    ↓
Provider Layer (LLM Abstraction)
```

**Coupling & Cohesion Score: 8/10**
- Protocol-based interfaces (`typing.Protocol`) provide duck-typing contracts
- Each pipeline component lives in its own file with versioned implementations
- `runtime.py` is a pure composition root — no business logic
- Skills and playbooks are discoverable via `entry_points` plugin architecture

**Dependency Injection: 7/10**
- Constructor injection used throughout
- `create_runtime()` factory function in `runtime.py` wires components
- Some implicit coupling via `os.environ` reads in providers/skills

**API Surface Stability: 7/10**
- Protocol interfaces in `interfaces.py` are stable contracts
- Pydantic models provide schema stability
- CLI built on Typer with structured options
- No public API versioning strategy

**Domain Separation: 9/10**
- Clear boundary between core (pipeline), skills (capabilities), playbooks (orchestration), providers (LLM), storage (persistence), and CLI (interface)
- Each layer has its own `interfaces.py` or `base.py` with contracts

**Architecture Diagram:**

```
┌─────────────────────────────────────────────┐
│           CLI Adapter (Typer)                │
│           cli/main.py (~2700 LOC)            │
└─────────────────┬───────────────────────────┘
                  │ TaskSpec
┌─────────────────▼───────────────────────────┐
│           Core Runtime Pipeline              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │ Planner  │→│Orchestr- │→│ Executor │     │
│  │V0/V1/V2/ │ │ator V0/V1│ │V0/V1/V2  │     │
│  │V3        │ │          │ │          │     │
│  └──────────┘ └────┬─────┘ └──────────┘     │
│                    │                         │
│  ┌──────────┐ ┌────▼─────┐                  │
│  │ Verifier │←│ Recorder │                  │
│  │V0/V1/V2  │ │ V0       │                  │
│  └──────────┘ └──────────┘                  │
└─────────┬───────────┬───────────────────────┘
          │           │
┌─────────▼──┐  ┌─────▼──────┐  ┌─────────────┐
│  Skills    │  │  Storage   │  │  Providers  │
│  Registry  │  │  SQLite +  │  │  OpenAI +   │
│  7 skills  │  │  Filesystem│  │  Stubs      │
└────────────┘  └────────────┘  └─────────────┘
```

**Architectural Risk Scoring:**

| Factor | Score | Notes |
|--------|-------|-------|
| Modularity | 9/10 | Clean protocol separation |
| Testability | 8/10 | FakeLLMProvider, full mock support |
| Extensibility | 8/10 | Plugin architecture for skills/playbooks |
| Scalability | 5/10 | Single-process, synchronous, no async |
| Resilience | 6/10 | Bounded retries, but no circuit breakers |
| Observability | 7/10 | RunTrace is thorough; no metrics/logging infra |

**Scalability Constraints:**
- Single-process synchronous execution — no async/await
- SQLite storage — single-writer constraint
- No horizontal scaling capability
- No caching layer
- Linear orchestration only (no parallel step execution yet)

### 2. Code Quality & Maintainability

#### Metrics

| Metric | Value | Assessment |
|--------|-------|------------|
| **Total Source Lines** | 14,292 | Moderate-size codebase |
| **Total Files** | 44 .py files | Well-organized |
| **Total Functions/Methods** | 364 | Reasonable density |
| **Test Count** | 814 (3 deselected) | Excellent test density |
| **Test Coverage** | **86%** | Good; exceeds 70% CI gate |
| **Lint Violations** | 0 (configured rules) | Clean |
| **Complex Functions (CC>10)** | 14 functions | **Attention needed** |
| **Highest Complexity** | CC=91 (`cli/main.py:run`) | **Critical refactor target** |

#### Cyclomatic Complexity (Functions CC > 10)

| Function | File | CC | Priority |
|----------|------|----|----------|
| `run()` | [cli/main.py](src/ag/cli/main.py#L392) | 91 | **CRITICAL** |
| `runs_show()` | [cli/main.py](src/ag/cli/main.py#L1412) | 39 | HIGH |
| `V1Orchestrator.run()` | [orchestrator.py](src/ag/core/orchestrator.py#L610) | 36 | HIGH |
| `V0Orchestrator.run()` | [orchestrator.py](src/ag/core/orchestrator.py#L145) | 27 | HIGH |
| `normalize_field_names()` | [emit_result.py](src/ag/skills/emit_result.py#L122) | 16 | MEDIUM |
| `_format_markdown()` | [emit_result.py](src/ag/skills/emit_result.py#L397) | 24 | HIGH |
| `doctor()` | [cli/main.py](src/ag/cli/main.py#L2724) | 22 | MEDIUM |
| `infer_artifact_category()` | [run_trace.py](src/ag/core/run_trace.py#L232) | 12 | LOW |
| `build_semantic_evidence()` | [verifier.py](src/ag/core/verifier.py#L395) | 14 | MEDIUM |
| `_parse_response()` | [planner.py](src/ag/core/planner.py#L444) | 12 | LOW |
| `_parse_feasibility_response()` | [planner.py](src/ag/core/planner.py#L1153) | 12 | LOW |
| `_parse_semantic_response()` | [verifier.py](src/ag/core/verifier.py#L319) | 11 | LOW |
| `execute()` (emit_result) | [emit_result.py](src/ag/skills/emit_result.py#L257) | 12 | LOW |
| `execute()` (load_documents) | [load_documents.py](src/ag/skills/load_documents.py#L139) | 10 | LOW |

#### Coverage by Module

| Module | Coverage | Gap Assessment |
|--------|----------|----------------|
| `core/` | 85-97% | Good — gaps in error paths |
| `providers/` | 85-100% | Good — OpenAI uncovered (requires API key) |
| `skills/` | 83-98% | Good — HTTP/network paths uncovered |
| `storage/` | 71-97% | `plan_store.py` at 71% needs attention |
| `playbooks/` | 75-100% | Registry at 75% |
| `cli/` | Not separately measured | Part of overall 86% |

#### Static Analysis

| Tool | Status | Result |
|------|--------|--------|
| Ruff (E, F, I, W) | PASS | 0 violations |
| Ruff format | PASS | All formatted |
| McCabe (CC>10) | 14 violations | See complexity table |
| Bandit (S rules) | 6 findings | Silent exception swallowing (S110/S112) |
| mypy strict | Configured | Strict mode enabled |

#### Dead Code Assessment

- No unused imports detected (ruff F rule active)
- Stub providers (Anthropic, Local) are placeholder code — intentional
- `FakeLLMProvider` in stubs.py used only in tests — appropriate

#### Documentation Completeness

| Document | Status |
|----------|--------|
| ARCHITECTURE.md | Comprehensive, current |
| README.md | Complete with setup instructions |
| CLI_REFERENCE.md | Exists |
| CHANGELOG.md | Maintained |
| Inline docstrings | Present on public APIs |
| API documentation | Not generated (no Sphinx/MkDocs) |

#### Code Quality Scorecard

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Coverage | 8.6/10 | 20% | 1.72 |
| Complexity | 6/10 | 15% | 0.90 |
| Lint cleanness | 9/10 | 10% | 0.90 |
| Architecture | 9/10 | 20% | 1.80 |
| Documentation | 7/10 | 15% | 1.05 |
| Test quality | 8/10 | 10% | 0.80 |
| Type safety | 8/10 | 10% | 0.80 |
| **Total** | | | **7.97/10** |

#### Refactor Priority Matrix

| Priority | Target | Impact | Effort |
|----------|--------|--------|--------|
| P1 | `cli/main.py:run()` CC=91 — split into sub-commands | High — maintainability | Medium |
| P1 | `cli/main.py:runs_show()` CC=39 — extract formatters | Medium — readability | Low |
| P2 | `orchestrator.py` V0/V1 duplication | Medium — maintainability | Medium |
| P2 | `emit_result.py` complexity (3 functions) | Medium — testability | Medium |
| P3 | `plan_store.py` coverage gap (71%) | Low — correctness confidence | Low |

### 3. Security Audit

#### Application Security

| Check | Status | Details |
|-------|--------|---------|
| **Input Validation** | PASS | Pydantic models validate all inputs; TaskSpec enforced |
| **Injection Vulnerabilities** | PASS | No eval/exec/subprocess; SQL uses parameterized queries |
| **AuthZ/AuthN Logic** | N/A | No authentication system; CLI tool |
| **Token Handling** | PASS | API keys from env vars; not logged/printed |
| **Session Management** | N/A | Stateless CLI; no sessions |
| **Path Traversal** | PASS | `_validate_safe_path_component()` prevents `..` injection |
| **Deserialization** | PASS | JSON + Pydantic only; no pickle/yaml.load |

#### Infrastructure Security

| Check | Status | Details |
|-------|--------|---------|
| **Secrets Management** | WARN | .env file with live API key exists locally (not in git) |
| **Key Storage** | WARN | No vault/keyring integration; plain environment variables |
| **Encryption at Rest** | N/A | SQLite unencrypted (local dev tool) |
| **Encryption in Transit** | PASS | httpx uses TLS by default |
| **Role-Based Access** | N/A | Single-user CLI tool |

#### Dependency Vulnerabilities (CVE Scan via pip-audit)

| Package | Version | CVE ID | Severity | Fix Version |
|---------|---------|--------|----------|-------------|
| `pip` | 25.2 | CVE-2025-8869 | — | 25.3 |
| `pip` | 25.2 | CVE-2026-1703 | — | 26.0 |
| `pygments` | 2.19.2 | CVE-2026-4539 | — | 2.20.0 |

**Note:** `pip` and `pygments` CVEs are in development tooling, not runtime. No CVEs in runtime dependencies.

**Packages not auditable** (not on PyPI): `ag-foundation` (local), `ddgs`, `primp` — these are installed from alternative sources.

#### Silent Exception Swallowing (Bandit S110/S112)

6 instances of `except Exception: pass/continue` found in:
- [orchestrator.py](src/ag/core/orchestrator.py) (4 instances) — workspace/provider initialization
- [plan_store.py](src/ag/storage/plan_store.py) (2 instances) — file parsing

**Risk:** Errors are silently discarded, making debugging difficult. Not a direct security vulnerability but could mask security-relevant failures.

#### Vulnerability Severity Report

| ID | Severity | Category | Location | Description |
|----|----------|----------|----------|-------------|
| SEC-001 | **CRITICAL** | Secrets Exposure | `.env` file | Live OpenAI API key in local `.env` file |
| SEC-002 | LOW | Silent Failures | `orchestrator.py` | 4x bare `except Exception: pass` |
| SEC-003 | LOW | Silent Failures | `plan_store.py` | 2x bare `except Exception: continue` |
| SEC-004 | INFO | No Key Rotation | Provider config | No key rotation/expiry mechanism |
| SEC-005 | INFO | Dev-only CVEs | pip, pygments | Known CVEs in dev tooling only |

#### OWASP Mapping

| OWASP Top 10 | Applicable? | Status |
|--------------|-------------|--------|
| A01:2021 Broken Access Control | No | CLI tool, no multi-user |
| A02:2021 Cryptographic Failures | No | No crypto operations |
| A03:2021 Injection | Yes | PASS — parameterized SQL, no eval |
| A04:2021 Insecure Design | Partial | PASS — protocol-based design |
| A05:2021 Security Misconfiguration | Yes | WARN — .env secret exposure |
| A06:2021 Vulnerable Components | Yes | LOW — dev-only CVEs |
| A07:2021 Auth Failures | No | No auth system |
| A08:2021 Data Integrity Failures | Partial | PASS — Pydantic validation |
| A09:2021 Logging Failures | Yes | WARN — silent exception swallowing |
| A10:2021 SSRF | Partial | LOW — URL fetch skill accepts user URLs |

#### Exploit Surface Analysis

- **Attack surface is small**: CLI tool, no network listeners, no API server
- **LLM prompt injection**: User prompts are passed to LLM — standard risk for all LLM applications
- **URL fetch skill**: Accepts URLs for web research — could be directed to internal network resources (SSRF risk in future API deployment)
- **Workspace file read**: `load_documents` skill reads from workspace path — bounded by path validation

#### Insider Threat Exposure

- Single author — full codebase knowledge
- No access controls on repository
- No signed commits
- No branch protection rules observed

### 4. Compliance Audit

| Framework | Applicable? | Alignment | Gap |
|-----------|-------------|-----------|-----|
| **ITAR/EAR** | No | N/A | No export-controlled technology |
| **GDPR** | Minimal | LOW RISK | No PII collection/processing; LLM prompts may contain user data → no DPA with OpenAI |
| **SOC2** | Not applicable | N/A | Pre-production; no customer data |
| **NIST 800-171** | Not applicable | N/A | No CUI handling |
| **CMMC** | Not applicable | N/A | No DoD context |

**Controlled Technical Data Exposure:** NONE  
**Data Residency Violations:** NONE (data stays local in SQLite)  
**Foreign Access Risks:** OpenAI API sends prompts to US-based servers  
**Logging Insufficiencies:** RunTrace provides execution audit trail; no structured security logging  

#### Compliance Gap Analysis

| Control Area | Status | Finding |
|-------------|--------|---------|
| Data Classification | NOT IMPLEMENTED | No data classification scheme |
| Audit Logging | PARTIAL | RunTrace captures execution; no security event logging |
| Access Control | NOT IMPLEMENTED | Single-user CLI; no RBAC |
| Incident Response | NOT IMPLEMENTED | No IR playbook |
| Change Management | PARTIAL | Git-based; no formal change approval process |
| Vendor Management | NOT IMPLEMENTED | No DPA with OpenAI |

**Regulatory Exposure Score: 2/10** (Low — pre-production CLI tool with minimal data handling)

---

## PART III — DEVOPS & OPERATIONAL REVIEW

| Capability | Status | Maturity |
|------------|--------|----------|
| **CI/CD Pipeline** | GitHub Actions | Basic — lint + test + coverage |
| **Pipeline Integrity** | PARTIAL | No signed artifacts, no SBOM |
| **Environment Parity** | NOT APPLICABLE | No staging/prod; dev-only |
| **Rollback Procedures** | Git-based | Manual git revert only |
| **Infrastructure Automation** | NONE | No IaC; local dev tool |
| **Observability** | MINIMAL | RunTrace only; no metrics/APM |
| **Logging** | MINIMAL | Console output via Rich; no structured logs |
| **Disaster Recovery** | NONE | Local SQLite; no backup strategy |
| **RTO/RPO** | UNDEFINED | Pre-production |
| **Vendor Lock-in** | LOW | Provider abstraction for LLMs |
| **Cloud Architecture** | NONE | Not deployed to cloud |
| **Pre-commit Hooks** | YES | `.pre-commit-config.yaml` exists |
| **Multi-Python Testing** | YES | Matrix: 3.10, 3.11, 3.12 |

#### CI/CD Pipeline Details

```yaml
Trigger: push/PR to main
Jobs:
  1. lint-and-test (matrix: 3.10, 3.11, 3.12)
     - ruff check, ruff format --check
     - pytest -W error --cov --cov-fail-under=70
  2. coverage (Python 3.11 only, depends on job 1)
     - pytest --cov --cov-fail-under=70
```

**Missing from CI:**
- Security scanning (SAST/DAST)
- Dependency audit (pip-audit)
- Container scanning
- SBOM generation
- Artifact signing
- Deployment stages
- Integration test gate
- Performance benchmarks

#### DevOps Maturity Score: **3/10**

| Level | Description | Status |
|-------|-------------|--------|
| L1 — Version Control | Git + GitHub | ACHIEVED |
| L2 — Basic CI | Lint + Test | ACHIEVED |
| L3 — Automated Testing | Coverage gates | ACHIEVED |
| L4 — Security Scanning | SAST/DAST/SCA | NOT ACHIEVED |
| L5 — Deployment Automation | CD pipeline | NOT ACHIEVED |
| L6 — Observability | Metrics/logs/traces | NOT ACHIEVED |
| L7 — Chaos Engineering | Resilience testing | NOT ACHIEVED |

#### Deployment Risk Assessment: LOW (not deployed)  
#### Incident Readiness Assessment: NOT APPLICABLE (pre-production)

---

## PART IV — DATA & AI MODEL AUDIT

| Aspect | Finding |
|--------|---------|
| **Training Data** | No ML models trained; uses third-party LLM (OpenAI) via API |
| **Data Licensing** | N/A — no training data |
| **Model Reproducibility** | N/A — no owned models |
| **Bias Exposure** | Inherits OpenAI model biases; no mitigation layer |
| **Export Classification** | N/A — no model weights |
| **Sensitive Dataset Contamination** | N/A |
| **PII Presence** | No PII stored; user prompts may contain PII and are sent to OpenAI |

#### LLM Integration Risk

| Risk | Severity | Details |
|------|----------|---------|
| Prompt injection | MEDIUM | User prompts passed to LLM without sanitization (standard for LLM tools) |
| Data leakage to LLM provider | MEDIUM | Workspace content sent to OpenAI for summarization/research |
| No DPA with OpenAI | LOW | Pre-production; no customer data |
| Model dependency | MEDIUM | Core functionality depends on OpenAI API availability |

#### Data Lineage Map  

```
User Prompt → TaskSpec (validated) → Planner (LLM call) → ExecutionPlan
    ↓
Workspace Files → load_documents skill → LLM (summarize/research)
    ↓
Web URLs → fetch_web_content skill → LLM (synthesize)
    ↓
LLM Response → Pydantic validation → RunTrace → SQLite + JSON files
```

**Data Governance Gap Analysis:**
- No data classification policy
- No data retention policy (SQLite grows unbounded)
- No data deletion capability (no "right to erasure")
- No data access logging beyond RunTrace

---

## PART V — RISK SCORING

| Category | Risk Level | Impact | Remediation Urgency |
|----------|-----------|--------|---------------------|
| **IP Ownership** | MEDIUM | HIGH | 0–30 Days |
| **License Risk** | LOW | LOW | 30–90 Days |
| **Security** | MEDIUM | MEDIUM | 0–30 Days |
| **Compliance** | LOW | LOW | 3–9 Months |
| **Architecture** | LOW | LOW | Strategic |
| **DevOps** | MEDIUM | MEDIUM | 30–90 Days |
| **Data Risk** | LOW | MEDIUM | 3–9 Months |

### Risk Heatmap

```
              LOW Impact    MEDIUM Impact    HIGH Impact
HIGH Risk    │             │                │
             │             │                │
MEDIUM Risk  │             │ Security       │ IP Ownership
             │             │ DevOps         │
LOW Risk     │ License     │ Data Risk      │
             │ Compliance  │                │
             │ Architecture│                │
```

---

## PART VI — REMEDIATION PLAN

### Phase 1: Immediate (0–30 Days)

| # | Action | Category | Risk Reduction |
|---|--------|----------|----------------|
| 1 | **Rotate exposed OpenAI API key** | Security | Critical — key in .env must be revoked |
| 2 | **Create LICENSE file** (MIT) at repo root | IP | Formalizes licensing |
| 3 | **Execute IP assignment agreement** for author | IP | Establishes clear ownership chain |
| 4 | **Add .env to .gitignore verification** | Security | Already present; verify enforcement |
| 5 | **Upgrade pip to 26.0+, pygments to 2.20.0+** | Security | Resolves known CVEs |
| 6 | **Replace silent exception swallowing** with logging | Security | 6 instances in orchestrator.py, plan_store.py |

**Estimated effort:** 1–2 person-days  
**Risk reduction:** Eliminates CRITICAL secret exposure + IP ambiguity

### Phase 2: Short-Term (30–90 Days)

| # | Action | Category | Risk Reduction |
|---|--------|----------|----------------|
| 7 | **Refactor cli/main.py:run()** (CC=91) into sub-functions | Quality | Major maintainability improvement |
| 8 | **Add pip-audit to CI pipeline** | Security | Automated CVE detection |
| 9 | **Add SAST scanning** (e.g., Bandit via ruff S rules) to CI | Security | Code security gate |
| 10 | **Increase plan_store.py coverage** from 71% to 85%+ | Quality | Correctness confidence |
| 11 | **Add structured logging** (Python logging module) | Operations | Debugging/audit capability |
| 12 | **Create SECURITY.md** with vulnerability reporting policy | Governance | Standard OSS practice |
| 13 | **Add OpenAI DPA** if any customer/user data flows through | Compliance | GDPR alignment |
| 14 | **Pin dependency versions** or generate lockfile | Supply Chain | Reproducible builds |

**Estimated effort:** 3–5 person-days  
**Risk reduction:** Automated security gates + code quality uplift

### Phase 3: Medium-Term (3–9 Months)

| # | Action | Category | Risk Reduction |
|---|--------|----------|----------------|
| 15 | **Add async support** to pipeline | Architecture | Scalability enablement |
| 16 | **Implement structured security event logging** | Compliance | Audit trail for security events |
| 17 | **Add data retention policy** and cleanup mechanism | Data | Unbounded SQLite growth prevention |
| 18 | **Implement RBAC** for multi-user scenarios | Security | Pre-production readiness |
| 19 | **Add SBOM generation** to CI | Supply Chain | Dependency transparency |
| 20 | **API documentation generation** (MkDocs/Sphinx) | Documentation | Developer onboarding |
| 21 | **Establish formal change management process** | Governance | Audit trail for code changes |

**Estimated effort:** 15–25 person-days  
**Risk reduction:** Production readiness + compliance foundation

### Phase 4: Strategic (9–18 Months)

| # | Action | Category | Risk Reduction |
|---|--------|----------|----------------|
| 22 | **API server deployment** (if planned) | Architecture | New attack surface management |
| 23 | **SOC2 Type I preparation** | Compliance | Customer trust |
| 24 | **Multi-provider LLM strategy** (reduce OpenAI dependency) | Architecture | Vendor risk reduction |
| 25 | **DevSecOps integration** (full pipeline) | Operations | Mature security posture |
| 26 | **IP portfolio formalization** (patent evaluation) | IP | Strategic asset protection |
| 27 | **Performance benchmarking framework** | Quality | Regression detection |

**Estimated effort:** 40–60 person-days  
**Risk reduction:** Enterprise readiness + strategic positioning

### Risk Reduction Summary by Phase

| Phase | Cumulative Risk Reduction | Investment |
|-------|--------------------------|------------|
| Phase 1 (0–30d) | 40% | 1–2 person-days |
| Phase 2 (30–90d) | 65% | 3–5 person-days |
| Phase 3 (3–9mo) | 85% | 15–25 person-days |
| Phase 4 (9–18mo) | 95% | 40–60 person-days |

---

## PART VII — TECHNICAL HANDOVER FRAMEWORK

### 1. Code Transfer Protocol

| Step | Action | Status |
|------|--------|--------|
| 1.1 | GitHub repository ownership transfer | Required |
| 1.2 | PyPI package name reservation (`ag-foundation`) | Not yet published |
| 1.3 | **Credential rotation**: OpenAI API key, GitHub PAT | **CRITICAL** |
| 1.4 | GitHub Actions secrets update | Required |
| 1.5 | .env template verification | `.env.example` exists |
| 1.6 | Domain/namespace claims | None identified |
| 1.7 | Third-party API account ownership (OpenAI, optional search APIs) | Transfer required |

### 2. Documentation Requirements

| Document | Status | Action |
|----------|--------|--------|
| System Architecture Manual | EXISTS | [ARCHITECTURE.md](ARCHITECTURE.md) — comprehensive |
| API Contract Documentation | PARTIAL | Protocol interfaces documented; no API spec |
| Deployment Guide | NOT EXISTS | Needed if deploying beyond local dev |
| Data Schema Documentation | EXISTS | Pydantic models are self-documenting |
| Security Playbook | NOT EXISTS | Create SECURITY.md + incident response |
| Incident Response Guide | NOT EXISTS | Create IR playbook |
| Operational Runbook | NOT EXISTS | Create for production deployment |

### 3. Knowledge Transfer Plan

| Activity | Duration | Description |
|----------|----------|-------------|
| Architecture walkthrough | 2 hours | Pipeline design, component versioning, plugin architecture |
| Codebase tour | 2 hours | Key files, patterns, conventions |
| Sprint/governance briefing | 1 hour | GVS framework, sprint cadence, decision records |
| Testing strategy review | 1 hour | Test taxonomy, fixtures, coverage strategy |
| LLM integration deep-dive | 1 hour | Provider abstraction, prompt engineering, token tracking |
| Operational shadow period | 1–2 weeks | Pair development on new features |
| Escalation contact map | N/A | Single author — full knowledge transfer critical |

### 4. Governance Framework

| Policy | Status | Recommendation |
|--------|--------|----------------|
| Code Ownership Mapping | Git blame only | Formalize CODEOWNERS file |
| Change Approval Policy | Informal | Implement PR review requirements |
| Security Review Policy | Not defined | Add security review checklist for PRs |
| Release Management | Manual | Semver + CHANGELOG; consider automated releases |
| Compliance Review | Not defined | Add compliance checkpoints for data-handling changes |

---

## FINAL DELIVERABLES CHECKLIST

| # | Deliverable | Status |
|---|------------|--------|
| 1 | Executive Summary (Board-ready) | Included above |
| 2 | Risk Heatmap | Included in Part V |
| 3 | IP Asset Register | Included in Part I |
| 4 | Code Audit Report | Included in Part II |
| 5 | Security Findings Report | Included in Part II.3 |
| 6 | Compliance Gap Analysis | Included in Part II.4 |
| 7 | DevOps Assessment | Included in Part III |
| 8 | Remediation Roadmap | Included in Part VI |
| 9 | Handover Plan | Included in Part VII |

---

## APPENDIX A — TECHNICAL INVENTORY

### Source Code Inventory

| Module | Files | Est. LOC | Coverage |
|--------|-------|----------|----------|
| `core/` | 13 | ~4,500 | 85-97% |
| `cli/` | 1 | ~2,700 | Included in 86% |
| `skills/` | 9 | ~2,500 | 83-98% |
| `playbooks/` | 7 | ~700 | 75-100% |
| `providers/` | 4 | ~650 | 85-100% |
| `storage/` | 4 | ~900 | 71-97% |
| `config.py` | 1 | ~245 | ~95% |
| **TOTAL** | **44** | **~14,292** | **86%** |

### Test Inventory

| Test File | Purpose |
|-----------|---------|
| `test_runtime.py` | Core pipeline integration |
| `test_planner.py` | V0–V3 planner logic |
| `test_executor.py` | V0–V2 executor |
| `test_verifier.py` | V0–V2 verifier |
| `test_cli.py` | CLI command testing |
| `test_storage.py` | SQLite/filesystem persistence |
| `test_skill_framework.py` | Skill registry + execution |
| `test_e2e_integration.py` | End-to-end pipeline |
| `test_contracts.py` | Interface contract compliance |
| `test_config.py` | Configuration loading |
| + 14 more test files | Various subsystems |

### Environment Variable Registry

| Variable | Purpose | Required | Scope |
|----------|---------|----------|-------|
| `OPENAI_API_KEY` | OpenAI authentication | Yes (LLM mode) | Runtime |
| `AG_DEV` | Enable manual/dev mode | No | Development |
| `AG_CONFIG_PATH` | Config file override | No | Runtime |
| `AG_WORKSPACE` | Default workspace name | No | Runtime |
| `AG_WORKSPACE_DIR` | Workspace root directory | No | Testing |
| `SERPER_API_KEY` | Serper web search | No | Runtime (optional) |
| `GOOGLE_API_KEY` | Google Custom Search | No | Runtime (optional) |
| `GOOGLE_SEARCH_ENGINE_ID` | Google CX parameter | No | Runtime (optional) |
| `BING_API_KEY` | Bing web search | No | Runtime (optional) |

---

## APPENDIX B — EVIDENCE INDEX

All findings in this report are evidence-based with file references:

| Finding | Evidence Location |
|---------|-------------------|
| Live API key in .env | `.env` file (local, not in git history) |
| Parameterized SQL | [sqlite_store.py](src/ag/storage/sqlite_store.py) — all `conn.execute()` calls |
| Path traversal protection | [workspace.py](src/ag/storage/workspace.py) — `_validate_safe_path_component()` |
| Schema validation | [schema_verifier.py](src/ag/core/schema_verifier.py) — bounded retry loop |
| No eval/exec/subprocess | Full codebase grep — zero matches |
| Silent exceptions | [orchestrator.py](src/ag/core/orchestrator.py) L172, L203, L703, L724; [plan_store.py](src/ag/storage/plan_store.py) L87, L165 |
| CVE findings | pip-audit scan output (2026-04-12) |
| CI pipeline | [.github/workflows/ci.yml](.github/workflows/ci.yml) |
| .gitignore .env | [.gitignore](.gitignore) L58-61 |
| LICENSE missing | `file_search LICENSE*` — no results |
| Coverage 86% | pytest --cov output (2026-04-12) — 814 passed |
| Complexity CC=91 | ruff C90 + AST analysis of `cli/main.py:run()` |

---

*End of Report*
