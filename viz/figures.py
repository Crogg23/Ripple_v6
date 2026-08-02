"""
Everything drawn on the map. Each function returns Plotly pieces; edit these
to change how the Library looks -- nothing else needs to know.

THE TRACE CONTRACT (performance is built on it, do not break it casually):

Every figure has a FIXED number of traces in a FIXED order for its lens --
empty traces are drawn as empty rather than omitted:

    subject      6 tile fills · 6 all-link tiers · 6 highlight tiers · halo · nodes
    connection       6 all-link tiers            · 6 highlight tiers · halo · nodes
    journey      2 pipeline   · 6 all-link tiers · 6 highlight tiers · halo · nodes

Because the order never changes, selecting a dataset does NOT rebuild the
figure. The app sends a Dash Patch that rewrites only the last eight traces'
arrays -- a few kilobytes instead of a two-megabyte figure -- which is the
difference between a click feeling instant and feeling like a page load.
Everything is Scattergl: 1,043 points and 16,000 line segments live on the
GPU, and panning never re-tessellates an SVG path.
"""

from __future__ import annotations

import math

import plotly.graph_objects as go

from viz.library_data import (BOX_H, BOX_W, CELL, EDGES, LADDER, LAY, MAX_LINKS,
                              N, NEIGHBOURS, POS, REF, STAGES, TABLES, XREF)
from viz.palette import (INK, INK_2, INK_3, LADDER_COLOUR, MONO, PANEL_2, RULE,
                         STAGE_COLOUR, STATE_COLOUR, STATE_OPACITY, SURFACE)

UNCHARTED = 3

# Background trace count per lens -- the highlight block starts here.
BG_COUNT = {"subject": 12, "connection": 6, "journey": 8}


# ------------------------------------------------------------------- links


def _tier_arrays(view, tier, only=None):
    """The curve points for every edge of one rung. only=<table index>
    restricts to that dataset's own links."""
    pos = POS[view]
    xs, ys = [], []
    for e in EDGES:
        if e[2] != tier:
            continue
        if only is not None and only not in (e[0], e[1]):
            continue
        (x0, y0), (x1, y1) = pos[e[0]], pos[e[1]]
        if view == "journey":
            # Links here sit inside one bank; bowing toward the middle would
            # drag them across unrelated stages.
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 - abs(y1 - y0) * 0.22
        else:
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            cx = mx + (BOX_W / 2 - mx) * 0.16
            cy = my + (BOX_H / 2 - my) * 0.16
        # A few points along the curve, so links fan out instead of stacking
        # into one illegible bar.
        for s in (0.0, 0.25, 0.5, 0.75, 1.0):
            xs.append((1 - s) ** 2 * x0 + 2 * (1 - s) * s * cx + s * s * x1)
            ys.append((1 - s) ** 2 * y0 + 2 * (1 - s) * s * cy + s * s * y1)
        xs.append(None)
        ys.append(None)
    return xs, ys


def link_traces(view, tiers_on, active):
    """Exactly six traces, strongest rung LAST so certainty lands on top.
    active=False keeps the slots but empties them (the trace contract)."""
    out = []
    for tier in range(len(LADDER) - 1, -1, -1):
        if active and tier in tiers_on:
            xs, ys = _tier_arrays(view, tier)
        else:
            xs, ys = [], []
        strong = tier == 0
        out.append(go.Scattergl(
            x=xs, y=ys, mode="lines",
            line=dict(color=LADDER_COLOUR[tier], width=1.6 if strong else 1.0),
            opacity=0.5 if strong else 0.24,
            name=f"links-{tier}", hoverinfo="skip", showlegend=False,
        ))
    return out


