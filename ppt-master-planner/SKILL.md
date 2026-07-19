---
name: ppt-master-planner
description: >
  AI-driven PPT generation system with integrated planning stage. Converts source
  documents (PDF/DOCX/URL/Markdown) into high-quality PPTX through 6-state pipeline:
  approach → content → plan → draft → review → export. Use when user asks to
  "create PPT", "make presentation", "生成PPT", "做PPT", "制作演示文稿",
  or mentions "ppt-master-planner".
---

# PPT Master Planner Skill

> AI-driven presentation generation system with integrated project planning stage. Merges execution pipeline with explicit planning workflows for content strategy, outline design, and page-level planning before SVG generation.

**Core Pipeline**: `SETUP(意图+源+基本信息) → CONTENT(分析+规划+内容打磨) → PLAN(设计规范+配色) → DRAFT(SVG+校验+自检循环) → REVIEW(审阅+批准) → EXPORT(SVG→PPTX)`

**State Machine**: `approach → content → plan → draft → review → export`

> [!CAUTION]
> ## Global Execution Discipline (MANDATORY)
>
> 1. **SERIAL EXECUTION** — Steps MUST be executed in order; the output of each step is the input for the next.
> 2. **BLOCKING = HARD STOP** — Steps marked BLOCKING require a full stop; the AI MUST wait for an explicit user response before proceeding.
> 3. **NO CROSS-PHASE BUNDLING** — Cross-phase bundling is FORBIDDEN.
> 4. **GATE BEFORE ENTRY** — Each Step has prerequisites (GATE) listed at the top; these MUST be verified before starting that Step.
> 5. **NO SPECULATIVE EXECUTION** — "Pre-preparing" content for subsequent Steps is FORBIDDEN.
> 6. **NO SUB-AGENT SVG GENERATION** — Executor SVG generation must be completed by the main agent end-to-end.
> 7. **SEQUENTIAL PAGE GENERATION ONLY** — SVG pages MUST be generated sequentially page by page, batch by batch.
> 8. **SPEC_LOCK RE-READ PER PAGE** — Before generating each SVG page, Executor MUST re-read `spec_lock.md`. All values MUST come from this file — no values from memory or invented on the fly.
> 9. **SVG MUST BE HAND-WRITTEN** — Every SVG page is written by the main agent directly. Script-generated SVGs are FORBIDDEN.
> 10. **GATE BEFORE PROGRESS** — Before state transitions, `pipeline_gate.py <project_dir> <gate>` MUST pass.
> 11. **PRESERVE SOURCE IMAGES** — When converting web/PDF/DOCX sources to Markdown, ALL original images MUST be downloaded and saved to `source/images/`, referenced with local paths in the output Markdown. Images are reference materials — never discard or omit them.
> 12. **ACCENT COLOR USAGE ON LIGHT PAGES** — See `references/style_system.md#accent-color-usage-rule-critical` for quantified limits. Accent color MUST NOT be used for large backgrounds on light pages.

> [!IMPORTANT]
> ## Language & Communication Rule
>
> - **Response language**: match the user's input and source materials. Explicit user override takes precedence.
> - **Template format**: `design_spec.md` MUST follow its original English template structure. Content values may be in the user's language.

> [!IMPORTANT]
> ## Compatibility With Generic Coding Skills
>
> - `ppt-master-planner` is a repository-specific workflow, not a general application scaffold.
> - On conflict with a generic coding skill, follow this skill unless the user explicitly says otherwise.

## Pipeline Scripts

