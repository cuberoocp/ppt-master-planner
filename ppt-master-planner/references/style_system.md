# Style System Reference

## Canvas
- **Resolution**: 1920×1080 (16:9)
- **Margins**: 80px (all sides)
- **Safe area**: 1760×920 (centered)

## Color Palette

### Palette Evaluation Against Image Colors

Before selecting a palette, extract dominant colors from any embedded source images and evaluate compatibility:

| Image Group | Dominant Colors | Temperature | Compatible Palette Direction |
|-------------|----------------|-------------|------------------------------|
| Diagrams/Flows | `#ffffff` + `#ececff` (lavender-blue) | **Cool** | Cool-based palettes (冰蓝/靛蓝/深蓝). 辅色 should be cool-neutral (`#f0f4ff` or `#e3f2fd`). Avoid warm 辅色 (beige, cream, warm white). |

If multiple images have consistent temperature, that confirms the direction. If no images exist, skip this check.

### Hierarchy (60-30-10 Rule)
The 60-30-10 proportion applies per-page. **主色（30%）** defines what color the deck is; **辅色（60%）** is the canvas; **点缀色（10%）** provides focus.

| 60-30-10 | Our Role | Coverage | Hex | Usage |
|----------|----------|----------|-----|-------|
| **Dominant 60%** | **辅色（底色）** | 60% | `#ffffff` | Light page background (pure white canvas). On dark pages → `#1a237e` replaces this role |
| **Secondary 30%** | **主色（色系色）** | 30% | `#1a237e` | Defines the deck's identity. Dark bg; light page title bar + left strip + thesis cards + section headers |
| **Accent 10%** | **点缀色** | 10% | `#ff5252` | Lines, badges, highlight text, small markers, CTAs |
| — | **辅色-卡片** | on light pages | `#f5f5f5` | Detail card backgrounds within the 60% Dominant zone |
| — | **辅色-深色版** | on dark pages | `#283552` | Dark page card backgrounds (within the 60% Dominant zone) |
| — | Border | decorative | `#e0e0e0` | Subtle borders between cards/sections |
| — | TextPrimary | text | `#333333` | Body text on light bg |
| — | TextDark | text | `#ffffff` | Body text on dark bg / dark cards |
| — | TextMuted | text | `#9fa8da` | Secondary/caption text (matches cover bottom-info range) |
| — | TextDim | text | `#7986cb` | Tertiary/metadata |

### Color Scheme Catalog（模板驱动 — 全 PPT 统一一套方案）

配色方案必须是整份 deck **全局统一**的，绝不可按 page_type 切换。
以下提炼自木友圈 2025 模板的 **3 种色彩关系模式**，每模式可派生无限具体方案。
选方案时：先定模式 → 再定品牌色 → 全 deck 锁定。

---

#### 模式 A：冷主暖点 (Cool Primary + Warm Accent)

**公式** — ac1=200-260° 色相（蓝/靛/青，30%主色），ac2=0-40°（橙/红，10%点缀），ac3-6=中性填充

| 实例 | ac1 主色 | ac2 点缀 | ac3 | ac4 | ac5 | ac6 |
|------|---------|---------|-----|-----|-----|-----|
| Corporate Default | `#4472C4` | `#ED7D31` | `#A5A5A5` | `#FFC000` | `#5B9BD5` | `#70AD47` |
| 标题栏样式-浅色 | `#1689F4` | `#16C0F4` | `#1BCFE4` | `#FFC000` | `#5B9BD5` | `#70AD47` |

**派生：** ac1 替换为品牌蓝色，ac2 替换为品牌暖色。品牌色越深，点缀色应越艳。ac3-6 一般不动。

---

#### 模式 B：全冷/全暖单色系 (All-Cool / All-Warm Monochrome)

**公式** — 6 个 accent 同色系 ±40° 色相内，通过明度/饱和度区分层次。无对位色。

| 实例 | 家族 | ac1 | ac2 | ac3 | ac4 | ac5 | ac6 |
|------|------|-----|-----|-----|-----|-----|-----|
| Monochrome Cool（图文排版） | 蓝-青 | `#486FDF` | `#518CFB` | `#0CBDB9` | `#48CDA0` | `#5B9BD5` | `#70AD47` |
| Deep Professional（封面页） | 蓝 | `#008DCC` | `#0071A4` | `#A5A5A5` | `#FFC000` | `#5B9BD5` | `#70AD47` |
| Data Contrast（数据图表） | 蓝 | `#005DAE` | `#5FC4E8` | `#A5A5A5` | `#FFC000` | `#5B9BD5` | `#70AD47` |

> Deep Professional / Data Contrast 的 ac3-6 沿用了 Office 默认填充（灰/金/浅蓝/绿），
> 完整单色方案应将 ac3-6 也约束在色系内，如 Monochrome Cool 那样。

**派生（选目标色相 H）：**
- ac1 = H ±10°, S50-70%, L40-60%
- ac2 = H ±15°, S40-60%, L55-75%
- ac3 = H ±30°, S50-70%, L50-70%
- ac4-6 = 同色系低饱和变体或中性灰

可做暖色系版本：H=0-40°（橙/红/珊瑚），结构不变。

---

#### 模式 C：黑底 + 跨色环霓虹 (Dark + Polychrome Neon)

**公式** — dk1≈#000，ac1/2/3 跨越色环 120°+，高饱和（S≥70%），无中性填充。

| 实例 | dk1 | ac1 | ac2 | ac3 | ac4 | ac5 | ac6 |
|------|-----|-----|-----|-----|-----|-----|-----|
| 流程&时间轴 | `#000000` | `#00CEFE` 青 | `#0552EB` 蓝 | `#D427DD` 紫 | `#03066C` | `#15D2FD` | `#1A63EF` |