def highlight_bundle(view, selected, tiers_on):
    """Everything a selection changes, as plain arrays -- consumed both by
    build_figure (on a lens rebuild) and by the app's Patch (on a click).

    Returns {tiers: [(xs, ys)] * 6, halo: (xs, ys), opac, widths, edge_colours}.
    """
    tiers = []
    for tier in range(len(LADDER)):
        if selected is not None and tier in tiers_on:
            tiers.append(_tier_arrays(view, tier, only=selected))
        else:
            tiers.append(([], []))

    _, _, opac = node_style(view)
    widths = [0.0] * N
    edge_colours = [LADDER_COLOUR[0]] * N
    if view == "journey":
        widths = [1.4 if t["deg"] else 0.0 for t in TABLES]

    if selected is None:
        halo = ([], [])
    else:
        x, y = POS[view][selected]
        halo = ([x], [y])
        focus = {selected}
        for ei in NEIGHBOURS[selected]:
            focus.add(EDGES[ei][0])
            focus.add(EDGES[ei][1])
        # The rest of the field steps back -- quiet, never invisible.
        opac = [o if i in focus else round(o * 0.22, 3)
                for i, o in enumerate(opac)]
        opac[selected] = 1.0
        widths[selected] = 3
        edge_colours[selected] = "#ffffff"
    return {"tiers": tiers, "halo": halo, "opac": opac,
            "widths": widths, "edge_colours": edge_colours}


def highlight_traces(view, selected, tiers_on):
    """The six per-selection link traces + the halo, weakest first."""
    hb = highlight_bundle(view, selected, tiers_on)
    out = []
    for tier in range(len(LADDER) - 1, -1, -1):
        xs, ys = hb["tiers"][tier]
        out.append(go.Scattergl(
            x=xs, y=ys, mode="lines",
            line=dict(color=LADDER_COLOUR[tier], width=1.7 if tier == 0 else 1.1),
            opacity=0.95, name=f"hl-{tier}",
            hoverinfo="skip", showlegend=False,
        ))
    out.append(go.Scattergl(
        x=hb["halo"][0], y=hb["halo"][1], mode="markers",
        marker=dict(size=26, color="rgba(251,192,106,.16)",
                    line=dict(width=1, color="rgba(251,192,106,.35)")),
        hoverinfo="skip", showlegend=False, name="halo",
    ))
    return out, hb


# ------------------------------------------------------------------- nodes


def node_style(view):
    """Per-dataset colour, size and base opacity for one lens. One function
    so the server figure and the clientside morph can never disagree."""
    conste = LAY["constellation"]["nodes"]
    band_cell = {b["id"]: b["cell"] for b in REF["bands"]}
    colours, sizes, opac = [], [], []
    for i, t in enumerate(TABLES):
        st = t["state"]
        if view == "connection":
            # Brightness = how many DISCRIMINATING IDs it carries. The bright
            # ones are the crossings, and that ranking is this view's argument.
            n = conste[i]
            colours.append(STATE_COLOUR[3] if st == UNCHARTED else
                           "#f4f0e8" if n["w"] >= 2 else
                           "#a8b8cc" if n["w"] == 1 else
                           STATE_COLOUR[2] if n["keyed"] else "#4a5866")
            sizes.append(3.5 if st == UNCHARTED
                         else round(5 + 13 * math.sqrt(t["deg"] / MAX_LINKS), 2))
        elif view == "subject":
            # The tile IS the dataset here; the marker is a click target that
            # roughly fills its shelf cell without competing with it.
            c = CELL[i]
            colours.append(STATE_COLOUR[st])
            sizes.append(round(max(3.5, min(min(c["w"], c["h"]) * 0.55, 20.0)), 2))
        else:
            seat_stage = REF["nodes"][XREF[i]]["s"]
            colours.append(STAGE_COLOUR[seat_stage])
            sizes.append(round(max(4.0, band_cell[seat_stage] * 0.9), 2))
        opac.append(round(STATE_OPACITY[st]
                          * (0.75 if view == "subject" else 1.0), 3))
    return colours, sizes, opac