| Script | Purpose |
|--------|---------|
| `scripts/pptflow.py` | State machine controller — manages `current.state`, `project.json` |
| `scripts/pipeline_gate.py` | Phase gate — validates prerequisites for state transitions |
| `scripts/init_project.py` | Project initialization — creates project directory structure |
| `scripts/planner.py` | Planning stage — content strategy, outline, page plan |
| `scripts/validate_project_contracts.py` | Validates content/layout/manifest contract files |
| `scripts/validate_svg_layout.py` | SVG quality check — prohibited features, text safety, canvas bounds |
| `scripts/native_svg_to_ppt.py` | SVG→PPTX (native python-pptx shapes: rect/circle/text/image/path) |
| `scripts/estimate_layout_capacity.py` | Text capacity estimation for layouts |
| `scripts/render_svg_png.py` | SVG→PNG preview rendering |
| `scripts/generate_layout_html.py` | Layout direction review HTML |
| `scripts/generate_review_html.py` | Visual review HTML (batch review) |
| `scripts/review_server.py` | HTTP review server with one-time-password auth |
| `scripts/source_to_md/pdf_to_md.py` | PDF to Markdown |
| `scripts/source_to_md/doc_to_md.py` | Documents to Markdown |
| `scripts/source_to_md/excel_to_md.py` | Excel workbooks to Markdown |
| `scripts/source_to_md/ppt_to_md.py` | PowerPoint to Markdown |
| `scripts/source_to_md/web_to_md.py` | Web page to Markdown |

## Template Index

| Index | Path | Purpose |
|-------|------|---------|
| Layout templates | `templates/layouts/layouts_index.json` | Available page layout templates |
| Brand presets | `templates/brands/brands_index.json` | Available brand identity presets |
| Design spec template | `templates/design_spec_reference.md` | design_spec.md template |
| Spec lock template | `templates/spec_lock_reference.md` | spec_lock.md template |

## Standalone Workflows

| Workflow | Path | Purpose |
|----------|------|---------|
| `planner` | `workflows/planner.md` | Planning phase — content strategy, outline, page-by-page plan |
| `topic-research` | `workflows/topic-research.md` | Pre-pipeline — gather web sources when only a topic is supplied |
| `content-polish` | `workflows/content-polish.md` | Content structure定型, language compression, 5-dimension scoring |
| `visual-review` | `workflows/visual-review.md` | Per-page visual quality check |
| `live-preview` | `workflows/live-preview.md` | Browser-based live SVG preview |
| `template-fill-pptx` | `workflows/template-fill-pptx.md` | Fill content into existing .pptx template |

## Main Pipeline Steps

### Step 0: Setup — Intent, Sources & Base Info Collection

**GATE**: User has expressed intent to create a presentation.

0.1 Clarify user intent — topic, audience, tone, desired length.

0.2 Collect source materials (PDF, DOCX, URL, existing PPTX, or direct topic).

0.3 If only a topic is given, run `workflows/topic-research.md` to gather web sources.

0.4 Convert sources to Markdown:
```bash
python scripts/source_to_md/pdf_to_md.py <file.pdf>
python scripts/source_to_md/doc_to_md.py <file.docx>
python scripts/source_to_md/web_to_md.py <URL>
```

0.5 Run gate:
```bash
python scripts/pipeline_gate.py <project_dir> approach-ready
```

0.6 **Collect project base info (BLOCKING)** — gather and record the project's base configuration that all later steps depend on. At minimum:
  - Canvas format & dimensions: e.g. `ppt169` (1920×1080), `story` (1080×1920), `square` (1080×1080), or a custom width×height. Stored as `canvas_width` / `canvas_height` in the project's pipeline config (see `init_project.py`).
  - Target audience, delivery context, language, tone.
  - **All subsequent size-dependent steps (SVG bounds, font scaling, render viewport, PNG clip, PPTX slide size, whitespace rules) MUST read from this collected canvas size — never hardcode 1920×1080.**
  - Recorded via `init_project.py` (Step 2.1): `--format ppt169|ppt43|xhs|story|square|custom`, with `--width/--height` for custom size, plus `--audience/--delivery-context/--language/--tone`. Values land in `_internal/00_project/flow_state.json` (`pipeline_config.canvas_width/height`, `project_info.*`).

### Step 1: Content — Source Analysis & Planning

**GATE**: Source materials assembled as Markdown.

1.1 Analyze source content — identify sections, key messages, data points, tone.

1.2 Run the planner:
```bash
python scripts/planner.py <source_md> --output <project_dir>
```

1.3 Review generated artifacts:
- `content_strategy.md` — target audience, core message, narrative structure
- `outline.md` — slide-by-slide title hierarchy
- `page_plan.json` — page-by-page purpose, type, layout hint

