"""OpenSCAD CLI invocation helpers."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path


LOGGER = logging.getLogger("scad_mcp.openscad.cli")


async def run_openscad(command: list[str]) -> tuple[int, str, str]:
    """Run an OpenSCAD subprocess and capture output.

    Args:
        command: Command list passed to the OpenSCAD executable.

    Returns:
        Tuple of exit code, stdout, and stderr.
    """
    LOGGER.debug("Running OpenSCAD command: %s", " ".join(command))
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    return process.returncode or 0, stdout.decode("utf-8", "ignore"), stderr.decode("utf-8", "ignore")


def resolve_openscad_path(candidates: list[Path]) -> Path | None:
    """Return the first existing path from candidates.

    Args:
        candidates: Candidate executable paths.

    Returns:
        First existing path or None if not found.
    """
    for candidate in candidates:
        if candidate and candidate.exists():
            return candidate
    return None