def node_trace(view, hb):
    """All 1,043 datasets, one trace, always LAST. customdata carries the row
    number -- how a click gets turned back into 'which dataset was that'."""
    pos = POS[view]
    colours, sizes, _ = node_style(view)
    text = []
    for t in TABLES:
        story = ["part of the mesh", "measured, no match yet",
                 "nothing to match on yet", "collected, not yet charted"][t["state"]]
        text.append(
            f"<b>{t['n']}</b><br>{t['dom'].replace('_', ' ').lower()}"
            f" · {t['rows']:,} records · {t['deg']} links · {story}"
            f"<br>IDs: {', '.join(t['keys']) or 'none to match on'}"
            "<extra></extra>")
    return go.Scattergl(
        x=[p[0] for p in pos], y=[p[1] for p in pos],
        mode="markers",
        marker=dict(color=colours, size=sizes, opacity=hb["opac"],
                    symbol="square" if view == "journey" else "circle",
                    line=dict(width=hb["widths"], color=hb["edge_colours"])),
        customdata=list(range(N)),
        hovertemplate="%{text}", text=text,
        name="datasets", showlegend=False,
    )


# --------------------------------------------------------------- background


def pipeline_traces():
    """The rest of the production line: every dbt object that is not one of
    the 1,043 datasets, and every handoff. Without this, five stage labels
    would promise 2,454 things and show 1,043. Always exactly two traces."""
    seated = set(XREF)
    band_cell = {b["id"]: b["cell"] for b in REF["bands"]}

    xs, ys, colours, sizes, labels = [], [], [], [], []
    for idx, node in enumerate(REF["nodes"]):
        if idx in seated:
            continue                 # already drawn, and clickable, above
        xs.append(node["x"])
        ys.append(node["y"])
        colours.append(STAGE_COLOUR[node["s"]])
        sizes.append(max(3.0, band_cell[node["s"]] * 0.9))
        stage = STAGES.get(node["s"])
        labels.append(f"<b>{node['id']}</b>"
                      f"<br>{stage['label'].lower() if stage else node['s']}"
                      "<extra></extra>")

    lx, ly = [], []
    for a, b in REF["links"]:
        u, v = REF["nodes"][a], REF["nodes"][b]
        mid = (u["x"] + v["x"]) / 2
        for s in (0.0, 0.33, 0.66, 1.0):
            # A gentle S-curve, so a thousand handoffs read as flow rather
            # than a solid block of straight lines.
            lx.append((1 - s) ** 3 * u["x"] + 3 * (1 - s) ** 2 * s * mid
                      + 3 * (1 - s) * s * s * mid + s ** 3 * v["x"])
            ly.append((1 - s) ** 3 * u["y"] + 3 * (1 - s) ** 2 * s * u["y"]
                      + 3 * (1 - s) * s * s * v["y"] + s ** 3 * v["y"])
        lx.append(None)
        ly.append(None)

    return [
        go.Scattergl(x=lx, y=ly, mode="lines",
                     line=dict(color="rgb(110,140,180)", width=0.8),
                     opacity=0.16, name="pipeline-links",
                     hoverinfo="skip", showlegend=False),
        go.Scattergl(x=xs, y=ys, mode="markers",
                     marker=dict(color=colours, size=sizes, symbol="square",
                                 line=dict(width=0)),
                     opacity=0.7, name="pipeline-nodes",
                     hovertemplate="%{text}", text=labels, showlegend=False),
    ]


def tile_traces():
    """The shelf tiles of the subject lens, drawn as SIX filled WebGL paths
    instead of 1,043 rectangle shapes.

    Layout shapes are SVG and re-tessellate on every pan frame; a thousand of
    them make the subject lens the slowest room in the house. Bucketing the
    tiles by brightness into a handful of None-separated fill traces is the
    same economy the links use. Always exactly six traces, even when a
    brightness bucket is empty -- the trace contract."""
    biggest = math.log10(max(max(t["rows"] for t in TABLES), 10))
    buckets: dict[int, list[int]] = {b: [] for b in range(6)}
    for i, t in enumerate(TABLES):
        shade = math.log10(max(t["rows"], 1)) / biggest
        buckets[min(5, int(shade * 6))].append(i)

    out = []
    for b in range(6):
        xs, ys = [], []
        for i in buckets[b]:
            c = CELL[i]
            x0, y0 = c["x"] + .6, c["y"] + .6
            x1, y1 = c["x"] + c["w"] - .6, c["y"] + c["h"] - .6
            xs += [x0, x1, x1, x0, x0, None]
            ys += [y0, y0, y1, y1, y0, None]
        # Quiet on purpose: the tiles are floor, the datasets are the light.
        alpha = 0.06 + 0.065 * b
        out.append(go.Scattergl(
            x=xs, y=ys, mode="lines", fill="toself",
            fillcolor=f"rgba(214,224,238,{alpha:.3f})",
            line=dict(width=0), hoverinfo="skip", showlegend=False,
            name=f"tiles-{b}",
        ))
    return out


