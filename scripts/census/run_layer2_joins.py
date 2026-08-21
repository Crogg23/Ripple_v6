"""Item 3 of layer 2: run the 206 already-proven-real joins for real.

Layer 1 flagged 206 counts as needs="two tables" -- it found the same strong
key (EIN, NPI, CIK, ...) living in more than one mart and wrote the per-key
join SQL, but never ran it. This script re-derives those same 206 pairs and,
for each, runs ONE overlap query:

    select count(*) as a_rows, count(b.key) as a_matched,
           count(*) - count(b.key) as a_unmatched
    from A left join B on A.key = B.key where A.key is not null;

-- "how many rows really match, how many don't" -- instead of the per-key
top-100 breakdown layer 1 generated. That is the literal ask for the
moderate tier: not noting on paper that a key exists on both sides, but
getting the real number.

THREE MODES, in order of increasing warehouse spend. Nothing runs against the
warehouse unless you pass --sample or --run -- the default is a local, free
price estimate. This is the CLAUDE.md 8.7 gate: a price tag shown before any
spend, every time.

  python run_layer2_joins.py            price estimate only, no warehouse
  python run_layer2_joins.py --sample 15   run 15 real queries, report the
                                            actual $/query so the full-run
                                            estimate below stops being a guess
  python run_layer2_joins.py --run         run all 206, write
                                            reports/layer2_joins.json for the
                                            layer 2 page to pick up

Cost model: X-Small Snowflake warehouse time, calibrated from this repo's own
history (the 2026-08-08 full spine rebuild: ~4.5h / ~$10-15 on X-Small, i.e.
roughly $2.20-$3.30/credit-hour) -- not a vendor list price, this warehouse's
own measured rate. Applied to each query's own elapsed wall time once
--sample or --run actually measures it; before that, it's an assumption
stated as one, not a fact.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from _snowflake_conn import connect  # noqa: E402

DB = "LIBRARY_MARTS"
LAYER1_JSON = os.path.join(REPO, "reports", "count_possibilities.json")
OUT = os.path.join(REPO, "reports", "layer2_joins.json")

# This repo's own measured rate for this warehouse size, not Snowflake's list
# price -- see the 2026-08-08 spine rebuild in memory. A range, used at its
# midpoint for the headline number and stated as a range everywhere else.
DOLLARS_PER_CREDIT_HOUR = (2.20, 3.30)

NEEDS_RE = re.compile(r"^two tables \((.+) \+ (.+)\)$")
KEY_RE = re.compile(r"on a\.([A-Z_0-9]+) = b\.")


def load_pairs():
    """The 206 (table, other_table, key) triples layer 1 already proved real."""
    d = json.load(open(LAYER1_JSON, encoding="utf-8"))
    tables_by_name = {t["table"]: t for t in d["tables"]}
    pairs = []
    for e in d["entries"]:
        m = NEEDS_RE.match(e["needs"])
        if not m:
            continue
        key_m = KEY_RE.search(e["sql"])
        if not key_m:
            continue
        a_table, b_table = m.group(1), m.group(2)
        pairs.append({
            "a_table": a_table, "b_table": b_table, "key": key_m.group(1),
            "a_meta": tables_by_name.get(a_table, {}),
            "noun": e["noun"], "noun_known": e["noun_known"],
        })
    return pairs


def rowcounts():
    out = {}
    with open(os.path.join(REPO, "reports", "time_index", "live_tables.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out[f"{r['schema_name']}.{r['table_name']}"] = int(r["row_count"] or 0)
    return out


def build_sql(p):
    a, b, key = p["a_table"], p["b_table"], p["key"]
    return (f"select count(*)                        as a_rows,\n"
            f"       count(b.{key})                   as a_matched,\n"
            f"       count(*) - count(b.{key})        as a_unmatched\n"
            f"from {DB}.{a} as a\n"
            f"left join {DB}.{b} as b\n"
            f"  on a.{key} = b.{key}\n"
            f"where a.{key} is not null;")


def price_estimate(pairs, rc):
    """Local, free: rank by rows scanned as the cost proxy, no warehouse call."""
    total_rows = 0
    ranked = []
    for p in pairs:
        a_rows = rc.get(p["a_table"], 0)
        b_rows = rc.get(p["b_table"], 0)
        scanned = a_rows + b_rows
        total_rows += scanned
        ranked.append((scanned, p))
    ranked.sort(key=lambda x: -x[0])
    return total_rows, ranked


def run_queries(pairs, limit=None, conn=None):
    close = conn is None
    conn = conn or connect(database=DB)
    results = []
    try:
        cur = conn.cursor()
        todo = pairs if limit is None else pairs[:limit]
        for i, p in enumerate(todo, 1):
            sql = build_sql(p)
            t0 = time.time()
            cur.execute(sql)
            a_rows, a_matched, a_unmatched = cur.fetchone()
            elapsed = time.time() - t0
            results.append({**p, "sql": sql, "a_rows": a_rows,
                            "a_matched": a_matched, "a_unmatched": a_unmatched,
                            "elapsed_s": elapsed})
            print(f"  [{i}/{len(todo)}] {p['a_table']} x {p['b_table']} on {p['key']}: "
                  f"{a_matched:,}/{a_rows:,} matched ({elapsed:.1f}s)")
    finally:
        if close:
            conn.close()
    return results


def to_page_entries(results):
    entries = []
    for r in results:
        a, b, key = r["a_table"], r["b_table"], r["key"]
        n_rows, n_matched, n_unmatched = r["a_rows"], r["a_matched"], r["a_unmatched"]
        pct = round(100.0 * n_matched / n_rows, 1) if n_rows else 0.0
        noun = r["noun"]
        schema = a.split(".")[0]
        meta = r["a_meta"]
        entries.append({
            "kind": "The real overlap",
            "question": f"How many {noun}-linked rows in {a.split('.')[-1]} really "
                        f"match {b.split('.')[-1]}, on {key}?",
            "means": (f"Run for real: of {n_rows:,} rows with a {key}, "
                     f"{n_matched:,} ({pct}%) match a row in {b}, and "
                     f"{n_unmatched:,} ({round(100 - pct, 1)}%) don't. Not a guess from "
                     f"the key existing on both sides -- the actual left join."),
            "sql": r["sql"], "table": a, "fqn": f"{DB}.{a}",
            "dataset": meta.get("dataset", ""), "subject": meta.get("subject", schema.replace("_", " ").title()),
            "rows": meta.get("rows"), "noun": noun, "noun_known": r["noun_known"],
        })
    return entries


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=0,
                    help="run N real queries to calibrate the $/query estimate")
    ap.add_argument("--run", action="store_true",
                    help="run all 206 for real and write reports/layer2_joins.json")
    args = ap.parse_args()

    pairs = load_pairs()
    rc = rowcounts()
    print(f"{len(pairs)} proven-real join pairs loaded from layer 1.")

    if args.run:
        print(f"Running all {len(pairs)} for real against the warehouse...")
        results = run_queries(pairs)
        entries = to_page_entries(results)
        total_s = sum(r["elapsed_s"] for r in results)
        lo, hi = (total_s / 3600 * d for d in DOLLARS_PER_CREDIT_HOUR)
        json.dump({"entries": entries}, open(OUT, "w", encoding="utf-8"), indent=1)
        print(f"\n{len(entries)} real joins run, {total_s:.0f}s total, "
              f"est. ${lo:.2f}-${hi:.2f} -> {OUT}")
        return

    if args.sample:
        n = min(args.sample, len(pairs))
        print(f"Sampling {n} real queries to calibrate cost (biggest first, worst case)...")
        total_rows, ranked = price_estimate(pairs, rc)
        sample_pairs = [p for _, p in ranked[:n]]
        results = run_queries(sample_pairs)
        sample_s = sum(r["elapsed_s"] for r in results)
        sample_rows = sum(rc.get(p["a_table"], 0) + rc.get(p["b_table"], 0) for p in sample_pairs)
        s_per_row = sample_s / sample_rows if sample_rows else 0
        est_total_s = s_per_row * total_rows
        lo, hi = (est_total_s / 3600 * d for d in DOLLARS_PER_CREDIT_HOUR)
        print(f"\nSample: {n} queries, {sample_s:.1f}s actual.")
        print(f"Extrapolated to all {len(pairs)}: ~{est_total_s:.0f}s, "
              f"est. ${lo:.2f}-${hi:.2f}.")
        print("Run with --run to execute all 206 for real and build the page data.")
        return

    # Default: free, local, no warehouse call.
    total_rows, ranked = price_estimate(pairs, rc)
    print(f"Rows scanned across all {len(pairs)} joins (both sides, proxy for cost): "
          f"{total_rows:,}")
    print("Biggest 5 (worst case for the estimate):")
    for scanned, p in ranked[:5]:
        print(f"  {scanned:>14,}  {p['a_table']} x {p['b_table']} on {p['key']}")
    print("\nNo warehouse call made. Run with --sample N for a real $/query number, "
          "or --run to execute all 206.")


if __name__ == "__main__":
    main()
