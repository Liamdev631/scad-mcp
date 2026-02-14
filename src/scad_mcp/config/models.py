"""Configuration model definitions for scad-mcp."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"


@dataclass(frozen=True)
class OpenScadConfig:
    """OpenSCAD configuration."""
    path: Path | None = None
    colorscheme: str = "Tomorrow Night"


@dataclass(frozen=True)
class RenderConfig:
    """Render defaults."""
    img_width: int = 1920
    img_height: int = 1080
    projection: str = "perspective"
    fov: float = 45.0
    output_dir: Path = Path("renders")


@dataclass(frozen=True)
class ServerConfig:
    """Server metadata configuration."""
    name: str = "scad-mcp"


@dataclass(frozen=True)
class AppConfig:
    """Combined application configuration."""
    server: ServerConfig = ServerConfig()
    logging: LoggingConfig = LoggingConfig()
    openscad: OpenScadConfig = OpenScadConfig()
    render: RenderConfig = RenderConfig()
