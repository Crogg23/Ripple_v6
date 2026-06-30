"""The connection graph, rendered LIVE from the cached artifact — retiring the
17MB frozen outputs/connection_explorer.html.

The hard rule (connect/cache_layout.py): the x/y are already baked onto every
connected node. We READ them and draw with WebGL (scattergl) — we never recompute
the O(n^2) spring layout (that recompute IS the 17MB/slow bug). The 82 isolated
nodes carry no x/y by design; we park them in a reserved gutter, never fabricate
organic coordinates.

Edges are drawn as ONE scattergl line trace PER TIER (<=6 traces total) using flat
x/y arrays with None separators — not 20,696 individual traces. Default view =
STEEL+STRONG+BRIDGE, portal samples hidden, with toggles for the rest.

`focus=[table,...]` (the dossier \"jump into the graph\") builds an ego graph: the
entity's member-table nodes + their 1-hop neighbors, with the focus nodes ringed.
Graph nodes are SOURCE tables, so a node click opens that source's page.
"""

from __future__ import annotations

import hashlib
import json
import numbers
import os
from datetime import datetime
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

ALL_TIERS = ["STEEL", "STRONG", "BRIDGE", "CORROBORATED", "GEO", "PROBABILISTIC"]
DEFAULT_TIERS = ["STEEL", "STRONG", "BRIDGE"]

# Tier styling (reuses the connect-engine TIER_RGB intent: strongest = brightest).
TIER_RGB = {
    "STEEL": "#ffd24d", "STRONG": "#f4a23a", "BRIDGE": "#c08bf0",
    "CORROBORATED": "#36c98a", "GEO": "#3a7bd5", "PROBABILISTIC": "#566270",
}
TIER_WIDTH = {"STEEL": 1.6, "BRIDGE": 1.6, "STRONG": 0.9,
              "CORROBORATED": 0.7, "GEO": 0.5, "PROBABILISTIC": 0.4}
TIER_OPACITY = {"STEEL": 0.9, "BRIDGE": 0.9, "STRONG": 0.55,
                "CORROBORATED": 0.5, "GEO": 0.28, "PROBABILISTIC": 0.22}
# weak -> strong so the steel/bridge edges land on top
TIER_Z = {"GEO": 0, "PROBABILISTIC": 1, "CORROBORATED": 2, "STRONG": 3, "BRIDGE": 4, "STEEL": 5}

BG = "#0d1117"
FG = "#e6edf3"

_PALETTE = ["#4c9aff", "#36c98a", "#f4a23a", "#e5534b", "#b07cf0", "#3ab0c4",
            "#f778ba", "#d29922", "#56d364", "#79c0ff", "#ffa657", "#a5d6ff"]


def graph_path() -> Path:
    env = os.getenv("RIPPLE_GRAPH_PATH")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[1] / "outputs" / "connect_graph.json"


@st.cache_data(ttl=3600, show_spinner="Loading the connection graph…")
def load_graph():
    p = graph_path()
    g = json.loads(p.read_text())
    asof = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d")
    return g, asof


def _domain_color(domain: str) -> str:
    if not domain:
        return "#6e7681"
    # Stable across process restarts: built-in hash() is salted per PYTHONHASHSEED,
    # which would reshuffle the legend colors on every app restart.
    return _PALETTE[int(hashlib.md5(domain.encode()).hexdigest(), 16) % len(_PALETTE)]


