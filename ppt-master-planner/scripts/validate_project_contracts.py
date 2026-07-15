#!/usr/bin/env python3
"""Validate project contracts — page_content.json, layout_plan.json, page_manifest.json.

Usage:
  python scripts/validate_project_contracts.py <project_dir> --stage content
  python scripts/validate_project_contracts.py <project_dir> --stage layout
  python scripts/validate_project_contracts.py <project_dir> --stage manifest
  python scripts/validate_project_contracts.py <project_dir> --stage all
"""

import argparse
import json
import sys
from pathlib import Path


def validate_content(project_dir: str) -> bool:
    content_path = Path(project_dir) / "_internal" / "01_content" / "page_content.json"
    if not content_path.exists():
        print(f"[CONTENT] ERROR: page_content.json not found")
        return False

    with open(content_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    errors = []
    pages = data.get("pages", [])
    if not pages:
        errors.append("No pages in page_content.json")

    for i, page in enumerate(pages):
        prefix = f"page[{i}]"
        if "page_key" not in page:
            errors.append(f"{prefix}: missing page_key")
        elif not page["page_key"].startswith("page_"):
            errors.append(f"{prefix}: page_key must start with 'page_'")
        if "action_title" not in page:
            errors.append(f"{prefix}: missing action_title")
        if "core_message" not in page:
            errors.append(f"{prefix}: missing core_message (use empty string if none)")
        if "body_blocks" not in page:
            errors.append(f"{prefix}: missing body_blocks")
        elif not isinstance(page["body_blocks"], list):
            errors.append(f"{prefix}: body_blocks must be a list")

    if errors:
        for e in errors:
            print(f"[CONTENT] {e}")
        return False

    print(f"[CONTENT] [OK] Valid — {len(pages)} pages")
    return True


def validate_layout(project_dir: str) -> bool:
    layout_path = Path(project_dir) / "_internal" / "01_layout_plan" / "layout_plan.json"
    if not layout_path.exists():
        print(f"[LAYOUT] ERROR: layout_plan.json not found")
        return False

    with open(layout_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    errors = []
    valid_layouts = [f"L{i:02d}" for i in range(16)]  # L00-L15
    pages = data.get("pages", [])
    if not pages:
        errors.append("No pages in layout_plan.json")

    for i, page in enumerate(pages):
        prefix = f"page[{i}]"
        if "page_key" not in page:
            errors.append(f"{prefix}: missing page_key")
        layout_id = page.get("layout_id", "")
        if layout_id not in valid_layouts:
            errors.append(f"{prefix}: invalid layout_id '{layout_id}' (must be L00-L15)")
        if "grid" not in page:
            errors.append(f"{prefix}: missing grid")
        if "wireframe" not in page:
            errors.append(f"{prefix}: missing wireframe")
        if "copy_handling" not in page:
            errors.append(f"{prefix}: missing copy_handling")
        else:
            ch = page["copy_handling"]
            if "final_on_slide" not in ch:
                errors.append(f"{prefix}.copy_handling: missing final_on_slide")
            if "compression_rationale" not in ch:
                errors.append(f"{prefix}.copy_handling: missing compression_rationale")

    if errors:
        for e in errors:
            print(f"[LAYOUT] {e}")
        return False

    print(f"[LAYOUT] [OK] Valid — {len(pages)} pages")
    return True


def validate_manifest(project_dir: str) -> bool:
    manifest_path = Path(project_dir) / "_internal" / "00_project" / "page_manifest.json"
    if not manifest_path.exists():
        print(f"[MANIFEST] ERROR: page_manifest.json not found")
        return False

    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    errors = []
    pages = data.get("pages", [])
    if not pages:
        errors.append("No pages in page_manifest.json")

    for i, page in enumerate(pages):
        prefix = f"page[{i}]"
        if "page_key" not in page:
            errors.append(f"{prefix}: missing page_key")
        if "status" not in page:
            errors.append(f"{prefix}: missing status")

        page_key = page.get("page_key", "")
        svg_path = page.get("svg_path", f"batch_1_{page_key}.svg")
        if not svg_path:
            errors.append(f"{prefix}: missing svg_path")

    valid_statuses = {"planned", "svg_generated", "validation_passed",
                      "preview_ready", "visual_approved", "skipped"}
    for i, page in enumerate(pages):
        status = page.get("status", "")
        if status and status not in valid_statuses:
            errors.append(f"page[{i}]: invalid status '{status}'")

    if errors:
        for e in errors:
            print(f"[MANIFEST] {e}")
        return False

    print(f"[MANIFEST] [OK] Valid — {len(pages)} pages")
    return True


def main():
    parser = argparse.ArgumentParser(description="Validate project contracts")
    parser.add_argument("project_dir", help="Project directory")
    parser.add_argument("--stage", choices=["content", "layout", "manifest", "all"],
                        default="all", help="Which contract(s) to validate")
    args = parser.parse_args()

    all_ok = True
    if args.stage in ("content", "all"):
        all_ok = validate_content(args.project_dir) and all_ok
    if args.stage in ("layout", "all"):
        all_ok = validate_layout(args.project_dir) and all_ok
    if args.stage in ("manifest", "all"):
        all_ok = validate_manifest(args.project_dir) and all_ok

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
