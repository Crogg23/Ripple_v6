"""
The Library Atlas -- Plotly + Dash.

    python -m viz.atlas_app          then open http://127.0.0.1:8050

Same map as docs/library-atlas.html, rebuilt so that everything you might want
to change is Python you can read. There is no JavaScript in this file. Click a
dataset and the side panel is built by `dossier()` a few screens down; change
what it says by editing that function.

THE THREE ARRANGEMENTS
    by subject      datasets in rooms with others about the same thing
    by connection   datasets pulled toward the ID they're identified by
    by journey      left to right in the order things actually run

They share one set of coordinates per dataset, worked out ahead of time by
viz/compile_anatomy.py. That means a dataset keeps its identity and simply
MOVES when you change the arrangement -- which is the point. Any one
arrangement is an argument about what matters; being able to flip between them
stops any single one posing as the truth.

WHERE THE DATA COMES FROM
    outputs/anatomy.json   built by:  python -m viz.compile_anatomy
Nothing here talks to Snowflake. Nothing here needs the internet.
"""

from __future__ import annotations

import json
import math
import pathlib

import plotly.graph_objects as go
from dash import ALL, Dash, Input, Output, State, ctx, dcc, html, no_update

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "outputs" / "anatomy.json"

# ---------------------------------------------------------------- the palette
#
# How sure we are that a link is real. ONE colour that simply gets dimmer as we
# get less sure, so a hunch can never be drawn as loudly as a certainty. The
# order is fixed and meaningful -- strongest first -- and must not be shuffled.
LADDER_COLOUR = ["#fbc06a", "#eda748", "#d98d33", "#bd7327", "#9d5c1e", "#7d4818"]

# The five steps data goes through, getting brighter as it becomes more useful.
STAGE_COLOUR = ["#256abf", "#3987e5", "#6da7ec", "#9ec5f4", "#cde2fb"]
STAGE_ORDER = ["intake", "staging", "bridge", "shelf", "desk"]

SURFACE = "#0d1117"
PANEL = "#0f1620"
PANEL_2 = "#121a24"
INK = "#e8eaed"
INK_2 = "#9aa4b2"
INK_3 = "#6b7684"
RULE = "rgba(255,255,255,.10)"
MONO = "ui-monospace, SFMono-Regular, Consolas, monospace"
SANS = 'ui-sans-serif, system-ui, "Segoe UI", sans-serif'

# An ID only tells you something if it's rare. Nearly every dataset carries a
# name and a ZIP code, so those two can't pick out anything on their own.
COMMON_ID_CUTOFF = 45


# ------------------------------------------------------------------- the data


def load():
    if not DATA.exists():
        raise SystemExit(
            f"{DATA} is missing.\nBuild it first:  python -m viz.compile_anatomy")
    return json.loads(DATA.read_text(encoding="utf-8"))


A = load()
TABLES = A["tables"]
EDGES = A["edges"]
LADDER = A["ladder_labels"]          # [[short name, what it means], ...]
STAGES = {s["id"]: s for s in A["stages"]}
LAY = A["layouts"]
BOX_W, BOX_H = LAY["stacks"]["box"]
N = len(TABLES)

# How many datasets carry each kind of ID -- used to tell a discriminating ID
# from one that everything has.
ID_USAGE: dict[str, int] = {}
for _t in TABLES:
    for _k in _t["keys"]:
        ID_USAGE[_k] = ID_USAGE.get(_k, 0) + 1


def is_rare(key: str) -> bool:
    return ID_USAGE.get(key, 0) <= COMMON_ID_CUTOFF


# Which datasets each one links to, so a click can answer instantly.
NEIGHBOURS: list[list[int]] = [[] for _ in range(N)]
for _i, _e in enumerate(EDGES):
    NEIGHBOURS[_e[0]].append(_i)
    NEIGHBOURS[_e[1]].append(_i)

# Where the pipeline puts each dataset, and what runs after what.
REF = LAY["refinery"]
SEAT = A["xref"]                                    # dataset -> seat on the line
KIDS: list[list[int]] = [[] for _ in REF["nodes"]]
PARENTS: list[list[int]] = [[] for _ in REF["nodes"]]
for _a, _b in REF["links"]:
    KIDS[_a].append(_b)
    PARENTS[_b].append(_a)

