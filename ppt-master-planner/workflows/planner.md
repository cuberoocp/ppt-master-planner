# Planner Workflow — Content Strategy, Outline & Page Plan

> Run this workflow BEFORE Step 1 of SKILL.md when the user wants structured planning before generation.

## Purpose

Analyze source materials and produce three planning artifacts:
1. **Content Strategy** — audience, key message, tone, narrative structure
2. **Outline** — slide-by-slide title hierarchy
3. **Page Plan** — each page's purpose, content type, layout hint, and key points

## Input

- Source materials (markdown text, PDF content, or user topic description)
- User-provided goals, audience, and constraints

## Process

### 1. Analyze Sources
Review all provided materials and identify:
- Core argument / narrative arc
- Logical section breaks
- Data points and evidence requiring visualization
- Audience knowledge level and expectations

### 2. Draft Content Strategy
Write to `content_strategy.md`:
- Target audience profile
- Primary message
- Secondary messages
- Tone and voice
- Call to action

### 3. Draft Outline
Write to `outline.md`:
- Section headings with slide counts
- Per-slide titles in sequence
- Flow annotations (e.g., "introduces problem", "presents data", "calls to action")

### 4. Draft Page Plan
Write to `page_plan.json`:
For each slide:
```json
{
  "page": 1,
  "title": "Slide Title",
  "type": "cover|toc|chapter|content|ending|full-bleed|data|comparison|timeline",
  "content_type": "text-heavy|visualization|image-led|mixed|quote|data",
  "layout_hint": "centered|two-column|three-column|grid|full-bleed",
  "key_points": ["point 1", "point 2"],
  "notes_hint": "what the presenter should cover"
}
```

### 5. Present for Confirmation (BLOCKING)
Show the user the strategy, outline, and page plan. Wait for approval or revision before proceeding.

## Output Directory

```
projects/<name>/plan/
├── content_strategy.md
├── outline.md
└── page_plan.json
```

The page plan feeds into the Strategist's Eight Confirmations and the Executor's sequential SVG generation.