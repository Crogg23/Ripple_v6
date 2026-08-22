"""The Ripples lag-drift pass -- the reporting lag AS the indicator.

WHAT THIS IS
------------
The lag sweep (reports/time_index/lag.jsonl, 2026-08-20) measured, per
both-clock table, the per-cohort distribution of happened->reported delay.
This pass reads those curves and scores the DRIFT: is the pipe getting
slower, faster, or holding steady over its cohorts?

Chris's framing (2026-08-21): the gap between the world's clock and the
paperwork's clock is a vital sign of the institution doing the paperwork.
A stretching lag = an institution drowning before its output numbers drop.
A sudden shortening = behavior changed (new rule, new pressure, new lawyer).

CENSORING GUARD (the 2026-08-20 time-censoring memory, non-negotiable):
recent cohorts always look faster than they are, because slow reports for
recent events have not arrived yet. Every table's newest cohorts are dropped
before the drift is fit -- the buffer is that table's own p90 lag, rounded up
to whole cohort periods, floored at one period. What remains is a completed
record, so a measured drift is real drift, not the censoring artifact.

All impartial: every measured pipe gets the identical treatment, ranked by
the size of its drift, no pipe pre-picked. Local files only; no warehouse.
"""
import json
import math
import os
from datetime import date

import numpy as np

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
TIME_INDEX = os.path.join(BASE, "reports", "time_index")

MIN_COHORTS = 6          # need a curve, not two dots
MIN_N_PER_COHORT = 20    # a cohort of 3 rows has no median worth trusting
PRESENT_YEAR = 2026      # cohorts beyond this are future/placeholder keys


def cohort_year(period):
    try:
        return int(str(period)[:4])
    except ValueError:
        return None


def main():
    rows = [json.loads(l) for l in open(os.path.join(TIME_INDEX, "lag.jsonl"))]
    results = []
    for r in rows:
        unit_days = 365.0 if r["unit"] == "years" else 1.0
        pts = []
        for p in r["points"]:
            y = cohort_year(p["period"])
            if y is None or y > PRESENT_YEAR or p["n"] < MIN_N_PER_COHORT:
                continue
            if p["p50"] is None or p["p50"] < 0:
                continue  # negative medians = clocks mislabelled, not a lag
            pts.append((y, p["p50"] * unit_days, p["p90"] * unit_days if p["p90"] is not None else None, p["n"]))
        if len(pts) < MIN_COHORTS:
            continue
        pts.sort()
        # censoring buffer: this table's own p90 lag, in whole years, min 1
        p90s = [p[2] for p in pts if p[2] is not None]
        buffer_years = max(1, math.ceil((np.median(p90s) if p90s else 0) / 365.0))
        cutoff = PRESENT_YEAR - buffer_years
        kept = [p for p in pts if p[0] <= cutoff]
        if len(kept) < MIN_COHORTS:
            continue
        years = np.array([p[0] for p in kept], dtype=float)
        med = np.array([p[1] for p in kept], dtype=float)
        # weighted straight-line fit of median lag over cohort year
        w = np.sqrt(np.array([p[3] for p in kept], dtype=float))
        slope, intercept = np.polyfit(years, med, 1, w=w)
        mean_lag = float(np.average(med, weights=w))
        if mean_lag <= 0:
            continue
        # recent-vs-early shift, a fit-free second opinion
        third = max(2, len(kept) // 3)
        early = float(np.median(med[:third]))
        late = float(np.median(med[-third:]))
        results.append({
            "table": r["table"],
            "happened_col": r["happened_col"], "reported_col": r["down_col"],
            "reported_role": r["down_role"],
            "n_rows": r["n_rows"],
            "cohorts_used": len(kept),
            "cohort_span": f"{int(years[0])}-{int(years[-1])}",
            "censoring_buffer_years": buffer_years,
            "mean_median_lag_days": round(mean_lag, 1),
            "drift_days_per_year": round(float(slope), 2),
            "drift_pct_per_year": round(100 * slope / mean_lag, 2),
            "early_median_days": round(early, 1),
            "late_median_days": round(late, 1),
            "shift_pct": round(100 * (late - early) / early, 1) if early > 0 else None,
            # Verdict on the early-vs-late shift, not slope/mean: dividing the
            # slope by the whole-span mean let a pipe that QUADRUPLED read as
            # "steady" (caught by the planted-signal test, 2026-08-21).
            "verdict": ("unscored" if early <= 0 else
                        "stretching" if late >= 1.2 * early else
                        "shrinking" if late <= 0.8 * early else "steady"),
        })
    results.sort(key=lambda x: -abs(x["drift_pct_per_year"]))
    out = os.path.join(BASE, "reports",
                       f"ripples_lag_drift_{date.today().isoformat()}.json")
    with open(out, "w") as fh:
        json.dump(results, fh, indent=1)
    from collections import Counter
    print(f"{len(rows)} measured pipes in; {len(results)} scoreable after the "
          f"censoring guard")
    print(Counter(x["verdict"] for x in results))
    print(f"Wrote {out}")
    for x in results[:12]:
        print(f"  {x['verdict']:10s} {x['drift_pct_per_year']:+7.1f}%/yr  "
              f"lag~{x['mean_median_lag_days']:8.0f}d  {x['table']}")


if __name__ == "__main__":
    main()
