"""Drop the duplicate ICIJ / RCRA table copies. 2026-08-31, Chris: 'greenlight destroy'.

Canonical = what the dbt staging layer reads (verified in repo):
  ICIJ: FED_ICIJ_OFFSHORELEAKS_*     drop: XC_ICIJ_OFFSHORE_NODES_* / XC_ICIJ_OFFSHORE_* / ICIJ_OFFSHORE_LEAKS_*
  RCRA: FED_EPA_RCRA_*               drop: FED_EPA_RCRA_RCRA_*  (except RCRA_NAICS — no twin, canonical as-is)

Safety: a copy is dropped ONLY if HASH_AGG(*) equals the canonical's — content identity,
not just row counts. Mismatches are reported and left alone. Snowflake time travel
allows UNDROP within retention. Log: reports/row1/drop_log_2026-08-31.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _snowflake_conn import connect

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "reports", "row1", "drop_log_2026-08-31.json")
DB = "LIBRARY_RAW.LANDING"

# (canonical, [duplicates])
FAMILIES = [
    ("FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS", ["XC_ICIJ_OFFSHORE_RELATIONSHIPS", "ICIJ_OFFSHORE_LEAKS_RELATIONSHIPS"]),
    ("FED_ICIJ_OFFSHORELEAKS_ENTITIES", ["XC_ICIJ_OFFSHORE_NODES_ENTITIES", "ICIJ_OFFSHORE_LEAKS_ENTITIES"]),
    ("FED_ICIJ_OFFSHORELEAKS_OFFICERS", ["XC_ICIJ_OFFSHORE_NODES_OFFICERS", "ICIJ_OFFSHORE_LEAKS_OFFICERS"]),
    ("FED_ICIJ_OFFSHORELEAKS_ADDRESSES", ["XC_ICIJ_OFFSHORE_NODES_ADDRESSES", "ICIJ_OFFSHORE_LEAKS_ADDRESSES"]),
    ("FED_ICIJ_OFFSHORELEAKS_INTERMEDIARIES", ["XC_ICIJ_OFFSHORE_NODES_INTERMEDIARIES", "ICIJ_OFFSHORE_LEAKS_INTERMEDIARIES"]),
    ("FED_ICIJ_OFFSHORELEAKS_OTHERS", ["XC_ICIJ_OFFSHORE_NODES_OTHERS", "ICIJ_OFFSHORE_LEAKS_OTHERS"]),
    ("FED_EPA_RCRA_FACILITIES", ["FED_EPA_RCRA_RCRA_FACILITIES"]),
    ("FED_EPA_RCRA_EVALUATIONS", ["FED_EPA_RCRA_RCRA_EVALUATIONS"]),
    ("FED_EPA_RCRA_VIOLATIONS", ["FED_EPA_RCRA_RCRA_VIOLATIONS"]),
    ("FED_EPA_RCRA_VIOSNC_HISTORY", ["FED_EPA_RCRA_RCRA_VIOSNC_HISTORY"]),
    ("FED_EPA_RCRA_ENFORCEMENTS", ["FED_EPA_RCRA_RCRA_ENFORCEMENTS"]),
]


def data_cols(cur, table):
    """Columns excluding per-load audit columns, which legitimately differ."""
    cur.execute(f"""select column_name from LIBRARY_RAW.information_schema.columns
        where table_schema='LANDING' and table_name='{table}'
          and column_name not in ('_INGESTED_AT','_SOURCE_RUN_ID','_SRC_SHA256',
                                  'INGESTED_AT','SOURCE_RUN_ID','SRC_SHA256')
        order by ordinal_position""")
    return [r[0] for r in cur.fetchall()]


def main():
    conn = connect()
    cur = conn.cursor()
    log = []
    for canon, dups in FAMILIES:
        ccols = data_cols(cur, canon)
        sel = ", ".join(f'"{c}"' for c in ccols)
        cur.execute(f"select hash_agg({sel}), count(*) from {DB}.{canon}")
        chash, crows = cur.fetchone()
        for dup in dups:
            dcols = data_cols(cur, dup)
            entry = dict(canonical=canon, duplicate=dup)
            if [c.upper() for c in dcols] != [c.upper() for c in ccols]:
                entry["action"] = "SKIPPED — column sets differ"
                entry["canon_cols"] = len(ccols); entry["dup_cols"] = len(dcols)
                log.append(entry); print(entry); continue
            cur.execute(f"select hash_agg({sel}), count(*) from {DB}.{dup}")
            dhash, drows = cur.fetchone()
            entry.update(rows=drows, content_identical=(chash == dhash and crows == drows))
            if entry["content_identical"]:
                cur.execute(f"drop table {DB}.{dup}")
                entry["action"] = "DROPPED"
            else:
                entry["action"] = "SKIPPED — content differs"
            log.append(entry); print(entry)
    conn.close()
    with open(OUT, "w") as fh:
        json.dump(log, fh, indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
