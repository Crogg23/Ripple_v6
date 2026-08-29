"""Rebuild reports/viz/join_handbook.html from the template + the inlined edge data.

The measured-overlap payload lives inside the existing built page (a single
`const DATA = {...}` line). This script lifts it out, drops it into the current
template, and writes the page back. Run it after any template edit:

    python reports/viz/_build/build_join_handbook.py

Pass --data <file.json> to build from a freshly exported payload instead.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent
VIZ = BUILD.parent
TEMPLATE = BUILD / "join_handbook_template.html"
PAGE = VIZ / "join_handbook.html"
MARKER = "const DATA = "
PLACEHOLDER = "__DATA_PLACEHOLDER__"


def extract_data(html: str) -> dict:
    """Pull the JSON payload out of a previously built page."""
    i = html.find(MARKER)
    if i < 0:
        raise SystemExit(f"no '{MARKER}' line found in the built page")
    start = i + len(MARKER)
    end = html.find("\n", start)
    return json.loads(html[start:end].rstrip().rstrip(";"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, help="JSON payload to build from (default: reuse the built page's)")
    ap.add_argument("--out", type=Path, default=PAGE)
    args = ap.parse_args()

    if args.data:
        data = json.loads(args.data.read_text(encoding="utf-8"))
    else:
        if not PAGE.exists():
            raise SystemExit(f"{PAGE} does not exist and no --data given")
        data = extract_data(PAGE.read_text(encoding="utf-8"))

    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise SystemExit(f"template is missing {PLACEHOLDER}")

    blob = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    # </script> inside a JS string literal would close the block early.
    blob = blob.replace("</", "<\\/")

    html = template.replace(PLACEHOLDER, blob)
    args.out.write_text(html, encoding="utf-8")

    edges = sum(len(v) for v in data["edges"].values())
    print(f"wrote {args.out}  ({len(html):,} bytes)")
    print(f"  {len(data['tables']):,} tables, {edges:,} measured connections")
    return 0


if __name__ == "__main__":
    sys.exit(main())
