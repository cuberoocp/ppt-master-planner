#!/usr/bin/env python3
"""Planner phase — content strategy, outline, and page plan.

This is the new phase that distinguishes ppt-master-planner from ppt-master.
It produces structured planning artifacts before visual design begins.

Usage:
  python scripts/planner.py <source_md> --output <output_dir>
"""

import argparse
import json
import sys
from pathlib import Path


def analyze_content(source_text: str) -> dict:
    """Content analysis helper — identifies sections, key points."""
    lines = source_text.split("\n")
    sections = []
    current_section = {"title": "Introduction", "content": [], "level": 1}

    for line in lines:
        if line.startswith("#"):
            if current_section["content"]:
                sections.append(current_section)
            level = len(line.split()[0])
            title = line.lstrip("#").strip()
            current_section = {"title": title, "content": [], "level": level}
        else:
            current_section["content"].append(line)

    if current_section["content"]:
        sections.append(current_section)

    return {
        "total_chars": len(source_text),
        "total_lines": len(lines),
        "sections": sections,
    }


def generate_strategy(source_md_path: str, name: str) -> str:
    """Generate content strategy markdown."""
    return f"""# Content Strategy: {name}

## Target Audience
[Identified from source material]

## Core Message
[Primary message distilled from source]

## Secondary Messages
[Supporting points]

## Tone & Voice
[Formal, conversational, authoritative, inspirational, etc.]

## Narrative Structure
1. Opening / Context
2. Problem / Challenge
3. Solution / Approach
4. Evidence / Results
5. Conclusion / Call to Action

## Source
{source_md_path}
"""


def generate_outline(analysis: dict, name: str) -> str:
    """Generate slide outline from content analysis."""
    outline = f"# Outline: {name}\n\n"
    for i, section in enumerate(analysis.get("sections", [])):
        outline += f"## Slide {i+1}: {section['title']}\n"
        content_preview = " ".join(section["content"][:5])[:200]
        if content_preview:
            outline += f"> {content_preview}...\n"
        outline += "\n"
    return outline


def generate_page_plan(analysis: dict, name: str) -> list:
    """Generate page plan JSON from content analysis."""
    pages = []
    for i, section in enumerate(analysis.get("sections", [])):
        content_text = " ".join(section["content"])
        has_data = any(kw in content_text.lower() for kw in
                       ["%", "增长", "下降", "比例", "数据", "chart", "figure", "table"])
        has_image = any(kw in content_text.lower() for kw in
                        ["图", "image", "photo", "screenshot", "示意图"])

        page_types = ["cover", "toc", "chapter", "content", "ending", "data", "comparison"]
        if i == 0:
            ptype = "cover"
        elif i == len(analysis["sections"]) - 1:
            ptype = "ending"
        elif has_data:
            ptype = "data"
        else:
            ptype = "content"

        content_types = ["text-heavy", "visualization", "image-led", "mixed", "data"]
        if has_data:
            ctype = "data"
        elif has_image:
            ctype = "image-led"
        else:
            ctype = "text-heavy"

        pages.append({
            "page": i + 1,
            "title": section["title"],
            "type": ptype,
            "content_type": ctype,
            "layout_hint": "centered" if ptype in ("cover", "ending") else "two-column",
            "key_points": section["content"][:3] if section["content"] else [],
        })

    return pages


def main():
    parser = argparse.ArgumentParser(description="PPT Master Planner — planning phase")
    parser.add_argument("source_md", help="Source markdown file")
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    parser.add_argument("--name", help="Project name (default: source filename)")
    args = parser.parse_args()

    source_path = Path(args.source_md)
    if not source_path.exists():
        print(f"[ERROR] Source file not found: {args.source_md}", file=sys.stderr)
        sys.exit(1)

    name = args.name or source_path.stem
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    source_text = source_path.read_text(encoding="utf-8")
    analysis = analyze_content(source_text)

    strategy = generate_strategy(args.source_md, name)
    outline = generate_outline(analysis, name)
    page_plan = generate_page_plan(analysis, name)

    (output_dir / "content_strategy.md").write_text(strategy, encoding="utf-8")
    print(f"[OK] content_strategy.md")

    (output_dir / "outline.md").write_text(outline, encoding="utf-8")
    print(f"[OK] outline.md")

    (output_dir / "page_plan.json").write_text(
        json.dumps(page_plan, indent=2, ensure_ascii=False))
    print(f"[OK] page_plan.json")

    print(f"\n[PLANNER] [OK] Planning output in {output_dir}")
    print(f"  {len(page_plan)} pages planned")
    print(f"  Next: Run init_project, then write page_content.json based on the outline")


if __name__ == "__main__":
    main()
