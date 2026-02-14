# scad-mcp
![CI](https://github.com/liamdev631/scad-mcp/actions/workflows/ci.yml/badge.svg)

Python MCP server for OpenSCAD design and rendering utilities.

## Requirements

- Python 3.12
- OpenSCAD installed and available in PATH or configured via --openscad-path argument
- uv for dependency management

## Run the MCP server


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

```json
{
  "angles": [
    "top",
    "front",
    "right"
  ],
  "scad_file": "\**\scad-mcp\examples\ferris_wheel.scad",
  "projection": "perspective",
  "fov": 45,
  "img_height": 1080,
  "img_width": 1920,
  "output_dir": "\**\scad-mcp\examples"
}
```

This command renders the ferris wheel model from a viewpoint that is the average of the front, left, and top camera angles. This is useful for getting an isometric-like perspective that shows depth and detail from multiple sides.

![Ferris wheel top-front-right](examples/ferris_wheel_perspective_fov45_top-front-right.png)

### SCAD model converter

Inputs:

- scad_file: path to .scad file
- output_format: target format (e.g. "stl", "3mf", "amf"). Optional if output_path is provided.
- output_path: explicit output path. If provided, output_format is ignored.

Outputs:

- output_path: path to the generated file
- command: command used to generate the file

## Testing

```bash
uv run pytest
```

Integration tests will skip if OpenSCAD is not installed.

## AI Assistant Configuration

To ensure optimal performance when using this MCP server with AI coding assistants (like Trae or Cursor), it is highly recommended to configure them with specific operational rules. These rules instruct the AI to follow an iterative "generate-render-verify" loop and to handle OpenSCAD's single-threaded nature correctly.

### Recommended Rule

**Usage:**
- **Trae:** Create a file at `.trae/rules/scad_mcp.md` and paste the content below.
- **Cursor:** Append the content below to your `.cursorrules` file.

```markdown
---
alwaysApply: true
---
Iteratively use the scad_mcp server tools to generate .scad files. Use the rendering tools to render the .scad files from appropriate angles and reference them to verify the correctness of the generated .scad files. Loop between editing and rendering the .scad files until the desired output is achieved. Use comments and a highly-modular code structure to make the code easy to understand and maintain. 

CRITICAL: Include sanity checks and assertions (using `assert()`) at the beginning of the file to validate parameters and ensure the correctness of the generated model (e.g., checking for collisions, invalid dimensions, or geometric constraints). This is MANDATORY.

Always use the OpenSCAD language reference manual at https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language before continuing with edits or designs. ALways include comments or notes about major architectural decisions, especially early in the design process. Always use more than one rendering to confirm results.

WARNING: OpenSCAD rendering is single-threaded and CPU-bound. This process may take a significant amount of time (minutes) to complete for complex models. Requests are processed sequentially to prevent resource exhaustion. NEVER assume the request has timed out; ALWAYS wait for the result. DO NOT retry the command if it seems slow.
```

## ToDo:

* Add multi-color support for 3D printing
* Add support for other 3D file formats (e.g., OBJ, STL)
