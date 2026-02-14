"""MCP tool for rendering SCAD files."""

from __future__ import annotations

import logging
import asyncio
from pathlib import Path

from scad_mcp.config.models import AppConfig
from scad_mcp.models import RenderRequest
from scad_mcp.openscad.installer import find_openscad_executable
from scad_mcp.openscad.renderer import render_scad

LOGGER = logging.getLogger("scad_mcp.tools.model_renderer")

# Global lock to ensure only one OpenSCAD instance runs at a time
RENDER_LOCK = asyncio.Lock()

async def render_model(
    config: AppConfig,
    scad_file: str,
    projection: str | None,
    fov: float | None,
    angles: list[str],
    output_dir: str | None,
    img_width: int | None = None,
    img_height: int | None = None,
    openscad_path: str | None = None,
) -> dict[str, str | list[str]]:
    """Render a SCAD file and return output metadata.

    Args:
        config: Application configuration.
        scad_file: Path to the .scad file.
        projection: Perspective or orthographic projection.
        fov: Field of view in degrees.
        angles: One or two view angles. The final angle is the mean of the two. Choices are "front", "back", "left", "right", "top", "bottom".
        output_dir: Optional output directory for renders.
        img_width: Output image width in pixels.
        img_height: Output image height in pixels.
        openscad_path: Optional path to OpenSCAD executable.

    Returns:
        Dict with rendered image path and command used.
    """
    render_cfg = config.render
    angle_list = angles or ["front"]
    request = RenderRequest(
        scad_file=Path(scad_file),
        projection=projection or render_cfg.projection,
        fov=fov if fov is not None else render_cfg.fov,
        angles=angle_list,
        output_dir=Path(output_dir) if output_dir else render_cfg.output_dir,
    )
    
    executable_path = Path(openscad_path) if openscad_path else config.openscad.path
    resolved_path = find_openscad_executable(executable_path)
    
    if not resolved_path:
        LOGGER.error("OpenSCAD executable not found for render.")
        raise RuntimeError("OpenSCAD executable not found.")
    try:
        async with RENDER_LOCK:
            result = await render_scad(
                request=request,
                openscad_path=resolved_path,
                img_width=img_width if img_width is not None else render_cfg.img_width,
                img_height=img_height if img_height is not None else render_cfg.img_height,
                colorscheme=config.openscad.colorscheme,
            )
    except Exception:
        LOGGER.exception("Render failed for %s", scad_file)
        raise
    return {
        "image_path": str(result.image_path),
        "command": result.command,
    }
