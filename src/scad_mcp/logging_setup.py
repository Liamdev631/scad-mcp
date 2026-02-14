"""Logging configuration for the scad-mcp service."""

import logging


def configure_logging(level: str) -> None:
    """Configure the root logger with the specified level and a standard format.

    Args:
        level: Logging level as a string (e.g., 'info', 'debug', 'warning').
    """
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