**派生：** dk1=#000 或 #0a0a12，选 3 色相约 120° 相隔（如 180/300/60，或 200/320/80）。
ac1=L70-80%，ac2=L30-40%，ac3=L50-60%。ac4-6 可保留或调整为更低亮度。

---

### 模式选择流程

1. **底色判断：** 浅底 → A 或 B；深底（黑）→ C
2. **是否要暖色：** 需要（品牌红/橙）→ **A**；不需要 → **B**
3. **若选 B（单色系）：** 选色相家族（蓝/青/紫/绿/红/橙），按派生规则生成 6 级
4. **锁定：** 选好后全 deck 锁定，不可按 page_type 切换

### Tone-Boldness 映射

| Tone | 推荐模式 | 说明 |
|------|---------|------|
| Professional / 中性 | **A** — 冷主暖点 | 蓝色专业感 + 暖色点睛，最稳妥 |
| Modern / 简洁 | **B** — 全冷单色系 | 单色家族天然干净 |
| Formal / 严肃 | **B** 变体 — 低饱和 | ac1-6 全部降饱和度，保留同色系结构 |
| Academic / 数据 | **B** 变体 — 高对比 | ac1 极深 + ac2 极浅，同色系 |
| Creative / 活力 | **C** — 黑底霓虹 | 高饱和跨色环，视觉冲击最强 |

### AI PM Skills 项目配色

**模式 A（冷主暖点）**，ac1=`#1a237e`，ac2=`#ff5252`：

| 60-30-10 | Hex | 说明 |
|----------|-----|------|
| 辅色 60% | `#ffffff` | 浅底色画布 |
| 主色 30% | `#1a237e` | 模式 A ac1，title bar/竖条/主色卡片 |
| 点缀色 10% | `#ff5252` | 模式 A ac2，badge/线/数字 |
| 辅色-卡片 | `#f5f5f5` | 卡片底 |
| 辅色-深色版 | `#283552` | 深色页卡片底 |
| 边框 | `#e0e0e0` | 卡片/区隔线 |
| 文字主色 | `#333333` | 浅底正文 |
| 文字浅色 | `#ffffff` | 深底文字 |
| 文字次要 | `#9fa8da` | 封面底部/二级 |
| 文字暗淡 | `#7986cb` | 三级/元数据 |

现有色彩规则（60-30-10、Functional Zones、点缀色 Usage Rule）不变——它们定义「怎么用」，本目录定义「用什么色值」。

### Functional Zones per Page Type

**Light content page (60-30-10 allocation):**
```
┌─────────────────────────────────────────────────┐
│  ████████████ 主色 title bar (part of 30%)       │  10px high
│  █  │  辅色/底色 60% (white #ffffff)            │
│  主  │  ┌── 辅色-卡片 #f5f5f5 ──┐               │
│  色  │  │  detail / info       │               │
│  竖  │  └──────────────────────┘               │
│  条  │  ┌── 主色 thesis card #1a237e ──┐       │
│  30% │  │  white text                 │       │  30%
│      │  └──────────────────────────────┘       │
│      │  ┌── 点缀色 badge #ff5252 ──┐           │  10%
│      │  └──────────────────────────┘           │
└─────────────────────────────────────────────────┘
```

**Dark page (cover/chapter/ending):**
- 辅色(60%) = `#1a237e` (the background IS the dark canvas)
- 主色(30%) = `#1a237e` same color, distinguished by content hierarchy
- 辅色-深色版(within 60%) = `#283552` for cards/blocks
- 点缀色(10%) = `#ff5252` for lines, numbers, badges

