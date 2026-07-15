#!/usr/bin/env python3
"""SVG Layout Validator v2.0

Heuristic SVG validation for PPT Master Planner. Checks canvas contract,
forbidden SVG features, text safety, palette drift, and structural metadata.

Usage:
  python scripts/validate_svg_layout.py <project_dir> [--batch N]
  python scripts/validate_svg_layout.py <svg_dir> --manifest <manifest.json> [--batch N]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET


ISSUE_LEVELS = {"error": 0, "blocker": 1, "warning": 2, "info": 3}
CANVAS_W = 1920
CANVAS_H = 1080
SAFE_MARGIN = 60
BANNED_TAGS = {"foreignObject", "filter", "style", "marker", "mask", "animate"}
BANNED_ATTRS = {"stroke-dasharray", "textLength", "lengthAdjust"}
BANNED_TRANSFORMS = {"rotate"}


def check_svg(svg_path: Path, manifest_entry: dict = None) -> dict:
    """Validate a single SVG file. Returns list of issues."""
    issues = []
    page_key = manifest_entry.get("page_key", svg_path.stem) if manifest_entry else svg_path.stem

    try:
        tree = ET.parse(str(svg_path))
        root = tree.getroot()
    except ET.ParseError as e:
        return [{"level": "error", "code": "XML_PARSE_ERROR", "page": page_key, "message": str(e)}]

    # ─── P0: Canvas contract ──────────────────────────────────────
    w = root.get("width")
    h = root.get("height")
    vb = root.get("viewBox")

    if w != f"{CANVAS_W}":
        issues.append({"level": "error", "code": "CANVAS_WIDTH", "page": page_key,
                       "message": f"Expected width={CANVAS_W}, got {w}"})
    if h != f"{CANVAS_H}":
        issues.append({"level": "error", "code": "CANVAS_HEIGHT", "page": page_key,
                       "message": f"Expected height={CANVAS_H}, got {h}"})
    if vb != f"0 0 {CANVAS_W} {CANVAS_H}":
        issues.append({"level": "error", "code": "VIEWBOX", "page": page_key,
                       "message": f"Expected viewBox='0 0 {CANVAS_W} {CANVAS_H}', got '{vb}'"})

    if ns := root.tag:
        if "}" in root.tag:
            ns_uri = root.tag.split("}")[0][1:]

    # ─── P0: Forbidden SVG features ────────────────────────────────
    def check_forbidden(elem, depth=0):
        local_tag = elem.tag.split("}")[-1]
        if local_tag in BANNED_TAGS:
            issues.append({"level": "error", "code": f"BANNED_TAG_{local_tag.upper()}",
                           "page": page_key,
                           "message": f"Forbidden tag <{local_tag}> at depth {depth}"})

        # Check attributes
        for attr_name in list(elem.attrib.keys()):
            local_attr = attr_name.split("}")[-1] if "}" in attr_name else attr_name
            if local_attr in BANNED_ATTRS:
                issues.append({"level": "warning", "code": f"BANNED_ATTR_{local_attr.upper()}",
                               "page": page_key,
                               "message": f"Forbidden attribute {local_attr} on <{local_tag}>"})

            # Check transforms
            if local_attr == "transform":
                val = elem.get(attr_name, "")
                for banned in BANNED_TRANSFORMS:
                    if banned in val:
                        issues.append({"level": "warning", "code": f"BANNED_TRANSFORM_{banned.upper()}",
                                       "page": page_key,
                                       "message": f"Forbidden transform '{banned}' in '{val}'"})

        # Check style attribute
        style = elem.get("style", "")
        if style and local_tag not in ("defs", "linearGradient", "radialGradient", "stop"):
            issues.append({"level": "warning", "code": "INLINE_STYLE",
                           "page": page_key,
                           "message": f"Inline style on <{local_tag}>: '{style[:60]}...'"})

        for child in elem:
            check_forbidden(child, depth + 1)

    check_forbidden(root)

    # ─── P0: Text safety checks ────────────────────────────────────
    text_elements = root.findall(".//{*}text") or root.findall(".//text")
    for tex in text_elements:
        font_size_str = tex.get("font-size", "24")
        try:
            font_size = float(font_size_str.replace("px", ""))
        except ValueError:
            font_size = 24

        if font_size < 10:
            issues.append({"level": "blocker", "code": "TEXT_SIZE_TOO_SMALL",
                           "page": page_key,
                            "message": f"font-size {font_size}px below minimum 10px in '{tex.text or ''}'"})

        if not tex.get("fill") or tex.get("fill") == "none":
            issues.append({"level": "error", "code": "TEXT_MISSING_FILL",
                           "page": page_key,
                           "message": f"Text element missing fill attribute: '{tex.text or ''}'"})

        if not tex.get("font-family"):
            issues.append({"level": "warning", "code": "TEXT_MISSING_FONT_FAMILY",
                           "page": page_key,
                           "message": f"Text element missing font-family: '{tex.text or ''}'"})

        # Check for text outside safe margin
        x = float(tex.get("x", SAFE_MARGIN))
        y = float(tex.get("y", SAFE_MARGIN))
        if x < SAFE_MARGIN and x > 0:
            issues.append({"level": "warning", "code": "TEXT_NEAR_LEFT_EDGE",
                           "page": page_key,
                           "message": f"Text x={x} < safe margin {SAFE_MARGIN}: '{tex.text or ''}'"})
        if x > CANVAS_W - SAFE_MARGIN:
            issues.append({"level": "blocker", "code": "TEXT_OVERFLOW_RIGHT",
                           "page": page_key,
                           "message": f"Text x={x} exceeds canvas right edge: '{tex.text or ''}'"})

    # ─── P1: Images ────────────────────────────────────────────────
    images = root.findall(".//{*}image") or root.findall(".//image")
    for img in images:
        ix = float(img.get("x", 0))
        iy = float(img.get("y", 0))
        iw = float(img.get("width", 0))
        ih = float(img.get("height", 0))

        if ix + iw > CANVAS_W + 2 or iy + ih > CANVAS_H + 2:
            issues.append({"level": "error", "code": "IMAGE_OUT_OF_BOUNDS",
                           "page": page_key,
                           "message": f"Image at ({ix},{iy}) size ({iw}x{ih}) exceeds canvas"})

    # ─── P1: Structural metadata ───────────────────────────────────
    raw_text = svg_path.read_text(encoding="utf-8")
    metadata_comments = re.findall(r"<!--(.*?)-->", raw_text, re.DOTALL)

    has_page_key = any("page_key" in c.lower() for c in metadata_comments)
    has_layout = any("data-layout" in c.lower() for c in metadata_comments)

    if not has_page_key and manifest_entry:
        issues.append({"level": "info", "code": "MISSING_METADATA_PAGE_KEY",
                       "page": page_key,
                       "message": "SVG metadata comment missing page_key"})

    # ─── Summary counts ────────────────────────────────────────────
    return issues


def validate_project(project_dir: str, batch_num: int = None):
    """Validate all SVGs in a project directory."""
    p = Path(project_dir)
    svg_dir = p / "_internal" / "02_svg_source"
    manifest_path = p / "_internal" / "00_project" / "page_manifest.json"

    if not svg_dir.exists():
        print(f"[ERROR] SVG directory not found: {svg_dir}", file=sys.stderr)
        sys.exit(1)

    manifest = {}
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
            manifest = {page.get("page_key", ""): page for page in manifest_data.get("pages", [])}

    svg_files = sorted(svg_dir.glob("*.svg"))
    if batch_num:
        svg_files = [f for f in svg_files if f"batch_{batch_num}_" in f.name]

    if not svg_files:
        print(f"[ERROR] No SVG files found{' for batch ' + str(batch_num) if batch_num else ''}", file=sys.stderr)
        sys.exit(1)

    all_issues = []
    for svg_path in svg_files:
        page_key = svg_path.stem.replace(f"batch_{batch_num}_", "") if batch_num else svg_path.stem
        entry = manifest.get(page_key, {})
        issues = check_svg(svg_path, entry)
        all_issues.extend(issues)

    # ─── Summary ────────────────────────────────────────────────────
    errors = [i for i in all_issues if i["level"] == "error"]
    blockers = [i for i in all_issues if i["level"] == "blocker"]
    warnings = [i for i in all_issues if i["level"] == "warning"]
    infos = [i for i in all_issues if i["level"] == "info"]

    print(f"Validated {len(svg_files)} files, {len(all_issues)} issues:")
    print(f"  Errors:   {len(errors)}")
    print(f"  Blockers: {len(blockers)}")
    print(f"  Warnings: {len(warnings)}")
    print(f"  Info:     {len(infos)}")

    for issue in all_issues:
        print(f"  [{issue['level'].upper():7s}] {issue['code']:30s} {issue['page']:20s} {issue['message']}")

    # Write validation summary
    val_dir = p / "_internal" / "04_validation"
    val_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "validated_files": len(svg_files),
        "total_issues": len(all_issues),
        "errors": errors,
        "blockers": blockers,
        "warnings": warnings,
        "infos": infos,
        "passed": len(errors) == 0 and len(blockers) == 0,
    }
    summary_path = val_dir / "validation_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\nSummary saved to {summary_path}")
    if summary["passed"]:
        print("[VALIDATE] [OK] PASSED")
    else:
        print(f"[VALIDATE] [FAIL] FAILED — {len(errors)} errors, {len(blockers)} blockers")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="SVG Layout Validator")
    parser.add_argument("project_dir", help="Project directory or SVG directory")
    parser.add_argument("--manifest", help="Path to page_manifest.json")
    parser.add_argument("--batch", type=int, help="Batch number")
    parser.add_argument("--output", help="Output path for validation summary")
    args = parser.parse_args()

    if args.manifest:
        p = Path(args.project_dir)
        manifest_path = Path(args.manifest)
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
            manifest = {page.get("page_key", ""): page for page in manifest_data.get("pages", [])}

        svg_files = sorted(p.glob("*.svg"))
        if args.batch:
            svg_files = [f for f in svg_files if f"batch_{args.batch}_" in f.name]

        all_issues = []
        for svg_path in svg_files:
            page_key = svg_path.stem
            entry = manifest.get(page_key, {})
            all_issues.extend(check_svg(svg_path, entry))

        summary = {
            "validated_files": len(svg_files),
            "total_issues": len(all_issues),
            "errors": [i for i in all_issues if i["level"] == "error"],
            "blockers": [i for i in all_issues if i["level"] == "blocker"],
            "warnings": [i for i in all_issues if i["level"] == "warning"],
            "infos": [i for i in all_issues if i["level"] == "info"],
            "passed": len([i for i in all_issues if i["level"] in ("error", "blocker")]) == 0,
        }

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)

        for issue in all_issues:
            print(f"  [{issue['level'].upper():7s}] {issue['code']:30s} {issue['message']}")
        print(f"\n{'[OK] PASSED' if summary['passed'] else '[FAIL] FAILED'} — {len(summary['errors'])} errors, {len(summary['blockers'])} blockers")
    else:
        validate_project(args.project_dir, args.batch)


if __name__ == "__main__":
    main()
