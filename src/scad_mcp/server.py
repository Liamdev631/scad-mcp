"""MCP server entry point for OpenSCAD tooling."""

from __future__ import annotations

import logging

from mcp.server.fastmcp import FastMCP

from scad_mcp.config import load_config
from scad_mcp.logging_setup import configure_logging
from scad_mcp.tools import check_openscad, render_model

LOGGER = logging.getLogger("scad_mcp.server")

app_config = load_config()
configure_logging(app_config.logging.level)

mcp = FastMCP(app_config.server.name)

@mcp.tool()
async def openscad_installation_checker() -> dict[str, str | bool | None]:
    """Check for OpenSCAD installation information.

    Returns:
        Dict with installation details including path and version.
    """
    try:
        # Force system search by ignoring configured path
        from dataclasses import replace
        config_force_search = replace(app_config, openscad=replace(app_config.openscad, path=None))
        return await check_openscad(config_force_search)
    except Exception:
        LOGGER.exception("OpenSCAD installation check failed.")
        raise


@mcp.tool()
async def scad_model_renderer(
    scad_file: str,
    projection: str | None = None,
    fov: float | None = None,
    angles: list[str] | None = None,
    output_dir: str | None = None,
    img_width: int = 1920,
    img_height: int = 1080,
    openscad_path: str | None = None,
) -> dict[str, str | list[str]]:
    """Render a SCAD file to an image.

    Args:
        scad_file: Path to the .scad file.
        projection: Perspective or orthographic projection.
        fov: Field of view in degrees (ignored if projection is orthographic).
        angles: One or two view angles. Final angle is the mean of the two. Choices are "front", "back", "left", "right", "top", "bottom".
        output_dir: Optional output directory for renders.
        img_width: Output image width in pixels.
        img_height: Output image height in pixels.
        openscad_path: Optional path to OpenSCAD executable.

    Returns:
        Dict containing image path and command used.
    """
    try:
        return await render_model(
            config=app_config,
            scad_file=scad_file,
            projection=projection,
            fov=fov,
            angles=angles or ["front"],
            output_dir=output_dir,
            img_width=img_width,
            img_height=img_height,
            openscad_path=openscad_path,
        )
    except Exception:
        LOGGER.exception("Render tool failed for %s", scad_file)
        raise


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
