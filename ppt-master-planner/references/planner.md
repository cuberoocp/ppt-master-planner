# Planner Role

The Planner is the new phase added by ppt-master-planner. It runs before the Strategist and produces structured planning artifacts.

## Input

- Source materials (markdown, PDF text, user topic description)
- User goals and audience information

## Outputs

### Content Strategy Document
- Target audience analysis
- Key message / core narrative
- Tone and voice guidelines
- Call to action

### Outline
- Slide-by-slide title hierarchy
- Section grouping
- Flow structure (problem → solution → evidence → action)

### Page Plan
Each page entry includes:
- **Page title** — slide title
- **Page type** — cover, toc, chapter, content, ending, full-bleed, data, comparison, timeline
- **Content type** — text-heavy, visualization, image-led, mixed, quote, data
- **Layout hint** — suggested layout template or structural notes
- **Key points** — 2-5 bullet points the page should communicate
- **Speaker notes hint** — what the presenter should say

## Output Format

```
projects/<name>/plan/
├── content_strategy.md
├── outline.md
└── page_plan.json
```