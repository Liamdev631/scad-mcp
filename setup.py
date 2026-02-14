"""Setuptools configuration for scad-mcp."""

from setuptools import find_packages, setup


setup(
    name="scad-mcp",
    version="0.1.0",
    description="MCP server for OpenSCAD rendering and manipulation",
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.12",
)
