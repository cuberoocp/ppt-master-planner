# Template Fill Workflow

> Run when the user provides an existing `.pptx` template and wants to reuse its design with new content. This route edits PPTX directly and must not enter the SVG generation pipeline.

## When to Use

- User provides `.pptx` file + text content
- User says "fill this back into the template", "reuse this deck's design"

## Process

1. Analyze the provided PPTX template (slide layouts, color theme, fonts)
2. Map new content to slide layouts
3. Fill content preserving original design
4. Export modified PPTX