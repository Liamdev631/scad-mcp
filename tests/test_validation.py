"""Tests for scad_mcp.validation module."""

from pathlib import Path
import pytest

from scad_mcp.validation import (
    validate_angles,
    validate_fov,
    validate_projection,
    validate_scad_file,
)

def test_validate_scad_file_requires_scad_extension(tmp_path: Path) -> None:
    """Reject non-SCAD file extensions."""
    file_path = tmp_path / "model.txt"
    file_path.write_text("cube([1,1,1]);", encoding="utf-8")
    with pytest.raises(ValueError):
        validate_scad_file(file_path)


def test_validate_scad_file_missing() -> None:
    """Raise when the SCAD file is missing."""
    with pytest.raises(FileNotFoundError):
        validate_scad_file(Path("missing.scad"))


def test_validate_projection() -> None:
    """Accept known projections and reject invalid ones."""
    validate_projection("perspective")
    validate_projection("orthographic")
    with pytest.raises(ValueError):
        validate_projection("wide")


def test_validate_fov() -> None:
    """Validate field of view bounds."""
    validate_fov(45.0)
    with pytest.raises(ValueError):
        validate_fov(0.0)





def test_validate_angles_single() -> None:
    """Accept a single view angle."""
    assert validate_angles(["top"]) == ["top"]


def test_validate_angles_dual() -> None:
    """Accept two compatible view angles."""
    assert validate_angles(["top", "left"]) == ["top", "left"]


def test_validate_angles_opposites() -> None:
    """Reject opposing angles."""
    with pytest.raises(ValueError):
        validate_angles(["left", "right"])


def test_validate_angles_duplicates() -> None:
    """Reject duplicate angles."""
    with pytest.raises(ValueError):
        validate_angles(["top", "top"])


def test_validate_angles_invalid() -> None:
    """Reject unsupported angles."""
    with pytest.raises(ValueError):
        validate_angles(["diagonal"])


def test_validate_angles_too_many() -> None:
    """Reject more than two angles."""
    with pytest.raises(ValueError):
        validate_angles(["top", "left", "front"])


def test_validate_angles_empty() -> None:
    """Reject empty angle lists."""
    with pytest.raises(ValueError):
        validate_angles([])
