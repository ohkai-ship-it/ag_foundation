"""Load Documents Skill — V2 File Loading (AF0065, AF0067).

Reads files from workspace matching glob patterns and returns structured
document objects for downstream processing. This is a simple v2 skill
that demonstrates file I/O without LLM interaction.

Pipeline Position:
    This is step 1 of the summarize_v0 playbook:
    load_documents → summarize_docs → emit_result

Schemas Defined (see docs/dev/additional/SCHEMA_INVENTORY.md):
    Document           — Single loaded document (path, content, size_bytes)
    LoadDocumentsInput — Skill input (patterns, max_files, max_size_kb)
    LoadDocumentsOutput — Skill output (documents list, total_size)

Usage:
    skill = LoadDocumentsSkill()
    output = skill.execute(
        LoadDocumentsInput(patterns=["*.md"], max_files=10),
        SkillContext(workspace_path=Path("/my/workspace"))
    )
    # output.documents contains list of Document objects

See Also:
    - base.py: Skill ABC and base schema definitions
    - summarize_docs.py: Next skill in pipeline (consumes documents)
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import BaseModel, Field

from ag.skills.base import Skill, SkillContext, SkillInput, SkillOutput

if TYPE_CHECKING:
    pass


# ---------------------------------------------------------------------------
# Schema Definitions
# ---------------------------------------------------------------------------


class Document(BaseModel):
    """A document loaded from the workspace.

    Represents a single file with its path and content.
    """

    path: str = Field(..., description="Relative path to the document")
    content: str = Field(..., description="Full text content of the document")
    size_bytes: int = Field(..., ge=0, description="Size of content in bytes")

    model_config = {"extra": "forbid"}


class LoadDocumentsInput(SkillInput):
    """Input schema for load_documents skill.

    Attributes:
        patterns: Glob patterns to match files (default: ["**/*.md"])
        max_files: Maximum number of files to load (default: 10)
    """

    patterns: list[str] = Field(
        default=["**/*.md"],
        description="Glob patterns to match files",
    )
    max_files: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of files to load",
    )

    model_config = {"extra": "forbid"}


class LoadDocumentsOutput(SkillOutput):
    """Output schema for load_documents skill.

    Attributes:
        documents: List of loaded documents
        file_count: Number of files loaded
        total_bytes: Total size of all documents in bytes
    """

    documents: list[Document] = Field(
        default_factory=list,
        description="List of loaded documents",
    )
    file_count: int = Field(
        default=0,
        ge=0,
        description="Number of files loaded",
    )
    total_bytes: int = Field(
        default=0,
        ge=0,
        description="Total size of all documents in bytes",
    )

    model_config = {"extra": "forbid"}


# ---------------------------------------------------------------------------
# Skill Implementation
# ---------------------------------------------------------------------------


class LoadDocumentsSkill(Skill[LoadDocumentsInput, LoadDocumentsOutput]):
    """Load documents from workspace matching glob patterns.

    This skill reads files from the workspace inputs directory (or root
    if inputs/ doesn't exist) and returns their contents as structured
    Document objects.

    Example usage:
        skill = LoadDocumentsSkill()
        ctx = SkillContext(workspace_path=Path("/my/workspace"))
        input = LoadDocumentsInput(patterns=["**/*.md"], max_files=10)
        output = skill.execute(input, ctx)
        # output.documents contains list of Document objects
    """

    name: ClassVar[str] = "load_documents"
    description: ClassVar[str] = "Load documents from workspace matching glob patterns"
    input_schema: ClassVar[type[SkillInput]] = LoadDocumentsInput
    output_schema: ClassVar[type[SkillOutput]] = LoadDocumentsOutput
    requires_llm: ClassVar[bool] = False
    policy_flags: ClassVar[list[str]] = ["file_read"]  # AF-0100

    # Default fallback patterns used when user-specified patterns find nothing
    _FALLBACK_PATTERNS: ClassVar[list[str]] = ["**/*.md", "**/*.txt"]

    def execute(
        self,
        input: LoadDocumentsInput,
        ctx: SkillContext,
    ) -> LoadDocumentsOutput:
        """Execute the load_documents skill.

        Args:
            input: Validated input with patterns and max_files
            ctx: Runtime context with workspace path

        Returns:
            LoadDocumentsOutput with loaded documents
        """
        # Validate workspace is available
        if not ctx.has_workspace or ctx.workspace_path is None:
            return LoadDocumentsOutput(
                success=False,
                summary="No workspace path provided",
                error="missing_workspace_path",
            )

        workspace_path = ctx.workspace_path
        if not workspace_path.exists():
            return LoadDocumentsOutput(
                success=False,
                summary=f"Workspace path does not exist: {workspace_path}",
                error="workspace_not_found",
            )

        # Use inputs/ subfolder if it exists (AF0058 structure)
        inputs_path = ctx.inputs_path
        if inputs_path is None or not inputs_path.exists():
            inputs_path = workspace_path

        try:
            documents = self._load_files(inputs_path, input.patterns, input.max_files)

            # AF-0107: fallback when user/planner patterns find nothing
            if not documents and input.patterns != self._FALLBACK_PATTERNS:
                documents = self._load_files(inputs_path, self._FALLBACK_PATTERNS, input.max_files)

            if not documents:
                return LoadDocumentsOutput(
                    success=False,
                    summary=f"No files found matching patterns: {input.patterns}",
                    error="no_files_found",
                )

            total_bytes = sum(doc.size_bytes for doc in documents)

            return LoadDocumentsOutput(
                success=True,
                summary=f"Loaded {len(documents)} documents ({total_bytes:,} bytes)",
                documents=documents,
                file_count=len(documents),
                total_bytes=total_bytes,
            )

        except Exception as e:
            return LoadDocumentsOutput(
                success=False,
                summary=f"Failed to load documents: {e}",
                error=str(e),
            )

    def _load_files(
        self,
        base_path: Path,
        patterns: list[str],
        max_files: int,
    ) -> list[Document]:
        """Load files matching glob patterns.

        Args:
            base_path: Base directory to search from
            patterns: Glob patterns to match
            max_files: Maximum number of files to load

        Returns:
            List of Document objects
        """
        documents: list[Document] = []
        seen_paths: set[Path] = set()

        for pattern in patterns:
            if len(documents) >= max_files:
                break

            # Match files using glob
            for file_path in base_path.glob(pattern):
                if len(documents) >= max_files:
                    break

                # Skip directories and already-seen files
                if not file_path.is_file() or file_path in seen_paths:
                    continue
                seen_paths.add(file_path)

                # Try to read the file
                try:
                    content = file_path.read_text(encoding="utf-8")
                    rel_path = str(file_path.relative_to(base_path))

                    documents.append(
                        Document(
                            path=rel_path,
                            content=content,
                            size_bytes=len(content.encode("utf-8")),
                        )
                    )
                except (OSError, UnicodeDecodeError):
                    # Skip files that can't be read
                    continue

        return documents

    def to_legacy_tuple(self, output: LoadDocumentsOutput) -> tuple[bool, str, dict[str, Any]]:
        """Convert output to legacy skill return format."""
        return output.to_legacy_tuple()
