#!/usr/bin/env python3
"""Generate layout review HTML page.

Reads page_content.json and layout_plan.json, generates an interactive
01_layout_direction.html with wireframes, copy handling, and approval controls.

Usage:
  python scripts/generate_layout_html.py <project_dir>
"""

import argparse
import json
import sys
from pathlib import Path


def generate_html(project_dir: str):
    p = Path(project_dir)
    content_path = p / "_internal" / "01_content" / "page_content.json"
    layout_path = p / "_internal" / "01_layout_plan" / "layout_plan.json"
    output_path = p / "_internal" / "01_layout_plan" / "01_layout_direction.html"

    if not content_path.exists():
        print(f"[ERROR] page_content.json not found", file=sys.stderr)
        sys.exit(1)

    with open(content_path, "r", encoding="utf-8") as f:
        content_data = json.load(f)

    layout_pages = []
    if layout_path.exists():
        with open(layout_path, "r", encoding="utf-8") as f:
            layout_data = json.load(f)
            layout_pages = layout_data.get("pages", [])

    layout_map = {lp.get("page_key", ""): lp for lp in layout_pages}
    pages = content_data.get("pages", [])

    html_parts = []
    html_parts.append("""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Layout Direction Review</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; color: #222; }
.header { background: #1a1a2e; color: #fff; padding: 24px 40px; position: sticky; top: 0; z-index: 100; }
.header h1 { font-size: 24px; }
.header .meta { color: #999; font-size: 14px; margin-top: 4px; }
.page { background: #fff; margin: 20px 40px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); overflow: hidden; }
.page-header { padding: 20px 24px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
.page-header h2 { font-size: 18px; }
.page-header .layout-badge { background: #e3f2fd; color: #1565c0; padding: 4px 12px; border-radius: 20px; font-size: 13px; }
.page-content { padding: 24px; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
@media (max-width: 800px) { .page-content { grid-template-columns: 1fr; } }
.section h3 { font-size: 14px; color: #666; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
.wireframe-box { background: #fafafa; border: 1px dashed #ccc; border-radius: 8px; min-height: 200px; position: relative; display: flex; align-items: center; justify-content: center; color: #999; font-size: 14px; }
.wireframe-box .zone { position: absolute; border: 1px solid #90caf9; background: rgba(144,202,249,0.1); border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 11px; color: #1565c0; }
.article-text { font-size: 15px; line-height: 1.6; color: #333; }
.article-text .tag { display: inline-block; background: #e8f5e9; color: #2e7d32; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-right: 4px; }
.copy-handling { font-size: 14px; line-height: 1.5; }
.copy-handling .original { color: #888; text-decoration: line-through; }
.copy-handling .compressed { color: #1565c0; }
.approval-panel { margin: 20px 40px; padding: 24px; background: #fff8e1; border-radius: 12px; border: 1px solid #ffe082; }
.approval-panel h3 { font-size: 16px; margin-bottom: 12px; }
.approval-panel label { display: block; margin: 8px 0; }
.approval-panel input[type="text"] { width: 100%; padding: 8px 12px; border: 1px solid #ccc; border-radius: 6px; font-size: 14px; }
.approval-panel button { background: #1565c0; color: #fff; border: none; padding: 10px 24px; border-radius: 6px; font-size: 15px; cursor: pointer; margin-top: 12px; }
.approval-panel button:hover { background: #0d47a1; }
.status-ok { color: #2e7d32; font-weight: bold; }
.status-error { color: #c62828; font-weight: bold; }
</style></head><body>
<div class="header">
  <h1>Layout Direction Review</h1>
  <div class="meta">Project: """ + content_data.get("project", Path(project_dir).name) + f""" | {len(pages)} pages | Session: {__import__('secrets').token_hex(4)}</div>
</div>
""")

    for i, page in enumerate(pages):
        page_key = page.get("page_key", f"page_{i+1:02d}")
        lp = layout_map.get(page_key, {})
        layout_id = lp.get("layout_id", "TBD")
        action_title = page.get("action_title", "Untitled")
        core_message = page.get("core_message", "")
        body_blocks = page.get("body_blocks", [])
        copy_handling = lp.get("copy_handling", {})
        final_on_slide = copy_handling.get("final_on_slide", {})
        wireframe = lp.get("wireframe", {})
        grid = lp.get("grid", {})

        html_parts.append(f'<div class="page" id="{page_key}">')
        html_parts.append(f'<div class="page-header"><h2>{page_key}: {action_title}</h2><span class="layout-badge">{layout_id}</span></div>')
        html_parts.append('<div class="page-content">')

        # Left: Wireframe
        html_parts.append('<div class="section"><h3>Wireframe / Layout</h3>')
        html_parts.append(f'<div class="wireframe-box" style="height:300px">')
        zones = wireframe.get("zones", [])
        if zones:
            for z in zones:
                zx = z.get("x", 0) / 1920 * 100
                zy = z.get("y", 0) / 1080 * 100
                zw = z.get("width", 100) / 1920 * 100
                zh = z.get("height", 100) / 1080 * 100
                html_parts.append(f'<div class="zone" style="left:{zx}%;top:{zy}%;width:{zw}%;height:{zh}%;">{z.get("type","")}</div>')
        else:
            html_parts.append('<span>Wireframe zones not defined</span>')
        html_parts.append('</div>')
        html_parts.append(f'<p style="font-size:12px;color:#999;margin-top:8px;">Grid: {grid.get("columns", "?")} col, rows: {grid.get("rows", "?")}</p>')
        html_parts.append('</div>')

        # Right: Copy handling
        html_parts.append('<div class="section">')
        html_parts.append(f'<h3>On-Slide Content</h3>')
        html_parts.append('<div class="copy-handling">')
        title_final = final_on_slide.get("title", action_title)
        body_final = final_on_slide.get("body", "")
        html_parts.append(f'<p><strong>Title:</strong> <span class="compressed">{title_final}</span></p>')
        if core_message:
            html_parts.append(f'<p><strong>Core:</strong> {core_message}</p>')
        if body_final:
            html_parts.append(f'<p><strong>Body:</strong></p><p>{body_final}</p>')
        # Source excerpt (collapsible)
        source_excerpt = page.get("source_excerpt", "")
        if source_excerpt:
            html_parts.append(f'<details><summary>Original source</summary><p class="original">{source_excerpt}</p></details>')
        compression = copy_handling.get("compression_rationale", "")
        if compression:
            html_parts.append(f'<p style="margin-top:8px;font-size:12px;color:#888;"><em>Rationale: {compression}</em></p>')
        # Visual asset strategy
        vas = lp.get("visual_asset_strategy", {})
        if vas:
            html_parts.append(f'<p style="margin-top:8px;"><span class="tag">Asset:</span> {vas.get("asset_type","")} — {vas.get("reason","")}</p>')
        html_parts.append('</div></div>')

        html_parts.append('</div></div>')

    # Approval panel
    html_parts.append(f"""
<div class="approval-panel">
  <h3>Submit Layout Approval</h3>
  <p>Review all pages above. When satisfied, enter the approval key and submit.</p>
  <label>Approval Key: <input type="text" id="approval-key" placeholder="Enter the one-time key from review_server"></label>
  <label><input type="checkbox" id="approve-all"> I approve the layout direction for all pages</label>
  <label>Comments:<br><textarea id="comments" rows="3" style="width:100%;padding:8px;border:1px solid #ccc;border-radius:6px;"></textarea></label>
  <button onclick="submitApproval()">Submit Approval</button>
  <p id="status" style="margin-top:8px;"></p>
</div>
<script>
async function submitApproval() {{
  const key = document.getElementById('approval-key').value;
  const approved = document.getElementById('approve-all').checked;
  const comments = document.getElementById('comments').value;
  const params = new URLSearchParams();
  params.append('approval_key', key);
  params.append('all_approved', approved ? 'true' : 'false');
  params.append('comments', comments);
  params.append('approved', approved ? 'true' : 'false');
  try {{
    const resp = await fetch('/layout-feedback', {{ method: 'POST', body: params }});
    const data = await resp.json();
    document.getElementById('status').innerHTML = data.status === 'ok'
      ? '<span class="status-ok">Approval submitted successfully!</span>'
      : '<span class="status-error">Error: ' + (data.error || 'unknown') + '</span>';
  }} catch(e) {{
    document.getElementById('status').innerHTML = '<span class="status-error">Error: ' + e.message + '</span>';
  }}
}}
</script>
</body></html>
""")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(html_parts), encoding="utf-8")
    print(f"[OK] Layout review HTML generated: {output_path}")
    print(f"[NEXT] Start review server: python scripts/review_server.py {project_dir}")


def main():
    parser = argparse.ArgumentParser(description="Generate layout review HTML")
    parser.add_argument("project_dir", help="Project directory")
    args = parser.parse_args()
    generate_html(args.project_dir)


if __name__ == "__main__":
    main()
