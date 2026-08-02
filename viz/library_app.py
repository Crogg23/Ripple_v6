"""
The Library Atlas -- Plotly + Dash.

    python -m viz.library_app        then open http://127.0.0.1:8050

All 1,043 datasets in the warehouse, every verified link between them, and
the pipeline that builds them -- drawn three ways from one set of shared
coordinates, so a dataset keeps its identity and simply MOVES when you change
the arrangement. Any one arrangement is an argument about what matters;
flipping between them stops any single one posing as the truth.

WHERE THE DATA COMES FROM
    outputs/library.json    built by:  python -m viz.compile_library
Nothing here talks to Snowflake. Nothing here needs the internet.

The drawing lives in viz/figures.py, the click-a-dataset panel in
viz/dossier.py, the colours in viz/palette.py. This file is only the frame
and the wiring.
"""

from __future__ import annotations

import os

from dash import ALL, Dash, Input, Output, Patch, State, ctx, dcc, html, no_update

from dash import ClientsideFunction, clientside_callback

from viz.dossier import about, dossier
from viz.figures import BG_COUNT, build_figure, highlight_bundle, lens_store
from viz.library_data import (EDGES, KIDS, LADDER, LAY, META, N, TABLES, XREF)
from viz.palette import (INK, INK_2, INK_3, LADDER_COLOUR, MONO, PANEL,
                         PANEL_2, RULE, SANS, SURFACE, VIEW_BLURB)

# Links per rung, for the honesty dial's live count.
TIER_EDGE_COUNT = [0] * len(LADDER)
for _e in EDGES:
    TIER_EDGE_COUNT[_e[2]] += 1


def _exemplars():
    """One hand-picked destination per lens for the 'show me' chip --
    computed from the data, not typed in."""
    # Subject: the most-connected dataset in the biggest room.
    big_room = max(LAY["stacks"]["rooms"], key=lambda r: (r["n"], r["d"]))["d"]
    subject = max((i for i, t in enumerate(TABLES) if t["dom"] == big_room),
                  key=lambda i: (TABLES[i]["deg"], TABLES[i]["n"]))
    # Connection: the busiest bridge -- most discriminating IDs, then links.
    wells = LAY["constellation"]["nodes"]
    connection = max(range(N), key=lambda i: (wells[i]["w"], TABLES[i]["deg"],
                                              TABLES[i]["n"]))
    # Journey: the linked dataset whose trip downstream runs deepest.
    depth: dict[int, int] = {}

    def down(u):
        if u not in depth:
            depth[u] = 1 + max((down(v) for v in KIDS[u]), default=0)
        return depth[u]

    journey = max((i for i in range(N) if TABLES[i]["deg"] > 0),
                  key=lambda i: (down(XREF[i]), TABLES[i]["n"]))
    return {"subject": subject, "connection": connection, "journey": journey}


EXEMPLAR = _exemplars()

app = Dash(__name__, title="The Library — Atlas",
           suppress_callback_exceptions=True)

CHIP = {"font": f"11px {MONO}", "letterSpacing": ".08em",
        "textTransform": "uppercase", "color": INK_2,
        "background": "transparent", "border": f"1px solid {RULE}",
        "borderRadius": "3px", "padding": "7px 14px", "cursor": "pointer",
        "transition": "all .15s ease"}
CHIP_ON = {**CHIP, "background": "rgba(251,192,106,.10)",
           "border": "1px solid rgba(251,192,106,.55)", "color": "#fbc06a"}

EMPTY_PANEL = html.Div(
    "Click any dataset to see what it is, what it links to, and where it "
    "came from.",
    style={"font": f"13px/1.6 {SANS}", "color": INK_3})

VIEWS = ["subject", "connection", "journey"]

