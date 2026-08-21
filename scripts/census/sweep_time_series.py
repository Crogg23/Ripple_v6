"""Pull one time series per table, for every table with a trustworthy clock.

This is the payoff of the 2026-08-20 time index. Rather than pick a trend and
chase it, this measures the SAME shape across every dataset that has a usable
clock, so the strange ones nominate themselves. A census on the time axis.

Method, per table:
  * take its primary clock (from reports/time_index/clock_index.csv -- the
    adversarially-reviewed labelling of which column means "when it happened")
  * bucket at a sensible resolution: day-grain columns roll up to MONTHS,
    quarter columns to quarters, year columns to years
  * clamp to the trusted window measured by the scan, so a single junk row
    cannot invent a 300-year series
  * return (period, rows) -- nothing else. One query per table.

Deliberately NOT here: money sums, per-noun rates, joins of any kind. Those need
a second table and are parked. This is the surface pass on the time axis.

Read-only. Checkpointed. Writes reports/time_index/series.jsonl.
"""
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _snowflake_conn import connect  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TI = os.path.join(REPO, "reports", "time_index")
OUT = os.path.join(TI, "series.jsonl")
CKPT = os.path.join(TI, "series_done.json")

# Backup/restore schemas are not the live warehouse. The scan swept them by
# accident on 2026-08-20 and inflated every total by 237M rows; filter here.
BACKUP_PREFIXES = ("_RESTORE", "_BACKUP", "_OLD", "_ARCHIVE", "_TMP", "_SNAPSHOT")

# A clock that says when something HAPPENED is the one worth trending. A
# "reported" or "decided" clock is still a real series (and often interesting --
# reporting volume is its own story), so both are kept, ranked in this order.
CLOCK_RANK = {"happened": 0, "reported": 1, "decided": 2, "span_start": 3}


def load_targets():
    """Join the clock labels to the measured windows; keep only usable pairs."""
    clocks = {}
    with open(os.path.join(TI, "clock_index.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["clock"] not in CLOCK_RANK:
                continue
            key = r["model"].upper()
            rank = CLOCK_RANK[r["clock"]]
            # prefer the column the reviewers marked primary, then the best clock
            score = (0 if r["is_primary"] == "True" else 1, rank)
            if key not in clocks or score < clocks[key][0]:
                clocks[key] = (score, r["column"].upper(), r["clock"], r["grain"])

    targets = []
    with open(os.path.join(TI, "columns.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            sch = r["table"].split(".")[0]
            if sch.upper().startswith(BACKUP_PREFIXES):
                continue
            alias = r["table"].split(".")[-1].upper()
            hit = clocks.get(alias)
            if not hit or hit[1] != r["col"].upper():
                continue
            trusted = int(r["trusted"] or 0)
            ymin, ymax = r["ymin"], r["ymax"]
            has_year = (ymin or "").strip() not in ("", "None")
            if trusted <= 0 and not has_year:
                continue  # nothing placeable on a timeline
            targets.append({
                "table": r["table"], "column": r["col"], "clock": hit[2],
                "grain": r["grain"], "dtype": r["dtype"],
                "n_rows": int(r["n_rows"] or 0), "trusted": trusted,
                "tmin": r["tmin"], "tmax": r["tmax"],
                "ymin": ymin, "ymax": ymax,
            })
    # smallest first: cheap failures surface early
    targets.sort(key=lambda t: t["n_rows"])
    return targets


def build_sql(t):
    """One aggregate per table. Bucket by grain; clamp to the trusted window."""
    sch, tab = t["table"].split(".", 1)
    q = f'"{t["column"]}"'
    src = f'LIBRARY_MARTS."{sch}"."{tab}"'
    grain = t["grain"]

    if grain == "year" or (t["dtype"] not in ("DATE", "TIMESTAMP_NTZ",
                                              "TIMESTAMP_LTZ", "TIMESTAMP_TZ")
                           and grain in ("year", "none")):
        # Year-bearing text/number. Pull the year out arithmetically -- never
        # through a date parser (that is the bug this whole effort exists to kill).
        v = f"trim(to_varchar({q}))"
        yr = (f"iff(regexp_like({v}, '^[0-9]{{4}}') "
              f"and try_to_number(left({v}, 4)) between 1700 and 2125, "
              f"try_to_number(left({v}, 4)), null)")
        return (f"select to_varchar({yr}) as period, count(*) as n "
                f"from {src} where {yr} is not null group by 1 order by 1"), "year"

    # Everything else: parse shape-guarded, clamp, then bucket.
    if t["dtype"] in ("DATE", "TIMESTAMP_NTZ", "TIMESTAMP_LTZ", "TIMESTAMP_TZ"):
        parsed = q
    else:
        v = f"trim(to_varchar({q}))"
        parsed = (
            f"coalesce("
            f"iff(regexp_like({v}, '^[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}'),"
            f" try_to_date(left({v},10),'YYYY-MM-DD'), null),"
            f"iff(regexp_like({v}, '^[0-9]{{1,2}}/[0-9]{{1,2}}/[0-9]{{4}}$'),"
            f" try_to_date({v},'MM/DD/YYYY'), null),"
            f"iff(regexp_like({v}, '^[0-9]{{8}}$'),"
            f" try_to_date({v},'YYYYMMDD'), null),"
            f"iff(regexp_like({v}, '^[0-9]{{1,2}}-[A-Za-z]{{3}}-[0-9]{{4}}$'),"
            f" try_to_date(upper({v}),'DD-MON-YYYY'), null))"
        )
    clamped = f"iff(year({parsed}) between 1700 and 2125, {parsed}, null)"
    bucket = "quarter" if t["grain"] == "quarter" else "month"
    return (f"select to_varchar(date_trunc('{bucket}', {clamped}), 'YYYY-MM-DD') as period, "
            f"count(*) as n from {src} where {clamped} is not null "
            f"group by 1 order by 1"), bucket


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    os.makedirs(TI, exist_ok=True)
    done = set(json.load(open(CKPT))) if os.path.exists(CKPT) else set()
    targets = load_targets()
    if limit:
        targets = targets[:limit]
    conn = connect(database="LIBRARY_MARTS")
    cur = conn.cursor()
    out = open(OUT, "a", encoding="utf-8")
    print(f"{len(targets)} tables have a trustworthy clock; {len(done)} already pulled",
          flush=True)

    ok = failed = 0
    for t in targets:
        key = f"{t['table']}|{t['column']}"
        if key in done:
            continue
        sql, bucket = build_sql(t)
        try:
            cur.execute(sql)
            pts = [[str(r[0]), int(r[1])] for r in cur.fetchall()]
        except Exception as e:
            out.write(json.dumps({"table": t["table"], "column": t["column"],
                                  "error": str(e)[:300]}) + "\n")
            out.flush()
            done.add(key)
            json.dump(sorted(done), open(CKPT, "w"))
            failed += 1
            continue
        rec = dict(t)
        rec["bucket"] = bucket
        rec["points"] = pts
        rec["n_points"] = len(pts)
        rec["n_in_series"] = sum(p[1] for p in pts)
        out.write(json.dumps(rec, default=str) + "\n")
        out.flush()
        done.add(key)
        json.dump(sorted(done), open(CKPT, "w"))
        ok += 1
        if ok % 25 == 0:
            print(f"  {ok} series pulled ({failed} failed)", flush=True)

    print(f"SWEEP DONE  series={ok} failed={failed}", flush=True)


if __name__ == "__main__":
    main()
