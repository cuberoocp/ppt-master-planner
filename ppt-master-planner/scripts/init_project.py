#!/usr/bin/env python3
"""PPT Master Planner — Project initialization scaffold.

Creates the _internal/ directory structure, writes empty contract files,
and sets the initial flow state to 'approach'.
"""

import argparse
import json
import os
import sys
from pathlib import Path


PROJECT_STRUCTURE = {
    "_internal": {
        "00_project": None,
        "01_content": None,
        "01_layout_plan": None,
        "02_svg_source": None,
        "03_png_preview": None,
        "04_validation": None,
        "05_review": {"batches": None, "versions": None},
        "06_ppt_output": None,
        "ref": None,
    }
}

FLOW_STATE_TEMPLATE = {
    "project": "",
    "version": "1.0",
    "current_state": "approach",
    "approach_complete": False,
    "content_complete": False,
    "layout_approved": False,
    "strategist_complete": False,
    "batches": [],
    "current_batch": 0,
    "export_allowed": False,
    "created_at": "",
    "updated_at": "",
}

PAGE_MANIFEST_TEMPLATE = {
    "project": "",
    "version": "1.0",
    "batch_size": 3,
    "batch_config": {},
    "pages": [],
}

PIPELINE_CONFIG_TEMPLATE = {
    "project": "",
    "canvas_format": "ppt169",
    "canvas_width": 1920,
    "canvas_height": 1080,
    "batch_size": 3,
    "svg_rules": {
        "allow_filter": False,
        "allow_use": False,
        "allow_style": False,
        "allow_foreign_object": False,
        "allow_animate": False,
        "allow_marker": False,
        "allow_mask": False,
        "allow_stroke_dasharray": False,
        "allow_rotate": False,
    },
    "safe_margin": 60,
    "min_font_size_px": 20,
}


def create_structure(base: Path, struct: dict, parent: Path = None):
    """Recursively create directory structure."""
    current = parent / base if parent else Path(base)
    for name, sub in struct.items():
        target = current / name
        target.mkdir(parents=True, exist_ok=True)
        if sub is not None:
            create_structure(name, sub, current)


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def init_project(project_dir: str, source: str = None, canvas_format: str = "ppt169"):
    project_path = Path(project_dir)
    if project_path.exists():
        print(f"[ERROR] Project directory already exists: {project_dir}", file=sys.stderr)
        sys.exit(1)

    canvas_config = {
        "ppt169": (1920, 1080),
        "ppt43": (1024, 768),
        "xhs": (1242, 1660),
        "story": (1080, 1920),
        "square": (1080, 1080),
    }

    w, h = canvas_config.get(canvas_format, (1920, 1080))

    project_path.mkdir(parents=True, exist_ok=True)

    internal = project_path / "_internal"
    for name in ["00_project", "01_content", "01_layout_plan", "02_svg_source",
                  "03_png_preview", "04_validation", "05_review", "06_ppt_output", "ref"]:
        (internal / name).mkdir(parents=True, exist_ok=True)
    (internal / "05_review" / "batches").mkdir(parents=True, exist_ok=True)
    (internal / "05_review" / "versions").mkdir(parents=True, exist_ok=True)

    flow_state = dict(FLOW_STATE_TEMPLATE)
    flow_state["project"] = project_path.name
    flow_state["created_at"] = __import__("datetime").datetime.now().isoformat()
    flow_state["updated_at"] = flow_state["created_at"]
    flow_state["pipeline_config"] = dict(PIPELINE_CONFIG_TEMPLATE)
    flow_state["pipeline_config"]["project"] = project_path.name
    flow_state["pipeline_config"]["canvas_format"] = canvas_format
    flow_state["pipeline_config"]["canvas_width"] = w
    flow_state["pipeline_config"]["canvas_height"] = h
    write_json(internal / "00_project" / "flow_state.json", flow_state)

    write_json(internal / "00_project" / "flow_events.jsonl", {})
    with open(internal / "00_project" / "flow_events.jsonl", "w", encoding="utf-8") as f:
        f.write("")

    write_json(internal / "00_project" / "page_manifest.json", dict(PAGE_MANIFEST_TEMPLATE))
    flow_state_copy = dict(flow_state)
    flow_state_copy["pipeline_config"] = PIPELINE_CONFIG_TEMPLATE

    blank_templates = {
        "page_content.json": {"project": project_path.name, "pages": []},
        "layout_plan.json": {"project": project_path.name, "pages": []},
        "layout_capacity_report.json": {"project": project_path.name, "pages": []},
        "layout_feedback.json": {"project": project_path.name, "approval": None},
        "feedback.json": {"project": project_path.name, "batches": {}},
        "feedback_archive.json": {"project": project_path.name, "archive": []},
    }
    for fname, template in blank_templates.items():
        target = internal / "01_content" if fname == "page_content.json" else \
                 internal / "01_layout_plan" if fname in ("layout_plan.json", "layout_capacity_report.json", "layout_feedback.json") else \
                 internal / "05_review"
        if fname == "feedback_archive.json":
            target = internal / "05_review"
        write_json(target / fname, template)

    write_json(internal / "00_project" / "manifest.json", {"project": project_path.name, "page_count": 0})

    if source:
        src_path = Path(source)
        if src_path.exists():
            sources_dir = project_path / "sources"
            sources_dir.mkdir(exist_ok=True)
            import shutil
            shutil.copy2(src_path, sources_dir / src_path.name)
            print(f"[COPY] {source} -> {sources_dir / src_path.name}")

    print(f"[OK] Project initialized at {project_path}")
    print(f"[OK] Canvas: {canvas_format} ({w}x{h})")
    print(f"[OK] Current state: approach")
    print(f"[NEXT] Run: python scripts/pptflow.py {project_dir} next")


def main():
    parser = argparse.ArgumentParser(description="PPT Master Planner — project init")
    parser.add_argument("project_dir", help="Project directory path")
    parser.add_argument("--source", help="Source file to copy into project")
    parser.add_argument("--format", default="ppt169",
                        choices=["ppt169", "ppt43", "xhs", "story", "square"],
                        help="Canvas format (default: ppt169)")
    args = parser.parse_args()
    init_project(args.project_dir, args.source, args.format)


if __name__ == "__main__":
    main()
