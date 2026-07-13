#!/usr/bin/env python3
"""Threshold-bunching detector v2 — calibration battery.

Metric v2 ("plateau shift"): median of the 8 bins 2..9 below the center vs the
median of the 8 bins 2..9 above it. The two bins adjacent to the center are
excluded on purpose — the exact-at-line / exact-round-value spike lives there,
which is what confounded metric v1. v2 measures whether the *level* of the
distribution drops across the center, which a round number does not produce.

The harness is C-shaped (era test ready):
  - signature is (table, amount_col, instrument, center, time_window)
  - the metric is computed per fiscal year inside the window
  - lines are one entity with effective-dated values, not one value per line

Fire threshold: set empirically from a null distribution — 40 seeded-random
centers that are neither lines nor round numbers ($5k multiples, not $25k
multiples, >=$60k from every registered line value). Fire = score > null p95.

Run:
    python3 scripts/detector_bunching_battery.py

Outputs:
    - battery table + full null distribution printed
    - outputs/detector_bunching_battery_2026-07-13.html (null histogram +
      battery markers)
    - one-line verdict
"""

from __future__ import annotations

import os
import random
import statistics
from dataclasses import dataclass, field

from dotenv import load_dotenv
import snowflake.connector
import plotly.graph_objects as go

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(REPO, "library-onboarding", ".env"))

TABLE = "LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS"
AMOUNT_COL = "federal_action_obligation"
BIN = 5_000
PLATEAU = range(2, 10)          # bins 2..9 on each side of the center
DENSITY_FLOOR = 30              # min plateau median per side, else score=None
TIME_WINDOW = ("2024-10-01", "2025-09-30")   # FY2025
AMT_CAP = 3_000_000             # fetch ceiling; all centers sit far below
NULL_N = 40
NULL_SEED = 20260713
NULL_RANGE = (100_000, 690_000)
NULL_LINE_BUFFER = 60_000       # metric reaches 45k out; buffer past that
OUT_HTML = os.path.join(REPO, "outputs", "detector_bunching_battery_2026-07-13.html")


# ---------------------------------------------------------------- line registry
@dataclass
class LineValue:
    value: int
    eff_from: str | None        # None = unknown/open start
    eff_to: str | None          # None = still in force
    verified: str               # what was actually verified, and what wasn't


@dataclass
class Line:
    name: str
    binds_on: tuple             # instrument types the line binds on, per rule text
    values: list
    note: str = ""

    def value_in_force(self, window):
        """The single value in force for the whole window. Raises on era
        straddle — the caller (C's loop) must split the window per era."""
        start, end = window
        hits = [
            v for v in self.values
            if (v.eff_from is None or v.eff_from <= start)
            and (v.eff_to is None or v.eff_to > end)
        ]
        if len(hits) != 1:
            raise ValueError(f"{self.name}: window {window} straddles eras or "
                             f"matches {len(hits)} values — split the window")
        return hits[0]


LINES = {
    "SAT": Line(
        name="simplified_acquisition_threshold",
        binds_on=("DELIVERY ORDER", "DEFINITIVE CONTRACT", "BPA CALL"),
        values=[
            LineValue(150_000, "2010-10-01", "2020-08-31",
                      "UNVERIFIED era boundaries — verify before any pre-2020 run"),
            LineValue(250_000, "2020-08-31", "2025-10-01",
                      "in force all FY2025 VERIFIED (Fed. Register 2025-16412); "
                      "2020 start date UNVERIFIED"),
            LineValue(350_000, "2025-10-01", None,
                      "VERIFIED (Fed. Register 2025-16412, acquisition.gov)"),
        ],
        note="PURCHASE ORDER is mechanically capped at the SAT, so it has no "
             "above-line population: plateau metric undefined, and no clean "
             "null range remains below the cap. Excluded from the battery.",
    ),
    "SUBK_PLAN": Line(
        name="subcontracting_plan_threshold",
        binds_on=("DEFINITIVE CONTRACT",),
        values=[
            LineValue(750_000, None, "2025-10-01", "in force FY2025 VERIFIED (FAR 19.702)"),
            LineValue(900_000, "2025-10-01", None, "VERIFIED (Oct 2025 inflation adjustment)"),
        ],
        note="Binds per contract for other-than-small offerors; for IDVs it is "
             "evaluated at the IDV level, NOT per delivery order. Small-business "
             "awards are exempt and the table has no size flag -> diluted.",
    ),
    "TINA": Line(
        name="certified_cost_or_pricing_data_threshold",
        binds_on=(),   # binds on a pricing-basis subset, not an instrument type
        values=[
            LineValue(2_000_000, "2018-07-01", "2025-10-01", "VERIFIED (FAR 15.403-4)"),
        ],
        note="DROPPED from the battery: applies to negotiated actions without "
             "adequate price competition — the table has no competition or "
             "pricing-basis column, so the bound population cannot be filtered.",
    ),
}