CELL = {c["i"]: c for c in LAY["stacks"]["cells"]}
MAX_LINKS = max(1, max(t["deg"] for t in TABLES))


def positions(view: str) -> list[tuple[float, float]]:
    """Where every dataset sits under one arrangement. Same order every time."""
    if view == "subject":
        return [(CELL[i]["x"] + CELL[i]["w"] / 2, CELL[i]["y"] + CELL[i]["h"] / 2)
                for i in range(N)]
    if view == "connection":
        return [(n["x"], n["y"]) for n in LAY["constellation"]["nodes"]]
    out = []
    for i in range(N):
        seat = SEAT[i]
        if seat >= 0:
            out.append((REF["nodes"][seat]["x"], REF["nodes"][seat]["y"]))
        else:
            # Measured, but never wired into the build, so it has no seat on the
            # line. Parked at the foot of the first bank rather than invented.
            band = next(b for b in REF["bands"] if b["id"] == "intake")
            out.append((band["x"] + band["w"] * (0.3 + 0.4 * (i % 2)), BOX_H - 14))
    return out


POS = {v: positions(v) for v in ("subject", "connection", "journey")}

VIEW_BLURB = {
    "subject": ("Arranged by subject",
                "Every dataset, in a room with the others about the same thing. "
                "Bigger room, more datasets. Bigger tile, more records inside it."),
    "connection": ("Arranged by what connects to what",
                   "Two datasets can only be linked if they share an ID. Each one "
                   "sits beside the ID it's identified by; the bright ones between "
                   "two wells carry two rare IDs, and those are what let a question "
                   "travel from one world to another."),
    "journey": ("Arranged by the journey data takes",
                "Left to right is the order things actually happen: raw files land, "
                "get tidied up, a few get combined, most become ready to use, and a "
                "handful end up in a queue for a person."),
}


# ------------------------------------------------------------------- drawing
#
# Each function below returns Plotly pieces. Edit these to change how the map
# looks -- nothing else needs to know.


def link_traces(view, tiers_on, highlight=None):
    """One trace per kind of link.

    All the segments of one kind go into a SINGLE trace, separated by None --
    that's the trick that keeps thousands of lines to a handful of traces
    instead of thousands of them.

    Because each kind is its own trace it gets its own legend entry, and
    clicking that entry hides it. That legend is the honesty dial: it's how you
    strip the map back to only the links we're certain about.
    """
    pos = POS[view]
    out = []
    # Weakest first so the certain links are stroked last and land on top. The
    # legend is then reversed, so a reader still sees strongest first.
    for tier in range(len(LADDER) - 1, -1, -1):
        xs, ys = [], []
        for e in EDGES:
            if e[2] != tier:
                continue
            if highlight is not None and highlight not in (e[0], e[1]):
                continue
            (x0, y0), (x1, y1) = pos[e[0]], pos[e[1]]
            if view == "journey":
                # Every link here sits inside one bank, so bowing toward the
                # middle would drag it across unrelated stages.
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 - abs(y1 - y0) * 0.22
            else:
                mx, my = (x0 + x1) / 2, (y0 + y1) / 2
                cx = mx + (BOX_W / 2 - mx) * 0.16
                cy = my + (BOX_H / 2 - my) * 0.16
            # A few points along the curve, so links fan out instead of
            # stacking into one illegible bar.
            for s in (0.0, 0.25, 0.5, 0.75, 1.0):
                xs.append((1 - s) ** 2 * x0 + 2 * (1 - s) * s * cx + s * s * x1)
                ys.append((1 - s) ** 2 * y0 + 2 * (1 - s) * s * cy + s * s * y1)
            xs.append(None)
            ys.append(None)
        if not xs:
            continue
        strong = tier == 0
        out.append(go.Scattergl(
            x=xs, y=ys, mode="lines",
            line=dict(color=LADDER_COLOUR[tier], width=1.6 if strong else 1.0),
            opacity=(0.95 if highlight is not None
                     else (0.5 if strong else 0.24)),
            name=LADDER[tier][0],
            legendgroup=LADDER[tier][0],
            visible=True if tier in tiers_on else "legendonly",
            hoverinfo="skip", showlegend=highlight is None,
        ))
    return out


