#!/usr/bin/env python3
"""PPT Master Planner — Pipeline gate enforcer.

Each gate validates that preconditions for the next pipeline state are met.
Gates are the only mechanism that advances flow_state.json (besides init).

Usage:
  python scripts/pipeline_gate.py <project_dir> <gate> [--batch N]
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def load_flow_state(project_dir: str) -> dict:
    path = Path(project_dir) / "_internal" / "00_project" / "flow_state.json"
    if not path.exists():
        print(f"[ERROR] flow_state.json not found", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_flow_state(project_dir: str, state: dict):
    path = Path(project_dir) / "_internal" / "00_project" / "flow_state.json"
    state["updated_at"] = datetime.now().isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def load_page_manifest(project_dir: str) -> dict:
    path = Path(project_dir) / "_internal" / "00_project" / "page_manifest.json"
    if not path.exists():
        print(f"[ERROR] page_manifest.json not found", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_page_manifest(project_dir: str, manifest: dict):
    path = Path(project_dir) / "_internal" / "00_project" / "page_manifest.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)


def require_review_provenance(file_path: Path) -> dict:
    """Check that a feedback file has valid review_server provenance."""
    if not file_path.exists():
        print(f"[ERROR] No feedback file at {file_path}", file=sys.stderr)
        sys.exit(1)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    approval = data.get("approval", data)
    if not approval.get("approval_key_verified", False):
        print(f"[ERROR] Approval key not verified — human approval required", file=sys.stderr)
        sys.exit(1)
    if not approval.get("approval_key_required", False):
        print(f"[ERROR] approval_key_required is false — invalid approval", file=sys.stderr)
        sys.exit(1)
    if not approval.get("provenance", {}).get("source", "").startswith("review_server"):
        print(f"[ERROR] Provenance source is not review_server", file=sys.stderr)
        sys.exit(1)

    return data


def enforce_batch_discipline(project_dir: str, batch_num: int):
    """Check that no future batch artifacts exist."""
    svg_dir = Path(project_dir) / "_internal" / "02_svg_source"
    png_dir = Path(project_dir) / "_internal" / "03_png_preview"

    for d, label in [(svg_dir, "SVG"), (png_dir, "PNG")]:
        if d.exists():
            for f in d.iterdir():
                if f.is_file():
                    for other_batch in range(batch_num + 1, 100):
                        if f"batch_{other_batch}_" in f.name:
                            print(f"[ERROR] Future {label} artifact found: {f.name}", file=sys.stderr)
                            print(f"[ERROR] Cannot generate batch {batch_num} when batch {other_batch} artifacts exist", file=sys.stderr)
                            sys.exit(1)


# ─── Gate implementations ────────────────────────────────────────────

def gate_approach_ready(project_dir: str):
    """Mark approach phase complete."""
    state = load_flow_state(project_dir)
    if state.get("approach_complete", False):
        print("[OK] Approach already complete")
        return

    state["approach_complete"] = True
    save_flow_state(project_dir, state)
    print("[GATE] [OK] approach-ready — state advanced from 'approach' to 'content'")


def gate_content_ready(project_dir: str):
    """Check page_content.json has pages."""
    content_path = Path(project_dir) / "_internal" / "01_content" / "page_content.json"
    if not content_path.exists():
        print(f"[ERROR] page_content.json not found", file=sys.stderr)
        sys.exit(1)
    with open(content_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    if not content.get("pages"):
        print(f"[ERROR] page_content.json has no pages", file=sys.stderr)
        sys.exit(1)

    manifest = load_page_manifest(project_dir)
    if not manifest.get("pages"):
        print(f"[ERROR] page_manifest.json has no pages", file=sys.stderr)
        sys.exit(1)

    state = load_flow_state(project_dir)
    state["content_complete"] = True
    save_flow_state(project_dir, state)

    total = len(content["pages"])
    batch_size = state.get("pipeline_config", {}).get("batch_size", 3)
    num_batches = (total + batch_size - 1) // batch_size
    state["batches"] = [{"status": "planned", "pages": []} for _ in range(num_batches)]

    for i, page_entry in enumerate(manifest["pages"]):
        batch_idx = i // batch_size
        if batch_idx < len(state["batches"]):
            state["batches"][batch_idx]["pages"].append(page_entry.get("page_key", f"page_{i+1:02d}"))
        page_entry["batch"] = batch_idx + 1
        page_entry["status"] = "planned"
        page_entry["layout_approved"] = False
        page_entry["visual_approved"] = False
        page_entry["export_allowed"] = False

    manifest["batch_size"] = batch_size
    manifest["batch_config"] = {"total_batches": num_batches}
    state["current_batch"] = 0
    save_page_manifest(project_dir, manifest)
    save_flow_state(project_dir, state)

    print(f"[GATE] [OK] content-ready — {total} pages arranged into {num_batches} batches")


def gate_layout_approved(project_dir: str):
    """Check layout_feedback.json has valid review_server approval."""
    feedback_path = Path(project_dir) / "_internal" / "01_layout_plan" / "layout_feedback.json"
    data = require_review_provenance(feedback_path)

    if not data.get("approval", data).get("approved", False):
        print(f"[ERROR] Layout not approved in feedback", file=sys.stderr)
        sys.exit(1)

    state = load_flow_state(project_dir)
    state["layout_approved"] = True
    save_flow_state(project_dir, state)

    # Mark all pages as layout_approved
    manifest = load_page_manifest(project_dir)
    for page in manifest["pages"]:
        page["layout_approved"] = True
    save_page_manifest(project_dir, manifest)

    print(f"[GATE] [OK] layout-approved — layout plan validated and approved")


def gate_strategist_ready(project_dir: str):
    """Check design_spec.md and spec_lock.md exist."""
    design_spec = Path(project_dir) / "design_spec.md"
    spec_lock = Path(project_dir) / "spec_lock.md"
    if not design_spec.exists():
        print(f"[ERROR] design_spec.md not found", file=sys.stderr)
        sys.exit(1)
    if not spec_lock.exists():
        print(f"[ERROR] spec_lock.md not found", file=sys.stderr)
        sys.exit(1)

    state = load_flow_state(project_dir)
    state["strategist_complete"] = True
    save_flow_state(project_dir, state)
    print(f"[GATE] [OK] strategist-ready — design spec locked")


def gate_batch_svg_ready(project_dir: str, batch_num: int):
    """Check all SVGs for the batch exist."""
    enforce_batch_discipline(project_dir, batch_num)

    manifest = load_page_manifest(project_dir)
    batch_pages = [p for p in manifest["pages"] if p.get("batch") == batch_num]

    if not batch_pages:
        print(f"[ERROR] No pages found for batch #{batch_num}", file=sys.stderr)
        sys.exit(1)

    svg_dir = Path(project_dir) / "_internal" / "02_svg_source"
    for page in batch_pages:
        page_key = page.get("page_key", f"page_{batch_num:02d}")
        svg_path = svg_dir / f"batch_{batch_num}_{page_key}.svg"
        if not svg_path.exists():
            print(f"[ERROR] Missing SVG: {svg_path}", file=sys.stderr)
            sys.exit(1)
        page["status"] = "svg_generated"

    save_page_manifest(project_dir, manifest)
    print(f"[GATE] [OK] batch-svg-ready — batch #{batch_num} SVG check passed")


def gate_preview_ready(project_dir: str, batch_num: int):
    """Check PNGs, validation, and self-review exist for the batch."""
    png_dir = Path(project_dir) / "_internal" / "03_png_preview"
    validation_dir = Path(project_dir) / "_internal" / "04_validation"
    manifest = load_page_manifest(project_dir)
    batch_pages = [p for p in manifest["pages"] if p.get("batch") == batch_num]

    for page in batch_pages:
        page_key = page.get("page_key", f"page_{batch_num:02d}")

        png_path = png_dir / f"batch_{batch_num}_{page_key}.png"
        if not png_path.exists():
            print(f"[ERROR] Missing PNG: {png_path}", file=sys.stderr)
            sys.exit(1)

    val_summary = validation_dir / "validation_summary.json"
    if not val_summary.exists():
        print(f"[ERROR] Missing validation_summary.json", file=sys.stderr)
        sys.exit(1)

    self_review = validation_dir / "self_review.json"
    if not self_review.exists():
        print(f"[ERROR] Missing self_review.json (model must complete visual self-check)", file=sys.stderr)
        sys.exit(1)

    with open(val_summary, "r", encoding="utf-8") as f:
        val_data = json.load(f)
    errors = val_data.get("errors", [])
    if errors:
        print(f"[ERROR] Validation errors found — fix before preview:\n{errors}", file=sys.stderr)
        sys.exit(1)

    for page in batch_pages:
        page["status"] = "preview_ready"
    save_page_manifest(project_dir, manifest)

    print(f"[GATE] [OK] preview-ready — batch #{batch_num} ready for visual review")


def gate_visual_approved(project_dir: str, batch_num: int):
    """Check visual review feedback has valid approval."""
    feedback_path = Path(project_dir) / "_internal" / "05_review" / "feedback.json"
    data = require_review_provenance(feedback_path)

    all_approved = data.get("approval", data).get("all_approved", False)
    if not all_approved:
        print(f"[ERROR] Visual approval not granted", file=sys.stderr)
        sys.exit(1)

    manifest = load_page_manifest(project_dir)
    batch_pages = [p for p in manifest["pages"] if p.get("batch") == batch_num]
    for page in batch_pages:
        page["visual_approved"] = True
        page["export_allowed"] = True

    state = load_flow_state(project_dir)
    # Advance to next batch if available
    if state["current_batch"] + 1 < len(state.get("batches", [])):
        state["current_batch"] += 1
        state["batches"][state["current_batch"]]["status"] = "in_progress"
        print(f"[GATE] [OK] visual-approved — batch #{batch_num} approved. Moving to batch #{state['current_batch'] + 1}")
    else:
        state["export_allowed"] = True
        print(f"[GATE] [OK] visual-approved — batch #{batch_num} approved. All batches done.")

    save_page_manifest(project_dir, manifest)
    save_flow_state(project_dir, state)


def gate_export_ready(project_dir: str):
    """Check every page is visual-approved and export allowed."""
    manifest = load_page_manifest(project_dir)
    for page in manifest["pages"]:
        if page.get("status") in ("planned", "skipped"):
            continue
        if not page.get("visual_approved", False):
            print(f"[ERROR] Page {page.get('page_key')} not visual-approved", file=sys.stderr)
            sys.exit(1)
        if not page.get("export_allowed", False):
            print(f"[ERROR] Page {page.get('page_key')} export not allowed", file=sys.stderr)
            sys.exit(1)
    print(f"[GATE] [OK] export-ready — all pages cleared for export")


GATES = {
    "approach-ready": ("approach", gate_approach_ready),
    "content-ready": ("content", gate_content_ready),
    "layout-approved": ("plan", gate_layout_approved),
    "strategist-ready": ("strategist", gate_strategist_ready),
    "batch-svg-ready": ("draft", gate_batch_svg_ready),
    "preview-ready": ("draft", gate_preview_ready),
    "visual-approved": ("review", gate_visual_approved),
    "export-ready": ("export_ready", gate_export_ready),
}


def main():
    parser = argparse.ArgumentParser(description="PPT Master Planner — pipeline gate")
    parser.add_argument("project_dir", help="Project directory")
    parser.add_argument("gate", choices=list(GATES.keys()),
                        help="Gate to enforce")
    parser.add_argument("--batch", type=int, default=None,
                        help="Batch number (required for batch-specific gates)")
    parser.add_argument("--allow-vision-unavailable", action="store_true",
                        help="Allow preview-ready without vision check (model cannot view images)")
    args = parser.parse_args()

    gate_name = args.gate
    expected_state, gate_func = GATES[gate_name]

    requires_batch = gate_name in ("batch-svg-ready", "preview-ready", "visual-approved")
    if requires_batch and args.batch is None:
        print(f"[ERROR] --batch is required for gate '{gate_name}'", file=sys.stderr)
        sys.exit(1)

    kwargs = {}
    if args.batch is not None:
        kwargs["batch_num"] = args.batch

    gate_func(args.project_dir, **kwargs)


if __name__ == "__main__":
    main()
