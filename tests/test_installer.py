"""Installer and configuration loader tests."""

from pathlib import Path

import pytest

import os
from unittest.mock import patch

from scad_mcp.config.loader import load_config
from scad_mcp.openscad import installer
from scad_mcp.openscad.installer import get_openscad_info


@pytest.mark.asyncio
async def test_get_openscad_info_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure missing OpenSCAD returns a not found result."""
    monkeypatch.setattr(installer, "find_openscad_executable", lambda _: None)
    info = await get_openscad_info(Path("missing/openscad.exe"))
    assert info.found is False


@pytest.mark.asyncio
async def test_get_openscad_info_found(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Validate version parsing when OpenSCAD is discovered."""
    openscad_path = tmp_path / "openscad.exe"
    openscad_path.write_text("binary", encoding="utf-8")

    async def fake_run(command: list[str]) -> tuple[int, str, str]:
        return 0, "OpenSCAD 2024.01", ""

    monkeypatch.setattr(installer, "find_openscad_executable", lambda _: openscad_path)
    monkeypatch.setattr(installer, "run_openscad", fake_run)

    info = await get_openscad_info(None)
    assert info.found is True
    assert info.path == openscad_path
    assert info.version == "OpenSCAD 2024.01"


def test_load_config_uses_env(tmp_path: Path) -> None:
    """Confirm OPENSCAD_PATH from env var is loaded into config."""
    with patch.dict(os.environ, {"OPENSCAD_PATH": r"C:\OpenSCAD\openscad.exe"}):
        config = load_config()
        assert config.openscad.path is not None
        assert str(config.openscad.path).endswith("openscad.exe") 
