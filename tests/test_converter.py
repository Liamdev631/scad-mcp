"""Tests for model converter."""

from pathlib import Path
import pytest
from scad_mcp.models import ConvertRequest
from scad_mcp.openscad import converter

@pytest.mark.asyncio
async def test_convert_scad_happy_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Convert a SCAD file using a stubbed OpenSCAD command."""
    scad_file = tmp_path / "model.scad"
    scad_file.write_text("cube([1,1,1]);", encoding="utf-8")
    output_file = tmp_path / "model.stl"
    
    request = ConvertRequest(
        scad_file=scad_file,
        output_file=output_file,
    )

    async def fake_run_openscad(command: list[str]) -> tuple[int, str, str]:
        # command should be [openscad, -o, output_file, scad_file]
        # Simulate creating the output file
        Path(command[2]).write_text("stl data", encoding="utf-8")
        return 0, "ok", ""

    monkeypatch.setattr(converter, "run_openscad", fake_run_openscad)

    result = await converter.convert_scad(
        request=request,
        openscad_path=Path("openscad"),
    )
    
    assert result.output_path == output_file
    assert result.output_path.exists()
    assert result.output_path.read_text(encoding="utf-8") == "stl data"

@pytest.mark.asyncio
async def test_convert_scad_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test conversion failure."""
    scad_file = tmp_path / "model.scad"
    scad_file.write_text("cube([1,1,1]);", encoding="utf-8")
    output_file = tmp_path / "model.stl"
    
    request = ConvertRequest(
        scad_file=scad_file,
        output_file=output_file,
    )

    async def fake_run_openscad(command: list[str]) -> tuple[int, str, str]:
        return 1, "", "Syntax error"

    monkeypatch.setattr(converter, "run_openscad", fake_run_openscad)

    with pytest.raises(RuntimeError, match="OpenSCAD conversion failed"):
        await converter.convert_scad(
            request=request,
            openscad_path=Path("openscad"),
        )
