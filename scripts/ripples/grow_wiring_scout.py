"""Grow-the-wiring scout (read-only).

The wire-confirm pass showed 81% of the resemblance queue touches tables the
entity spine has never wired. This scout answers, cheaply and impartially:

  1. WHICH dark tables block the most queue pairs (the ranked build list).
  2. WHAT joinable-looking ID columns those tables actually contain.
  3. Whether each candidate key is REAL -- count, distinct count, and a value
     sample together (the bare-COUNT trap has burned this platform twice).

Read-only: no writes anywhere. Output: reports/wiring_scout_<date>.json + .md.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, os.path.join(BASE, "scripts"))

TOP_N_TABLES = int(sys.argv[1]) if len(sys.argv) > 1 else 25
ID_PATTERNS = [
    ("EIN", r"\bEIN\b|FEIN|EMPLOYER_ID"),
    ("NPI", r"\bNPI\b"),
    ("UEI", r"\bUEI\b|UNIQUE_ENTITY"),
    ("DUNS", r"DUNS"),
    ("CIK", r"\bCIK\b"),
    ("LEI", r"\bLEI\b"),
    ("CMS_CCN", r"\bCCN\b|PROVNUM|PROVIDER_NUM|FEDERAL_PROVIDER"),
    ("FRS_ID", r"FRS_ID|REGISTRY_ID"),
    ("DEA_NO", r"\bDEA\b"),
    ("DOCKET", r"DOCKET"),
    ("PERMIT", r"PERMIT_?(NO|NUM|ID)"),
    ("BIOGUIDE", r"BIOGUIDE"),
    ("FEC_ID", r"FEC_?(ID|CAND|CMTE)|CAND_ID|CMTE_ID"),
    ("ZIP", r"\bZIP\b|ZIP_?CODE|POSTAL"),
    ("STATE", r"^STATE$|STATE_?(CODE|ABBR)$"),
    ("FIPS", r"FIPS|COUNTY_CODE"),
    ("NAME", r"(COMPANY|ORG|FACILITY|EMPLOYER|SPONSOR|RECIPIENT|CONTRIBUTOR|"
             r"VENDOR|OWNER|PROVIDER|BUSINESS)_?NAME|^NAME$|LEGAL_NAME"),
]


def node_id(table):
    t = table.split(".")[-1]
    if "__" in t:
        t = t.split("__", 1)[1]
    return t.upper()


def main():
    from _snowflake_conn import connect
    with open(os.path.join(
            BASE, "reports",
            "ripples_lead_lag_deseasonalized_2026-08-21.json")) as fh:
        queue = json.load(fh)["survivors"]

    conn = connect()
    cur = conn.cursor()
    cur.execute('select A, B from LIBRARY_META."CONNECT".CONNECT_EDGES')
    spine_nodes = set()
    for a, b in cur.fetchall():
        spine_nodes.add(a)
        spine_nodes.add(b)
    print(f"{len(spine_nodes)} tables on the spine")

    # 1. rank dark tables by how many queue pairs they block
    blocked = Counter()
    table_full = {}
    for p in queue:
        for t in (p["a_table"], p["b_table"]):
            n = node_id(t)
            table_full[n] = t
            if n not in spine_nodes:
                blocked[n] += 1
    ranked = blocked.most_common(TOP_N_TABLES)
    print(f"{len(blocked)} dark tables; top {TOP_N_TABLES} block "
          f"{sum(c for _, c in ranked)} pair-slots")

    # 2+3. column hunt with the fake-ID guard, per top table
    results = []
    for node, n_blocked in ranked:
        full = table_full[node]
        db_schema, tbl = full.rsplit(".", 1)
        schema = db_schema.split(".")[-1] if "." in db_schema else db_schema
        try:
            cur.execute(
                "select COLUMN_NAME from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS "
                "where TABLE_SCHEMA = %s and TABLE_NAME = %s", (schema, tbl))
            cols = [r[0] for r in cur.fetchall()]
        except Exception as e:
            results.append({"table": full, "blocked_pairs": n_blocked,
                            "error": str(e)[:200]})
            continue
        hits = []
        for kind, pat in ID_PATTERNS:
            for c in cols:
                if re.search(pat, c.upper()):
                    hits.append((kind, c))
                    break
        checked = []
        for kind, c in hits:
            try:
                cur.execute(
                    f'select count("{c}"), count(distinct "{c}") '
                    f'from LIBRARY_MARTS.{schema}."{tbl}"')
                n, nd = cur.fetchone()
                cur.execute(
                    f'select "{c}", count(*) c from LIBRARY_MARTS.{schema}."{tbl}" '
                    f'where "{c}" is not null group by 1 order by 2 desc limit 5')
                sample = cur.fetchall()
                # sentinel guard: a "key" whose top value covers >30% is suspect
                top_share = (sample[0][1] / n) if n and sample else None
                verdict = ("REAL" if nd and nd > 50 and (top_share or 0) < 0.3
                           else "SUSPECT")
                checked.append({
                    "kind": kind, "column": c, "count": n, "distinct": nd,
                    "top_values": [[str(v)[:40], k] for v, k in sample],
                    "top_share": round(top_share, 3) if top_share else None,
                    "verdict": verdict})
            except Exception as e:
                checked.append({"kind": kind, "column": c,
                                "error": str(e)[:150]})
        results.append({"table": full, "blocked_pairs": n_blocked,
                        "n_columns": len(cols), "keys": checked})
        real = [k["kind"] for k in checked if k.get("verdict") == "REAL"]
        print(f"{node:55s} blocks {n_blocked:3d}  real keys: {real}")

    conn.close()
    out = {"as_of": str(date.today()), "spine_tables": len(spine_nodes),
           "dark_tables_total": len(blocked), "scouted": results}
    path = os.path.join(BASE, "reports",
                        f"wiring_scout_{date.today()}.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote", path)


if __name__ == "__main__":
    main()