app.layout = html.Div([
    dcc.Store(id="selected"),
    dcc.Store(id="view", data="subject"),
    # Everything the clientside morph needs, shipped to the browser once.
    dcc.Store(id="lens-store", data=lens_store()),
    dcc.Store(id="tiers-on", data=list(range(len(LADDER)))),
    dcc.Store(id="intro-done"),
    html.Div([
        html.Div([
            html.Div(["RIPPLE · ", html.B("THE LIBRARY",
                                          style={"color": INK})],
                     style={"font": f"12px {MONO}", "letterSpacing": ".22em",
                            "color": INK_3}),
            html.Div([html.Span(f"{META['tables']:,}",
                                style={"color": "#fbc06a"}),
                      " datasets · ",
                      html.Span(f"{META['links']:,}",
                                style={"color": "#fbc06a"}),
                      " verified links"],
                     style={"font": f"10.5px {MONO}", "color": INK_3,
                            "letterSpacing": ".04em", "marginTop": "3px"}),
        ], style={"marginRight": "8px"}),
        # Plain buttons rather than radio inputs: Dash styles its own radios
        # and they collide with their labels at this font. Buttons we control.
        html.Div([html.Button(label, id={"kind": "view", "value": value},
                              n_clicks=0, className="chip", style=CHIP)
                  for value, label in [("subject", "by subject"),
                                       ("connection", "by connection"),
                                       ("journey", "by journey")]],
                 style={"display": "flex", "gap": "6px"}),
        dcc.Dropdown(
            id="find", placeholder="find a dataset…",
            options=[{"label": t["n"], "value": i}
                     for i, t in enumerate(TABLES)],
            style={"width": "320px", "font": f"12px {MONO}"}),
        dcc.Checklist(
            id="show-all", options=[{"label": "show every link at once",
                                     "value": "yes"}], value=[],
            style={"font": f"11.5px {MONO}"},
            inputStyle={"marginRight": "7px", "accentColor": "#fbc06a"},
            labelStyle={"display": "flex", "alignItems": "center",
                        "color": INK_2, "cursor": "pointer",
                        "whiteSpace": "nowrap"}),
    ], style={"display": "flex", "alignItems": "center", "gap": "18px",
              "padding": "10px 16px", "borderBottom": f"1px solid {RULE}",
              "background": PANEL_2, "flexWrap": "wrap", "flex": "none"}),

    html.Div([
        html.Div(id="hint",
                 style={"font": f"12px/1.5 {SANS}", "color": INK_3,
                        "flex": "1", "minWidth": "260px"}),
        html.Button("show me something", id="showme", n_clicks=0,
                    className="chip", title="fly to something worth seeing "
                    "in this arrangement",
                    style={**CHIP, "padding": "4px 10px",
                           "font": f"11px {MONO}"}),
        # The honesty dial. Six rungs, strongest first; click one to strip
        # that kind of link off the map. A hunch is never drawn as loudly as
        # a certainty -- this is where you choose how sure you want to be.
        html.Div([
            html.Span("how sure do you want to be?",
                      style={"font": f"10px {MONO}", "color": INK_3,
                             "letterSpacing": ".08em",
                             "textTransform": "uppercase"}),
            html.Div([html.Button(
                "", id={"kind": "tier", "value": i}, n_clicks=0,
                className="rung", title=f"{LADDER[i][0]} — {LADDER[i][1]}",
                style={"width": "18px", "height": "14px", "padding": "0",
                       "cursor": "pointer", "borderRadius": "2px",
                       "border": "1px solid rgba(255,255,255,.18)",
                       "background": LADDER_COLOUR[i]})
                for i in range(len(LADDER))],
                style={"display": "flex", "gap": "4px"}),
            html.Span(id="dial-count",
                      children=f"showing {META['links']:,} of "
                               f"{META['links']:,} links",
                      style={"font": f"10.5px {MONO}", "color": INK_3}),
        ], style={"display": "flex", "alignItems": "center", "gap": "10px"}),
        html.Button("about this build", id="about-btn", n_clicks=0,
                    className="chip",
                    style={**CHIP, "padding": "4px 10px",
                           "font": f"11px {MONO}"}),
    ], style={"display": "flex", "alignItems": "center", "gap": "16px",
              "padding": "8px 16px", "borderBottom": f"1px solid {RULE}",
              "background": PANEL, "flex": "none", "flexWrap": "wrap"}),

    html.Div([
        # flex:1 + minWidth:0 is what makes the map fill the space left over.
        # Without it dcc.Graph sits at its default 700px and leaves a gap.
        dcc.Graph(id="map", style={"flex": "1", "minWidth": "0",
                                   "height": "100%"},
                  config={"scrollZoom": True, "displaylogo": False,
                          "modeBarButtonsToRemove": ["select2d", "lasso2d",
                                                     "autoScale2d"]}),
        html.Aside(id="panel", children=[EMPTY_PANEL],
                   style={"width": "400px", "flex": "none",
                          "overflowY": "auto",
                          "boxSizing": "border-box",  # or the padding widens it
                          "padding": "16px 18px 40px", "background": PANEL,
                          "borderLeft": f"1px solid {RULE}"}),
    ], style={"display": "flex", "flex": "1", "minHeight": "0"}),

    # The Census Roll's title card. viz/assets/morph.js runs the show and
    # fades this out; any key or click skips straight to the finished map.
    html.Div([
        html.Div("THE LIBRARY",
                 style={"font": f"600 34px {SANS}", "letterSpacing": ".3em",
                        "color": INK}),
        html.Div(f"{META['tables']:,} public-record datasets, mapped.",
                 style={"font": f"15px {MONO}", "color": INK_2,
                        "marginTop": "14px"}),
        html.Div("Everything here is real, measured, and clickable.",
                 style={"font": f"13px {SANS}", "color": INK_3,
                        "marginTop": "8px"}),
        html.Div(id="intro-count", children="",
                 style={"font": f"13px {MONO}", "color": "#fbc06a",
                        "marginTop": "26px", "minHeight": "18px"}),
        html.Div(("Every line was tested — "
                  + (f"{META['pairs_tested']:,} pairs checked "
                     if META.get("pairs_tested") else "millions of pairs checked ")
                  + f"to find {META['links']:,} verified links."),
                 style={"font": f"12px {SANS}", "color": INK_3,
                        "marginTop": "8px"}),
    ], id="intro",
        style={"position": "fixed", "inset": "0", "zIndex": "10",
               "display": "flex", "flexDirection": "column",
               "alignItems": "center", "justifyContent": "center",
               "background": "rgba(13,17,23,.94)", "pointerEvents": "none",
               "transition": "opacity .9s ease", "textAlign": "center"}),
], style={"position": "fixed", "inset": "0", "display": "flex",
          "flexDirection": "column", "background": SURFACE, "color": INK,
          "font": f"14px {SANS}"})


