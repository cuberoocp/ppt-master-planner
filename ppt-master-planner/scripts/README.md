# Scripts

This directory contains the Python scripts used in the PPT Master Planner pipeline.

## Source Conversion

| Script | Purpose |
|--------|---------|
| `source_to_md/pdf_to_md.py` | PDF to Markdown |
| `source_to_md/doc_to_md.py` | DOCX/ODT/HTML to Markdown |
| `source_to_md/excel_to_md.py` | Excel to Markdown |
| `source_to_md/ppt_to_md.py` | PPTX to Markdown |
| `source_to_md/web_to_md.py` | Web page to Markdown |

## Planning

| Script | Purpose |
|--------|---------|
| `planner.py` | Planning stage — content strategy, outline, page plan |

## Management

| Script | Purpose |
|--------|---------|
| `project_manager.py` | Project init, source import, validation |

## Image & SVG

| Script | Purpose |
|--------|---------|
| `analyze_images.py` | Image analysis |
| `image_gen.py` | AI image generation |
| `svg_quality_checker.py` | SVG validation |
| `latex_render.py` | LaTeX formula rendering |

## Post-processing

| Script | Purpose |
|--------|---------|
| `total_md_split.py` | Speaker notes extraction |
| `finalize_svg.py` | SVG cleanup and embedding |
| `svg_to_pptx.py` | PPTX export |
| `update_spec.py` | spec_lock.md propagation |