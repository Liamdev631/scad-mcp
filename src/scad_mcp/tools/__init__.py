"""Tool entry points for MCP usage."""

from scad_mcp.tools.installation_checker import check_openscad
from scad_mcp.tools.model_renderer import render_model

__all__ = ["check_openscad", "render_model"]