1.4 **Content Polish** — optimize per-slide content quality:
    1.4.1 Run `workflows/content-polish.md`:
      - **Pass 1: 结构定型** — assign structure type (总分总/总分/并列/递进/对比) per page
      - **Pass 2: 语言压缩** — long sentence → short sentence → short phrase
      - **Pass 3: 五维评分** — score 逻辑清晰度/信息密度/内容焦点/口语化/感染力; iterate until all ≥ 4
    1.4.2 Write report to `planning/content_polish_report.md`
    1.4.3 Update `_internal/01_content/page_content.json` with polished content
     1.4.4 Repeat Pass 2-3 iteratively until user approves (BLOCKING)

     1.4.5 **Image source decision** — review all images in source materials against page content:
       - Determine which images carry semantic value relevant to page content (e.g. diagrams, screenshots)
       - Skip irrelevant images (avatars, QR codes, navigation icons, footer decorations, copyright badges)
       - Write `images` array per page in `page_content.json` with src, placement, alt

1.5 Present the plan to the user for confirmation (BLOCKING).

1.6 Run gate:
```bash
python scripts/pipeline_gate.py <project_dir> content-ready
```

### Step 2: Plan — Design Specification

**GATE**: Planning artifacts confirmed by user.

2.1 Initialize project — this also records the base info collected in Step 0.6:
```bash
python scripts/init_project.py <project_dir> \
  --format ppt169|ppt43|xhs|story|square|custom \
  --width <W> --height <H>            # only with --format custom
  --audience <text> --delivery-context <text> --language <lang> --tone <text>
```
> 源材料统一放在项目根的 `source/`，`init_project.py` 不再复制源文件（已移除 `--source` 逻辑）。Canvas size and project info are written to `_internal/00_project/flow_state.json` and consumed by all later size-dependent steps.

2.2 **Color research + auto-style application**:  
   2.2.1 Search web for 3 professional color palette options from reputable sources (Coolors, Adobe Color, PresentationGO, DesignBombs, or known brand palettes). Extract verified hex codes.  
   2.2.2 **Image color compatibility check** — if source images exist, extract dominant colors per `references/style_system.md#image-color-compatibility-palette-selection`. Classify images as cool/warm/neutral. Discard palettes whose 辅色 clashes with image temperature.  
   2.2.3 Apply **Tone-Boldness filter** (`references/style_system.md#tone-boldness-principle`): discard palettes mismatched to content energy level.  
   2.2.5 **Auto-apply style rules** from `references/style_system.md`:
     - Icon style → per `#icon-style-selection-automatic` (decision priority: tone → image compatibility → page type → density)
     - Font selection → per `#font-selection-automatic` (default: Microsoft YaHei + Arial)
     - Data display form → per `#data-display-selection-automatic` (per-page, by data point count)
   Write selected values to `planning/style_decisions.json`.

2.3 **Layout strategy auto-generation**:  
   Map each page's structure type → layout_variant using rules from `references/style_system.md#layout-variant-mapping`:
   - `总分` → `content-single` (thesis + details, ≤4 items) or `content-list` (>4 items)
   - `总分总` → `content-three`
   - `并列` → `content-cards` (items with title+desc) or `content-table` (plain text items)
   - `递进` → `content-flow`
   - `对比` → `content-split`
   Write to `_internal/01_layout_plan/layout_plan.json`.

2.4 **Strategist** produces `design_spec.md` and `spec_lock.md` with:
- Canvas format & dimensions — read from the collected base info (Step 0.6), NOT hardcoded to 1920×1080.
- Visual theme (palette from research + auto-applied style values)
- Layout strategy (from layout_plan.json)
- Icon, font, data display specifications (from style_decisions.json / style_system.md rules)
- Image requirements
- Content outline (from page_content.json)
- Tech constraints (SVG rules)

2.5 **Color palette confirmation (BLOCKING)** — generate an HTML palette preview (per `references/style_system.md#palette-preview-requirement`) with all options displayed as color swatches alongside embedded source images. Open in browser, present options, wait for user choice.

2.6 Validate contracts:
```bash
python scripts/validate_project_contracts.py <project_dir>
```

2.7 Run gate:
```bash
python scripts/pipeline_gate.py <project_dir> strategist-ready
```

### Step 3: Draft — SVG Generation (Batch)

**GATE**: Design spec confirmed, contracts valid.