def furniture(view):
    """The rooms, wells and banks the datasets sit in. Shapes stay behind
    everything and never steal a click."""
    shapes, notes = [], []
    if view == "subject":
        for r in LAY["stacks"]["rooms"]:
            shapes.append(dict(type="rect", x0=r["x"], y0=r["y"],
                               x1=r["x"] + r["w"], y1=r["y"] + r["h"],
                               fillcolor="rgba(157,180,215,.030)",
                               line=dict(color="rgba(157,180,215,.14)", width=1),
                               layer="below"))
            if r["w"] > 92 and r["h"] > 24:
                notes.append(dict(x=r["x"] + 6, y=r["y"] + 13,
                                  text=f"<b>{r['d'].replace('_', ' ').upper()}</b>"
                                       f"  <span style='color:rgba(154,164,178,.75)'>{r['n']}</span>",
                                  showarrow=False, xanchor="left", yanchor="top",
                                  font=dict(family=MONO, size=10,
                                            color="rgba(232,234,237,.62)")))
        ax = LAY["stacks"]["annex"]
        shapes.append(dict(type="rect", x0=ax["x"], y0=ax["y"],
                           x1=ax["x"] + ax["w"], y1=ax["y"] + ax["h"],
                           fillcolor="rgba(157,180,215,.012)",
                           line=dict(color="rgba(157,180,215,.08)", width=1,
                                     dash="dot"),
                           layer="below"))
        notes.append(dict(x=ax["x"] + 5, y=ax["y"] + 10, showarrow=False,
                          xanchor="left", yanchor="top",
                          text="THE ANNEX — collected, not yet wired in",
                          font=dict(family=MONO, size=9.5,
                                    color="rgba(107,118,132,.9)")))
    elif view == "connection":
        for w in LAY["constellation"]["wells"]:
            r = 34 + math.sqrt(w["n"]) * 7
            shapes.append(dict(type="circle", x0=w["x"] - r, y0=w["y"] - r,
                               x1=w["x"] + r, y1=w["y"] + r,
                               fillcolor="rgba(157,180,215,.07)",
                               line=dict(color="rgba(157,180,215,.10)",
                                         width=1), layer="below"))
            dx, dy = w["x"] - BOX_W / 2, w["y"] - BOX_H / 2
            d = math.hypot(dx, dy) or 1
            m = 1 + 92 / d
            notes.append(dict(
                x=BOX_W / 2 + dx * m, y=BOX_H / 2 + dy * m, showarrow=False,
                text=f"<b>{w['k']}</b><br>"
                     f"<span style='font-size:9px'>{w['h']} here · {w['n']} use it</span>",
                font=dict(family=MONO, size=11, color=INK_2)))
    else:
        for k, b in enumerate(REF["bands"]):
            st = STAGES.get(b["id"])
            shapes.append(dict(type="rect", x0=b["x"] - 8, y0=18,
                               x1=b["x"] + b["w"] + 8, y1=BOX_H - 22,
                               fillcolor="rgba(157,180,215,.022)" if k % 2
                                         else "rgba(157,180,215,.012)",
                               line=dict(width=0), layer="below"))
            if st:
                head = (f"<b>{st['label']}</b><br>"
                        f"<span style='font-size:9px'>{st['count']:,}</span>")
            else:
                n_sid = sum(1 for t in TABLES if t["state"] == UNCHARTED)
                head = (f"<b>NOT YET BUILT ON</b><br>"
                        f"<span style='font-size:9px'>{n_sid:,}</span>")
            notes.append(dict(x=b["x"] + b["w"] / 2, y=4, showarrow=False,
                              yanchor="top", text=head,
                              font=dict(family=MONO, size=10.5, color=INK_3)))
    return shapes, notes


