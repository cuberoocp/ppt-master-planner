# CLAUDE.md

This file is the project entry point for Claude Code.

**You MUST read [`ppt-master-planner/SKILL.md`](ppt-master-planner/SKILL.md) before any PPT generation task or repo modification.**

## Project Overview

PPT Master Planner is an AI-driven presentation generation system with an integrated planning phase. Multi-role collaboration (Planner → Strategist → Image_Generator → Executor) converts source documents (PDF/DOCX/URL/Markdown) into natively editable PPTX with real PowerPoint shapes (DrawingML).

**Core Pipeline**: `Source Document → Planning Phase → Create Project → [Template] → Strategist → [Image_Generator] → Executor → Quality Check → Post-processing → Export PPTX`

> Topic-only requests with no source material: run the standalone [`topic-research`](ppt-master-planner/workflows/topic-research.md) workflow first.
>
> Content planning: when the user wants structured planning before generation, run the standalone [`planner`](ppt-master-planner/workflows/planner.md) workflow.
>
> Template fill: run the standalone [`template-fill-pptx`](ppt-master-planner/workflows/template-fill-pptx.md) workflow.
>
> Phase B resumption: run the standalone [`resume-execute`](ppt-master-planner/workflows/resume-execute.md) workflow.
>
> Visual self-check: run the standalone [`visual-review`](ppt-master-planner/workflows/visual-review.md) workflow.

## Execution Requirements

- Technical SVG/PPT constraints: [`ppt-master-planner/references/shared-standards.md`](ppt-master-planner/references/shared-standards.md)
- Canvas choices: [`ppt-master-planner/references/canvas-formats.md`](ppt-master-planner/references/canvas-formats.md)

## Command Quick Reference

```bash
# Source content conversion
python3 ppt-master-planner/scripts/source_to_md/pdf_to_md.py <PDF_file>
python3 ppt-master-planner/scripts/source_to_md/doc_to_md.py <DOCX_file>
python3 ppt-master-planner/scripts/source_to_md/excel_to_md.py <XLSX_file>
python3 ppt-master-planner/scripts/source_to_md/ppt_to_md.py <PPTX_file>
python3 ppt-master-planner/scripts/source_to_md/web_to_md.py <URL>

# Planning
python3 ppt-master-planner/scripts/planner.py <source_md> --output <project_path>/plan

# Project management
python3 ppt-master-planner/scripts/project_manager.py init <project_name> --format ppt169
python3 ppt-master-planner/scripts/project_manager.py import-sources <project_path> <source_files...> --move

# Post-processing pipeline
python3 ppt-master-planner/scripts/total_md_split.py <project_path>
python3 ppt-master-planner/scripts/finalize_svg.py <project_path>
python3 ppt-master-planner/scripts/svg_to_pptx.py <project_path>
```

## Core Directories

- `ppt-master-planner/SKILL.md` — main workflow authority
- `ppt-master-planner/references/` — role definitions and technical specs
- `ppt-master-planner/scripts/` — tool scripts
- `ppt-master-planner/templates/` — layout, chart, icon, brand templates
- `ppt-master-planner/workflows/` — standalone workflow files