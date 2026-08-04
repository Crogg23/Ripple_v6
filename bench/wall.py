#!/usr/bin/env python
"""
THE WALL - every chart Plotly can make, on one page.

Run it:      python bench/wall.py
Output:      outputs/plotly_wall.html   (opens in your browser by default)
Flags:       --no-open      build the file, don't open it
             --offline      inline the whole plotly.js library (~5 MB file,
                            but it works with no internet at all)

Everything here is made-up data generated with numpy. No database, no
credentials, no network calls. It runs on a plane.

HOW THIS FILE IS ORGANISED
--------------------------
Charts are grouped by the QUESTION you walked in holding, not by the chart's
name. Ten questions:

    COMPARE  DISTRIBUTE  RELATE  COMPOSE  FLOW
    RANK     LOCATE      CHANGE  CONNECT  SINGLE VALUE

Every chart lives in its own small function named `c_<something>`. Right above
each function is an `@chart(...)` line holding the label, the one-line call
that made it, the data shape it needs, and a plain-English "use when". That
metadata is printed on the page next to the chart, so the HTML and this file
say the same thing.

Read it top to bottom as a reference, or jump to the section for your question.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
import warnings
import webbrowser
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.io as pio
from plotly.offline import get_plotlyjs, get_plotlyjs_version
from plotly.subplots import make_subplots

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "outputs" / "plotly_wall.html"

# One seed, so the page looks identical every time you build it.
RNG = np.random.default_rng(7)


# =====================================================================
# FAKE DATA
# ---------------------------------------------------------------------
# Each helper returns the *shape* named in its docstring. The shape is the
# thing that decides which charts are even possible, so they're named after
# the shape and not after the story.
# =====================================================================

AGENCIES = ["Health", "Defense", "Transport", "Energy", "Justice", "Labor"]
REGIONS = ["North", "South", "East", "West"]
STAGES = ["Filed", "Screened", "Investigated", "Cited", "Penalised"]


def d_category() -> pd.DataFrame:
    """One label column + one number. One row per label."""
    return pd.DataFrame(
        {"agency": AGENCIES, "spend": [82.0, 140.0, 61.0, 47.0, 33.0, 25.0]}
    )


def d_category_2way() -> pd.DataFrame:
    """Two label columns + one number. One row per pair."""
    rows = []
    for a in AGENCIES:
        for r in REGIONS:
            rows.append({"agency": a, "region": r, "spend": float(RNG.integers(5, 60))})
    return pd.DataFrame(rows)


def d_long() -> pd.DataFrame:
    """One category column + one number, NOT summarised - many rows per label."""
    frames = []
    for i, a in enumerate(AGENCIES):
        n = 160 + i * 40
        frames.append(
            pd.DataFrame(
                {
                    "agency": a,
                    "region": RNG.choice(REGIONS, n),
                    "award": RNG.gamma(2.0 + i * 0.35, 9_000, n),
                }
            )
        )
    return pd.concat(frames, ignore_index=True)


def d_bimodal() -> pd.DataFrame:
    """One number + one category, where one group is secretly two groups."""
    one = pd.DataFrame({"group": "single peak", "score": RNG.normal(50, 9, 500)})
    two = pd.DataFrame(
        {
            "group": "two peaks",
            "score": np.r_[RNG.normal(30, 6, 300), RNG.normal(74, 7, 300)],
        }
    )
    return pd.concat([one, two], ignore_index=True)


def d_scatter(n: int = 450) -> pd.DataFrame:
    """Two number columns, one row per thing (+ a category and a size column)."""
    insp = RNG.integers(1, 70, n).astype(float)
    viol = np.clip(insp * 0.45 + RNG.normal(0, 5, n), 0, None)
    return pd.DataFrame(
        {
            "inspections": insp,
            "violations": viol,
            "fines": np.clip(viol * 900 + RNG.normal(0, 4000, n), 0, None),
            "employees": RNG.integers(5, 900, n),
            "region": RNG.choice(REGIONS, n),
        }
    )


def d_numeric_block(n: int = 300) -> pd.DataFrame:
    """Several number columns describing the same rows. For splom / parcoords."""
    base = RNG.normal(0, 1, n)
    return pd.DataFrame(
        {
            "inspections": (base * 8 + 40 + RNG.normal(0, 4, n)).round(1),
            "violations": (base * 5 + 18 + RNG.normal(0, 3, n)).round(1),
            "fines": (base * 2200 + 9000 + RNG.normal(0, 1500, n)).round(0),
            "employees": (RNG.gamma(2, 120, n)).round(0),
            "risk": (RNG.random(n) * 100).round(1),
        }
    )


def d_timeseries(days: int = 420) -> pd.DataFrame:
    """One date column + one category + one number. Many rows per date."""
    dates = pd.date_range("2023-01-02", periods=days, freq="D")
    frames = []
    for i, r in enumerate(REGIONS):
        walk = np.cumsum(RNG.normal(0.35 + i * 0.1, 3.0, days)) + 120 + i * 25
        frames.append(pd.DataFrame({"date": dates, "region": r, "claims": np.abs(walk)}))
    return pd.concat(frames, ignore_index=True)


def d_hierarchy() -> pd.DataFrame:
    """Nested category columns (broad -> narrow) + one number."""
    rows = []
    for a in AGENCIES[:4]:
        for prog in ("Grants", "Contracts", "Direct"):
            for v in ("Alpha Co", "Beta LLC", "Gamma Inc"):
                rows.append(
                    {
                        "agency": a,
                        "program": prog,
                        "vendor": v,
                        "amount": float(RNG.integers(4, 90)),
                    }
                )
    return pd.DataFrame(rows)


def d_flow() -> pd.DataFrame:
    """A from-column, a to-column, and an amount. The edge list."""
    rows = []
    for src in ("PAC Alpha", "PAC Beta", "Corp Gamma"):
        for dst in ("Cmte North", "Cmte South", "Cmte East"):
            rows.append({"source": src, "target": dst, "amount": float(RNG.integers(3, 40))})
    for src in ("Cmte North", "Cmte South", "Cmte East"):
        for dst in ("Rep A", "Rep B"):
            rows.append({"source": src, "target": dst, "amount": float(RNG.integers(4, 30))})
    return pd.DataFrame(rows)


def d_stages() -> pd.DataFrame:
    """Ordered stages + a count that shrinks."""
    return pd.DataFrame({"stage": STAGES, "cases": [12000, 8400, 4100, 1500, 420]})


def d_geo_points(n: int = 500) -> pd.DataFrame:
    """A latitude column + a longitude column + a number."""
    lat = np.r_[RNG.normal(40.7, 0.9, n // 2), RNG.normal(34.0, 1.1, n - n // 2)]
    lon = np.r_[RNG.normal(-74.0, 1.1, n // 2), RNG.normal(-118.2, 1.3, n - n // 2)]
    return pd.DataFrame({"lat": lat, "lon": lon, "amount": RNG.gamma(2, 900, n)})


def d_metro_points(n: int = 350) -> pd.DataFrame:
    """Lat/lon + a number, all inside one city.

    Tile maps live in a narrow card here. A continent-wide view at this width
    leaves the points too sparse to read, and a tile map's whole reason to
    exist is zooming in far enough to see streets - so the demo data is one
    metro area rather than a whole country.
    """
    return pd.DataFrame(
        {
            "lat": RNG.normal(40.73, 0.10, n),
            "lon": RNG.normal(-73.98, 0.13, n),
            "amount": RNG.gamma(2, 900, n),
        }
    )


def d_states() -> pd.DataFrame:
    """A place-code column + one number, and one number that straddles zero."""
    codes = [
        "AL", "AZ", "AR", "CA", "CO", "CT", "FL", "GA", "ID", "IL", "IN", "IA",
        "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE",
        "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI",
        "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    ]
    return pd.DataFrame(
        {
            "state": codes,
            "rate": RNG.gamma(3, 12, len(codes)).round(1),
            "change": RNG.normal(0, 14, len(codes)).round(1),
        }
    )


def d_ohlc(n: int = 70) -> pd.DataFrame:
    """One date column + open / high / low / close per period."""
    dates = pd.bdate_range("2024-01-01", periods=n)
    close = 100 + np.cumsum(RNG.normal(0, 1.6, n))
    open_ = close + RNG.normal(0, 0.8, n)
    high = np.maximum(open_, close) + np.abs(RNG.normal(0, 1.0, n))
    low = np.minimum(open_, close) - np.abs(RNG.normal(0, 1.0, n))
    return pd.DataFrame(
        {"date": dates, "open": open_, "high": high, "low": low, "close": close}
    )


def d_grid(rows: int = 8, cols: int = 12) -> pd.DataFrame:
    """An already-shaped grid - a pivot table. Rows x columns of numbers."""
    z = RNG.gamma(3, 8, (rows, cols)).round(1)
    return pd.DataFrame(
        z,
        index=[f"Region {c}" for c in "ABCDEFGH"[:rows]],
        columns=[f"M{m:02d}" for m in range(1, cols + 1)],
    )


def d_surface(n: int = 40) -> np.ndarray:
    """A number computed over a grid of two inputs. For 3D surfaces / contours."""
    x = np.linspace(-3, 3, n)
    xx, yy = np.meshgrid(x, x)
    return (np.sin(xx) * np.cos(yy) * 3 + np.exp(-(xx**2 + yy**2) / 6) * 4).round(3)


def d_volume(n: int = 14):
    """x, y, z and a value at every point of a 3D grid."""
    g = np.linspace(-2.2, 2.2, n)
    xx, yy, zz = np.meshgrid(g, g, g, indexing="ij")
    val = xx**2 + yy**2 + zz**2
    return xx.ravel(), yy.ravel(), zz.ravel(), val.ravel()


def d_vectorfield(n: int = 6):
    """x, y, z positions and u, v, w directions - six equal-length arrays."""
    g = np.linspace(0, 3, n)
    xx, yy, zz = np.meshgrid(g, g, g, indexing="ij")
    x, y, z = xx.ravel(), yy.ravel(), zz.ravel()
    return x, y, z, np.ones_like(x), np.sin(y) * 0.6, np.cos(z) * 0.6


def d_ternary(n: int = 120) -> pd.DataFrame:
    """Three numbers per row that are parts of one whole."""
    raw = RNG.dirichlet([2.2, 1.6, 1.2], n) * 100
    return pd.DataFrame(
        {
            "federal": raw[:, 0].round(1),
            "state": raw[:, 1].round(1),
            "private": raw[:, 2].round(1),
            "region": RNG.choice(REGIONS, n),
        }
    )


def d_wind(n: int = 16) -> pd.DataFrame:
    """A wrap-around category (compass / hour / month) + a number."""
    dirs = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW",
    ][:n]
    return pd.DataFrame(
        {
            "direction": dirs,
            "frequency": (RNG.gamma(2.5, 3, n) + 2).round(1),
            "strength": RNG.choice(["light", "moderate", "strong"], n),
        }
    )


def d_gantt() -> pd.DataFrame:
    """One row per event with a BEGIN date and an END date."""
    return pd.DataFrame(
        {
            "contract": ["Alpha Co", "Beta LLC", "Gamma Inc", "Delta Ltd", "Alpha Co"],
            "start": pd.to_datetime(
                ["2023-01-15", "2023-04-01", "2023-02-20", "2023-09-10", "2024-01-05"]
            ),
            "end": pd.to_datetime(
                ["2023-08-30", "2024-03-15", "2023-06-01", "2024-06-30", "2024-09-01"]
            ),
            "status": ["closed", "open", "closed", "open", "open"],
        }
    )


def d_rank_over_time() -> pd.DataFrame:
    """Entity + a number + a date, over many periods."""
    years = list(range(2015, 2025))
    ents = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
    rows = []
    for i, e in enumerate(ents):
        walk = np.cumsum(RNG.normal(0.4 - i * 0.15, 1.4, len(years))) + 20 + i * 2
        for y, v in zip(years, walk):
            rows.append({"year": y, "entity": e, "score": float(v)})
    df = pd.DataFrame(rows)
    df["rank"] = df.groupby("year")["score"].rank(ascending=False, method="first")
    return df


def d_geojson_boxes() -> tuple[dict, pd.DataFrame]:
    """Your own polygon boundaries + one row per region + a number."""
    feats, recs = [], []
    for i in range(9):
        r, c = divmod(i, 3)
        lon0, lat0 = -74.2 + c * 0.22, 40.55 + r * 0.16
        feats.append(
            {
                "type": "Feature",
                "id": f"Z{i}",
                "properties": {"zone": f"Z{i}"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [lon0, lat0],
                            [lon0 + 0.2, lat0],
                            [lon0 + 0.2, lat0 + 0.14],
                            [lon0, lat0 + 0.14],
                            [lon0, lat0],
                        ]
                    ],
                },
            }
        )
        recs.append({"zone": f"Z{i}", "rate": float(RNG.integers(10, 95))})
    return {"type": "FeatureCollection", "features": feats}, pd.DataFrame(recs)


# =====================================================================
# THEME
# ---------------------------------------------------------------------
# One dark template registered once, so every figure on the page matches
# without repeating forty lines of update_layout.
# =====================================================================

INK = "#e8edf4"
MUTED = "#8b98ab"
PANEL = "#12171f"
GRID = "#232b38"

# A categorical palette that stays distinguishable for colour-blind readers.
CATS = [
    "#5aa9ff", "#ffb454", "#4ecb8d", "#ff7b9c",
    "#b48cff", "#4fd6d2", "#ffd866", "#ff9f7a",
]

pio.templates["wall"] = go.layout.Template(
    layout=dict(
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font=dict(family="ui-sans-serif, Segoe UI, system-ui, sans-serif", color=INK, size=12),
        colorway=CATS,
        margin=dict(l=56, r=22, t=34, b=44),
        title=dict(x=0.01, xanchor="left", font=dict(size=13, color=MUTED)),
        xaxis=dict(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID, automargin=True),
        yaxis=dict(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID, automargin=True),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        hoverlabel=dict(bgcolor="#0b0f14", bordercolor=GRID, font=dict(color=INK, size=12)),
        colorscale=dict(sequential="Viridis", diverging="RdBu"),
        coloraxis=dict(colorbar=dict(outlinewidth=0, thickness=11, len=0.8)),
        polar=dict(bgcolor=PANEL, angularaxis=dict(gridcolor=GRID), radialaxis=dict(gridcolor=GRID)),
        ternary=dict(
            bgcolor=PANEL,
            aaxis=dict(gridcolor=GRID, linecolor=GRID),
            baxis=dict(gridcolor=GRID, linecolor=GRID),
            caxis=dict(gridcolor=GRID, linecolor=GRID),
        ),
        scene=dict(
            xaxis=dict(backgroundcolor=PANEL, gridcolor=GRID, color=MUTED),
            yaxis=dict(backgroundcolor=PANEL, gridcolor=GRID, color=MUTED),
            zaxis=dict(backgroundcolor=PANEL, gridcolor=GRID, color=MUTED),
        ),
        geo=dict(
            bgcolor=PANEL,
            landcolor="#1b2230",
            lakecolor=PANEL,
            subunitcolor=GRID,
            coastlinecolor=GRID,
            countrycolor=GRID,
        ),
    )
)
pio.templates.default = "wall"
px.defaults.template = "wall"
px.defaults.color_discrete_sequence = CATS


# =====================================================================
# REGISTRY
# ---------------------------------------------------------------------
# @chart(...) puts each figure function on the page with its metadata.
# Order of declaration is order of appearance.
# =====================================================================

SECTIONS: list[tuple[str, str]] = [
    ("COMPARE", "which one is bigger?"),
    ("DISTRIBUTE", "how is it spread out?"),
    ("RELATE", "does X track Y?"),
    ("COMPOSE", "what is it made of?"),
    ("FLOW", "what moves where?"),
    ("RANK", "who is on top, and did it change?"),
    ("LOCATE", "where?"),
    ("CHANGE", "what happened over time?"),
    ("CONNECT", "what links to what?"),
    ("SINGLE VALUE", "one number that matters"),
]


@dataclass
class Chart:
    section: str
    name: str
    call: str
    shape: str
    use_when: str
    fn: Callable[[], go.Figure] | None = None
    note: str = ""
    blocked: str = ""
    traces: list[str] = field(default_factory=list)
    height: int = 340


CHARTS: list[Chart] = []


def chart(section, name, call, shape, use_when, note="", height=340):
    """Register a chart function on the wall. The metadata lands on the page."""

    def deco(fn):
        CHARTS.append(
            Chart(
                section=section,
                name=name,
                call=call,
                shape=shape,
                use_when=use_when,
                fn=fn,
                note=note,
                height=height,
            )
        )
        return fn

    return deco


def blocked(section, name, call, shape, use_when, reason):
    """Register a chart that CANNOT render here, with the honest reason why."""
    CHARTS.append(
        Chart(
            section=section,
            name=name,
            call=call,
            shape=shape,
            use_when=use_when,
            blocked=reason,
        )
    )


# =====================================================================
# COMPARE - "which one is bigger?"
# =====================================================================


@chart(
    "COMPARE", "Bar chart", "px.bar(df, x='agency', y='spend')",
    "One label column + one number, one row per label.",
    "You have a handful of named things with a number each and you want to see which is biggest and by how much.",
    note="px.bar does NOT group by. Duplicate x values stack into segments instead of summing. Pre-aggregate first.",
)
def c_bar():
    return px.bar(d_category(), x="agency", y="spend", color="agency",
                  labels={"spend": "Spend ($m)", "agency": "Agency"})


@chart(
    "COMPARE", "Horizontal bar (ranked)",
    "px.bar(df.sort_values('spend'), x='spend', y='agency', orientation='h')",
    "One label column + one number, and the labels are long words.",
    "Your category names are words, not codes. Sideways labels are readable; rotated ones are not.",
    note="Sorting inverts: an ASCENDING sort puts the biggest bar at the TOP of a horizontal chart.",
)
def c_bar_h():
    d = d_category().sort_values("spend")
    return px.bar(d, x="spend", y="agency", orientation="h", color="agency",
                  labels={"spend": "Spend ($m)", "agency": ""})


@chart(
    "COMPARE", "Grouped bar", "px.bar(df, x='agency', y='spend', color='region', barmode='group')",
    "Two label columns + one number, one row per pair.",
    "Every thing is split the same way and you want to compare the splits side by side rather than as a total.",
)
def c_bar_group():
    return px.bar(d_category_2way(), x="agency", y="spend", color="region", barmode="group",
                  labels={"spend": "Spend ($m)"})


@chart(
    "COMPARE", "Sorted bar via categoryorder",
    "px.bar(...).update_xaxes(categoryorder='total descending')",
    "One label column + one number, in whatever order the query returned.",
    "You want the biggest first and would rather not sort in SQL or pandas. 18 orderings are built in.",
    note="Silent no-op unless the axis resolves to type 'category'. Integer codes on x need .astype(str) first.",
)
def c_bar_sorted():
    d = d_long().groupby("agency", as_index=False)["award"].sum()
    return px.bar(d, x="agency", y="award", color="agency").update_xaxes(
        categoryorder="total descending"
    )


@chart(
    "COMPARE", "Histogram as GROUP BY",
    "px.histogram(df, x='agency', y='award', histfunc='sum')",
    "One category column + one number, un-summarised, many rows per category.",
    "You want a total or average per group and would rather not write the GROUP BY. histfunc does it for you.",
    note="histfunc takes count, sum, avg, min, max.",
)
def c_hist_groupby():
    return px.histogram(d_long(), x="agency", y="award", histfunc="sum", color="agency",
                        labels={"award": "Total awarded ($)"})


@chart(
    "COMPARE", "Box plot (compare groups)", "px.box(df, x='agency', y='award')",
    "One category column + one number, many rows per category.",
    "Comparing averages would lie. You want to see which group runs higher AND which has wild outliers.",
)
def c_box_compare():
    return px.box(d_long(), x="agency", y="award", color="agency", points="outliers",
                  labels={"award": "Award ($)"})


@chart(
    "COMPARE", "Heatmap of a pivot table", "px.imshow(pivot_df, aspect='auto')",
    "An already-shaped grid: rows x columns of numbers (a pivot, or df.corr()).",
    "You have a number for every combination of two things and you want to see which cells run hot.",
    note="imshow colours a grid you already made. density_heatmap bins raw rows for you. Different jobs. Index and column names become the tick labels for free.",
)
def c_imshow():
    g = d_grid(6, 10)
    return px.imshow(g, aspect="auto", color_continuous_scale="Viridis",
                     labels=dict(color="Rate"))


@chart(
    "COMPARE", "Correlation matrix", "px.imshow(df.corr(), text_auto='.2f', zmin=-1, zmax=1)",
    "Several number columns describing the same rows.",
    "You want one number for how strongly every pair moves together, printed in the cell.",
    note="Use a diverging scale pinned at zero. A sequential scale here hides which correlations are negative.",
)
def c_corr():
    return px.imshow(d_numeric_block().corr().round(2), text_auto=".2f",
                     zmin=-1, zmax=1, color_continuous_scale="RdBu", aspect="auto")


@chart(
    "COMPARE", "Heatmap (go.Heatmap, long form)",
    "go.Heatmap(x=cols, y=rows, z=grid, xgap=1, ygap=1)",
    "Two category columns + one number for every pair.",
    "Same question as a pivot heatmap, built by hand so you control the gaps, the cell text and the colour bar.",
)
def c_heatmap():
    g = d_grid(8, 12)
    return go.Figure(
        go.Heatmap(z=g.values, x=list(g.columns), y=list(g.index), xgap=1, ygap=1,
                   colorscale="Viridis", colorbar=dict(title="Rate"))
    )


@chart(
    "COMPARE", "Annotated heatmap", "ff.create_annotated_heatmap(z=grid, x=cols, y=rows)",
    "A small grid of numbers where the exact value matters as much as the colour.",
    "The reader must read numbers off the grid, not eyeball them against a colour ramp.",
)
def c_annotated_heatmap():
    g = d_grid(5, 6)
    fig = ff.create_annotated_heatmap(
        z=g.values.round(0), x=list(g.columns), y=list(g.index),
        colorscale="Viridis", showscale=True,
    )
    fig.update_layout(template="wall")
    fig.update_annotations(font_size=10)
    return fig


@chart(
    "COMPARE", "Contour of a computed grid",
    "go.Contour(z=grid, contours=dict(showlabels=True))",
    "A value already computed across a grid of two inputs (a model surface, a cost function).",
    "You want ridges and valleys, not a cell-by-cell readout. Like elevation rings on a walking map.",
    note="No px route. px.density_contour bins raw points; go.Contour draws a grid you already have.",
)
def c_contour():
    return go.Figure(
        go.Contour(z=d_surface(60), colorscale="Viridis",
                   contours=dict(showlabels=True, labelfont=dict(size=9, color=INK)))
    )


@chart(
    "COMPARE", "Constraint contour (feasible region)",
    "go.Contour(z=grid, contours=dict(type='constraint', operation='[]', value=[0, 3]))",
    "The same computed grid, but the question is pass/fail rather than how much.",
    "You want the shaded area where a condition holds - under a cap, inside a tolerance band.",
    note="operation accepts 13 values including '[]' for 'between these two numbers'.",
)
def c_contour_constraint():
    z = d_surface(60)
    return go.Figure(
        [
            go.Contour(z=z, contours=dict(type="constraint", operation="[]", value=[0, 3]),
                       fillcolor="rgba(90,169,255,0.35)", line=dict(color="#5aa9ff"),
                       name="between 0 and 3", showlegend=True),
            go.Contour(z=z, contours=dict(type="constraint", operation="<", value=-2),
                       fillcolor="rgba(255,123,156,0.35)", line=dict(color="#ff7b9c"),
                       name="below -2", showlegend=True),
        ]
    )


@chart(
    "COMPARE", "Wind rose (polar bar)", "px.bar_polar(df, r='frequency', theta='direction')",
    "A wrap-around category (compass point, hour of day, month) + a number.",
    "Your categories loop back on themselves. On a straight axis December and January sit at opposite ends, which is a lie.",
)
def c_bar_polar():
    return px.bar_polar(d_wind(), r="frequency", theta="direction", color="frequency",
                        color_continuous_scale="Viridis")


@chart(
    "COMPARE", "Dumbbell chart", "2 x go.Scatter + one add_shape line per row",
    "One entity column + exactly two numbers (before and after, budget and actual).",
    "The gap between the two numbers IS the story. The bar's length is the change, read straight off the chart.",
    note="No go.Dumbbell exists. You build it from two scatters and a line shape per row.",
)
def c_dumbbell():
    lab = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
    a = np.array([22.0, 41, 33, 18, 55])
    b = a + np.array([14.0, -6, 21, 9, -12])
    fig = go.Figure()
    for l, x0, x1 in zip(lab, a, b):
        fig.add_shape(type="line", x0=x0, x1=x1, y0=l, y1=l,
                      line=dict(color=MUTED, width=3), layer="below")
    fig.add_trace(go.Scatter(x=a, y=lab, mode="markers", name="2019",
                             marker=dict(size=13, color=CATS[0])))
    fig.add_trace(go.Scatter(x=b, y=lab, mode="markers", name="2024",
                             marker=dict(size=13, color=CATS[1])))
    return fig


@chart(
    "COMPARE", "Lollipop chart", "go.Scatter(mode='markers') + a line shape from zero",
    "One label column + one number, many labels.",
    "Same question as a bar chart, but 30 fat bars is a wall of ink and 30 stalks is not.",
)
def c_lollipop():
    d = d_category().sort_values("spend")
    fig = go.Figure()
    for l, x in zip(d.agency, d.spend):
        fig.add_shape(type="line", x0=0, x1=x, y0=l, y1=l, line=dict(color=MUTED, width=2))
    fig.add_trace(go.Scatter(x=d.spend, y=d.agency, mode="markers",
                             marker=dict(size=15, color=CATS[0]), name="spend"))
    return fig


@chart(
    "COMPARE", "Cleveland dot plot", "two go.Scatter(mode='markers') sharing a category axis",
    "One entity column + two or more comparable numbers.",
    "Several measures per entity, and you want them read against each other without stacking or grouping bars.",
)
def c_cleveland():
    fig = go.Figure()
    for i, (nm, vals) in enumerate(
        [("2023", [40, 62, 31, 25, 18, 12]), ("2024", [52, 55, 44, 21, 29, 15])]
    ):
        fig.add_trace(go.Scatter(x=vals, y=AGENCIES, mode="markers", name=nm,
                                 marker=dict(size=12, color=CATS[i])))
    return fig.update_layout(xaxis_title="Spend ($m)")


@chart(
    "COMPARE", "Marimekko / mosaic", "go.Bar(x=centres, y=share, width=array, offset=0)",
    "Two category columns + a number, where the categories are wildly different sizes.",
    "A 100% stacked bar makes a tiny category shout as loud as a huge one. Bar WIDTH fixes that: width = how big the category is.",
    note="No go.Marimekko. The trick is passing an array to width= and setting offset=0.",
)
def c_marimekko():
    w = np.array([40.0, 25, 20, 15])
    centres = np.cumsum(w) - w / 2
    a = np.array([62.0, 48, 71, 35])
    fig = go.Figure(
        [
            go.Bar(x=centres, y=a, width=w, offset=0, name="Incumbent",
                   marker_color=CATS[0], customdata=REGIONS,
                   hovertemplate="%{customdata}<br>share %{y}%<extra></extra>"),
            go.Bar(x=centres, y=100 - a, width=w, offset=0, name="Challenger",
                   marker_color=CATS[1], customdata=REGIONS,
                   hovertemplate="%{customdata}<br>share %{y}%<extra></extra>"),
        ]
    )
    return fig.update_layout(barmode="stack", bargap=0,
                             xaxis=dict(tickvals=centres, ticktext=REGIONS,
                                        title="Region (width = market size)"),
                             yaxis_title="Share (%)")


@chart(
    "COMPARE", "Two-level category axis",
    "go.Bar(x=[[outer, outer, ...], [inner, inner, ...]])",
    "One number nested under two category levels (quarter, then region).",
    "You want the grouping printed on the axis itself instead of explained in a legend.",
    note="Set by handing x a list of TWO parallel lists. The axis type becomes 'multicategory'.",
)
def c_multicategory():
    outer = sum([[q] * 4 for q in ("Q1", "Q2", "Q3")], [])
    inner = REGIONS * 3
    return go.Figure(
        go.Bar(x=[outer, inner], y=RNG.integers(10, 60, 12), marker_color=CATS[0])
    ).update_layout(xaxis=dict(dividercolor=GRID, dividerwidth=2))


@chart(
    "COMPARE", "Small multiples (facets)", "px.histogram(df, x='award', facet_col='agency')",
    "One number + one or two low-cardinality category columns.",
    "The question is 'does this hold in EVERY group, or only some?' Colour puts them all on one panel and they turn to mush.",
    note="Facets share axes by default. update_yaxes(matches=None) unshares them - a deliberate choice, since unshared panels look comparable and are not.",
    height=310,
)
def c_facets():
    fig = px.histogram(d_long(), x="award", facet_col="agency", facet_col_wrap=3,
                       color="agency", nbins=30)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig.update_layout(showlegend=False)


@chart(
    "COMPARE", "Facet grid (figure factory)",
    "ff.create_facet_grid(df, x='inspections', y='violations', facet_col='region')",
    "Two numbers + a category.",
    "You want faceting but you are not building the figure with plotly express.",
    height=310,
)
def c_ff_facet_grid():
    d = d_scatter(220)
    fig = ff.create_facet_grid(d, x="inspections", y="violations", facet_col="region",
                               marker=dict(size=4, opacity=0.6))
    fig.update_layout(template="wall", showlegend=False)
    return fig


@chart(
    "COMPARE", "Table", "go.Table(header=dict(values=cols), cells=dict(values=[col1, col2]))",
    "Rows and columns, where the exact numbers are the receipt.",
    "A chart of 200 ranked rows is unreadable and a scrollable table is not. Use it beside the chart that summarises it.",
    note="cells.values is COLUMN-major - a list per column. Feeding it rows silently transposes your table.",
)
def c_table():
    d = d_category().sort_values("spend", ascending=False)
    return go.Figure(
        go.Table(
            header=dict(values=["<b>Agency</b>", "<b>Spend ($m)</b>"],
                        fill_color="#1b2230", font=dict(color=INK), align="left", height=30),
            cells=dict(values=[d.agency, d.spend],
                       fill_color=[["#12171f", "#161c26"] * 3], font=dict(color=INK),
                       align="left", height=26, format=[None, ",.0f"]),
        )
    )


@chart(
    "COMPARE", "Table (figure factory)", "ff.create_table(df)",
    "A small dataframe.",
    "You want a styled table in one call and do not care to configure fills and formats yourself.",
)
def c_ff_table():
    d = d_category().sort_values("spend", ascending=False).round(0)
    fig = ff.create_table(d, colorscale=[[0, "#1b2230"], [0.5, "#161c26"], [1, "#12171f"]],
                          font_colors=[INK, INK, INK])
    fig.update_layout(template="wall", margin=dict(l=8, r=8, t=8, b=8))
    return fig


# =====================================================================
# DISTRIBUTE - "how is it spread out?"
# =====================================================================


@chart(
    "DISTRIBUTE", "Histogram", "px.histogram(df, x='award', nbins=50, marginal='box')",
    "One number column, many rows. No categories needed.",
    "You want to know what is typical, how wide the spread runs, and whether the tail is long. Plotly does the counting.",
    note="bargap=0 so the bins touch. A gap implies a gap in the data that is not there. marginal adds a box, violin or rug strip on top.",
)
def c_histogram():
    return px.histogram(d_long(), x="award", nbins=50, marginal="box",
                        labels={"award": "Award ($)"}).update_layout(bargap=0.02)


@chart(
    "DISTRIBUTE", "Histogram, normalised and cumulative",
    "px.histogram(df, x='award', histnorm='percent', cumulative=True)",
    "One number column, many rows, often split by a group.",
    "The question is 'what share of rows sit below X', or two differently-sized groups need comparing fairly on one axis.",
)
def c_histogram_cum():
    return px.histogram(d_long(), x="award", nbins=60, histnorm="percent", cumulative=True,
                        color="agency", opacity=0.6).update_layout(barmode="overlay", bargap=0)


@chart(
    "DISTRIBUTE", "ECDF - the share below any value", "px.ecdf(df, x='award', color='agency')",
    "One number column spread across thousands of entities, especially money.",
    "You want to read off 'what fraction is below THIS amount' for every possible amount at once, with no bins to argue about.",
    note="ecdfnorm: probability / percent / None (raw counts). Two overlaid ECDFs are a fair fight; two overlaid histograms are a mess.",
)
def c_ecdf():
    # render_mode='svg' because px silently switches to WebGL above 1000 points,
    # and a browser only grants a page about 16 WebGL contexts at once.
    return px.ecdf(d_long(), x="award", color="agency", ecdfnorm="percent",
                   render_mode="svg", labels={"award": "Award ($)"})


@chart(
    "DISTRIBUTE", "ECDF, complementary, log-log",
    "px.ecdf(df, x='award', ecdfmode='complementary', log_x=True, log_y=True)",
    "One money-like number across thousands of entities.",
    "The question is concentration: are the top 1% holding half the money? On log-log a power law draws as a STRAIGHT LINE, so a kink is an anomaly you spot with your eye.",
    note="'complementary' flips it to 'what share sit at or ABOVE this value' - the survival curve.",
)
def c_ecdf_ccdf():
    d = d_long()
    return px.ecdf(d[d.award > 0], x="award", ecdfmode="complementary", render_mode="svg",
                   log_x=True, log_y=True, labels={"award": "Award ($)"})


@chart(
    "DISTRIBUTE", "ECDF weighted by a count column", "px.ecdf(df, x='bucket', y='n')",
    "One number + a count/weight column - i.e. rows you already aggregated.",
    "Your warehouse returned one row per unique value with a count beside it. y= weights each row by that count instead of treating it as one.",
)
def c_ecdf_weighted():
    d = d_long().assign(bucket=lambda x: (x.award // 5000 * 5000))
    agg = d.groupby("bucket", as_index=False).size().rename(columns={"size": "n"})
    return px.ecdf(agg, x="bucket", y="n", ecdfnorm="percent",
                   labels={"bucket": "Award bucket ($)", "n": "share of rows"})


@chart(
    "DISTRIBUTE", "Box plot", "px.box(df, x='agency', y='award', notched=True)",
    "One number column, optionally split by a category.",
    "Where is the middle, how wide is the middle half, and who is a straggler. Box = 25th to 75th percentile, line = median.",
    note="points: 'outliers' (default), 'suspectedoutliers', 'all', False. If two notches do not overlap, the medians differ meaningfully - a significance test you read by eye.",
)
def c_box():
    return px.box(d_long(), x="agency", y="award", color="agency", notched=True,
                  points="suspectedoutliers", labels={"award": "Award ($)"})


@chart(
    "DISTRIBUTE", "Box from pre-computed quartiles",
    "go.Box(q1=..., median=..., q3=..., lowerfence=..., upperfence=...)",
    "Five summary numbers per group, computed in SQL. NOT raw rows.",
    "You have 800 million rows. Run APPROX_PERCENTILE in the warehouse and ship five numbers per group instead of ten million.",
    note="Same picture, roughly 7 KB instead of 2.7 MB. The single biggest scale lever in the library.",
)
def c_box_precomputed():
    g = d_long().groupby("agency")["award"]
    q = pd.DataFrame(
        {"q1": g.quantile(0.25), "median": g.median(), "q3": g.quantile(0.75),
         "lo": g.quantile(0.02), "hi": g.quantile(0.98), "mean": g.mean()}
    ).reset_index()
    return go.Figure(
        go.Box(x=q.agency, q1=q.q1, median=q["median"], q3=q.q3,
               lowerfence=q.lo, upperfence=q.hi, mean=q["mean"],
               marker_color=CATS[0], name="award")
    ).update_layout(yaxis_title="Award ($)")


@chart(
    "DISTRIBUTE", "Violin", "px.violin(df, x='group', y='score', box=True)",
    "One number split by a category, where you suspect the shape is lumpy.",
    "A box plot hides two humps completely. A violin's width at each height is how many rows sit at that value, so two humps show as two bulges.",
    note="scalemode='count' makes fatness proportional to how many rows are in the group. The default makes a group of 12 shout as loud as a group of 12,000.",
)
def c_violin():
    return px.violin(d_bimodal(), x="group", y="score", color="group", box=True, points=False)


@chart(
    "DISTRIBUTE", "Split violin (back to back)",
    "go.Violin(side='negative') + go.Violin(side='positive'), violinmode='overlay'",
    "One number, one grouping category, and one two-value split (year, region, before/after).",
    "You want two distributions compared on the exact same axis with no eye travel between panels.",
)
def c_violin_split():
    d = d_long()
    fig = go.Figure()
    for side, region, colour in (("negative", "North", CATS[0]), ("positive", "South", CATS[1])):
        sub = d[d.region == region]
        fig.add_trace(go.Violin(x=sub.agency, y=sub.award, side=side, name=region,
                                line_color=colour, fillcolor=colour, opacity=0.6,
                                points=False, scalemode="count"))
    return fig.update_layout(violinmode="overlay", violingap=0.15, yaxis_title="Award ($)")


@chart(
    "DISTRIBUTE", "Ridgeline", "stacked go.Violin(side='positive', orientation='h'), violingap=0",
    "One number + one category with 5-40 levels (states, years, agencies).",
    "50 states as bars is 50 numbers. 50 states as ridges is 50 DISTRIBUTIONS - fat right tails versus fat middles, which is the difference between one bad actor and a systemic policy.",
    note="No go.Ridgeline. violingap=0 is the load-bearing trick that fuses the ridges into one landscape. On a log x-axis you must set an explicit range: the smoothed curve runs past zero, and the log of a negative number is undefined, which silently breaks the gridlines.",
    height=380,
)
def c_ridgeline():
    d = d_long()
    fig = go.Figure()
    for i, a in enumerate(AGENCIES):
        # Log the DATA, not the axis - see the note above.
        vals = np.log10(d.loc[d.agency == a, "award"].clip(lower=1))
        fig.add_trace(
            go.Violin(x=vals, name=a, side="positive", orientation="h", width=3,
                      points=False, line_color=CATS[i % len(CATS)],
                      fillcolor=CATS[i % len(CATS)], opacity=0.6,
                      hovertemplate="%{x:.2f} (log10 $)<extra>" + a + "</extra>")
        )
    decades = [3, 4, 5]
    return fig.update_layout(
        violingap=0, violingroupgap=0, showlegend=False,
        xaxis=dict(title="Award ($, log scale)", range=[2.7, 5.3],
                   tickvals=decades, ticktext=[f"${10 ** k:,.0f}" for k in decades]),
    )


@chart(
    "DISTRIBUTE", "Strip plot - every single row", "px.strip(df, x='agency', y='award')",
    "One number + one category, with fewer than about 500 rows per category.",
    "Summarising five points would be a lie, and you want to be able to point at ONE dot and name it.",
    note="px.strip is secretly a box trace with the box made invisible (boxpoints='all', transparent fill and line).",
)
def c_strip():
    d = d_long().groupby("agency", group_keys=False).sample(45, random_state=1)
    return px.strip(d, x="agency", y="award", color="agency", labels={"award": "Award ($)"})


@chart(
    "DISTRIBUTE", "Beeswarm", "go.Scatter(x=values, y=small random jitter, mode='markers')",
    "One number column, a few hundred rows.",
    "Same as a strip plot but you control the jitter, so overlapping points spread out instead of stacking into a solid stripe.",
)
def c_beeswarm():
    v = d_long().award.sample(400, random_state=2).to_numpy()
    return go.Figure(
        go.Scatter(x=v, y=RNG.normal(0, 0.09, v.size), mode="markers",
                   marker=dict(size=5, opacity=0.55, color=CATS[0]))
    ).update_layout(yaxis=dict(visible=False), xaxis_title="Award ($)")


@chart(
    "DISTRIBUTE", "Raincloud", "go.Violin(side='positive') + go.Box + jittered go.Scatter",
    "One number column, a few hundred rows.",
    "You want the shape, the summary and the raw rows all at once, so nobody can accuse the summary of hiding something.",
)
def c_raincloud():
    v = d_long().award.sample(350, random_state=3).to_numpy()
    return go.Figure(
        [
            go.Violin(x=v, side="positive", points=False, width=1.4, y0=0.45,
                      line_color=CATS[0], fillcolor=CATS[0], opacity=0.5, name="shape"),
            go.Box(x=v, y=["summary"] * v.size, boxpoints=False, width=0.22,
                   marker_color=CATS[1], name="summary"),
            go.Scatter(x=v, y=RNG.normal(-0.35, 0.05, v.size), mode="markers",
                       marker=dict(size=4, opacity=0.45, color=CATS[2]), name="rows"),
        ]
    ).update_layout(yaxis=dict(visible=False), xaxis_title="Award ($)", showlegend=False)


@chart(
    "DISTRIBUTE", "2D density heatmap",
    "px.density_heatmap(df, x='inspections', y='violations', nbinsx=40, nbinsy=40)",
    "Two number columns with far too many rows to plot as dots.",
    "The scatter has gone to a solid blob. This bins both axes and colours the cells, so you can see the blob's interior.",
    note="No color= parameter - the colour channel is already spent on density. Its sibling density_contour does have one.",
)
def c_density_heatmap():
    d = d_scatter(4000)
    fig = px.density_heatmap(d, x="inspections", y="violations", nbinsx=40, nbinsy=40,
                             marginal_x="histogram", marginal_y="histogram")
    # Set the scale AFTER the fact: passing color_continuous_scale alongside
    # marginals tries to hand the scale name to the marginal traces' marker.color.
    return fig.update_coloraxes(colorscale="Viridis")


@chart(
    "DISTRIBUTE", "2D density contour",
    "px.density_contour(df, x='inspections', y='violations', color='region')",
    "Two number columns plus a group you want to overlay.",
    "Same binning as the density heatmap, drawn as rings. Better for asking whether two clouds sit in different places.",
)
def c_density_contour():
    return px.density_contour(d_scatter(2500), x="inspections", y="violations", color="region")


@chart(
    "DISTRIBUTE", "2D density (figure factory)", "ff.create_2d_density(x, y)",
    "Two number columns, many rows.",
    "You want the scatter, the contours and both edge histograms assembled for you in one call.",
)
def c_ff_2d_density():
    d = d_scatter(1500)
    fig = ff.create_2d_density(d.inspections, d.violations, colorscale="Viridis", point_size=3)
    fig.update_layout(template="wall", showlegend=False)
    return fig


@chart(
    "DISTRIBUTE", "Isosurface - the 3D threshold shell",
    "go.Isosurface(x, y, z, value=..., isomin=..., isomax=...)",
    "Four equal-length arrays: x, y, z positions and a value at each - a 3D grid.",
    "A number measured throughout a volume (concentration, temperature, dose) and you want the boundary of the hot zone.",
)
def c_isosurface():
    x, y, z, v = d_volume(14)
    return go.Figure(
        go.Isosurface(x=x, y=y, z=z, value=v, isomin=1.5, isomax=4.0, surface_count=3,
                      opacity=0.5, colorscale="Viridis",
                      caps=dict(x_show=False, y_show=False, z_show=False))
    )


@chart(
    "DISTRIBUTE", "Volume - the whole 3D cloud",
    "go.Volume(x, y, z, value=..., opacity=0.12, surface_count=16)",
    "The same four arrays as isosurface.",
    "You want the whole gradient rather than one boundary. Many nested shells at once.",
    note="Untuned you get fog. opacityscale is what makes the low-value regions see-through.",
)
def c_volume():
    x, y, z, v = d_volume(14)
    return go.Figure(
        go.Volume(x=x, y=y, z=z, value=v, isomin=0.4, isomax=5.0, opacity=0.12,
                  surface_count=16, colorscale="Viridis")
    )


blocked(
    "DISTRIBUTE", "Distplot (histogram + smooth curve + rug)",
    "ff.create_distplot([values], ['label'])",
    "One or more number columns.",
    "You want a histogram with a smoothed curve over it plus a rug - one tick mark per row along the axis, so you see individual rows and the shape together.",
    "Needs scipy, which is not installed here. `pip install scipy` unblocks it. "
    "px.histogram(marginal='rug') plus px.violin(box=True) covers most of it with no extra package.",
)

blocked(
    "DISTRIBUTE", "Violin with smoothed curve (figure factory)",
    "ff.create_violin(df, data_header='v', group_header='g')",
    "One number + one grouping column.",
    "The figure-factory violin recipe, with the smoothing computed in Python rather than the browser.",
    "Needs scipy. go.Violin and px.violin work fine without it - that curve is computed by JavaScript in the browser.",
)


# =====================================================================
# RELATE - "does X track Y?"
# =====================================================================


@chart(
    "RELATE", "Scatter plot", "px.scatter(df, x='inspections', y='violations', color='region')",
    "Two number columns, one row per thing.",
    "Do these two move together, and who are the weirdos sitting far from the pack?",
    note="px.scatter has the most options of any px function (49). It silently switches to WebGL rendering above 1000 points.",
)
def c_scatter():
    return px.scatter(d_scatter(600), x="inspections", y="violations", color="region",
                      opacity=0.7)


@chart(
    "RELATE", "Scatter with edge distributions",
    "px.scatter(df, x=..., y=..., marginal_x='histogram', marginal_y='violin')",
    "Two number columns, one row per thing.",
    "You want the relationship AND each number's own spread, without building three charts and lining them up.",
    note="marginal_x / marginal_y exist on exactly 3 functions: scatter, density_contour, density_heatmap.",
)
def c_scatter_marginal():
    return px.scatter(d_scatter(700), x="inspections", y="violations",
                      marginal_x="histogram", marginal_y="violin", opacity=0.55)


@chart(
    "RELATE", "Scatter with a trend line",
    "px.scatter(df, x=..., y=..., trendline='rolling', trendline_options=dict(window=40))",
    "Two number columns where one is naturally ordered.",
    "The cloud has a direction and you want it drawn, not guessed at.",
    note="trendline='ols' and 'lowess' need statsmodels, which is NOT installed here. rolling / expanding / ewm are pure pandas and work now.",
)
def c_scatter_trend():
    d = d_scatter(500).sort_values("inspections")
    return px.scatter(d, x="inspections", y="violations", trendline="rolling",
                      trendline_options=dict(window=40), trendline_color_override=CATS[3],
                      opacity=0.45)


@chart(
    "RELATE", "Bubble chart", "px.scatter(df, x=..., y=..., size='employees', color='fines')",
    "Two numbers on the axes plus a third as dot size and a fourth as colour.",
    "Four variables at once, and the question is which entities are extreme on several of them together.",
    note="Set marker.sizemode='area' or big values visually lie - a doubled radius is a quadrupled blob.",
)
def c_bubble():
    d = d_scatter(180)
    return px.scatter(d, x="inspections", y="violations", size="employees", color="fines",
                      size_max=34, color_continuous_scale="Viridis", opacity=0.7)


@chart(
    "RELATE", "WebGL scatter (huge point counts)",
    "px.scatter(df, x=..., y=..., render_mode='webgl')  # or go.Scattergl(...)",
    "Two number columns with tens of thousands of rows.",
    "Same question as a plain scatter, but the page has gone sticky. This draws on the graphics card instead.",
    note="Fewer styling options than plain scatter (66 props vs 77) and it rasterises on PDF export. Casting to float32 first halves the bytes shipped to the browser - measured 562 KB down to 283 KB for these 25,000 points.",
)
def c_scattergl():
    d = d_scatter(25000).astype({"inspections": "float32", "violations": "float32"})
    return px.scatter(d, x="inspections", y="violations", render_mode="webgl",
                      opacity=0.25).update_traces(marker=dict(size=3))


@chart(
    "RELATE", "Quadrant scatter",
    "px.scatter(...).add_hline(y=median).add_vline(x=median)",
    "Two number columns plus a rule about what counts as high.",
    "You want to name a corner - 'high fines AND low inspections' - rather than describe a slope.",
)
def c_quadrant():
    d = d_scatter(400)
    mx, my = d.inspections.median(), d.violations.median()
    fig = px.scatter(d, x="inspections", y="violations", opacity=0.55)
    fig.add_hline(y=my, line_dash="dot", line_color=MUTED)
    fig.add_vline(x=mx, line_dash="dot", line_color=MUTED)
    fig.add_annotation(x=d.inspections.max(), y=d.violations.max(), text="high / high",
                       showarrow=False, xanchor="right", font=dict(color=CATS[3]))
    fig.add_annotation(x=d.inspections.min(), y=d.violations.max(), text="low insp / high viol",
                       showarrow=False, xanchor="left", font=dict(color=CATS[1]))
    return fig


@chart(
    "RELATE", "Scatter plot matrix (splom)",
    "px.scatter_matrix(df, dimensions=[...])",
    "Four to eight number columns describing the same rows, no hypothesis yet.",
    "Which PAIRS of these are related at all? Every column plotted against every other, in one grid.",
    note="Ships with dragmode='select' - lasso in one cell and the same rows highlight in every other cell.",
    height=420,
)
def c_splom():
    d = d_numeric_block(260)
    return px.scatter_matrix(d, dimensions=["inspections", "violations", "fines", "risk"],
                             opacity=0.5).update_traces(diagonal_visible=False,
                                                        showupperhalf=False, marker_size=4)


@chart(
    "RELATE", "Scatterplot matrix (figure factory)",
    "ff.create_scatterplotmatrix(df, diag='histogram')",
    "Several number columns on the same rows.",
    "Same question as a splom, assembled from ordinary scatter and histogram traces so you can restyle every panel.",
    height=420,
)
def c_ff_splom():
    d = d_numeric_block(200)[["inspections", "violations", "risk"]]
    fig = ff.create_scatterplotmatrix(d, diag="histogram", height=420, width=None)
    fig.update_layout(template="wall", showlegend=False)
    return fig


@chart(
    "RELATE", "Parallel coordinates",
    "px.parallel_coordinates(df, dimensions=[...], color='risk')",
    "One row per entity and four to ten NUMBER columns.",
    "Which entities are high on several measures at once? No scatter answers that past two columns.",
    note="Drag a bracket on any axis and every line outside it greys out - a live multi-column WHERE clause. Warning: it has no hover tooltips.",
)
def c_parcoords():
    d = d_numeric_block(400)
    return px.parallel_coordinates(
        d, dimensions=["inspections", "violations", "fines", "employees", "risk"],
        color="risk", color_continuous_scale="Viridis",
    )


@chart(
    "RELATE", "Parallel coordinates with a locked filter",
    "go.Parcoords(dimensions=[dict(label=..., values=..., constraintrange=[20, 50])])",
    "The same shape, but you want the page to open already filtered.",
    "You are publishing a finding and want the reader to land on the subset that matters, still able to widen it.",
)
def c_parcoords_constrained():
    d = d_numeric_block(400)
    return go.Figure(
        go.Parcoords(
            line=dict(color=d.risk, colorscale="Viridis", showscale=True),
            dimensions=[
                dict(label="inspections", values=d.inspections, constraintrange=[42, 60]),
                dict(label="violations", values=d.violations),
                dict(label="fines", values=d.fines),
                dict(label="risk", values=d.risk),
            ],
        )
    )


@chart(
    "RELATE", "3D scatter", "px.scatter_3d(df, x=..., y=..., z=..., color=...)",
    "Three number columns per row.",
    "Do all three move together, and do the rows split into clumps you cannot see in two dimensions?",
    note="Honest warning: a 2D scatter with colour and size encodes four columns and is easier to read. Use 3D only when the reader can rotate it.",
)
def c_scatter3d():
    d = d_numeric_block(300)
    return px.scatter_3d(d, x="inspections", y="violations", z="fines", color="risk",
                         color_continuous_scale="Viridis", opacity=0.7).update_traces(
        marker_size=4
    )


@chart(
    "RELATE", "3D line", "px.line_3d(df, x=..., y=..., z=...)",
    "Three numbers in sequence.",
    "What path does this trace through three-dimensional space? A trajectory, not a cloud.",
)
def c_line3d():
    t = np.linspace(0, 12 * np.pi, 500)
    d = pd.DataFrame({"x": np.cos(t) * t / 8, "y": np.sin(t) * t / 8, "z": t})
    return px.line_3d(d, x="x", y="y", z="z")


@chart(
    "RELATE", "3D ribbon (filled 3D line)",
    "go.Scatter3d(mode='lines', surfaceaxis=1, surfacecolor='...')",
    "Three numbers in sequence, where one dimension is a baseline.",
    "The 3D equivalent of an area chart: drop a filled wall from the line down to a plane so the depth reads.",
    note="surfaceaxis takes -1, 0, 1 or 2. It is the only thing separating a 3D line from a 3D ribbon.",
)
def c_scatter3d_ribbon():
    fig = go.Figure()
    x = np.linspace(0, 10, 80)
    for i, off in enumerate((0, 2, 4)):
        fig.add_trace(
            go.Scatter3d(x=x, y=np.full_like(x, off), z=np.sin(x + i) + 1.5,
                         mode="lines", surfaceaxis=1, surfacecolor=CATS[i],
                         line=dict(color=CATS[i], width=4), name=f"series {i + 1}")
        )
    return fig


@chart(
    "RELATE", "Surface", "go.Surface(z=grid)",
    "A value computed over a grid of two inputs.",
    "You want the shape of the response - where the peak is, how steep the sides run.",
    note="No px route. contours= projects lines onto the surface or the walls of the box.",
)
def c_surface():
    return go.Figure(
        go.Surface(z=d_surface(50), colorscale="Viridis",
                   contours=dict(z=dict(show=True, usecolormap=True, project_z=True)))
    )


@chart(
    "RELATE", "Mesh3d - a solid from a point cloud",
    "go.Mesh3d(x, y, z, alphahull=5)",
    "A 3D point cloud, or explicit vertices plus triangle indices.",
    "You have points in space and want them skinned into a solid shape rather than left as dots.",
    note="Three routes in: explicit i/j/k triangles, alphahull to auto-wrap a shell, or delaunayaxis for roughly-flat points.",
)
def c_mesh3d():
    n = 220
    u, v = RNG.random(n) * 2 * np.pi, np.arccos(2 * RNG.random(n) - 1)
    r = 1 + 0.25 * np.sin(3 * u) * np.sin(2 * v)
    return go.Figure(
        go.Mesh3d(x=r * np.sin(v) * np.cos(u), y=r * np.sin(v) * np.sin(u), z=r * np.cos(v),
                  alphahull=3, opacity=0.75, colorscale="Viridis", intensity=r,
                  flatshading=False)
    )


@chart(
    "RELATE", "Trisurf (figure factory)",
    "ff.create_trisurf(x, y, z, simplices=triangles)",
    "3D points plus an explicit list of which three points make each triangle.",
    "You already computed a triangulation and want it coloured and shaded in one call.",
)
def c_ff_trisurf():
    n = 90
    u = np.linspace(0, 2 * np.pi, 10)
    w = np.linspace(0, 2 * np.pi, 9)
    uu, ww = np.meshgrid(u, w)
    uu, ww = uu.ravel(), ww.ravel()
    x, y, z = (2 + np.cos(ww)) * np.cos(uu), (2 + np.cos(ww)) * np.sin(uu), np.sin(ww)
    simp = np.array([[i, (i + 1) % n, (i + 10) % n] for i in range(n)])
    fig = ff.create_trisurf(x=x, y=y, z=z, simplices=simp, colormap="Viridis",
                            show_colorbar=False, title="")
    fig.update_layout(template="wall")
    return fig


@chart(
    "RELATE", "Radar / spider chart",
    "go.Scatterpolar(r=[...], theta=[...], fill='toself')",
    "Five to eight comparable measures for one to three entities.",
    "What is this entity's SILHOUETTE, and is that one a different shape? Two entities with the same total can look completely different.",
    note="No go.Radar. Repeat the first point at the end to close the loop, or use px.line_polar(line_close=True). polar.gridshape='linear' gives the polygonal grid.",
)
def c_radar():
    axes = ["Inspections", "Violations", "Fines", "Repeat rate", "Backlog", "Appeals"]
    fig = go.Figure()
    for i, (nm, vals) in enumerate(
        [("Alpha Co", [8, 6, 9, 3, 5, 4]), ("Beta LLC", [4, 9, 3, 8, 7, 6])]
    ):
        fig.add_trace(go.Scatterpolar(r=vals + vals[:1], theta=axes + axes[:1],
                                      fill="toself", name=nm, line_color=CATS[i],
                                      opacity=0.75))
    return fig.update_layout(polar=dict(gridshape="linear",
                                        radialaxis=dict(range=[0, 10])))


@chart(
    "RELATE", "Polar scatter / line", "px.line_polar(df, r='frequency', theta='direction', line_close=True)",
    "A cyclical category or angle + a number.",
    "The x axis wraps around - hour of day, month, compass bearing - and you want that wrap drawn honestly.",
)
def c_polar():
    d = d_wind()
    return px.line_polar(d, r="frequency", theta="direction", line_close=True,
                         markers=True)


@chart(
    "RELATE", "Polar scatter, WebGL",
    "px.scatter_polar(df, r=..., theta=..., render_mode='webgl')",
    "The same polar shape with tens of thousands of points.",
    "The polar chart has gone sticky. Same trick as scattergl, on a circle.",
)
def c_scatterpolargl():
    n = 6000
    return px.scatter_polar(r=RNG.gamma(3, 2, n), theta=RNG.random(n) * 360,
                            render_mode="webgl", opacity=0.3).update_traces(marker_size=3)


@chart(
    "RELATE", "Two units on one x axis (secondary y)",
    "make_subplots(specs=[[{'secondary_y': True}]])",
    "Two numbers on very different scales sharing one x axis.",
    "A 0-1 rate plotted against a 30,000 count flattens to a dead line on the floor. Give it its own axis.",
    note="Honest warning: dual axes can manufacture a correlation that is not there, purely by choosing the two ranges.",
)
def c_secondary_y():
    d = d_timeseries(180)
    m = d[d.region == "North"].reset_index(drop=True)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=m.date, y=m.claims, name="claims (count)",
                         marker_color=CATS[0], opacity=0.6), secondary_y=False)
    fig.add_trace(go.Scatter(x=m.date, y=m.claims / m.claims.max(), name="approval rate",
                             line=dict(color=CATS[1], width=2)), secondary_y=True)
    fig.update_yaxes(title_text="claims", secondary_y=False)
    fig.update_yaxes(title_text="rate", secondary_y=True, showgrid=False,
                     tickformat=".0%")
    return fig


@chart(
    "RELATE", "Smith chart", "go.Scattersmith(real=[...], imag=[...])",
    "Complex numbers from radio-frequency or transmission-line measurements.",
    "Electrical impedance. Outside RF engineering this has essentially no use - it is here so nothing is hidden from you.",
)
def c_scattersmith():
    n = 60
    return go.Figure(
        go.Scattersmith(real=RNG.gamma(2, 0.4, n), imag=RNG.normal(0, 0.7, n),
                        mode="markers", marker=dict(size=7, color=CATS[0]))
    )


@chart(
    "RELATE", "Carpet - the graph paper itself",
    "go.Carpet(a=..., b=..., x=..., y=...)",
    "Two independent variables that are not perpendicular - moving A also shifts where B sits.",
    "Engineering and aerodynamics charts. On its own a carpet draws almost nothing: it is the warped grid other traces sit on.",
    note="No hover. If you are not doing engineering charts with non-perpendicular variables you will never need this.",
)
def c_carpet():
    a = np.tile(np.linspace(0, 4, 5), 4)
    b = np.repeat(np.linspace(1, 4, 4), 5)
    return go.Figure(
        go.Carpet(a=a, b=b, x=a + b * 0.35, y=b * 1.4 + np.sin(a) * 0.6, carpet="grid1",
                  aaxis=dict(gridcolor=GRID, title="a"),
                  baxis=dict(gridcolor=GRID, title="b"))
    )


@chart(
    "RELATE", "Scattercarpet - points on a warped grid",
    "go.Carpet(carpet='c1') + go.Scattercarpet(a=..., b=..., carpet='c1')",
    "Readings taken at (a, b) positions on a non-perpendicular grid.",
    "Same as a scatter, but the coordinate system itself is warped, so the dot's position means something the axes cannot show.",
    note="Requires a go.Carpet trace with a matching carpet id already in the figure.",
)
def c_scattercarpet():
    a = np.tile(np.linspace(0, 4, 5), 4)
    b = np.repeat(np.linspace(1, 4, 4), 5)
    return go.Figure(
        [
            go.Carpet(a=a, b=b, x=a + b * 0.35, y=b * 1.4 + np.sin(a) * 0.6, carpet="c1",
                      aaxis=dict(gridcolor=GRID), baxis=dict(gridcolor=GRID)),
            go.Scattercarpet(a=[0.5, 1.6, 2.8, 3.4], b=[1.4, 2.2, 3.1, 3.8], carpet="c1",
                             mode="markers+lines", marker=dict(size=10, color=CATS[1]),
                             line=dict(color=CATS[1]), name="run 1"),
        ]
    )


@chart(
    "RELATE", "Contourcarpet - contours on a warped grid",
    "go.Carpet(carpet='c1') + go.Contourcarpet(a=..., b=..., z=..., carpet='c1')",
    "A value measured across a non-perpendicular grid.",
    "The contour version of the above. Also has no hover.",
)
def c_contourcarpet():
    a = np.tile(np.linspace(0, 4, 5), 4)
    b = np.repeat(np.linspace(1, 4, 4), 5)
    return go.Figure(
        [
            go.Carpet(a=a, b=b, x=a + b * 0.35, y=b * 1.4 + np.sin(a) * 0.6, carpet="c1",
                      aaxis=dict(gridcolor=GRID), baxis=dict(gridcolor=GRID)),
            go.Contourcarpet(a=a, b=b, z=(a * 2 + b**1.4), carpet="c1",
                             colorscale="Viridis", contours=dict(showlines=True)),
        ]
    )


blocked(
    "RELATE", "Ordinary-least-squares / lowess trend line",
    "px.scatter(df, x=..., y=..., trendline='ols')",
    "Two number columns.",
    "The straight-line fit everybody reaches for, plus the R-squared you get from px.get_trendline_results(fig).",
    "Needs statsmodels, which is NOT installed here. Both 'ols' and 'lowess' raise ModuleNotFoundError. "
    "`pip install statsmodels` unblocks them. trendline='rolling' / 'expanding' / 'ewm' work today - see the chart above.",
)

blocked(
    "RELATE", "Dendrogram (clustering tree)",
    "ff.create_dendrogram(matrix)",
    "A matrix of rows to be clustered.",
    "You want to see which rows group together and at what distance they merge - the tree above a clustered heatmap.",
    "Needs scipy. `pip install scipy` unblocks it. A treemap or icicle covers a hierarchy you already know; "
    "the dendrogram is for one you want DISCOVERED.",
)


# =====================================================================
# COMPOSE - "what is it made of?"
# =====================================================================


@chart(
    "COMPOSE", "Pie / donut", "px.pie(df, names='agency', values='spend', hole=0.45)",
    "One category column + one number that genuinely sums to a real whole, under about six slices.",
    "Roughly what share is each? Past six slices nobody can read it - use a sorted bar instead.",
    note="The only part-of-whole chart in px that facets. hole= makes it a donut, which at least puts a number in the middle.",
)
def c_pie():
    return px.pie(d_category(), names="agency", values="spend", hole=0.45).update_traces(
        textposition="inside", textinfo="percent+label"
    )


@chart(
    "COMPOSE", "Stacked bar", "px.bar(df, x='agency', y='spend', color='region')",
    "One category column + a subcategory + a number.",
    "You want the total AND what is inside each total, for several things at once.",
)
def c_bar_stacked():
    return px.bar(d_category_2way(), x="agency", y="spend", color="region",
                  labels={"spend": "Spend ($m)"})


@chart(
    "COMPOSE", "100% stacked bar", "px.bar(...).update_layout(barnorm='percent')",
    "The same shape, when the totals differ wildly.",
    "The question is whether the MIX differs, not the size. Every bar becomes the same height and shows share.",
    note="This throws the total away. Only do it when the total genuinely does not matter to the question.",
)
def c_bar_barnorm():
    return px.bar(d_category_2way(), x="agency", y="spend", color="region").update_layout(
        barnorm="percent", yaxis_title="Share of agency spend (%)"
    )


@chart(
    "COMPOSE", "Area chart", "px.area(df, x='date', y='claims', color='region')",
    "A date column + a category + a number.",
    "How did the total change, and how did the mix inside it change, at the same time?",
    note="px.area is px.line plus two properties: stackgroup=1 and mode='lines'. That is the entire difference.",
)
def c_area():
    return px.area(d_timeseries(240), x="date", y="claims", color="region")


@chart(
    "COMPOSE", "100% stacked area", "px.area(df, ..., groupnorm='fraction')",
    "A date column + a category + a number.",
    "Is one player's SHARE growing? This strips out total growth so composition is the only signal left.",
)
def c_area_norm():
    return px.area(d_timeseries(240), x="date", y="claims", color="region",
                   groupnorm="fraction").update_layout(yaxis_tickformat=".0%",
                                                       yaxis_title="Share")


@chart(
    "COMPOSE", "Streamgraph", "go.Scatter(stackgroup='one', mode='none') per series",
    "A date column + several categories + a number.",
    "Many categories over time where the rise and fall of each band is the story, not exact values.",
    note="Same stacking as an area chart, drawn centred rather than sitting on a baseline.",
)
def c_streamgraph():
    d = d_timeseries(240)
    fig = go.Figure()
    for i, r in enumerate(REGIONS):
        s = d[d.region == r]
        fig.add_trace(go.Scatter(x=s.date, y=s.claims, stackgroup="one", mode="none",
                                 name=r, fillcolor=CATS[i], hoverinfo="x+y+name"))
    return fig.update_layout(yaxis=dict(visible=False))


@chart(
    "COMPOSE", "Treemap", "px.treemap(df, path=['agency', 'program', 'vendor'], values='amount')",
    "Nested category columns (broad to narrow) + a number.",
    "Where inside a structure is the mass? Nested rectangles sized by value. Best of the three when comparing SIZES.",
    note="branchvalues: px sets 'total' for you when you use path=. Building go.Treemap by hand, the default is 'remainder' - and if your SQL already returns parent totals that double-counts silently.",
    height=380,
)
def c_treemap():
    return px.treemap(d_hierarchy(), path=["agency", "program", "vendor"], values="amount",
                      color="amount", color_continuous_scale="Viridis")


@chart(
    "COMPOSE", "Sunburst", "px.sunburst(df, path=[...], values='amount')",
    "The same nested columns + a number.",
    "Same question as a treemap, when the DEPTH of the nesting is the story. Concentric rings out from the centre.",
    note="textinfo='label+percent parent' prints what share each slice is of its own parent - how you find 'one vendor is 80% of one programme'.",
    height=380,
)
def c_sunburst():
    return px.sunburst(d_hierarchy(), path=["agency", "program", "vendor"], values="amount",
                       color="amount", color_continuous_scale="Viridis").update_traces(
        textinfo="label+percent parent"
    )


@chart(
    "COMPOSE", "Icicle", "px.icicle(df, path=[...], values='amount')",
    "The same nested columns + a number.",
    "Same question again, when the labels are long words that need horizontal room, or the tree is deep and narrow.",
    height=380,
)
def c_icicle():
    return px.icicle(d_hierarchy(), path=["agency", "program", "vendor"], values="amount",
                     color="amount", color_continuous_scale="Viridis")


@chart(
    "COMPOSE", "Flame graph", "go.Icicle(tiling=dict(orientation='v', flip='y'))",
    "The same hierarchy, when you want the root at the BOTTOM.",
    "The profiler's view - root at the bottom, children stacking upward. This orientation is the actual reason to pick icicle over treemap.",
    note="tiling.orientation takes 'v' or 'h'; tiling.flip takes 'x' and/or 'y'.",
    height=380,
)
def c_flamegraph():
    d = d_hierarchy()
    labels, parents, values = ["all"], [""], [float(d.amount.sum())]
    for a, g in d.groupby("agency"):
        labels.append(a); parents.append("all"); values.append(float(g.amount.sum()))
        for p, gg in g.groupby("program"):
            key = f"{a}/{p}"
            labels.append(key); parents.append(a); values.append(float(gg.amount.sum()))
            for _, row in gg.iterrows():
                labels.append(f"{key}/{row.vendor}"); parents.append(key)
                values.append(float(row.amount))
    return go.Figure(
        go.Icicle(labels=labels, parents=parents, values=values, branchvalues="total",
                  tiling=dict(orientation="v", flip="y"),
                  marker=dict(colorscale="Viridis", colors=values))
    )


@chart(
    "COMPOSE", "Funnel area", "px.funnel_area(names=stages, values=counts)",
    "Ordered stages + shrinking counts.",
    "Same data as a funnel, drawn as a cone in its own box so it sits next to pies rather than on axes.",
)
def c_funnelarea():
    d = d_stages()
    return px.funnel_area(names=d.stage, values=d.cases)


@chart(
    "COMPOSE", "Ternary scatter", "px.scatter_ternary(df, a='federal', b='state', c='private')",
    "Three numbers per row that are parts of one whole.",
    "Who is balanced, who is lopsided, and do the lopsided ones cluster? The ONLY chart that shows three-way composition for many entities at once.",
    note="Dead centre means one third each. A stacked bar can only show a handful of entities; this shows hundreds.",
)
def c_ternary():
    return px.scatter_ternary(d_ternary(), a="federal", b="state", c="private",
                              color="region", opacity=0.7)


@chart(
    "COMPOSE", "Ternary line", "px.line_ternary(df, a=..., b=..., c=...)",
    "The same three-part mix, in sequence.",
    "How did the three-way split DRIFT over time - did it move toward one corner?",
)
def c_line_ternary():
    n = 40
    t = np.linspace(0, 1, n)
    d = pd.DataFrame({"year": np.arange(1985, 1985 + n),
                      "federal": 60 - 30 * t + RNG.normal(0, 1.5, n),
                      "state": 25 + 5 * t + RNG.normal(0, 1.5, n),
                      "private": 15 + 25 * t + RNG.normal(0, 1.5, n)})
    return px.line_ternary(d, a="federal", b="state", c="private", markers=True)


@chart(
    "COMPOSE", "Waffle / unit chart", "go.Heatmap(z=100_cell_grid, xgap=3, ygap=3)",
    "One category column + a share of 100.",
    "Percentages that a reader should be able to COUNT. One square is one percent, so 37% is 37 countable squares.",
)
def c_waffle():
    shares = [37, 28, 20, 15]
    names = REGIONS
    g = np.zeros(100)
    start = 0
    for i, s in enumerate(shares):
        g[start:start + s] = i
        start += s
    return go.Figure(
        go.Heatmap(z=g.reshape(10, 10), xgap=4, ygap=4, showscale=False,
                   colorscale=[[i / (len(shares) - 1), CATS[i]] for i in range(len(shares))],
                   hovertemplate="%{z}<extra></extra>")
    ).update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False, scaleanchor="x"),
                    title=" / ".join(f"{n} {s}%" for n, s in zip(names, shares)))


@chart(
    "COMPOSE", "Population pyramid",
    "two go.Bar(orientation='h'), one side negated, barmode='relative'",
    "An ordered band column (age group) + two counts.",
    "Two populations compared band by band, mirrored around a shared spine.",
)
def c_pyramid():
    bands = [f"{i}-{i + 9}" for i in range(0, 80, 10)]
    left = np.array([88.0, 91, 95, 84, 72, 55, 38, 19])
    right = left * RNG.uniform(0.85, 1.2, len(bands))
    return go.Figure(
        [
            go.Bar(y=bands, x=-left, orientation="h", name="Region A",
                   marker_color=CATS[0], hovertemplate="%{y}: %{customdata}<extra></extra>",
                   customdata=left.round(0)),
            go.Bar(y=bands, x=right, orientation="h", name="Region B",
                   marker_color=CATS[1], hovertemplate="%{y}: %{x:.0f}<extra></extra>"),
        ]
    ).update_layout(barmode="relative", bargap=0.08,
                    xaxis=dict(title="thousands of people", tickformat="~s"))


blocked(
    "COMPOSE", "Ternary contour",
    "ff.create_ternary_contour(coords, values)",
    "Three parts summing to a whole, plus a fourth measured value.",
    "Contour bands drawn INSIDE the triangle - 'what is the yield at each blend?'",
    "Needs scikit-image, which is not installed here. `pip install scikit-image` unblocks it. "
    "px.scatter_ternary with color= shows the same fourth variable as dot colour, with no extra package.",
)


# =====================================================================
# FLOW - "what moves where?"
# =====================================================================


def _sankey_arrays(df: pd.DataFrame):
    """Turn a from/to/amount table into the integer index arrays sankey needs."""
    names = list(dict.fromkeys(list(df.source) + list(df.target)))
    idx = {n: i for i, n in enumerate(names)}
    return names, df.source.map(idx).to_list(), df.target.map(idx).to_list()


@chart(
    "FLOW", "Sankey diagram",
    "go.Sankey(node=dict(label=names), link=dict(source=idx, target=idx, value=amounts))",
    "A from-column, a to-column and an amount - any GROUP BY a, b, SUM(x) you have ever run.",
    "Where did the money actually come from and where did it end up? Two bar charts cannot tell you WHICH source fed WHICH destination, and that relationship is the story.",
    note="The trap: link.source and link.target must be INTEGER POSITIONS into node.label, not the names. Strings validate cleanly and then render nothing.",
    height=400,
)
def c_sankey():
    d = d_flow()
    names, src, tgt = _sankey_arrays(d)
    return go.Figure(
        go.Sankey(
            arrangement="snap",
            node=dict(label=names, pad=18, thickness=16, line=dict(color=GRID, width=1),
                      color=[CATS[i % len(CATS)] for i in range(len(names))]),
            link=dict(source=src, target=tgt, value=d.amount,
                      color="rgba(90,169,255,0.22)",
                      hovertemplate="%{source.label} to %{target.label}<br>$%{value}m<extra></extra>"),
        )
    ).update_layout(margin=dict(l=8, r=8, t=8, b=8))


@chart(
    "FLOW", "Sankey with grouped nodes and arrow links",
    "go.Sankey(node=dict(groups=[[3, 4]], align='left'), link=dict(arrowlen=15))",
    "The same edge list, when some nodes should be collapsed into one box.",
    "Several destinations are really one thing, or you want the ribbons to read directionally with arrow tips.",
    note="node.groups merges nodes; node.align takes justify / left / right / centre; link.arrowlen puts a point on each ribbon.",
    height=400,
)
def c_sankey_grouped():
    d = d_flow()
    names, src, tgt = _sankey_arrays(d)
    return go.Figure(
        go.Sankey(
            arrangement="snap",
            node=dict(label=names, pad=18, thickness=16, align="left",
                      groups=[[len(names) - 2, len(names) - 1]],
                      color=[CATS[i % len(CATS)] for i in range(len(names))]),
            link=dict(source=src, target=tgt, value=d.amount, arrowlen=14,
                      color="rgba(78,203,141,0.22)"),
        )
    ).update_layout(margin=dict(l=8, r=8, t=8, b=8))


@chart(
    "FLOW", "Parallel categories",
    "px.parallel_categories(df, dimensions=['agency', 'region', 'band'])",
    "Three to six CATEGORY columns describing the same rows.",
    "Which combinations actually occur together, and which never do? Ribbon thickness is how many rows took that path.",
    note="Needs zero reshaping - hand it the wide table. It silently drops any column with more than 50 distinct values. Feed it a pre-aggregated counts= array to scale.",
    height=380,
)
def c_parcats():
    d = d_long().sample(1200, random_state=4).copy()
    d["band"] = pd.cut(d.award, 3, labels=["low", "mid", "high"]).astype(str)
    d["outcome"] = RNG.choice(["cited", "cleared"], len(d), p=[0.35, 0.65])
    return px.parallel_categories(d, dimensions=["agency", "region", "band", "outcome"],
                                  color=d.award, color_continuous_scale="Viridis")


@chart(
    "FLOW", "Funnel", "px.funnel(df, x='cases', y='stage')",
    "Ordered stages + a count that shrinks at each one.",
    "Where does the process leak? A bar chart of stage counts makes you do the subtraction in your head, and the story is the biggest GAP, not the biggest bar.",
    note="textinfo='percent previous' prints the drop-off from the step before, straight on the chart.",
)
def c_funnel():
    d = d_stages()
    return px.funnel(d, x="cases", y="stage").update_traces(
        textinfo="value+percent previous", marker_color=CATS[0]
    )


@chart(
    "FLOW", "Grouped funnel", "px.funnel(df, x='cases', y='stage', color='agency')",
    "Ordered stages + a count, for two or more entities.",
    "Two agencies run the same process and you want to see who leaks where.",
)
def c_funnel_grouped():
    rows = []
    for i, a in enumerate(AGENCIES[:3]):
        base = 9000 - i * 1500
        for j, s in enumerate(STAGES):
            rows.append({"agency": a, "stage": s, "cases": int(base * (0.62 - i * 0.04) ** j)})
    return px.funnel(pd.DataFrame(rows), x="cases", y="stage", color="agency")


@chart(
    "FLOW", "Cone - a 3D vector field",
    "go.Cone(x, y, z, u, v, w)",
    "Six equal-length arrays: three for position, three for direction.",
    "Each point in space has a direction and a strength - wind, current, magnetic field - and you want to see which way it pushes.",
)
def c_cone():
    x, y, z, u, v, w = d_vectorfield(6)
    return go.Figure(
        go.Cone(x=x, y=y, z=z, u=u, v=v, w=w, colorscale="Viridis", sizemode="scaled",
                sizeref=0.5, showscale=False)
    )


@chart(
    "FLOW", "Streamtube - the paths through a field",
    "go.Streamtube(x, y, z, u, v, w)",
    "The same six arrays as cone.",
    "The question is about PATHS, not arrows: where does something released here end up?",
)
def c_streamtube():
    x, y, z, u, v, w = d_vectorfield(8)
    return go.Figure(
        go.Streamtube(x=x, y=y, z=z, u=u, v=v, w=w, colorscale="Viridis",
                      sizeref=0.4, showscale=False,
                      starts=dict(x=[0] * 5, y=list(np.linspace(0.4, 2.6, 5)),
                                  z=[1.5] * 5))
    )


@chart(
    "FLOW", "Quiver plot (2D arrows)", "ff.create_quiver(x, y, u, v)",
    "Four arrays: two for position, two for direction, all in 2D.",
    "The flat version of a cone plot. Each arrow shows direction and strength at that spot.",
)
def c_ff_quiver():
    g = np.linspace(0, 2, 12)
    xx, yy = np.meshgrid(g, g)
    fig = ff.create_quiver(xx, yy, np.cos(xx * 2) * 0.15, np.sin(yy * 2) * 0.15,
                           scale=1.0, arrow_scale=0.35,
                           line=dict(width=1.2, color=CATS[0]))
    fig.update_layout(template="wall")
    return fig


@chart(
    "FLOW", "Streamlines (2D)", "ff.create_streamline(x, y, u, v)",
    "A 2D grid of positions plus a direction at each.",
    "Same field as the quiver, drawn as continuous paths rather than separate arrows.",
)
def c_ff_streamline():
    x = np.linspace(-2, 2, 24)
    y = np.linspace(-2, 2, 24)
    xx, yy = np.meshgrid(x, y)
    fig = ff.create_streamline(x, y, -1 - xx**2 + yy, 1 + xx - yy**2,
                               arrow_scale=0.08, density=1.1,
                               line=dict(width=1, color=CATS[2]))
    fig.update_layout(template="wall", showlegend=False)
    return fig


# =====================================================================
# RANK - "who is on top, and did it change?"
# =====================================================================


@chart(
    "RANK", "Ranked horizontal bar",
    "px.bar(df.sort_values('score'), x='score', y='entity', orientation='h')",
    "One entity column + one number.",
    "Who is on top right now. The default and usually the correct answer.",
    note="Sort ASCENDING for a horizontal bar - plotly draws bottom-to-top, so ascending puts the winner at the top.",
)
def c_rank_bar():
    d = d_rank_over_time()
    last = d[d.year == d.year.max()].sort_values("score")
    return px.bar(last, x="score", y="entity", orientation="h", color="entity",
                  text_auto=".1f").update_layout(showlegend=False)


@chart(
    "RANK", "Bump chart", "px.line(df, x='year', y='rank').update_yaxes(autorange='reversed')",
    "One entity column + a number + a date, over many periods.",
    "Who is climbing and who is falling? A grouped bar of 5 entities x 10 years is 50 bars your eye cannot follow. Here CROSSINGS are visible events.",
    note="No px.bump. The whole trick is autorange='reversed' so rank 1 sits at the top.",
)
def c_bump():
    d = d_rank_over_time()
    return px.line(d, x="year", y="rank", color="entity", markers=True).update_yaxes(
        autorange="reversed", dtick=1, title="rank"
    )


@chart(
    "RANK", "Slope chart", "px.line(df[df.year.isin([first, last])], x='year', y='score', color='entity')",
    "One entity column + one number at exactly two points in time.",
    "Then versus now. Up-sloping and down-sloping separate instantly, and the steepest line is the biggest mover.",
    note="A before/after grouped bar makes the reader compute the change. The slope IS the change.",
)
def c_slope():
    d = d_rank_over_time()
    ends = d[d.year.isin([d.year.min(), d.year.max()])].copy()
    ends["year"] = ends.year.astype(str)
    fig = px.line(ends, x="year", y="score", color="entity", markers=True)
    for i, e in enumerate(sorted(ends.entity.unique())):
        v = ends[(ends.entity == e) & (ends.year == str(d.year.max()))].score.iloc[0]
        fig.add_annotation(x=str(d.year.max()), y=v, text=f" {e}", showarrow=False,
                           xanchor="left", font=dict(color=CATS[i % len(CATS)], size=11))
    return fig.update_layout(showlegend=False, xaxis=dict(type="category"),
                             margin=dict(r=90))


@chart(
    "RANK", "Pareto chart",
    "make_subplots(secondary_y=True) + sorted go.Bar + cumulative % go.Scatter",
    "One entity column + one number, many entities.",
    "How few entities account for most of the total? Read across at 80% on the right axis to find the answer.",
)
def c_pareto():
    d = d_long().groupby("agency", as_index=False)["award"].sum().sort_values(
        "award", ascending=False
    )
    cum = d.award.cumsum() / d.award.sum() * 100
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=d.agency, y=d.award, marker_color=CATS[0], name="total"),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=d.agency, y=cum, mode="lines+markers", name="cumulative %",
                             line=dict(color=CATS[1], width=2)), secondary_y=True)
    fig.add_hline(y=80, line_dash="dot", line_color=MUTED, secondary_y=True,
                  annotation_text="80%", annotation_position="top left")
    fig.update_yaxes(title_text="Awarded ($)", secondary_y=False)
    fig.update_yaxes(title_text="cumulative %", range=[0, 105], secondary_y=True,
                     showgrid=False)
    return fig


@chart(
    "RANK", "Rank as a heatmap", "go.Heatmap(z=rank_matrix, x=years, y=entities)",
    "One entity column x one period column + a rank or a value.",
    "The whole leaderboard's history in one grid. 50 numbers as bars is unreadable; as a grid it is a picture.",
)
def c_rank_heatmap():
    d = d_rank_over_time()
    m = d.pivot(index="entity", columns="year", values="rank")
    return go.Figure(
        go.Heatmap(z=m.values, x=[str(c) for c in m.columns], y=list(m.index),
                   xgap=2, ygap=2, colorscale="Viridis_r", reversescale=False,
                   colorbar=dict(title="rank"),
                   texttemplate="%{z:.0f}", textfont=dict(size=10))
    )


@chart(
    "RANK", "Legend as an isolate control",
    "fig.update_layout(legend=dict(itemclick='toggleothers'))",
    "Many series on one chart.",
    "Twenty lines and the reader wants one. One click isolates it instead of nineteen clicks to hide the rest.",
    note="itemclick: 'toggle' / 'toggleothers' / False. Pair with visible='legendonly' to start with only the top few showing.",
)
def c_legend_isolate():
    d = d_timeseries(300)
    fig = px.line(d, x="date", y="claims", color="region", render_mode="svg")
    fig.data[2].visible = "legendonly"
    fig.data[3].visible = "legendonly"
    return fig.update_layout(
        legend=dict(itemclick="toggleothers", itemdoubleclick="toggle",
                    orientation="h", y=1.08, x=0, title_text="click to isolate  "),
    )


# =====================================================================
# LOCATE - "where?"
# =====================================================================


@chart(
    "LOCATE", "Choropleth (built-in outlines)",
    "px.choropleth(df, locations='state', locationmode='USA-states', color='rate', scope='usa')",
    "One place-code column (state code, ISO country code) + one number.",
    "Which places run high. Start here: the built-in outlines mean you need NO geojson file at all.",
    note="locationmode takes 'ISO-3', 'USA-states', 'country names'. The outline map needs no tiles and no token, and unlike tile maps it can be faceted.",
)
def c_choropleth():
    return px.choropleth(d_states(), locations="state", locationmode="USA-states",
                         color="rate", scope="usa", color_continuous_scale="Viridis")


@chart(
    "LOCATE", "Diverging choropleth",
    "px.choropleth(..., color_continuous_scale='RdBu', color_continuous_midpoint=0)",
    "One place code + one number that can sit above OR below a baseline.",
    "The number is a change or a rate, so the reader needs to see instantly which side of zero each place is on.",
    note="Without the midpoint, the neutral colour lands wherever the data average happens to be, and 'white means zero' silently becomes a lie.",
)
def c_choropleth_diverging():
    return px.choropleth(d_states(), locations="state", locationmode="USA-states",
                         color="change", scope="usa", color_continuous_scale="RdBu",
                         color_continuous_midpoint=0)


@chart(
    "LOCATE", "Small-multiple maps (facets)",
    "px.choropleth(df, ..., facet_col='year')",
    "A place code + a number + one more low-cardinality column.",
    "One map per year, side by side, on a shared colour scale.",
    note="Only the outline (_geo) family facets. The tile-map family (scatter_map, density_map, choropleth_map) cannot.",
    height=280,
)
def c_choropleth_facet():
    base = d_states()
    frames = []
    for y in (2022, 2023, 2024):
        f = base.copy()
        f["year"] = y
        f["rate"] = (f["rate"] * RNG.uniform(0.7, 1.3, len(f))).round(1)
        frames.append(f)
    d = pd.concat(frames)
    fig = px.choropleth(d, locations="state", locationmode="USA-states", color="rate",
                        scope="usa", facet_col="year", color_continuous_scale="Viridis")
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig


@chart(
    "LOCATE", "Geo scatter (bubble map)",
    "px.scatter_geo(df, lat='lat', lon='lon', size='amount')",
    "A latitude column + a longitude column (+ a number for size).",
    "Where are these, and are they clustered? Circles sized by value beat a choropleth for raw COUNTS, because a choropleth of counts is a population map wearing a costume.",
)
def c_scatter_geo():
    d = d_geo_points(300)
    return px.scatter_geo(d, lat="lat", lon="lon", size="amount", color="amount",
                          scope="usa", color_continuous_scale="Viridis", size_max=18,
                          opacity=0.65)


@chart(
    "LOCATE", "Geo connection map", "px.line_geo(df, lat=..., lon=..., color='route')",
    "Origin and destination coordinate pairs.",
    "What connects to what, geographically - shipments, ownership chains, transfers.",
)
def c_line_geo():
    hubs = {"NY": (40.7, -74.0), "LA": (34.0, -118.2), "CHI": (41.9, -87.6),
            "HOU": (29.8, -95.4), "MIA": (25.8, -80.2)}
    rows = []
    for dst in ("LA", "CHI", "HOU", "MIA"):
        for a in ("NY", dst):
            rows.append({"route": f"NY-{dst}", "lat": hubs[a][0], "lon": hubs[a][1]})
    return px.line_geo(pd.DataFrame(rows), lat="lat", lon="lon", color="route",
                       scope="usa", markers=True)


@chart(
    "LOCATE", "Orthographic globe",
    "px.scatter_geo(..., projection='orthographic')",
    "Any lat/lon or place-code data.",
    "The default flat projection distorts area badly at the poles. 22 projections are built in; this one is a globe.",
    note="projection takes 22 values. scope takes world / usa / europe / asia / africa / north america / south america. fitbounds auto-zooms to your data.",
)
def c_geo_projection():
    d = d_geo_points(200)
    return px.scatter_geo(d, lat="lat", lon="lon", color="amount",
                          projection="orthographic", color_continuous_scale="Viridis",
                          opacity=0.7)


@chart(
    "LOCATE", "Tile-map scatter", "px.scatter_map(df, lat='lat', lon='lon', size='amount')",
    "A latitude column + a longitude column.",
    "Same as a geo scatter, but the reader needs to zoom in and see the actual streets under the dots.",
    note="Built with map_style='white-bg' so this page needs no tile server. Switch to 'carto-darkmatter' or 'open-street-map' when you have internet.",
)
def c_scatter_map():
    d = d_metro_points()
    return px.scatter_map(d, lat="lat", lon="lon", size="amount", color="amount",
                          zoom=9.6, center=dict(lat=40.73, lon=-73.98),
                          map_style="white-bg", color_continuous_scale="Viridis",
                          size_max=16, opacity=0.7)


@chart(
    "LOCATE", "Tile-map density (hotspot blur)",
    "px.density_map(df, lat=..., lon=..., z='amount', radius=25)",
    "So many lat/lon points that individual dots turn to mush.",
    "Where is the hotspot? radius= controls the blur size in pixels and is the only knob that really matters.",
)
def c_density_map():
    d = d_metro_points(1200)
    return px.density_map(d, lat="lat", lon="lon", z="amount", radius=20, zoom=9.6,
                          center=dict(lat=40.73, lon=-73.98), map_style="white-bg",
                          color_continuous_scale="Viridis")


@chart(
    "LOCATE", "Tile-map choropleth (your own boundaries)",
    "px.choropleth_map(df, geojson=gj, locations='zone', featureidkey='properties.zone', color='rate')",
    "One row per named region + one number, plus a geojson of the boundaries.",
    "The regions are not countries or states - census tracts, ZIPs, precincts, sales territories - and the question is which neighbourhoods are high.",
    note="featureidkey names the property INSIDE your geojson that your locations column matches. Default is 'id'.",
)
def c_choropleth_map():
    gj, d = d_geojson_boxes()
    return px.choropleth_map(d, geojson=gj, locations="zone",
                             featureidkey="properties.zone", color="rate",
                             zoom=8.4, center=dict(lat=40.75, lon=-73.9),
                             map_style="white-bg", opacity=0.75,
                             color_continuous_scale="Viridis")


@chart(
    "LOCATE", "Line map (tile)", "px.line_map(df, lat=..., lon=..., color='route')",
    "Sequences of lat/lon points that form a journey.",
    "Routes on a zoomable tile map rather than a fixed outline.",
)
def c_line_map():
    hubs = {"NY": (40.7, -74.0), "PHL": (39.95, -75.16), "DC": (38.9, -77.0),
            "BOS": (42.36, -71.06)}
    rows = []
    for dst in ("PHL", "DC", "BOS"):
        for a in ("NY", dst):
            rows.append({"route": f"NY-{dst}", "lat": hubs[a][0], "lon": hubs[a][1]})
    return px.line_map(pd.DataFrame(rows), lat="lat", lon="lon", color="route",
                       zoom=5.2, center=dict(lat=40.3, lon=-74.5), map_style="white-bg")


@chart(
    "LOCATE", "Hexbin map", "ff.create_hexbin_map(lat=..., lon=..., nx_hexagon=20)",
    "Thousands of lat/lon points and no natural boundary to aggregate into.",
    "Bins the points into equal-size hexagons, which kills the 'big states look important' distortion completely.",
    note="There is no hexbin TRACE. This factory builds hexagons out of a choroplethmap.",
)
def c_ff_hexbin():
    d = d_metro_points(1200)
    fig = ff.create_hexbin_map(lat=d.lat.to_list(), lon=d.lon.to_list(), nx_hexagon=18,
                               opacity=0.7, color_continuous_scale="Viridis",
                               min_count=1, zoom=9.3, center=dict(lat=40.73, lon=-73.98))
    fig.update_layout(template="wall", map_style="white-bg",
                      margin=dict(l=0, r=0, t=0, b=0))
    return fig


@chart(
    "LOCATE", "Geo subplot grid",
    "make_subplots(rows=1, cols=3, specs=[[{'type': 'geo'}] * 3])",
    "Several maps that need to sit in one figure.",
    "One map per measure or per period, hand-built rather than faceted, so each panel can be a different map entirely.",
    note="specs type 'geo' is a real cell type. It is missing from most cheat sheets, which only list xy / scene / polar / ternary / map / domain.",
    height=280,
)
def c_geo_subplots():
    d = d_states()
    fig = make_subplots(rows=1, cols=3, specs=[[{"type": "geo"}] * 3],
                        subplot_titles=("Rate", "Change", "Rate (log)"))
    for i, (col, scale, mid) in enumerate(
        [("rate", "Viridis", None), ("change", "RdBu", 0), ("rate", "Plasma", None)], start=1
    ):
        fig.add_trace(
            go.Choropleth(locations=d.state, locationmode="USA-states", z=d[col],
                          colorscale=scale, zmid=mid, showscale=False),
            row=1, col=i,
        )
    fig.update_geos(scope="usa", bgcolor=PANEL, lakecolor=PANEL, landcolor="#1b2230",
                    subunitcolor=GRID)
    return fig


@chart(
    "LOCATE", "Image as a plot layer", "go.Image(z=rgb_array)",
    "Actual pixels: a scan, a floor plan, a screenshot, a satellite tile.",
    "The 'map' is a picture, and you want chart marks sitting on top of it in the picture's own coordinates.",
    note="Also reachable via px.imshow on an H x W x 3 array. Feeding a 2D array instead gives you a heatmap.",
)
def c_image():
    h, w = 90, 140
    yy, xx = np.mgrid[0:h, 0:w]
    rgb = np.stack(
        [
            (128 + 110 * np.sin(xx / 13)).clip(0, 255),
            (128 + 110 * np.sin(yy / 9)).clip(0, 255),
            (128 + 110 * np.cos((xx + yy) / 17)).clip(0, 255),
        ],
        axis=-1,
    ).astype(np.uint8)
    fig = go.Figure(go.Image(z=rgb))
    fig.add_trace(go.Scatter(x=[30, 70, 110], y=[30, 55, 25], mode="markers+text",
                             text=["site A", "site B", "site C"], textposition="top center",
                             marker=dict(size=12, color=CATS[3], line=dict(width=2, color="white")),
                             name="sites"))
    return fig.update_layout(showlegend=False)


@chart(
    "LOCATE", "Deprecated mapbox family",
    "px.scatter_mapbox / line_mapbox / density_mapbox / choropleth_mapbox",
    "Exactly the same shapes as the map family above.",
    "Never, in new code. This is here so you recognise it in old code and know what to replace it with.",
    note="All four raise a DeprecationWarning on construction. Replace with scatter_map / line_map / density_map / choropleth_map. The only signature difference is mapbox_style= instead of map_style=.",
)
def c_mapbox_deprecated():
    d = d_metro_points(250)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig = px.scatter_mapbox(d, lat="lat", lon="lon", size="amount", color="amount",
                                zoom=9.6, center=dict(lat=40.73, lon=-73.98),
                                mapbox_style="white-bg",
                                color_continuous_scale="Viridis", size_max=14, opacity=0.6)
    return fig


@chart(
    "LOCATE", "Deprecated mapbox: density, choropleth and line",
    "px.density_mapbox(...) / px.choropleth_mapbox(...) / px.line_mapbox(...)",
    "Same shapes as density_map, choropleth_map and line_map.",
    "Legacy maintenance only. Prop-for-prop identical to their replacements.",
    note="All three deprecated trace types shown together rather than silently dropped. Each px call emits TWO DeprecationWarnings - one from px, one from the underlying go object.",
    height=560,
)
def c_mapbox_deprecated_2():
    gj, dz = d_geojson_boxes()
    dp = d_metro_points(600)
    hubs = {"NY": (40.7, -74.0), "PHL": (39.95, -75.16), "DC": (38.9, -77.0)}
    route = pd.DataFrame(
        [{"route": f"NY-{d}", "lat": hubs[a][0], "lon": hubs[a][1]}
         for d in ("PHL", "DC") for a in ("NY", d)]
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # Build each one through its px wrapper, then park the traces in one grid.
        f_den = px.density_mapbox(dp, lat="lat", lon="lon", z="amount", radius=16)
        f_cho = px.choropleth_mapbox(dz, geojson=gj, locations="zone",
                                     featureidkey="properties.zone", color="rate",
                                     opacity=0.75)
        f_lin = px.line_mapbox(route, lat="lat", lon="lon", color="route")

        # Stacked in ONE column: a tile map needs real width to render anything,
        # and three side by side inside this card would be 150 px each.
        fig = make_subplots(rows=3, cols=1, specs=[[{"type": "mapbox"}]] * 3,
                            vertical_spacing=0.06,
                            subplot_titles=("px.density_mapbox", "px.choropleth_mapbox",
                                            "px.line_mapbox"))
        for row, src in enumerate((f_den, f_cho, f_lin), start=1):
            for tr in src.data:
                fig.add_trace(tr.update(showlegend=False), row=row, col=1)
        fig.update_traces(showscale=False, selector=dict(type="densitymapbox"))
        fig.update_traces(showscale=False, selector=dict(type="choroplethmapbox"))
        fig.update_layout(
            mapbox=dict(style="white-bg", zoom=9.2, center=dict(lat=40.73, lon=-73.98)),
            mapbox2=dict(style="white-bg", zoom=7.6, center=dict(lat=40.75, lon=-73.9)),
            mapbox3=dict(style="white-bg", zoom=5.0, center=dict(lat=40.0, lon=-75.5)),
            margin=dict(l=0, r=0, t=24, b=0), coloraxis_showscale=False,
        )
    return fig


@chart(
    "LOCATE", "Hexbin map (deprecated mapbox twin)",
    "ff.create_hexbin_mapbox(lat=..., lon=..., nx_hexagon=18)",
    "The same thousands of lat/lon points.",
    "Legacy code only. Identical output to create_hexbin_map.",
    note="On plotly 6.9 this factory already emits the modern choroplethmap trace, so the only thing still 'mapbox' about it is the function name.",
)
def c_ff_hexbin_mapbox():
    d = d_metro_points(900)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig = ff.create_hexbin_mapbox(lat=d.lat.to_list(), lon=d.lon.to_list(),
                                      nx_hexagon=14, opacity=0.7, min_count=1,
                                      color_continuous_scale="Plasma",
                                      zoom=9.3, center=dict(lat=40.73, lon=-73.98))
    fig.update_layout(template="wall", map_style="white-bg",
                      margin=dict(l=0, r=0, t=0, b=0))
    return fig


blocked(
    "LOCATE", "US county choropleth by FIPS",
    "ff.create_choropleth(fips=['06001', ...], values=[...])",
    "A FIPS county-code column + a number.",
    "County-level maps of the whole US, with state outlines drawn on top, in one call.",
    "Needs the plotly-geo package, which is not installed here. `pip install plotly-geo` unblocks it. "
    "Workaround with no extra package: px.choropleth with a county geojson passed to geojson= "
    "and featureidkey='id'.",
)


# =====================================================================
# CHANGE - "what happened over time?"
# =====================================================================


@chart(
    "CHANGE", "Line chart", "px.line(df, x='date', y='claims', color='region')",
    "One ordered column (usually a date) + one number, optionally per entity.",
    "Is this going up or down? The single most-used shape in the whole library.",
    note="px.line connects rows in DATAFRAME ORDER, not sorted order. Unsorted input gives you spaghetti - sort first. And dates arriving as strings sort alphabetically.",
)
def c_line():
    d = d_timeseries(365).sort_values("date")
    return px.line(d, x="date", y="claims", color="region",
                   render_mode="svg").update_layout(hovermode="x unified")


@chart(
    "CHANGE", "Step line", "px.line(df, x='date', y='rate', line_shape='hv')",
    "A date column + a number that HOLDS then JUMPS.",
    "Regulations, rate schedules, headcounts, price bands. A straight sloping line implies gradual change that never happened.",
    note="line_shape takes linear / spline / hv / vh / hvh / vhv. 'hv' is the step; 'spline' is a smooth curve.",
)
def c_line_step():
    dates = pd.date_range("2023-01-01", periods=14, freq="MS")
    rate = np.repeat([2.5, 3.0, 3.75, 4.25, 4.25, 4.0, 3.5], 2)
    d = pd.DataFrame({"date": dates, "rate": rate})
    return px.line(d, x="date", y="rate", line_shape="hv", markers=True).update_layout(
        yaxis_ticksuffix="%"
    )


@chart(
    "CHANGE", "Line with a confidence band",
    "go.Scatter(x=x+x[::-1], y=hi+lo[::-1], fill='toself') then the mean line on top",
    "A date column + a central number + an upper and lower bound.",
    "The estimate has uncertainty and hiding it would be dishonest. The band is the uncertainty, drawn.",
    note="The trick is one closed polygon: x forwards then backwards, y upper then lower reversed, with fill='toself'.",
)
def c_band():
    n = 120
    x = pd.date_range("2024-01-01", periods=n, freq="D")
    y = np.cumsum(RNG.normal(0.2, 1.0, n)) + 40
    se = np.linspace(1.5, 5.0, n)
    return go.Figure(
        [
            go.Scatter(x=np.r_[x, x[::-1]], y=np.r_[y + se, (y - se)[::-1]],
                       fill="toself", fillcolor="rgba(90,169,255,0.18)",
                       line=dict(width=0), hoverinfo="skip", name="95% band"),
            go.Scatter(x=x, y=y, mode="lines", line=dict(color=CATS[0], width=2),
                       name="estimate"),
        ]
    ).update_layout(hovermode="x unified")


@chart(
    "CHANGE", "Event markers on a time series",
    "fig.add_vrect(x0=..., x1=..., annotation_text='...') and fig.add_vline(...)",
    "Any time series, plus dates when something happened.",
    "Context that is invisible in the data itself - a rule change, an outage, a lockdown. This is how a chart makes a causal claim visible.",
    note="layer='below' puts the shading behind the data. Four helpers: add_hline, add_vline, add_hrect, add_vrect.",
)
def c_events():
    d = d_timeseries(400).sort_values("date")
    d = d[d.region == "North"]
    fig = px.line(d, x="date", y="claims")
    fig.add_vrect(x0="2023-06-01", x1="2023-10-01", fillcolor=CATS[1], opacity=0.12,
                  line_width=0, layer="below", annotation_text="rule in force",
                  annotation_position="top left",
                  annotation_font=dict(color=CATS[1], size=11))
    fig.add_vline(x="2024-01-15", line_dash="dash", line_color=CATS[3],
                  annotation_text="repeal", annotation_position="top right",
                  annotation_font=dict(color=CATS[3], size=11))
    return fig


@chart(
    "CHANGE", "Range slider + range selector",
    "fig.update_xaxes(rangeslider_visible=True, rangeselector=dict(buttons=[...]))",
    "A long time series - more than a few hundred points.",
    "3,650 daily points crammed into 900 pixels. The mini overview strip and the 1m/6m/YTD buttons let the reader look without you deciding for them.",
    note="rangeslider and rangeselector exist on xaxis and NOT on yaxis. That asymmetry is most of the size difference between the two axis objects.",
    height=380,
)
def c_rangeslider():
    d = d_timeseries(420).sort_values("date")
    d = d[d.region == "North"]
    fig = px.line(d, x="date", y="claims")
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            bgcolor="#1b2230", activecolor=CATS[0], font=dict(color=INK),
            buttons=[
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all", label="All"),
            ],
        ),
    )
    return fig


@chart(
    "CHANGE", "Rangebreaks - delete the dead time",
    "fig.update_xaxes(rangebreaks=[dict(bounds=['sat', 'mon'])])",
    "A time series with structural gaps - weekends, holidays, overnight.",
    "A price chart with a flat step every weekend is drawing time that does not exist. This removes it from the axis entirely.",
)
def c_rangebreaks():
    d = d_ohlc(90)
    fig = px.line(d, x="date", y="close")
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"]),
                                  dict(values=["2024-01-01", "2024-02-19"])])
    return fig


@chart(
    "CHANGE", "Zoom-aware date labels",
    "fig.update_xaxes(tickformatstops=[dict(dtickrange=[None, 86400000], value='%H:%M'), ...])",
    "A long time series the reader will zoom into.",
    "Zoomed out you want 'Jan 2024'; zoomed into one day you want '14:30'. Stops swap the format automatically by zoom level.",
    note="dtickrange is in MILLISECONDS. 86400000 is one day, 604800000 is one week.",
)
def c_tickformatstops():
    n = 600
    d = pd.DataFrame({"t": pd.date_range("2024-03-01", periods=n, freq="h"),
                      "v": np.cumsum(RNG.normal(0, 1, n)) + 50})
    fig = px.line(d, x="t", y="v")
    fig.update_xaxes(tickformatstops=[
        dict(dtickrange=[None, 3_600_000], value="%H:%M"),
        dict(dtickrange=[3_600_000, 86_400_000], value="%e %b %H:%M"),
        dict(dtickrange=[86_400_000, 604_800_000], value="%e %b"),
        dict(dtickrange=[604_800_000, None], value="%b %Y"),
    ])
    return fig


@chart(
    "CHANGE", "Bars over periods", "px.bar(df, x='month', y='claims')",
    "A chunky period column (month, quarter) + a number.",
    "The periods are countable, not continuous. A line implies you could read a value halfway between two months, and you cannot.",
)
def c_bar_time():
    d = d_timeseries(365)
    m = d.groupby([pd.Grouper(key="date", freq="MS"), "region"], as_index=False)["claims"].sum()
    return px.bar(m, x="date", y="claims", color="region")


@chart(
    "CHANGE", "Gantt / timeline", "px.timeline(df, x_start='start', x_end='end', y='contract')",
    "One row per event with a BEGIN date and an END date.",
    "Who overlapped with whom, and what ran long? Contracts, licences, debarments, employment spells, suspensions.",
    note="Three arguments are non-negotiable: x_start, x_end and y. Underneath it is a bar trace with the start dates in base= and the durations in milliseconds in x=.",
)
def c_timeline():
    return px.timeline(d_gantt(), x_start="start", x_end="end", y="contract",
                       color="status").update_yaxes(autorange="reversed")


@chart(
    "CHANGE", "Gantt (figure factory)", "ff.create_gantt(list_of_dicts)",
    "Task, Start and Finish per row.",
    "The same shape, with the older factory that colours by a named column and adds a date axis for you.",
)
def c_ff_gantt():
    rows = [dict(Task=t, Start=str(s.date()), Finish=str(f.date()), Resource=r)
            for t, s, f, r in zip(d_gantt().contract, d_gantt().start, d_gantt().end,
                                  d_gantt().status)]
    fig = ff.create_gantt(rows, index_col="Resource", show_colorbar=True,
                          group_tasks=True, bar_width=0.3,
                          colors=[CATS[0], CATS[1]])
    fig.update_layout(template="wall")
    return fig


@chart(
    "CHANGE", "Waterfall", "go.Waterfall(measure=[...], x=labels, y=deltas)",
    "A starting total, a list of signed changes, and an ending total.",
    "The number went from 100 to 110 - what were the PIECES? Two bars say 'it went up 10'. This says '40 arrived and 30 left', which is a completely different story.",
    note="measure tags each bar 'absolute', 'relative' or 'total'. Without it you just get a bar chart. The validator does not check the strings, so a typo silently renders as a relative step.",
)
def c_waterfall():
    return go.Figure(
        go.Waterfall(
            measure=["absolute", "relative", "relative", "relative", "relative", "total"],
            x=["2023 total", "new entrants", "exits", "reclassified", "price effect",
               "2024 total"],
            y=[420, 96, -68, 24, -31, None],
            connector=dict(line=dict(color=MUTED, dash="dot")),
            increasing=dict(marker_color=CATS[2]),
            decreasing=dict(marker_color=CATS[3]),
            totals=dict(marker_color=CATS[0]),
            textposition="outside", texttemplate="%{delta:+,.0f}",
        )
    ).update_layout(yaxis_title="Cases", margin=dict(t=44))


@chart(
    "CHANGE", "Candlestick", "go.Candlestick(x=dates, open=..., high=..., low=..., close=...)",
    "One date column + four price-like numbers per period.",
    "Did it close above or below where it opened, and how wild was the swing inside the period?",
    note="Plotly auto-adds a rangeslider under candlesticks. Kill it with xaxis_rangeslider_visible=False.",
)
def c_candlestick():
    d = d_ohlc(60)
    return go.Figure(
        go.Candlestick(x=d.date, open=d.open, high=d.high, low=d.low, close=d.close,
                       increasing=dict(line=dict(color=CATS[2])),
                       decreasing=dict(line=dict(color=CATS[3])))
    ).update_layout(xaxis_rangeslider_visible=False)


@chart(
    "CHANGE", "OHLC bars", "go.Ohlc(x=dates, open=..., high=..., low=..., close=...)",
    "The same four price columns per period.",
    "Same question as a candlestick. This is the low-ink version, which reads better when you cram hundreds of periods into one width.",
)
def c_ohlc():
    d = d_ohlc(60)
    return go.Figure(
        go.Ohlc(x=d.date, open=d.open, high=d.high, low=d.low, close=d.close,
                increasing=dict(line=dict(color=CATS[2])),
                decreasing=dict(line=dict(color=CATS[3])))
    ).update_layout(xaxis_rangeslider_visible=False)


@chart(
    "CHANGE", "Candlestick (figure factory)", "ff.create_candlestick(open, high, low, close, dates)",
    "The same four price columns.",
    "The factory recipe - it builds the same picture out of ordinary box traces you can restyle.",
)
def c_ff_candlestick():
    d = d_ohlc(45)
    fig = ff.create_candlestick(d.open, d.high, d.low, d.close, dates=d.date)
    fig.update_layout(template="wall", xaxis_rangeslider_visible=False)
    return fig


@chart(
    "CHANGE", "OHLC (figure factory)", "ff.create_ohlc(open, high, low, close, dates)",
    "The same four price columns.",
    "The factory version of the OHLC bar, built from scatter traces.",
)
def c_ff_ohlc():
    d = d_ohlc(45)
    fig = ff.create_ohlc(d.open, d.high, d.low, d.close, dates=d.date)
    fig.update_layout(template="wall", xaxis_rangeslider_visible=False)
    return fig


@chart(
    "CHANGE", "Calendar heatmap", "go.Heatmap(z=weekday_by_week_grid, xgap=2, ygap=2)",
    "A date column + a count.",
    "Is there a weekly or seasonal rhythm? Filings clustering on the last day of a quarter show up as a stripe you cannot see in a line chart.",
    note="No calendar-heatmap chart type exists. You reshape to a 7 x 52 grid yourself.",
    height=260,
)
def c_calendar_heatmap():
    dates = pd.date_range("2024-01-01", "2024-12-31", freq="D")
    counts = RNG.poisson(4, len(dates)) + (dates.dayofweek < 5) * 6
    counts = counts + (dates.is_quarter_end) * 40
    df = pd.DataFrame({"date": dates, "n": counts})
    df["week"] = df.date.dt.isocalendar().week.astype(int)
    df["dow"] = df.date.dt.dayofweek
    grid = df.pivot_table(index="dow", columns="week", values="n", aggfunc="sum")
    return go.Figure(
        go.Heatmap(z=grid.values, x=[str(c) for c in grid.columns],
                   y=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                   xgap=2, ygap=2, colorscale="Viridis",
                   colorbar=dict(title="filings"))
    ).update_layout(xaxis_title="ISO week", yaxis_autorange="reversed")


@chart(
    "CHANGE", "Entity x period heatmap", "go.Heatmap(z=matrix, zmid=0, colorscale='RdBu')",
    "One entity column x one period column + a number that straddles zero.",
    "50 entities over 10 years is 500 numbers. As bars it is unreadable; as a grid you spot the unusual cells at a glance.",
)
def c_entity_period_heatmap():
    ents = [f"Entity {c}" for c in "ABCDEFGHIJKL"]
    yrs = list(range(2015, 2025))
    z = RNG.normal(0, 12, (len(ents), len(yrs))).round(1)
    z[3, 6:] += 34
    return go.Figure(
        go.Heatmap(z=z, x=[str(y) for y in yrs], y=ents, xgap=1, ygap=1,
                   colorscale="RdBu", zmid=0, colorbar=dict(title="% change"))
    )


@chart(
    "CHANGE", "Animation over time",
    "px.scatter(df, ..., animation_frame='year', animation_group='entity', range_x=[...], range_y=[...])",
    "Two numbers + an entity + a time column.",
    "How did the whole picture move, year by year? A grid of 10 years is 10 things to compare from memory; motion makes the change itself the thing you see.",
    note="Two non-negotiable rules: set range_x/range_y by hand or the axes rescale each frame and everything appears to stand still, and set animation_group so a dot glides instead of teleporting.",
    height=400,
)
def c_animation():
    rows = []
    for e in ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta"]:
        x, y, s = RNG.uniform(10, 60), RNG.uniform(10, 60), RNG.uniform(20, 300)
        for yr in range(2015, 2025):
            x += RNG.normal(2, 3); y += RNG.normal(1.5, 3); s *= RNG.uniform(0.95, 1.12)
            rows.append({"year": yr, "entity": e, "inspections": max(x, 1),
                         "violations": max(y, 1), "size": max(s, 10)})
    d = pd.DataFrame(rows)
    return px.scatter(d, x="inspections", y="violations", size="size", color="entity",
                      animation_frame="year", animation_group="entity",
                      range_x=[0, 110], range_y=[0, 110], size_max=45,
                      hover_name="entity")


# =====================================================================
# CONNECT - "what links to what?"
# =====================================================================


@chart(
    "CONNECT", "Node-link network",
    "one go.Scatter(mode='lines') with None between each pair, plus a go.Scatter for the nodes",
    "An edge list plus x/y positions you computed yourself.",
    "Who connects to whom, as a web rather than a tree. Plotly has NO network trace - this is the standard hand-built recipe.",
    note="The None between each pair breaks the line, so all 400 edges live in ONE trace instead of 400. That is the difference between a chart that renders and a page that hangs.",
    height=380,
)
def c_network():
    n = 22
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r = 1 + RNG.uniform(-0.18, 0.18, n)
    pos = np.c_[np.cos(ang) * r, np.sin(ang) * r]
    edges = [(i, (i + k) % n) for i in range(n) for k in (1, 5, 9) if RNG.random() < 0.55]
    ex, ey = [], []
    for a, b in edges:
        ex += [pos[a, 0], pos[b, 0], None]
        ey += [pos[a, 1], pos[b, 1], None]
    deg = np.bincount(np.array(edges).ravel(), minlength=n)
    return go.Figure(
        [
            go.Scatter(x=ex, y=ey, mode="lines", line=dict(width=0.8, color=GRID),
                       hoverinfo="skip", showlegend=False),
            go.Scatter(x=pos[:, 0], y=pos[:, 1], mode="markers+text",
                       text=[f"N{i}" for i in range(n)], textposition="top center",
                       textfont=dict(size=9, color=MUTED),
                       marker=dict(size=8 + deg * 2.2, color=deg, colorscale="Viridis",
                                   line=dict(width=1, color=PANEL),
                                   colorbar=dict(title="links")),
                       hovertemplate="%{text}<br>%{marker.color} links<extra></extra>",
                       showlegend=False),
        ]
    ).update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False, scaleanchor="x"))


@chart(
    "CONNECT", "Arc diagram",
    "go.Scatter(mode='lines') with a semicircle of points per edge, nodes on one axis",
    "An edge list where the nodes have a natural ORDER.",
    "Same links as a network, but the nodes stay in your chosen order (time, size, alphabet) so you can see whether links are mostly local or mostly long-range.",
    note="Not a chart type. Each arc is a half-circle of points appended to one scatter trace, separated by None.",
)
def c_arc_diagram():
    n = 16
    xs = np.arange(n, dtype=float)
    ax, ay = [], []
    for a, b in [(i, i + k) for i in range(n) for k in (1, 3, 7) if i + k < n and RNG.random() < 0.5]:
        c, rad = (a + b) / 2, abs(b - a) / 2
        t = np.linspace(0, np.pi, 30)
        ax += list(c + rad * np.cos(t)) + [None]
        ay += list(rad * np.sin(t)) + [None]
    return go.Figure(
        [
            go.Scatter(x=ax, y=ay, mode="lines", line=dict(width=1, color=CATS[0]),
                       opacity=0.5, hoverinfo="skip"),
            go.Scatter(x=xs, y=np.zeros(n), mode="markers",
                       marker=dict(size=9, color=CATS[1])),
        ]
    ).update_layout(showlegend=False, yaxis=dict(visible=False),
                    xaxis=dict(title="node, in order", showgrid=False))


@chart(
    "CONNECT", "Overlap matrix",
    "px.imshow(overlap_matrix, text_auto=True)",
    "A square grid of how much every thing shares with every other thing.",
    "Which two datasets can I actually join? A network diagram of 1,000 nodes is a hairball; a sorted 1,000 x 1,000 grid is readable and zoomable.",
    note="For 'entity appears in 2 of 5 datasets' there is no Venn or UpSet chart in plotly - build a bar chart of set-combination counts instead.",
)
def c_overlap_matrix():
    names = [f"DS{i}" for i in range(9)]
    m = RNG.integers(0, 90, (9, 9))
    m = ((m + m.T) // 2)
    np.fill_diagonal(m, 100)
    return px.imshow(m, x=names, y=names, text_auto=True, aspect="auto",
                     color_continuous_scale="Viridis",
                     labels=dict(color="% shared"))


@chart(
    "CONNECT", "Set-combination bar (UpSet's top half)",
    "px.bar on a table of combination -> count",
    "One row per entity + a boolean column per set it belongs to.",
    "Which COMBINATIONS of memberships are common? This is the honest substitute for a Venn diagram past three sets.",
    note="Plotly has no Venn and no UpSet chart. Count the combinations in pandas and plot them as a sorted bar.",
)
def c_upset_bar():
    sets = ["NPPES", "FEC", "SAM", "OSHA"]
    n = 3000
    member = RNG.random((n, len(sets))) < [0.7, 0.35, 0.5, 0.25]
    combos = ["+".join([s for s, m in zip(sets, row) if m]) or "(none)" for row in member]
    d = pd.Series(combos).value_counts().head(12).reset_index()
    d.columns = ["combination", "entities"]
    return px.bar(d.sort_values("entities"), x="entities", y="combination",
                  orientation="h", color="entities",
                  color_continuous_scale="Viridis").update_layout(coloraxis_showscale=False)


# =====================================================================
# SINGLE VALUE - "one number that matters"
# =====================================================================


@chart(
    "SINGLE VALUE", "Indicator - number and delta",
    "go.Indicator(mode='number+delta', value=..., delta=dict(reference=...))",
    "One number, plus a prior value to compare it against.",
    "What is it right now, and is it up or down? This is the KPI tile. There is NO px.indicator.",
    note="The smallest trace in the library (24 properties). No hover, no legend. It is a domain trace, so in a subplot grid the cell needs type='indicator' or 'domain'.",
    height=200,
)
def c_indicator():
    return go.Figure(
        go.Indicator(mode="number+delta", value=4207,
                     number=dict(valueformat=",.0f", font=dict(size=54)),
                     delta=dict(reference=3810, relative=True, valueformat=".1%",
                                increasing=dict(color=CATS[2]),
                                decreasing=dict(color=CATS[3])),
                     title=dict(text="Cases closed this quarter",
                                font=dict(size=13, color=MUTED)))
    ).update_layout(margin=dict(l=10, r=10, t=30, b=10))


@chart(
    "SINGLE VALUE", "Indicator - gauge dial",
    "go.Indicator(mode='gauge+number', gauge=dict(shape='angular', steps=[...], threshold=...))",
    "One number, a scale it lives on, and a target.",
    "Where does this sit between bad and good, and are we past the line? steps colour the bands, threshold draws the target.",
    height=260,
)
def c_indicator_gauge():
    return go.Figure(
        go.Indicator(
            mode="gauge+number+delta", value=427, delta=dict(reference=380),
            title=dict(text="Backlog (days)", font=dict(size=13, color=MUTED)),
            gauge=dict(
                shape="angular", axis=dict(range=[0, 600], tickcolor=MUTED),
                bar=dict(color=CATS[0]),
                bgcolor=PANEL, borderwidth=0,
                steps=[dict(range=[0, 200], color="#1b2230"),
                       dict(range=[200, 400], color="#232b38"),
                       dict(range=[400, 600], color="#2c3546")],
                threshold=dict(line=dict(color=CATS[3], width=3), thickness=0.85, value=500),
            ),
        )
    ).update_layout(margin=dict(l=24, r=24, t=40, b=10))


@chart(
    "SINGLE VALUE", "Indicator - bullet bar",
    "go.Indicator(mode='number+gauge+delta', gauge=dict(shape='bullet'))",
    "One number, a target, and good/ok/bad bands.",
    "The compact version of the dial. Several of these stack into a scoreboard where a round gauge would not fit.",
    height=220,
)
def c_indicator_bullet():
    fig = go.Figure()
    for i, (label, val, ref, mx) in enumerate(
        [("Cases closed", 427, 380, 600), ("Median days", 38, 45, 90),
         ("Appeal rate %", 12, 9, 30)]
    ):
        fig.add_trace(
            go.Indicator(
                mode="number+gauge+delta", value=val,
                delta=dict(reference=ref),
                title=dict(text=label, font=dict(size=11, color=MUTED)),
                domain=dict(x=[0.32, 1], y=[i / 3 + 0.04, (i + 1) / 3 - 0.04]),
                gauge=dict(shape="bullet", axis=dict(range=[0, mx]),
                           bar=dict(color=CATS[i], thickness=0.55), bgcolor=PANEL,
                           borderwidth=0,
                           steps=[dict(range=[0, mx * 0.5], color="#1b2230"),
                                  dict(range=[mx * 0.5, mx], color="#232b38")],
                           threshold=dict(line=dict(color=CATS[3], width=2),
                                          thickness=0.8, value=ref)),
            )
        )
    return fig.update_layout(margin=dict(l=8, r=18, t=12, b=12))


@chart(
    "SINGLE VALUE", "KPI row",
    "make_subplots(rows=1, cols=4, specs=[[{'type': 'indicator'}] * 4])",
    "Four numbers, each with a prior value.",
    "The header strip of a dashboard, as one figure rather than four.",
    note="Indicator is a DOMAIN trace. In a subplot grid the cell must be declared type='indicator' (or 'domain') or the trace silently refuses to land.",
    height=180,
)
def c_kpi_row():
    fig = make_subplots(rows=1, cols=4, specs=[[{"type": "indicator"}] * 4])
    vals = [("Entities", 41_308, 39_902, ",.0f"), ("Awards ($m)", 1_284, 1_401, ",.0f"),
            ("Median award", 12_400, 11_950, ",.0f"), ("Open cases", 372, 418, ",.0f")]
    for i, (label, v, ref, fmt) in enumerate(vals, start=1):
        fig.add_trace(
            go.Indicator(mode="number+delta", value=v,
                         number=dict(valueformat=fmt, font=dict(size=30)),
                         delta=dict(reference=ref, valueformat=fmt,
                                    increasing=dict(color=CATS[2]),
                                    decreasing=dict(color=CATS[3])),
                         title=dict(text=label, font=dict(size=11, color=MUTED))),
            row=1, col=i,
        )
    return fig.update_layout(margin=dict(l=8, r=8, t=30, b=8))


@chart(
    "SINGLE VALUE", "Bullet chart (figure factory)",
    "ff.create_bullet(df, markers='point', measures='performance', ranges='range')",
    "One label + a value + a target + qualitative bands.",
    "The pre-built target-versus-actual bar, if you would rather not wire gauge.shape='bullet' yourself.",
    height=240,
)
def c_ff_bullet():
    data = [
        dict(label="Cases closed", range=[300, 600], performance=[427, 380], point=[500]),
        dict(label="Median days", range=[20, 90], performance=[38, 45], point=[40]),
        dict(label="Appeal rate", range=[5, 30], performance=[12, 9], point=[10]),
    ]
    # No marker_size here: create_bullet forwards unknown kwargs straight to Layout.
    fig = ff.create_bullet(pd.DataFrame(data), markers="point", measures="performance",
                           ranges="range", titles="label", title="",
                           measure_colors=[CATS[0], CATS[4]],
                           range_colors=["#1b2230", "#2c3546"])
    fig.update_layout(template="wall", margin=dict(l=110, r=18, t=8, b=12))
    # create_bullet writes its row labels as annotations in its own dark colour.
    fig.update_annotations(font=dict(color=INK, size=11))
    return fig


@chart(
    "SINGLE VALUE", "Number with a sparkline behind it",
    "go.Indicator(domain=...) + go.Scatter(fill='tozeroy') with both axes hidden",
    "One number plus the short series that produced it.",
    "A number with no trend behind it hides whether it is a blip or a shift.",
    height=220,
)
def c_sparkline_kpi():
    n = 60
    y = np.cumsum(RNG.normal(0.6, 2.2, n)) + 60
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=y, mode="lines", fill="tozeroy", line=dict(color=CATS[0], width=2),
                             fillcolor="rgba(90,169,255,0.15)", hoverinfo="skip"))
    fig.add_trace(
        go.Indicator(mode="number+delta", value=float(y[-1]),
                     number=dict(valueformat=".1f", font=dict(size=40)),
                     delta=dict(reference=float(y[-8]), valueformat=".1f"),
                     title=dict(text="Filings per day", font=dict(size=12, color=MUTED)),
                     domain=dict(x=[0.02, 0.45], y=[0.35, 1.0]))
    )
    return fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False),
                             showlegend=False, margin=dict(l=8, r=8, t=8, b=8))


@chart(
    "SINGLE VALUE", "One number with its context rows",
    "go.Table with a single highlighted row",
    "One number that only means something next to three others.",
    "A big number alone is not information. Sometimes the honest KPI tile is a four-row table.",
    height=220,
)
def c_kpi_table():
    return go.Figure(
        go.Table(
            columnwidth=[3, 2, 2],
            header=dict(values=["<b>Measure</b>", "<b>This period</b>", "<b>Prior</b>"],
                        fill_color="#1b2230", font=dict(color=INK), align="left", height=30),
            cells=dict(
                values=[["Cases closed", "Median days", "Appeal rate", "Backlog"],
                        ["4,207", "38", "12%", "427"],
                        ["3,810", "45", "9%", "380"]],
                fill_color=[["#161c26", "#12171f", "#161c26", "#1e2836"]],
                font=dict(color=[[INK, INK, INK, CATS[3]]]), align="left", height=28),
        )
    ).update_layout(margin=dict(l=6, r=6, t=6, b=6))


# =====================================================================
# PAGE ASSEMBLY
# ---------------------------------------------------------------------
# plotly.js is loaded ONCE for the whole page. Each figure is written as
# its own div plus a block of JSON, and a small runtime draws a figure
# only when it scrolls near the viewport, then throws it away again when
# it scrolls far off.
#
# Why bother: a browser hands a single page only about 16 WebGL contexts.
# This page has ~24 charts that need one (every 3D chart, every tile map,
# splom, parcoords, parcats, and anything drawn with render_mode='webgl').
# Draw them all at once and the earliest ones have their context taken
# away and go blank - with no error in the console. Drawing on demand
# keeps the number of live contexts near what is actually on screen, and
# it means the page shows something in well under a second instead of
# chewing through 139 figures before it paints.
# =====================================================================

PLOT_CONFIG = {
    "displaylogo": False,
    "responsive": True,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
    "toImageButtonOptions": {"format": "svg", "scale": 2},
}

CSS = """
:root{--bg:#0a0d12;--panel:#12171f;--line:#232b38;--ink:#e8edf4;--muted:#8b98ab;
      --accent:#5aa9ff;--warn:#ffb454;--stop:#ff7b9c;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
     font:15px/1.55 ui-sans-serif,'Segoe UI',system-ui,sans-serif;}
