#!/usr/bin/env python3
"""Threshold-bunching detector — calibration harness.

Tests whether the detector fires on a known positive (the FY2025 Simplified
Acquisition Threshold, $250,000) and stays silent on a known negative (a round
number with no regulatory meaning, $450,000), using identical SQL for both.

Data: LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS (FY2025 prime contract
actions). "Base award" = earliest action per CONTRACT_AWARD_UNIQUE_KEY
(largest same-day obligation as tie-break), positive amounts only, single
award type (DELIVERY ORDER). Bins are right-closed — ($245k, $250k] — so an
award of exactly $250,000 counts below the line, matching "not exceeding the
simplified acquisition threshold".

Run:
    python3 scripts/detector_threshold_bunching.py

Outputs:
    - both distributions printed as tables
    - one summary ratio per distribution (bin just below / bin just above)
    - outputs/detector_threshold_bunching_2026-07-12.html (side-by-side chart)
    - a one-line detector verdict
"""

import os

from dotenv import load_dotenv
import snowflake.connector
import plotly.graph_objects as go
from plotly.subplots import make_subplots

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(REPO, "library-onboarding", ".env"))

TABLE = "LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS"
AWARD_TYPE = "DELIVERY ORDER"
BIN = 5_000
HALF_WINDOW = 100_000
PANELS = [
    ("Known positive — Simplified Acquisition Threshold", 250_000),
    ("Control — round number, no known reporting line", 450_000),
]
OUT_HTML = os.path.join(REPO, "outputs", "detector_threshold_bunching_2026-07-12.html")

# The one query, identical for both panels; only %(center)s changes.
SQL = f"""
WITH base AS (
  SELECT TRY_TO_NUMBER(federal_action_obligation, 38, 2) AS amt
  FROM {TABLE}
  WHERE award_type = %(award_type)s
  QUALIFY ROW_NUMBER() OVER (
    PARTITION BY contract_award_unique_key
    ORDER BY TRY_TO_DATE(action_date) ASC,
             TRY_TO_NUMBER(federal_action_obligation, 38, 2) DESC
  ) = 1
)
SELECT CEIL(amt / {BIN}) * {BIN} AS bin_upper, COUNT(*) AS n_awards
FROM base
WHERE amt > %(center)s - {HALF_WINDOW}
  AND amt <= %(center)s + {HALF_WINDOW}
GROUP BY 1
ORDER BY 1
"""

# Reference palette (dataviz skill, light mode)
SURFACE = "#fcfcfb"
SERIES = "#2a78d6"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
FONT = 'system-ui, -apple-system, "Segoe UI", sans-serif'


def fetch_bins(cur, center):
    cur.execute(SQL, {"award_type": AWARD_TYPE, "center": center})
    return {int(b): int(n) for b, n in cur.fetchall()}


def kfmt(v):
    return f"${v / 1000:,.0f}k"