# Line values a null center must keep its distance from (residual $150k included).
NULL_AVOID = sorted({v.value for ln in LINES.values() for v in ln.values})


# ---------------------------------------------------------------- battery spec
@dataclass
class Test:
    label: str
    instrument: str
    center: int
    expect: str                 # pre-registered expectation
    blind: bool                 # False = distribution already seen before this run
    scored: bool = True         # False = descriptive probe, not pass/fail
    result: dict = field(default_factory=dict)


BATTERY = [
    Test("P1  SAT $250k (line in force, binds here)", "DELIVERY ORDER", 250_000,
         "FIRE", blind=False),
    Test("N1  $450k (assigned control, no line)", "DELIVERY ORDER", 450_000,
         "silent", blind=False),
    Test("N2  $350k (SAT value effective 2025-10-01 — after window)", "DELIVERY ORDER",
         350_000, "silent — line not yet in force", blind=True),
    Test("N3  $750k (line binds on DEFINITIVE CONTRACT, not here)", "DELIVERY ORDER",
         750_000, "silent — wrong instrument", blind=True),
    Test("PROBE  $750k subK plan on DEFINITIVE CONTRACT", "DEFINITIVE CONTRACT",
         750_000,
         "at-line spike WITHOUT level shift (post-hoc: shape seen in density check)",
         blind=False, scored=False),
]


# ---------------------------------------------------------------------- fetch
# Dedupe to base awards over the FULL table first, then filter base actions to
# the time window — so the same SQL stays correct when the table spans >1 FY.
SQL = f"""
WITH base AS (
  SELECT award_type,
         TRY_TO_DATE(action_date) AS d,
         TRY_TO_NUMBER({AMOUNT_COL}, 38, 2) AS amt
  FROM {TABLE}
  WHERE award_type IN (%(i1)s, %(i2)s)
  QUALIFY ROW_NUMBER() OVER (
    PARTITION BY contract_award_unique_key
    ORDER BY TRY_TO_DATE(action_date) ASC,
             TRY_TO_NUMBER({AMOUNT_COL}, 38, 2) DESC
  ) = 1
)
SELECT award_type,
       YEAR(DATEADD(month, 3, d))    AS fy,
       QUARTER(DATEADD(month, 3, d)) AS fq,
       CEIL(amt / {BIN}) * {BIN}     AS bin_upper,
       COUNT(*)                      AS n
FROM base
WHERE d BETWEEN %(win_start)s AND %(win_end)s
  AND amt > 0 AND amt <= {AMT_CAP}
GROUP BY 1, 2, 3, 4
"""


def fetch(instruments, window):
    """-> {instrument: {(fy, fq): {bin_upper: n}}}"""
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
        cur.execute(SQL, {"i1": instruments[0], "i2": instruments[1],
                          "win_start": window[0], "win_end": window[1]})
        out = {i: {} for i in instruments}
        for itype, fy, fq, b, n in cur.fetchall():
            out[itype].setdefault((int(fy), int(fq)), {})[int(b)] = int(n)
        return out
    finally:
        conn.close()


def merge_bins(per_quarter, keys=None):
    """Sum quarter-grain bins into one dict (FY grain, or any subset of keys)."""
    tot = {}
    for k, bins in per_quarter.items():
        if keys is not None and k not in keys:
            continue
        for b, n in bins.items():
            tot[b] = tot.get(b, 0) + n
    return tot


# --------------------------------------------------------------------- metric
def metric_v2(bins, center):
    """Plateau shift: median(bins 2..9 below) / median(bins 2..9 above)."""
    below = [bins.get(center - i * BIN, 0) for i in PLATEAU]
    above = [bins.get(center + (i + 1) * BIN, 0) for i in PLATEAU]
    mb, ma = statistics.median(below), statistics.median(above)
    ok = mb >= DENSITY_FLOOR and ma >= DENSITY_FLOOR
    return {"score": (mb / ma) if (ok and ma) else None,
            "below_med": mb, "above_med": ma, "ok": ok}