# Full rebuilds happen only when the ARRANGEMENT changes -- lens, dial, or
# show-all. A selection never rebuilds: see select_patch below.
@app.callback(Output("map", "figure"), Output("hint", "children"),
              Input("view", "data"),
              Input("show-all", "value"), Input("tiers-on", "data"),
              State("selected", "data"))
def redraw(view, show_all, tiers_on, selected):
    if selected is not None and int(selected) < 0:
        selected = None                       # -1 means the About panel
    title, blurb = VIEW_BLURB[view]
    fig = build_figure(view, set(tiers_on or []), selected,
                       show_all=bool(show_all))
    return fig, html.Span([html.B(title), " — ", blurb])


# A click rewrites only the eight selection traces -- a few KB instead of a
# 2 MB figure. This is what makes selecting feel instant. Trace indices are
# fixed by the trace contract in viz/figures.py.
@app.callback(Output("map", "figure", allow_duplicate=True),
              Input("selected", "data"),
              State("view", "data"), State("tiers-on", "data"),
              prevent_initial_call=True)
def select_patch(selected, view, tiers_on):
    if selected is not None and int(selected) < 0:
        selected = None
    hb = highlight_bundle(view, selected, set(tiers_on or []))
    bg = BG_COUNT[view]
    p = Patch()
    for k, tier in enumerate(range(len(LADDER) - 1, -1, -1)):
        xs, ys = hb["tiers"][tier]
        p["data"][bg + k]["x"] = xs
        p["data"][bg + k]["y"] = ys
    p["data"][bg + 6]["x"] = hb["halo"][0]
    p["data"][bg + 6]["y"] = hb["halo"][1]
    node = p["data"][bg + 7]["marker"]
    node["opacity"] = hb["opac"]
    node["line"]["width"] = hb["widths"]
    node["line"]["color"] = hb["edge_colours"]
    return p


@app.callback(Output("tiers-on", "data"),
              Output({"kind": "tier", "value": ALL}, "style"),
              Output("dial-count", "children"),
              Input({"kind": "tier", "value": ALL}, "n_clicks"),
              State("tiers-on", "data"))
