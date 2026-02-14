"""Module for converting SCAD files to other formats."""

from __future__ import annotations

import logging
from pathlib import Path

from scad_mcp.models import ConvertRequest, ConvertResult
from scad_mcp.openscad.cli import run_openscad
from scad_mcp.validation import validate_scad_file

LOGGER = logging.getLogger("scad_mcp.openscad.converter")


async def convert_scad(
    request: ConvertRequest,
    openscad_path: Path,
) -> ConvertResult:
    """Convert a SCAD file to another format using OpenSCAD.

    Args:
        request: Convert request parameters.
        openscad_path: Path to the OpenSCAD executable.

    Returns:
        ConvertResult with output path and executed command.

    Raises:
        FileNotFoundError: When the SCAD file does not exist.
        RuntimeError: When the OpenSCAD command fails.
    """
    scad_file = request.scad_file
    validate_scad_file(scad_file)

    output_file = request.output_file
    output_file.parent.mkdir(parents=True, exist_ok=True)

    command = [
        str(openscad_path),
        "-o",
        str(output_file),
        str(scad_file),
    ]

    LOGGER.info("Converting %s to %s", scad_file, output_file)
    return_code, _, stderr = await run_openscad(command)

    if return_code != 0:
        LOGGER.error("OpenSCAD conversion failed: %s", stderr)
        raise RuntimeError(f"OpenSCAD conversion failed with code {return_code}: {stderr}")

    if not output_file.exists():
        LOGGER.error("OpenSCAD conversion failed: Output file not created.")
        raise RuntimeError("OpenSCAD conversion failed: Output file not created.")

    return ConvertResult(output_path=output_file, command=command)
