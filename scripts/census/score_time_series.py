"""Score every warehouse time series for how strange its shape is, then rank.

The point of the census-on-the-time-axis: don't pick a trend, measure the same
shapes across everything and let the outliers nominate themselves. Nobody is
singled out; every series is measured with the same ruler.

Nine shapes, each scored 0-1 from the series alone (no joins, no second table):

  pile_up      most of the rows land in ONE period -- almost always a load
               artifact, occasionally a real mass event
  sudden_stop  the series ends long before the data's own latest date -- a
               publisher went quiet, or an ingest silently stopped
  sudden_start it begins at full volume instead of ramping -- a coverage floor,
               not a beginning
  collapse     recent volume far below the historical norm
  explosion    recent volume far above it
  spike        one period towering over its neighbours
  level_shift  a step change: the mean before a breakpoint differs from after
  gaps         periods inside the span with no rows at all -- silence is itself
               a finding
  seasonal     a strong repeating month-of-year pattern

Reads reports/time_index/series.jsonl, writes series_ranked.csv + FINDINGS.md.
Pure arithmetic -- no warehouse, no model calls.

HONEST LIMIT, stated once and loudly: every one of these measures REPORTING as
much as reality. A collapse can be an agency that stopped publishing; an
explosion can be a backfill. Separating the two needs a denominator per series
and is deliberately parked.
"""
import csv
import json
import os
import statistics as st
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TI = os.path.join(REPO, "reports", "time_index")


def to_year(period):
    return int(str(period)[:4])


def month_of(period):
    p = str(period)
    return int(p[5:7]) if len(p) >= 7 and "-" in p else None