### 主色 Presence Rules (CRITICAL)
On every light-background content page, the 主色 (#1a237e) MUST cover ~30% of the visible area:
1. **Top title bar** — full-width bar, 12px height, at top of safe area
2. **Left vertical strip** — 12px wide bar, full height of safe area, at left edge. Applies ONLY to light-background content pages — do NOT add this strip to full-canvas dark pages (cover, ending, chapter dividers).
3. **Thesis/key card** — at least one content block with `#1a237e` background + `#ffffff` text
These three elements together achieve ~30% 主色 footprint. For pages with naturally more dark elements (e.g. content-list with dark headers), the left strip can be reduced to 8px.

## Typography

Size values are in SVG px at 144 DPI (1920×1080 canvas on 13.33"×7.5" slide). 1pt = 2px.

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Main Title | Microsoft YaHei | 64px | Bold |
| Slide Title | Microsoft YaHei | 42-56px | Bold |
| Subtitle | Microsoft YaHei | 32-36px | Regular |
| Body | Microsoft YaHei | 28px | Regular |
| Card Body | Microsoft YaHei | 24px | Regular |
| Caption | Arial | 20px | Regular |
| Numbering | Arial | 16px | Regular |
| Accent Text | Microsoft YaHei | 24px | Semibold |
| Footnote | Arial | 16px | Regular |

📊 Body text at 28px (14pt) is confirmed by 2294 occurrences in 木友圈 2025 analysis. 32px (16pt) is the second most common with 1790 occurrences — use 32px for short body text on low-density slides, 28px for multi-line body text on dense slides. Avoid mixing both on the same page.

## Layout Grid

All measurements in SVG px at 144 DPI (1920×1080 canvas on 13.33"×7.5" slide). 1" = 144px.

- **Margins**: 96px (0.67") on all sides. 📊 Derived from 木友圈 templates where 0.7" (101px) is the most common left margin. Our previous 80px was too tight.
- **Safe area**: 1728×888 (centered). Left=96, Top=96, Right=1824, Bottom=984.
- **Column gutter**: 96px (0.67") between columns. 📊 木友圈 2025 templates (843 slides) show actual column gaps of 0.8-1.0" (115-144px) after filtering out intra-card spacing (0.2-0.3"). Our previous 40px gutter was far too narrow; 80px was still tight.
- **2-column**: left 816px + gutter 96px + right 816px = 1728px
- **3-column**: 3× 512px + 2× gutter 96px = 1728px (perfect fit)
- **4-column**: 4× 384px + 3× gutter 96px = 1824px — exceeds safe area by 96px. Instead use 4× 352px + 3× 96px = 1696px (32px slack). Better: avoid 4-column layout.
- **Single**: centered (cover, ending)
- **Title bar**: 96px at top (content slides), matching the top margin
- **Page numbers**: lower-right corner, at y=936 (48px above bottom margin)
- **8pt Grid**: all element x, y, width, height values MUST be multiples of 8px (96=12×8, 816=102×8, 512=64×8, 384=48×8). The 8pt grid is a MINIMUM standard — 16pt grid is preferred where content allows.
- **Margin verification**: outermost content starts at x=96, y=96; rightmost content ≤ x=1824.

## Design Patterns (Living Rules — Updated by Proven Examples)

These patterns are extracted from successful iterations and are MEANT TO BE CHALLENGED. If a new design produces a clearly better result while violating a pattern, the pattern gets updated — not the other way around.

Patterns marked with 📊 are **derived from analysis of 11 professional PPTX samples** (1655 slides covering 科技风/学术风/医疗风/商业路演/中国风/产品介绍/企业介绍/总结汇报/毕业答辩/求职竞聘/营销策划). These are empirical patterns, not theoretical preferences.

### How Patterns Evolve
1. A new design is proposed and reviewed
2. If it wins (user confirms it's better), the patterns are updated to reflect the new winning approach
3. Patterns are written as "what worked in prior confirmed designs", not "the only correct way"
4. When two designs both work well but use different approaches, both are documented as alternatives

### Universal Patterns (All Pages)
1. **Font size hierarchy** — the dominant element on the page should be ≥2× the smallest text size. 📊 木友圈 843-slide analysis confirms: body 14pt(28px) → heading bold 20pt(40px) → title 24-28pt(48-56px). If the smallest text is 20px (caption), titles should be ≥40px. The hierarchy MUST span at least 2× between the smallest and largest text on the page.
2. **One focal technique per page** — pick one visual anchor: a gradient band, OR a decorative shape, OR an accent line. Using multiple competing techniques reduces clarity.
3. **Margin consistency** — all text blocks on the same page should share a consistent left edge within each column. Mixing margins weakens the grid. 📊 木友圈 templates show preferred left margin of 0.7" (101px), close to our 96px standard.
4. **No orphan decorative boxes** — every visible `<rect>` must contain text or have opacity ≤ 0.5 (background-only). An empty opaque box looks like an unfinished template.
5. **8pt Grid alignment** — every element position and size SHOULD be a multiple of 8px (e.g., margins 96px=12×8, card widths 520px=65×8, heights 64px=8×8). This creates invisible structure perceived as "clean" by audiences.
6. **15-20% Whitespace** — at least 15-20% of each slide's safe area (1728×888 = 1,534,464px²) should remain empty. This means at least ~230,000–307,000px² of unfilled canvas per page. 📊 Real PPTX samples consistently leave 40-60% whitespace — our 15-20% is a MINIMUM, not a target. When in doubt, add more breathing room.
7. **Typography Scale Discipline** — use ONLY the sizes defined in the Typography section above. Never add arbitrary sizes (no 13px, 19px, 25px, etc.). The limited scale is what creates visual consistency across all 22 slides.
8. **One Message Per Slide** — if you cannot summarize the slide's point in a single sentence, split it across two slides. An extra slide costs zero; a confusing slide costs audience attention.
9. **5-Line Text Cap** — no content page should have more than 5 lines of running text in the body area. Lists, cards, and tables count separately from prose. If text exceeds 5 lines, split into two slides or use card-based layout to visually break density. 📊 With body text at 28-32px (per PPTX evidence), 5 lines = 140-160px vertical space, which naturally keeps slides from becoming text-heavy.

### Cover Page Patterns (from confirmed iteration #1)
1. **Diagonal gradient background** — `linearGradient x1=0 y1=0 x2=1 y2=1` (dark→slightly darker). This produced noticeably more depth than solid fill.
2. **Title backdrop** — a full-width gradient band (≥380px tall) behind the title, spanning left→right with decreasing opacity. This anchors the title without a hard-edged box.
3. **Title size ≥80px** — the winning iteration used 88px. Smaller titles looked underpowered against the 1080px canvas.
4. **Single accent line** — a 4-5px line under the subtitle, not beside it. The vertical bar + underline combo was tested and rejected.
5. **No English tags** — English-for-decoration was tested and rejected as template leftover.
6. **Bottom info muted** — presenter/date at bottom-left, in `#7986cb`–`#9fa8da` range. Not bright white — it's secondary info. Use 24-28px on full-canvas dark backgrounds (cover/ending); 20-24px on light pages or constrained areas. On a 1080px canvas, 20px is visually insignificant against 88px titles.
7. **Decorative circles on the right** — large-radius concentric circles (one 主色 thick stroke, one 点缀色 thin stroke) placed outside the text block, never overlapping the title area.
8. **Monochrome-with-Pop compatibility** — our confirmed palette (white bg + deep navy + coral accent) follows the "Monochrome with a Pop" trend from 2026 design references. The deck is essentially black-and-white plus one accent color. This means: never introduce a second accent color. If coral (#ff5252) marks emphasis on one page, coral marks emphasis on every page.
9. **No left vertical strip on full-canvas dark pages** — the 12px 主色 left strip (from 主色 Presence Rules) applies only to light-background content pages. On cover/ending/chapter pages with full-canvas dark backgrounds, the dark canvas itself provides the visual structure. Adding the left strip creates visual clutter by competing with the accent line, decorative circles, and title backdrop — all on the same page. ONly one focal technique per page (rule #2 in Universal Patterns) overrides.

### Content Page Patterns (from external consulting standards + PPTX sample analysis + 木友圈 template analysis)
1. **Card-based layout** — content blocks should use visible `<rect>` cards (rx="8") rather than floating text. All cards on the same page must share the same rx value.
2. **Card hierarchy** — primary card uses 主色 background, secondary cards use 主色-toned fills (`#3949ab`, `#5c6bc0`). Avoid `#f5f5f5` as default card fill — use it only for alternating table rows.
3. **30% 主色 mechanism** — 12px title bar + 12px left strip + one 主色 card (these dimensions remain unchanged, positioned relative to 96px margin).
4. **Alternating rows** for tables/metric cards — improves scanability.
5. **Z-Pattern Flow** — content should guide the eye top→left→right→down→left→right. The title is at top-left, the primary visual/card is mid-left, secondary content is mid-right, and the bottom zone (CTA or page number) is lower-right. This matches natural reading patterns.
6. **Multi-column with adequate gutter** — column width depends on count, but gutter MUST be ≥96px (0.67"). 📊 木友圈 843-slide analysis confirms real column gaps are 0.8-1.0" (115-144px). Use 2 equal columns (816px+96px+816px) for paired content, or 3 equal columns (512px+96px+512px+96px+512px) for triples. The column structure must fit within the 1728px safe area.
7. **Data + Insight Split** — when a page contains data, place the chart/visual on the left (~60% width) and the insight callout text on the right (~40% width). Use 1040px left + 96px gutter + 592px right.
8. **Card border-radius consistency** — all cards on the same page MUST use the same rx value. Mixing rx="8" with rx="12" on the same page breaks visual consistency. Preferred rx="8" for content pages.
9. **Left-aligned card text** — all text inside cards should be left-aligned, not centered. Centered text works only for the Cover and Ending title. On content pages, left alignment supports scanning.
10. **Icon row > bullet list** — replace bullet-point text with a row of 3-4 icon+label pairs (each ≤240px wide) whenever possible. Icon rows are more scannable than bullet paragraphs.
11. **Card proportion by column count** — 📊 木友圈 2025 templates (881 cards, 843 slides) show card ratios vary by layout:
    - **2-column layout** (两段内容页, 120 cards): 5.2"×4.0" (755×576px), ratio **1.3:1** — nearly square, side by side
    - **3-column layout** (三段内容页, 82 cards): 4.4"×3.4" (634×490px), ratio **1.6:1** — wider for three-across
    - **Data/metric cards** (数据图表页, 127 cards): 4.4"×4.0" (634×576px), ratio **1.3:1** — matching 2-column form factor
    - **Process/flow cards** (流程&时间轴, 67 cards): 2.9"×1.4" (418×202px), ratio **2.8:1** — wide and short for step diagrams
    Always match card ratio to layout type. Default to 1.3:1 for content pages. Avoid ratio >5:1 unless used as full-width banners.
12. **Card count per row: 2-3** — 📊 木友圈 templates predominantly use 2-card rows (for paired comparison) or 3-card rows (for triples). Single cards fill the full content width. Never use 4+ cards in a single row - the individual cards become too narrow.
13. **Top card accent band** — each content card should have a thin (6-8px) horizontal band at the top, using 点缀色 (#ff5252) for primary cards or 主色 for secondary cards. Color-coded bands help the audience distinguish card roles at a glance.

### Chapter Page Patterns (from external consulting standards + 木友圈 templates)
1. **Chapter number** prominent (≥60px, 点缀色).
2. **Title ≥56px bold**, subtitle 32px muted.
3. **Full-bleed background** — chapter pages use a full-slide background fill (dark #1a237e or light tint #f0f2f5), never card-based layout.
3. **Two-column preview** in the bottom half — showing section highlights (card or mini-list each side), not leaving it empty.
4. **Distinct background** — use a subtle dark or tinted variant of the 辅色 (e.g., `#f0f2f5`) to visually signal a section transition. On dark-themed decks, use a darker shade (e.g., `#0d0d1a`).
5. **Minimal text** — the chapter page should have ≤10 words total (number + title + subtitle). It is a breather page, not a content page.

### Introduction / Radial Layout Patterns (from AI PM Skills deck P3, confirmed iteration)
1. **Radial visual anchor** — a large filled circle (主色 `#1a237e`, r≥260) paired with a concentric ring (辅色 `#e8eaf6`, stroke=12, r≥500) creates a strong focal point. The ring MUST be placed at the SVG bottom layer (after `<rect>` background) so it sits behind all content.
2. **Center offset for content balance** — when content wraps the right side of the ring, move the ring center right of middle and below vertical center (proven: cx=520, cy=580 on 1920×1080). This counterbalances the right-side content weight.
3. **No-background cards** — cards wrapping a decorative element should strip card fill (`#f5f5f5`) and top accent band (`#ff5252` 6px). Keep only the numbered circle + text. The radial anchor provides sufficient visual structure; card backgrounds compete with it.
4. **Radial equidistance** — numbered circles must maintain equal gap from the ring's outer edge, not equal x/y coordinates. Calculate: `target_dist = ring_outer_r + gap + card_circle_r`. A 22-24px gap is proven to look balanced.
5. **Staggered wrap by ring curve** — card x-positions follow the ring's tangent curve:
   - Items above the ring's widest point → closer to center (ring narrows upward)
   - Items at the ring's widest point → pushed farthest right
   - Items below the widest point → pull back in as ring narrows
6. **dominant-baseline="central"** — use `dominant-baseline="central"` on text inside numbered circles. Set `y` = circle `cy` (no manual offset). This works reliably for SVG rendering and ensures true vertical center.
7. **Font sizing in radial layouts** — card content can use larger sizes than standard content pages (proven: card titles 30px, body 26px, list items 24px) because the decorative ring absorbs whitespace, making the page feel airy despite larger text.
8. **No card background when not needed** — the `#f5f5f5` card fill and top accent band are OPTIONAL. Only use them on content pages where cards need visual separation from each other. On pages with a strong decorative anchor (radial ring, gradient band), omit card backgrounds to reduce visual noise.

### Ending Page Patterns (from external consulting standards)
1. **Centered layout** — title centered horizontally, vertical center of safe area.
2. **Thank you text** 56-64px bold (主色 on light bg, white on dark) + English muted below (24-28px).
3. **CTA** at mid-page if content provides one (e.g., "Contact us", "Learn more").
4. **Decorative anchor** — one large decorative element (concentric circles, or a single large accent line under the title) to anchor the page. No more than one decorative element.
5. **Contact info line** — at bottom of safe area in muted text (24-28px on full-canvas dark bg, 20-24px on light), provide presenter name/email/affiliation. This distinguishes the ending from a generic "Thanks" slide.

### Data Page Patterns (from consulting standards + PPTX sample analysis)
1. **Hero Number for single metrics** — a single key number should fill ~50% of the available width, set at 72-80px bold, with a subtitle label below in 24-28px. This is more impactful than embedding the number in a sentence.
2. **Metric Cards for 2-4 KPIs** — arrange as a row of 3-4 equally-spaced cards (each ≤400px wide). Each card has a number (48-56px bold, 点缀色 or 主色) + label (20-24px regular, muted). Prefer colored card fills over gray. 📊 Real PPTX samples show metric cards with width:height ratio ~3:1 (wide card, short label area).
3. **Bar Chart for 2-5 item comparisons** — hand-drawn via `<rect>` elements with height proportional to value. Include value labels at bar ends. Keep bars ≤120px tall max to prevent visual domination.
4. **Chart + Insight pairing** — every chart/visual on a content page must have an adjacent insight callout (2-3 lines max) that states the conclusion. Never place a chart without telling the audience what to see.
5. **Consistent chart styling** — all chart bars use 主色 for primary series, 点缀色 for highlighted series, and 辅色-卡片 for the baseline. Axis labels must be 20-24px Arial (adjusted for larger body text scale). Grid lines (if any) must be `#e0e0e0` 1px.

### Data-Driven Content Page Patterns (from AI PM Skills deck P4, confirmed iteration)
1. **Full-width gradient bottom bar** — a full-bleed gradient bar (`#1a237e`→`#0d1442`, x=0~1920, height 160-200px) at the canvas bottom serves as the primary visual anchor. This is an alternative to the traditional top title bar + left strip for pages where a solid bottom anchor better frames the content. The gradient (lighter at top, darker at bottom) creates a natural visual boundary.
2. **No top bar + no left strip** — when a full-width bottom bar is used, the 12px top title bar and 12px left vertical strip can be omitted. The bottom bar alone provides sufficient 主色 presence (~25-30% of page vertical area). This follows the "one focal technique" rule — don't use both top/bottom anchors simultaneously.
3. **Card backgrounds without accent band** — `#f5f5f5` card fill with rx=8 is used WITHOUT the 6px #ff5252 top accent band. This is a middle ground between traditional cards (with accent band) and no-background cards (P3 radial pattern). The card background gives structure without competing with the page's focal point (hero numbers + bottom bar).
4. **Hero number as card focal point** — each card centers a large percentage (80px bold, 主色) at the top, followed by a 点缀色 label (26px), with left-aligned description and bullet points below. The hero number dominates the card's visual weight.
5. **Symmetrical three-column balance** — three equal-width cards (496px on 1728px safe area) centered on the page midline (x=960). Each card aligns to an 8pt grid with 96px gutters. Left/right margins from safe area edge are equal (24px each), creating perfect horizontal symmetry.
6. **Vertical card centering** — cards are vertically centered in the space between the thesis text (last text baseline) and the bottom bar (top edge). Equal gap above and below the cards creates visual equilibrium. Formula: `card_top = thesis_bottom + bar_top / 2 - card_height / 2`.
7. **Minimum font size 24px** — on this page type, all content text (including bullet points and page numbers) is ≥24px. This is larger than the 16-20px minimum on other pages, justified by the card-based layout and the need for readability in three-column format.
8. **Thesis text without decorative line** — the introductory thesis (30px) and subtitle (24px) sit as plain text without accent underline or decorative shape. The thesis is positioned at the standard left margin (x=144), with the subtitle on the same x. This keeps the focus on the hero numbers below.

### TOC / Agenda Page Patterns (from confirmed iteration #3 — AI PM Skills deck)
1. **Full-bleed gradient header band** — a tall full-width gradient band (400px, `#0d1442→#1a237e` 上深下浅) replaces the thin 12px title bar. The band spans x=0 to x=1920, creating a strong visual anchor. The vertical gradient (top darker, bottom lighter) creates a smooth transition to the white card area below.
2. **Centered title in band** — the title "5 项核心能力总览" is center-aligned (x=960) at y=218, white, 64px bold. No accent underline below the title — the band itself is the visual statement.
3. **Card-based item layout** — each TOC item uses a card (`#f5f5f5`, rx=8, 6px #ff5252 top accent band, 216px tall). Cards give each item visual weight and make the TOC feel designed rather than just a list.
4. **Filled circle numbers** — numbers sit inside filled circles (`#ff5252` fill, white text, r=26, font-size=34px bold). Filled circles pop more than outline circles and visually anchor each card.
5. **3+2 staggered row layout** — for 5 items, use 3 cards in the top row (y=448, left/center/right) + 2 cards centered in the bottom row (y=696). This breaks the rigid column grid and makes the page feel more dynamic than 2-column vertical lists.
6. **Title + description inside card** — each card contains: number circle (left), title (bold 主色, 32px), description (muted, 26px, single line). Text is left-aligned inside the card. Larger font sizes (32px titles, 26px desc) are appropriate when cards are the primary content carriers.
7. **No left vertical strip** — the 12px 主色 left strip does NOT apply to TOC pages. The gradient header band + card grid provide sufficient visual structure.
8. **Minimal decoration beyond cards** — no decorative circles, accent lines, or shapes. Background below the band is plain white. The card grid and gradient band are the only visual elements.

## SVG Text-in-Circle Centering Rule

When placing text inside a circle for numbered steps, list markers, or icons:

### Dual-Context Rule (Browser Preview + PPTX Pipeline)
SVG files in this pipeline are viewed in TWO contexts with different text rendering engines:

| Context | Renderer | `dominant-baseline` | Formula needed? |
|---------|----------|---------------------|-----------------|
| Browser (review HTML) | CSS/SVG DOM | **Supported** | No — `y=cy` works |
| PPTX export (`native_svg_to_ppt.py`) | Python script reads `y` attribute | **Ignored** | Yes — `y=cy+offset` needed |

**Hybrid approach** (use in SVG source files):
- Keep `y` = circle `cy` + (font-size × 0.35) as the canonical position — this ensures PPTX export renders correctly
- Add `dominant-baseline="central"` — this shifts the browser render to match while the PPTX pipeline ignores it and uses the `y` value directly

Example:
```svg
<circle cx="192" cy="510" r="26" fill="#ff5252"/>
<text x="192" y="522" text-anchor="middle"
      dominant-baseline="central"
      font-family="Arial" font-size="34" font-weight="bold" fill="#ffffff">1</text>
```
Here `y=522 = 510 + (34×0.35) = 522`. In browsers, `dominant-baseline="central"` overrides this and centers at cy=510. In PPTX (Python script), the script reads `y=522` and positions the text baseline there, centering correctly.

### Confirmed reference values from TOC (iteration #3)
- circle r=26, font-size=34px → `cx=192, cy=510, y=522` (cy + 34×0.35 = cy+12)
- circle r=22, font-size=28px → `cx=1030, cy=310, y=320` (cy + 28×0.35 = cy+10)

### Simple formula
`text_y = circle_cy + (font-size × 0.35)`

Always use `dominant-baseline="central"` on the `<text>` element to ensure browser preview also looks correct.

## SVG→PPTX Mapping
- `<rect>` → `shapes.add_shape(MSO_SHAPE.RECTANGLE)`
- `<circle>` → `shapes.add_shape(MSO_SHAPE.OVAL)`
- `<line>` → `shapes.add_shape(MSO_SHAPE.SINGLE_ARROW)`
- `<text>` → `text_frame.paragraphs[0]`
- `<image xlink:href="...">` → `shapes.add_picture()`

## Decorations
- Accent line: 3-4px solid `#ff5252`, placed under titles
- Circles: outline-only, 1-2px, used sparingly for visual hierarchy
- Cards: 8px border-radius rectangles with 1px border `#e0e0e0`
- **One decoration rule**: use at most ONE decorative technique per page (accent line XOR circles XOR gradient band). Using more than one dilutes the focal point.

## Palette Preview Requirement

Every color selection round MUST produce a visual preview (HTML) showing:
1. All candidate palette options side by side as color swatches with hex codes
2. The embedded source images (if any) displayed alongside, to verify visual compatibility
3. A clear recommendation marker per option

The preview is opened in the user's browser for visual comparison. User makes the final call.

## Image Color Compatibility (Palette Selection)

When source documents contain embedded images (diagrams, screenshots, illustrations) that will appear in the final PPT, the selected color palette MUST be compatible with the image's dominant colors.

### Extraction Method
1. Use Python (Pillow) to resize image to 100×100px and count pixel color frequency
2. Identify top 3-5 dominant colors (excluding pure white `#ffffff`)
3. Classify image's overall temperature: **cool** (blue/purple/cyan dominant), **warm** (red/orange/yellow/brown dominant), or **neutral** (gray/white/black dominant)

### Compatibility Rules
| Image Temperature | Recommended 辅色 (Background) | Recommended 主色 (Identity) | Avoid |
|-------------------|-------------------------------|----------------------------|-------|
| **Cool** (蓝/紫/青) | Cool neutrals: `#f0f4ff`, `#e3f2fd`, `#f5f7fa` | Deep blue: `#1a237e`, `#283593`, `#2c3e50` | Warm-tinted backgrounds (`#fafafa`, cream, beige) |
| **Warm** (红/橙/棕/黄) | Warm neutrals: `#fafafa`, `#fdf6f0`, `#fff8f0` | Dark brown/warm navy: `#3e2723`, `#263238` | Cool-tinted backgrounds (ice blue, lavender) |
| **Neutral** (灰/白/黑) | Any neutral: `#f5f5f5`, `#fafafa`, `#ffffff` | Any; use tone-boldness filter | None |

### Per-Image Placement Impact
- Images placed as **full-slide background** → full compatibility required (主色 must harmonize)
- Images placed as **step-illustration / card content** → only 辅色 compatibility matters (image sits inside a card area)
- Images placed as **decorative corner** → minimal impact, no restriction

## Tone-Boldness Principle
Content energy level determines palette boldness:

| Content Tone | Palette Direction | Saturation | Contrast | 推荐模式 | Example |
|-------------|------------------|-----------|----------|----------|---------|
| Creative / 活力 / 营销 | Bold, vibrant | High | High | C — 黑底霓虹 | 亮橙+深蓝, 荧光绿+黑 |
| Professional / 中性 / 内部培训 | Balanced | Medium | Medium | A — 冷主暖点 | 深蓝+白+红点缀 |
| Formal / 严肃 / 技术文档 | Dark, subdued | Low | Low | B 低饱和变体 | 深灰+白, 墨绿+白 |
| Academic / 学术 / 数据报告 | Muted, clean | Low-Medium | Medium | B 高对比变体 | 深蓝+浅灰+青绿 |
| Modern / 简洁 / 产品介绍 | Clean, minimal | Medium | Medium | B — 全冷单色系 | 单色家族渐变 |

**Rule**: After searching for color palettes, always filter through this table — discard palettes that conflict with the content's energy level.

## 点缀色 Usage Rule (CRITICAL)
This rule applies ONLY to 点缀色 (accent, #ff5252). The 主色 (#1a237e) has its own presence rules above (30% per page).

**On light-background slides**, the 点缀色 MUST ONLY be used for:
- Highlighted text (small portions only, ≤2 lines per page)
- Small badge/标签 backgrounds (≤60×24px)
- List dots / step numbers / small decorative markers
- CTA buttons (small, ≤160×40px)
- Underline accent beneath 主色 title bar (2px, 60-120px width, centered under title text)

**RESTRICTIONS**:
- 点缀色 MUST NEVER be used for large card backgrounds, wide text boxes, or content areas
- 点缀色 surface area on any light page MUST NOT exceed 10% of slide surface
- Large decorative blocks on light pages use 主色 (#1a1a2e) or 辅色 (#f8f9fa), NOT 点缀色
- The top border line and left vertical strip are **主色** elements, NOT 点缀色

**On dark-background slides**, 点缀色 can be used more freely:
- Underline bars, accent lines
- Chapter numbers
- Small decorative elements

## Icon Style Selection (AUTOMATIC)

Three icon styles — icons are visual markers (numbered circles, list dots, tags, arrows):

| Style | Elements | Visual Weight | When to Use |
|-------|----------|---------------|-------------|
| **A 简洁线条** | Hollow outline circles, solid tiny dots | Light | Content slides, 2-column layout, medium density |
| **B 几何色块** | Solid rounded capsules/tags, small squares | Heavy | Cover, TOC, chapter dividers, low-density cards |
| **C 纯文字** | No graphics; color/bold weight only | None | Text-heavy pages, formal/academic tone, full-bleed layout |

### Decision Priority (first match wins)

1. **Tone** (via Tone-Boldness table):
   - Creative/Vibrant → **B**
   - Professional/Neutral → **A** (default)
   - Formal/Technical → **C**
   - Academic → **C**

2. **Image color compatibility** — if source images have embedded diagrams with consistent color temperature, reflect that in icon style:
   - Cool-toned images (blue/lavender diagrams) → **A** (clean lines match technical diagrams)
   - Warm-toned images → **B** (solid blocks match organic/earthy feel)
   - Neutral → no override
   - See `references/style_system.md#image-color-compatibility-palette-selection` for extraction method

3. **Page type** (only if tone result is A, and no image conflict):
   - Cover, Ending → **C** (decorative text only)
   - TOC, Chapter → **B** (needs visual anchors)
   - Content, card-based → **B**
   - Content, text-heavy → **C**

4. **Content density** override:
   - If text lines >12 per page → downgrade: B→A, A→C
   - If text lines <5 per page → upgrade: A→B

### SVG Implementation

| Style | Element | SVG |
|-------|---------|-----|
| A | Numbered step | `<circle fill="none" stroke="[accent]" stroke-width="2.5"/>` + `<text>` |
| A | List dot | `<circle fill="[accent]" r="4"/>` |
| B | Numbered step | `<rect rx="14" fill="[accent]"/>` + `<text fill="#fff">` |
| B | List marker | `<rect rx="3" width="12" height="12" fill="[accent]"/>` |
| C | Numbered step | `<text font-weight="bold" fill="[accent]">01 Title</text>` |
| C | List marker | `<text fill="[accent]">■ text</text>` |

## Font Selection (AUTOMATIC)

### Default (Zero-Dependency)
Use **Microsoft YaHei（微软雅黑）** for both title and body, with **Arial** for English/numbers. No font installation needed — guaranteed rendering on all Windows systems.

### Alternative Pairs

| Pair | Title | Body | English | Best For | Availability |
|------|-------|------|---------|----------|-------------|
| **MSYH** (默认) | Microsoft YaHei | Microsoft YaHei | Arial | All-purpose, 零依赖 | Windows built-in |
| **Source Han** | Source Han Sans SC Bold | Source Han Sans SC Regular | Arial | 现代感, cross-platform | Free download |
| **Noto** | Noto Sans CJK SC Bold | Noto Sans CJK SC Regular | Noto Sans SC | 字重丰富, Google生态 | Free download |
| **SimHei** | SimHei Bold | Microsoft YaHei | Arial | 强对比, 粗黑配细雅黑 | Windows built-in |

### Decision Priority

1. **Installation check** — prefer fonts already on the system
2. **Tone** (via Tone-Boldness table):
   - Creative/Vibrant → **Source Han** (几何现代感)
   - Professional/Neutral → **MSYH** (default)
   - Formal/Technical → **SimHei + MSYH** (粗黑标题显正式)
   - Academic → **Source Han** or **Noto** (字怀大, 学术感)
3. **Page type** override (only when tone result is ambiguous):
   - Cover title → pair that emphasizes contrast (SimHei+MSYH or Source Han)
   - Body-heavy slides → MSYH (最佳屏幕阅读)
   - Data/number-heavy slides → pair with Arial numbers (all pairs satisfy)

## Layout Variant Mapping (AUTOMATIC)

Each page's `structure` type (from `page_content.json`) maps to a layout variant:

| Structure | Default Variant | Condition | Alternative |
|-----------|----------------|-----------|-------------|
| `总分` | `content-single` | details ≤4 items | `content-list` when >4 items |
| `总分总` | `content-three` | — | — |
| `并列` | `content-cards` | items[] have title+desc | `content-table` when items are plain text strings |
| `递进` | `content-flow` | steps ≤6 | vertical flow when >6 steps |
| `对比` | `content-split` | — | — |
| `N/A` | per page_type | cover→`cover`, toc→`toc`, chapter→`chapter`, ending→`ending` | — |

### Decision Priority

1. **Page type** (cover/toc/chapter/content/ending) determines template
2. **Structure** determines variant for content pages
3. **Item count & structure** fine-tunes: fewer items → simpler layout, more items → list/table
4. **Layout plan** in `_internal/01_layout_plan/layout_plan.json` — always regenerate if page_content.json changes

### Size Scale (applies to any font pair)

```
Cover title:       64px Bold       (matches Typography table)
Slide title:       48-56px Bold    (matches Typography table; use 56px for single-line, 48px for multi-line)
Section subtitle:  32px Regular    (matches Typography table)
Body text:         28px Regular    (matches Typography table; use 28px for multi-line, 32px for single-line / short body)
Card body:         24px Regular    (slightly smaller inside card contexts)
Caption/label:     20px Regular    (matches Typography table)
Page number:       16px Arial      (matches Typography table)
Footnote:          16px Arial      (minimum)
Accent text:       24px Semibold   (matches Typography table)
```

**Typography Scale Discipline**: Use ONLY the sizes above. Never add arbitrary intermediate sizes (no 13px, 19px, 25px, 30px, 34px, etc.). The limited scale is what creates the visual consistency that professional decks depend on. If content does not fit at the allowed sizes, split the slide — do not shrink the text. 📊 木友圈 2025 analysis confirms that content slides maintain 13-17 unique font-size values (median 15), while our disciplined approach targets exactly 6 distinct sizes — the constraint is intentional and improves consistency.

## Data Display Selection (AUTOMATIC)

### Available Forms

| Form | SVG Technique | Visual Weight | Best For |
|------|--------------|---------------|----------|
| **Hero Number** | `<text font-size="72-80" font-weight="bold">` + subtitle (24-28px) | 极重 | 单个核心指标，封面/结尾页 |
| **Metric Cards** | 2-4 `<rect rx="8">` cards each with number+label | 重 | 一组 KPI（如效率+30%/成本-50%/质量+25%） |
| **Bar Chart** (hand-drawn) | `<rect>` stacked, height proportional to value | 中 | 2-5 项横向数值对比 |
| **Progress Ring** | `<circle>` with `stroke-dasharray` arc fill | 中 | 百分比/完成度（如 75% 熟练度） |
| **Table** | `<line>` grid + `<text>` cells | 轻 | 多行多列结构化数据 |

### Decision Priority

1. **Data point count** (primary):
   - 1 key number → **Hero Number**
   - 2-4 metrics → **Metric Cards**
   - 5-20 items, 1 dimension → **Bar Chart**
   - 5-20 items, 2+ dimensions → **Table**
   - 1 percentage (with no other numbers) → **Progress Ring**

2. **Tone override** (only when count result is ambiguous):
   - Creative/Vibrant → upgrade: Table→Bar, Bar→Cards, Cards→Hero
   - Formal/Technical → downgrade: Hero→Cards, Cards→Bar, Bar→Table

3. **Page layout constraint**:
   - Full-bleed / minimal text → **Hero Number** or **Progress Ring**
   - Two-column (left text, right visual) → **Bar Chart** or **Progress Ring**
   - Card grid layout → **Metric Cards**
   - Text-heavy → **Table** (lowest visual intrusion)

4. **Space available** (final check):
   - Total page text lines > 8 → prefer lighter form (Bar→Cards→Hero)
   - Available width < 400px → prefer vertical stack (Cards stacked, Bar vertical)

## Naming Conventions
- SVG template files: `{type}.svg` (cover, toc, chapter, content, ending)
- Output PPTX: `{project_name}_{timestamp}.pptx`
- Layout marker comments in SVG: `<!-- LAYOUT:{type} -->`
