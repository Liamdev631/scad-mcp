"""Load application configuration and environment overrides."""

from __future__ import annotations

from pathlib import Path
import os

from scad_mcp.config.models import AppConfig, OpenScadConfig


def load_config(openscad_path: str | None = None) -> AppConfig:
    """Load application configuration.

    Args:
        openscad_path: Optional path to OpenSCAD executable from CLI args.

    Returns:
        Parsed application configuration.
    """
    openscad_cfg = OpenScadConfig(
        path=Path(openscad_path) if openscad_path else None,
    )
    
    return AppConfig(openscad=openscad_cfg)
