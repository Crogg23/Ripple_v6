#!/usr/bin/env python3
"""What years does each table actually hold, and do two tables share any?

WHY THIS EXISTS
Two of the six dead 2026-09-05 politics probes died on time windows that never
overlapped. Hunch 91: trades end 2020-12, bills start 2023-01. Hunch 83: lobby
filings stop 2021, the CMS rules start 2023-01. Both were discovered the
expensive way, by writing the join, running it, and getting zero rows back.
SOURCE_REGISTRY.TEMPORAL_COVERAGE is hand-typed at register time and nothing
re-measures it, so it is a claim, not a fact.

WHY A YEAR HISTOGRAM AND NOT MIN/MAX
Min and max cannot see a hole in the middle. The lobby table runs 1999-2021 on
paper while 2011-2019 is missing outright, so a min/max answer there is right
only by luck. One row per year per table, with its count, makes the hole
visible and makes overlap mean "years where BOTH sides actually have rows".

NOT EVERY TABLE IS MAPPED
freshness_mapping.json covers 102 sources; the politics probe tables are not
among them. Name any table directly with --table plus --col, and it is stored
under that fully qualified name as its own source id.

WHERE THE REUSED COLUMN IS THE WRONG ONE
The freshness ledger asks "how recent is this table" and the answer is one
column's MAX. Coverage asks "what years does it hold". Those are the same
column on an event table and different columns on a snapshot table. EPA ECHO
maps to FAC_DATE_LAST_INSPECTION, a per-facility attribute, so its histogram is
a picture of inspection dates and 82% of its rows carry none. Every scan reports
its unparsed share for exactly this reason; a high share means read the span as
a statement about the parsed rows, not about the table.

WHAT IT REUSES
The date parsing is build_freshness_ledger's, not a second copy. Landing stores
most dates as TEXT, and that parser already handles every shape they throw plus
the epoch trap, where a bare '2023' silently reads as 1970. Sources and their
recency columns come from scripts/freshness_mapping.json, the same 102 the
freshness ledger measures. Load stamps are ineligible there and stay ineligible
here, so a table loaded yesterday can never read as covering one day.

USAGE
    coverage_probe.py measure --all              # dry run, prints the SQL
    coverage_probe.py measure fed_x --run        # scan and print, store nothing
    coverage_probe.py measure --all --write      # scans and records
    coverage_probe.py measure fed_x fed_y --write
    coverage_probe.py measure --table DB.SCH.T --col FILED --kind mixed --write
    coverage_probe.py overlap fed_x fed_y        # the check that was missing
    coverage_probe.py show fed_x                 # one table's years and holes

`--write` scans every measured table once. That is a warehouse write and real
compute on the big ones, so it gets a price line first, per CLAUDE.md.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
sys.path.insert(0, str(_LIB))
sys.path.insert(0, str(_REPO / "scripts"))
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

import snow  # noqa: E402
from build_freshness_ledger import MAPPING, recency_inner  # noqa: E402

COVERAGE_TABLE = "LIBRARY_META.REGISTRY.SOURCE_COVERAGE_YEARS"

# Anything outside this is a parse artifact, not coverage. CA_LOBBY_COVER holds
# dates spanning year 4 to 5005; FEC indiv carries strays out to 3312. Left in,
# a single bad row makes a table appear to overlap everything. The floor is not
# 1789: SlaveVoyages starts 1550 and OWID CO2 reaches back to 1750.
YEAR_FLOOR = 1500


def year_ceiling() -> int:
    return _dt.date.today().year + 2


CREATE_SQL = f"""
CREATE TABLE IF NOT EXISTS {COVERAGE_TABLE} (
    SOURCE_ID    VARCHAR,
    LANDING_FQN  VARCHAR,
    RECENCY_COL  VARCHAR,
    DATA_YEAR    NUMBER,
    N_ROWS       NUMBER,
    N_YEARS      NUMBER,     -- years this run expected to write; short means partial
    N_UNPARSED   NUMBER,     -- rows whose date did not parse, or fell outside the window
    N_TOTAL      NUMBER,     -- rows in the table when measured
    MEASURED_AT  TIMESTAMP_NTZ
)
"""

# Newest run per source. Every reader goes through this, so re-measuring a
# source after a backfill never has to remove the old rows.
LATEST_CTE = f"""
WITH runs AS (
    SELECT SOURCE_ID, MAX(MEASURED_AT) AS AT
    FROM {COVERAGE_TABLE} GROUP BY SOURCE_ID
),
latest AS (
    SELECT c.* FROM {COVERAGE_TABLE} c
    JOIN runs r ON r.SOURCE_ID = c.SOURCE_ID AND r.AT = c.MEASURED_AT
)
"""


def load_mapping() -> dict[str, dict]:
    return {m["source_id"]: m for m in json.loads(MAPPING.read_text())}


def fqn_of(m: dict) -> str:
    return m.get("landing_fqn") or f"LIBRARY_RAW.LANDING.{m['source_id'].upper()}"


def years_sql(m: dict) -> str | None:
    """One scan. Row count per data year, artifacts already dropped."""
    col = m.get("recency_col")
    if not col:
        return None
    inner = recency_inner(col, m.get("recency_kind", "mixed"))
    if inner is None:
        return None
    y = f"YEAR({inner})"
    keep = f"{y} BETWEEN {YEAR_FLOOR} AND {year_ceiling()}"
    # The excluded count rides along. Without it a table whose dates mostly fail
    # to parse still prints "no gaps" and gives no way to know.
    return (
        f"SELECT IFF({keep}, {y}, NULL) AS DATA_YEAR, COUNT(*) AS N_ROWS\n"
        f"FROM {fqn_of(m)}\n"
        f"GROUP BY 1 ORDER BY 1 NULLS LAST"
    )


# A year holding this small a share of the table is a stray, not coverage.
# CA_LOBBY_COVER has 17 rows out of 568,988 scattered from 1927 to 1999, which
# would otherwise claim 73 years and overlap anything pre-2000.
STRAY_SHARE = 0.001


def dense_years(years: dict[int, int]) -> dict[int, int]:
    """Drop stray years from the two ends. Interior years are never touched.

    A hole in the middle is the finding; a lone row at the edge is noise. So
    trimming works inward from each end and stops at the first real year.
    """
    if not years:
        return {}
    total = sum(years.values())
    floor = total * STRAY_SHARE
    ordered = sorted(years)
    lo, hi = 0, len(ordered) - 1
    while lo < hi and years[ordered[lo]] < floor:
        lo += 1
    while hi > lo and years[ordered[hi]] < floor:
        hi -= 1
    return {y: years[y] for y in ordered[lo:hi + 1]}


def _span(years: dict[int, int]) -> str:
    if not years:
        return "not measured"
    dense = dense_years(years)
    lo, hi = min(dense), max(dense)
    holes = sorted(set(range(lo, hi + 1)) - set(dense))
    out = f"{lo}-{hi}" + (f", missing {len(holes)}" if holes else "")
    strays = len(years) - len(dense)
    return out + (f", {strays} stray year(s) trimmed" if strays else "")


def measure_one(conn, m: dict, run: bool) -> list[tuple]:
    sid = m["source_id"]
    sql = years_sql(m)
    if sql is None:
        print(f"  {sid}: no usable date column, skipped")
        return []
    if not run:
        print(f"\n-- {sid}\n{sql}\n")
        return []

    cur = conn.cursor()
    try:
        cur.execute(sql)
        found = cur.fetchall()
    except Exception as exc:
        print(f"  {sid}: SCAN ERROR {str(exc)[:110]}")
        return []
    finally:
        cur.close()

    dropped = sum(int(n) for y, n in found if y is None)
    found = [(y, n) for y, n in found if y is not None]
    total = dropped + sum(int(n) for _, n in found)
    if not found:
        print(f"  {sid}: no parseable dates in {total:,} rows, coverage unknown")
        return []

    now = _dt.datetime.now(_dt.timezone.utc).replace(tzinfo=None)
    years = [int(y) for y, _ in found]
    rows = [(sid, fqn_of(m), m.get("recency_col"), int(y), int(n), len(years),
             dropped, total, now) for y, n in found]
    hist = {int(y): int(n) for y, n in found}
    share = f", {100 * dropped / total:.2f}% unparsed" if dropped else ""
    print(f"  {sid}: {_span(hist)}, {len(dense_years(hist))} year(s){share}")
    return rows


def verify(conn, mapping: dict, wanted: list[str]) -> int:
    """Does each source's SQL actually compile against the live table?

    A mapping entry can name a column that is not there, or one whose real name
    has a space, and neither shows up until the scan runs. LIMIT 0 finds those
    for nothing.
    """
    bad = []
    cur = conn.cursor()
    for sid in wanted:
        sql = years_sql(mapping[sid])
        if sql is None:
            bad.append((sid, "no usable date column in the mapping"))
            continue
        try:
            cur.execute(sql.replace(" ORDER BY 1 NULLS LAST", "") + " LIMIT 0")
            cur.fetchall()
        except Exception as exc:
            bad.append((sid, str(exc).split("\n")[0][:90]))
    cur.close()
    ok = len(wanted) - len(bad)
    print(f"{ok} of {len(wanted)} compile against the live table\n")
    for sid, why in bad:
        print(f"  {sid:44} {why}")
    return 1 if bad else 0


def save(conn, rows: list[tuple]) -> None:
    if not rows:
        return
    cur = conn.cursor()
    try:
        cur.executemany(
            f"INSERT INTO {COVERAGE_TABLE} "
            "(SOURCE_ID, LANDING_FQN, RECENCY_COL, DATA_YEAR, N_ROWS, N_YEARS, "
            "N_UNPARSED, N_TOTAL, MEASURED_AT) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", rows)
    finally:
        cur.close()


def read_years(conn, sid: str) -> dict[int, int]:
    """Years the newest run recorded for one source, and rows in each."""
    cur = conn.cursor()
    try:
        cur.execute(LATEST_CTE + "SELECT DATA_YEAR, N_ROWS, N_YEARS, N_UNPARSED, N_TOTAL "
                                 "FROM latest WHERE SOURCE_ID = %s", (sid,))
        found = cur.fetchall()
    except Exception:
        return {}   # nothing measured yet, or the table is not there
    finally:
        cur.close()
    if found and len(found) != int(found[0][2]):
        print(f"  warning: {sid} stored {len(found)} of {found[0][2]} years; "
              "that run was cut short. Re-measure it.")
    if found and found[0][4] and found[0][3] / found[0][4] > 0.25:
        share = 100 * found[0][3] / found[0][4]
        print(f"  warning: {sid} had {share:.0f}% of rows fail to parse. "
              "Its span describes the rows that did, not the table.")
    return {int(y): int(n) for y, n, _, _, _ in found}


def show(conn, sid: str) -> int:
    years = read_years(conn, sid)
    if not years:
        print(f"{sid}: not measured yet. Run `measure {sid} --write` first.")
        return 2
    print(f"{sid}  {_span(years)}\n")
    dense = dense_years(years)
    for y in range(min(years), max(years) + 1):
        n = years.get(y, 0)
        if y not in dense and n:
            mark = "   <- stray, below the coverage floor"
        elif n == 0:
            mark = "   <- empty"
        else:
            mark = ""
        print(f"  {y}  {n:>12,}{mark}")
    return 0


def shared_spans(ya: dict[int, int], yb: dict[int, int]) -> tuple[list[int], str]:
    """Years where BOTH sides actually have rows, collapsed into runs.

    Set intersection, not a min/max compare, so a hole on either side removes
    that year instead of hiding inside a span.
    """
    shared = sorted(set(ya) & set(yb))
    if not shared:
        return [], ""
    runs, start = [], shared[0]
    for prev, nxt in zip(shared, shared[1:] + [None]):
        if nxt != prev + 1:
            runs.append((start, prev))
            start = nxt
    return shared, ", ".join(f"{a}-{b}" if a != b else str(a) for a, b in runs)


def overlap(conn, a: str, b: str) -> int:
    ya, yb = read_years(conn, a), read_years(conn, b)
    for sid, y in ((a, ya), (b, yb)):
        if not y:
            print(f"{sid}: not measured yet. Run `measure {sid} --write` first.")
            return 2
    print(f"{a}  {_span(ya)}")
    print(f"{b}  {_span(yb)}")
    shared, spans = shared_spans(dense_years(ya), dense_years(yb))
    if not shared:
        print("\nNO OVERLAP. A join across these returns zero rows.")
        return 1
    thin = min(min(ya[y], yb[y]) for y in shared)
    print(f"\nshared years {spans}, {len(shared)} of them")
    print(f"thinnest shared year holds {thin:,} rows on the smaller side")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("measure", help="scan sources, record rows per data year")
    m.add_argument("sources", nargs="*", help="source_id, one or more")
    m.add_argument("--all", action="store_true", help="every mapped source")
    m.add_argument("--table", help="an unmapped table, DATABASE.SCHEMA.TABLE")
    m.add_argument("--col", help="its date column, required with --table")
    m.add_argument("--kind", default="mixed",
                   choices=["date", "timestamp", "yyyymmdd_text",
                            "year_text", "year_int", "mixed"],
                   help="how that column stores its date")
    m.add_argument("--verify", action="store_true",
                   help="compile-check each source with LIMIT 0. Scans nothing.")
    m.add_argument("--run", action="store_true",
                   help="scan and print the years. Stores nothing.")
    m.add_argument("--write", action="store_true",
                   help="scan and record. Implies --run.")

    o = sub.add_parser("overlap", help="years two sources share")
    o.add_argument("source_a")
    o.add_argument("source_b")

    s = sub.add_parser("show", help="one source's years, holes marked")
    s.add_argument("source_id")

    args = ap.parse_args(argv)
    mapping = load_mapping()

    if args.cmd == "measure":
        if args.table:
            if not args.col:
                ap.error("--table needs --col")
            fqn = args.table.upper()
            parts = fqn.split(".")
            if len(parts) != 3 or not all(
                    re.fullmatch(r"[A-Z_][A-Z0-9_$]*", x) for x in parts):
                ap.error(f"--table needs DATABASE.SCHEMA.TABLE, got {args.table!r}")
            mapping[fqn] = {"source_id": fqn, "landing_fqn": fqn,
                            "recency_col": args.col, "recency_kind": args.kind}
            wanted = [fqn]
        elif args.all:
            wanted = list(mapping)
        else:
            wanted = args.sources
        if not wanted:
            ap.error("name a source_id, or pass --all, or use --table with --col")
        missing = [s for s in wanted if s not in mapping]
        if missing:
            ap.error(f"not in the mapping: {', '.join(missing)}")
        args.run = args.run or args.write
        if not args.run:
            print(f"dry run over {len(wanted)} source(s). --run scans, --write records.\n")

    conn = snow.connect()
    try:
        if args.cmd == "measure":
            if args.verify:
                return verify(conn, mapping, wanted)
            if args.write:
                # Always, and before any scanning. A scan is real money; never
                # pay for one and then lose it to a missing destination.
                snow.execute(conn, CREATE_SQL)
                # Additive only, and safe to repeat: an older table predates
                # the unparsed counters.
                for col in ("N_UNPARSED NUMBER", "N_TOTAL NUMBER"):
                    snow.execute(conn, f"ALTER TABLE {COVERAGE_TABLE} "
                                       f"ADD COLUMN IF NOT EXISTS {col}")
            failed = []
            for sid in wanted:
                rows = measure_one(conn, mapping[sid], args.run)
                if args.run and not rows:
                    failed.append(sid)
                    if args.write and read_years(conn, sid):
                        # An earlier run stored a span for this source. Saying
                        # nothing would leave that stale answer standing as
                        # current, which is how a failed re-measure passes for
                        # an unchanged one.
                        print(f"    NOTE: {sid} has an older stored span that "
                              "this run could not refresh. Treat it as stale.")
                if args.write:
                    save(conn, rows)   # per source, so source 90 of 102 keeps 89
            if failed:
                print(f"\n{len(failed)} of {len(wanted)} produced nothing: "
                      f"{', '.join(failed[:8])}{' ...' if len(failed) > 8 else ''}")
                return 1
            return 0
        if args.cmd == "show":
            return show(conn, args.source_id)
        return overlap(conn, args.source_a, args.source_b)
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
