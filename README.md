# scad-mcp

Python MCP server for OpenSCAD rendering and model utilities.

## Requirements

- Python 3.12
- OpenSCAD installed and available in PATH or configured via --openscad-path argument
- uv for dependency management

## Setup

Activate the local conda environment:

```bash
conda activate C:\Users\liamb\Projects\scad-mcp\.conda
uv sync
```

On Linux:

```bash
conda activate /path/to/scad-mcp/.conda
uv sync
```

## Run the MCP server

```bash
uv run scad-mcp
```

Set the environment to use production config:

```bash
$env:SCAD_MCP_ENV="prod"
uv run scad-mcp
```

On Linux:

```bash
export SCAD_MCP_ENV=prod
uv run scad-mcp
```

## Tools

### OpenSCAD installation checker

Inputs: none

Outputs:

- found: bool
- path: str | None
- version: str | None
- details: str

### SCAD model renderer

Inputs:

- scad_file: path to .scad file
- projection: perspective or orthographic
- fov: 1 to 120
- angles: one, two, or three of top, bottom, front, back, left, right
- output_dir: optional output folder

The renderer names output files using:

```
<stem>_<projection>_fov<FOV>_<angle1[-angle2][-angle3]>.png
```

Example usage:

```bash
mcp-call scad_model_renderer --scad-file examples/ferris_wheel.scad --angles front left top --output-dir examples
```

This command renders the ferris wheel model from a viewpoint that is the average of the front, left, and top camera angles. This is useful for getting an isometric-like perspective that shows depth and detail from multiple sides.

| Render | Command |
| --- | --- |
| ![Ferris wheel top-front-right](examples/ferris_wheel_perspective_fov45_top-front-right.png) | `mcp-call scad_model_renderer --scad-file examples/ferris_wheel.scad --angles top front right --output-dir examples` |

## Configuration
 
Config files live in config/dev.toml and config/prod.toml.
 
To specify the OpenSCAD executable path, pass it as a command-line argument when running the server:
 
```bash
uv run scad-mcp --openscad-path "C:\Program Files\OpenSCAD\openscad.exe"
```
 
For MCP configuration (e.g., in `.trae/mcp.json`):
 
```json
{
  "mcpServers": {
    "scad-mcp": {
      "command": "uv",
      "args": [
        "run",
        "scad-mcp",
        "--openscad-path",
        "C:\\Program Files\\OpenSCAD\\openscad.exe"
      ]
    }
  }
}
```

## Testing

```bash
uv run pytest
```

Integration tests will skip if OpenSCAD is not installed.