a{color:var(--accent)}
code,kbd{font-family:ui-monospace,'Cascadia Code',Consolas,monospace}
header{padding:34px 26px 22px;border-bottom:1px solid var(--line);
       background:linear-gradient(180deg,#141a24,#0a0d12);}
header h1{margin:0 0 8px;font-size:27px;letter-spacing:-.4px}
header p{margin:0 0 6px;color:var(--muted);max-width:78ch}
.counts{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.pill{background:#161d28;border:1px solid var(--line);border-radius:999px;
      padding:5px 13px;font-size:12.5px;color:var(--muted)}
.pill b{color:var(--ink)}
nav{position:sticky;top:0;z-index:20;background:rgba(10,13,18,.94);
    backdrop-filter:blur(8px);border-bottom:1px solid var(--line);
    padding:11px 26px;display:flex;flex-wrap:wrap;gap:7px}
nav a{color:var(--muted);text-decoration:none;font-size:12.5px;font-weight:600;
      letter-spacing:.4px;border:1px solid var(--line);border-radius:6px;padding:4px 10px}
nav a:hover{color:var(--ink);border-color:var(--accent)}
main{padding:8px 26px 90px;max-width:2100px;margin:0 auto}
section{padding-top:34px;scroll-margin-top:58px}
.sechead{border-left:3px solid var(--accent);padding:2px 0 2px 13px;margin:0 0 6px}
.sechead h2{margin:0;font-size:21px;letter-spacing:.6px}
.sechead .q{color:var(--muted);font-size:15px;font-style:italic}
.sechead .n{color:var(--muted);font-size:12.5px;margin-top:4px}
.grid{display:grid;gap:18px;margin-top:18px;
      grid-template-columns:repeat(auto-fill,minmax(470px,1fr))}
.card{background:var(--panel);border:1px solid var(--line);border-radius:11px;
      overflow:hidden;display:flex;flex-direction:column}
.card h3{margin:0;padding:13px 15px 9px;font-size:16px;letter-spacing:-.2px}
.meta{padding:0 15px 12px;display:flex;flex-direction:column;gap:7px}
.call{background:#0a0e14;border:1px solid var(--line);border-radius:6px;
      padding:7px 9px;font:12px/1.45 ui-monospace,'Cascadia Code',Consolas,monospace;
      color:#9fd0ff;overflow-x:auto;white-space:pre-wrap;overflow-wrap:anywhere}
.row{font-size:13.2px;color:var(--muted)}
.row b{color:var(--ink);font-weight:600}
.use{font-size:13.6px;color:var(--ink);background:#161d28;border-left:2px solid var(--accent);
     border-radius:0 6px 6px 0;padding:8px 11px}
.note{font-size:12.6px;color:var(--warn);background:#1d1a12;border-left:2px solid var(--warn);
      border-radius:0 6px 6px 0;padding:8px 11px}
.plot{padding:0 10px 10px;overflow-x:auto}
.plot>div{width:100%}
.pending{display:flex;align-items:center;justify-content:center;color:var(--muted);
         font-size:12.5px;letter-spacing:.4px}
.blockedcard{border-color:#3a2732}
.blockedcard h3{color:var(--stop)}
.blockedmsg{margin:0 15px 16px;font-size:13.2px;color:var(--ink);background:#20141a;
      border-left:2px solid var(--stop);border-radius:0 6px 6px 0;padding:11px 12px}
.tag{display:inline-block;font-size:10.5px;letter-spacing:.7px;font-weight:700;
     color:var(--stop);border:1px solid var(--stop);border-radius:4px;padding:1px 6px;
     margin-left:8px;vertical-align:middle}
footer{border-top:1px solid var(--line);padding:26px;color:var(--muted);font-size:13px}
footer b{color:var(--ink)}
@media (max-width:560px){.grid{grid-template-columns:1fr}main,header,nav{padding-left:14px;padding-right:14px}}
"""


def _esc(s: str) -> str:
    return html.escape(str(s), quote=False)


# Trace types the browser draws with the GPU. Each one on screen holds a WebGL
# context, and a page only gets about 16 before the browser starts taking them
# back - at which point the oldest chart goes blank with nothing in the console.
#
# This is the renderer's own list, not a guess: every trace whose registration
# in the shipped plotly.min.js carries the "gl" category. Reproduce it with
#   re.findall(r'moduleType:"trace",name:"(\w+)".{0,400}?categories:\[(.*?)\]', bundle)
# Note parcats is NOT on it - it looks exotic but draws as plain SVG.
GPU_TRACES = {
    "scattergl", "scatterpolargl", "splom", "parcoords",
    "scatter3d", "surface", "mesh3d", "isosurface", "volume", "cone", "streamtube",
    "scattermap", "densitymap", "choroplethmap",
    "scattermapbox", "densitymapbox", "choroplethmapbox",
}

# How many GPU-backed figures may be alive at once. Big enough that nothing on
# screen ever gets purged out from under the reader (this grid shows at most
# ~6 cards at a time), small enough to stay clear of the browser's context cap.
GPU_BUDGET = 10

LAZY_JS = """
// Draw a figure when it is close to the viewport; throw it away when it is far.
// Two separate budgets:
//   - ordinary SVG charts: drawn near the viewport, purged well away from it
//   - GPU charts (3D, maps, splom, parcoords, anything WebGL): additionally
//     capped at GPU_BUDGET alive at once, oldest-drawn purged first. Without
//     this cap the browser silently revokes contexts and charts go blank.
(function () {
  var CFG = %CONFIG%;
  var BUDGET = %BUDGET%;
  var drawn = Object.create(null);
  var gpuOrder = [];   // ids of live GPU figures, oldest first
  var inflight = Object.create(null);  // id -> the unresolved newPlot promise
  var token = Object.create(null);     // id -> bumped on every draw/drop

  // Plotly.newPlot is async. Scroll fast enough and the "far" observer fires
  // while a figure is still building; purging a half-built tile map throws
  // "Cannot read properties of undefined (reading '_scrollZoom')" and can leave
  // the panel wedged. So a purge that lands mid-draw waits for the draw to
  // settle, and the token check makes sure it aborts if the reader scrolled
  // back and the figure got redrawn in the meantime.

  function spec(id) {
    var el = document.getElementById('spec-' + id);
    return el ? JSON.parse(el.textContent) : null;
  }
  function isGpu(box) { return box.dataset.gpu === '1'; }

  function draw(box) {
    var id = box.id;
    if (drawn[id]) return;
    var s = spec(id);
    if (!s) return;
    if (isGpu(box)) {
      // Free the oldest GPU figures before claiming another context.
      while (gpuOrder.length >= BUDGET) {
        var old = document.getElementById(gpuOrder[0]);
        if (!old || old === box) { gpuOrder.shift(); continue; }
        drop(old);
      }
      gpuOrder.push(id);
    }
    drawn[id] = true;
    var my = (token[id] = (token[id] || 0) + 1);
    box.classList.remove('pending');
    box.textContent = '';
    var p = Plotly.newPlot(box, s.data, s.layout, CFG).then(function () {
      // Tile maps measure their container as they initialise and can latch onto
      // a stale size, which leaves the map blank. One resize after the fact
      // settles it. Harmless for every other chart type.
      if (token[id] === my && drawn[id]) {
        try { Plotly.Plots.resize(box); } catch (e) {}
      }
    }, function () { /* a failed draw must not wedge a pending purge */ });
    inflight[id] = p;
  }

  function drop(box) {
    var id = box.id;
    if (!drawn[id]) return;
    delete drawn[id];
    var i = gpuOrder.indexOf(id);
    if (i > -1) gpuOrder.splice(i, 1);
    var my = (token[id] = (token[id] || 0) + 1);
    var p = inflight[id];

    function teardown() {
      if (token[id] !== my) return;   // redrawn while we waited - leave it alone
      delete inflight[id];
      try { Plotly.purge(box); } catch (e) {}
      box.classList.add('pending');
      box.textContent = 'scroll back to draw';
    }

    if (p) { p.then(teardown, teardown); } else { teardown(); }
  }

  var near = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) draw(e.target); });
  }, { rootMargin: '300px 0px' });

  var far = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (!e.isIntersecting) drop(e.target); });
  }, { rootMargin: '1100px 0px' });

  var boxes = document.querySelectorAll('.plotbox');
  for (var i = 0; i < boxes.length; i++) { near.observe(boxes[i]); far.observe(boxes[i]); }

  // Anchor jumps land instantly, so draw whatever the jump landed on.
  window.addEventListener('hashchange', function () {
    setTimeout(function () {
      document.querySelectorAll('.plotbox').forEach(function (b) {
        var r = b.getBoundingClientRect();
        if (r.top < window.innerHeight + 300 && r.bottom > -300) draw(b);
      });
    }, 60);
  });
})();
"""


def _fig_block(ch: Chart, fig: go.Figure, div_id: str) -> str:
    """A sized placeholder div plus the figure's JSON, for the lazy runtime."""
    spec = {"data": json.loads(pio.to_json(fig))["data"],
            "layout": json.loads(pio.to_json(fig))["layout"]}
    # </script> inside embedded JSON would close the tag early; escaping '<' stops that.
    payload = json.dumps(spec, separators=(",", ":")).replace("<", "\\u003c")
    gpu = "1" if (set(ch.traces) & GPU_TRACES) else "0"
    return (
        f'<div id="{div_id}" class="plotbox pending" data-gpu="{gpu}" '
        f'style="height:{ch.height}px">drawing on scroll</div>'
        f'<script type="application/json" id="spec-{div_id}">{payload}</script>'
    )


