"""Emit Result Skill — V2 Artifact Output (AF0065, AF0067).

Stores structured output as a workspace artifact. This skill demonstrates
file output and artifact registration without LLM interaction.

Pipeline Position:
    This is step 3 (final) of the summarize_v0 playbook:
    load_documents → summarize_docs → emit_result

Schemas Defined (see docs/dev/additional/SCHEMA_INVENTORY.md):
    EmitResultInput  — Skill input (document_summary, key_points, sources, etc.)
    EmitResultOutput — Skill output (artifact_path, artifact_id)

Artifact Output:
    This skill writes the result to workspace/outputs/:
    - JSON file with structured summary data
    - Returns artifact_path and artifact_id for trace recording

Usage:
    skill = EmitResultSkill()
    output = skill.execute(
        EmitResultInput(
            document_summary="...",
            key_points=["point1", "point2"],
            artifact_name="summary"
        ),
        SkillContext(workspace_path=Path("/my/workspace"))
    )
    # output.artifact_path contains path to written file

See Also:
    - base.py: Skill ABC and base schema definitions
    - summarize_docs.py: Previous skill in pipeline (produces summary)
"""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import Field

from ag.skills.base import Skill, SkillContext, SkillInput, SkillOutput

if TYPE_CHECKING:
    pass


# ---------------------------------------------------------------------------
# Schema Definitions
# ---------------------------------------------------------------------------


class EmitResultInput(SkillInput):
    """Input schema for emit_result skill.

    Receives results from previous pipeline step (e.g., summarize_docs output).

    Attributes:
        document_summary: Summary text from previous step
        key_points: Key points extracted
        sources: Source file paths
        artifact_name: Name for the artifact file
        artifact_type: MIME type of the artifact
    """

    # Pipeline results from previous step
    document_summary: str = Field(
        default="",
        description="Summary text from previous step",
    )
    key_points: list[str] = Field(
        default_factory=list,
        description="Key points extracted",
    )
    sources: list[str] = Field(
        default_factory=list,
        description="Source file paths",
    )
    source_count: int = Field(
        default=0,
        description="Number of source files",
    )

    # Artifact configuration
    artifact_name: str = Field(
        default="summary.json",
        description="Name for the artifact file",
    )
    artifact_type: str = Field(
        default="application/json",
        description="MIME type of the artifact",
    )

    model_config = {"extra": "ignore"}  # Allow extra fields from pipeline


class EmitResultOutput(SkillOutput):
    """Output schema for emit_result skill.

    Attributes:
        artifact_id: Unique identifier for the artifact
        artifact_path: Path where artifact was stored
        bytes_written: Size of artifact in bytes
    """

    artifact_id: str = Field(
        default="",
        description="Unique identifier for the artifact",
    )
    artifact_path: str = Field(
        default="",
        description="Path where artifact was stored",
    )
    bytes_written: int = Field(
        default=0,
        ge=0,
        description="Size of artifact in bytes",
    )

    model_config = {"extra": "forbid"}


# ---------------------------------------------------------------------------
# Skill Implementation
# ---------------------------------------------------------------------------


class EmitResultSkill(Skill[EmitResultInput, EmitResultOutput]):
    """Store structured output as a workspace artifact.

    This skill serializes result data to JSON and stores it
    in the workspace's runs directory as an artifact.

    Example usage:
        skill = EmitResultSkill()
        ctx = SkillContext(
            workspace_path=Path("/my/workspace"),
            run_id="run-abc123",
        )
        input = EmitResultInput(
            data={"summary": "...", "key_points": [...]},
            artifact_name="summary.json",
        )
        output = skill.execute(input, ctx)
    """

    name: ClassVar[str] = "emit_result"
    description: ClassVar[str] = "Store structured output as workspace artifact"
    input_schema: ClassVar[type[SkillInput]] = EmitResultInput
    output_schema: ClassVar[type[SkillOutput]] = EmitResultOutput
    requires_llm: ClassVar[bool] = False

    def execute(
        self,
        input: EmitResultInput,
        ctx: SkillContext,
    ) -> EmitResultOutput:
        """Execute the emit_result skill.

        Args:
            input: Validated input with data and artifact name
            ctx: Runtime context with workspace path and run_id

        Returns:
            EmitResultOutput with artifact location info
        """
        # Validate workspace is available
        if not ctx.has_workspace or ctx.workspace_path is None:
            return EmitResultOutput(
                success=False,
                summary="No workspace path provided",
                error="missing_workspace_path",
            )

        workspace_path = ctx.workspace_path
        if not workspace_path.exists():
            return EmitResultOutput(
                success=False,
                summary=f"Workspace path does not exist: {workspace_path}",
                error="workspace_not_found",
            )

        try:
            # Generate artifact ID
            artifact_id = f"art-{uuid.uuid4().hex[:12]}"

            # Determine artifact path (in runs/<run_id>/ if available)
            if ctx.run_id:
                runs_dir = workspace_path / "runs" / ctx.run_id
            else:
                runs_dir = workspace_path / "runs" / "artifacts"

            runs_dir.mkdir(parents=True, exist_ok=True)
            artifact_path = runs_dir / input.artifact_name

            # Build output data from pipeline results
            output_data = {
                "artifact_id": artifact_id,
                "created_at": datetime.now(UTC).isoformat(),
                "run_id": ctx.run_id,
                "step_number": ctx.step_number,
                # Actual content from pipeline
                "summary": input.document_summary,
                "key_points": input.key_points,
                "sources": input.sources,
                "source_count": input.source_count,
            }

            # Write to file
            content = json.dumps(output_data, indent=2, default=str)
            artifact_path.write_text(content, encoding="utf-8")
            bytes_written = len(content.encode("utf-8"))

            # Return relative path from workspace
            rel_path = str(artifact_path.relative_to(workspace_path))

            return EmitResultOutput(
                success=True,
                summary=f"Artifact stored: {rel_path} ({bytes_written:,} bytes)",
                artifact_id=artifact_id,
                artifact_path=rel_path,
                bytes_written=bytes_written,
            )

        except Exception as e:
            return EmitResultOutput(
                success=False,
                summary=f"Failed to emit artifact: {e}",
                error=str(e),
            )

    def to_legacy_tuple(self, output: EmitResultOutput) -> tuple[bool, str, dict[str, Any]]:
        """Convert output to legacy skill return format."""
        return output.to_legacy_tuple()