def build_figure(graph: dict, *, tiers, include_samples: bool,
                 focus=None, enrich=None, asof=None) -> go.Figure:
    enrich = enrich or {}
    tiers = set(tiers) & set(ALL_TIERS) or set(DEFAULT_TIERS)
    nodes_by_id = {n["id"]: n for n in graph["nodes"]}
    focus = [f for f in (focus or []) if f in nodes_by_id]

    # ---- which edges / nodes are visible -----------------------------------
    if focus:
        fset = set(focus)
        edges = [e for e in graph["edges"]
                 if e["tier"] in tiers and (e["a"] in fset or e["b"] in fset)]
        visible = set(focus)
        for e in edges:
            visible.add(e["a"]); visible.add(e["b"])
        edges = [e for e in edges if e["a"] in visible and e["b"] in visible]
    else:
        visible = set(nodes_by_id)
        if not include_samples:
            visible = {i for i in visible if not i.startswith("PORTAL")}
        edges = [e for e in graph["edges"]
                 if e["tier"] in tiers and e["a"] in visible and e["b"] in visible]

    # ---- positions: read baked x/y; gutter the isolated --------------------
    pos = {}
    for nid in visible:
        n = nodes_by_id[nid]
        if n.get("x") is not None and n.get("y") is not None:
            pos[nid] = (n["x"], n["y"])
    placed = list(pos.values())
    # No baked x/y on any visible node -> the artifact shipped without a cached
    # layout. Surface it loudly instead of silently stacking all 764 nodes in the
    # gutter column (which reads as one vertical line, not a graph).
    if not placed:
        st.warning("Graph layout not cached — run: python3 -m connect.cache_layout")
    if placed:
        xs = [p[0] for p in placed]; ys = [p[1] for p in placed]
        minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    else:
        minx = maxx = miny = maxy = 0.0
    span_x = (maxx - minx) or 1.0
    span_y = (maxy - miny) or 1.0
    gutter_x = minx - 0.16 * span_x
    isolated = sorted(nid for nid in visible if nid not in pos)
    for i, nid in enumerate(isolated):
        step = span_y / max(len(isolated) - 1, 1) if len(isolated) > 1 else 0
        pos[nid] = (gutter_x, maxy - i * step)

    # ---- degree (for node size) --------------------------------------------
    degree = {nid: 0 for nid in visible}
    for e in edges:
        degree[e["a"]] = degree.get(e["a"], 0) + 1
        degree[e["b"]] = degree.get(e["b"], 0) + 1

    fig = go.Figure()

    # ---- edges: one scattergl trace per tier (None-separated segments) ------
    for tier in sorted(tiers, key=lambda t: TIER_Z.get(t, 0)):
        ex, ey = [], []
        for e in edges:
            if e["tier"] != tier:
                continue
            if e["a"] not in pos or e["b"] not in pos:
                continue
            ax, ay = pos[e["a"]]; bx, by = pos[e["b"]]
            ex += [ax, bx, None]; ey += [ay, by, None]
        if not ex:
            continue
        fig.add_trace(go.Scattergl(
            x=ex, y=ey, mode="lines", name=f"{tier} ({sum(1 for e in edges if e['tier']==tier)})",
            line=dict(color=TIER_RGB[tier], width=TIER_WIDTH[tier]),
            opacity=TIER_OPACITY[tier], hoverinfo="skip",
        ))

    # ---- nodes: context vs focus -------------------------------------------
    def _node_trace(ids, *, ring, base_size, name, showlegend):
        nx, ny, color, size, cd, hov = [], [], [], [], [], []
        for nid in ids:
            x, y = pos[nid]
            meta = enrich.get(nid.lower(), {})
            dom = meta.get("domain") or nodes_by_id[nid].get("domain") or "other"
            rows = meta.get("rows")
            rows = rows if rows is not None else nodes_by_id[nid].get("rows")
            keys = ", ".join(nodes_by_id[nid].get("keys", []))
            nx.append(x); ny.append(y); color.append(_domain_color(dom))
            size.append(min(base_size + 1.6 * degree.get(nid, 0) ** 0.5, base_size + 16))
            cd.append(nid)
            hov.append(f"<b>{nid}</b><br>{meta.get('name','') or ''}"
                       f"<br>domain: {dom}<br>rows: {int(rows):,}" if isinstance(rows, numbers.Number)
                       else f"<b>{nid}</b><br>domain: {dom}")
            hov[-1] += f"<br>keys: {keys}" if keys else ""
            hov[-1] += f"<br>degree: {degree.get(nid,0)}"
        fig.add_trace(go.Scattergl(
            x=nx, y=ny, mode="markers", name=name, showlegend=showlegend,
            marker=dict(size=size, color=(FG if ring else color),
                        line=dict(color=("#ffffff" if ring else BG), width=(2.4 if ring else 0.5)),
                        symbol="circle"),
            customdata=cd, hoverinfo="text", hovertext=hov,
        ))

    fset = set(focus)
    context_ids = [nid for nid in pos if nid not in fset]
    if context_ids:
        _node_trace(context_ids, ring=False, base_size=6, name="sources", showlegend=False)
    if focus:
        _node_trace(list(fset), ring=True, base_size=13, name="this entity's sources", showlegend=True)

    # ---- gutter + as-of annotations ----------------------------------------
    if isolated:
        fig.add_annotation(x=gutter_x, y=maxy + 0.06 * span_y, xref="x", yref="y",
                           text="islands (no measured link)", showarrow=False,
                           font=dict(color="#8b949e", size=10), xanchor="center")
    title = "Connection graph"
    if focus:
        title = f"Connection neighborhood · {len(focus)} source(s) for this entity"
    sub = f"as of {asof}  ·  {len(edges):,} edges · {len(pos):,} sources shown"
    fig.update_layout(
        title=dict(text=f"{title}<br><span style='font-size:12px;color:#8b949e'>{sub}</span>",
                   font=dict(color=FG, size=18), x=0.01, xanchor="left"),
        paper_bgcolor=BG, plot_bgcolor=BG,
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        legend=dict(font=dict(color=FG, size=11), bgcolor="rgba(0,0,0,0)",
                    orientation="h", y=-0.04),
        hoverlabel=dict(bgcolor="#161b22", font=dict(color=FG, size=12)),
        margin=dict(l=10, r=10, t=64, b=30), height=680, dragmode="pan",
    )
    return fig