def node_trace(view, selected=None):
    """The datasets themselves. customdata carries the row number, which is how
    a click gets turned back into 'which dataset was that'."""
    pos = POS[view]
    conste = LAY["constellation"]["nodes"]
    intake_cell = next(b["cell"] for b in REF["bands"] if b["id"] == "intake")
    colours, sizes, text, edge = [], [], [], []
    for i, t in enumerate(TABLES):
        n = conste[i]
        if view == "connection":
            # Brightness = how many DISCRIMINATING IDs it carries. The bright
            # ones are the crossings, and that ranking is this view's argument.
            colours.append("#41505f" if not n["keyed"] else
                           "#eef1f5" if n["w"] >= 2 else
                           "#9fb0c6" if n["w"] == 1 else "#5d6d80")
            sizes.append(5 + 13 * math.sqrt(t["deg"] / MAX_LINKS))
            edge.append(0)
        elif view == "subject":
            # The tile IS the dataset here, so the marker is only a modest
            # click target rather than something competing with the tile.
            colours.append("#eef1f5" if t["deg"] else "#5d6d80")
            sizes.append(4 + 7 * math.sqrt(t["deg"] / MAX_LINKS))
            edge.append(0)
        else:
            # On the production line it's a station in its bank, like every
            # other object -- gold-edged if we've charted links for it, which
            # is the only thing distinguishing it from plain raw intake.
            colours.append(STAGE_COLOUR[0])
            sizes.append(max(4.0, intake_cell * 0.9))
            edge.append(1.4 if t["deg"] else 0)
        text.append(
            f"<b>{t['n']}</b><br>{t['dom'].replace('_', ' ').lower()}"
            f" · {t['rows']:,} records · {t['deg']} links"
            f"<br>IDs: {', '.join(t['keys']) or 'none to match on'}"
            "<extra></extra>")

    widths, edge_colours = list(edge), [LADDER_COLOUR[0]] * N
    if selected is not None:
        widths = [3 if i == selected else edge[i] for i in range(N)]
        edge_colours = ["#ffffff" if i == selected else LADDER_COLOUR[0]
                        for i in range(N)]
    return go.Scattergl(
        x=[p[0] for p in pos], y=[p[1] for p in pos],
        mode="markers",
        marker=dict(color=colours, size=sizes,
                    symbol="square" if view == "journey" else "circle",
                    line=dict(width=widths, color=edge_colours)),
        opacity=0.6 if view == "subject" else 1.0,
        customdata=list(range(N)),
        hovertemplate="%{text}", text=text,
        name="datasets", showlegend=False,
    )


def pipeline_traces():
    """The production line itself: every object in the build, and what runs
    after what.

    The 368 datasets are only the first bank. If we drew nothing else, the five
    stage labels would promise 2,454 things and show 368 -- so this draws the
    rest of the machine, and the handoffs between them.
    """
    seated = {SEAT[i] for i in range(N) if SEAT[i] >= 0}
    band_cell = {b["id"]: b["cell"] for b in REF["bands"]}

    xs, ys, colours, sizes, labels = [], [], [], [], []
    for idx, node in enumerate(REF["nodes"]):
        if idx in seated:
            continue                     # already drawn, and clickable, above
        xs.append(node["x"])
        ys.append(node["y"])
        colours.append(STAGE_COLOUR[STAGE_ORDER.index(node["s"])])
        sizes.append(max(3.0, band_cell[node["s"]] * 0.9))
        labels.append(f"<b>{node['id']}</b><br>{STAGES[node['s']]['label'].lower()}"
                      "<extra></extra>")

    lx, ly = [], []
    for a, b in REF["links"]:
        u, v = REF["nodes"][a], REF["nodes"][b]
        mid = (u["x"] + v["x"]) / 2
        for s in (0.0, 0.33, 0.66, 1.0):
            # A gentle S-curve, so a thousand handoffs read as flow rather than
            # as a solid block of straight lines.
            lx.append((1 - s) ** 3 * u["x"] + 3 * (1 - s) ** 2 * s * mid
                      + 3 * (1 - s) * s * s * mid + s ** 3 * v["x"])
            ly.append((1 - s) ** 3 * u["y"] + 3 * (1 - s) ** 2 * s * u["y"]
                      + 3 * (1 - s) * s * s * v["y"] + s ** 3 * v["y"])
        lx.append(None)
        ly.append(None)

    return [
        go.Scattergl(x=lx, y=ly, mode="lines",
                     line=dict(color="rgb(120,150,190)", width=0.8),
                     opacity=0.22, name="what feeds what",
                     hoverinfo="skip", showlegend=False),
        go.Scattergl(x=xs, y=ys, mode="markers",
                     marker=dict(color=colours, size=sizes, symbol="square",
                                 line=dict(width=0)),
                     opacity=0.75, name="the rest of the build",
                     hovertemplate="%{text}", text=labels, showlegend=False),
    ]


