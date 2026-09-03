"""Inject atlas_data.json into atlas_template.html -> reports/viz/atlas.html.

Run after build_atlas_data.py + build_atlas_layout.py:
    python reports/viz/_build/build_atlas_page.py
"""

import json
from pathlib import Path

BUILD = Path(__file__).resolve().parent
data = json.loads((BUILD / "atlas_data.json").read_text(encoding="utf-8"))
tpl = (BUILD / "atlas_template.html").read_text(encoding="utf-8")
payload = json.dumps(data, separators=(",", ":"))
out = BUILD.parent / "atlas.html"
out.write_text(tpl.replace("__DATA__", payload), encoding="utf-8")
print(f"wrote {out}  ({out.stat().st_size/1024:.0f} KB)")
