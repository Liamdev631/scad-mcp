"""Load application configuration and environment overrides."""

from __future__ import annotations

from pathlib import Path
import os

from scad_mcp.config.models import AppConfig, OpenScadConfig


def load_config() -> AppConfig:
    """Load application configuration from environment variables.

    Returns:
        Parsed application configuration.
    """
    env_data = dict(os.environ)

    openscad_path = env_data.get("OPENSCAD_PATH", "")
    
    # We can override other defaults here if needed using env_data
    # For now, we rely on the dataclass defaults for most settings
    
    openscad_cfg = OpenScadConfig(
        path=Path(openscad_path) if openscad_path else None,
        # Default colorscheme is "Tomorrow Night" from models.py
    )
    
    return AppConfig(openscad=openscad_cfg)
