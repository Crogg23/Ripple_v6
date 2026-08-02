"""Compile the Library Map — one interactive picture of the whole warehouse.

    python -m viz.compile_map      ->  docs/library_map.html

One standalone page, double-click to open, no server. At rest it is the wall
map: all 1,043 datasets placed by the shipped gravity-well layout, all 2,694
verified links drawn with the ladder's grammar (stronger proof = heavier,
brighter line), the ID wells labelled, and editorial callouts explaining the
regions. Every element is a door: click a dataset and its neighbourhood lights
while a dossier drawer opens (columns, fill rates, every link graded); search
flies you anywhere; six grade switches peel the mesh weakest-first.

Geometry is reused, not reinvented: positions come straight from
outputs/library.json (compile_library's constellation layout), the edge
Béziers and trace contract are ports of viz/figures.py, and the dossier
payload is viz/compile_dictionary.build_payload. JS only ever restyles the
fixed traces — the figure is never rebuilt.
"""
import json
import math
import os

from plotly.offline import get_plotlyjs

from viz.compile_dictionary import build_payload, STATE_NAME, STATE_STORY
from viz.palette import (INK, INK_2, INK_3, LADDER_COLOUR, MONO, PANEL_2, RULE,
                         STATE_COLOUR, STATE_OPACITY, SURFACE)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "library_map.html")
UNCHARTED = 3


# --------------------------------------------------------------- figure build