def furniture(view):
    """The rooms, wells and banks the datasets sit in. Drawn as shapes so they
    stay behind everything and never steal a click."""
    shapes, notes = [], []
    if view == "subject":
        for r in LAY["stacks"]["rooms"]:
            shapes.append(dict(type="rect", x0=r["x"], y0=r["y"],
                               x1=r["x"] + r["w"], y1=r["y"] + r["h"],
                               fillcolor="rgba(255,255,255,.035)",
                               line=dict(color="rgba(255,255,255,.15)", width=1),
                               layer="below"))
            if r["w"] > 92 and r["h"] > 24:
                notes.append(dict(x=r["x"] + 5, y=r["y"] + 12,
                                  text=f"{r['d'].replace('_', ' ')}  {r['n']}",
                                  showarrow=False, xanchor="left", yanchor="top",
                                  font=dict(family=MONO, size=10,
                                            color="rgba(232,234,237,.8)")))
        # One tile per dataset, sized by how much is in it.
        biggest = math.log10(max(max(t["rows"] for t in TABLES), 10))
        for i, c in CELL.items():
            shade = 0.17 + 0.62 * (math.log10(max(TABLES[i]["rows"], 1)) / biggest)
            shapes.append(dict(type="rect", x0=c["x"] + .6, y0=c["y"] + .6,
                               x1=c["x"] + c["w"] - .6, y1=c["y"] + c["h"] - .6,
                               fillcolor=f"rgba(226,233,243,{shade:.3f})",
                               line=dict(width=0), layer="below"))
    elif view == "connection":
        for w in LAY["constellation"]["wells"]:
            r = 34 + math.sqrt(w["n"]) * 7
            shapes.append(dict(type="circle", x0=w["x"] - r, y0=w["y"] - r,
                               x1=w["x"] + r, y1=w["y"] + r,
                               fillcolor="rgba(157,180,215,.10)",
                               line=dict(width=0), layer="below"))
            dx, dy = w["x"] - BOX_W / 2, w["y"] - BOX_H / 2
            d = math.hypot(dx, dy) or 1
            m = 1 + 92 / d
            notes.append(dict(
                x=BOX_W / 2 + dx * m, y=BOX_H / 2 + dy * m, showarrow=False,
                text=f"<b>{w['k']}</b><br>{w['h']} here · {w['n']} use it",
                font=dict(family=MONO, size=11, color=INK_2)))
    else:
        for b in REF["bands"]:
            st = STAGES[b["id"]]
            shapes.append(dict(type="rect", x0=b["x"] - 8, y0=18,
                               x1=b["x"] + b["w"] + 8, y1=BOX_H - 22,
                               fillcolor="rgba(255,255,255,.025)",
                               line=dict(width=0), layer="below"))
            notes.append(dict(x=b["x"] + b["w"] / 2, y=6, showarrow=False,
                              text=f"<b>{st['label']}</b><br>{st['count']:,}",
                              font=dict(family=MONO, size=11, color=INK_3)))
    return shapes, notes