def score(rec):
    pts = rec.get("points") or []
    if len(pts) < 3:
        return None
    counts = [p[1] for p in pts]
    periods = [p[0] for p in pts]
    total = sum(counts)
    if total < 100:
        return None  # too small for the shape to mean anything

    s = {}
    notes = {}

    # pile_up -- one period holds most of the rows
    top = max(counts)
    s["pile_up"] = min(1.0, max(0.0, (top / total - 0.30) / 0.65))
    if s["pile_up"] > 0.25:
        notes["pile_up"] = f"{top/total:.0%} of all rows in {periods[counts.index(top)]}"

    # gaps -- periods inside the span with nothing in them
    first_y, last_y = to_year(periods[0]), to_year(periods[-1])
    span_years = max(1, last_y - first_y + 1)
    if rec["bucket"] == "year":
        expected = span_years
    elif rec["bucket"] == "quarter":
        expected = span_years * 4
    else:
        expected = span_years * 12
    present = len(pts)
    missing = max(0, expected - present)
    s["gaps"] = min(1.0, missing / expected) if expected else 0.0
    if s["gaps"] > 0.2:
        notes["gaps"] = f"{missing} of {expected} periods empty"

    # sudden_stop -- how long ago the series ends, in its own units
    # (compare to 2026 rather than a clock, so the score is reproducible)
    years_silent = 2026 - last_y
    s["sudden_stop"] = min(1.0, max(0.0, (years_silent - 1) / 8.0))
    if s["sudden_stop"] > 0.2:
        notes["sudden_stop"] = f"nothing after {periods[-1]}"

    # tail vs body -- collapse and explosion
    n = len(counts)
    tail_n = max(1, n // 8)
    body = counts[:-tail_n] or counts
    tail = counts[-tail_n:]
    body_med = st.median(body) or 1
    tail_med = st.median(tail)
    ratio = tail_med / body_med if body_med else 1
    s["collapse"] = min(1.0, max(0.0, (1 - ratio - 0.25) / 0.7))
    s["explosion"] = min(1.0, max(0.0, (ratio - 2.0) / 8.0))
    if s["collapse"] > 0.25:
        notes["collapse"] = f"recent periods at {ratio:.0%} of the historical norm"
    if s["explosion"] > 0.25:
        notes["explosion"] = f"recent periods at {ratio:.1f}x the historical norm"

    # sudden_start -- opens at or above its own median instead of ramping
    head_med = st.median(counts[:tail_n])
    overall_med = st.median(counts) or 1
    s["sudden_start"] = min(1.0, max(0.0, (head_med / overall_med - 0.8) / 2.0))
    if s["sudden_start"] > 0.3:
        notes["sudden_start"] = f"opens at {head_med/overall_med:.1f}x its own median"

    # spike -- tallest period vs the median, excluding a pure pile-up
    if overall_med:
        s["spike"] = min(1.0, max(0.0, (top / overall_med - 4) / 30.0))
        if s["spike"] > 0.25:
            notes["spike"] = (f"{periods[counts.index(top)]} is "
                              f"{top/overall_med:.0f}x the median period")
    else:
        s["spike"] = 0.0

    # level_shift -- best split point by difference of means
    best = 0.0
    cut = None
    if n >= 8:
        for i in range(max(2, n // 8), n - max(2, n // 8)):
            a, b = counts[:i], counts[i:]
            ma, mb = st.mean(a), st.mean(b)
            if ma + mb == 0:
                continue
            d = abs(ma - mb) / max(ma, mb)
            if d > best:
                best, cut = d, i
    s["level_shift"] = min(1.0, max(0.0, (best - 0.4) / 0.55))
    if s["level_shift"] > 0.3 and cut:
        notes["level_shift"] = f"step change at {periods[cut]}"

    # seasonal -- month-of-year concentration, monthly series only
    s["seasonal"] = 0.0
    if rec["bucket"] == "month" and n >= 24:
        by_m = {}
        for p, c in pts:
            m = month_of(p)
            if m:
                by_m.setdefault(m, []).append(c)
        if len(by_m) >= 10:
            means = {m: st.mean(v) for m, v in by_m.items()}
            hi, lo = max(means.values()), min(means.values())
            if hi:
                s["seasonal"] = min(1.0, max(0.0, ((hi - lo) / hi - 0.4) / 0.55))
                if s["seasonal"] > 0.3:
                    peak = max(means, key=means.get)
                    notes["seasonal"] = f"peaks in month {peak}, {hi/max(lo,1):.1f}x the quietest"

    # A series is interesting if ANY shape is strong -- not the average, which
    # would drown a single dramatic signal in seven quiet ones.
    top_shapes = sorted(s.items(), key=lambda kv: -kv[1])
    weirdness = top_shapes[0][1] * 0.7 + top_shapes[1][1] * 0.3
    return {
        "weirdness": round(weirdness, 3),
        "scores": {k: round(v, 3) for k, v in s.items()},
        "notes": notes,
        "top_shape": top_shapes[0][0],
        "span": f"{periods[0]} to {periods[-1]}",
        "n_points": n,
        "n_rows": total,
    }


def main():
    recs = []
    with open(os.path.join(TI, "series.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if "error" in r or not r.get("points"):
                continue
            sc = score(r)
            if not sc:
                continue
            recs.append({**r, **sc})
    recs.sort(key=lambda r: -r["weirdness"])

    with open(os.path.join(TI, "series_ranked.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["rank", "weirdness", "top_shape", "table", "column", "clock",
                    "bucket", "span", "n_points", "n_rows", "notes",
                    "pile_up", "sudden_stop", "sudden_start", "collapse",
                    "explosion", "spike", "level_shift", "gaps", "seasonal"])
        for i, r in enumerate(recs, 1):
            sc = r["scores"]
            w.writerow([i, r["weirdness"], r["top_shape"], r["table"], r["column"],
                        r["clock"], r["bucket"], r["span"], r["n_points"],
                        r["n_rows"], "; ".join(f"{k}: {v}" for k, v in r["notes"].items()),
                        sc["pile_up"], sc["sudden_stop"], sc["sudden_start"],
                        sc["collapse"], sc["explosion"], sc["spike"],
                        sc["level_shift"], sc["gaps"], sc["seasonal"]])
    print(f"scored {len(recs)} series -> reports/time_index/series_ranked.csv")
    import collections
    print("top shape distribution:",
          dict(collections.Counter(r["top_shape"] for r in recs).most_common()))

    # A raw weirdness ranking is dominated by tiny scrape tables, where one
    # pile-up period or a sparse span pegs every score at 1.0. That is real but
    # it is bookkeeping, not the world. So: two views. The unweighted ranking
    # stays (it is the honest census), and a size-gated one surfaces the series
    # big enough for a shape to mean something about the subject matter.
    BIG = 100_000
    big = [r for r in recs if r["n_rows"] >= BIG]
    print(f"\nseries with >= {BIG:,} rows: {len(big)}")

    for label, rows in (("WEIRDEST OVERALL", recs[:15]),
                        (f"WEIRDEST AMONG SUBSTANTIAL SERIES (>= {BIG:,} rows)", big[:25])):
        print(f"\n{label}")
        for i, r in enumerate(rows, 1):
            note = "; ".join(f"{v}" for v in r["notes"].values())[:76]
            print(f"{i:3}. {r['weirdness']:.2f} {r['top_shape']:12} "
                  f"{r['n_rows']:>12,}  {r['table'].split('.')[-1][:34]:34} {note}")

    with open(os.path.join(TI, "series_ranked_substantial.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["rank", "weirdness", "top_shape", "table", "column", "clock",
                    "span", "n_rows", "notes"])
        for i, r in enumerate(big, 1):
            w.writerow([i, r["weirdness"], r["top_shape"], r["table"], r["column"],
                        r["clock"], r["span"], r["n_rows"],
                        "; ".join(f"{k}: {v}" for k, v in r["notes"].items())])
    print(f"\nwrote reports/time_index/series_ranked_substantial.csv")


if __name__ == "__main__":
    main()
