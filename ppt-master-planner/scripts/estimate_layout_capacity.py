#!/usr/bin/env python3
"""Estimate layout capacity — check if wireframe zones can hold planned text.

Reads page_content.json and layout_plan.json, estimates text fit per zone.

Usage:
  python scripts/estimate_layout_capacity.py <project_dir>
"""

import argparse
import json
import sys
from pathlib import Path


def estimate_text_capacity(text: str, font_size_px: int = 20, zone_width_px: int = 400) -> dict:
    """Rough estimate of text capacity in a zone."""
    if not text:
        return {"chars": 0, "estimated_lines": 0, "needed_height_px": 0, "status": "empty"}

    char_count = len(text)
    avg_char_width_px = font_size_px * 0.6
    chars_per_line = max(1, int(zone_width_px / avg_char_width_px))
    estimated_lines = max(1, -(-char_count // chars_per_line))
    line_height_px = font_size_px * 1.5
    needed_height = estimated_lines * line_height_px

    if needed_height <= font_size_px * 2:
        status = "ok"
    elif needed_height <= zone_width_px * 0.6:
        status = "tight"
    elif needed_height <= zone_width_px * 0.8:
        status = "overfull"
    else:
        status = "critical"

    return {
        "chars": char_count,
        "estimated_lines": estimated_lines,
        "needed_height_px": int(needed_height),
        "chars_per_line": chars_per_line,
        "status": status,
    }


def estimate(project_dir: str):
    p = Path(project_dir)
    content_path = p / "_internal" / "01_content" / "page_content.json"
    layout_path = p / "_internal" / "01_layout_plan" / "layout_plan.json"
    output_path = p / "_internal" / "01_layout_plan" / "layout_capacity_report.json"

    if not content_path.exists() or not layout_path.exists():
        print(f"[ERROR] page_content.json or layout_plan.json missing", file=sys.stderr)
        sys.exit(1)

    with open(content_path, "r", encoding="utf-8") as f:
        content_data = json.load(f)
    with open(layout_path, "r", encoding="utf-8") as f:
        layout_data = json.load(f)

    content_pages = {p.get("page_key", ""): p for p in content_data.get("pages", [])}
    layout_pages = {p.get("page_key", ""): p for p in layout_data.get("pages", [])}

    report = {"project": content_data.get("project", ""), "pages": []}

    for page_key in sorted(set(list(content_pages.keys()) + list(layout_pages.keys()))):
        cp = content_pages.get(page_key, {})
        lp = layout_pages.get(page_key, {})

        wireframe = lp.get("wireframe", {})
        zones = wireframe.get("zones", [])
        copy_handling = lp.get("copy_handling", {})
        final_on_slide = copy_handling.get("final_on_slide", {})

        body_text = final_on_slide.get("body", "") or " ".join(cp.get("body_blocks", []))
        title_text = final_on_slide.get("title", "") or cp.get("action_title", "")

        page_report = {
            "page_key": page_key,
            "layout_id": lp.get("layout_id", "TBD"),
            "zones": len(zones),
            "capacity": {},
        }

        if not zones:
            page_report["capacity"]["no_zones"] = True
            page_report["capacity"]["status"] = "unknown"
        else:
            # Assume first zone is for title (if it's top), others for body
            title_zone = None
            body_zones = []
            for z in zones:
                zy = z.get("y", 0)
                if zy < 200 and not title_zone:
                    title_zone = z
                else:
                    body_zones.append(z)

            if title_text and title_zone:
                zw = title_zone.get("width", 800)
                cap = estimate_text_capacity(title_text, 28, zw)
                page_report["capacity"]["title"] = cap

            if body_text and body_zones:
                total_body_area = sum(z.get("width", 400) * z.get("height", 200) for z in body_zones)
                avg_zone_w = sum(z.get("width", 400) for z in body_zones) / len(body_zones)
                cap = estimate_text_capacity(body_text, 20, int(avg_zone_w))
                page_report["capacity"]["body"] = cap
                page_report["capacity"]["body_zones"] = len(body_zones)

            statuses = [v.get("status", "ok") for v in page_report["capacity"].values() if isinstance(v, dict)]
            if "critical" in statuses:
                page_report["capacity"]["status"] = "critical"
            elif "overfull" in statuses:
                page_report["capacity"]["status"] = "overfull"
            elif "tight" in statuses:
                page_report["capacity"]["status"] = "tight"
            else:
                page_report["capacity"]["status"] = "ok"

        report["pages"].append(page_report)

        status_icon = {"ok": "[OK]", "tight": "[WARN]", "overfull": "[FAIL]", "critical": "[ERR]", "unknown": "[?]"}
        icon = status_icon.get(page_report["capacity"].get("status", "unknown"), "❓")
        status = page_report["capacity"].get("status", "unknown")
        print(f"  {icon} {page_key}: {status} ({page_report['layout_id']})")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    overfull = [p for p in report["pages"] if p["capacity"].get("status") in ("overfull", "critical")]
    if overfull:
        print(f"\n[WARN] {len(overfull)} page(s) may overflow — consider adjusting copy_handling or wireframe zones")
    else:
        print(f"\n[OK] All pages appear within capacity")

    print(f"Report saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Estimate layout capacity")
    parser.add_argument("project_dir", help="Project directory")
    args = parser.parse_args()
    estimate(args.project_dir)


if __name__ == "__main__":
    main()