def build_figure(view, tiers_on, selected=None, show_all=False):
    """Assemble one arrangement.

    Where the links belong depends on the arrangement, and pretending otherwise
    is what turns a map into a hairball. In the connection view they ARE the
    subject, so they're all drawn. Over the subject rooms or the production line
    they'd bury everything, so there they're drawn for whatever you've clicked --
    unless you deliberately ask for all of them.
    """
    shapes, notes = furniture(view)
    draw_all = show_all or view == "connection"
    traces = []
    if view == "journey":
        traces += pipeline_traces()      # the machine, under everything else
    if draw_all:
        traces += link_traces(view, tiers_on)
    if selected is not None:
        traces += link_traces(view, tiers_on, highlight=selected)
    traces.append(node_trace(view, selected))

    fig = go.Figure(traces)
    fig.update_layout(
        paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
        margin=dict(l=4, r=4, t=34, b=4),   # t leaves room for the legend
        shapes=shapes, annotations=notes,
        showlegend=True,
        legend=dict(orientation="h", y=1, x=0, yanchor="bottom",
                    traceorder="reversed",       # strongest link kind first
                    bgcolor="rgba(0,0,0,0)",
                    font=dict(family=MONO, size=11, color=INK_2),
                    itemsizing="constant"),
        hoverlabel=dict(bgcolor=PANEL_2, bordercolor=RULE, align="left",
                        font=dict(family=MONO, size=11, color=INK)),
        dragmode="pan",
        # Keeps your zoom and pan when the figure is rebuilt. Without it, every
        # click would throw you back out to the whole map.
        uirevision=view,
    )
    axis = dict(visible=False, showgrid=False, zeroline=False,
                constrain="domain")
    fig.update_xaxes(range=[0, BOX_W], **axis)
    # y is flipped because the layout was worked out with y going down the page.
    #
    # No aspect lock. Locking it keeps circles perfectly round but leaves half
    # the window empty, and none of these three arrangements is a measurement --
    # the distance between two wells doesn't mean anything in units. Filling the
    # window is worth more than perfectly round wells.
    fig.update_yaxes(range=[BOX_H, 0], **axis)
    return fig


# --------------------------------------------------------------- side panel
#
# This is the whole dossier. It's plain Python building plain HTML -- change
# what a click tells you by editing this one function.


def _h4(txt):
    return html.H4(txt, style={"font": f"600 11px {MONO}", "letterSpacing": ".12em",
                               "textTransform": "uppercase", "color": INK_3,
                               "margin": "22px 0 9px"})