# ------------------------------------------------------------------ figure


def build_figure(view, tiers_on, selected=None, show_all=False):
    """Assemble one arrangement, honouring the trace contract above.

    In the connection view the links ARE the subject, so they're all drawn.
    Over the subject rooms or the pipeline they'd bury everything, so there
    they're drawn for whatever you've clicked -- unless you ask for all.
    """
    if selected is not None and selected < 0:
        selected = None
    shapes, notes = furniture(view)
    draw_all = show_all or view == "connection"

    traces = []
    if view == "subject":
        traces += tile_traces()
    if view == "journey":
        traces += pipeline_traces()      # the machine, under everything else
    traces += link_traces(view, tiers_on, active=draw_all)
    assert len(traces) == BG_COUNT[view]
    hl, hb = highlight_traces(view, selected, tiers_on)
    traces += hl
    traces.append(node_trace(view, hb))

    fig = go.Figure(traces)
    fig.update_layout(
        paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
        margin=dict(l=4, r=4, t=26, b=4),
        shapes=shapes, annotations=notes,
        showlegend=False,
        hoverlabel=dict(bgcolor=PANEL_2, bordercolor=RULE, align="left",
                        font=dict(family=MONO, size=11, color=INK)),
        dragmode="pan",
        # Keeps zoom and pan when the figure is rebuilt; without it every
        # rebuild would throw you back out to the whole map.
        uirevision=view,
    )
    axis = dict(visible=False, showgrid=False, zeroline=False,
                constrain="domain")
    xr, yr = axis_ranges(view)
    fig.update_xaxes(range=xr, **axis)
    fig.update_yaxes(range=yr, **axis)
    return fig


def axis_ranges(view):
    """Camera home for one lens. Shared with the clientside morph so the
    range tween lands exactly where the server's next figure starts."""
    # The connection ring overhangs the box on purpose; give it air.
    pad = 120 if view == "connection" else 0
    # y flipped: the layouts were worked out with y running down the page.
    return [-pad, BOX_W + pad], [BOX_H + pad * 0.6, -pad * 0.6]


def lens_store():
    """Everything the clientside morph and intro need, per lens: positions,
    marker styling, symbol, camera home, and the intro's running order. Sent
    to the browser once."""
    out = {}
    for view in ("subject", "connection", "journey"):
        colours, sizes, opac = node_style(view)
        xr, yr = axis_ranges(view)
        out[view] = {
            "x": [p[0] for p in POS[view]],
            "y": [p[1] for p in POS[view]],
            "colours": colours, "sizes": sizes, "opac": opac,
            "symbol": "square" if view == "journey" else "circle",
            "xrange": xr, "yrange": yr,
        }

    # The Census Roll: rooms pour in largest first, the annex last, and the
    # count ticking up to 1,043 is the emotional beat. reveal[i] is dataset
    # i's step in that running order.
    rooms = sorted(LAY["stacks"]["rooms"], key=lambda r: (-r["n"], r["d"]))
    rank = {r["d"]: k for k, r in enumerate(rooms)}
    annex_step = len(rooms)
    reveal = [annex_step if t["state"] == UNCHARTED else rank[t["dom"]]
              for t in TABLES]

    from viz.library_data import META
    name_idx = {t["n"]: i for i, t in enumerate(TABLES)}
    out["meta"] = {
        "reveal": reveal,
        "steps": annex_step + 1,
        "intro_pick": name_idx[META["hubs"][0][0]],
        "tables": META["tables"],
        "links": META["links"],
        "pairs": META.get("pairs_tested"),
    }
    return out
