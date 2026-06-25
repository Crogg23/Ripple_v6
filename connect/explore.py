"""Render the interactive connection explorer.

Takes the real edge-list from discover and draws it: every connected dataset is
a node (sized by row count, colored by investigation domain); every REAL
connection is an edge (width by how many rows actually matched, color by trust
tier). Hover an edge to see the key, the match count/rate and a sample. Below the
map, a sortable/filterable table of every connection so you can scan and rank.

Plotly only (the fixed stack). Self-contained HTML — double-click to open.

Run:  python -m connect.explore
"""

from __future__ import annotations

import html
import json
import math
import random
from pathlib import Path

import plotly.graph_objects as go

from .discover import GRAPH_OUT

OUT = Path(__file__).resolve().parents[1] / "outputs" / "connection_explorer.html"

TIER_STYLE = {  # trust tier -> (color, label)
    "STEEL": ("#f4c20d", "STEEL · hard entity ID"),
    "STRONG": ("#4da6ff", "STRONG · domain ID"),
    "BRIDGE": ("#e879f9", "BRIDGE · via a hop (crosswalk)"),
    "CORROBORATED": ("#22d3ee", "CORROBORATED · name + place"),
    "GEO": ("#36c98a", "GEO · place / spatial"),
    "PROBABILISTIC": ("#9aa0a6", "PROBABILISTIC · name / address"),
}
DOMAIN_COLOR = {
    "health": "#ff6b6b", "justice": "#845ef7", "economics": "#20c997",
    "foreign_influence": "#ff922b", "governance": "#4dabf7", "maritime": "#15aabf",
    "hazards": "#fab005", "housing": "#f783ac", "corporate_registry": "#a9e34b",
    "history": "#e8a87c", "other": "#868e96",
}


def _spring_layout(nodes, elist, iters=240, seed=7):
    rnd = random.Random(seed)
    pos = {n: [rnd.uniform(-1, 1), rnd.uniform(-1, 1)] for n in nodes}
    n = len(nodes)
    if n <= 1:
        return pos
    k = math.sqrt(1.0 / n)
    temp = 0.12
    for _ in range(iters):
        disp = {x: [0.0, 0.0] for x in nodes}
        for i in range(n):
            a = nodes[i]
            for j in range(i + 1, n):
                b = nodes[j]
                dx, dy = pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]
                d = math.hypot(dx, dy) or 0.01
                f = k * k / d
                ux, uy = dx / d, dy / d
                disp[a][0] += ux * f; disp[a][1] += uy * f
                disp[b][0] -= ux * f; disp[b][1] -= uy * f
        for a, b, w in elist:
            dx, dy = pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]
            d = math.hypot(dx, dy) or 0.01
            f = d * d / k * (0.4 + w)
            ux, uy = dx / d, dy / d
            disp[a][0] -= ux * f; disp[a][1] -= uy * f
            disp[b][0] += ux * f; disp[b][1] += uy * f
        for x in nodes:
            dx, dy = disp[x]
            d = math.hypot(dx, dy) or 0.01
            pos[x][0] += dx / d * min(d, temp)
            pos[x][1] += dy / d * min(d, temp)
        temp = max(0.01, temp * 0.985)
    return pos


def _short(table: str) -> str:
    return table.replace("FED_", "").replace("INTL_", "").replace("XC_", "").replace("_", " ").title()


