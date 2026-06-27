"""Render the warehouse as ER diagrams — boxes = datasets, lines = measured joins.

This is the 'what data do I have and what connects to what' view, done as a schema
diagram instead of a force-graph hairball. One diagram PER join key (NPI, CCN, EIN…)
so each stays readable. Output:
  - outputs/erd/erd_<key>.md   → paste-free: open in VS Code (Mermaid preview)
  - outputs/erd/index.html     → self-contained, offline, double-click (mermaid vendored)

Run:  python3 scripts/erd.py
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G = json.loads((ROOT / "outputs" / "connect_graph.json").read_text())
N = {n["id"]: n for n in G["nodes"]}

ENT_IDS = {"NPI","CCN","EIN","UEI","CIK","IMO","MMSI","LEI","NDC","NCES"}
KEYS = ["NPI","CCN","EIN","NCES","CIK","UEI"]   # one ER diagram each (entity hard-IDs)

def mermaid(key: str) -> tuple[str, int, int]:
    edges = [e for e in G["edges"] if e["key"] == key]
    nids = sorted({e["a"] for e in edges} | {e["b"] for e in edges})
    L = ["erDiagram"]
    for nid in nids:
        L.append(f"  {nid} {{")
        for k in N[nid].get("keys", []):
            L.append(f"    {'id' if k in ENT_IDS else 'col'} {k}")
        L.append("  }")
    seen = set()
    for e in sorted(edges, key=lambda e: -e["matched"]):
        a, b = sorted((e["a"], e["b"]))
        if (a, b) in seen:
            continue
        seen.add((a, b))
        L.append(f'  {a} }}o--o{{ {b} : "{e["matched"]:,}"')
    return "\n".join(L), len(nids), len(seen)

OUT = ROOT / "outputs" / "erd"
OUT.mkdir(parents=True, exist_ok=True)
blocks = []
for key in KEYS:
    code, nn, ne = mermaid(key)
    if nn == 0:
        continue
    (OUT / f"erd_{key}.md").write_text(f"# Joins on {key}  ·  {nn} datasets, {ne} links\n\n```mermaid\n{code}\n```\n")
    blocks.append((key, nn, ne, code))
    print(f"  {key}: {nn} datasets, {ne} links -> outputs/erd/erd_{key}.md")

# self-contained offline viewer
sections, nav = [], []
for key, nn, ne, code in blocks:
    nav.append(f'<a href="#{key}">{key} ({nn})</a>')
    sections.append(f'<h2 id="{key}">Joins on {key} — {nn} datasets · {ne} links</h2>'
                    f'<pre class="mermaid">{code}</pre>')
html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Ripple — schema (ER diagrams)</title>
<script src="mermaid.min.js"></script>
<style>
 body{{background:#0d1117;color:#e8eaed;font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:0;padding:0 28px 80px}}
 h1{{font-size:22px}} h2{{font-size:16px;color:#9aa0a6;margin:34px 0 6px;border-top:1px solid #21262d;padding-top:22px}}
 nav{{position:sticky;top:0;background:#0d1117;padding:12px 0;border-bottom:1px solid #21262d;z-index:9}}
 nav a{{color:#4da6ff;margin-right:16px;text-decoration:none;font-size:13px}}
 .mermaid{{background:#0d1117}}
</style></head><body>
<h1>Ripple warehouse — what connects to what</h1>
<p style="color:#9aa0a6;font-size:13px">Each box is a landed dataset; lines are <b>measured</b> joins (row count = how many actually match). One diagram per entity key.</p>
<nav>{' '.join(nav)}</nav>
{''.join(sections)}
<script>mermaid.initialize({{startOnLoad:true,theme:'dark',er:{{useMaxWidth:false}},securityLevel:'loose'}});</script>
</body></html>"""
(OUT / "index.html").write_text(html, encoding="utf-8")
print(f"\nwrote {OUT/'index.html'}  (offline, double-click)")
