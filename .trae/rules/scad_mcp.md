---
alwaysApply: true
---
Iteratively use the scad_mcp server tools to generate .scad files. Use the rendering tools to render the .scad files from appropriate angles and reference them to verify the correctness of the generated .scad files. Loop between editing and rendering the .scad files until the desired output is achieved. Use comments and a highly-modular code structure to make the code easy to understand and maintain. 

CRITICAL: Include sanity checks and assertions (using `assert()`) at the beginning of the file to validate parameters and ensure the correctness of the generated model (e.g., checking for collisions, invalid dimensions, or geometric constraints). This is MANDATORY.

Always use the OpenSCAD language reference manual at https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language before continuing with edits or designs. ALways include comments or notes about major architectural decisions, especially early in the design process. Always use more than one rendering to confirm results.

WARNING: OpenSCAD rendering is single-threaded and CPU-bound. This process may take a significant amount of time (minutes) to complete for complex models. Requests are processed sequentially to prevent resource exhaustion. NEVER assume the request has timed out; ALWAYS wait for the result. DO NOT retry the command if it seems slow.