def build_figure(graph: dict) -> go.Figure:
    edges = graph["edges"]
    nodes_by_id = {n["id"]: n for n in graph["nodes"]}
    connected = sorted({e["a"] for e in edges} | {e["b"] for e in edges})

    max_m = max((e["matched"] for e in edges), default=1)
    elist = [(e["a"], e["b"], math.log1p(e["matched"]) / math.log1p(max_m)) for e in edges]
    pos = _spring_layout(connected, elist)

    fig = go.Figure()

    # --- edges, grouped by tier (one trace each so the legend filters by trust)
    for tier, (color, label) in TIER_STYLE.items():
        tedges = [e for e in edges if e["tier"] == tier]
        if not tedges:
            continue
        xs, ys, hx, hy, htext = [], [], [], [], []
        for e in tedges:
            a, b = e["a"], e["b"]
            xs += [pos[a][0], pos[b][0], None]
            ys += [pos[a][1], pos[b][1], None]
            hx.append((pos[a][0] + pos[b][0]) / 2)
            hy.append((pos[a][1] + pos[b][1]) / 2)
            mode = "in" if e["mode"] == "spatial" else "↔"
            via = f"via {_short(e['via'])} ({e.get('hop','')})<br>" if e.get("via") else ""
            htext.append(
                f"<b>{_short(a)} {mode} {_short(b)}</b><br>"
                f"key: {e['key']} ({tier}) · confidence {e.get('confidence', 0)}<br>"
                f"{via}"
                f"<b>{e['matched']:,}</b> matched · {e['match_rate']}% overlap<br>"
                + (f"e.g. {', '.join(map(str, e['sample'][:4]))}" if e.get("sample") else "")
            )
        width = 1.5 if tier in ("PROBABILISTIC",) else 2.5
        dash = "dot" if tier == "PROBABILISTIC" else ("dash" if tier in ("GEO", "BRIDGE") else "solid")
        fig.add_trace(go.Scatter(
            x=xs, y=ys, mode="lines", line=dict(color=color, width=width, dash=dash),
            opacity=0.55 if tier == "PROBABILISTIC" else 0.8, hoverinfo="skip",
            name=label, legendgroup=tier,
        ))
        fig.add_trace(go.Scatter(
            x=hx, y=hy, mode="markers", marker=dict(size=10, color=color, opacity=0.001),
            hoverinfo="text", hovertext=htext, showlegend=False, legendgroup=tier,
        ))

    # --- nodes
    deg = {n: 0 for n in connected}
    for e in edges:
        deg[e["a"]] += 1; deg[e["b"]] += 1
    nx, ny, nsize, ncolor, ntext, nhover = [], [], [], [], [], []
    for nid in connected:
        nd = nodes_by_id[nid]
        nx.append(pos[nid][0]); ny.append(pos[nid][1])
        nsize.append(14 + 6 * math.log10(max(nd["rows"], 10)))
        ncolor.append(DOMAIN_COLOR.get(nd["domain"], "#868e96"))
        ntext.append(_short(nid))
        conns = sorted([e for e in edges if nid in (e["a"], e["b"])],
                       key=lambda e: -e["matched"])[:6]
        clines = "<br>".join(
            f"  • {e['key']} {('in ' if e['mode']=='spatial' else '↔ ')}"
            f"{_short(e['b'] if e['a']==nid else e['a'])}: {e['matched']:,}"
            for e in conns)
        nhover.append(
            f"<b>{_short(nid)}</b>  ({nd['domain']})<br>"
            f"{nd['rows']:,} rows · {deg[nid]} connections<br>"
            f"keys: {', '.join(nd['keys'])}<br>—<br>{clines}"
        )
    fig.add_trace(go.Scatter(
        x=nx, y=ny, mode="markers+text", text=ntext, textposition="top center",
        textfont=dict(color="#e8eaed", size=10),
        marker=dict(size=nsize, color=ncolor, line=dict(color="#0d1117", width=1.5)),
        hoverinfo="text", hovertext=nhover, showlegend=False,
    ))

    fig.update_layout(
        title=dict(text="Ripple — Real Connection Map  ·  edges = rows that actually join",
                   font=dict(color="#e8eaed", size=20), x=0.02),
        paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
        showlegend=True, legend=dict(font=dict(color="#e8eaed"), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        hoverlabel=dict(bgcolor="#161b22", font=dict(color="#e8eaed", size=12)),
        margin=dict(l=10, r=10, t=50, b=10), height=720,
    )
    return fig


def _table_html(graph: dict) -> str:
    rows = []
    for e in graph["edges"]:
        color = TIER_STYLE.get(e["tier"], ("#888",))[0]
        mode = "in" if e["mode"] == "spatial" else "↔"
        samp = html.escape(", ".join(map(str, e.get("sample", [])[:4])))
        rows.append(
            f"<tr data-tier='{e['tier']}'>"
            f"<td><span class='badge' style='background:{color}'>{e['tier']}</span></td>"
            f"<td>{e['key']}</td>"
            f"<td>{_short(e['a'])} <span class='m'>{mode}</span> {_short(e['b'])}</td>"
            f"<td class='num'>{e['matched']:,}</td>"
            f"<td class='num'>{e['match_rate']}%</td>"
            f"<td class='num'>{e.get('confidence', 0)}</td>"
            f"<td class='samp'>{samp}</td></tr>"
        )
    return "\n".join(rows)


def render(graph: dict | None = None, open_browser: bool = True) -> Path:
    graph = graph or json.loads(GRAPH_OUT.read_text())
    fig = build_figure(graph)
    plot_div = fig.to_html(full_html=False, include_plotlyjs=True, config={"displaylogo": False})

    m = graph["meta"]
    unconnected = sorted(n["id"] for n in graph["nodes"]
                         if n["id"] not in {e["a"] for e in graph["edges"]}
                         and n["id"] not in {e["b"] for e in graph["edges"]})
    page = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Ripple — Connection Explorer</title>
<style>
  body{{background:#0d1117;color:#e8eaed;font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:0;padding:0 24px 60px}}
  h1{{font-size:22px;margin:18px 0 2px}} .sub{{color:#9aa0a6;margin:0 0 14px;font-size:13px}}
  .wrap{{max-width:1200px;margin:0 auto}}
  table{{border-collapse:collapse;width:100%;font-size:13px;margin-top:8px}}
  th,td{{padding:7px 10px;border-bottom:1px solid #21262d;text-align:left}}
  th{{cursor:pointer;color:#9aa0a6;user-select:none;position:sticky;top:0;background:#0d1117}}
  td.num{{text-align:right;font-variant-numeric:tabular-nums}} td.samp{{color:#9aa0a6;font-size:11px}}
  .m{{color:#9aa0a6}} .badge{{color:#0d1117;font-weight:700;padding:1px 7px;border-radius:9px;font-size:11px}}
  #q{{background:#161b22;border:1px solid #30363d;color:#e8eaed;padding:7px 10px;border-radius:6px;width:280px;margin-right:8px}}
  .pill{{display:inline-block;background:#161b22;border:1px solid #30363d;padding:3px 9px;border-radius:12px;margin:2px;font-size:11px;color:#9aa0a6}}
</style></head><body><div class="wrap">
<h1>Ripple — Connection Explorer</h1>
<p class="sub">{len(graph['nodes'])} datasets · <b>{m['edges']} real connections</b> from {m['pairs_tested']} pairs tested
({m.get('gated_out', 0)} flukes gated out, {m['pairs_skipped']} skipped). Edge = rows that actually join, scored by confidence (0–1). Hover the map; sort/filter the table.</p>
{plot_div}
<h1 style="font-size:17px;margin-top:26px">Every connection, ranked</h1>
<p class="sub">Type to filter (dataset, key, tier). Click a header to sort.
Looking for a specific person/company/facility? Resolve it with
<code>python -m connect dossier --q "name"</code> (or <code>--npi/--ccn/--ein</code>).</p>
<input id="q" placeholder="filter… e.g. NPI, LEIE, STEEL">
<table id="t"><thead><tr>
  <th>Tier</th><th>Key</th><th>Connection</th><th class="num">Matched</th><th class="num">Rate</th><th class="num">Conf</th><th>Sample</th>
</tr></thead><tbody>
{_table_html(graph)}
</tbody></table>
<h1 style="font-size:15px;margin-top:26px">No connection found yet ({len(unconnected)})</h1>
<p class="sub">Landed, but no shared live key with another source — candidates for a bridge/crosswalk later.</p>
<div>{''.join(f'<span class="pill">{_short(u)}</span>' for u in unconnected)}</div>
</div>
<script>
const q=document.getElementById('q'), t=document.getElementById('t');
q.addEventListener('input',()=>{{const v=q.value.toLowerCase();
  for(const r of t.tBodies[0].rows) r.style.display = r.innerText.toLowerCase().includes(v)?'':'none';}});
for(const [i,th] of [...t.tHead.rows[0].cells].entries()){{
  th.addEventListener('click',()=>{{
    const num=i>=3&&i<=5, rs=[...t.tBodies[0].rows];
    const dir=th.dataset.d=th.dataset.d==='1'?'':'1';
    rs.sort((a,b)=>{{let x=a.cells[i].innerText,y=b.cells[i].innerText;
      if(num){{x=parseFloat(x.replace(/[^0-9.]/g,''))||0;y=parseFloat(y.replace(/[^0-9.]/g,''))||0;return dir?y-x:x-y;}}
      return dir?y.localeCompare(x):x.localeCompare(y);}});
    rs.forEach(r=>t.tBodies[0].appendChild(r));}});
}}
</script></body></html>"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT}")
    if open_browser:
        try:
            import webbrowser
            webbrowser.open(OUT.resolve().as_uri())
            print("opened in your browser")
        except Exception:
            print(f"open it manually: {OUT}")
    return OUT


if __name__ == "__main__":
    render()
