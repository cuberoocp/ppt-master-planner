#!/usr/bin/env python3
# Based on hugohe3/ppt-master (MIT) — https://github.com/hugohe3/ppt-master
"""PDF to Markdown converter (delegates to source_to_md.py)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from source_to_md import convert_pdf

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/source_to_md/pdf_to_md.py <PDF_file>")
        sys.exit(1)
    convert_pdf(sys.argv[1])
