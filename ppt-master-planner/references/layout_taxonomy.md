<!-- Based on hugohe3/ppt-master (MIT) — https://github.com/hugohe3/ppt-master -->
<!-- Planning/review workflow inspired by thePlannerIvan/planners-ppt-hell (AGPL-3.0) -->
# Layout Taxonomy

## Layout Types

### 1. cover
- **Purpose**: Opening slide, first impression
- **Structure**: Centered title + subtitle + metadata footer
- **Background**: Dark (`#1a1a2e`) with accent border
- **Elements**: Main title (64px), subtitle (32px), presenter, date, event badge
- **Variants**: 
  - `cover.full` — full-bleed background image
  - `cover.minimal` — title only on white
  - `cover.brand` — with logo lockup

### 2. toc
- **Purpose**: Table of contents / agenda
- **Structure**: Dark left panel (480px) + numbered item list on right
- **Background**: Dark left panel, white right panel
- **Elements**: "目录" header, TOC items with numbers
- **Variants**:
  - `toc.simple` — flat list
  - `toc.grouped` — with section headers

### 3. chapter
- **Purpose**: Section divider / chapter opener
- **Structure**: Dark title block (top) + content preview area (bottom)
- **Background**: Full dark, accent card for title
- **Elements**: Chapter number, title, subtitle, content preview area
- **Variants**:
  - `chapter.full` — with full page number
  - `chapter.minimal` — title only, image background

### 4. content
- **Purpose**: Primary slide type for information delivery
- **Structure**: 2-column layout — left content + right supporting content
- **Background**: White with colored title bar (80px)
- **Elements**: Title bar, left column (text-heavy), right column (images/data)
- **Sub-variants**:
  - `content.text` — both columns text
  - `content.data` — right column as chart/data zone
  - `content.image` — right column as image zone
  - `content.comparison` — two equal columns for A/B comparison
  - `content.timeline` — horizontal timeline across middle

### 5. ending
- **Purpose**: Closing slide, Q&A / thank you
- **Structure**: Centered, dark background with decorative circles
- **Background**: Dark (`#1a1a2e`), concentric accent circles
- **Elements**: Thank you message, closing message, contact info
- **Variants**:
  - `ending.qa` — Q&A prompt instead of thank you
  - `ending.contact` — with full contact details
  - `ending.cta` — call to action

### 6. data (special)
- **Purpose**: Data-heavy slide (inherits from content)
- **Structure**: Wider data area, reduced text
- **Background**: White with accent data visualizations
- **Use in page_plan type**: `"data"`

### 7. comparison (special)
- **Purpose**: Side-by-side comparison
- **Structure**: Two equal columns with divider
- **Use in page_plan type**: `"comparison"`

## Layout Selection Logic
- `page_plan.json` → `page_plan[i].type` maps to layout type
- Each type looks for exact match, then falls back to generic (e.g., `cover.brand` → `cover`)
- Final fallback: `content` layout

## Page Plan Metadata Schema
```json
{
  "page": 1,
  "title": "Slide Title",
  "type": "cover|toc|chapter|content|ending|data|comparison",
  "content_type": "text-heavy|visualization|image-led|mixed|data",
  "layout_hint": "centered|two-column|split",
  "key_points": ["point1", "point2"]
}
```
