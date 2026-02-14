"""Validation helpers for render inputs."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


VALID_ANGLES = {"top", "bottom", "front", "back", "left", "right"}
OPPOSITES = {
    ("top", "bottom"),
    ("front", "back"),
    ("left", "right"),
}


def validate_scad_file(scad_file: Path) -> None:
    """Validate that the path exists and is a .scad file.

    Args:
        scad_file: Path to the SCAD file.

    Raises:
        ValueError: When file extension is not .scad.
        FileNotFoundError: When the file does not exist.
    """
    if scad_file.suffix.lower() != ".scad":
        raise ValueError("Input file must have .scad extension.")
    if not scad_file.exists():
        raise FileNotFoundError(f"SCAD file not found: {scad_file}")


def validate_projection(projection: str) -> None:
    """Validate projection name.

    Args:
        projection: Projection name to validate.

    Raises:
        ValueError: When projection is not supported.
    """
    if projection not in {"perspective", "orthographic"}:
        raise ValueError("Projection must be perspective or orthographic.")


def validate_fov(fov: float) -> None:
    """Validate field of view range.

    Args:
        fov: Field of view in degrees.

    Raises:
        ValueError: When the field of view is out of range.
    """
    if not 1.0 <= fov <= 120.0:
        raise ValueError("FOV must be between 1 and 120 degrees.")

def validate_angles(angles: Iterable[str]) -> list[str]:
    """Validate view angles and return normalized list.

    Args:
        angles: Iterable of view angle strings.

    Returns:
        Normalized list of angles.

    Raises:
        ValueError: When angles are missing, invalid, or incompatible.
    """
    normalized = [angle.lower() for angle in angles]
    if not normalized:
        raise ValueError("At least one angle must be provided.")
    if len(normalized) > 3:
        raise ValueError("Provide at most three angles.")
    if any(angle not in VALID_ANGLES for angle in normalized):
        raise ValueError("Angles must be one of top, bottom, front, back, left, right.")
    if len(set(normalized)) != len(normalized):
        raise ValueError("Duplicate angles are not allowed.")
    if len(normalized) >= 2:
        for pair in OPPOSITES:
            if set(pair).issubset(set(normalized)):
                raise ValueError(f"Opposite angles {pair} cannot be combined.")
    return normalized
