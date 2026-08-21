"""Score the four widened time shapes and rank them by how strange they are.

Companion to score_time_series.py, which scored the count-per-period sweep. That
one measured whether the VOLUME moved. These four measure things volume cannot
show:

  lag       how long between happening and being told, and whether that is drifting
  spans     how many were live at once, how long they last, how many never closed
  mix       whether the make-up changed, not just the amount
  cohorts   entities arriving and leaving, and how long they stay

THE TWO CENSORING TRAPS, HANDLED HERE ONCE AND LOUDLY
-----------------------------------------------------
These shapes have a failure mode the count sweep did not, and it produces
confident nonsense if ignored:

  LEFT censoring  -- in the FIRST year of any dataset, every entity is new. A
                     naive birth curve therefore always opens with a giant spike
                     that means nothing. The first year is excluded from every
                     birth statistic and reported separately.
  RIGHT censoring -- in the LAST year, every entity still present looks like it
                     just died, and every span still running looks like it just
                     ended. The last year is excluded from every death statistic.

Neither exclusion deletes data: the raw sweep files keep every period. The
excluded values are carried on the output rows so the choice stays auditable.

THE TRAP THAT ALMOST SHIPPED (worth its own heading)
----------------------------------------------------
The first version of this scorer ranked "the reporting gap collapsed" at the top
of nearly every table, and "things last shorter now" at the top of nearly every
span table. Both were artifacts, and both are the SAME artifact.

An event from 1950 can be reported at any distance up to the present, so old
cohorts can show enormous gaps. An event from last month cannot possibly show a
ten-year gap yet -- there has not been ten years. So a raw median lag ALWAYS
falls over time, in every dataset, whether or not anything changed. Identically,
a span that started long ago has had time to run long; one that started recently
is cut off at today, so raw durations ALWAYS shrink.

The fix is a FIXED HORIZON, which is comparable across cohorts. Instead of "how
long was the gap," ask "what share were reported within one year of happening" --
and only ask it of cohorts old enough for the answer to be knowable. Same for
spans: "what share had closed within a year of starting." Raw medians are still
reported, because they are useful description, but nothing is RANKED on them.

Pure arithmetic. No warehouse, no model calls. Reads the four *.jsonl files in
reports/time_index/ and writes ranked CSVs plus WIDENED_FINDINGS.md.
"""
import csv
import json
import os
import statistics as st

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TI = os.path.join(REPO, "reports", "time_index")

MIN_ROWS = 1000        # below this a shape is noise, not a finding
WINDOW = 3             # years compared at each end when measuring drift


def read(name):
    path = os.path.join(TI, name)
    if not os.path.exists(path):
        return []
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def ratio_score(a, b):
    """0-1 strangeness for 'b differs from a by a lot', symmetric in direction."""
    if not a or not b or a <= 0 or b <= 0:
        return 0.0
    r = max(a, b) / min(a, b)
    return min(1.0, (r - 1.5) / 8.5) if r > 1.5 else 0.0


