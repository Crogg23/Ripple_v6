"""Drop the 8 surviving ICIJ copy tables — proven same-snapshot duplicates.

Evidence chain: reports/row1/icij_vintage_verdict_2026-08-31.md.
Safety: each copy is re-proven identical to canonical at run time with a
blank-normalized HASH_AGG (trim; '', 'NA', 'None', 'N/A', 'n/a' -> NULL)
over non-audit columns, plus matching row counts. Any mismatch = skip.

Run by Chris's own hand after "greenlight destroy":
    python3 scripts/drop_icij_copies_2026_08_31.py
Log: reports/row1/icij_drop_log_2026-08-31.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connect import db

DB = "LIBRARY_RAW"
SCHEMA = "LANDING"
PAIRS = [
    ("FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS", "XC_ICIJ_OFFSHORE_RELATIONSHIPS"),
    ("FED_ICIJ_OFFSHORELEAKS_ENTITIES", "XC_ICIJ_OFFSHORE_NODES_ENTITIES"),
    ("FED_ICIJ_OFFSHORELEAKS_OFFICERS", "XC_ICIJ_OFFSHORE_NODES_OFFICERS"),
    ("FED_ICIJ_OFFSHORELEAKS_ADDRESSES", "XC_ICIJ_OFFSHORE_NODES_ADDRESSES"),
    ("FED_ICIJ_OFFSHORELEAKS_INTERMEDIARIES", "XC_ICIJ_OFFSHORE_NODES_INTERMEDIARIES"),
    ("FED_ICIJ_OFFSHORELEAKS_ENTITIES", "ICIJ_OFFSHORE_LEAKS_ENTITIES"),
    ("FED_ICIJ_OFFSHORELEAKS_OFFICERS", "ICIJ_OFFSHORE_LEAKS_OFFICERS"),
    ("FED_ICIJ_OFFSHORELEAKS_ADDRESSES", "ICIJ_OFFSHORE_LEAKS_ADDRESSES"),
]
AUDIT = ("_INGESTED_AT", "_SOURCE_RUN_ID", "_SRC_SHA256",
         "INGESTED_AT", "SOURCE_RUN_ID", "SRC_SHA256")

# Known residue after normalization: ENTITIES bare-prefix has exactly 5 rows
# where canonical NULL = copy 'n/a' in IBCRUC (case-sensitive miss). The
# normalizer below folds lowercase too, so run-time hashes should match; if
# they do not, the pair is skipped and logged.


def norm(col):
    inner = f'trim("{col}")'
    for blank in ("''", "'NA'", "'None'", "'N/A'", "'n/a'"):
        inner = f"nullif({inner},{blank})"
    return inner


def main():
    conn = db.connect()
    cur = conn.cursor()
    log = []
    for canon, dup in PAIRS:
        entry = {"canonical": canon, "duplicate": dup}
        cur.execute(
            "select column_name from %s.information_schema.columns "
            "where table_schema='%s' and table_name='%s' order by ordinal_position"
            % (DB, SCHEMA, canon)
        )
        cols = [r[0] for r in cur.fetchall() if r[0] not in AUDIT]
        cur.execute(
            "select column_name from %s.information_schema.columns "
            "where table_schema='%s' and table_name='%s'" % (DB, SCHEMA, dup)
        )
        dup_cols = {r[0] for r in cur.fetchall() if r[0] not in AUDIT}
        if set(cols) != dup_cols:
            entry["action"] = "SKIPPED — column sets differ"
            print(entry)
            log.append(entry)
            continue
        sel = ",".join(norm(c) for c in cols)
        hashes = []
        ok = True
        for t in (canon, dup):
            try:
                cur.execute(f"select hash_agg({sel}), count(*) from {DB}.{SCHEMA}.{t}")
                hashes.append(cur.fetchone())
            except Exception as exc:
                entry["error"] = f"{t}: {exc}"
                ok = False
                break
        if ok and hashes[0] == hashes[1]:
            entry["rows"] = hashes[0][1]
            cur.execute(f"drop table {DB}.{SCHEMA}.{dup}")
            entry["action"] = "DROPPED"
        elif ok:
            entry["action"] = "SKIPPED — normalized content still differs"
            entry["rows"] = [hashes[0][1], hashes[1][1]]
        else:
            entry["action"] = "SKIPPED — error"
        print(entry)
        log.append(entry)
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "reports", "row1", "icij_drop_log_2026-08-31.json")
    with open(path, "w") as fh:
        json.dump(log, fh, indent=2)
    print("log written:", path)


if __name__ == "__main__":
    main()
