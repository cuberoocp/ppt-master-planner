# AGENTS.md

This file is the project entry point for general AI agents.

**You MUST read [`SKILL.md`](SKILL.md) before any PPT generation task or repo modification.**

## Project Overview

PPT Master Planner is an AI-driven presentation generation system with an integrated planning phase. Multi-role collaboration (Planner → Strategist → Image_Generator → Executor) converts source documents (PDF/DOCX/URL/Markdown) into natively editable PPTX with real PowerPoint shapes (DrawingML).

**Core Pipeline**: `Source Document → Planning Phase → Create Project → [Template] → Strategist → [Image_Generator] → Executor → Quality Check → Post-processing → Export PPTX`

## Required Conventions

- Repo-wide style rules in [`docs/rules/`](docs/rules/).
- Markdown files under `workflows/`, `references/`, and `docs/` are single-language per directory.

## Compatibility Boundary

- This repository is a workflow/skill package, not an app or service scaffold.
- On conflict with a generic coding skill, prioritize [`ppt-master-planner/SKILL.md`](ppt-master-planner/SKILL.md).

## Core Directories

- `SKILL.md` — main workflow authority
- `references/` — role definitions and technical specs
- `scripts/` — tool scripts
- `templates/` — layout, icon, chart, brand templates
- `workflows/` — standalone workflow files
- `docs/` — user-facing documentation
- `examples/` — example projects
- `projects/` — user project workspace