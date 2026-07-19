#!/usr/bin/env python3
# Based on hugohe3/ppt-master (MIT) — https://github.com/hugohe3/ppt-master
# Planning/review workflow inspired by thePlannerIvan/planners-ppt-hell (AGPL-3.0)
"""Render SVG pages to PNG preview images.

Requires: playwright (pip install playwright)
  Then: playwright install chromium

Usage:
  python scripts/render_svg_png.py <project_dir> [--batch N]
"""

import argparse
import sys
from pathlib import Path


def load_canvas_size(project_dir: str):
    flow_state = Path(project_dir) / "_internal" / "00_project" / "flow_state.json"
    if flow_state.exists():
        try:
            import json
            data = json.loads(flow_state.read_text(encoding="utf-8"))
            cfg = data.get("pipeline_config", {})
            w = cfg.get("canvas_width")
            h = cfg.get("canvas_height")
            if w and h:
                return int(w), int(h)
        except Exception:
            pass
    return 1920, 1080


def render_svgs(project_dir: str, batch_num: int = None):
    p = Path(project_dir)
    svg_dir = p / "_internal" / "02_svg_source"
    png_dir = p / "_internal" / "03_png_preview"
    png_dir.mkdir(parents=True, exist_ok=True)

    if not svg_dir.exists():
        print(f"[ERROR] SVG directory not found: {svg_dir}", file=sys.stderr)
        sys.exit(1)

    svg_files = sorted(svg_dir.glob("*.svg"))
    if not svg_files:
        print(f"[ERROR] No SVG files found in {svg_dir}", file=sys.stderr)
        sys.exit(1)

    canvas_w, canvas_h = load_canvas_size(project_dir)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[ERROR] playwright not installed. Run: pip install playwright && playwright install chromium", file=sys.stderr)
        sys.exit(1)

    batch_desc = f"batch #{batch_num}" if batch_num else "all"
    print(f"[RENDER] Rendering {len(svg_files)} SVGs ({batch_desc}) at {canvas_w}x{canvas_h}...")

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": canvas_w, "height": canvas_h})

        for svg_path in svg_files:
            if batch_num and f"batch_{batch_num}_" not in svg_path.name:
                continue

            png_path = png_dir / svg_path.with_suffix(".png").name

            if png_path.exists():
                print(f"  [SKIP] {svg_path.name} — PNG already exists")
                continue

            svg_url = svg_path.absolute().as_uri()
            page.goto(svg_url, wait_until="networkidle")
            page.screenshot(path=str(png_path), clip={"x": 0, "y": 0, "width": canvas_w, "height": canvas_h})
            print(f"  [OK] {svg_path.name} -> {png_path.name}")

        browser.close()

    print(f"[RENDER] [OK] Done — {len(svg_files)} SVGs rendered")


def main():
    parser = argparse.ArgumentParser(description="Render SVG to PNG")
    parser.add_argument("project_dir", help="Project directory")
    parser.add_argument("--batch", type=int, help="Batch number to render")
    args = parser.parse_args()

    render_svgs(args.project_dir, args.batch)


if __name__ == "__main__":
    main()
