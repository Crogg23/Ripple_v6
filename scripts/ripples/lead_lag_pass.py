"""The Ripples lead-lag pass (Box 3 + Box 4 of the flow ladder, docs/RIPPLES.md).

WHAT THIS IS
------------
The trend sweep (reports/time_index/series.jsonl, 2026-08-20) measured every
stream alone. This pass measures streams AGAINST EACH OTHER, impartially:
every qualifying pair gets the identical treatment, no pair is pre-picked.

Per pair of streams sharing a grain and enough overlap:
  Box 3 (co-movement): correlation of period-over-period changes at lag 0.
  Box 4 (lead-lag):    the lag offset (in periods) that maximizes |corr|;
                       a consistent nonzero best lag = one stream leads.

NULL CHECK (landmine 2, non-negotiable): for each pair, the changes of one
series are circularly shifted at every possible rotation; the observed best
|corr| must beat the 95th percentile of that rotation distribution to survive.
Circular shifts preserve each series' own autocorrelation, which plain
shuffling would destroy (and plain shuffling makes everything look
significant).

RAGGED-CLOCK GUARD (landmine 1): each stream is annotated with its table's
median reporting lag from lag_ranked.csv where measured. A "lead" smaller
than the DIFFERENCE in the two streams' reporting lags is flagged
fax_machine_suspect=True: A may only "lead" B because A's paperwork is filed
faster. Those pairs are kept and labelled, never dropped -- the lag is itself
information (Chris, 2026-08-21: a landmine is a wrong explanation, not
forbidden data).

Runs entirely from files on disk. No warehouse connection, no writes outside
reports/.
"""
import csv
import json
import os
from collections import defaultdict
from datetime import date

import numpy as np

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
TIME_INDEX = os.path.join(BASE, "reports", "time_index")

MIN_MONTHLY_OVERLAP = 36   # 3 years of common months
MIN_YEARLY_OVERLAP = 10    # 10 common years
MAX_LAG_MONTHLY = 12       # search offsets up to a year
MAX_LAG_YEARLY = 3         # up to 3 years
NULL_PCTILE = 95
MIN_ABS_CORR = 0.3         # below this, "significant" is still not interesting
TAIL_TRIM_MONTHS = 6       # drop the newest months: incomplete periods fake collapses
TAIL_TRIM_YEARS = 1


def load_series():
    out = []
    with open(os.path.join(TIME_INDEX, "series.jsonl")) as fh:
        for line in fh:
            s = json.loads(line)
            if s["bucket"] == "month" and s["n_points"] >= MIN_MONTHLY_OVERLAP:
                out.append(s)
            elif s["bucket"] == "year" and s["n_points"] >= MIN_YEARLY_OVERLAP:
                out.append(s)
    return out


def load_reporting_lags():
    """table -> median reporting lag in days, where the lag pass measured one."""
    lags = {}
    path = os.path.join(TIME_INDEX, "lag_ranked.csv")
    if not os.path.exists(path):
        return lags
    with open(path) as fh:
        for row in csv.DictReader(fh):
            try:
                v = float(row["median_lag"])
            except (ValueError, KeyError):
                continue
            unit = row.get("unit", "days")
            days = v * (365.0 if unit == "years" else 1.0)
            if row.get("clocks_reversed") == "True" or days < 0:
                continue  # a mislabelled clock is not a lag measurement
            t = row["table"]
            lags[t] = min(lags.get(t, float("inf")), days)
    return {t: v for t, v in lags.items() if v != float("inf")}


def to_vector(s):
    """series -> (sorted period keys, counts). Trims the incomplete tail."""
    pts = sorted(s["points"], key=lambda p: p[0])
    trim = TAIL_TRIM_MONTHS if s["bucket"] == "month" else TAIL_TRIM_YEARS
    if trim and len(pts) > trim:
        pts = pts[:-trim]
    return {p[0]: float(p[1]) for p in pts}


def changes(vals, months=None):
    """log-difference of counts, the scale-free 'did it move' signal.
    For monthly series, the month-of-year mean change is subtracted first --
    otherwise every pair of seasonal streams "co-moves" on the government's
    shared calendar (fiscal years, court terms, filing seasons), which the
    first run of this pass demonstrated at scale."""
    v = np.log1p(np.asarray(vals, dtype=float))
    d = np.diff(v)
    if months is not None:
        m = np.asarray(months[1:])
        for mo in set(m.tolist()):
            idx = m == mo
            d[idx] = d[idx] - d[idx].mean()
    return d


