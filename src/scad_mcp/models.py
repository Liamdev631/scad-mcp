"""Shared data models for OpenSCAD tools."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class OpenScadInfo:
    """OpenSCAD installation details."""
    found: bool
    path: Path | None
    version: str | None
    details: str


@dataclass(frozen=True)
class RenderRequest:
    """Input parameters for a render request."""
    scad_file: Path
    projection: str
    fov: float
    angles: Sequence[str]
    output_dir: Path


@dataclass(frozen=True)
class RenderResult:
    """Result of a render operation."""
    image_path: Path
    command: list[str]
