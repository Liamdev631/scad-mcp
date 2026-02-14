# scad-mcp

Python MCP server for OpenSCAD rendering and model utilities.

## Requirements

- Python 3.12
- OpenSCAD installed and available in PATH or configured via OPENSCAD_PATH
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
- angles: one or two of top, bottom, front, back, left, right
- output_dir: optional output folder

The renderer names output files using:

```
<stem>_<projection>_fov<FOV>_<angle1[-angle2]>.png
```

## Configuration

Config files live in config/dev.toml and config/prod.toml. Use OPENSCAD_PATH in .env to specify the OpenSCAD executable when it is not in PATH.

Example .env entry on Windows:

```
OPENSCAD_PATH="C:\Program Files\OpenSCAD\openscad.exe"
```

## Testing

```bash
uv run pytest
```

Integration tests will skip if OpenSCAD is not installed.
