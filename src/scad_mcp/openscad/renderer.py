"""Render SCAD files via OpenSCAD CLI."""

from __future__ import annotations

import logging
from pathlib import Path

from scad_mcp.models import RenderRequest, RenderResult
from scad_mcp.openscad.cli import run_openscad
from scad_mcp.validation import validate_angles, validate_fov, validate_projection, validate_scad_file

LOGGER = logging.getLogger("scad_mcp.openscad.renderer")

ANGLE_VECTORS = {
    "top": (0.0, 0.0, 1.0),
    "bottom": (0.0, 0.0, -1.0),
    "front": (0.0, -1.0, 0.0),
    "back": (0.0, 1.0, 0.0),
    "left": (-1.0, 0.0, 0.0),
    "right": (1.0, 0.0, 0.0),
}

def build_camera(angles: list[str], fov: float) -> str:
    """Build the OpenSCAD camera parameter string using vector camera.

    Args:
        angles: One or two normalized view angles. Choices are "front", "back", "left", "right", "top", "bottom".
        fov: Field of view in degrees.

    Returns:
        Camera parameter string for OpenSCAD in format:
        eye_x,eye_y,eye_z,center_x,center_y,center_z
    """
    # Calculate target distance
    dist = max(30.0, 200.0 - fov)
    
    # Calculate eye position based on angles
    # Start with origin
    eye_x, eye_y, eye_z = 0.0, 0.0, 0.0
    
    # Sum up vectors for multiple angles
    for angle in angles:
        vec = ANGLE_VECTORS[angle]
        eye_x += vec[0]
        eye_y += vec[1]
        eye_z += vec[2]
    
    # Normalize and scale by distance
    length = (eye_x**2 + eye_y**2 + eye_z**2)**0.5
    if length > 0:
        eye_x = (eye_x / length) * dist
        eye_y = (eye_y / length) * dist
        eye_z = (eye_z / length) * dist
    else:
        # Default to front view if length is 0 (e.g. conflicting angles)
        eye_y = -dist

    # Center is always origin (0,0,0) for now
    center_x, center_y, center_z = 0.0, 0.0, 0.0
    
    return f"{eye_x},{eye_y},{eye_z},{center_x},{center_y},{center_z}"


def output_name(scad_file: Path, projection: str, fov: float, angles: list[str]) -> str:
    """Generate a render output filename.

    Args:
        scad_file: Source SCAD file path.
        projection: Perspective or orthographic.
        fov: Field of view in degrees.
        angles: One or two normalized view angles.

    Returns:
        Output filename for the rendered image.
    """
    angle_part = "-".join(angles)
    return f"{scad_file.stem}_{projection}_fov{int(fov)}_{angle_part}.png"


async def render_scad(
    request: RenderRequest,
    openscad_path: Path,
    img_width: int,
    img_height: int,
    colorscheme: str,
) -> RenderResult:
    """Render a SCAD file to an image using OpenSCAD.

    Args:
        request: Render request parameters.
        openscad_path: Path to the OpenSCAD executable.
        img_width: Output image width in pixels.
        img_height: Output image height in pixels.
        colorscheme: OpenSCAD colorscheme name.

    Returns:
        RenderResult with image path and executed command.

    Raises:
        FileNotFoundError: When the SCAD file does not exist.
        ValueError: When projection, fov, or angles are invalid.
        RuntimeError: When the OpenSCAD command fails.
    """
    validate_scad_file(request.scad_file)
    validate_projection(request.projection)
    validate_fov(request.fov)
    angles = validate_angles(request.angles)

    request.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = request.output_dir / output_name(request.scad_file, request.projection, request.fov, angles)
    camera = build_camera(angles, request.fov)
    command = [
        str(openscad_path),
        "-o",
        str(output_path),
        str(request.scad_file),
        "--render",
        f"--imgsize={img_width},{img_height}",
        f"--projection={request.projection}",
        f"--camera={camera}",
        "--backend=Manifold",
        "--autocenter",
        "--viewall",
    ]
    if colorscheme:
        command.append(f"--colorscheme={colorscheme}")
    LOGGER.info("Rendering %s to %s", request.scad_file, output_path)
    exit_code, stdout, stderr = await run_openscad(command)
    if exit_code != 0:
        message = stderr.strip() or stdout.strip() or "OpenSCAD render failed."
        LOGGER.error("Render failed: %s", message)
        raise RuntimeError(message)
    return RenderResult(image_path=output_path, command=command)
