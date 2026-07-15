# Shared Standards — SVG & PPTX Constraints

## SVG Banned Features

- `<mask>` — not supported in PowerPoint DrawingML conversion
- `style` attribute — use explicit presentation attributes instead
- `<foreignObject>` — not supported
- CSS `@media` queries — not supported
- JavaScript — not supported
- External resources (except approved image URLs)

## Marker Constraints

- Only simple arrowheads on `<path>` elements
- No custom marker shapes

## Clip-Path Rules

- Use basic `<clipPath>` with simple shapes only
- No nested clip-paths

## PPT Compatibility

- All text must be real text elements (not paths)
- Use standard web fonts or specify fallback fonts
- Images must be embedded as base64 or external reference
- Maximum SVG viewport: 1920x1080 (16:9) or 1024x768 (4:3)