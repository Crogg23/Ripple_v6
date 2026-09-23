"""Measure whether the join columns on the map actually hold values.

The map says two tables link because both carry a column called EIN. That is a
name match on the column, not proof there is anything in it. NPPES carries an
EIN column that is 100% empty strings, so a route through it joins nothing.

For every table that carries a key column, this counts:
  rows            how many rows the table holds
  filled          rows where the column is not null and not an empty string
  distinct        how many different values, approximately
It writes one row per table and column to a tsv, and a json the map reads.

One query per table, only the key columns, so Snowflake reads those columns
and nothing else.
"""
from __future__ import annotations

import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor

from connect.db import connect, dicts

CAT = "outputs/catalog/catalog.json"
OUT_TSV = "reports/key_fill_2026-09-23.tsv"
OUT_JSON = "outputs/catalog/keyfill.json"
WORKERS = 6

SAFE = re.compile(r"^[A-Z0-9_$]+$")


def safe(name: str) -> str:
    n = name.strip().upper()
    if not SAFE.match(n):
        raise ValueError("unsafe identifier: " + repr(name))
    return n


def probe(job):
    """One table. Returns a list of (schema, table, column, key, rows, filled, distinct)."""
    schema, table, cols = job
    picks = []
    for c in cols:
        col = safe(c["c"])
        picks.append(
            "count_if({0} is not null and trim(cast({0} as varchar)) <> '') as f_{1}".format(col, len(picks))
        )
        picks.append(
            "approx_count_distinct(case when trim(cast({0} as varchar)) <> '' then {0} end) as d_{1}".format(col, len(picks) // 2)
        )
    sql = "select count(*) as n, {} from LIBRARY_MARTS.{}.{}".format(
        ", ".join(picks), safe(schema), safe(table)
    )
    conn = connect()
    try:
        row = dicts(conn, sql)[0]
    finally:
        conn.close()
    out = []
    for i, c in enumerate(cols):
        out.append({
            "s": schema, "t": table, "c": c["c"], "k": c["k"],
            "rows": int(row["N"] or 0),
            "filled": int(row["F_%d" % i] or 0),
            "distinct": int(row["D_%d" % i] or 0),
        })
    return out


def main():
    cat = json.load(open(CAT))
    jobs = []
    for t in cat["tables"]:
        cols = [c for c in t["cols"] if c["k"]]
        # one column per key family is enough to judge the link
        seen, picks = set(), []
        for c in cols:
            if c["k"] in seen:
                continue
            seen.add(c["k"])
            picks.append(c)
        if picks:
            jobs.append((t["s"], t["t"], picks[:8]))

    print("tables to probe:", len(jobs), flush=True)
    rows, failed = [], []
    done = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(probe, j): j for j in jobs}
        for fut in futures:
            pass
        for fut, job in futures.items():
            try:
                rows.extend(fut.result())
            except Exception as exc:
                failed.append((job[0] + "." + job[1], str(exc)[:110]))
            done += 1
            if done % 50 == 0:
                print("  %d of %d" % (done, len(jobs)), flush=True)

    with open(OUT_TSV, "w", encoding="utf-8") as f:
        f.write("schema\ttable\tcolumn\tkey\trows\tfilled\tpct_filled\tdistinct\n")
        for r in sorted(rows, key=lambda r: (r["k"], -r["rows"])):
            pct = (r["filled"] / r["rows"] * 100) if r["rows"] else 0.0
            f.write("%s\t%s\t%s\t%s\t%d\t%d\t%.1f\t%d\n" % (
                r["s"], r["t"], r["c"], r["k"], r["rows"], r["filled"], pct, r["distinct"]))

    # what the map needs: per table, per key, how usable the column is
    fill = {}
    for r in rows:
        pct = (r["filled"] / r["rows"] * 100) if r["rows"] else 0.0
        fill.setdefault(r["s"] + "." + r["t"], {})[r["k"]] = [
            round(pct, 1), r["distinct"]
        ]
    json.dump(fill, open(OUT_JSON, "w"), separators=(",", ":"))

    print("wrote", OUT_TSV, "and", OUT_JSON)
    print("rows measured:", len(rows), "tables failed:", len(failed))
    for name, err in failed[:10]:
        print("  FAILED", name, err)


if __name__ == "__main__":
    main()