3.1 Divide pages into batches. Batch size is not a page-count default — total page count is determined dynamically by the PLAN phase from the actual source content, never preset to a fixed number (e.g. 30). Choose a reasonable batch size (commonly 3 pages/batch) once the real page count is known.

3.2 For each batch, generate SVG pages sequentially (page by page, hand-written SVG). Before validation, run the design-quality self-check (`references/style_system.md#design-quality-rules-critical--pre-review-self-check`); every SVG MUST pass before proceeding.

3.3 Run the DRAFT command sequence (order is fixed, do not reorder):
```bash
# 1. gate before draft entry
python scripts/pipeline_gate.py <project_dir> batch-svg-ready --batch <N>
# 2. render PNG preview (ONCE per batch) — viewport/clip read from collected canvas size
python scripts/render_svg_png.py <project_dir>
# 3. static layout validation → _internal/04_validation/validation_summary.json
python scripts/validate_svg_layout.py <project_dir>/_internal/02_svg_source \
  --manifest <project_dir>/_internal/00_project/page_manifest.json --batch <N> \
  --output <project_dir>/_internal/04_validation/validation_summary.json
# 4. gate: requires PNG present + self-review present + validation passed
python scripts/pipeline_gate.py <project_dir> preview-ready --batch <N>
```
PNG output: `_internal/03_png_preview/slide_XX.png` (dimensions = collected canvas size).

3.4 **Self-check → revise → self-check loop**: the model reviews the rendered PNG and writes `self_review.json` / `integrated_review.json` under `_internal/04_validation/`. If the validator reports error or blocker-class warning (e.g. `TEXT_OVERFLOW_MAJOR`, `FOOTER_ZONE_INVASION`), return to the SVG, fix it, then re-render PNG, re-validate, and rewrite the review JSON — repeat until no blocking errors remain before the `preview-ready` gate. Loop discipline: non-blocking warnings allow only one high-value revision pass; if the same issue type stays unresolved for two consecutive passes, escalate to PLAN / user confirmation — never silently change layout, shrink font, or split pages in the SVG stage.

### Step 4: Review — Visual Quality & Batch Approval

**GATE**: All SVG pages generated, all batches passed `preview-ready`.

4.1 Generate visual review HTML (uses the already-rendered PNGs — does NOT re-render):
```bash
python scripts/generate_review_html.py <project_dir> --batch <N>
```

4.2 (Optional) Generate layout direction review:
```bash
python scripts/generate_layout_html.py <project_dir>
```

4.3 Start review server; user views PNGs in browser and submits feedback (BLOCKING — user must approve before export):
```bash
python scripts/review_server.py <project_dir>
```
Feedback is written to `_internal/05_review/feedback.json` and archived per batch.

4.4 Run gate (sets `visual_approved` / `export_allowed` in manifest):
```bash
python scripts/pipeline_gate.py <project_dir> visual-approved --batch <N>
```

### Step 5: Export — SVG→PPTX Conversion

**GATE**: All pages approved by user (`visual-approved` set `export_allowed` for every batch).

5.1 Convert all SVGs to PPTX (native python-pptx shapes; slide size derived from each SVG's viewBox, matching the collected canvas size — does NOT read PNG, does NOT re-render):
```bash
export SMART_SVG_EXPORT_APPROVED_BY_PPTFLOW=1
python scripts/native_svg_to_ppt.py <project_dir> -o <project_dir>/../dist/<name>.pptx
```

5.2 Deliver final PPTX to user.

> PNG previews are produced only once, in Step 3 (DRAFT). Export never re-renders PNG.

## Core Directories

- `SKILL.md` — main workflow authority
- `references/` — role definitions, style system, SVG rules, layout taxonomy, quality checklist
- `scripts/` — runnable tool scripts
- `templates/` — layout templates (SVG), spec reference templates, brand presets
- `workflows/` — standalone workflow files
- `agents/` — agent configuration files
- `layouts/` — SVG layout templates (cover, toc, chapter, content, ending)

## State Transition Summary

```
approach ──gate──→ content ──gate──→ plan ──gate──→ draft ──gate──→ review ──gate──→ export
    │                  │                │               │                │                │
    └── source_md      └── planning     └── spec_lock   └── all SVGs    └── approved    └── PPTX
```
