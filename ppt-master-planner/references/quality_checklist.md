# Quality Checklist

## Content Quality
- [ ] Each slide has exactly one main message
- [ ] Text optimized for reading (≤ 7 bullet points per slide)
- [ ] No orphaned headings or empty slides
- [ ] Content logically flows from slide to slide
- [ ] Key data points are highlighted, not buried in text
- [ ] Tone is consistent throughout
- [ ] Each slide passes the "5-second test" (main message clear in 5s)

## Visual Quality
- [ ] Colors match style system palette
- [ ] No more than 3 font families used
- [ ] Text/background contrast ratio ≥ 4.5:1 (WCAG AA)
- [ ] Images properly sized (not stretched/pixelated)
- [ ] Alignment consistent across slides
- [ ] White space balanced (not too cramped, not too sparse)
- [ ] SVG passes `validate_svg_layout.py` with 0 errors
- [ ] SVG elements within canvas bounds (1920×1080)

## Technical Quality
- [ ] SVG→PPTX conversion completes without errors
- [ ] All text elements render in PPTX
- [ ] Hyperlinks functional (if any)
- [ ] Slide dimensions correct (16:9)
- [ ] File size reasonable (< 10MB for 20-slide deck)
- [ ] Review HTML renders correctly in browser
- [ ] Review server returns valid one-time-password confirmation

## Pipeline Gate Checklist
- [ ] Content phase: `pipeline_gate.py --phase content` passes
- [ ] Plan phase: `pipeline_gate.py --phase plan` passes  
- [ ] Draft phase: `pipeline_gate.py --phase draft` passes
- [ ] Review phase: `pipeline_gate.py --phase review` passes
- [ ] Export phase: `pipeline_gate.py --phase export` passes

## Batch Review (per batch of ~3 slides)
- [ ] Batch page plan consistent with overall outline
- [ ] SVG layout matches planned layout type
- [ ] Visual density appropriate (not overstuffed)
- [ ] Color usage consistent with adjacent batches
- [ ] Review server confirms batch approval
