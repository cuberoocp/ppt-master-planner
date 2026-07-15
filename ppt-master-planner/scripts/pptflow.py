#!/usr/bin/env python3
"""PPT Master Planner — State machine controller.

Manages the 6-state pipeline:
  approach → content → plan → draft → review → export

Usage:
  python scripts/pptflow.py <project_dir> status
  python scripts/pptflow.py <project_dir> next
  python scripts/pptflow.py <project_dir> export
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def load_flow_state(project_dir: str) -> dict:
    path = Path(project_dir) / "_internal" / "00_project" / "flow_state.json"
    if not path.exists():
        print(f"[ERROR] flow_state.json not found at {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_flow_state(project_dir: str, state: dict):
    path = Path(project_dir) / "_internal" / "00_project" / "flow_state.json"
    state["updated_at"] = datetime.now().isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def append_event(project_dir: str, event: dict):
    path = Path(project_dir) / "_internal" / "00_project" / "flow_events.jsonl"
    event["timestamp"] = datetime.now().isoformat()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def load_page_manifest(project_dir: str) -> dict:
    path = Path(project_dir) / "_internal" / "00_project" / "page_manifest.json"
    if not path.exists():
        return {"project": Path(project_dir).name, "version": "1.0", "batch_size": 3, "pages": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_page_manifest(project_dir: str, manifest: dict):
    path = Path(project_dir) / "_internal" / "00_project" / "page_manifest.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)


def derive_state(project_dir: str) -> str:
    """Determine the current state based on artifacts on disk."""
    state = load_flow_state(project_dir)
    p = Path(project_dir)
    internal = p / "_internal"

    # APPROACH -> CONTENT gate: approach_complete
    if not state.get("approach_complete", False):
        return "approach"

    # CONTENT gate: page_content.json has pages
    content_path = internal / "01_content" / "page_content.json"
    content_complete = state.get("content_complete", False)
    if not content_complete:
        return "content"

    # PLAN gate: layout_approved
    if not state.get("layout_approved", False):
        return "plan"

    # STRATEGIST gate: strategist_complete
    if not state.get("strategist_complete", False):
        return "strategist"

    # EXPORT gate: all_batches_visual_approved
    manifest = load_page_manifest(project_dir)
    all_approved = all(
        page.get("visual_approved", False) and page.get("export_allowed", False)
        for page in manifest.get("pages", [])
        if page.get("status") != "planned"
    )

    if all_approved and state.get("export_allowed", False):
        return "export_ready"

    # Check if current batch has visual approval
    current_batch = state.get("current_batch", 0)
    batches = state.get("batches", [])

    if current_batch >= len(batches):
        # All batches done -> check export
        return "export_ready" if state.get("export_allowed", False) else "review"

    # Determine if current batch is in draft or review
    batch_info = batches[current_batch]
    batch_pages = [p for p in manifest.get("pages", [])
                   if p.get("batch", 0) == current_batch + 1]

    if all(p.get("visual_approved", False) for p in batch_pages if p.get("status") != "planned"):
        if current_batch + 1 >= len(batches):
            return "review"  # waiting for export gate
        return "review"  # all batches done, waiting for next batch or export

    # Check if SVGs exist for current batch
    svg_dir = internal / "02_svg_source"
    if svg_dir.exists():
        batch_svgs = list(svg_dir.glob(f"batch_{current_batch + 1}_*.svg"))
        if batch_svgs:
            return "draft"

    return "draft"


def cmd_status(project_dir: str):
    state = load_flow_state(project_dir)
    current = derive_state(project_dir)

    print(f"Project: {state['project']}")
    print(f"State:   {current}")
    print(f"Canvas:  {state.get('pipeline_config', {}).get('canvas_format', 'ppt169')}")
    print()

    manifest = load_page_manifest(project_dir)
    total = len(manifest.get("pages", []))
    approved = sum(1 for p in manifest.get("pages", []) if p.get("visual_approved", False))
    print(f"Pages:   {total} total, {approved} approved")

    batches = state.get("batches", [])
    print(f"Batches: {len(batches)} configured, current batch #{state.get('current_batch', 0) + 1}")

    print(f"\nFlow flags:")
    for key in ["approach_complete", "content_complete", "layout_approved",
                "strategist_complete", "export_allowed"]:
        print(f"  {key}: {state.get(key, False)}")


def cmd_next(project_dir: str):
    current = derive_state(project_dir)
    state = load_flow_state(project_dir)

    print(f"[NEXT] Current state: {current}\n")

    if current == "approach":
        print("1. Gather source materials and place in sources/")
        print("2. Run: python scripts/pipeline_gate.py <project_dir> approach-ready")
        print("3. If using topic-research workflow, run that first")

    elif current == "content":
        print("1. Read source materials and write _internal/01_content/page_content.json")
        print("2. Write page list to _internal/00_project/page_manifest.json")
        print("3. Validate: python scripts/validate_project_contracts.py <project_dir> --stage content")
        print("4. Gate: python scripts/pipeline_gate.py <project_dir> content-ready")

    elif current == "plan":
        print("1. Read references/layout_taxonomy.md and references/layout_plan_contract.md")
        print("2. Write _internal/01_layout_plan/layout_plan.json with per-page layout")
        print("3. Estimate capacity: python scripts/estimate_layout_capacity.py <project_dir>")
        print("4. Generate layout review: python scripts/generate_layout_html.py <project_dir>")
        print("5. Start review server: python scripts/review_server.py <project_dir>")
        print("6. User reviews layout in browser, submits approval")
        print("7. Gate: python scripts/pipeline_gate.py <project_dir> layout-approved")

    elif current == "strategist":
        print("1. Read references/strategist.md")
        print("2. Read existing page_content.json and layout_plan.json")
        print("3. Present 8 Confirmations to user (BLOCKING - chat)")
        print("4. Write design_spec.md and spec_lock.md to project root")
        print("5. Gate: python scripts/pipeline_gate.py <project_dir> strategist-ready")

    elif current == "draft":
        state = load_flow_state(project_dir)
        batch_num = state.get("current_batch", 0) + 1
        print(f"1. Generate SVG pages for batch #{batch_num}")
        print(f"   Write to _internal/02_svg_source/batch_{batch_num}_*.svg")
        print("2. Run pipeline gate to confirm SVGs exist:")
        print(f"   python scripts/pipeline_gate.py <project_dir> batch-svg-ready --batch {batch_num}")
        print("3. Render PNGs:")
        print(f"   python scripts/render_svg_png.py <project_dir> --batch {batch_num}")
        print("4. Validate SVGs:")
        print(f"   python scripts/validate_svg_layout.py <project_dir> --batch {batch_num}")
        print("5. Run preview-ready gate:")
        print(f"   python scripts/pipeline_gate.py <project_dir> preview-ready --batch {batch_num}")

    elif current == "review":
        batch_num = state.get("current_batch", 0) + 1
        print(f"1. Generate visual review HTML:")
        print(f"   python scripts/generate_review_html.py <project_dir> --batch {batch_num}")
        print("2. Start review server:")
        print("   python scripts/review_server.py <project_dir>")
        print("3. User reviews batch in browser, submits approval")
        print(f"4. Gate: python scripts/pipeline_gate.py <project_dir> visual-approved --batch {batch_num}")
        print("5. After approval, next batch starts or proceed to export")

    elif current == "export_ready":
        print("1. All batches approved!")
        print("2. Run: python scripts/pptflow.py <project_dir> export")
        print("   This will run: total_md_split → finalize_svg → svg_to_pptx")


def cmd_export(project_dir: str):
    current = derive_state(project_dir)
    if current != "export_ready":
        print(f"[ERROR] Cannot export. Current state: {current}", file=sys.stderr)
        print("[ERROR] All pages must be visual-approved before export.", file=sys.stderr)
        sys.exit(1)

    print("[EXPORT] Running export pipeline...")
    scripts_dir = Path(__file__).parent

    print("[EXPORT 1/3] Running pipeline_gate export-ready...")
    result = subprocess.run(
        [sys.executable, str(scripts_dir / "pipeline_gate.py"), project_dir, "export-ready"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[ERROR] Export-ready gate failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(result.stdout)

    os.environ["SMART_SVG_EXPORT_APPROVED_BY_PPTFLOW"] = "1"

    svg_to_ppt_script = scripts_dir / "native_svg_to_ppt.py"
    if svg_to_ppt_script.exists():
        print("[EXPORT 2/3] Running native_svg_to_ppt.py...")
        result = subprocess.run(
            [sys.executable, str(svg_to_ppt_script), project_dir],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"[WARN] SVG to PPTX had issues:\n{result.stderr}", file=sys.stderr)
        print(result.stdout)
    else:
        print("[WARN] native_svg_to_ppt.py not found — SVG to PPTX conversion skipped.")

    print(f"[EXPORT] Complete! PPTX should be at {project_dir}/final_deck.pptx")


def main():
    parser = argparse.ArgumentParser(description="PPT Master Planner — flow controller")
    parser.add_argument("project_dir", help="Project directory")
    parser.add_argument("command", choices=["status", "next", "export"],
                        help="Command to execute")
    args = parser.parse_args()

    if args.command == "status":
        cmd_status(args.project_dir)
    elif args.command == "next":
        cmd_next(args.project_dir)
    elif args.command == "export":
        cmd_export(args.project_dir)


if __name__ == "__main__":
    main()