def bezier(x0, y0, x1, y1, bw, bh):
    """5-point quadratic bow toward box centre (port of figures._tier_arrays)."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    cx = mx + (bw / 2 - mx) * 0.16
    cy = my + (bh / 2 - my) * 0.16
    xs, ys = [], []
    for s in (0.0, 0.25, 0.5, 0.75, 1.0):
        xs.append(round((1 - s) ** 2 * x0 + 2 * (1 - s) * s * cx + s * s * x1, 1))
        ys.append(round((1 - s) ** 2 * y0 + 2 * (1 - s) * s * cy + s * s * y1, 1))
    return xs, ys


def build_map():
    with open(os.path.join(ROOT, "outputs", "library.json"), encoding="utf-8") as f:
        lib = json.load(f)
    bw, bh = lib["box"]
    pos = lib["positions"]["connection"]
    tables, edges = lib["tables"], lib["edges"]
    conste = lib["layouts"]["constellation"]["nodes"]
    wells = lib["layouts"]["constellation"]["wells"]
    n = len(tables)

    # ---- 6 all-link tier traces, weakest FIRST so certainty lands on top
    tier_xy = {t: ([], []) for t in range(6)}
    for e in edges:
        xs, ys = tier_xy[e[2]]
        bx, by = bezier(*pos[e[0]], *pos[e[1]], bw, bh)
        xs += bx + [None]
        ys += by + [None]
    link_traces = []
    for tier in range(5, -1, -1):
        xs, ys = tier_xy[tier]
        link_traces.append({
            "type": "scattergl", "x": xs, "y": ys, "mode": "lines",
            "line": {"color": LADDER_COLOUR[tier], "width": 1.6 if tier == 0 else 1.0},
            "opacity": 0.5 if tier == 0 else 0.24,
            "name": f"links-{tier}", "hoverinfo": "skip", "showlegend": False,
        })

    # ---- 6 empty highlight traces + halo (filled by JS on selection)
    hl_traces = [{
        "type": "scattergl", "x": [], "y": [], "mode": "lines",
        "line": {"color": LADDER_COLOUR[tier], "width": 1.7 if tier == 0 else 1.1},
        "opacity": 0.95, "name": f"hl-{tier}", "hoverinfo": "skip",
        "showlegend": False,
    } for tier in range(5, -1, -1)]
    halo_trace = {
        "type": "scattergl", "x": [], "y": [], "mode": "markers",
        "marker": {"size": 26, "color": "rgba(251,192,106,.16)",
                   "line": {"width": 1, "color": "rgba(251,192,106,.35)"}},
        "hoverinfo": "skip", "showlegend": False, "name": "halo",
    }

    # ---- node trace (port of figures.node_style / node_trace, connection view)
    max_links = max((t["deg"] for t in tables), default=1) or 1
    colours, sizes, opac, text = [], [], [], []
    for i, t in enumerate(tables):
        st, nd = t["state"], conste[i]
        colours.append(STATE_COLOUR[3] if st == UNCHARTED else
                       "#f4f0e8" if nd["w"] >= 2 else
                       "#a8b8cc" if nd["w"] == 1 else
                       STATE_COLOUR[2] if nd["keyed"] else "#4a5866")
        sizes.append(3.5 if st == UNCHARTED
                     else round(5 + 13 * math.sqrt(t["deg"] / max_links), 2))
        opac.append(STATE_OPACITY[st])
        story = ["part of the mesh", "measured, no match yet",
                 "nothing to match on yet", "collected, not yet charted"][st]
        text.append(f"<b>{t['n']}</b><br>{t['dom'].replace('_',' ').lower()}"
                    f" · {t['rows']:,} records · {t['deg']} links · {story}"
                    f"<br>IDs: {', '.join(t['keys']) or 'none to match on'}"
                    "<br><span style='color:#9aa4b2'>click to open the dossier</span>"
                    "<extra></extra>")
    node_trace = {
        "type": "scattergl",
        "x": [p[0] for p in pos], "y": [p[1] for p in pos], "mode": "markers",
        "marker": {"color": colours, "size": sizes, "opacity": opac,
                   "line": {"width": [0.0] * n, "color": [LADDER_COLOUR[0]] * n}},
        "customdata": list(range(n)),
        "hovertemplate": "%{text}", "text": text,
        "name": "datasets", "showlegend": False,
    }

    # ---- furniture: ID wells (port of figures.furniture, connection view)
    shapes, notes = [], []
    for w in wells:
        r = 34 + math.sqrt(w["n"]) * 7
        shapes.append({"type": "circle", "x0": w["x"] - r, "y0": w["y"] - r,
                       "x1": w["x"] + r, "y1": w["y"] + r,
                       "fillcolor": "rgba(157,180,215,.07)",
                       "line": {"color": "rgba(157,180,215,.10)", "width": 1},
                       "layer": "below"})
        dx, dy = w["x"] - bw / 2, w["y"] - bh / 2
        d = math.hypot(dx, dy) or 1
        m = 1 + 92 / d
        notes.append({"x": bw / 2 + dx * m, "y": bh / 2 + dy * m,
                      "showarrow": False,
                      "text": f"<b>{w['k']}</b><br><span style='font-size:9px'>"
                              f"{w['h']} here · {w['n']} use it</span>",
                      "font": {"family": MONO, "size": 11, "color": INK_2}})

    # ---- editorial callouts, computed from the data itself
    name_ix = {t["n"]: i for i, t in enumerate(tables)}
    meta = lib["meta"]
    l3 = sum(1 for e in edges if e[2] == 3)
    pct = round(100 * l3 / len(edges))
    n_keyless = sum(1 for t in tables if t["state"] == 2)
    n_unch = sum(1 for t in tables if t["state"] == UNCHARTED)
    unch_rows = sum(t["rows"] or 0 for t in tables if t["state"] == UNCHARTED)
    all_rows = sum(t["rows"] or 0 for t in tables)
    ring_top = min(pos[i][1] for i, t in enumerate(tables) if t["state"] == UNCHARTED)

    def callout(x, y, txt, ax, ay, anchor="left"):
        notes.append({"x": x, "y": y, "ax": ax, "ay": ay,
                      "xanchor": anchor, "showarrow": True,
                      "arrowcolor": "rgba(232,234,237,.45)", "arrowwidth": 1,
                      "arrowhead": 0, "text": txt, "align": anchor,
                      "font": {"family": MONO, "size": 10.5, "color": INK},
                      "bgcolor": "rgba(15,22,32,.82)",
                      "bordercolor": "rgba(255,255,255,.14)", "borderpad": 5})

    for hub, label in ((meta["hubs"][0][0], "the biggest junction"),
                       (meta["hubs"][1][0], "the other junction")):
        i = name_ix.get(hub)
        if i is None:
            continue
        deg = tables[i]["deg"]
        short = hub.replace("FED_", "").replace("_", " ").title()
        left = pos[i][0] < bw / 2
        # label always points INWARD so it can't run off the plot edge
        callout(pos[i][0], pos[i][1],
                f"<b>{short}</b><br>{label} — {deg} links route through it",
                120 if left else -120, -60, "left" if left else "right")
    callout(bw / 2, bh / 2,
            f"<b>the void</b> — {n_keyless} datasets with no usable ID yet."
            "<br>nothing to join on; a better column is the fix",
            0, 120, "center")
    callout(bw / 2, ring_top,
            f"<b>the outer ring</b> — {n_unch} datasets queued for link discovery."
            f"<br>{unch_rows/1e6:.0f}M rows, {100*unch_rows/all_rows:.1f}% of the library — quiet, not missing",
            180, -34)
    # anchor the name+zip note on the NAME well if present
    wname = next((w for w in wells if w["k"] == "NAME"), None)
    if wname:
        callout(wname["x"], wname["y"],
                f"<b>name + place matches</b> — {l3:,} links, {pct}% of the mesh."
                "<br>reach, not proof: the thin pale lines",
                -250, 26, "right")

    pad = 120
    layout = {
        "paper_bgcolor": SURFACE, "plot_bgcolor": SURFACE,
        "margin": {"l": 4, "r": 4, "t": 4, "b": 4},
        "shapes": shapes, "annotations": notes, "showlegend": False,
        "hoverlabel": {"bgcolor": PANEL_2, "bordercolor": RULE, "align": "left",
                       "font": {"family": MONO, "size": 11, "color": INK}},
        "dragmode": "pan", "uirevision": "map",
        "xaxis": {"visible": False, "range": [-pad, bw + pad], "constrain": "domain"},
        "yaxis": {"visible": False, "range": [bh + pad * 0.6, -pad * 0.6]},
    }

    fig = {"data": link_traces + hl_traces + [halo_trace, node_trace],
           "layout": layout}

    # ---- aux for the JS layer
    neighbours = [[] for _ in range(n)]
    for ei, e in enumerate(edges):
        neighbours[e[0]].append(ei)
        neighbours[e[1]].append(ei)
    ladder_counts = [0] * 6
    for e in edges:
        ladder_counts[e[2]] += 1
    aux = {
        "pos": pos, "box": [bw, bh], "neighbours": neighbours,
        "baseOpac": opac, "ladderCounts": ladder_counts,
        "ladderColour": LADDER_COLOUR, "stateColour": STATE_COLOUR,
        "stateName": STATE_NAME, "stateStory": STATE_STORY,
        "stateOpacity": STATE_OPACITY,
    }
    return fig, aux


def main():
    fig, aux = build_map()
    data = build_payload()          # tables + column profiles + edges + ladder
    html = (TEMPLATE
            .replace("/*__PLOTLYJS__*/", get_plotlyjs())
            .replace("/*__FIG__*/", json.dumps(fig, separators=(",", ":")))
            .replace("/*__AUX__*/", json.dumps(aux, separators=(",", ":")))
            .replace("/*__DATA__*/", json.dumps(data, separators=(",", ":"))))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    n_traces = len(fig["data"])
    print(f"wrote {OUT} ({os.path.getsize(OUT)/1024/1024:.1f} MB) -- "
          f"{len(data['tables'])} tables, {len(data['edges'])} links, "
          f"{n_traces} traces (6 link tiers + 6 highlight + halo + nodes)")


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Library Map</title>
<style>
  :root{--surface:#0d1117;--panel:#0f1620;--panel2:#121a24;--panel3:#17202c;
    --ink:#e8eaed;--ink2:#9aa4b2;--ink3:#6b7684;--rule:rgba(255,255,255,.10);
    --amber:#eda748;--blue:#6da7ec}
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%;overflow:hidden}
  body{background:var(--surface);color:var(--ink);
    font:13.5px/1.5 ui-sans-serif,system-ui,"Segoe UI",sans-serif}
  .mono{font-family:ui-monospace,Consolas,monospace}

  #topbar{position:fixed;inset:0 0 auto 0;z-index:20;display:flex;gap:12px;
    align-items:center;padding:9px 14px;background:rgba(15,22,32,.92);
    border-bottom:1px solid var(--rule);backdrop-filter:blur(4px);flex-wrap:wrap}
  #topbar h1{font-size:14px;font-weight:600;letter-spacing:.05em;white-space:nowrap;cursor:pointer}
  #topbar h1 span{color:var(--amber)}
  #searchwrap{position:relative;flex:1 1 240px;max-width:430px}
  #q{width:100%;background:var(--panel3);border:1px solid var(--rule);border-radius:6px;
    color:var(--ink);padding:6px 12px;font-size:13.5px;outline:none}
  #q:focus{border-color:var(--amber)}
  #hits{position:absolute;top:calc(100% + 4px);left:0;right:0;background:var(--panel2);
    border:1px solid var(--rule);border-radius:6px;display:none;max-height:320px;
    overflow-y:auto;box-shadow:0 10px 30px rgba(0,0,0,.5)}
  #hits div{padding:6px 12px;cursor:pointer;font-family:ui-monospace,Consolas,monospace;
    font-size:12px;display:flex;justify-content:space-between;gap:10px}
  #hits div:hover,#hits div.hot{background:var(--panel3)}
  #hits .m{color:var(--ink3);font-size:11px;white-space:nowrap}
  select{background:var(--panel3);border:1px solid var(--rule);border-radius:6px;
    color:var(--ink2);padding:5px 8px;font-size:12px;outline:none;max-width:160px}
  .tgl{display:flex;gap:5px;align-items:center}
  .grade{font-size:10px;padding:3px 8px;border-radius:999px;color:#1a1206;font-weight:600;
    cursor:pointer;border:1px solid transparent;user-select:none;white-space:nowrap}
  .grade.off{background:transparent!important;color:var(--ink3);border-color:var(--rule);
    text-decoration:line-through}
  #home{background:var(--panel3);border:1px solid var(--rule);border-radius:6px;
    color:var(--ink2);padding:5px 12px;font-size:12px;cursor:pointer}
  #home:hover{border-color:var(--amber);color:var(--ink)}

  #map{position:fixed;inset:0}
  #map .js-plotly-plot,#map .plot-container{height:100%}

  /* how-to-read panel */
  #legend{position:fixed;left:14px;bottom:14px;z-index:15;width:280px;
    background:rgba(15,22,32,.92);border:1px solid var(--rule);border-radius:8px;
    backdrop-filter:blur(4px);font-size:12px}
  #legend header{padding:8px 12px;cursor:pointer;font-size:10.5px;letter-spacing:.18em;
    color:var(--ink3);text-transform:uppercase;display:flex;justify-content:space-between}
  #legend .body{padding:0 12px 10px;display:block}
  #legend.min .body{display:none}
  .lrow{display:flex;gap:8px;align-items:center;padding:2.5px 0;color:var(--ink2)}
  .lrow .sw{width:26px;height:0;border-top-style:solid;flex:none}
  .lrow b{color:var(--ink);font-weight:600;font-variant-numeric:tabular-nums;min-width:40px;text-align:right}
  .lrow .dot{width:8px;height:8px;border-radius:50%;flex:none;margin:0 9px}
  #legend .hint{color:var(--ink3);font-size:11px;margin-top:7px;border-top:1px solid var(--rule);padding-top:7px}

  /* dossier drawer */
  #drawer{position:fixed;top:0;right:0;bottom:0;width:400px;max-width:92vw;z-index:25;
    background:var(--panel);border-left:1px solid var(--rule);overflow-y:auto;
    padding:16px 20px 30px;transform:translateX(102%);transition:transform .22s ease}
  #drawer.open{transform:none}
  #drawer .close{position:sticky;top:0;float:right;background:var(--panel3);
    border:1px solid var(--rule);border-radius:6px;color:var(--ink2);width:28px;height:28px;
    cursor:pointer;font-size:14px;line-height:26px;text-align:center}
  #drawer .close:hover{color:var(--ink);border-color:var(--amber)}
  h2.tname{font-family:ui-monospace,Consolas,monospace;font-size:16px;font-weight:600;
    word-break:break-all;margin:4px 90px 0 0;padding-right:0}
  .badges{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0 4px}
  .badge{font-size:11px;padding:2px 9px;border-radius:999px;border:1px solid var(--rule);
    color:var(--ink2);background:var(--panel2)}
  .badge b{color:var(--ink)}
  .desc{color:var(--ink2);font-size:12.5px;margin:8px 0 2px}
  .story{color:var(--ink3);font-size:11.5px}
  h3.sect{font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink3);
    margin:20px 0 8px;border-bottom:1px solid var(--rule);padding-bottom:5px}
  h3.sect .n{color:var(--amber)}
  table.cols{border-collapse:collapse;width:100%;font-size:11.5px}
  table.cols th{font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink3);
    text-align:left;padding:3px 8px 3px 0;font-weight:500}
  table.cols td{padding:3px 8px 3px 0;border-top:1px solid rgba(255,255,255,.05)}
  table.cols td.c{font-family:ui-monospace,Consolas,monospace}
  table.cols td.k{color:var(--blue);white-space:nowrap}
  table.cols td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
  .fill{display:inline-block;width:40px;height:4px;border-radius:2px;background:var(--panel3);
    vertical-align:middle;margin-right:5px;overflow:hidden}
  .fill i{display:block;height:100%;background:var(--blue)}
  .lowfill i{background:#7a5a2f}
  .neigh{display:flex;gap:8px;align-items:baseline;padding:5px 0;
    border-top:1px solid rgba(255,255,255,.05);flex-wrap:wrap;font-size:12px}
  .neigh a{font-family:ui-monospace,Consolas,monospace;font-size:11.5px;color:var(--ink);
    text-decoration:none;cursor:pointer;word-break:break-all}
  .neigh a:hover{color:var(--amber)}
  .gchip{font-size:9.5px;padding:1px 7px;border-radius:999px;color:#1a1206;font-weight:600;white-space:nowrap}
  .gkey{font-family:ui-monospace,Consolas,monospace;font-size:10px;color:var(--ink3)}
</style>
</head>
<body>
<div id="map"></div>

<div id="topbar">
  <h1 onclick="clearSel();goHome()"><span>&#9670;</span> THE LIBRARY MAP</h1>
  <div id="searchwrap">
    <input id="q" type="search" placeholder="Search 1,043 datasets &mdash; name, description, column&hellip; ( / )" autocomplete="off">
    <div id="hits"></div>
  </div>
  <select id="fDom"><option value="">All shelves</option></select>
  <select id="fState"><option value="">Any presence</option></select>
  <div class="tgl" id="grades" title="The honesty dial — click a grade to hide it"></div>
  <button id="home" onclick="goHome()">&#8962; whole map</button>
</div>

<div id="legend">
  <header onclick="this.parentElement.classList.toggle('min')">
    <span>How to read this map</span><span>&#9650;</span>
  </header>
  <div class="body" id="legendbody"></div>
</div>

<div id="drawer"><button class="close" onclick="clearSel()">&times;</button><div id="dossier"></div></div>

<script>/*__PLOTLYJS__*/</script>
<script>
"use strict";
const FIG = /*__FIG__*/;
const AUX = /*__AUX__*/;
const DATA = /*__DATA__*/;

/* trace contract: 0-5 all-link tiers (weakest first), 6-11 highlight tiers
   (weakest first), 12 halo, 13 nodes. tier t -> link trace (5-t), hl (6+5-t). */
const T_LINK = t => 5 - t, T_HL = t => 11 - t, HALO = 12, NODES = 13;
const T = DATA.tables, E = DATA.edges, N = T.length;
const [BW, BH] = AUX.box;
const byName = new Map(T.map((t,i)=>[t.n,i]));
const hay = T.map(t=>(t.n+" "+t.desc+" "+t.keys.join(" ")+" "+t.cols.map(c=>c.c).join(" ")).toLowerCase());
const fmtRows = r => r>=1e6 ? (r/1e6).toFixed(1)+"M" : r.toLocaleString("en-US");
const gd = document.getElementById("map");

let sel = null;                     // selected table index
const gradesOn = new Set([0,1,2,3,4,5]);
let fDomV = "", fStateV = "";

Plotly.newPlot(gd, FIG.data, FIG.layout,
  {scrollZoom:true, displaylogo:false, responsive:true,
   modeBarButtonsToRemove:["select2d","lasso2d","autoScale2d","toImage"]});

/* ---------- selection ---------- */
function bez(a,b){                  // same bow the Python side draws
  const [x0,y0]=AUX.pos[a],[x1,y1]=AUX.pos[b];
  const mx=(x0+x1)/2,my=(y0+y1)/2,cx=mx+(BW/2-mx)*.16,cy=my+(BH/2-my)*.16;
  const xs=[],ys=[];
  for(const s of [0,.25,.5,.75,1]){
    xs.push((1-s)**2*x0+2*(1-s)*s*cx+s*s*x1);
    ys.push((1-s)**2*y0+2*(1-s)*s*cy+s*s*y1);
  }
  xs.push(null);ys.push(null);
  return [xs,ys];
}
function applyNodes(){
  /* node opacity = base x filter-dim x selection-dim; ring/width for selection */
  const focus=new Set();
  if(sel!=null){focus.add(sel);for(const ei of AUX.neighbours[sel]){focus.add(E[ei][0]);focus.add(E[ei][1]);}}
  const opac=new Array(N),width=new Array(N),ecol=new Array(N);
  for(let i=0;i<N;i++){
    let o=AUX.baseOpac[i];
    if(fDomV && T[i].dom!==fDomV) o*=0.14;
    if(fStateV!=="" && T[i].state!==+fStateV) o*=0.14;
    if(sel!=null && !focus.has(i)) o*=0.22;
    opac[i]=Math.round(o*1000)/1000;
    width[i]=i===sel?3:0;
    ecol[i]=i===sel?"#ffffff":AUX.ladderColour[0];
  }
  if(sel!=null) opac[sel]=1;
  Plotly.restyle(gd,{"marker.opacity":[opac],"marker.line.width":[width],
                     "marker.line.color":[ecol]},[NODES]);
}
function applyHighlight(){
  const ix=[],xs=[],ys=[];
  for(let t=0;t<6;t++){
    let X=[],Y=[];
    if(sel!=null && gradesOn.has(t)){
      for(const ei of AUX.neighbours[sel]){
        if(E[ei][2]!==t) continue;
        const [bx,by]=bez(E[ei][0],E[ei][1]);
        X=X.concat(bx);Y=Y.concat(by);
      }
    }
    ix.push(T_HL(t));xs.push(X);ys.push(Y);
  }
  Plotly.restyle(gd,{x:xs,y:ys},ix);
  Plotly.restyle(gd,{x:[sel!=null?[AUX.pos[sel][0]]:[]],
                     y:[sel!=null?[AUX.pos[sel][1]]:[]]},[HALO]);
}
const BASE_OP=[0.5,0.24,0.24,0.24,0.24,0.24]; // per tier, L0 first
function applyGrades(){
  const ix=[],vis=[],ops=[];
  /* while something is selected the whole base mesh steps back by ONE shared
     factor — uniform, so the ladder's ordering can never invert */
  const dim=sel!=null?0.35:1;
  for(let t=0;t<6;t++){ix.push(T_LINK(t));vis.push(gradesOn.has(t));
    ops.push(Math.round(BASE_OP[t]*dim*1000)/1000);}
  Plotly.restyle(gd,{visible:vis,opacity:ops},ix);
  applyHighlight();
  for(let t=0;t<6;t++)
    document.getElementById("g"+t).classList.toggle("off",!gradesOn.has(t));
}
function select(i,fly){
  sel=i;
  location.hash = i!=null ? "t="+encodeURIComponent(T[i].n) : "";
  applyNodes();applyGrades();
  if(i!=null){renderDossier(i);drawer.classList.add("open");
    if(fly){const [x,y]=AUX.pos[i];
      Plotly.animate(gd,{layout:{xaxis:{range:[x-300,x+300]},yaxis:{range:[y+180,y-180]}}},
        {transition:{duration:420,easing:"cubic-in-out"},frame:{duration:420}});}}
  else drawer.classList.remove("open");
}
function clearSel(){select(null,false);}
function goHome(){
  Plotly.animate(gd,{layout:{xaxis:{range:FIG.layout.xaxis.range.slice()},
                             yaxis:{range:FIG.layout.yaxis.range.slice()}}},
    {transition:{duration:480,easing:"cubic-in-out"},frame:{duration:480}});
}
gd.on("plotly_click",ev=>{
  const p=ev.points && ev.points.find(p=>p.curveNumber===NODES);
  if(p) select(p.customdata,false);
});

/* ---------- dossier drawer (adapted from the dictionary) ---------- */
const drawer=document.getElementById("drawer"),dossier=document.getElementById("dossier");
const gchip=t=>`<span class="gchip" style="background:${AUX.ladderColour[t]}">${DATA.ladder[t].name}</span>`;
function renderDossier(i){
  const t=T[i],st=t.state;
  let h=`<h2 class="tname">${t.n}</h2>`;
  h+=`<div class="badges">`+
     `<span class="badge" style="border-color:${AUX.stateColour[st]}"><b>${AUX.stateName[st]}</b></span>`+
     `<span class="badge">shelf: <b>${t.dom}</b></span>`+
     `<span class="badge"><b>${fmtRows(t.rows)}</b> rows</span>`+
     (t.keys.length?`<span class="badge">speaks: <b>${t.keys.join(", ")}</b></span>`:"")+`</div>`;
  if(t.desc) h+=`<p class="desc">${t.desc}</p>`;
  h+=`<p class="story">${AUX.stateStory[st]}</p>`;
  h+=`<h3 class="sect">ID columns profiled <span class="n">${t.cols.length}</span></h3>`;
  if(t.cols.length){
    h+=`<table class="cols"><tr><th>column</th><th>family</th><th>filled</th><th>distinct</th></tr>`;
    for(const c of t.cols){
      h+=`<tr><td class="c">${c.c}</td><td class="k">${c.k}</td>`+
         `<td class="num"><span class="fill${c.p<50?" lowfill":""}"><i style="width:${Math.max(2,c.p)}%"></i></span>${c.p}%</td>`+
         `<td class="num">${(c.d??"").toLocaleString?.("en-US")??c.d}</td></tr>`;
    }
    h+=`</table>`;
  } else h+=`<p class="story">No ID-bearing columns profiled.</p>`;
  const grp=new Map();
  for(const ei of AUX.neighbours[i]){
    const e=E[ei],j=e[0]===i?e[1]:e[0];
    if(!grp.has(j))grp.set(j,[]);
    grp.get(j).push(e);
  }
  const nn=[...grp.entries()].map(([j,ls])=>({j,ls,best:Math.min(...ls.map(l=>l[2]))}))
    .sort((a,b)=>a.best-b.best||b.ls.length-a.ls.length);
  h+=`<h3 class="sect">Verified connections <span class="n">${AUX.neighbours[i].length}</span>${nn.length?` links to <span class="n">${nn.length}</span> tables`:""}</h3>`;
  if(nn.length){
    for(const {j,ls} of nn){
      const parts=ls.sort((a,b)=>a[2]-b[2]).map(l=>gchip(l[2])+` <span class="gkey">${l[3]}</span>`).join(" ");
      h+=`<div class="neigh"><a onclick="select(${j},true)">${T[j].n}</a> ${parts}</div>`;
    }
    h+=`<p class="story" style="margin-top:8px">The lit lines on the map are these links — click any name to fly there.</p>`;
  } else {
    h+=`<p class="story">${st===1?"The search ran; nothing matched yet — a measured fact, on the follow-up list."
        :st===2?"Nothing to join on yet: no column carries a usable ID."
        :st===3?"Queued: link discovery hasn't run over this table yet."
        :"No links recorded."}</p>`;
  }
  dossier.innerHTML=h;
  drawer.scrollTop=0;
}

/* ---------- topbar: filters, grades, search ---------- */
const fDom=document.getElementById("fDom"),fState=document.getElementById("fState");
const doms=[...new Set(T.map(t=>t.dom))].sort();
fDom.innerHTML='<option value="">All shelves</option>'+doms.map(d=>`<option>${d}</option>`).join("");
fState.innerHTML='<option value="">Any presence</option>'+
  AUX.stateName.map((s,i)=>`<option value="${i}">${s}</option>`).join("");
fDom.onchange=()=>{fDomV=fDom.value;applyNodes();};
fState.onchange=()=>{fStateV=fState.value;applyNodes();};

const gradesEl=document.getElementById("grades");
gradesEl.innerHTML=DATA.ladder.map((l,t)=>
  `<span class="grade" id="g${t}" style="background:${AUX.ladderColour[t]}"
    title="${l.gloss}">${l.name} ${AUX.ladderCounts[t]}</span>`).join("");
for(let t=0;t<6;t++)
  document.getElementById("g"+t).onclick=()=>{
    gradesOn.has(t)?gradesOn.delete(t):gradesOn.add(t);applyGrades();};

const qEl=document.getElementById("q"),hits=document.getElementById("hits");
let hitIdx=[],hot=0;
function doSearch(){
  const q=(qEl.value||"").toLowerCase().trim();
  if(!q){hits.style.display="none";hitIdx=[];return;}
  hitIdx=[];
  for(let i=0;i<N && hitIdx.length<400;i++) if(hay[i].includes(q)) hitIdx.push(i);
  hitIdx.sort((a,b)=>(T[a].state-T[b].state)||(T[b].rows-T[a].rows));
  hitIdx=hitIdx.slice(0,12);hot=0;
  hits.innerHTML=hitIdx.map((i,k)=>
    `<div class="${k===0?"hot":""}" onclick="pick(${i})">${T[i].n}`+
    `<span class="m">${T[i].dom} · ${fmtRows(T[i].rows)}${T[i].state===0?" · "+AUX.neighbours[i].length+"&#8599;":""}</span></div>`).join("");
  hits.style.display=hitIdx.length?"block":"none";
}
function pick(i){hits.style.display="none";qEl.blur();select(i,true);}
qEl.addEventListener("input",doSearch);
qEl.addEventListener("keydown",e=>{
  if(e.key==="Enter" && hitIdx.length) pick(hitIdx[hot]);
  else if(e.key==="ArrowDown"||e.key==="ArrowUp"){
    e.preventDefault();
    hot=e.key==="ArrowDown"?Math.min(hitIdx.length-1,hot+1):Math.max(0,hot-1);
    [...hits.children].forEach((el,k)=>el.classList.toggle("hot",k===hot));
  }
});
document.addEventListener("click",e=>{if(!e.target.closest("#searchwrap"))hits.style.display="none";});
document.addEventListener("keydown",e=>{
  if(e.key==="/" && document.activeElement!==qEl){e.preventDefault();qEl.focus();qEl.select();}
  else if(e.key==="Escape"){qEl.value="";hits.style.display="none";clearSel();}
});

/* ---------- legend ---------- */
const widths=[3,2.6,2.2,1.6,1.2,1];
document.getElementById("legendbody").innerHTML=
  DATA.ladder.map((l,t)=>
    `<div class="lrow"><span class="sw" style="border-top-width:${widths[t]}px;border-top-color:${AUX.ladderColour[t]}"></span><b>${AUX.ladderCounts[t].toLocaleString()}</b><span>${l.name}</span></div>`).join("")+
  `<div style="height:6px"></div>`+
  AUX.stateName.map((s,i)=>{
    const c=T.filter(t=>t.state===i).length;
    return `<div class="lrow"><span class="dot" style="background:${AUX.stateColour[i]};opacity:${AUX.stateOpacity[i]}"></span><b>${c}</b><span>${s}</span></div>`;}).join("")+
  `<div class="hint">Bigger dot = more links. Bright dots carry 2+ rare IDs — the crossings.
   Click anything; <span class="mono">/</span> to search; scroll to zoom; Esc steps back.
   Every link was verified; a person signs every finding.</div>`;

/* ---------- routing ---------- */
window.addEventListener("hashchange",()=>{
  const m=location.hash.match(/t=([^&]+)/);
  const i=m?byName.get(decodeURIComponent(m[1])):null;
  if((i??null)!==sel) select(i??null,true);
});
const m0=location.hash.match(/t=([^&]+)/);
if(m0){const i=byName.get(decodeURIComponent(m0[1]));if(i!=null)select(i,true);}
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