def main():
    conn = snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PAT"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        role=os.environ.get("SNOWFLAKE_ROLE") or None,
        session_parameters={"STATEMENT_TIMEOUT_IN_SECONDS": 600},
    )
    try:
        cur = conn.cursor()
        results = [(title, center, fetch_bins(cur, center)) for title, center in PANELS]
    finally:
        conn.close()

    fig = make_subplots(
        rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.06,
        subplot_titles=[t for t, _, _ in results],
    )

    ratios = []
    for i, (title, center, bins) in enumerate(results, start=1):
        below, above = bins.get(center, 0), bins.get(center + BIN, 0)
        ratio = below / above if above else float("inf")
        ratios.append((title, center, below, above, ratio))

        edges = sorted(bins)
        xs = [e - BIN / 2 for e in edges]           # bar sits on its bin's midpoint
        ys = [bins[e] for e in edges]
        fig.add_trace(
            go.Bar(
                x=xs, y=ys, width=BIN * 0.9, marker_color=SERIES,
                customdata=[[kfmt(e - BIN), kfmt(e)] for e in edges],
                hovertemplate="(%{customdata[0]} – %{customdata[1]}]: %{y:,} awards<extra></extra>",
                showlegend=False,
            ),
            row=1, col=i,
        )
        fig.add_vline(
            x=center, line_dash="dash", line_color=MUTED, line_width=1, row=1, col=i,
        )
        fig.add_annotation(
            x=center, y=0.97, yref=f"y{'' if i == 1 else i} domain",
            text=f"center {kfmt(center)}", showarrow=False, yanchor="top",
            font=dict(color=MUTED, size=11), row=1, col=i,
        )
        # selective direct labels: only the two bins the summary ratio uses
        for edge, n, anchor in [(center, below, "right"), (center + BIN, above, "left")]:
            fig.add_annotation(
                x=edge - BIN / 2, y=n, text=f"{n:,}", showarrow=False,
                yanchor="bottom", xanchor=anchor, yshift=2,
                font=dict(color=INK_2, size=11), row=1, col=i,
            )
        tick0 = (center - HALF_WINDOW) // 50_000 * 50_000 + 50_000
        tickvals = list(range(tick0, center + HALF_WINDOW + 1, 50_000))
        fig.update_xaxes(
            tickvals=tickvals, ticktext=[kfmt(v) for v in tickvals],
            linecolor=BASELINE, tickcolor=BASELINE, tickfont=dict(color=MUTED),
            showgrid=False, row=1, col=i,
        )

    ymax = max(max(b.values()) for _, _, b in results)
    fig.update_yaxes(
        range=[0, ymax * 1.12], gridcolor=GRID, gridwidth=1, zeroline=False,
        tickfont=dict(color=MUTED), row=1, col=1,
    )
    fig.update_yaxes(range=[0, ymax * 1.12], showgrid=True, gridcolor=GRID,
                     zeroline=False, tickfont=dict(color=MUTED), row=1, col=2)
    fig.update_layout(
        title=dict(
            text=(f"Base {AWARD_TYPE.lower()} obligations, FY2025 — awards per {kfmt(BIN)} bin"
                  f"<br><sup>Same query, same window (±{kfmt(HALF_WINDOW)}), same bins;"
                  f" only the center point differs. Bins right-closed: exactly-at-center"
                  f" counts below the line.</sup>"),
            font=dict(color=INK, size=16),
        ),
        paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
        font=dict(family=FONT, color=INK_2),
        bargap=0.1, margin=dict(t=110, b=60, l=70, r=30), height=520, width=1200,
    )

    os.makedirs(os.path.dirname(OUT_HTML), exist_ok=True)
    fig.write_html(OUT_HTML, include_plotlyjs="cdn")

    print(f"\nwindow = center ±{kfmt(HALF_WINDOW)}, bins = {kfmt(BIN)}, "
          f"award_type = {AWARD_TYPE}, base actions only, amounts > 0\n")
    for (title, center, bins), (_, _, below, above, ratio) in zip(results, ratios):
        print(f"--- {title} (center {kfmt(center)}) ---")
        for e in sorted(bins):
            marker = " <== just below" if e == center else (" <== just above" if e == center + BIN else "")
            print(f"  ({kfmt(e - BIN)} – {kfmt(e)}]  {bins[e]:>6,}{marker}")
        print(f"  summary: below/above = {below:,}/{above:,} = {ratio:.2f}\n")

    pos, neg = ratios[0][4], ratios[1][4]
    fired_pos, fired_neg = pos >= 2.0, neg >= 2.0
    print(f"chart: {OUT_HTML}")
    print(f"verdict: positive ratio {pos:.2f} ({'fired' if fired_pos else 'silent'}), "
          f"control ratio {neg:.2f} ({'fired' if fired_neg else 'silent'}) -> "
          f"{'CALIBRATED' if fired_pos and not fired_neg else 'NOT CALIBRATED'} "
          f"(fire threshold: ratio >= 2.0)")


if __name__ == "__main__":
    main()
