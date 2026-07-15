# Visual Review Workflow

> Per-page visual self-check. Only run when the user explicitly requests a visual review.

## Process

1. Render each SVG page to PNG for visual inspection
2. Check Hard Rules (H1-H9):
   - No text overflow
   - All images render
   - Colors match spec_lock.md
   - Fonts match spec_lock.md
   - Layout follows design_spec
   - Speaker notes present
   - Valid SVG XML
   - No banned features
   - Page count matches outline
3. Check Soft Rules (S1-S10):
   - Visual hierarchy
   - Color contrast
   - Text readability
   - Balance
   - Icon consistency
4. Report findings to user
5. Fix identified issues