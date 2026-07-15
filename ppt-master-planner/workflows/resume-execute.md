# Resume Execute Workflow

> Phase B resumption — when the user opens a fresh chat and says "继续生成 projects/<x>" or similar.

## Process

1. Validate project directory exists with completed design_spec.md and spec_lock.md
2. Verify images directory and any existing SVG pages
3. Determine next ungenerated page from the page plan
4. Resume sequential SVG generation from that page
5. Continue through post-processing and export