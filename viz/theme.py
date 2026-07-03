"""The one house theme: a Plotly template called ``ripple_dark``.

Every chart the instrument makes runs through this template, so the four
palettes that drifted apart across connect/explore.py, serve/serve_graph.py,
connect/leads_overlay.py and build_library_map.py stop multiplying here.

The categorical palette is NOT hand-picked: it is the validated 8-slot dark
palette from the dataviz method (OKLCH lightness band, chroma floor, adjacent-
pair CVD separation, >=3:1 contrast), re-validated against THIS surface
(#0d1117) on 2026-07-03. CVD separation sits in the 8-12 floor band, which is
legal only with secondary encoding — plugs always ship a legend (>=2 series)
and hover labels, so identity is never color-alone.

Rules encoded here (don't fight them in a card, they're the method):
  * categorical hues are assigned in FIXED order, never cycled — a 9th series
    folds into 'Other' (plugs handle the fold);
  * sequential = one blue ramp, light->dark; diverging = blue<->red with a
    NEUTRAL gray midpoint; never a rainbow;
  * one axis. No dual-axis chart, ever. Two scales = two charts.

Lazy plotly import so offline tests can import viz.theme without the viz dep.
"""

from __future__ import annotations

import hashlib

# --- surfaces + ink (the GitHub-dark house look serve/ and connect/ already use)
BG = "#0d1117"        # chart + page surface
PANEL = "#161b22"     # hover labels, panels
FG = "#e6edf3"        # primary ink
MUTED = "#8b949e"     # secondary ink (captions, as-of stamps, badges)
GRID = "#21262d"      # recessive gridlines
ACCENT = "#3987e5"    # slot-1 blue — the default single-series color

# --- validated categorical palette (dark steps, fixed order — never cycle)
CATEGORICAL = [
    "#3987e5",  # 1 blue
    "#199e70",  # 2 aqua
    "#c98500",  # 3 yellow
    "#008300",  # 4 green
    "#9085e9",  # 5 violet
    "#e66767",  # 6 red
    "#d55181",  # 7 magenta
    "#d95926",  # 8 orange
]

# --- sequential blue ramp (magnitude: heatmaps, choropleths), light -> dark
SEQUENTIAL = [
    "#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7",
    "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b",
]

# --- diverging blue <-> red with a neutral dark-gray midpoint (polarity only)
DIVERGING = [
    "#3987e5", "#6da7ec", "#9ec5f4", "#cde2fb", "#383835",
    "#f4c7c7", "#ee9d9d", "#e66767", "#c94040",
]

TEMPLATE_NAME = "ripple_dark"


def register() -> str:
    """Register the ripple_dark template with plotly (idempotent). Returns its name."""
    import plotly.graph_objects as go
    import plotly.io as pio

    if TEMPLATE_NAME in pio.templates:
        return TEMPLATE_NAME

    axis = dict(
        gridcolor=GRID, linecolor=GRID, zeroline=False,
        title_font=dict(color=MUTED), tickfont=dict(color=MUTED),
    )
    pio.templates[TEMPLATE_NAME] = go.layout.Template(
        layout=dict(
            paper_bgcolor=BG,
            plot_bgcolor=BG,
            font=dict(color=FG, size=13),
            title=dict(font=dict(color=FG, size=18), x=0.02, xanchor="left"),
            colorway=CATEGORICAL,
            colorscale=dict(
                sequential=_scale(SEQUENTIAL),
                diverging=_scale(DIVERGING),
            ),
            xaxis=axis,
            yaxis=axis,
            hoverlabel=dict(bgcolor=PANEL, font=dict(color=FG)),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=FG)),
            margin=dict(l=60, r=30, t=70, b=90),
        )
    )
    return TEMPLATE_NAME


def _scale(colors: list[str]) -> list[list]:
    """Evenly spaced [fraction, color] pairs — the shape plotly colorscales want."""
    n = len(colors) - 1
    return [[i / n, c] for i, c in enumerate(colors)]


def apply(fig):
    """Stamp the house template + logo-off config hint onto an existing figure."""
    register()
    fig.update_layout(template=TEMPLATE_NAME)
    return fig


def domain_color(domain: str) -> str:
    """A stable color per Library domain — md5, NOT hash() (which is seed-salted
    per process and would reshuffle colors on every restart)."""
    if not domain:
        return MUTED
    idx = int(hashlib.md5(domain.encode()).hexdigest(), 16) % len(CATEGORICAL)
    return CATEGORICAL[idx]


# write_html/show config every card uses (plotly's `config`, not template, carries this)
PLOT_CONFIG = {"displaylogo": False}
