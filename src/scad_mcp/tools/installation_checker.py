"""MCP tool for OpenSCAD installation checks."""

from __future__ import annotations

from scad_mcp.config.models import AppConfig
from scad_mcp.openscad.installer import get_openscad_info


async def check_openscad(config: AppConfig) -> dict[str, str | bool | None]:
    """Return OpenSCAD installation data for the MCP tool response.

    Args:
        config: Application configuration.

    Returns:
        Dict with installation details for the MCP tool response.
    """
    info = await get_openscad_info(config.openscad.path)
    return {
        "found": info.found,
        "path": str(info.path) if info.path else None,
        "version": info.version,
        "details": info.details,
    }
