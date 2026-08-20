"""Shape 7 of the time census: the MIX shifting, not the total moving.

A count going up tells you volume changed. It cannot tell you the thing itself
changed character. This sweep measures the other half: for every clocked table
that carries a low-cardinality category -- a violation type, a case disposition,
an agency, a severity grade, a filing form -- it measures the SHARE of each
category per year.

Why it earns its place: a mix flip is much harder to explain away as a
collection artifact than a raw count is. If total inspections double, that is
probably budget or backfill. If the SHARE of the most serious violation class
triples while the total holds flat, something changed about the thing being
measured, or about who decides how to classify it. Both are findings.

It also detects the two collection tells the count sweep is blind to:
  * a category that APPEARS mid-series -- almost always a schema or form change
  * a category that VANISHES -- a code retired, or a reporting pathway closed

Two stages per table, both aggregate-only:
  1. measure the cardinality of every candidate category column (one scan)
  2. for the columns that are genuinely categorical, one GROUPING SETS query
     returns year x value counts for ALL of them in a single further scan

Read-only. Checkpointed per table. Writes reports/time_index/mix.jsonl.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _snowflake_conn import connect  # noqa: E402
from _time_targets import (TI, Checkpoint, DATE_TYPES, date_expr,  # noqa: E402
                           load_catalog, load_clock_roles, load_measured,
                           pick_measurable, table_alias_map, year_expr)

OUT = os.path.join(TI, "mix.jsonl")
CKPT = os.path.join(TI, "mix_done.json")

CAT_NAME = re.compile(
    r"(^|_)(TYPE|STATUS|CATEGORY|CATEG|CLASS|KIND|REASON|OUTCOME|DISPOSITION|"
    r"RESULT|SOURCE|AGENCY|PROGRAM|SECTOR|INDUSTRY|GROUP|LEVEL|SEVERITY|GRADE|"
    r"STATE|COUNTRY|REGION|PARTY|GENDER|SEX|RACE|METHOD|MODE|ACTION|FLAG|"
    r"INDICATOR|SCOPE|TIER|ROLE|UNIT|BRANCH|FORM|RATING|JURISDICTION|OFFICE|"
    r"DIVISION|DEPARTMENT|CHAPTER|COURT|CIRCUIT|DECISION|VERDICT|SANCTION)($|_)")
ID_NAME = re.compile(r"(^|_)(ID|IDS|NUMBER|NUM|NO|KEY|CODE|SEQ|UUID|GUID)$")
# Priority when a table offers more candidates than we are willing to scan.
PRIORITY = ["TYPE", "STATUS", "CATEGORY", "CLASS", "SEVERITY", "GRADE", "OUTCOME",
            "DISPOSITION", "REASON", "ACTION", "LEVEL", "AGENCY", "PROGRAM"]
MAX_COLS = 10          # candidate columns scanned per table
MIN_DISTINCT = 2       # one value is not a mix
MAX_DISTINCT = 60      # beyond this it is an identifier or free text, not a category
MAX_CELLS = 60000
CLOCK_RANK = {"happened": 0, "reported": 1, "decided": 2, "span_start": 3}


def _priority(col):
    for i, p in enumerate(PRIORITY):
        if p in col:
            return i
    return len(PRIORITY)


def load_targets():
    roles = load_clock_roles()
    meas = load_measured()
    alias = table_alias_map()
    cat = load_catalog()
    targets = []
    for model, byrole in roles.items():
        clock = cm = None
        for role in sorted(CLOCK_RANK, key=CLOCK_RANK.get):
            cm = pick_measurable(byrole, role, model, meas)
            if cm is not None:
                clock = (role, cm)
                break
        full = alias.get(model)
        if clock is None or not full:
            continue
        if int(cm["trusted"] or 0) <= 0 and not (cm["ymin"] or "").strip():
            continue
        clock_col = cm["col"].upper()
        cands = [c for c, dt in cat.get(model, [])
                 if dt == "TEXT" and CAT_NAME.search(c) and not ID_NAME.search(c)
                 and c != clock_col and not c.startswith("_")]
        if not cands:
            continue
        cands.sort(key=lambda c: (_priority(c), len(c)))
        targets.append({
            "table": full, "model": model, "clock": clock[0],
            "clock_col": cm["col"], "clock_dtype": cm["dtype"],
            "clock_grain": cm["grain"],
            "candidates": cands[:MAX_COLS],
            "n_candidates_total": len(cands),
            "n_rows": int(cm["n_rows"] or 0),
        })
    targets.sort(key=lambda t: t["n_rows"])
    return targets


def year_of_clock(t):
    """Year expression for the table's primary clock, cast-safe either way."""
    if t["clock_grain"] == "year" and t["clock_dtype"] not in DATE_TYPES:
        return year_expr(t["clock_col"])
    return "year({})".format(date_expr(t["clock_col"], t["clock_dtype"]))