def _card(ch: Chart, frag: str) -> str:
    """One chart's card: title, call, shape, use-when, optional note, then the plot."""
    note = f'<div class="note"><b>Watch out:</b> {_esc(ch.note)}</div>' if ch.note else ""
    return f"""<article class="card">
  <h3>{_esc(ch.name)}</h3>
  <div class="meta">
    <div class="call">{_esc(ch.call)}</div>
    <div class="row"><b>Data shape:</b> {_esc(ch.shape)}</div>
    <div class="use"><b>Use when:</b> {_esc(ch.use_when)}</div>
    {note}
  </div>
  <div class="plot">{frag}</div>
</article>"""


def _blocked_card(ch: Chart) -> str:
    return f"""<article class="card blockedcard">
  <h3>{_esc(ch.name)}<span class="tag">CANNOT RENDER HERE</span></h3>
  <div class="meta">
    <div class="call">{_esc(ch.call)}</div>
    <div class="row"><b>Data shape:</b> {_esc(ch.shape)}</div>
    <div class="use"><b>Use when:</b> {_esc(ch.use_when)}</div>
  </div>
  <div class="blockedmsg"><b>Why not here:</b> {_esc(ch.blocked)}</div>
</article>"""


def build(offline: bool = False) -> tuple[str, int, int, list[str]]:
    """Render every registered chart and glue the fragments into one page."""
    rendered, failures = 0, []
    by_section: dict[str, list[str]] = {name: [] for name, _ in SECTIONS}
    trace_types: set[str] = set()

    for i, ch in enumerate(CHARTS):
        if ch.blocked:
            by_section[ch.section].append(_blocked_card(ch))
            continue
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                fig = ch.fn()
                fig.update_layout(height=ch.height, autosize=True,
                                  template=fig.layout.template or "wall")
                ch.traces = sorted({t.type for t in fig.data if t.type})
                trace_types.update(ch.traces)
                frag = _fig_block(ch, fig, f"fig{i:03d}")
            by_section[ch.section].append(_card(ch, frag))
            rendered += 1
        except Exception as exc:  # keep going, report at the end
            failures.append(f"{ch.section} / {ch.name}: {type(exc).__name__}: {exc}")
            broken = Chart(ch.section, ch.name, ch.call, ch.shape, ch.use_when,
                           blocked=f"Failed while building this page: "
                                   f"{type(exc).__name__}: {exc}")
            by_section[ch.section].append(_blocked_card(broken))

    n_blocked = sum(1 for c in CHARTS if c.blocked)
    nav = "".join(
        f'<a href="#{name.replace(" ", "-").lower()}">{name}</a>' for name, _ in SECTIONS
    )
    body = []
    for name, question in SECTIONS:
        cards = by_section[name]
        anchor = name.replace(" ", "-").lower()
        body.append(
            f'<section id="{anchor}"><div class="sechead">'
            f'<h2>{name} <span class="q">&ldquo;{question}&rdquo;</span></h2>'
            f'<div class="n">{len(cards)} charts</div></div>'
            f'<div class="grid">{"".join(cards)}</div></section>'
        )

    head = f"""<header>
  <h1>The Wall &mdash; every chart Plotly can make</h1>
  <p>Grouped by the question you walked in holding, not by the chart's name. Find your
     question, then find the card whose <b>data shape</b> matches the columns you actually
     have. The chart's name is the last thing you need to know.</p>
  <p>Every figure on this page is drawn from made-up numbers generated with numpy. Nothing
     here touched a database or the network. Press <kbd>Ctrl-F</kbd> and type a chart name
     to jump to it.</p>
  <div class="counts">
    <span class="pill"><b>{rendered}</b> charts rendered</span>
    <span class="pill"><b>{len(trace_types)}</b> of 49 trace types used</span>
    <span class="pill"><b>{n_blocked}</b> listed but unrenderable here</span>
    <span class="pill">plotly <b>6.9.0</b></span>
    <span class="pill">missing: <b>scipy, statsmodels, kaleido, scikit-image, plotly-geo</b></span>
  </div>
</header>"""

    libnote = (
        "This build has plotly.js <b>inlined</b>, so it needs no internet for the library itself."
        if offline else
        "This build loads plotly.js from <code>cdn.plot.ly</code>, so <b>the whole page needs "
        "internet to draw anything</b>. Rebuild with <code>--offline</code> to inline the "
        "library (~5 MB file) and remove that dependency."
    )
    foot = f"""<footer>
  <p><b>Trace types drawn on this page ({len(trace_types)}):</b> {", ".join(sorted(trace_types))}</p>
  <p><b>What this page needs from the network.</b> {libnote} Separately, the outline maps
     (choropleth, scatter_geo) fetch their country shapes from <code>cdn.plot.ly</code> when
     the page opens, so those specific panels need internet <em>even in</em>
     <code>--offline</code> mode. Every other chart is self-contained once the library loads.</p>
  <p><b>What this page cannot show you.</b> Static image export needs <code>kaleido</code>,
     which is not installed &mdash; interactive HTML works, PNG and SVG from Python do not.</p>
  <p>Rebuild with <code>python bench/wall.py</code>.</p>
</footer>"""

    # ONE copy of plotly.js for the whole page: a CDN tag (7 KB of HTML) or the
    # library inlined (~5 MB, works with no internet at all).
    if offline:
        lib = f"<script>{get_plotlyjs()}</script>"
    else:
        lib = (f'<script src="https://cdn.plot.ly/plotly-{get_plotlyjs_version()}'
               f'.min.js" charset="utf-8"></script>')

    runtime = (LAZY_JS.replace("%CONFIG%", json.dumps(PLOT_CONFIG))
                      .replace("%BUDGET%", str(GPU_BUDGET)))

    page = (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>The Wall - every Plotly chart type</title>"
        f"<style>{CSS}</style>{lib}</head><body>"
        f"{head}<nav>{nav}</nav><main>{''.join(body)}</main>{foot}"
        f"<script>{runtime}</script>"
        "</body></html>"
    )
    return page, rendered, n_blocked, failures


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the Plotly chart wall.")
    ap.add_argument("--no-open", action="store_true", help="build but do not open a browser")
    ap.add_argument("--offline", action="store_true",
                    help="inline plotly.js (~5 MB file, needs no internet)")
    args = ap.parse_args()

    print(f"Building {len(CHARTS)} charts ...")
    page, rendered, n_blocked, failures = build(offline=args.offline)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")

    size_kb = OUT.stat().st_size / 1024
    print(f"  rendered      : {rendered}")
    print(f"  listed-blocked: {n_blocked}")
    print(f"  file          : {OUT}  ({size_kb:,.0f} KB)")
    if failures:
        print(f"  FAILURES ({len(failures)}):")
        for f in failures:
            print(f"    - {f}")
    else:
        print("  failures      : none")

    if not args.no_open:
        webbrowser.open(OUT.as_uri())
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
