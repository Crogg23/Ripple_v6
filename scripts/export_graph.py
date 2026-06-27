"""Export outputs/connect_graph.json into formats real graph tools eat.

Plotly can't do interactive network graphs; purpose-built tools can. This turns the
cached graph into:
  - outputs/graph_nodes.csv / graph_links.csv  → Cosmograph (cosmograph.app), Gephi, sigma
  - outputs/graph.gexf                         → Gephi / yEd / Cytoscape (positions + attrs)

Run:  python3 scripts/export_graph.py
"""
from __future__ import annotations
import csv, json, math
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
G = json.loads((ROOT / "outputs" / "connect_graph.json").read_text())
nodes, edges = G["nodes"], G["edges"]

TIER_RANK = {"STEEL":6,"STRONG":5,"BRIDGE":4,"CORROBORATED":3,"GEO":2,"PROBABILISTIC":1}
TIER_RGB = {"STEEL":(244,194,13),"STRONG":(77,166,255),"BRIDGE":(232,121,249),
            "CORROBORATED":(34,211,238),"GEO":(54,201,138),"PROBABILISTIC":(154,160,166)}
deg, mtier = {}, {}
for e in edges:
    r = TIER_RANK.get(e["tier"], 0)
    for x in (e["a"], e["b"]):
        deg[x] = deg.get(x, 0) + 1
        mtier[x] = max(mtier.get(x, 0), r)
rank_tier = {v: k for k, v in TIER_RANK.items()}

def label(nid):
    s = nid
    for p in ("PORTAL_SOC_","PORTAL_ARC_","PORTAL_"): 
        if s.startswith(p): s = s[len(p):]; break
    return s.replace("FED_","").replace("INTL_","").replace("XC_","").replace("_"," ").title()

# ---- CSVs ----
with open(ROOT/"outputs"/"graph_nodes.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["id","label","domain","rows","degree","tier","x","y"])
    for n in nodes:
        nid=n["id"]; t=rank_tier.get(mtier.get(nid,0),"")
        w.writerow([nid,label(nid),n["domain"],n["rows"],deg.get(nid,0),t,
                    n.get("x",""),n.get("y","")])
with open(ROOT/"outputs"/"graph_links.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["source","target","tier","key","matched","match_rate"])
    for e in edges:
        w.writerow([e["a"],e["b"],e["tier"],e["key"],e["matched"],e["match_rate"]])

# ---- GEXF (positions + attributes, Gephi opens it directly) ----
out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
       '<graph defaultedgetype="undirected">',
       '<attributes class="node">',
       '<attribute id="0" title="domain" type="string"/>',
       '<attribute id="1" title="rows" type="long"/>',
       '<attribute id="2" title="degree" type="integer"/>',
       '<attribute id="3" title="tier" type="string"/></attributes>',
       '<attributes class="edge">',
       '<attribute id="10" title="key" type="string"/>',
       '<attribute id="11" title="tier" type="string"/></attributes>',
       '<nodes>']
for n in nodes:
    nid=n["id"]; t=rank_tier.get(mtier.get(nid,0),"")
    r,g,b = TIER_RGB.get(t,(120,120,120))
    size = 6 + 4*math.log10(max(deg.get(nid,1),1))
    x,y = n.get("x",0.0)*50, n.get("y",0.0)*50
    out.append(f'<node id="{escape(nid)}" label="{escape(label(nid))}">')
    out.append(f'<attvalues><attvalue for="0" value="{escape(n["domain"])}"/>'
               f'<attvalue for="1" value="{n["rows"]}"/>'
               f'<attvalue for="2" value="{deg.get(nid,0)}"/>'
               f'<attvalue for="3" value="{t}"/></attvalues>')
    out.append(f'<viz:position x="{x:.2f}" y="{y:.2f}" z="0"/>')
    out.append(f'<viz:size value="{size:.2f}"/>')
    out.append(f'<viz:color r="{r}" g="{g}" b="{b}"/></node>')
out.append('</nodes><edges>')
for i,e in enumerate(edges):
    out.append(f'<edge id="{i}" source="{escape(e["a"])}" target="{escape(e["b"])}" '
               f'weight="{max(e["matched"],1)}"><attvalues>'
               f'<attvalue for="10" value="{escape(e["key"])}"/>'
               f'<attvalue for="11" value="{e["tier"]}"/></attvalues></edge>')
out.append('</edges></graph></gexf>')
(ROOT/"outputs"/"graph.gexf").write_text("\n".join(out), encoding="utf-8")

print(f"nodes={len(nodes)} edges={len(edges)}")
for fn in ("graph_nodes.csv","graph_links.csv","graph.gexf"):
    p = ROOT/"outputs"/fn
    print(f"  {p}  ({p.stat().st_size/1024:.0f} KB)")
