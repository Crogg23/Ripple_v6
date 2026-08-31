"""Row 1 of the verification audit: loads vs publisher reality.

Read-only. Dumps to reports/row1/:
  - landing_counts.json  : every BASE TABLE in LIBRARY_RAW.LANDING with row counts (info_schema)
  - orphans.json         : registry rows with no landing table (flag INCLUDE=true),
                           landing tables with no registry row
Publisher-side totals are gathered separately (web) and joined by hand in the report.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _snowflake_conn import connect

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "reports", "row1")
os.makedirs(OUT, exist_ok=True)


def main():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        select table_name, row_count, bytes
        from LIBRARY_RAW.information_schema.tables
        where table_schema = 'LANDING' and table_type = 'BASE TABLE'
        order by row_count desc
    """)
    landing = [{"table": r[0], "rows": r[1], "bytes": r[2]} for r in cur.fetchall()]

    cur.execute("""
        select SOURCE_ID, INCLUDE, VOLUME, NOTES
        from LIBRARY_META.REGISTRY.SOURCE_REGISTRY
    """)
    registry = [{"source_id": r[0], "include": r[1], "volume": r[2], "notes": r[3]}
                for r in cur.fetchall()]
    conn.close()

    for r in registry:
        r["include"] = str(r["include"]).upper() in ("Y", "TRUE", "T", "1")

    landing_names = {t["table"] for t in landing}
    reg_no_landing = [r for r in registry
                      if (r["source_id"] or "").upper() not in landing_names]
    reg_names = {(r["source_id"] or "").upper() for r in registry}
    landing_no_reg = [t for t in landing if t["table"] not in reg_names]

    with open(os.path.join(OUT, "landing_counts.json"), "w") as fh:
        json.dump(landing, fh, indent=1)
    with open(os.path.join(OUT, "registry_dump.json"), "w") as fh:
        json.dump(registry, fh, indent=1)
    with open(os.path.join(OUT, "orphans.json"), "w") as fh:
        json.dump({
            "registry_rows_no_landing": reg_no_landing,
            "registry_rows_no_landing_include_true":
                [r for r in reg_no_landing if r["include"]],
            "landing_tables_no_registry": landing_no_reg,
        }, fh, indent=1)

    print(f"landing tables: {len(landing)}  total rows: {sum(t['rows'] or 0 for t in landing):,}")
    print(f"registry rows: {len(registry)}")
    print(f"registry-no-landing: {len(reg_no_landing)} "
          f"(INCLUDE=true: {sum(1 for r in reg_no_landing if r['include'])})")
    print(f"landing-no-registry: {len(landing_no_reg)}")
    print("top 40 by rows:")
    for t in landing[:40]:
        print(f"  {t['rows']:>13,}  {t['table']}")


if __name__ == "__main__":
    main()