def dossier(i: int):
    t = TABLES[i]

    by_tier: dict[int, int] = {}
    for ei in NEIGHBOURS[i]:
        by_tier[EDGES[ei][2]] = by_tier.get(EDGES[ei][2], 0) + 1
    most = max(by_tier.values(), default=1)

    links = sorted(
        ({"j": e[1] if e[0] == i else e[0], "tier": e[2], "key": e[3],
          "matched": e[4]} for e in (EDGES[ei] for ei in NEIGHBOURS[i])),
        key=lambda d: (d["tier"], -d["matched"]))[:40]

    rows = [
        _h4("what this is"),
        html.P(t["desc"] or "No description recorded for this one yet.",
               style={"font": f"13.5px/1.6 {SANS}", "color": INK_2, "margin": 0}),
        _h4("the numbers"),
        html.Div([
            html.Div([html.Span("records ", style={"color": INK_3}),
                      html.Span(f"{t['rows']:,}")]),
            html.Div([html.Span("links ", style={"color": INK_3}),
                      html.Span(str(t["deg"]))]),
            html.Div([html.Span("subject ", style={"color": INK_3}),
                      html.Span(t["dom"].replace("_", " ").lower())]),
        ], style={"font": f"13px {MONO}", "color": INK, "lineHeight": "1.7"}),
        _h4("what it can be matched on"),
        html.Div(
            [html.Span(k, style={
                "font": f"11px {MONO}", "padding": "2px 7px", "borderRadius": "2px",
                "border": f"1px solid {'rgba(251,192,106,.42)' if is_rare(k) else RULE}",
                "color": LADDER_COLOUR[0] if is_rare(k) else INK_2,
                "marginRight": "5px", "display": "inline-block",
                "marginBottom": "5px"}) for k in t["keys"]]
            or [html.Span("nothing yet", style={"font": f"11px {MONO}",
                                                "color": INK_3})]),
        html.P("Gold means an ID rare enough to pick out one specific thing. "
               "Almost every dataset has a name and a ZIP code, so those two "
               "can't identify anyone on their own.",
               style={"font": f"12px/1.55 {SANS}", "color": INK_3,
                      "margin": "9px 0 0"}),
    ]

    if by_tier:
        rows.append(_h4("how sure we are of its links"))
        for tier, count in sorted(by_tier.items()):
            rows.append(html.Div([
                html.Span(style={"width": "9px", "height": "9px", "flex": "none",
                                 "borderRadius": "1px",
                                 "background": LADDER_COLOUR[tier]}),
                html.Span(LADDER[tier][0], style={"width": "132px", "flex": "none",
                                                  "color": INK_2}),
                html.Span(str(count), style={"width": "34px", "flex": "none",
                                             "textAlign": "right", "color": INK}),
                html.Span(style={"height": "5px", "borderRadius": "2px",
                                 "background": LADDER_COLOUR[tier],
                                 "width": f"{100 * count / most:.0f}%"}),
            ], title=LADDER[tier][1],
                style={"display": "flex", "alignItems": "center", "gap": "9px",
                       "font": f"12.5px {MONO}", "margin": "5px 0"}))

    if links:
        rows.append(_h4("links to"))
        for L in links:
            rows.append(html.Div([
                html.Span(style={"width": "7px", "height": "7px", "flex": "none",
                                 "borderRadius": "1px",
                                 "background": LADDER_COLOUR[L["tier"]]}),
                html.Span(TABLES[L["j"]]["n"],
                          style={"flex": "1", "wordBreak": "break-all"}),
                html.Span(L["key"], style={"flex": "none", "color": INK_3}),
            ], style={"display": "flex", "gap": "9px", "alignItems": "center",
                      "font": f"11.5px {MONO}", "color": INK_2, "padding": "6px 0",
                      "borderBottom": "1px solid rgba(255,255,255,.05)"}))

    rows.append(_h4("where it comes from, and where it goes"))
    seat = SEAT[i]
    if seat < 0:
        rows.append(html.P(
            "We measured this one, but it was never wired into the build — so "
            "there's no journey to show. That's a gap in our plumbing, not "
            "something about the data.",
            style={"font": f"13px/1.6 {SANS}", "color": INK_2, "margin": 0}))
    else:
        chain, seen = [], {seat}

        def walk(u, step):
            for v in (KIDS[u] if step > 0 else PARENTS[u]):
                if v in seen:
                    continue
                seen.add(v)
                chain.append((v, step))
                walk(v, step + (1 if step > 0 else -1))

        walk(seat, 1)
        walk(seat, -1)
        for node, depth in sorted([(seat, 0)] + chain, key=lambda c: c[1])[:26]:
            n = REF["nodes"][node]
            rows.append(html.Div([
                html.Span(style={"width": "7px", "height": "7px", "flex": "none",
                                 "borderRadius": "1px", "marginTop": "5px",
                                 "background": STAGE_COLOUR[
                                     STAGE_ORDER.index(n["s"])]}),
                html.Span(n["id"], style={"wordBreak": "break-all",
                                          "color": INK if node == seat else INK_2}),
            ], style={"display": "flex", "gap": "9px", "alignItems": "flex-start",
                      "font": f"11.5px/1.75 {MONO}"}))

    return [
        html.Div(t["dom"].replace("_", " ").lower(),
                 style={"font": f"11px {MONO}", "letterSpacing": ".13em",
                        "textTransform": "uppercase", "color": LADDER_COLOUR[0]}),
        html.H3(t["n"], style={"font": f"640 14px/1.35 {MONO}", "color": INK,
                               "margin": "6px 0 0", "wordBreak": "break-all"}),
        html.Div(rows, style={"marginTop": "4px"}),
    ]


# ------------------------------------------------------------------- the app

app = Dash(__name__, title="The Library — Atlas")

CHIP = {"font": f"12px {MONO}", "color": INK_2, "background": "transparent",
        "border": f"1px solid {RULE}", "borderRadius": "3px",
        "padding": "6px 13px", "cursor": "pointer"}