def best_lag_corr(a, b, max_lag):
    """(best_lag, best_corr, corr_at_zero). Positive lag = a leads b."""
    best = (0, 0.0)
    zero = 0.0
    for lag in range(-max_lag, max_lag + 1):
        if lag >= 0:
            x, y = a[: len(a) - lag or None], b[lag:]
        else:
            x, y = a[-lag:], b[: len(b) + lag or None]
        if len(x) < 8 or np.std(x) == 0 or np.std(y) == 0:
            continue
        c = float(np.corrcoef(x, y)[0, 1])
        if lag == 0:
            zero = c
        if abs(c) > abs(best[1]):
            best = (lag, c)
    return best[0], best[1], zero


def null_threshold(a, b, max_lag):
    """95th pct of best |corr| over every circular rotation of b's changes."""
    n = len(b)
    vals = []
    for rot in range(1, n):
        if abs(rot) <= max_lag or abs(rot - n) <= max_lag:
            continue  # rotations that reproduce a tested lag are not null
        br = np.roll(b, rot)
        _, c, _ = best_lag_corr(a, br, max_lag)
        vals.append(abs(c))
    if not vals:
        return 1.0
    return float(np.percentile(vals, NULL_PCTILE))


def main():
    series = load_series()
    rep_lags = load_reporting_lags()
    monthly = [s for s in series if s["bucket"] == "month"]
    yearly = [s for s in series if s["bucket"] == "year"]
    print(f"{len(monthly)} monthly + {len(yearly)} yearly streams qualify")

    vectors = {}
    for s in series:
        key = (s["table"], s["column"])
        vectors[key] = (s, to_vector(s))

    results = []
    tested = 0
    for bucket, pool, max_lag, min_overlap in (
        ("month", monthly, MAX_LAG_MONTHLY, MIN_MONTHLY_OVERLAP),
        ("year", yearly, MAX_LAG_YEARLY, MIN_YEARLY_OVERLAP),
    ):
        for i in range(len(pool)):
            si = pool[i]
            ki = (si["table"], si["column"])
            for j in range(i + 1, len(pool)):
                sj = pool[j]
                if sj["table"] == si["table"]:
                    continue  # same table's columns co-move by construction
                kj = (sj["table"], sj["column"])
                common = sorted(set(vectors[ki][1]) & set(vectors[kj][1]))
                if len(common) < min_overlap:
                    continue
                months = ([int(str(p)[5:7]) for p in common]
                          if bucket == "month" else None)
                a = changes([vectors[ki][1][p] for p in common], months)
                b = changes([vectors[kj][1][p] for p in common], months)
                if np.std(a) == 0 or np.std(b) == 0:
                    continue
                tested += 1
                lag, corr, zero = best_lag_corr(a, b, max_lag)
                if abs(corr) < MIN_ABS_CORR:
                    continue
                thr = null_threshold(a, b, max_lag)
                if abs(corr) <= thr:
                    continue
                period_days = 30.4 if bucket == "month" else 365.0
                la = rep_lags.get(si["table"])
                lb = rep_lags.get(sj["table"])
                fax = None
                if lag != 0 and la is not None and lb is not None:
                    leader_lag, follower_lag = (la, lb) if lag > 0 else (lb, la)
                    fax = (follower_lag - leader_lag) >= abs(lag) * period_days
                results.append({
                    "bucket": bucket,
                    "a_table": si["table"], "a_column": si["column"],
                    "a_clock": si["clock"], "a_rows": si["n_rows"],
                    "b_table": sj["table"], "b_column": sj["column"],
                    "b_clock": sj["clock"], "b_rows": sj["n_rows"],
                    "n_common_periods": len(common),
                    "corr_at_zero": round(zero, 3),
                    "best_lag_periods": lag,
                    "best_corr": round(corr, 3),
                    "null_95_threshold": round(thr, 3),
                    "margin_over_null": round(abs(corr) - thr, 3),
                    "leader": (si["table"] if lag > 0 else sj["table"]) if lag != 0 else None,
                    "a_reporting_lag_days": la, "b_reporting_lag_days": lb,
                    "fax_machine_suspect": fax,
                })
            if i % 25 == 0:
                print(f"  [{bucket}] {i}/{len(pool)} streams paired, "
                      f"{tested:,} pairs tested, {len(results):,} survive so far")

    results.sort(key=lambda r: -r["margin_over_null"])
    out = os.path.join(BASE, "reports",
                       f"ripples_lead_lag_deseasonalized_{date.today().isoformat()}.json")
    with open(out, "w") as fh:
        json.dump({"tested_pairs": tested, "survivors": results}, fh, indent=1)
    n_lead = sum(1 for r in results if r["best_lag_periods"] != 0)
    n_fax = sum(1 for r in results if r["fax_machine_suspect"])
    print(f"\n{tested:,} pairs tested; {len(results):,} beat the rotation null; "
          f"{n_lead:,} with a nonzero lead; {n_fax:,} flagged fax-machine-suspect")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