def head_tail(values, k=WINDOW):
    """First k and last k entries of a period-ordered list, non-overlapping."""
    if len(values) < 2:
        return [], []
    k = min(k, len(values) // 2)
    k = max(1, k)
    return values[:k], values[-k:]


def wmedian(pairs):
    """Median of values weighted by count, from [(value, weight), ...]."""
    pairs = [(v, w) for v, w in pairs if v is not None and w > 0]
    if not pairs:
        return None
    pairs.sort()
    total = sum(w for _, w in pairs)
    seen = 0
    for v, w in pairs:
        seen += w
        if seen >= total / 2:
            return v
    return pairs[-1][0]


# ---------------------------------------------------------------- reporting lag

def score_lag(rows):
    out = []
    for r in rows:
        if r.get("error") or not r.get("points"):
            continue
        pts = [p for p in r["points"] if str(p["period"]).isdigit()]
        pts.sort(key=lambda p: int(p["period"]))
        n = sum(p["n"] for p in pts)
        if n < MIN_ROWS or len(pts) < 3:
            continue
        neg = sum(p["negative"] for p in pts)
        unrep = sum(p["unreported"] for p in pts)
        slow = sum(p["slow"] for p in pts)
        measured = n - unrep

        # Drift: compare the typical lag early against the typical lag late,
        # weighting each year by how many rows it carries.
        early, late = head_tail(pts)
        e_lag = wmedian([(p["p50"], p["n"]) for p in early])
        l_lag = wmedian([(p["p50"], p["n"]) for p in late])
        overall = wmedian([(p["p50"], p["n"]) for p in pts])

        neg_share = neg / measured if measured else 0.0
        unrep_share = unrep / n if n else 0.0
        slow_share = slow / measured if measured else 0.0

        notes = []
        # A mostly-negative gap does not mean impossible data. It means the two
        # clocks are labelled in the wrong order -- a finding about the index.
        reversed_clocks = neg_share > 0.8
        if reversed_clocks:
            notes.append("clocks appear reversed: '{}' almost always precedes '{}'"
                         .format(r["down_col"], r["happened_col"]))
        elif neg_share > 0.02:
            notes.append("{:.1%} reported BEFORE they happened -- impossible, "
                         "so one clock is mislabelled or misparsed".format(neg_share))
        if unrep_share > 0.5:
            notes.append("{:.0%} never got a reported date at all".format(unrep_share))

        # THE COMPARABLE MEASURE: share reported within one year of happening.
        # A cohort is only comparable once its SLOW TAIL has had time to arrive.
        # Two years is not enough when the downstream event routinely takes a
        # decade. The retraction table is the case that forced this: it contains
        # only papers that were eventually retracted, so a 2025 cohort can only
        # show the fast retractions -- the slow ones have not happened yet -- and
        # a naive read says retractions got dramatically faster. Wait out the
        # 90th-percentile gap before comparing.
        p90 = wmedian([(p["p90"], p["n"]) for p in pts if p["p90"] is not None])
        p90_years = 0.0
        if p90 is not None:
            p90_years = abs(p90) / 365.0 if r.get("unit") == "days" else abs(p90)
        buffer_years = int(min(10, max(2, round(p90_years + 0.5))))
        last_y = int(pts[-1]["period"])
        eligible = [p for p in pts
                    if int(p["period"]) <= last_y - buffer_years
                    and (p["n"] - p["unreported"]) >= 50]
        # A table holding ONLY completed cases cannot show the incomplete ones,
        # so its recent cohorts are a survivor set however wide the buffer.
        completed_only = unrep_share < 0.05
        prompt_rate = None
        rate_shift = 0.0
        e_rate = l_rate = None
        if len(eligible) >= 4 and not reversed_clocks:
            def rate(ps):
                m = sum(p["n"] - p["unreported"] for p in ps)
                s = sum(p["slow"] for p in ps)
                return None if m <= 0 else 1.0 - s / m
            e_grp, l_grp = head_tail(eligible)
            e_rate, l_rate = rate(e_grp), rate(l_grp)
            prompt_rate = rate(eligible)
            if e_rate is not None and l_rate is not None:
                rate_shift = abs(l_rate - e_rate)
                if rate_shift > 0.15:
                    word = "rose" if l_rate > e_rate else "fell"
                    notes.append("share reported within a year {} from {:.0%} to {:.0%} "
                                 "(cohorts up to {}, waiting out a {}-year tail)"
                                 .format(word, e_rate, l_rate, last_y - buffer_years,
                                         buffer_years))
                if completed_only:
                    notes.append("CAUTION: every row here already has its downstream "
                                 "date, so the table holds only finished cases -- the "
                                 "recent cohorts are a survivor set")

        # Raw medians are description, never a ranking input -- see the docstring.
        big_early_lag = e_lag is not None and abs(e_lag) > (1825 if r.get("unit") == "days" else 5)
        backfilled = big_early_lag and l_lag is not None and abs(l_lag) < abs(e_lag) / 4
        if backfilled:
            notes.append("assembled retroactively: the earliest records were entered "
                         "~{:.0f} {} after the fact, recent ones ~{:.0f} -- that is the "
                         "archive being built, not reporting speeding up"
                         .format(abs(e_lag), r.get("unit", "days"), abs(l_lag)))
        if slow_share > 0.25 and not reversed_clocks:
            notes.append("{:.0%} took more than a year to appear".format(slow_share))

        # Rank on the censoring-safe measure and on outright data faults. A
        # backfilled archive is informative but well understood, so it scores
        # modestly rather than crowding out real shifts.
        # A retroactive archive EXPLAINS its own prompt-rate shift, so the shift
        # stops being evidence of anything and must not crowd the ranking.
        strangeness = max(0.0 if backfilled else rate_shift,
                          min(1.0, neg_share * 1.25) if not reversed_clocks else 0.35,
                          unrep_share * 0.6,
                          0.30 if backfilled else 0.0)
        out.append({
            "table": r["table"], "happened_col": r["happened_col"],
            "downstream_role": r["down_role"], "downstream_col": r["down_col"],
            "unit": r.get("unit"), "n_rows": n, "n_periods": len(pts),
            "median_lag": overall, "early_lag": e_lag, "late_lag": l_lag,
            "pct_reported_within_year": None if prompt_rate is None else round(prompt_rate, 4),
            "early_prompt_rate": None if e_rate is None else round(e_rate, 4),
            "late_prompt_rate": None if l_rate is None else round(l_rate, 4),
            "prompt_rate_shift": round(rate_shift, 3),
            "tail_buffer_years": buffer_years,
            "completed_cases_only": completed_only,
            "pct_negative": round(neg_share, 4),
            "pct_unreported": round(unrep_share, 4),
            "pct_slow": round(slow_share, 4),
            "clocks_reversed": reversed_clocks,
            "retroactive_archive": backfilled,
            "n_cohorts_comparable": len(eligible),
            "strangeness": round(strangeness, 3),
            "notes": "; ".join(notes),
        })
    out.sort(key=lambda x: -x["strangeness"])
    return out


# ----------------------------------------------------------------------- spans

def score_spans(rows):
    out = []
    for r in rows:
        if r.get("error") or not r.get("cells"):
            continue
        cells = [c for c in r["cells"] if c[0] is not None]
        n = sum(c[2] for c in cells)
        if n < MIN_ROWS:
            continue
        years = [c[0] for c in cells] + [c[1] for c in cells if c[1] is not None]
        if not years:
            continue
        y0, y1 = min(years), max(years)
        if y1 - y0 > 200:                       # a junk tail, not a real span
            y1 = min(y1, y0 + 200)

        # The stock curve: how many were live in each year. Rows with no end are
        # treated as still running, which is what "no end recorded" claims.
        active = {}
        for ys, ye, cnt, _ in cells:
            end = y1 if ye is None else min(ye, y1)
            if end < ys:
                continue                         # backwards; counted separately
            for y in range(max(ys, y0), end + 1):
                active[y] = active.get(y, 0) + cnt
        curve = [(y, active[y]) for y in sorted(active)]

        n_open = r.get("n_open", 0)
        n_back = r.get("n_backwards", 0)
        open_share = n_open / n if n else 0.0
        back_share = n_back / n if n else 0.0

        # Duration drift, weighted by how many rows each start-year holds.
        by_start = {}
        for ys, ye, cnt, p50 in cells:
            if p50 is None:
                continue
            by_start.setdefault(ys, []).append((p50, cnt))
        starts = sorted(by_start)
        e_years, l_years = head_tail(starts)
        e_dur = wmedian([p for y in e_years for p in by_start[y]])
        l_dur = wmedian([p for y in l_years for p in by_start[y]])
        overall_dur = wmedian([p for y in starts for p in by_start[y]])

        # A single duration dominating means a template, not a lifetime.
        dur_counts = {}
        for ys, ye, cnt, p50 in cells:
            if p50 is not None:
                dur_counts[p50] = dur_counts.get(p50, 0) + cnt
        dur_total = sum(dur_counts.values())
        modal_share = (max(dur_counts.values()) / dur_total) if dur_total else 0.0
        modal_dur = max(dur_counts, key=dur_counts.get) if dur_counts else None

        # THE COMPARABLE MEASURE, for the same reason as reporting lag: raw
        # durations always shrink toward the present, because a span that began
        # last month cannot have run ten years yet. So ask instead what SHARE of
        # each start-year cohort had closed within a year -- and ask it only of
        # cohorts that have had a year.
        tot_by_start, closed_by_start = {}, {}
        for ys, ye, cnt, _ in cells:
            tot_by_start[ys] = tot_by_start.get(ys, 0) + cnt
            if ye is not None and ys <= ye <= ys + 1:
                closed_by_start[ys] = closed_by_start.get(ys, 0) + cnt
        eligible = [y for y in sorted(tot_by_start)
                    if y <= y1 - 2 and tot_by_start[y] >= 50]
        closure_shift = 0.0
        e_close = l_close = overall_close = None
        if len(eligible) >= 4:
            def closed_rate(ys_list):
                t = sum(tot_by_start[y] for y in ys_list)
                c = sum(closed_by_start.get(y, 0) for y in ys_list)
                return None if t <= 0 else c / t
            e_grp, l_grp = head_tail(eligible)
            e_close, l_close = closed_rate(e_grp), closed_rate(l_grp)
            overall_close = closed_rate(eligible)
            if e_close is not None and l_close is not None:
                closure_shift = abs(l_close - e_close)

        notes = []
        if back_share > 0.001:
            notes.append("{:.2%} end before they start -- impossible".format(back_share))
        if open_share > 0.3:
            notes.append("{:.0%} have no end recorded".format(open_share))
        if closure_shift > 0.15:
            word = "rose" if l_close > e_close else "fell"
            notes.append("share closing within a year {} from {:.0%} to {:.0%}"
                         .format(word, e_close, l_close))
        # Raw duration is kept as description only -- never ranked on.
        drift = ratio_score(abs(e_dur or 0) + 1, abs(l_dur or 0) + 1)
        if modal_share > 0.5 and modal_dur:
            notes.append("{:.0%} share one exact duration ({:.0f} {}) -- a standard "
                         "term, not a measured lifetime"
                         .format(modal_share, modal_dur, r.get("unit", "days")))

        # Stock shape: how many were live at once. Only trustworthy when most
        # rows actually have an end -- otherwise the curve only ever rises,
        # because nothing is ever allowed to leave it.
        # The first years of ANY span dataset understate the live population,
        # because spans that began before the window simply are not in the file.
        # The curve therefore always ramps in from near zero. Skip that ramp
        # rather than reporting it as growth.
        stock_drift = 0.0
        stock_trustworthy = open_share <= 0.3
        ramp = max(1, len(curve) // 5)
        cmp_curve = [c[1] for c in curve[ramp:]]
        if len(cmp_curve) >= 4:
            ec, lc = head_tail(cmp_curve)
            stock_drift = ratio_score(st.mean(ec), st.mean(lc))
            # A curve that starts at a handful and ends in the hundreds of
            # thousands is the window opening, not growth. Judge it relative to
            # where it ends, not against a fixed floor.
            ramping_in = st.mean(ec) < max(10.0, 0.02 * st.mean(lc))
            if ramping_in:
                stock_drift = 0.0
                notes.append("the live-at-once curve climbs from almost nothing -- "
                             "that is the window opening, not a population growing")
            elif stock_drift > 0.2 and stock_trustworthy:
                word = "grew" if st.mean(lc) > st.mean(ec) else "shrank"
                notes.append("how many were live at once {} from {:,.0f} to {:,.0f}"
                             .format(word, st.mean(ec), st.mean(lc)))
            elif stock_drift > 0.2:
                stock_drift = 0.0
                notes.append("the live-at-once curve only rises, because {:.0%} of "
                             "rows never close -- not a real population trend"
                             .format(open_share))
        peak = max(curve, key=lambda c: c[1]) if curve else (None, 0)

        strangeness = max(closure_shift,
                          stock_drift if stock_trustworthy else 0.0,
                          min(1.0, back_share * 20),
                          max(0.0, (open_share - 0.3) / 0.7) * 0.5)
        out.append({
            "table": r["table"], "start_col": r["start_col"], "end_col": r["end_col"],
            "unit": r.get("unit"), "n_rows": n,
            "first_year": y0, "last_year": y1,
            "median_duration": overall_dur,
            "early_duration": e_dur, "late_duration": l_dur,
            "pct_closed_within_year": None if overall_close is None else round(overall_close, 4),
            "early_closure_rate": None if e_close is None else round(e_close, 4),
            "late_closure_rate": None if l_close is None else round(l_close, 4),
            "closure_shift": round(closure_shift, 3),
            "n_cohorts_comparable": len(eligible),
            "pct_open": round(open_share, 4), "pct_backwards": round(back_share, 5),
            "modal_duration": modal_dur, "modal_share": round(modal_share, 3),
            "peak_live_year": peak[0], "peak_live": peak[1],
            "stock_curve_trustworthy": stock_trustworthy,
            "raw_duration_drift_descriptive_only": round(drift, 3),
            "stock_drift": round(stock_drift, 3),
            "strangeness": round(strangeness, 3),
            "notes": "; ".join(notes),
            "_curve": curve,
        })
    out.sort(key=lambda x: -x["strangeness"])
    return out


# ------------------------------------------------------------------ category mix

# Provenance columns are not categories. They record where a row came from, so
# "the most common source file changed" is a restatement of the load history.
PROVENANCE = ("SOURCE_FILE", "SOURCE_URL", "_URL", "_FILE", "FILENAME", "FILE_NAME",
              "SOURCE_TABLE", "DATA_SOURCE_FILE")


def score_mix(rows):
    out = []
    for r in rows:
        if r.get("error"):
            continue
        for ser in r.get("series") or []:
            if any(p in ser["col"] for p in PROVENANCE):
                continue
            cells = [c for c in ser["cells"] if c[0] is not None]
            n = sum(c[2] for c in cells)
            if n < MIN_ROWS:
                continue
            by_year = {}
            for y, val, cnt in cells:
                key = "(blank)" if val is None else str(val)
                slot = by_year.setdefault(y, {})
                slot[key] = slot.get(key, 0) + cnt
            # Years too thin to carry a share are excluded from the comparison
            # windows but still counted in the totals.
            solid = [y for y in sorted(by_year) if sum(by_year[y].values()) >= 50]
            if len(solid) < 4:
                continue
            e_years, l_years = head_tail(solid)
            e_rows = sum(sum(by_year[y].values()) for y in e_years)
            l_rows = sum(sum(by_year[y].values()) for y in l_years)

            def shares(years):
                agg = {}
                for y in years:
                    for k, v in by_year[y].items():
                        agg[k] = agg.get(k, 0) + v
                tot = sum(agg.values())
                return {k: v / tot for k, v in agg.items()} if tot else {}

            early, late = shares(e_years), shares(l_years)
            keys = set(early) | set(late)
            # Total variation distance: 0 = identical make-up, 1 = no overlap.
            tvd = 0.5 * sum(abs(late.get(k, 0) - early.get(k, 0)) for k in keys)

            # A column that was simply EMPTY in the older records produces a
            # perfect 1.00 flip that means only "this field was added later".
            # Measure the shift again among the values that actually exist, and
            # rank on that instead.
            def drop_blanks(d):
                kept = {k: v for k, v in d.items() if k.strip() not in ("", "(blank)")}
                tot = sum(kept.values())
                return {k: v / tot for k, v in kept.items()} if tot else {}

            e_real, l_real = drop_blanks(early), drop_blanks(late)
            real_keys = set(e_real) | set(l_real)
            tvd_real = (0.5 * sum(abs(l_real.get(k, 0) - e_real.get(k, 0))
                                  for k in real_keys)) if e_real and l_real else 0.0
            early_blank = sum(v for k, v in early.items()
                              if k.strip() in ("", "(blank)"))
            late_blank = sum(v for k, v in late.items() if k.strip() in ("", "(blank)"))
            field_arrived = early_blank > 0.5 and late_blank < 0.2
            appeared = sorted([k for k in keys
                               if early.get(k, 0) < 0.005 and late.get(k, 0) > 0.05],
                              key=lambda k: -late.get(k, 0))
            vanished = sorted([k for k in keys
                               if early.get(k, 0) > 0.05 and late.get(k, 0) < 0.005],
                              key=lambda k: -early.get(k, 0))
            top_e = max(early, key=early.get) if early else None
            top_l = max(late, key=late.get) if late else None

            # A lifecycle status column usually reads as of TODAY, not as of the
            # year on the row. "Older ones are closed, newer ones are open" is
            # then a tautology, not a change. Flagged, not dropped -- some status
            # columns are genuine point-in-time records.
            snapshot_risk = any(w in ser["col"] for w in ("STATUS", "CURRENT", "ACTIVE"))

            # Survivorship: when each row is a durable THING dated by when it came
            # into existence, and the table is today's register of them, the early
            # years show only what is still standing. The 1900s of a power-plant
            # register look overwhelmingly hydro partly because hydro dams last a
            # century and the coal units beside them were retired and removed.
            birth_clock = ("OPERATING", "ESTABLISH", "INCORPORAT", "COMMISSION",
                           "BUILT", "FOUNDED", "OPENED", "CONSTRUCT", "CHARTER",
                           "REGISTERED", "CREATED", "INSTALL")
            survivorship_risk = (r.get("clock") in ("happened", "span_start")
                                 and any(w in (r.get("clock_col") or "")
                                         for w in birth_clock))

            top_er = max(e_real, key=e_real.get) if e_real else None
            top_lr = max(l_real, key=l_real.get) if l_real else None
            # A 100%-to-100% flip built on forty rows is arithmetic, not evidence.
            # Damp rather than drop, so thin tables stay visible but stay down.
            thin = min(1.0, min(e_rows, l_rows) / 200.0)

            notes = []
            if field_arrived:
                notes.append("the field was blank in {:.0%} of the early records -- it "
                             "was added later, so the headline flip is the column "
                             "arriving".format(early_blank))
            if top_er != top_lr and top_er and top_lr:
                notes.append("among values that exist, the most common flipped from "
                             "'{}' ({:.0%}) to '{}' ({:.0%})"
                             .format(top_er, e_real.get(top_er, 0),
                                     top_lr, l_real.get(top_lr, 0)))
            if snapshot_risk:
                notes.append("CAUTION: a status column normally reads as of today, "
                             "not as of the row's year")
            if survivorship_risk:
                notes.append("CAUTION: rows are dated by when the thing came into "
                             "existence, so the early years show only what SURVIVED "
                             "to be in today's register")
            if thin < 1.0:
                notes.append("thin at one end ({:,} rows early, {:,} late) -- ranked "
                             "down accordingly".format(e_rows, l_rows))
            if appeared:
                notes.append("appeared mid-series: {}".format(", ".join(
                    "'{}' now {:.0%}".format(k, late[k]) for k in appeared[:3])))
            if vanished:
                notes.append("vanished: {}".format(", ".join(
                    "'{}' was {:.0%}".format(k, early[k]) for k in vanished[:3])))

            out.append({
                "table": r["table"], "column": ser["col"], "clock": r.get("clock"),
                "n_rows": n, "n_values": len(keys), "n_years": len(solid),
                "first_year": solid[0], "last_year": solid[-1],
                "mix_shift": round(tvd_real, 3),
                "mix_shift_with_blanks": round(tvd, 3),
                "field_arrived_midway": field_arrived,
                "snapshot_risk": snapshot_risk,
                "survivorship_risk": survivorship_risk,
                "pct_blank_early": round(early_blank, 3),
                "pct_blank_late": round(late_blank, 3),
                "top_early": top_er, "top_early_share": round(e_real.get(top_er, 0), 3) if top_er else None,
                "top_late": top_lr, "top_late_share": round(l_real.get(top_lr, 0), 3) if top_lr else None,
                "dominance_flipped": bool(top_er and top_lr and top_er != top_lr),
                "n_appeared": len(appeared), "n_vanished": len(vanished),
                "appeared": "|".join(appeared[:5]), "vanished": "|".join(vanished[:5]),
                "window_rows_early": e_rows, "window_rows_late": l_rows,
                "strangeness": round(tvd_real * thin, 3),
                "notes": "; ".join(notes),
            })
    out.sort(key=lambda x: -x["strangeness"])
    return out


# --------------------------------------------------------------- entity cohorts

def score_cohorts(rows):
    out = []
    for r in rows:
        if r.get("error") or r.get("skipped") or not r.get("curves"):
            continue
        born = {y: n for y, n, _ in r["curves"].get("born", [])}
        died = {y: n for y, n, _ in r["curves"].get("died", [])}
        life = {y: n for y, n, _ in r["curves"].get("lifespan", [])}
        total_entities = sum(born.values())
        n_rows = r.get("n_rows_live") or r.get("n_rows") or 0
        if total_entities < 50 or n_rows < MIN_ROWS:
            continue
        years = sorted(set(born) | set(died))
        if len(years) < 4:
            continue
        y0, y1 = years[0], years[-1]

        # Censoring, handled explicitly (see the module docstring).
        first_year_births = born.get(y0, 0)
        last_year_deaths = died.get(y1, 0)
        real_births = [(y, born.get(y, 0)) for y in years if y != y0]
        real_deaths = [(y, died.get(y, 0)) for y in years if y != y1]

        living, churn = {}, []
        alive = 0
        for y in years:
            alive += born.get(y, 0)
            living[y] = alive
            if y not in (y0, y1) and alive > 0:
                churn.append((y, (born.get(y, 0) + died.get(y, 0)) / alive))
            alive -= died.get(y, 0)

        # When the clock IS the thing's own birth date, "first seen" and "last
        # seen" are the same row by construction, so births/deaths restate the
        # count sweep and every entity looks like a one-year wonder. Flag it.
        BIRTH_CLOCK = ("OPERATING", "ESTABLISH", "INCORPORAT", "COMMISSION", "BUILT",
                       "FOUNDED", "OPENED", "CONSTRUCT", "CHARTER", "REGISTERED",
                       "CREATED", "INSTALL", "ENROLL", "APPROVAL", "ISSUE")
        birth_clock_tautology = any(w in (r.get("clock_col") or "") for w in BIRTH_CLOCK)

        one_and_done = life.get(0, 0) / total_entities if total_entities else 0.0
        median_life = wmedian(list(life.items()))
        rows_per_entity = n_rows / total_entities if total_entities else 0

        notes = []
        b_vals = [n for _, n in real_births]
        d_vals = [n for _, n in real_deaths]
        birth_drift = death_drift = 0.0
        if len(b_vals) >= 4:
            eb, lb = head_tail(b_vals)
            birth_drift = ratio_score(st.mean(eb), st.mean(lb))
            if birth_drift > 0.2:
                word = "more" if st.mean(lb) > st.mean(eb) else "fewer"
                notes.append("{} new arrivals lately: {:,.0f}/yr -> {:,.0f}/yr"
                             .format(word, st.mean(eb), st.mean(lb)))
        if len(d_vals) >= 4:
            ed, ld = head_tail(d_vals)
            death_drift = ratio_score(st.mean(ed), st.mean(ld))
            if death_drift > 0.2:
                word = "more" if st.mean(ld) > st.mean(ed) else "fewer"
                notes.append("{} last-sightings lately: {:,.0f}/yr -> {:,.0f}/yr"
                             .format(word, st.mean(ed), st.mean(ld)))
        if one_and_done > 0.7:
            notes.append("{:.0%} of entities appear in ONE year only -- either real "
                         "churn or an identifier that is not stable across years"
                         .format(one_and_done))
        if first_year_births / total_entities > 0.5:
            notes.append("{:.0%} of all entities are 'born' in the first year -- "
                         "that is the data starting, not the world"
                         .format(first_year_births / total_entities))

        if birth_clock_tautology:
            notes.append("the clock is the thing's own start date, so 'first seen' "
                         "and 'last seen' are the same row -- this is the count "
                         "sweep restated, not a population turning over")
        strangeness = max(birth_drift, death_drift,
                          max(0.0, (one_and_done - 0.7) / 0.3) * 0.6)
        if birth_clock_tautology:
            strangeness *= 0.25
        out.append({
            "table": r["table"], "entity_col": r.get("chosen"),
            "clock": r.get("clock"), "clock_col": r.get("clock_col"),
            "n_rows": n_rows, "n_entities": total_entities,
            "rows_per_entity": round(rows_per_entity, 2),
            "first_year": y0, "last_year": y1,
            "median_lifespan_years": median_life,
            "pct_single_year": round(one_and_done, 3),
            "birth_clock_tautology": birth_clock_tautology,
            "births_excluded_first_year": first_year_births,
            "deaths_excluded_last_year": last_year_deaths,
            "birth_drift": round(birth_drift, 3), "death_drift": round(death_drift, 3),
            "peak_living_year": max(living, key=living.get) if living else None,
            "peak_living": max(living.values()) if living else 0,
            "strangeness": round(strangeness, 3),
            "notes": "; ".join(notes),
        })
    out.sort(key=lambda x: -x["strangeness"])
    return out


# ------------------------------------------------------------------------ output

def write_csv(name, rows):
    if not rows:
        return 0
    cols = [c for c in rows[0] if not c.startswith("_")]
    path = os.path.join(TI, name)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def coverage(rows, label):
    """Never report a sweep without saying what it could NOT measure."""
    err = sum(1 for r in rows if r.get("error"))
    skip = sum(1 for r in rows if r.get("skipped") or r.get("note"))
    return {"shape": label, "pulled": len(rows), "errors": err, "no_signal": skip}


DATESTAMP = "2026-08-20"


def _table(rows, cols, headers):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        cells = []
        for c in cols:
            v = r.get(c)
            if isinstance(v, float):
                v = round(v, 3)
            cells.append(str(v if v not in (None, "") else "-").replace("|", "/"))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def write_findings(lag, spans, mix, coh, cov):
    """Emit the receipts as one readable file. Interpretation goes on top by hand."""
    L = ["# The widened time census - " + DATESTAMP, "",
         "The count sweep asked one question of every clocked table: how many rows",
         "per period. These four ask what counting cannot answer.", "",
         "| shape | tables pulled | scored | errors |", "|---|---:|---:|---:|"]
    for c, scored in zip(cov, [len(lag), len(spans), len(mix), len(coh)]):
        L.append("| {} | {} | {} | {} |".format(c["shape"], c["pulled"], scored,
                                                c["errors"]))
    L += ["", "## How the two censoring traps were handled", "",
          "Raw lag and raw duration ALWAYS appear to shrink toward the present, in",
          "every dataset, whether or not anything changed: an old record has had",
          "years in which to be reported or to run long, and a recent one has not.",
          "Nothing here is ranked on a raw median. Everything is ranked on a fixed",
          "horizon -- share reported within a year, share closed within a year --",
          "asked only of cohorts old enough to answer it. Birth curves drop their",
          "first year and death curves drop their last, for the same reason.", ""]

    L += ["## 1. Reporting lag -- the gap between happening and being told", ""]
    impossible = [r for r in lag if r["pct_negative"] > 0.02 and not r["clocks_reversed"]]
    L += ["**{} tables have the downstream clock landing BEFORE the event clock.**"
          .format(len(impossible)),
          "Being told about something before it happens is impossible, so each of",
          "these is one of two things: a parse fault, or -- more often -- two columns",
          "that are not a report-of-an-event pair at all. The aircraft registry",
          "compares year-of-manufacture against last-registry-action; the water",
          "enforcement tables compare last-inspection against last-formal-action.",
          "Neither is a reporting gap. Either way the clock labels need revisiting,",
          "which is a finding about the index rather than about the world.", "",
          _table(sorted(impossible, key=lambda r: -r["pct_negative"])[:15],
                 ["table", "happened_col", "downstream_col", "n_rows", "pct_negative"],
                 ["table", "happened clock", "downstream clock", "rows",
                  "share impossible"]), ""]
    silent = [r for r in lag if r["pct_unreported"] > 0.5]
    L += ["**{} tables leave the downstream clock empty for most rows** -- the field"
          .format(len(silent)),
          "exists but is blank, so the gap is unmeasurable there.", "",
          _table(sorted(silent, key=lambda r: -r["pct_unreported"])[:10],
                 ["table", "downstream_col", "n_rows", "pct_unreported"],
                 ["table", "downstream clock", "rows", "share never reported"]), ""]
    retro = [r for r in lag if r["retroactive_archive"]]
    L += ["**{} tables are retroactive archives** -- the oldest records were entered"
          .format(len(retro)),
          "long after the fact, so their early years describe when someone typed the",
          "history in, not when anything happened.", "",
          _table(sorted(retro, key=lambda r: -r["n_rows"])[:10],
                 ["table", "n_rows", "early_lag", "late_lag", "unit"],
                 ["table", "rows", "earliest gap", "recent gap", "unit"]), ""]
    real_lag = [r for r in lag if not r["retroactive_archive"]
                and not r["clocks_reversed"] and r["prompt_rate_shift"] > 0.15
                and r["pct_negative"] < 0.02 and not r["completed_cases_only"]]
    L += ["**{} tables show a real change in how promptly things get reported**,"
          .format(len(real_lag)),
          "measured like-for-like. This is the collection signal the count sweep",
          "could never separate out.", "",
          _table(sorted(real_lag, key=lambda r: -r["prompt_rate_shift"])[:15],
                 ["table", "n_rows", "early_prompt_rate", "late_prompt_rate",
                  "n_cohorts_comparable", "tail_buffer_years"],
                 ["table", "rows", "reported within a year (early)", "(recent)",
                  "years compared", "tail waited out"]), ""]

    L += ["## 2. Spans -- what was live at once, and for how long", ""]
    backwards = [r for r in spans if r["pct_backwards"] > 0.0005]
    L += ["**{} tables contain spans that END BEFORE THEY START.**".format(len(backwards)),
          "", _table(sorted(backwards, key=lambda r: -r["pct_backwards"])[:10],
                     ["table", "start_col", "end_col", "n_rows", "pct_backwards"],
                     ["table", "start", "end", "rows", "share backwards"]), ""]
    template = [r for r in spans if r["modal_share"] > 0.5]
    L += ["**{} tables are dominated by ONE exact duration** -- a standard term (a"
          .format(len(template)),
          "30-day window, a 3-year permit), not a measured lifetime. An average",
          "length computed on these measures the form, not the world.", "",
          _table(sorted(template, key=lambda r: -r["modal_share"])[:12],
                 ["table", "n_rows", "modal_duration", "unit", "modal_share"],
                 ["table", "rows", "the one duration", "unit", "share on it"]), ""]
    never_close = [r for r in spans if r["pct_open"] > 0.3]
    L += ["**{} tables never record an end for most rows.** Their live-at-once curve"
          .format(len(never_close)),
          "can only ever rise, so it is not a population trend.", "",
          _table(sorted(never_close, key=lambda r: -r["pct_open"])[:10],
                 ["table", "end_col", "n_rows", "pct_open"],
                 ["table", "end clock", "rows", "share with no end"]), ""]
    stock = [r for r in spans if r["stock_curve_trustworthy"] and r["stock_drift"] > 0.2]
    L += ["**{} tables have a trustworthy live-at-once curve that MOVED.**".format(len(stock)),
          "", _table(sorted(stock, key=lambda r: -r["stock_drift"])[:12],
                     ["table", "n_rows", "peak_live_year", "peak_live", "notes"],
                     ["table", "rows", "peak year", "peak live", "what moved"]), ""]

    L += ["## 3. Category mix -- the make-up changing, not the amount", ""]
    clean = [r for r in mix if not r["field_arrived_midway"] and not r["snapshot_risk"]
             and not r["survivorship_risk"]
             and r["window_rows_early"] >= 200 and r["window_rows_late"] >= 200]
    L += ["**{} table/column pairs measured; {} shift on solid ground** (the field"
          .format(len(mix), len(clean)),
          "existed throughout, it is not a lifecycle status that reads as of today,",
          "and both ends carry real volume).", "",
          _table(sorted(clean, key=lambda r: -r["strangeness"])[:25],
                 ["table", "column", "n_rows", "top_early", "top_early_share",
                  "top_late", "top_late_share", "mix_shift"],
                 ["table", "column", "rows", "was mostly", "share", "now mostly",
                  "share", "shift"]), ""]
    arrived = [r for r in mix if r["field_arrived_midway"]]
    L += ["**{} pairs are a field ARRIVING, not a mix changing** -- blank in the early"
          .format(len(arrived)),
          "records because the column did not exist yet. Named so nobody mistakes",
          "them for findings later.", "",
          _table(sorted(arrived, key=lambda r: -r["n_rows"])[:12],
                 ["table", "column", "n_rows", "pct_blank_early", "pct_blank_late"],
                 ["table", "column", "rows", "blank early", "blank now"]), ""]
    surv = [r for r in mix if r["survivorship_risk"] and r["strangeness"] > 0.5]
    L += ["**{} pairs are dated by when the thing came into existence.** Their early"
          .format(len(surv)),
          "years are a survivor list, not a census of what was built then.", "",
          _table(sorted(surv, key=lambda r: -r["strangeness"])[:10],
                 ["table", "column", "n_rows", "top_early", "top_late"],
                 ["table", "column", "rows", "was mostly", "now mostly"]), ""]
    snap = [r for r in mix if r["snapshot_risk"] and r["strangeness"] > 0.5]
    L += ["**{} pairs are lifecycle status columns that flipped.** Treat with"
          .format(len(snap)),
          "suspicion: a status normally reads as of today, so 'old ones are closed",
          "and new ones are open' is a tautology rather than a change.", "",
          _table(sorted(snap, key=lambda r: -r["strangeness"])[:10],
                 ["table", "column", "n_rows", "top_early", "top_late"],
                 ["table", "column", "rows", "was mostly", "now mostly"]), ""]

    L += ["## 4. Entity cohorts -- things arriving and leaving", ""]
    unstable = [r for r in coh if r["pct_single_year"] > 0.7
                and not r["birth_clock_tautology"]]
    L += ["**{} tables have entities appearing in one year only**, for more than 70%"
          .format(len(unstable)),
          "of the population. Either the churn is real or the identifier is not",
          "stable across years -- and from inside one table those look identical.", "",
          _table(sorted(unstable, key=lambda r: -r["n_rows"])[:12],
                 ["table", "entity_col", "n_rows", "n_entities", "pct_single_year"],
                 ["table", "entity column", "rows", "entities", "one-year-only"]), ""]
    churny = [r for r in coh if r["pct_single_year"] <= 0.7
              and not r["birth_clock_tautology"]
              and max(r["birth_drift"], r["death_drift"]) > 0.2]
    L += ["**{} tables show a real change in arrivals or departures.**".format(len(churny)),
          "", _table(sorted(churny, key=lambda r: -r["strangeness"])[:20],
                     ["table", "entity_col", "n_entities", "median_lifespan_years",
                      "peak_living_year", "peak_living", "notes"],
                     ["table", "entity column", "entities", "median years alive",
                      "peak year", "peak population", "what moved"]), ""]
    stable = [r for r in coh if r["pct_single_year"] <= 0.5
              and not r["birth_clock_tautology"] and r["rows_per_entity"] >= 2]
    L += ["**{} tables carry a population that persists across years** -- these are the"
          .format(len(stable)),
          "ones where 'events per living entity' is computable inside a single table,",
          "with no second source needed.", "",
          _table(sorted(stable, key=lambda r: -r["n_entities"])[:20],
                 ["table", "entity_col", "n_rows", "n_entities", "rows_per_entity",
                  "median_lifespan_years"],
                 ["table", "entity column", "rows", "entities", "rows each",
                  "median years alive"]), ""]

    L += ["## What these four sweeps still cannot do", "",
          "1. **No cross-table comparison.** Every measurement uses one table and its",
          "   own columns. Nothing is joined to anything.",
          "2. **A category is whatever the publisher called it.** A mix flip can be a",
          "   coding change with nothing underneath, and that is not visible from",
          "   inside the column.",
          "3. **Last seen is not dead; no end recorded is not still running.** Both are",
          "   reported as measured, with the censoring stated.",
          "4. **Strangeness is not importance.** A small registry with a clean flip",
          "   outranks a huge table that changed slowly. Row counts are on every line",
          "   so it can be re-sorted by hand.", "",
          "## Files", "", "| file | what it holds |", "|---|---|",
          "| `lag.jsonl` / `lag_ranked.csv` | per-year reporting gap, every table with two clocks |",
          "| `spans.jsonl` / `spans_ranked.csv` | start-year x end-year grid and the ranked read of it |",
          "| `mix.jsonl` / `mix_ranked.csv` | year x category counts and the ranked shifts |",
          "| `cohorts.jsonl` / `cohorts_ranked.csv` | births, deaths and lifespans per table |"]

    path = os.path.join(TI, "WIDENED_FINDINGS.md")
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
    return path


def main():
    lag_raw, span_raw = read("lag.jsonl"), read("spans.jsonl")
    mix_raw, coh_raw = read("mix.jsonl"), read("cohorts.jsonl")

    lag, spans = score_lag(lag_raw), score_spans(span_raw)
    mix, coh = score_mix(mix_raw), score_cohorts(coh_raw)

    counts = {
        "lag": write_csv("lag_ranked.csv", lag),
        "spans": write_csv("spans_ranked.csv", spans),
        "mix": write_csv("mix_ranked.csv", mix),
        "cohorts": write_csv("cohorts_ranked.csv", coh),
    }
    cov = [coverage(lag_raw, "reporting lag"), coverage(span_raw, "spans"),
           coverage(mix_raw, "category mix"), coverage(coh_raw, "entity cohorts")]

    print("SCORED")
    for c in cov:
        print("  {:<15} pulled={:<5} errors={:<4} no-signal={}"
              .format(c["shape"], c["pulled"], c["errors"], c["no_signal"]))
    for k, v in counts.items():
        print("  {:<15} ranked={}".format(k, v))
    json.dump({"counts": counts, "coverage": cov},
              open(os.path.join(TI, "widened_summary.json"), "w"), indent=2)
    print("  wrote " + write_findings(lag, spans, mix, coh, cov))


if __name__ == "__main__":
    main()
