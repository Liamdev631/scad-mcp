"""Integration tests for real OpenSCAD rendering."""

from pathlib import Path

import pytest

from scad_mcp.openscad.installer import find_openscad_executable
from scad_mcp.openscad.renderer import render_scad
from scad_mcp.models import RenderRequest


@pytest.mark.asyncio
async def test_openscad_render_integration(tmp_path: Path) -> None:
    """Render a SCAD file with the installed OpenSCAD binary."""
    openscad = find_openscad_executable(None)
    if not openscad:
        pytest.skip("OpenSCAD not installed.")
    scad_file = tmp_path / "integration.scad"
    scad_file.write_text("cube([2,2,2]);", encoding="utf-8")
    output_dir = tmp_path / "renders"
    request = RenderRequest(
        scad_file=scad_file,
        projection="perspective",
        fov=45.0,
        angles=["front"],
        output_dir=output_dir,
    )
    result = await render_scad(
        request=request,
        openscad_path=openscad,
        img_width=400,
        img_height=300,
        colorscheme="",
    )
    assert result.image_path.exists()