def honesty_dial(_clicks, tiers_on):
    tiers = set(tiers_on if tiers_on is not None else range(len(LADDER)))
    if isinstance(ctx.triggered_id, dict) and ctx.triggered[0]["value"]:
        i = ctx.triggered_id["value"]
        tiers.symmetric_difference_update({i})
    styles = []
    for i in range(len(LADDER)):
        on = i in tiers
        styles.append({"width": "18px", "height": "14px", "padding": "0",
                       "cursor": "pointer", "borderRadius": "2px",
                       "border": "1px solid rgba(255,255,255,.18)" if on
                                 else "1px solid rgba(255,255,255,.30)",
                       "background": LADDER_COLOUR[i] if on else "transparent"})
    shown = sum(TIER_EDGE_COUNT[i] for i in tiers)
    return (sorted(tiers), styles,
            f"showing {shown:,} of {META['links']:,} links")


# The lens switch is clientside: viz/assets/morph.js tweens the 1,043 nodes
# to their new seats at 60fps, then returns the picked lens -- which is what
# triggers the server's full redraw. The tween is the transition; the server
# render is the destination.
clientside_callback(
    ClientsideFunction(namespace="atlas", function_name="switch_lens"),
    Output("view", "data"),
    Input({"kind": "view", "value": ALL}, "n_clicks"),
    State("view", "data"),
    State("lens-store", "data"),
    prevent_initial_call=True,
)


@app.callback(Output({"kind": "view", "value": ALL}, "style"),
              Input("view", "data"))
def chip_styles(view):
    return [CHIP_ON if v == view else CHIP for v in VIEWS]


@app.callback(Output("selected", "data"),
              Input("map", "clickData"),
              Input("find", "value"),
              Input({"kind": "goto", "value": ALL, "row": ALL}, "n_clicks"),
              Input({"kind": "clear", "value": ALL}, "n_clicks"),
              Input("showme", "n_clicks"),
              Input("about-btn", "n_clicks"),
              State("view", "data"),
              prevent_initial_call=True)
def choose(click, found, _goto, _clear, _showme, _about, view):
    trig = ctx.triggered_id
    if __debug__ and os.environ.get("ATLAS_TRACE"):
        print("choose:", trig, ctx.triggered[:2], flush=True)
    if isinstance(trig, dict) and trig.get("kind") == "clear":
        return None if ctx.triggered[0]["value"] else no_update
    if trig == "about-btn":
        return -1                    # the About panel wears the dossier's seat
    if trig == "showme":
        return EXEMPLAR[view]
    if trig == "find":
        return found
    if isinstance(trig, dict) and trig.get("kind") == "goto":
        # A "links to" row in the dossier: walk to the neighbour. The
        # callback also fires when a fresh dossier mounts its rows with zero
        # clicks -- ignore that, or every selection would re-select itself.
        if ctx.triggered[0]["value"]:
            return trig["value"]
        return no_update
    if not click:
        return no_update
    # Pipeline stations and shelf tiles carry no customdata; clicking one
    # keeps the current selection instead of silently clearing it.
    cd = click["points"][0].get("customdata")
    return cd if cd is not None else no_update


@app.callback(Output("panel", "children"), Input("selected", "data"))
def show(selected):
    if selected is None:
        return EMPTY_PANEL
    if int(selected) < 0:
        return about()
    return dossier(int(selected))


# The Census Roll. Triggered by the lens store, which is set exactly once at
# page load -- NOT by the figure, because figure -> intro -> selection ->
# figure would be a dependency cycle and the renderer quietly drops the last
# update in one. morph.js polls until Plotly has actually mounted the map.
clientside_callback(
    ClientsideFunction(namespace="atlas", function_name="census_roll"),
    Output("intro-done", "data"),
    Input("lens-store", "data"),
    prevent_initial_call=False,
)


def main():
    port = int(os.environ.get("ATLAS_PORT", "8050"))
    print(f"  {N} datasets · {len(EDGES)} links · from outputs/library.json")
    print(f"  open  http://127.0.0.1:{port}")
    app.run(debug=False, port=port)


if __name__ == "__main__":
    main()
