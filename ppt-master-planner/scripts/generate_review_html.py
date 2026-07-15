#!/usr/bin/env python3
"""Generate visual review HTML page.

Reads SVG pages, validation summary, and renders an interactive 02_visual_review.html
for per-batch human visual approval.

Usage:
  python scripts/generate_review_html.py <project_dir> --batch N
"""

import argparse
import json
import sys
from pathlib import Path


def generate_review_html(project_dir: str, batch_num: int):
    p = Path(project_dir)
    svg_dir = p / "_internal" / "02_svg_source"
    png_dir = p / "_internal" / "03_png_preview"
    val_dir = p / "_internal" / "04_validation"
    manifest_path = p / "_internal" / "00_project" / "page_manifest.json"
    output_path = p / "_internal" / "05_review" / "02_visual_review.html"

    if not manifest_path.exists():
        print(f"[ERROR] page_manifest.json not found", file=sys.stderr)
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    batch_pages = [pg for pg in manifest.get("pages", []) if pg.get("batch") == batch_num]

    if not batch_pages:
        print(f"[ERROR] No pages found for batch #{batch_num}", file=sys.stderr)
        sys.exit(1)

    validation = {}
    val_summary_path = val_dir / "validation_summary.json"
    if val_summary_path.exists():
        with open(val_summary_path, "r", encoding="utf-8") as f:
            validation = json.load(f)

    html_parts = []
    html_parts.append(f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Visual Review — Batch #{batch_num}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; color: #222; }}
.header {{ background: #1a1a2e; color: #fff; padding: 24px 40px; position: sticky; top: 0; z-index: 100; }}
.header h1 {{ font-size: 24px; }}
.header .meta {{ color: #999; font-size: 14px; margin-top: 4px; }}
.page {{ background: #fff; margin: 20px 40px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); overflow: hidden; }}
.page-header {{ padding: 20px 24px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }}
.page-header h2 {{ font-size: 18px; }}
.page-preview {{ padding: 24px; text-align: center; background: #fafafa; }}
.page-preview img {{ max-width: 100%; max-height: 500px; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
.page-issues {{ padding: 12px 24px; }}
.issue {{ padding: 6px 12px; margin: 4px 0; border-radius: 4px; font-size: 13px; }}
.issue.error {{ background: #ffebee; color: #c62828; }}
.issue.warning {{ background: #fff3e0; color: #e65100; }}
.issue.info {{ background: #e3f2fd; color: #1565c0; }}
.approval-panel {{ margin: 20px 40px; padding: 24px; background: #fff8e1; border-radius: 12px; border: 1px solid #ffe082; }}
.approval-panel h3 {{ font-size: 16px; margin-bottom: 12px; }}
.approval-panel label {{ display: block; margin: 8px 0; }}
.approval-panel input[type="text"] {{ width: 100%; padding: 8px 12px; border: 1px solid #ccc; border-radius: 6px; font-size: 14px; }}
.approval-panel textarea {{ width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 6px; font-size: 14px; }}
.approval-panel button {{ background: #1565c0; color: #fff; border: none; padding: 10px 24px; border-radius: 6px; font-size: 15px; cursor: pointer; margin-top: 12px; }}
.approval-panel button:hover {{ background: #0d47a1; }}
.approval-panel button.secondary {{ background: #666; }}
.status-ok {{ color: #2e7d32; font-weight: bold; }}
.status-error {{ color: #c62828; font-weight: bold; }}
</style></head><body>
<div class="header">
  <h1>Visual Review — Batch #{batch_num}</h1>
  <div class="meta">{len(batch_pages)} pages | Validation: {validation.get('passed', False) and '[OK] Passed' or '[FAIL] Issues found'}</div>
</div>
""")

    for page in batch_pages:
        page_key = page.get("page_key", f"batch_{batch_num}")
        svg_file = f"batch_{batch_num}_{page_key}.svg"
        png_file = f"batch_{batch_num}_{page_key}.png"

        png_path = png_dir / png_file
        png_url = png_path.as_uri() if png_path.exists() else ""

        page_issues = [i for i in validation.get("warnings", []) + validation.get("errors", []) + validation.get("blockers", []) if i.get("page") == page_key]
        page_issues += [i for i in validation.get("infos", []) if i.get("page") == page_key]

        html_parts.append(f'<div class="page" id="{page_key}">')
        html_parts.append(f'<div class="page-header"><h2>{page_key}</h2><span class="layout-badge">{svg_file}</span></div>')
        html_parts.append(f'<div class="page-preview">')
        if png_url:
            html_parts.append(f'<img src="{png_url}" alt="{page_key} preview">')
        else:
            html_parts.append(f'<p style="color:#999;">PNG preview not available. Run: python scripts/render_svg_png.py {project_dir} --batch {batch_num}</p>')
        html_parts.append('</div>')

        if page_issues:
            html_parts.append('<div class="page-issues">')
            for issue in page_issues:
                cls = issue.get("level", "info")
                html_parts.append(f'<div class="issue {cls}">[{cls.upper()}] {issue.get("code","")}: {issue.get("message","")}</div>')
            html_parts.append('</div>')

        html_parts.append('</div>')

    # Approval panel
    html_parts.append(f"""
<div class="approval-panel">
  <h3>Submit Visual Approval — Batch #{batch_num}</h3>
  <p>Review all pages above. Check each page's PNG and validation issues, then submit.</p>
  <label>Approval Key: <input type="text" id="approval-key" placeholder="Enter the one-time key from review_server"></label>
  <label><input type="checkbox" id="approve-all"> I approve all pages in this batch</label>
  <label>Comments:<br><textarea id="comments" rows="3" style="width:100%;"></textarea></label>
  <button onclick="submitReview()">Submit Approval</button>
  <button class="secondary" onclick="submitReject()">Request Changes</button>
  <p id="status" style="margin-top:8px;"></p>
</div>
<script>
async function submitReview(approved) {{
  const key = document.getElementById('approval-key').value;
  const allApproved = approved !== undefined ? approved : document.getElementById('approve-all').checked;
  const comments = document.getElementById('comments').value;
  const params = new URLSearchParams();
  params.append('approval_key', key);
  params.append('all_approved', allApproved ? 'true' : 'false');
  params.append('comments', comments);
  params.append('batch_id', 'batch_{batch_num}');
  try {{
    const resp = await fetch('/review-feedback', {{ method: 'POST', body: params }});
    const data = await resp.json();
    document.getElementById('status').innerHTML = data.status === 'ok'
      ? '<span class="status-ok">Feedback submitted! Run: pipeline_gate visual-approved --batch {batch_num}</span>'
      : '<span class="status-error">Error: ' + (data.error || 'unknown') + '</span>';
  }} catch(e) {{
    document.getElementById('status').innerHTML = '<span class="status-error">Error: ' + e.message + '</span>';
  }}
}}
function submitReject() {{ submitReview(false); }}
</script>
</body></html>
""")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(html_parts), encoding="utf-8")
    print(f"[OK] Visual review HTML generated: {output_path}")
    print(f"[NEXT] Start review server: python scripts/review_server.py {project_dir}")


def main():
    parser = argparse.ArgumentParser(description="Generate visual review HTML")
    parser.add_argument("project_dir", help="Project directory")
    parser.add_argument("--batch", type=int, required=True, help="Batch number")
    args = parser.parse_args()
    generate_review_html(args.project_dir, args.batch)


if __name__ == "__main__":
    main()
