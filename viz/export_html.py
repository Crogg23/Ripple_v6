"""
The postcard: one standalone HTML file of the Library Atlas.

    python -m viz.export_html        # -> outputs/library_atlas.html

The Dash app (viz/library_app.py) is the instrument -- morph, dossier,
honesty dial. This is the send-a-link version built from the SAME figure
factory: all three arrangements in one double-clickable file, lens buttons
along the top, hover intact, no server, no network.

Hard cuts between lenses here, not morphs -- a static export has no
clientside wiring, and pretending otherwise would mean shipping a second
copy of the app. The postcard shows the map; the instrument plays it.
"""

from __future__ import annotations

import pathlib

import plotly.graph_objects as go

from viz.figures import axis_ranges, build_figure
from viz.library_data import META, ROOT
from viz.palette import INK, INK_2, MONO, SURFACE, VIEW_BLURB

OUT = ROOT / "outputs" / "library_atlas.html"

VIEWS = ["subject", "connection", "journey"]


def build_postcard():
    """One figure holding all three lenses; buttons flip visibility, ranges
    and furniture in a single relayout."""
    figs = {v: build_figure(v, tiers_on=set(range(6)), selected=None,
                            show_all=(v == "connection")) for v in VIEWS}

    traces, spans = [], {}
    for v in VIEWS:
        start = len(traces)
        traces.extend(figs[v].data)
        spans[v] = (start, len(traces))

    def mask(view):
        lo, hi = spans[view]
        return [lo <= i < hi for i in range(len(traces))]

    buttons = []
    for v in VIEWS:
        lay = figs[v].layout
        xr, yr = axis_ranges(v)
        buttons.append(dict(
            label=f"by {v}", method="update",
            args=[{"visible": mask(v)},
                  {"shapes": lay.shapes, "annotations": lay.annotations,
                   "xaxis.range": xr, "yaxis.range": yr}],
        ))

    fig = go.Figure(traces)
    fig.update_layout(figs["subject"].layout)
    for i, on in enumerate(mask("subject")):
        fig.data[i].visible = on
    fig.update_layout(
        updatemenus=[dict(
            type="buttons", direction="right", buttons=buttons,
            x=0, y=1.06, xanchor="left", yanchor="bottom",
            bgcolor=SURFACE, bordercolor="rgba(255,255,255,.18)",
            font=dict(family=MONO, size=12, color=INK_2),
        )],
        title=dict(
            text=(f"THE LIBRARY — {META['tables']:,} public-record datasets, "
                  f"{META['links']:,} verified links"),
            font=dict(family=MONO, size=14, color=INK),
            x=0.5, y=0.995),
        margin=dict(l=4, r=4, t=64, b=4),
    )
    return fig


def main():
    fig = build_postcard()
    fig.write_html(
        OUT, include_plotlyjs=True, full_html=True,
        config={"scrollZoom": True, "displaylogo": False},
        div_id="atlas-postcard",
    )
    print(f"postcard -> {OUT.relative_to(ROOT)}  "
          f"({OUT.stat().st_size / 1024:.0f} KB)")
    for v in VIEWS:
        print(f"  {v}: {VIEW_BLURB[v][0]}")


if __name__ == "__main__":
    main()