def metric_v1(bins, center):
    """v1 for the probe row: bin just below / bin just above."""
    b, a = bins.get(center, 0), bins.get(center + BIN, 0)
    return b / a if a else None


# ----------------------------------------------------------------------- null
def null_centers():
    rng = random.Random(NULL_SEED)
    lo, hi = NULL_RANGE
    picked = set()
    while len(picked) < NULL_N:
        c = rng.randrange(lo // BIN, hi // BIN + 1) * BIN
        if c % 25_000 == 0:
            continue                          # round-number attractor
        if min(abs(c - v) for v in NULL_AVOID) <= NULL_LINE_BUFFER:
            continue                          # too close to a registered line
        picked.add(c)
    return sorted(picked)


def pctl(sorted_vals, p):
    """Linear-interpolated percentile of a pre-sorted list."""
    idx = p * (len(sorted_vals) - 1)
    lo, frac = int(idx), idx - int(idx)
    return sorted_vals[lo] + frac * (sorted_vals[min(lo + 1, len(sorted_vals) - 1)] - sorted_vals[lo])


# ---------------------------------------------------------------------- chart
SURFACE, SERIES, INK, INK_2 = "#fcfcfb", "#2a78d6", "#0b0b0b", "#52514e"
MUTED, GRID, BASELINE = "#898781", "#e1e0d9", "#c3c2b7"
POSITIVE_C, NEGATIVE_C = "#4a3aa7", "#1baf7a"     # categorical slots 5 and 2
FONT = 'system-ui, -apple-system, "Segoe UI", sans-serif'


def render_chart(null_scores, threshold, tests):
    lo = min(null_scores + [t.result["score"] for t in tests if t.scored]) - 0.05
    hi = max(null_scores + [t.result["score"] for t in tests if t.scored]) + 0.05
    step = 0.025
    edges, counts = [], {}
    for s in null_scores:
        b = round(int((s - lo) / step) * step + lo, 4)
        counts[b] = counts.get(b, 0) + 1
    edges = sorted(counts)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[e + step / 2 for e in edges], y=[counts[e] for e in edges],
        width=step * 0.9, marker_color=SERIES, name="null centers (n=40)",
        hovertemplate="score %{x:.3f}: %{y} centers<extra></extra>",
    ))
    fig.add_vline(x=threshold, line_dash="dash", line_color=MUTED, line_width=1)
    fig.add_annotation(x=threshold, y=0.78, yref="y domain", yanchor="top",
                       xanchor="left", xshift=6,
                       text=f"fire threshold =<br>null p95 = {threshold:.3f}",
                       align="left", showarrow=False,
                       font=dict(color=MUTED, size=11))
    ymax = max(counts.values())
    for t in tests:
        if not t.scored or t.result["score"] is None:
            continue
        color = POSITIVE_C if t.expect == "FIRE" else NEGATIVE_C
        short = t.label.split("  ")[0]
        fig.add_trace(go.Scatter(
            x=[t.result["score"]], y=[ymax * 0.55], mode="markers+text",
            marker=dict(symbol="diamond", size=12, color=color,
                        line=dict(width=2, color=SURFACE)),
            text=[short], textposition="top center",
            textfont=dict(color=INK_2, size=11),
            name=("expected fire" if t.expect == "FIRE" else "expected silent"),
            legendgroup=("fire" if t.expect == "FIRE" else "silent"),
            showlegend=(short in ("P1", "N1")),
            hovertemplate=f"{t.label}: %{{x:.3f}}<extra></extra>",
        ))
    fig.update_xaxes(title="metric v2 score (plateau below / plateau above)",
                     linecolor=BASELINE, tickcolor=BASELINE,
                     tickfont=dict(color=MUTED), showgrid=False)
    fig.update_yaxes(title="null centers per bucket", range=[0, ymax * 1.35],
                     gridcolor=GRID, zeroline=False, tickfont=dict(color=MUTED))
    fig.update_layout(
        title=dict(text=("Detector calibration — null distribution vs battery, FY2025"
                         "<br><sup>Delivery-order base obligations; 40 seeded-random "
                         "non-line, non-round centers form the null. Diamonds are the "
                         "battery tests.</sup>"),
                   font=dict(color=INK, size=16)),
        paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
        font=dict(family=FONT, color=INK_2), bargap=0.05,
        legend=dict(orientation="h", y=1.06, x=1, xanchor="right"),
        margin=dict(t=120, b=70, l=70, r=30), height=520, width=1100,
    )
    os.makedirs(os.path.dirname(OUT_HTML), exist_ok=True)
    fig.write_html(OUT_HTML, include_plotlyjs="cdn")


