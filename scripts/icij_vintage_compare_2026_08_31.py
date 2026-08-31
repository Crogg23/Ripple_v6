"""Which ICIJ snapshot is newer — canonical FED_ICIJ_OFFSHORELEAKS_* or the
skipped copies (XC_ICIJ_OFFSHORE_*, ICIJ_OFFSHORE_LEAKS_*)?

Read-only. For each table that still exists:
  - row count
  - which audit/ingest columns it carries and their max value
  - node_id range (min/max) where a node_id-ish column exists
Writes reports/row1/icij_vintage_compare_2026-08-31.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connect import db


def connect():
    return db.connect()

FAMILIES = {
    "RELATIONSHIPS": ["FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS", "XC_ICIJ_OFFSHORE_RELATIONSHIPS", "ICIJ_OFFSHORE_LEAKS_RELATIONSHIPS"],
    "ENTITIES": ["FED_ICIJ_OFFSHORELEAKS_ENTITIES", "XC_ICIJ_OFFSHORE_NODES_ENTITIES", "ICIJ_OFFSHORE_LEAKS_ENTITIES"],
    "OFFICERS": ["FED_ICIJ_OFFSHORELEAKS_OFFICERS", "XC_ICIJ_OFFSHORE_NODES_OFFICERS", "ICIJ_OFFSHORE_LEAKS_OFFICERS"],
    "ADDRESSES": ["FED_ICIJ_OFFSHORELEAKS_ADDRESSES", "XC_ICIJ_OFFSHORE_NODES_ADDRESSES", "ICIJ_OFFSHORE_LEAKS_ADDRESSES"],
    "INTERMEDIARIES": ["FED_ICIJ_OFFSHORELEAKS_INTERMEDIARIES", "XC_ICIJ_OFFSHORE_NODES_INTERMEDIARIES", "ICIJ_OFFSHORE_LEAKS_INTERMEDIARIES"],
    "OTHERS": ["FED_ICIJ_OFFSHORELEAKS_OTHERS", "XC_ICIJ_OFFSHORE_NODES_OTHERS", "ICIJ_OFFSHORE_LEAKS_OTHERS"],
}

AUDIT_HINTS = ("_INGESTED_AT", "INGESTED_AT", "_LOADED_AT", "LOADED_AT", "_SOURCE_RUN_ID", "SOURCE_RUN_ID")
ID_HINTS = ("NODE_ID", "_ID", "ID")


def main():
    conn = connect()
    cur = conn.cursor()
    cur.execute("select current_database()")
    db = cur.fetchone()[0]
    cur.execute(
        "select table_schema, table_name from information_schema.tables "
        "where table_name in (%s)" % ",".join("'%s'" % t for f in FAMILIES.values() for t in f)
    )
    located = {r[1]: r[0] for r in cur.fetchall()}
    out = {"database": db, "located": located, "families": {}}
    for fam, tables in FAMILIES.items():
        rows = []
        for t in tables:
            if t not in located:
                rows.append({"table": t, "exists": False})
                continue
            fq = '%s."%s"."%s"' % (db, located[t], t)
            cur.execute(
                "select column_name from information_schema.columns "
                "where table_schema='%s' and table_name='%s'" % (located[t], t)
            )
            cols = [r[0] for r in cur.fetchall()]
            info = {"table": t, "exists": True, "schema": located[t], "n_cols": len(cols)}
            cur.execute("select count(*) from %s" % fq)
            info["rows"] = cur.fetchone()[0]
            for c in cols:
                if c.upper() in AUDIT_HINTS:
                    cur.execute('select min("%s"), max("%s") from %s' % (c, c, fq))
                    mn, mx = cur.fetchone()
                    info.setdefault("audit", {})[c] = {"min": str(mn), "max": str(mx)}
            idcol = next((c for c in cols if c.upper() == "NODE_ID"), None)
            if idcol:
                cur.execute('select min(try_to_number("%s")), max(try_to_number("%s")) from %s' % (idcol, idcol, fq))
                mn, mx = cur.fetchone()
                info["node_id_range"] = [str(mn), str(mx)]
            rows.append(info)
        out["families"][fam] = rows
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reports", "row1", "icij_vintage_compare_2026-08-31.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
