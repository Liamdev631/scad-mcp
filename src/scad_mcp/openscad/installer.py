"""OpenSCAD discovery and version inspection utilities."""

from __future__ import annotations

import logging
import os
from pathlib import Path
import shutil

from scad_mcp.models import OpenScadInfo
from scad_mcp.openscad.cli import resolve_openscad_path, run_openscad

LOGGER = logging.getLogger("scad_mcp.openscad.installer")

def default_windows_paths() -> list[Path]:
    """Return default Windows OpenSCAD installation paths.

    Returns:
        List of common installation locations on Windows.
    """
    return [
        Path(r"C:\Program Files\OpenSCAD\openscad.exe"),
        Path(r"C:\Program Files (x86)\OpenSCAD\openscad.exe"),
    ]


def find_openscad_executable(configured_path: Path | None) -> Path | None:
    """Find the OpenSCAD executable using config, PATH, and defaults.

    Args:
        configured_path: Optional configured executable path.

    Returns:
        Resolved executable path or None if not found.
    """
    candidates: list[Path] = []
    if configured_path:
        candidates.append(configured_path)
    which_path = shutil.which("openscad")
    if which_path:
        candidates.append(Path(which_path))
    if os.name == "nt":
        candidates.extend(default_windows_paths())
    return resolve_openscad_path(candidates)

async def get_openscad_info(configured_path: Path | None) -> OpenScadInfo:
    """Return OpenSCAD installation details and version info.

    Args:
        configured_path: Optional configured executable path.

    Returns:
        OpenScadInfo describing installation state.
    """
    path = find_openscad_executable(configured_path)
    if not path:
        LOGGER.warning("OpenSCAD executable not found.")
        return OpenScadInfo(
            found=False,
            path=None,
            version=None,
            details="OpenSCAD executable not found in PATH or configured location.",
        )
    exit_code, stdout, stderr = await run_openscad([str(path), "--version"])
    if exit_code != 0:
        LOGGER.error("OpenSCAD returned non-zero exit code: %s", stderr.strip())
        return OpenScadInfo(
            found=False,
            path=path,
            version=None,
            details=stderr.strip() or "OpenSCAD returned a non-zero exit code.",
        )
    version_line = stdout.strip().splitlines()[0] if stdout.strip() else "Unknown"
    LOGGER.info("OpenSCAD detected at %s", path)
    return OpenScadInfo(
        found=True,
        path=path,
        version=version_line,
        details="OpenSCAD detected successfully.",
    )
