"""
The side panel. Plain Python building plain HTML -- change what a click
tells you by editing this one file.

Every dossier ends with a door, not a wall: the "links to" rows are buttons
that select their dataset, so exploring the Library is a walk, not a search.
"""

from __future__ import annotations

from dash import html

from viz.library_data import (EDGES, KIDS, LADDER, META, NEIGHBOURS, PARENTS,
                              REF, STAGES, TABLES, XREF, is_rare)
from viz.palette import (INK, INK_2, INK_3, LADDER_COLOUR, MONO, RULE, SANS,
                         STAGE_COLOUR, STATE_STORY)

MAX_LINK_ROWS = 40
MAX_CHAIN_ROWS = 26


def _h4(txt):
    return html.H4(txt, style={"font": f"600 11px {MONO}",
                               "letterSpacing": ".12em",
                               "textTransform": "uppercase", "color": INK_3,
                               "margin": "22px 0 9px"})


def _more(n, what):
    """Caps are honest here: if a list is cut, the cut is announced."""
    return html.Div(f"… and {n:,} more {what}",
                    style={"font": f"11px {MONO}", "color": INK_3,
                           "padding": "6px 0"})


def about():
    """The 'about this build' panel. Every number here is computed at
    compile time from the warehouse registry -- nothing is typed in by hand."""
    pairs = META.get("pairs_tested")
    stage_counts = META["stage_counts"]

    def p(children):
        return html.P(children, style={"font": f"13px/1.65 {SANS}",
                                       "color": INK_2, "margin": 0})

    def num(v):
        return html.B(f"{v:,}", style={"color": INK})

    return [
        html.Div([
            html.Div("about this build",
                     style={"font": f"11px {MONO}", "letterSpacing": ".13em",
                            "textTransform": "uppercase", "flex": "1",
                            "color": LADDER_COLOUR[0]}),
            html.Button("✕", id={"kind": "clear", "value": 0}, n_clicks=0,
                        className="clearbtn", title="close (Esc)",
                        style={"background": "transparent", "border": "none",
                               "color": INK_3, "cursor": "pointer",
                               "font": f"13px {MONO}"}),
        ], style={"display": "flex", "alignItems": "center"}),
        html.H3("The Library Atlas", style={"font": f"640 14px/1.35 {MONO}",
                                            "color": INK,
                                            "margin": "6px 0 0"}),
        html.Div([
            _h4("the stack"),
            p("Python · Plotly + Dash · Snowflake · dbt. One JavaScript file "
              "(the lens morph); everything else is Python you can read."),
            _h4("the evidence"),
            p([num(META["links"]), " verified links, found by testing ",
               num(pairs) if pairs else "millions of", " candidate pairs "
               "across 15+ named ID systems, each graded on a 6-rung "
               "evidence ladder. A hunch is never drawn as loudly as a "
               "certainty — that rule is load-bearing."]),
            _h4("the pipeline"),
            p([num(META["dbt_objects"]), " dbt objects in five stages ("]
              + [html.Span(f"{s['id']} {stage_counts[s['id']]:,}"
                           + ("" if k == len(STAGES) - 1 else " · "),
                           style={"color": INK_2})
                 for k, s in enumerate(STAGES.values())]
              + [f") wired by {META['lineage_edges']:,} lineage edges. "
                 f"The journey lens draws all of it."]),
            _h4("the census"),
            p([num(META["tables"]), " datasets, all drawn, all clickable: ",
               f"{META['states']['lit']:,} linked · "
               f"{META['states']['dark']:,} measured with no match yet · "
               f"{META['states']['keyless']:,} with nothing to match on · "
               f"{META['states']['uncharted']:,} collected and queued for "
               f"link discovery."]),
            _h4("the engineering"),
            p("2,694 links are drawn as six traces, not thousands — all "
              "segments of one confidence rung share a single WebGL trace. "
              "The three arrangements share one coordinate space, so a "
              "dataset keeps its identity and simply moves when the argument "
              "changes. Layouts are precompiled and deterministic: same "
              "inputs, same map, byte for byte."),
            _h4("the ground rule"),
            p("Nothing here talks to the warehouse at view time. "
              "`python -m viz.compile_library` reads the registry and emits "
              "one JSON; the app reads that. Every number on this page is "
              "computed at compile time. Nothing is typed in by hand."),
        ], style={"marginTop": "4px"}),
    ]