app.layout = html.Div([
    dcc.Store(id="selected"),
    html.Div([
        html.Div(["Ripple · ", html.B("The Library")],
                 style={"font": f"12px {MONO}", "letterSpacing": ".15em",
                        "textTransform": "uppercase", "color": INK_3}),
        # Plain buttons rather than radio inputs: Dash styles its own radios and
        # they collide with their labels at this font. Buttons we control.
        html.Div([html.Button(label, id={"kind": "view", "value": value}, n_clicks=0,
                              style=CHIP)
                  for value, label in [("subject", "1  by subject"),
                                       ("connection", "2  by connection"),
                                       ("journey", "3  by journey")]],
                 style={"display": "flex", "gap": "6px"}),
        dcc.Store(id="view", data="subject"),
        dcc.Dropdown(
            id="find", placeholder="find a dataset…",
            options=[{"label": t["n"], "value": i} for i, t in enumerate(TABLES)],
            style={"width": "320px", "font": f"12px {MONO}"}),
        dcc.Checklist(
            id="show-all", options=[{"label": "show every link at once",
                                     "value": "yes"}], value=[],
            style={"font": f"11.5px {MONO}"},
            inputStyle={"marginRight": "7px", "accentColor": LADDER_COLOUR[0]},
            labelStyle={"display": "flex", "alignItems": "center", "color": INK_2,
                        "cursor": "pointer", "whiteSpace": "nowrap"}),
    ], style={"display": "flex", "alignItems": "center", "gap": "18px",
              "padding": "10px 16px", "borderBottom": f"1px solid {RULE}",
              "background": PANEL_2, "flexWrap": "wrap", "flex": "none"}),

    html.Div(id="hint",
             style={"font": f"12px/1.5 {SANS}", "color": INK_3,
                    "padding": "8px 16px", "borderBottom": f"1px solid {RULE}",
                    "background": PANEL, "flex": "none"}),

    html.Div([
        # flex:1 + minWidth:0 is what makes the map actually fill the space left
        # over. Without it dcc.Graph sits at its default 700px and leaves a gap.
        dcc.Graph(id="map", style={"flex": "1", "minWidth": "0", "height": "100%"},
                  config={"scrollZoom": True, "displaylogo": False,
                          "modeBarButtonsToRemove": ["select2d", "lasso2d",
                                                     "autoScale2d"]}),
        html.Aside(id="panel", children=[
            html.Div("Click any dataset to see what it is, what it links to, "
                     "and where it came from.",
                     style={"font": f"13px/1.6 {SANS}", "color": INK_3})],
            style={"width": "400px", "flex": "none", "overflowY": "auto",
                   "boxSizing": "border-box",   # or the padding widens it
                   "padding": "16px 18px 40px", "background": PANEL,
                   "borderLeft": f"1px solid {RULE}"}),
    ], style={"display": "flex", "flex": "1", "minHeight": "0"}),
], style={"position": "fixed", "inset": "0", "display": "flex",
          "flexDirection": "column", "background": SURFACE, "color": INK,
          "font": f"14px {SANS}"})


@app.callback(Output("map", "figure"), Output("hint", "children"),
              Input("view", "data"), Input("selected", "data"),
              Input("show-all", "value"), State("map", "figure"))
def redraw(view, selected, show_all, current):
    # Which link kinds are switched off in the legend right now, so that
    # rebuilding the figure doesn't quietly switch them all back on.
    tiers_on = set(range(len(LADDER)))
    if current:
        shown = {tr.get("name"): tr.get("visible", True)
                 for tr in current.get("data", [])}
        for idx, lab in enumerate(LADDER):
            if shown.get(lab[0]) == "legendonly":
                tiers_on.discard(idx)
    title, blurb = VIEW_BLURB[view]
    tail = ("Click any dataset to see what it is and what it links to. "
            "Click a legend entry to hide a kind of link.")
    fig = build_figure(view, tiers_on, selected, show_all=bool(show_all))
    return fig, html.Span([html.B(title), " — ", blurb, "  ·  ", tail])


@app.callback(Output("view", "data"),
              Output({"kind": "view", "value": ALL}, "style"),
              Input({"kind": "view", "value": ALL}, "n_clicks"),
              State("view", "data"))
def switch_view(_clicks, current):
    picked = ctx.triggered_id["value"] if isinstance(ctx.triggered_id, dict) else current
    order = ["subject", "connection", "journey"]
    on = {**CHIP, "background": INK, "color": SURFACE, "fontWeight": "600"}
    return picked, [on if v == picked else CHIP for v in order]


@app.callback(Output("selected", "data"),
              Input("map", "clickData"), Input("find", "value"))
def choose(click, found):
    if ctx.triggered_id == "find":
        return found
    if not click:
        return no_update
    return click["points"][0].get("customdata")


@app.callback(Output("panel", "children"), Input("selected", "data"))
def show(selected):
    if selected is None:
        return html.Div("Click any dataset to see what it is, what it links to, "
                        "and where it came from.",
                        style={"font": f"13px/1.6 {SANS}", "color": INK_3})
    return dossier(int(selected))


def main():
    print(f"  {N} datasets · {len(EDGES)} links · built from {DATA.name}")
    print("  open  http://127.0.0.1:8050")
    app.run(debug=False, port=8050)


if __name__ == "__main__":
    main()