# ----------------------------------------------------------------------- main
def main():
    # sanity: every battery line value must be the one in force for the window
    assert LINES["SAT"].value_in_force(TIME_WINDOW).value == 250_000
    assert LINES["SUBK_PLAN"].value_in_force(TIME_WINDOW).value == 750_000

    data = fetch(("DELIVERY ORDER", "DEFINITIVE CONTRACT"), TIME_WINDOW)
    fys = sorted({fy for fy, _ in data["DELIVERY ORDER"]})
    print(f"time window {TIME_WINDOW} -> fiscal years in data: {fys}\n")

    # battery + null are evaluated per FY (one FY here; C loops this)
    for fy in fys:
        fy_keys = {(fy, q) for q in (1, 2, 3, 4)}
        do_bins = merge_bins(data["DELIVERY ORDER"], fy_keys)
        dc_bins = merge_bins(data["DEFINITIVE CONTRACT"], fy_keys)
        bins_for = {"DELIVERY ORDER": do_bins, "DEFINITIVE CONTRACT": dc_bins}

        centers = null_centers()
        null_scores = []
        for c in centers:
            m = metric_v2(do_bins, c)
            if m["score"] is not None:
                null_scores.append(round(m["score"], 4))
        null_scores.sort()
        thr = pctl(null_scores, 0.95)

        print(f"== FY{fy} ==")
        print(f"null: {len(null_scores)}/{len(centers)} centers usable "
              f"(density floor {DENSITY_FLOOR}/bin)")
        print(f"null scores: min {null_scores[0]:.3f} | p50 "
              f"{pctl(null_scores, .5):.3f} | p90 {pctl(null_scores, .9):.3f} | "
              f"p95 {thr:.3f} | max {null_scores[-1]:.3f}")
        print(f"null centers+scores: "
              f"{list(zip(centers, null_scores)) if len(null_scores)==len(centers) else 'see below'}\n")

        print(f"{'test':64} {'v2':>7} {'v1':>7}  expectation")
        results = []
        for t in BATTERY:
            m = metric_v2(bins_for[t.instrument], t.center)
            t.result = {**m, "v1": metric_v1(bins_for[t.instrument], t.center)}
            v2s = f"{m['score']:.3f}" if m["score"] is not None else "  n/a"
            v1s = f"{t.result['v1']:.3f}" if t.result["v1"] else "  n/a"
            print(f"{t.label:64} {v2s:>7} {v1s:>7}  {t.expect}"
                  f"{'' if t.blind else '  [seen before run]'}")
            if t.scored:
                fired = m["score"] is not None and m["score"] > thr
                results.append((t, fired))
        print()

        # per-quarter stability of P1 (the slice-thinness test for C)
        print("P1 per fiscal quarter (metric must survive slicing):")
        for q in (1, 2, 3, 4):
            qbins = merge_bins(data["DELIVERY ORDER"], {(fy, q)})
            m = metric_v2(qbins, 250_000)
            s = f"{m['score']:.3f}" if m["score"] is not None else "n/a (floor)"
            print(f"  FY{fy}Q{q}: {s}  (plateau medians {m['below_med']:.0f}/{m['above_med']:.0f})")
        print()

        render_chart(null_scores, thr, BATTERY)
        print(f"chart: {OUT_HTML}")

        ok = all(fired == (t.expect == "FIRE") for t, fired in results)
        parts = ", ".join(f"{t.label.split('  ')[0]} {'fired' if f else 'silent'}"
                          f" ({t.result['score']:.3f})" for t, f in results)
        print(f"\nverdict FY{fy}: {parts}; threshold {thr:.3f} -> "
              f"{'CALIBRATED' if ok else 'NOT CALIBRATED'}")


if __name__ == "__main__":
    main()
