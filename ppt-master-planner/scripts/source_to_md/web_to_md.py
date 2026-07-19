#!/usr/bin/env python3
# Based on hugohe3/ppt-master (MIT) — https://github.com/hugohe3/ppt-master
"""Web to Markdown converter (delegates to source_to_md.py).

Usage:
  python scripts/source_to_md/web_to_md.py <URL> [output.md]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from source_to_md import convert_web

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/source_to_md/web_to_md.py <URL> [output.md]")
        sys.exit(1)
    url = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    convert_web(url, output)
