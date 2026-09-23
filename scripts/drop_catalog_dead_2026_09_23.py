"""One-off, 2026-09-23: remove the dead objects the catalog audit found. Needs `greenlight destroy`.

What goes (audit/catalog_audit_2026-09-23_verdict.md, fix 8):
  1. The 7 __PREV_ backup tables in LIBRARY_MARTS, snapshots taken 2026-09-06/07 before
     reloads. Each live table they back up has been rebuilt since. Last read 2026-09-08.
  2. LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT,
     an exact copy of HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT. Its dbt model is disabled
     in dbt_project.yml the same day, so no build brings it back.

Proof taken at run time, before anything drops:
  - zero rows in SNOWFLAKE.ACCOUNT_USAGE.OBJECT_DEPENDENCIES naming any of them
  - the PECOS pair still matches: same row count, same column list
  - each table's DDL and row count saved to outputs/catalog_dropped_ddl_2026-09-23.sql
Table DATA is not saved: LIBRARY_MARTS keeps dropped tables 1 day, so UNDROP TABLE works
until 24 hours after the drop, and never after.

Dry run by default; --apply executes.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

OUT = REPO / "outputs" / "catalog_dropped_ddl_2026-09-23.sql"
DEAD = [
    ("FINANCE", "FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES__PREV_20260906"),
    ("FINANCE", "FINANCE__FED_FEC_INDIV_CONTRIBUTIONS__PREV_20260906"),
    ("HEALTH", "HEALTH__FED_CMS_HCRIS__PREV_20260906"),
    ("HEALTH", "HEALTH__FED_HRSA_SHORTAGE_AREAS__PREV_20260907"),
    ("POLITICS", "POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP__PREV_20260906"),
    ("POLITICS", "POLITICS__FED_GOVINFO_BILLSTATUS__PREV_20260907"),
    ("SCIENCE", "SCIENCE__INTL_EMBL_ENSEMBL__PREV_20260907"),
    ("IMMIGRATION", "IMMIGRATION__FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT"),
]
KEEP_TWIN = ("HEALTH", "HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT")


def cols(conn, s, t):
    return [r[0] for r in db.rows(conn, f"""select column_name from LIBRARY_MARTS.information_schema.columns
        where table_schema='{s}' and table_name='{t}' order by ordinal_position""")]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    apply = ap.parse_args().apply
    conn = db.connect()

    names = ",".join(f"'{t}'" for _, t in DEAD)
    readers = db.rows(conn, f"""select referenced_object_name, referencing_database||'.'||referencing_schema||'.'||referencing_object_name
        from SNOWFLAKE.ACCOUNT_USAGE.OBJECT_DEPENDENCIES
        where referenced_database='LIBRARY_MARTS' and referenced_object_name in ({names})""")
    if readers:
        print("STOP: something reads an object on the list:", readers)
        return 1
    print("readers: 0")

    (ks, kt), (ds, dt_) = KEEP_TWIN, DEAD[-1]
    n_keep = db.rows(conn, f'select count(*) from LIBRARY_MARTS."{ks}"."{kt}"')[0][0]
    n_dead = db.rows(conn, f'select count(*) from LIBRARY_MARTS."{ds}"."{dt_}"')[0][0]
    if n_keep != n_dead or cols(conn, ks, kt) != cols(conn, ds, dt_):
        print(f"STOP: PECOS twin no longer matches ({n_keep:,} vs {n_dead:,} rows, or columns differ)")
        return 1
    print(f"PECOS twin still matches: {n_keep:,} rows, same columns")

    parts = ["-- Removed 2026-09-23 by scripts/drop_catalog_dead_2026_09_23.py. Structure only.\n"
             "-- UNDROP TABLE <name> restores data within 24 hours of removal.\n"]
    for s, t in DEAD:
        n = db.rows(conn, f'select count(*) from LIBRARY_MARTS."{s}"."{t}"')[0][0]
        ddl = db.rows(conn, f"select get_ddl('table', 'LIBRARY_MARTS.{s}.{t}', true)")[0][0]
        parts.append(f"-- LIBRARY_MARTS.{s}.{t}  rows at removal: {n:,}\n{ddl}\n")
        print(f"  {s}.{t}: {n:,} rows")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print("saved DDL to", OUT.relative_to(REPO))

    if not apply:
        print("DRY RUN -- nothing removed.")
        return 0
    # --apply runs only after Chris types `greenlight destroy` (CLAUDE.md, Don't do damage)
    for s, t in DEAD:
        db.rows(conn, f'drop table if exists LIBRARY_MARTS."{s}"."{t}"')
        print("removed", f"{s}.{t}")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
