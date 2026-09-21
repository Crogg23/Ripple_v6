"""One-off, 2026-09-21: remove dead objects found by the pre-launch audit. Chris gave `greenlight destroy`.

What goes, and the proof taken before it goes:
  1. Staging views in LIBRARY_STAGING.DBT_CROGERS with no dbt model file behind them. Re-derived at run time,
     then each one re-checked for zero readers in SNOWFLAKE.ACCOUNT_USAGE.OBJECT_DEPENDENCIES.
  2. Schema LIBRARY_STAGING.DBT_CROGERS_RIPPLE, the frozen pre-fix copy. Zero readers.
  3. Two junk public views, THE_LIBRARY.JUSTICE.FRAUD_SETTLEMENTS (DOJ nav-menu text) and
     THE_LIBRARY.COMPANIES.BENEFICIAL_OWNERSHIP_REGISTRY (one row saying ACCESS RESTRICTED), plus their two
     rows in LIBRARY_META.REGISTRY.FRIENDLY_LAYER.

What does NOT go, on purpose: the capped landing tables FED_SAM_EXCLUSIONS and FED_USASPENDING_ASSISTANCE_FULL
(dbt landing_clean and staging models still read them) and the __PREV_ backup tables (11 of them, not reviewed).

Every dropped view's DDL, fully qualified, and the two registry rows are written to
outputs/step1_dropped_ddl_2026-09-21.sql BEFORE the first drop. Dry run by default; --apply executes.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

OUT = REPO / "outputs" / "step1_dropped_ddl_2026-09-21.sql"
JUNK = [("JUSTICE", "FRAUD_SETTLEMENTS"), ("COMPANIES", "BENEFICIAL_OWNERSHIP_REGISTRY")]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    apply = ap.parse_args().apply
    conn = db.connect()

    live = {r[0] for r in db.rows(conn, "select table_name from LIBRARY_STAGING.information_schema.views where table_schema='DBT_CROGERS'")}
    files = {p.stem.upper() for p in (REPO / "library-onboarding" / "ripple_dbt" / "models").rglob("*.sql")}
    orphans = sorted(live - files)
    read = {r[0] for r in db.rows(conn, """select referenced_object_name from SNOWFLAKE.ACCOUNT_USAGE.OBJECT_DEPENDENCIES
        where referenced_database='LIBRARY_STAGING' and referenced_schema='DBT_CROGERS'
          and not (referencing_database='LIBRARY_STAGING' and referencing_schema='DBT_CROGERS_RIPPLE')""")}
    held = [o for o in orphans if o in read]
    orphans = [o for o in orphans if o not in read]
    print(f"orphan staging views to drop: {len(orphans)}; held back because something reads them: {len(held)} {held[:5]}")

    frozen_readers = db.rows(conn, "select count(*) from SNOWFLAKE.ACCOUNT_USAGE.OBJECT_DEPENDENCIES where referenced_schema='DBT_CROGERS_RIPPLE'")[0][0]
    print("frozen schema DBT_CROGERS_RIPPLE readers:", frozen_readers)
    junk_readers = db.rows(conn, """select count(*) from SNOWFLAKE.ACCOUNT_USAGE.OBJECT_DEPENDENCIES
        where referenced_database='THE_LIBRARY' and referenced_object_name in ('FRAUD_SETTLEMENTS','BENEFICIAL_OWNERSHIP_REGISTRY')""")[0][0]
    print("junk public view readers:", junk_readers)
    if frozen_readers or junk_readers:
        print("STOP: something reads an object on the list.")
        return 1

    # ---- save everything first
    parts = ["-- Dropped 2026-09-21 by scripts/drop_dead_objects_2026_09_21.py. Fully qualified; run a statement to bring a view back.\n"]
    for o in orphans:
        ddl = db.rows(conn, f"select get_ddl('view', 'LIBRARY_STAGING.DBT_CROGERS.{o}', true)")[0][0]
        parts.append(f"-- LIBRARY_STAGING.DBT_CROGERS.{o}\n{ddl}\n")
    for s, t in JUNK:
        ddl = db.rows(conn, f"select get_ddl('view', 'THE_LIBRARY.{s}.{t}', true)")[0][0]
        parts.append(f"-- THE_LIBRARY.{s}.{t}\n{ddl}\n")
    reg = db.rows(conn, "select * from LIBRARY_META.REGISTRY.FRIENDLY_LAYER where friendly_name in ('FRAUD_SETTLEMENTS','BENEFICIAL_OWNERSHIP_REGISTRY')")
    parts.append("-- LIBRARY_META.REGISTRY.FRIENDLY_LAYER rows removed:\n" + "\n".join("-- " + repr(r) for r in reg) + "\n")
    parts.append("-- LIBRARY_STAGING.DBT_CROGERS_RIPPLE: frozen one-shot copy of the staging schema from before the 2026-09-19 dedupe fix.\n"
                 "-- Its view bodies are the pre-fix staging models, which live in git history. Not re-created here.\n")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"saved {len(orphans) + len(JUNK)} view definitions and {len(reg)} registry rows to {OUT.relative_to(REPO)}")

    if not apply:
        print("DRY RUN -- nothing dropped.")
        return 0

    done = 0
    for o in orphans:
        db.rows(conn, f"drop view if exists LIBRARY_STAGING.DBT_CROGERS.{o}")
        done += 1
    print("dropped orphan staging views:", done)
    db.rows(conn, "drop schema if exists LIBRARY_STAGING.DBT_CROGERS_RIPPLE")
    print("dropped schema DBT_CROGERS_RIPPLE")
    for s, t in JUNK:
        db.rows(conn, f"drop view if exists THE_LIBRARY.{s}.{t}")
    n = db.rows(conn, "delete from LIBRARY_META.REGISTRY.FRIENDLY_LAYER where friendly_name in ('FRAUD_SETTLEMENTS','BENEFICIAL_OWNERSHIP_REGISTRY')")
    print("dropped 2 junk public views; registry rows deleted:", n)
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
