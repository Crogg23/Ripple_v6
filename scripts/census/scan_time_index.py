"""Pass 1 of the time index: measure the real clock behind every mart table.

WHY THIS EXISTS
---------------
The 2026-08-17 census fill only measured columns whose Snowflake TYPE was DATE or
TIMESTAMP (see scripts/census/fill_tier_b.py, the `datec` filter). Landing is
all-VARCHAR by design, so almost every real date in this warehouse is a STRING that
staging re-parses. Result: the census measured 349 tables and missed a real clock on
143 more holding ~229M rows, and it mislabelled tables whose only typed column was
Ripple's own ingest timestamp.

This scan fixes that. It measures every time-shaped column regardless of type and
derives, per column, a TRUSTED WINDOW: the floor and ceiling between which the values
are believable, with the sentinel pile-ups counted and excluded rather than deleted.

THE CAST-SAFETY RULE (this script must not commit the bug it is measuring)
-------------------------------------------------------------------------
A bare TRY_TO_DATE() on a small number is read by Snowflake as epoch SECONDS. That is
how a fiscal-year column ('2012') collapsed 20M contract rows onto 1970-01-01, and how
a date-precision code (values 1-5) mangled 386k conflict records. A bare TO_TIMESTAMP()
on a microsecond epoch produces the year 56,000,000, which is how Ripple's own
INGESTED_AT column poisoned the offshore-leaks family's measured date range.

So this script NEVER parses blind. Every parse is guarded by a regex that first proves
the value has the shape of the format being applied. A value that does not match any
known shape is counted as unparseable, not silently turned into 1970.

Read-only. Aggregate-only. One query per table. Checkpointed per table so it can be
killed and resumed. Writes reports/time_index/scan.jsonl.

Usage:
    python scripts/census/scan_time_index.py                    # all mart tables
    python scripts/census/scan_time_index.py --limit 20         # smoke test
    python scripts/census/scan_time_index.py --tables f.txt     # SCHEMA.TABLE per line
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _snowflake_conn import connect  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTDIR = os.path.join(REPO, "reports", "time_index")
OUT = os.path.join(OUTDIR, "scan.jsonl")
CKPT = os.path.join(OUTDIR, "scan_done.json")
CANDIDATES = os.path.join(REPO, "reports", "_time_candidates_marts.json")

# Column-name shapes that can carry a clock. Deliberately wide: a column that turns out
# not to be a date is a FINDING (that is the bug class), so we would rather measure it
# and rule it out than never look.
TIME_NAME = re.compile(
    r"(^|_)(year|yr|date|dt|period|quarter|qtr|month|mo|week|day|cycle|fy|time|"
    r"timestamp|asof|as_of|since|until|start|end|begin|expir\w*|effective|filed|"
    r"received|posted|issued|approved|created|updated|modified|closed|opened|term|"
    r"vintage|age|duration|days|elapsed)($|_)",
    re.I,
)
TIME_ANY = re.compile(
    r"year|date|_dt$|^dt_|quarter|qtr|month|week|timestamp|period|cycle|vintage|"
    r"asof|as_of|_ts$",
    re.I,
)
DATE_TYPES = ("DATE", "TIMESTAMP_NTZ", "TIMESTAMP_LTZ", "TIMESTAMP_TZ")

MAX_COLS_PER_TABLE = 12  # keep the generated SQL sane on very wide tables

# A believable window for anything in the public record this warehouse holds. Values
# outside it are counted, never silently dropped -- the counts ARE the finding.
FLOOR_YEAR = 1700
CEIL_YEAR = 2035

# One field layout for every column, typed or not, so the result rows line up.
FIELDS = [
    "nonnull", "distinct", "raw_min", "raw_max", "trusted_min", "trusted_max",
    "trusted_n", "n_1970_01_01", "n_1900_01_01", "n_year_9000_plus",
    "n_before_floor", "n_after_ceiling", "n_jan_first",
    "shape_iso", "shape_us", "shape_yyyymmdd", "shape_year_only",
    "shape_yyyymm", "shape_year_quarter", "shape_dd_mon_yyyy",
    "year_min", "year_max",
]


def time_like(col, dtype):
    if dtype in DATE_TYPES:
        return True
    return bool(TIME_NAME.search(col) or TIME_ANY.search(col))


def col_exprs(col, dtype):
    """Aggregates for one candidate column.

    Returns (list_of_sql_exprs, list_of_field_names) in matching order. Every parse is
    shape-guarded -- see the cast-safety rule in the module docstring.
    """
    q = f'"{col}"'
    v = f"trim(to_varchar({q}))"  # one text view of the value, whatever the type

    if dtype in DATE_TYPES:
        # Already typed. Measure it directly, but still bound the trusted window and
        # count the sentinel pile-ups rather than assuming the range is honest.
        trusted = f"iff(year({q}) between {FLOOR_YEAR} and {CEIL_YEAR}, {q}, null)"
        exprs = [
            f"count({q})",
            f"approx_count_distinct({q})",
            f"to_varchar(min({q}))",
            f"to_varchar(max({q}))",
            f"to_varchar(min({trusted}))",
            f"to_varchar(max({trusted}))",
            f"count({trusted})",
            f"count_if({q} = '1970-01-01'::date)",
            f"count_if({q} = '1900-01-01'::date)",
            f"count_if(year({q}) >= 9000)",
            f"count_if(year({q}) < {FLOOR_YEAR})",
            f"count_if(year({q}) > {CEIL_YEAR} and year({q}) < 9000)",
            f"count_if(year({q}) between {FLOOR_YEAR} and {CEIL_YEAR} "
            f"and month({q})=1 and day({q})=1)",
            "null", "null", "null", "null", "null", "null", "null",
            f"min(year({trusted}))",
            f"max(year({trusted}))",
        ]
        names = FIELDS
        return exprs, names

    # Untyped (TEXT or NUMBER). Probe the SHAPE first, then parse only what matches.
    iso = rf"regexp_like({v}, '^[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}.*')"
    us = rf"regexp_like({v}, '^[0-9]{{1,2}}/[0-9]{{1,2}}/[0-9]{{4}}$')"
    ymd = rf"regexp_like({v}, '^[0-9]{{8}}$')"
    # DD-MON-YYYY, e.g. '15-APR-2011'. Real and common here: the IRS revocation file
    # and the offshore-leaks family both ship it. The first pass missed this shape and
    # scored 22,512 perfectly good dates as unparseable, so it is first-class now.
    dmon = rf"regexp_like({v}, '^[0-9]{{1,2}}-[A-Za-z]{{3}}-[0-9]{{4}}$')"
    yr = rf"regexp_like({v}, '^[0-9]{{4}}$')"
    ym = rf"regexp_like({v}, '^[0-9]{{4}}-?[0-9]{{2}}$')"
    yq = rf"regexp_like({v}, '^[0-9]{{4}}[ -]?[Qq]?[1-4]$')"

    # Guarded parses. Each one is wrapped so the format is only applied to values that
    # already proved they have that shape, and the result is bounded to the trusted
    # window. Nothing can fall through to an epoch reading.
    p_iso = f"iff({iso}, try_to_date(left({v},10), 'YYYY-MM-DD'), null)"
    p_us = f"iff({us}, try_to_date({v}, 'MM/DD/YYYY'), null)"
    p_ymd = (f"iff({ymd} and left({v},4) between '{FLOOR_YEAR}' and '{CEIL_YEAR}', "
             f"try_to_date({v}, 'YYYYMMDD'), null)")
    p_dmon = f"iff({dmon}, try_to_date(upper({v}), 'DD-MON-YYYY'), null)"
    parsed = f"coalesce({p_iso}, {p_us}, {p_ymd}, {p_dmon})"
    trusted = f"iff(year({parsed}) between {FLOOR_YEAR} and {CEIL_YEAR}, {parsed}, null)"
    # Year-bearing values never go through a date parser -- that is the exact bug this
    # whole pass exists to stop. Pull the year out arithmetically instead, so a
    # year-only or year-quarter column still lands on the timeline at its true grain.
    yr_num = (f"try_to_number(iff({yr} or {ym} or {yq}, left({v},4), null))")
    yr_num = (f"iff({yr_num} between {FLOOR_YEAR} and {CEIL_YEAR}, {yr_num}, null)")

    exprs = [
        f"count({q})",
        f"approx_count_distinct({q})",
        f"min({v})",
        f"max({v})",
        f"to_varchar(min({trusted}))",
        f"to_varchar(max({trusted}))",
        f"count({trusted})",
        f"count_if({parsed} = '1970-01-01'::date)",
        f"count_if({parsed} = '1900-01-01'::date)",
        f"count_if(year({parsed}) >= 9000)",
        f"count_if({parsed} is not null and year({parsed}) < {FLOOR_YEAR})",
        f"count_if(year({parsed}) > {CEIL_YEAR} and year({parsed}) < 9000)",
        f"count_if({trusted} is not null and month({trusted})=1 and day({trusted})=1)",
        f"count_if({iso})",
        f"count_if({us})",
        f"count_if({ymd})",
        f"count_if({yr})",
        f"count_if({ym})",
        f"count_if({yq})",
        f"count_if({dmon})",
        f"min({yr_num})",
        f"max({yr_num})",
    ]
    return exprs, FIELDS


def target_tables(conn, limit=None, tables_file=None):
    if tables_file:
        keys = [t.strip() for t in open(tables_file, encoding="utf-8") if t.strip()]
    else:
        cur = conn.cursor()
        cur.execute(
            "select table_schema, table_name, row_count "
            "from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES "
            "where table_schema <> 'INFORMATION_SCHEMA' "
            "order by coalesce(row_count, 0) asc"  # smallest first: fail fast, cheap
        )
        keys = [f"{r[0]}.{r[1]}" for r in cur.fetchall()]
    return keys[:limit] if limit else keys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--tables", default=None, help="file of SCHEMA.TABLE, one per line")
    args = ap.parse_args()

    os.makedirs(OUTDIR, exist_ok=True)
    done = set(json.load(open(CKPT))) if os.path.exists(CKPT) else set()

    conn = connect(database="LIBRARY_MARTS")
    cur = conn.cursor()
    keys = target_tables(conn, args.limit, args.tables)
    out = open(OUT, "a", encoding="utf-8")
    print(f"{len(keys)} tables targeted, {len(done)} already scanned", flush=True)

    scanned = skipped = failed = 0
    for key in keys:
        if key in done:
            continue
        sch, tab = key.split(".", 1)
        cur.execute(
            "select column_name, data_type from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS "
            "where table_schema=%s and table_name=%s order by ordinal_position",
            (sch, tab),
        )
        cols = cur.fetchall()
        cands = [(c, t) for c, t in cols if time_like(c, t)][:MAX_COLS_PER_TABLE]
        if not cands:
            out.write(json.dumps({"table": key, "n_time_columns": 0,
                                  "verdict": "NO_CLOCK"}) + "\n")
            out.flush()
            done.add(key)
            json.dump(sorted(done), open(CKPT, "w"))
            skipped += 1
            continue

        exprs = ["count(*)"]
        layout = []
        for c, t in cands:
            e, n = col_exprs(c, t)
            layout.append((c, t, n))
            exprs.extend(e)
        sql = f'select {", ".join(exprs)} from LIBRARY_MARTS."{sch}"."{tab}"'

        print(f"scan {key} ({len(cands)} time cols)", flush=True)
        try:
            cur.execute(sql)
            vals = list(cur.fetchone())
        except Exception as e:
            out.write(json.dumps({"table": key, "error": str(e)[:400],
                                  "n_time_columns": len(cands)}) + "\n")
            out.flush()
            done.add(key)
            json.dump(sorted(done), open(CKPT, "w"))
            failed += 1
            continue

        rec = {"table": key, "n_rows": vals[0], "n_time_columns": len(cands), "columns": {}}
        p = 1
        for c, t, names in layout:
            rec["columns"][c] = {"data_type": t}
            for nm in names:
                val = vals[p]
                rec["columns"][c][nm] = str(val)[:120] if isinstance(val, str) else val
                p += 1
        out.write(json.dumps(rec, default=str) + "\n")
        out.flush()
        done.add(key)
        json.dump(sorted(done), open(CKPT, "w"))
        scanned += 1

    print(f"TIME INDEX SCAN DONE  scanned={scanned} no_clock={skipped} failed={failed}",
          flush=True)


if __name__ == "__main__":
    main()
