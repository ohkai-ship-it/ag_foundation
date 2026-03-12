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

from pydantic import Field, model_validator

from ag.skills.base import Skill, SkillContext, SkillInput, SkillOutput

if TYPE_CHECKING:
    pass


# ---------------------------------------------------------------------------
# Schema Definitions
# ---------------------------------------------------------------------------


class EmitResultInput(SkillInput):
    """Input schema for emit_result skill.

    Receives results from previous pipeline step (e.g., summarize_docs or
    synthesize_research output).

    Attributes:
        document_summary: Summary text from previous step (or 'report')
        key_points: Key points extracted (or 'key_findings')
        sources: Source file paths (or 'sources_used')
        artifact_name: Name for the artifact file
        artifact_type: MIME type of the artifact

    Note:
        Accepts both summarize_docs schema (document_summary, key_points, sources)
        and synthesize_research schema (report, key_findings, sources_used).
    """

    # Pipeline results from previous step (canonical field names)
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

    # Aliased fields from synthesize_research (normalized by validator)
    report: str = Field(
        default="",
        description="Alias for document_summary (from synthesize_research)",
    )
    key_findings: list[str] = Field(
        default_factory=list,
        description="Alias for key_points (from synthesize_research)",
    )
    sources_used: list[str] = Field(
        default_factory=list,
        description="Alias for sources (from synthesize_research)",
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

    @model_validator(mode="before")
    @classmethod
    def normalize_field_names(cls, data: dict) -> dict:
        """Normalize synthesize_research schema to emit_result schema.

        Maps:
            report → document_summary
            key_findings → key_points
            sources_used → sources
        """
        if isinstance(data, dict):
            # Map synthesize_research fields to emit_result canonical fields
            if "report" in data and not data.get("document_summary"):
                data["document_summary"] = data["report"]
            if "key_findings" in data and not data.get("key_points"):
                data["key_points"] = data["key_findings"]
            if "sources_used" in data and not data.get("sources"):
                data["sources"] = data["sources_used"]
        return data


class EmitResultOutput(SkillOutput):
    """Output schema for emit_result skill.

    Attributes:
        artifact_id: Unique identifier for the artifact
        artifact_path: Path where artifact was stored
        artifact_type: MIME type of the artifact
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
    artifact_type: str = Field(
        default="application/json",
        description="MIME type of the artifact",
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

            # Determine artifact path (in runs/<run_id>/artifacts/ if available)
            if ctx.run_id:
                artifacts_dir = workspace_path / "runs" / ctx.run_id / "artifacts"
            else:
                artifacts_dir = workspace_path / "runs" / "artifacts"

            artifacts_dir.mkdir(parents=True, exist_ok=True)

            # AF-0090: Determine output format from artifact_type parameter
            # For backwards compatibility, also infer from filename extension if artifact_type
            # is the default value and filename has a recognized extension
            default_mime = "application/json"
            requested_mime = input.artifact_type
            artifact_name_lower = input.artifact_name.lower()

            # Backwards compatibility: infer from filename extension if using default type
            if requested_mime == default_mime:
                if artifact_name_lower.endswith((".md", ".markdown")):
                    requested_mime = "text/markdown"
                elif artifact_name_lower.endswith(".txt"):
                    requested_mime = "text/plain"
                # else keep default application/json

            # Map MIME types to file extensions
            mime_to_ext = {
                "text/markdown": ".md",
                "text/plain": ".txt",
                "application/json": ".json",
            }

            is_markdown = requested_mime == "text/markdown"
            is_plain_text = requested_mime == "text/plain"

            # Determine correct file extension based on MIME type
            correct_ext = mime_to_ext.get(requested_mime, ".json")

            # Use artifact_name but ensure correct extension for the MIME type
            artifact_base = input.artifact_name
            # Strip any existing extension if it doesn't match requested type
            if artifact_base.endswith((".md", ".markdown", ".json", ".txt")):
                artifact_base = artifact_base.rsplit(".", 1)[0]
            artifact_filename = artifact_base + correct_ext

            artifact_path = artifacts_dir / artifact_filename

            if is_markdown:
                # Write markdown format for text/markdown
                # AF-0082: Pass trace metadata for polished reports
                content = self._format_markdown(input, artifact_id, ctx.run_id, ctx.trace_metadata)
                mime_type = "text/markdown"
            elif is_plain_text:
                # Write plain text for text/plain
                content = self._format_plain_text(input)
                mime_type = "text/plain"
            else:
                # Write JSON format (default)
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
                content = json.dumps(output_data, indent=2, default=str)
                mime_type = "application/json"

            # Write to file
            artifact_path.write_text(content, encoding="utf-8")
            bytes_written = len(content.encode("utf-8"))

            # Return relative path from workspace
            rel_path = str(artifact_path.relative_to(workspace_path))

            return EmitResultOutput(
                success=True,
                summary=f"Artifact stored: {rel_path} ({bytes_written:,} bytes)",
                artifact_id=artifact_id,
                artifact_path=rel_path,
                artifact_type=mime_type,
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

    def _format_markdown(
        self,
        input: EmitResultInput,
        artifact_id: str,
        run_id: str | None,
        trace_metadata: dict[str, Any] | None = None,
    ) -> str:
        """Format result as markdown document.

        Args:
            input: Skill input with document_summary, key_points, sources
            artifact_id: Generated artifact ID
            run_id: Optional run ID
            trace_metadata: Optional trace metadata (AF-0082) with:
                - elapsed_ms: Duration so far
                - model: LLM model name
                - playbook_name: Playbook name
                - playbook_version: Playbook version
                - steps_summary: List of {skill, duration_ms, output_summary}

        Returns:
            Formatted markdown string
        """
        lines = []

        # Title - use first 50 chars of summary if available
        title = "Research Report"
        if input.document_summary:
            # Extract first sentence or first 50 chars for title
            first_line = input.document_summary.split("\n")[0]
            if len(first_line) > 60:
                title = f"Research Report: {first_line[:50]}..."
            elif first_line:
                title = f"Research Report: {first_line}"

        lines.append(f"# {title}")
        lines.append("")

        # AF-0082: Visible metadata header
        lines.append(f"**Generated:** {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        if trace_metadata:
            if "elapsed_ms" in trace_metadata:
                duration_s = trace_metadata["elapsed_ms"] / 1000
                lines.append(f"**Duration:** {duration_s:.1f} seconds")
            if "model" in trace_metadata:
                lines.append(f"**Model:** {trace_metadata['model']}")
            if "playbook_name" in trace_metadata:
                pb_name = trace_metadata["playbook_name"]
                pb_ver = trace_metadata.get("playbook_version", "")
                if pb_ver:
                    lines.append(f"**Playbook:** {pb_name}@{pb_ver}")
                else:
                    lines.append(f"**Playbook:** {pb_name}")

        # Hidden metadata for traceability
        lines.append("")
        lines.append(f"<!-- artifact_id: {artifact_id} -->")
        if run_id:
            lines.append(f"<!-- run_id: {run_id} -->")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Summary/Report
        if input.document_summary:
            lines.append("## Summary")
            lines.append("")
            lines.append(input.document_summary)
            lines.append("")

        # Key Points/Findings
        if input.key_points:
            lines.append("---")
            lines.append("")
            lines.append("## Key Findings")
            lines.append("")
            for point in input.key_points:
                lines.append(f"- {point}")
            lines.append("")

        # Sources - with clickable links for URLs
        if input.sources:
            lines.append("---")
            lines.append("")
            lines.append("## Sources")
            lines.append("")
            lines.append("| # | Source |")
            lines.append("|---|--------|")
            for i, source in enumerate(input.sources, 1):
                # Make URLs clickable
                if source.startswith(("http://", "https://")):
                    # Extract domain for display
                    try:
                        from urllib.parse import urlparse

                        parsed = urlparse(source)
                        display = parsed.netloc + parsed.path[:30]
                        if len(parsed.path) > 30:
                            display += "..."
                        lines.append(f"| {i} | [{display}]({source}) |")
                    except Exception:
                        lines.append(f"| {i} | [{source}]({source}) |")
                else:
                    lines.append(f"| {i} | {source} |")
            lines.append("")

        # AF-0082: Execution details table
        if trace_metadata and trace_metadata.get("steps_summary"):
            lines.append("---")
            lines.append("")
            lines.append("## Execution Details")
            lines.append("")
            lines.append("| Step | Skill | Duration | Output |")
            lines.append("|------|-------|----------|--------|")

            for idx, step_info in enumerate(trace_metadata["steps_summary"]):
                skill = step_info.get("skill", "-")
                duration_ms = step_info.get("duration_ms", 0)
                output = step_info.get("output_summary", "-")[:50]
                if len(step_info.get("output_summary", "")) > 50:
                    output += "..."
                # Format duration nicely
                if duration_ms >= 1000:
                    duration_str = f"{duration_ms / 1000:.1f}s"
                else:
                    duration_str = f"{duration_ms}ms"
                lines.append(f"| {idx} | {skill} | {duration_str} | {output} |")

            # Total duration
            if "elapsed_ms" in trace_metadata:
                total_s = trace_metadata["elapsed_ms"] / 1000
                lines.append("")
                lines.append(f"**Total Duration:** {total_s:.1f}s")

            if run_id:
                lines.append(f"**Run ID:** `{run_id}`")

            lines.append("")

        return "\n".join(lines)

    def _format_plain_text(self, input: EmitResultInput) -> str:
        """Format result as plain text document.

        Args:
            input: Skill input with document_summary, key_points, sources

        Returns:
            Formatted plain text string
        """
        lines = []

        # Summary/Report
        if input.document_summary:
            lines.append("SUMMARY")
            lines.append("=" * 40)
            lines.append(input.document_summary)
            lines.append("")

        # Key Points/Findings
        if input.key_points:
            lines.append("KEY FINDINGS")
            lines.append("=" * 40)
            for i, point in enumerate(input.key_points, 1):
                lines.append(f"{i}. {point}")
            lines.append("")

        # Sources
        if input.sources:
            lines.append("SOURCES")
            lines.append("=" * 40)
            for i, source in enumerate(input.sources, 1):
                lines.append(f"{i}. {source}")
            lines.append("")

        return "\n".join(lines)
