"""MCP tool for converting SCAD files."""

from __future__ import annotations

import logging
from pathlib import Path

from scad_mcp.config.models import AppConfig
from scad_mcp.models import ConvertRequest
from scad_mcp.openscad.installer import find_openscad_executable
from scad_mcp.openscad.converter import convert_scad
from scad_mcp.tools.model_renderer import RENDER_LOCK

LOGGER = logging.getLogger("scad_mcp.tools.model_converter")


async def convert_model(
    config: AppConfig,
    scad_file: str,
    output_format: str | None = None,
    output_path: str | None = None,
) -> dict[str, str | list[str]]:
    """Convert a SCAD file to another format.

    Args:
        config: Application configuration.
        scad_file: Path to the .scad file.
        output_format: Target format (e.g. "stl", "3mf", "amf"). Optional if output_path is provided.
        output_path: Optional explicit output path. If provided, output_format is ignored.

    Returns:
        Dict with output file path and command used.
    """
    scad_path = Path(scad_file)

    if output_path:
        out_path = Path(output_path)
    elif output_format:
        out_path = scad_path.with_suffix(f".{output_format.lstrip('.')}")
    else:
        raise ValueError("Either output_format or output_path must be provided.")

    request = ConvertRequest(
        scad_file=scad_path,
        output_file=out_path,
    )

    executable_path = config.openscad.path
    resolved_path = find_openscad_executable(executable_path)

    if not resolved_path:
        LOGGER.error("OpenSCAD executable not found for conversion.")
        raise RuntimeError("OpenSCAD executable not found.")

    try:
        # Use the same lock as rendering since OpenSCAD is single-threaded
        async with RENDER_LOCK:
            result = await convert_scad(
                request=request,
                openscad_path=resolved_path,
            )
    except Exception:
        LOGGER.exception("Conversion failed for %s", scad_file)
        raise

    return {
        "output_path": str(result.output_path),
        "command": result.command,
    }
