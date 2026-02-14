"""Renderer tests for OpenSCAD integration."""

from pathlib import Path

import pytest

from scad_mcp.config.models import AppConfig, LoggingConfig, OpenScadConfig, RenderConfig, ServerConfig
from scad_mcp.models import RenderRequest
from scad_mcp.openscad import renderer
from scad_mcp.tools import model_renderer
from scad_mcp.tools.model_renderer import render_model


@pytest.mark.asyncio
async def test_render_scad_happy_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Render a SCAD file using a stubbed OpenSCAD command."""
    scad_file = tmp_path / "demo.scad"
    scad_file.write_text("cube([1,1,1]);", encoding="utf-8")
    output_dir = tmp_path / "renders"
    request = RenderRequest(
        scad_file=scad_file,
        projection="perspective",
        fov=45.0,
        angles=["front"],
        output_dir=output_dir,
    )

    async def fake_run_openscad(command: list[str]) -> tuple[int, str, str]:
        Path(command[2]).write_text("image", encoding="utf-8")
        return 0, "ok", ""

    monkeypatch.setattr(renderer, "run_openscad", fake_run_openscad)

    result = await renderer.render_scad(
        request=request,
        openscad_path=Path("openscad"),
        img_width=800,
        img_height=600,
    )
    assert result.image_path.exists()


def test_output_name_and_camera() -> None:
    """Verify output naming and camera string formatting."""
    name = renderer.output_name(Path("demo.scad"), "perspective", 45.0, ["front"])
    assert name == "demo_perspective_fov45_front.png"
    # For top view with vector camera: eye=(0,0,dist), center=(0,0,0)
    camera = renderer.build_camera(["top"], 45.0)
    # Expected format: eye_x,eye_y,eye_z,center_x,center_y,center_z
    # eye_z should be 155.0 (200.0 - 45.0)
    assert camera == "0.0,0.0,155.0,0.0,0.0,0.0"


@pytest.mark.asyncio
async def test_render_model_tool(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure the MCP tool wrapper returns a rendered image path."""
    config = AppConfig(
        server=ServerConfig(name="scad-mcp"),
        logging=LoggingConfig(level="INFO"),
        openscad=OpenScadConfig(path=Path("openscad")),
        render=RenderConfig(
            img_width=300,
            img_height=200,
            projection="perspective",
            fov=45.0,
            output_dir=tmp_path / "renders",
        ),
    )

    async def fake_render_scad(**kwargs: object) -> renderer.RenderResult:
        output_path = config.render.output_dir / "demo.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("image", encoding="utf-8")
        return renderer.RenderResult(image_path=output_path, command=["openscad"])

    monkeypatch.setattr(model_renderer, "render_scad", fake_render_scad)
    monkeypatch.setattr(model_renderer, "find_openscad_executable", lambda _: Path("openscad"))

    result = await render_model(
        config=config,
        scad_file=str(tmp_path / "model.scad"),
        projection=None,
        fov=None,
        angles=["front"],
        output_dir=None,
    )
    assert result["image_path"].endswith("demo.png")
