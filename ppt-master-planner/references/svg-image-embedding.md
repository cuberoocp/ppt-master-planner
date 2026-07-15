# SVG Image Embedding Guide

## Methods

1. **External Reference URLs** — `<image href="https://..." />` — preferred for web-sourced images
2. **Base64 Data URIs** — `<image href="data:image/png;base64,..." />` — preferred for local/self-contained files

## Workflow

1. Image acquisition writes images to `<project>/images/` directory
2. Executor references images via `<project>/images/<filename>` in SVG
3. Finalize step converts paths to appropriate embedding format