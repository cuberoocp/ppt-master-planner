# PPT Master Planner Skill

> AI-driven presentation generation system with integrated planning phase. Converts source documents into natively editable PPTX through a 6-state pipeline.

**Version**: 0.1.0

**Core Pipeline**: `SETUP(意图+源+基本信息) → CONTENT(分析+规划+内容打磨) → PLAN(设计规范+配色) → DRAFT(SVG+校验+自检循环) → REVIEW(审阅+批准) → EXPORT(SVG→PPTX)`

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
| 0 | approach | Clarify intent, collect sources, **collect base info (canvas size, audience, language, tone)** |
| 1 | content | Source analysis, planning, **content polish** (结构定型 → 语言压缩 → 五维评分), image decision |
| 2 | plan | Design spec, **color palette research + confirmation**, layout strategy, `spec_lock.md` |
| 3 | draft | SVG generation (batch); render PNG once → validate → **self-check → revise → self-check loop** → `preview-ready` gate |
| 4 | review | Visual review HTML + review server; user approval → `visual-approved` gate |
| 5 | export | SVG→PPTX conversion (native shapes, slide size from SVG viewBox) |

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
SETUP → CONTENT → PLAN → DRAFT → REVIEW → EXPORT
```

## Key Conventions

- **Canvas size is collected once** at Step 0.6 (via `init_project.py --format/--width/--height`) and stored in `_internal/00_project/flow_state.json`. Every later step that depends on size — SVG bounds validation, PNG render viewport, PPTX slide size — reads this value. **Never hardcode 1920×1080.**
- **PNG preview is rendered exactly once**, in DRAFT (Step 3). REVIEW reuses those PNGs; EXPORT never re-renders.
- **Self-check loop**: in DRAFT, if validation reports an error or blocker warning, fix the SVG, re-render, re-validate, and re-review until clean before the `preview-ready` gate.
- **Dependencies**: `python-pptx`, `pypdf`, `python-docx`, `openpyxl`, `requests`, `beautifulsoup4`, `Pillow`, `lxml`. PNG preview is optional and needs `playwright` + Chromium: `pip install playwright && playwright install chromium`.

See [`SKILL.md`](SKILL.md) for the full workflow and gate commands.

## Acknowledgments

This skill is built upon and inspired by:

- **[hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)** — SVG-to-PPTX execution pipeline
- **[thePlannerIvan/planners-ppt-hell](https://github.com/thePlannerIvan/planners-ppt-hell)** — Planning phase workflows