def dossier(i: int):
    t = TABLES[i]

    by_tier: dict[int, int] = {}
    for ei in NEIGHBOURS[i]:
        by_tier[EDGES[ei][2]] = by_tier.get(EDGES[ei][2], 0) + 1
    most = max(by_tier.values(), default=1)

    all_links = sorted(
        ({"j": e[1] if e[0] == i else e[0], "tier": e[2], "key": e[3],
          "matched": e[4]} for e in (EDGES[ei] for ei in NEIGHBOURS[i])),
        key=lambda d: (d["tier"], -d["matched"]))
    links = all_links[:MAX_LINK_ROWS]

    state_title, state_words = STATE_STORY[t["state"]]

    rows = [
        _h4("what this is"),
        html.P(t["desc"] or "No description recorded for this one yet.",
               style={"font": f"13.5px/1.6 {SANS}", "color": INK_2,
                      "margin": 0}),
        _h4("where it stands"),
        html.P([html.B(state_title, style={"color": INK}), " — ", state_words],
               style={"font": f"13px/1.6 {SANS}", "color": INK_2, "margin": 0}),
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
                "font": f"11px {MONO}", "padding": "2px 7px",
                "borderRadius": "2px",
                "border": f"1px solid "
                          f"{'rgba(251,192,106,.42)' if is_rare(k) else RULE}",
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
                html.Span(style={"width": "9px", "height": "9px",
                                 "flex": "none", "borderRadius": "1px",
                                 "background": LADDER_COLOUR[tier]}),
                html.Span(LADDER[tier][0], style={"width": "132px",
                                                  "flex": "none",
                                                  "color": INK_2}),
                html.Span(str(count), style={"width": "34px", "flex": "none",
                                             "textAlign": "right",
                                             "color": INK}),
                html.Span(style={"height": "5px", "borderRadius": "2px",
                                 "background": LADDER_COLOUR[tier],
                                 "width": f"{100 * count / most:.0f}%"}),
            ], title=LADDER[tier][1],
                style={"display": "flex", "alignItems": "center", "gap": "9px",
                       "font": f"12.5px {MONO}", "margin": "5px 0"}))

    if links:
        rows.append(_h4("links to  ·  click one to walk there"))
        for row_no, L in enumerate(links):
            rows.append(html.Button([
                html.Span(style={"width": "7px", "height": "7px",
                                 "flex": "none", "borderRadius": "1px",
                                 "background": LADDER_COLOUR[L["tier"]]}),
                html.Span(TABLES[L["j"]]["n"],
                          style={"flex": "1", "wordBreak": "break-all",
                                 "textAlign": "left"}),
                html.Span(L["key"], style={"flex": "none", "color": INK_3}),
                # row is part of the id because two rows can point at the
                # SAME neighbour over different IDs -- duplicate component
                # ids silently break click delivery.
            ], id={"kind": "goto", "value": L["j"], "row": row_no}, n_clicks=0,
                className="walk",
                style={"display": "flex", "gap": "9px",
                       "alignItems": "center", "width": "100%",
                       "font": f"11.5px {MONO}", "color": INK_2,
                       "padding": "6px 2px", "background": "transparent",
                       "border": "none", "cursor": "pointer",
                       "borderBottom": "1px solid rgba(255,255,255,.05)"}))
        if len(all_links) > MAX_LINK_ROWS:
            rows.append(_more(len(all_links) - MAX_LINK_ROWS, "links"))

    rows.append(_h4("where it comes from, and where it goes"))
    seat = XREF[i]
    if REF["nodes"][seat]["s"] == "siding":
        rows.append(html.P(
            "Collected and measured, but never wired into the build — so "
            "there's no journey to show yet. It sits in the siding, waiting "
            "on the pipeline, not on the data.",
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
        ordered = sorted([(seat, 0)] + chain, key=lambda c: c[1])
        for node, depth in ordered[:MAX_CHAIN_ROWS]:
            n = REF["nodes"][node]
            rows.append(html.Div([
                html.Span(style={"width": "7px", "height": "7px",
                                 "flex": "none", "borderRadius": "1px",
                                 "marginTop": "5px",
                                 "background": STAGE_COLOUR[n["s"]]}),
                html.Span(n["id"], style={"wordBreak": "break-all",
                                          "color": INK if node == seat
                                          else INK_2}),
            ], style={"display": "flex", "gap": "9px",
                      "alignItems": "flex-start",
                      "font": f"11.5px/1.75 {MONO}"}))
        if len(ordered) > MAX_CHAIN_ROWS:
            rows.append(_more(len(ordered) - MAX_CHAIN_ROWS, "steps"))

    # The exit ramp: every dossier ends pointing somewhere.
    if t["deg"]:
        tail = ("This is one of 1,043. Click any neighbour above to keep "
                "walking.")
    else:
        tail = ("This is one of 1,043. Flip to the connection view to see "
                "where it would sit if a link turns up.")
    rows.append(html.P(tail, style={"font": f"12px/1.6 {SANS}",
                                    "color": INK_3, "margin": "18px 0 0"}))

    return [
        html.Div([
            html.Div(t["dom"].replace("_", " ").lower(),
                     style={"font": f"11px {MONO}", "letterSpacing": ".13em",
                            "textTransform": "uppercase", "flex": "1",
                            "color": LADDER_COLOUR[0]}),
            # Pattern id, not a plain one: this button only exists while a
            # dossier is open, and Dash refuses to wire a callback to a plain
            # id that is missing from the page.
            html.Button("✕", id={"kind": "clear", "value": 0}, n_clicks=0,
                        className="clearbtn", title="clear selection (Esc)",
                        style={"background": "transparent", "border": "none",
                               "color": INK_3, "cursor": "pointer",
                               "font": f"13px {MONO}"}),
        ], style={"display": "flex", "alignItems": "center"}),
        html.H3(t["n"], style={"font": f"640 14px/1.35 {MONO}", "color": INK,
                               "margin": "6px 0 0", "wordBreak": "break-all"}),
        html.Div(rows, style={"marginTop": "4px"}),
    ]
