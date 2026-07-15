# SVG Layout Rules

## Prohibited Features
The following features are **not supported** in SVG→PPTX conversion and will be rejected by `validate_svg_layout.py`:

1. `<filter>` — cannot be converted to PPTX
2. `<clipPath>` — only basic rectangle clips supported
3. `<mask>` — not supported, use opacity instead
4. `<use>` — resolve manually or duplicate elements
5. `<defs>` containing gradients/patterns — use solid fill only
6. `<animate>` / `<animateTransform>` — PPTX has no animation-to-PPTX path
7. `<foreignObject>` — cannot embed HTML in PPTX shapes
8. CSS `@import` or external stylesheets — inline styles only
9. JavaScript / `<script>` tags — stripped
10. `<a>` (links) — stripped, map to PPTX hyperlinks separately

## Text Safety Rules

| Constraint | Limit |
|-----------|-------|
| Max characters per text element | 500 |
| Max font size | 96px |
| Min font size | 10px |
| Max font families per SVG | 3 |
| No text overflow | text must fit within parent rect bounds |

## Canvas Boundaries

- All elements must be within `[0, 0, 1920, 1080]`
- Elements exceeding bounds by >5px are flagged
- Text elements beyond the right edge (x + estimated_width > 1920) are flagged
- Overlapping interactive zones (buttons/links) not checked

## Fill & Stroke Rules

- **Fill**: solid colors only (`#RRGGBB` or `#RRGGBBAA`). Named colors only in a whitelist (black, white, red, etc.)
- **Stroke**: solid colors, width 0.5–10px, `stroke-linecap="butt"` or `"round"`
- **Opacity**: element-level `opacity` or `fill-opacity` supported; group opacity not supported
- **Transform**: `translate(x, y)` and `rotate(deg, cx, cy)` supported; `scale()` not supported

## Validation Severity
- `error`: blocks processing (prohibited feature)
- `warning`: logged but proceed (text overflow, minor bound exceed)
- `info`: informational (used font, element count)

## Text Measurement Heuristic
`estimated_width = font_size × len(text) × 0.6` (Chinese: ~1.0, ASCII: ~0.6, mixed: weighted)

Used by `estimate_layout_capacity.py` and `validate_svg_layout.py`.