def _src(t):
    sch, tab = t["table"].split(".", 1)
    return 'LIBRARY_MARTS."{}"."{}"'.format(sch, tab)


def cardinality_sql(t):
    parts = []
    for c in t["candidates"]:
        parts.append('approx_count_distinct("{}")'.format(c))
        parts.append('count("{}")'.format(c))
    return "select {} from {}".format(", ".join(parts), _src(t))


def mix_sql(t, cols):
    sel = ", ".join('to_varchar("{}") as c{}'.format(c, i) for i, c in enumerate(cols))
    names = ", ".join("c{}".format(i) for i in range(len(cols)))
    sets = ", ".join("(y, c{})".format(i) for i in range(len(cols)))
    return (
        "with b as (select {} as y, {} from {}) "
        "select grouping_id({}) as gid, y, {}, count(*) as n "
        "from b where y is not null "
        "group by grouping sets ({}) "
        "order by gid, y"
    ).format(year_of_clock(t), sel, _src(t), names, names, sets)


def gid_for(index, n_cols):
    """GROUPING_ID bitmask when column `index` is the one being grouped by.

    GROUPING_ID sets a bit for every listed column that is AGGREGATED away, with
    the first column as the most significant bit. So exactly one bit is clear.
    """
    return ((1 << n_cols) - 1) ^ (1 << (n_cols - 1 - index))


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    targets = load_targets()
    if limit:
        targets = targets[:limit]
    ck = Checkpoint(OUT, CKPT)
    conn = connect(database="LIBRARY_MARTS")
    cur = conn.cursor()
    print("{} clocked tables offer a candidate category column; {} already measured"
          .format(len(targets), len(ck.done)), flush=True)

    ok = skipped = failed = 0
    for t in targets:
        key = t["table"]
        if ck.has(key):
            continue
        try:
            cur.execute(cardinality_sql(t))
            row = cur.fetchone()
        except Exception as e:
            ck.write(key, dict(t, stage="cardinality", error=str(e)[:300]))
            failed += 1
            continue

        card = []
        for i, c in enumerate(t["candidates"]):
            card.append({"col": c, "approx_distinct": int(row[2 * i] or 0),
                         "nonnull": int(row[2 * i + 1] or 0)})
        keep = [k["col"] for k in card
                if MIN_DISTINCT <= k["approx_distinct"] <= MAX_DISTINCT
                and k["nonnull"] > 0]
        if not keep:
            ck.write(key, dict(t, cardinality=card, kept=[], series=[],
                               note="no column in the categorical band"))
            skipped += 1
            continue

        try:
            cur.execute(mix_sql(t, keep))
            rows = cur.fetchmany(MAX_CELLS)
            truncated = len(rows) == MAX_CELLS and cur.fetchone() is not None
        except Exception as e:
            ck.write(key, dict(t, cardinality=card, kept=keep, stage="mix",
                               error=str(e)[:300]))
            failed += 1
            continue

        want = {gid_for(i, len(keep)): i for i in range(len(keep))}
        series = {c: [] for c in keep}
        for r in rows:
            idx = want.get(int(r[0]))
            if idx is None:
                continue
            col = keep[idx]
            series[col].append([None if r[1] is None else int(r[1]),
                                r[2 + idx], int(r[-1])])
        rec = dict(t)
        rec["cardinality"] = card
        rec["kept"] = keep
        rec["truncated"] = truncated
        rec["series"] = [{"col": c, "cells": series[c]} for c in keep]
        ck.write(key, rec)
        ok += 1
        if ok % 25 == 0:
            print("  {} measured, {} had no real category ({} failed)"
                  .format(ok, skipped, failed), flush=True)

    print("MIX SWEEP DONE  measured={} skipped={} failed={}"
          .format(ok, skipped, failed), flush=True)


if __name__ == "__main__":
    main()
