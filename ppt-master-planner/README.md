# PPT Master Planner Skill

> AI-driven presentation generation system with integrated planning phase. Converts source documents into natively editable PPTX through a 6-state pipeline.

**Version**: 0.1.0

**Core Pipeline**: `Source → Planning → Content Polish → Strategist → DRAFT(batch) → REVIEW → EXPORT`

**State Machine**: `approach → content → plan → draft → review → export`

## Prerequisites

- Python 3.10+
- Install dependencies: `pip install -r requirements.txt`

## Usage

After installing the skill, tell your AI agent:

```
Use ppt-master-planner to turn this document into an editable PPTX with planning.
Start from content planning, then show me the outline before generating SVG pages.
```

The agent will guide you through the 6-step pipeline:

| Step | State | Description |
|------|-------|-------------|
| 0 | approach | Clarify intent, collect source materials |
| 1 | content | Source analysis, content strategy, outline |
| 2 | plan | Design spec, color palette, layout strategy |
| 3 | draft | SVG page generation (batch) |
| 4 | review | Visual quality check & approval |
| 5 | export | SVG→PPTX conversion |

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `scripts/pptflow.py` | State machine controller |
| `scripts/pipeline_gate.py` | Phase gate validation |
| `scripts/init_project.py` | Project initialization |
| `scripts/planner.py` | Content strategy & outline |
| `scripts/native_svg_to_ppt.py` | SVG→PPTX conversion |
| `scripts/validate_svg_layout.py` | SVG quality check |
| `scripts/review_server.py` | Visual review HTTP server |
| `scripts/source_to_md/*.py` | Source format converters |

## Pipeline Overview

```
Source → Planning → Content Polish → Strategist → DRAFT(batch) → REVIEW → EXPORT
```

See [`ppt-master-planner/SKILL.md`](ppt-master-planner/SKILL.md) for the full workflow.

## Acknowledgments

This skill is built upon and inspired by:

- **[hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)** — SVG-to-PPTX execution pipeline
- **[thePlannerIvan/planners-ppt-hell](https://github.com/thePlannerIvan/planners-ppt-hell)** — Planning phase workflows