"""Repair the 5 THE_LIBRARY views that repair_library_views.py skipped (2026-09-20).

Those 5 are not column drift. The source was reloaded in a different shape after the
friendly layer was last built (2026-07-12), so the old column list AND the old catalog
description are both wrong. Two were 1-row stubs then and hold real data now.

Each view is repointed at its cleaned mart with `select *`, gets a comment that says what
the data is today, and two get an honest new name:
    FBI_CRIME_INCIDENTS    -> FBI_CRIME_STATE_MONTHLY        (no incident rows exist)
    CDC_MORTALITY_QUERIES  -> CDC_MORTALITY_BY_CAUSE_AND_SEX (a result table, not a query log)

A rename is `alter view ... rename to`, never a drop. The same name/one_liner/comment is
written to LIBRARY_META.REGISTRY.FRIENDLY_LAYER and outputs/thelibrary_content.json. The names
file needs an entry keyed by the MART fqn too (thelibrary_build.py looks names up by the inventory
key, which is the mart); those were added by hand 2026-09-20. Not proven against a real refresh:
as of 2026-09-20 the names file covers 35 of 428 inventory keys, so a refresh would rename most of
the shelf -- do not run one until that is fixed. Note Snowflake stores a `select *` view with its
column list expanded: these can drift again when the mart changes shape.

    python scripts/repair_library_views_reshaped.py            # dry run
    python scripts/repair_library_views_reshaped.py --apply
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from connect import db  # noqa: E402

READ_ROLES = ("RIPPLE_READER", "CLAUDE_MCP_READONLY")
CONTENT = REPO / "outputs" / "thelibrary_content.json"

# landing fqn (the FRIENDLY_LAYER key) -> the repair
TARGETS = {
    "LIBRARY_RAW.LANDING.FED_FBI_CDE": {
        "schema": "CRIME_SECURITY", "old": "FBI_CRIME_INCIDENTS", "new": "FBI_CRIME_STATE_MONTHLY",
        "mart": "LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FBI_CDE",
        "one_liner": "FBI Crime Data Explorer monthly offense and clearance counts by state, 1985-2023.",
        "comment": "State-by-month counts from the FBI Crime Data Explorer: 51 states incl. DC, 10 offense "
                   "types, one row per state x offense x month with OFFENSES and CLEARANCES side by side, each "
                   "with a rate per 100K (landing holds them as two rows). Summary counts only -- "
                   "there are no incident, agency, victim or weapon rows here. Curated mart table.",
    },
    "LIBRARY_RAW.LANDING.FED_CDC_WONDER": {
        "schema": "HEALTH", "old": "CDC_MORTALITY_QUERIES", "new": "CDC_MORTALITY_BY_CAUSE_AND_SEX",
        "mart": "LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_WONDER",
        "one_liner": "CDC WONDER national deaths, population and crude rate by year, ICD chapter and sex, 1999-2020.",
        "comment": "National death counts from CDC WONDER, one row per year x ICD-10 chapter x sex, 1999-2020, "
                   "with population and crude rate per 100K. No age-adjusted rates, no state or county split. "
                   "Curated mart table.",
    },
    "LIBRARY_RAW.LANDING.FED_VA_ALLCAUSE_MORTALITY": {
        "schema": "HEALTH", "old": "VETERAN_MORTALITY_APPENDIX", "new": "VETERAN_MORTALITY_APPENDIX",
        "mart": "LIBRARY_MARTS.HEALTH.HEALTH__FED_VA_ALLCAUSE_MORTALITY",
        "one_liner": "VA leading causes of death for veterans by year, cohort and sex, 2018-2023.",
        "comment": "The all-cause mortality appendix from the VA, parsed into columns: ranked cause of death, "
                   "deaths, percent, unadjusted and age-adjusted rates, years of potential life lost, by year "
                   "2018-2023, cohort (Veteran, Recent-VHA Veteran, Other Veteran) and sex. Curated mart table.",
    },
    "LIBRARY_RAW.LANDING.FED_BIA_TRIBAL_GEO": {
        "schema": "GEOGRAPHY", "old": "TRIBAL_LANDS_GEO", "new": "TRIBAL_LANDS_GEO",
        "mart": "LIBRARY_MARTS.LAND_AND_TERRITORY.LAND_AND_TERRITORY__FED_BIA_TRIBAL_GEO",
        "one_liner": "Bureau of Indian Affairs land area representations: name, acres and boundary geometry.",
        "comment": "BIA Land Area Representations (LAR) from the BIA ArcGIS portal: LAR id, name, GIS acres, "
                   "shape area and length, and the boundary as GeoJSON-style rings. Curated mart table.",
    },
    "LIBRARY_RAW.LANDING.FED_NCUA_CALL_REPORTS": {
        "schema": "MONEY", "old": "CREDIT_UNION_CALL_REPORTS", "new": "CREDIT_UNION_CALL_REPORTS",
        "mart": "LIBRARY_MARTS.FINANCE.FINANCE__FED_NCUA_CALL_REPORTS_FS220",
        "one_liner": "NCUA quarterly call report (form FS220), one wide row per federally insured credit union, cycle 2026-03-31.",
        "comment": "The credit-union equivalent of a bank call report, NCUA form FS220: one row per credit union, with each account code as its own ACCT_ column (wide form, not one row per account). Holds one cycle date today, 2026-03-31. For names join to the NCUA FOICU call-report table on CU_NUMBER (4,336 of 4,336 match); the federally-insured list is keyed by CHARTER_NUMBER, not CU_NUMBER. Curated mart table.",
    },
}


def esc(s: str) -> str:
    return s.replace("'", "''")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="execute the DDL (default is a dry run)")
    args = ap.parse_args()

    conn = db.connect()
    cur = conn.cursor()
    plans = []
    for key, t in TARGETS.items():
        old_fqn = f'THE_LIBRARY."{t["schema"]}"."{t["old"]}"'
        new_fqn = f'THE_LIBRARY."{t["schema"]}"."{t["new"]}"'
        cur.execute(f"select get_ddl('view', '{old_fqn}', true)")
        old_ddl = cur.fetchone()[0]
        cur.execute(f"select * from {t['mart']} limit 0")
        n_cols = len(cur.description)
        cur.execute(f"select count(*) from {t['mart']}")
        n_rows = cur.fetchone()[0]
        if t["new"] != t["old"]:
            cur.execute(f"show views like '{t['new']}' in schema THE_LIBRARY.\"{t['schema']}\"")
            if cur.fetchall():
                print(f"SKIP {old_fqn} -- {t['new']} already exists"); continue
        cur.execute("select * from LIBRARY_META.REGISTRY.FRIENDLY_LAYER where LANDING_FQN = %s", (key,))
        fl_cols = [d[0] for d in cur.description]
        fl_rows = [dict(zip(fl_cols, (str(x) if x is not None else None for x in r))) for r in cur.fetchall()]
        print(f"\n{old_fqn}" + (f"  ->  {t['new']}" if t["new"] != t["old"] else ""))
        print(f"   source: {t['mart']}  ({n_cols} columns, {n_rows:,} rows)")
        print(f"   friendly-layer rows to update: {len(fl_rows)}")
        plans.append({**t, "key": key, "old_fqn": old_fqn, "new_fqn": new_fqn, "old_ddl": old_ddl,
                      "fl_rows": fl_rows, "n_rows": n_rows})

    print(f"\n{len(plans)} of {len(TARGETS)} views ready.")
    if not args.apply:
        print("DRY RUN -- nothing was changed. Re-run with --apply to execute.")
        return 0

    stamp = f"{dt.date.today():%Y-%m-%d}"
    out = REPO / "outputs" / f"library_view_rollback_reshaped_{stamp}.sql"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n\n".join(
        f"-- {p['old_fqn']}" + (f"\n-- renamed to {p['new_fqn']}: run `alter view {p['new_fqn']} rename to {p['old_fqn']};` first"
                                 if p["new"] != p["old"] else "")
        + f"\n-- FRIENDLY_LAYER before: {json.dumps(p['fl_rows'])}\n{p['old_ddl']}" for p in plans), encoding="utf-8")
    print(f"rollback DDL + friendly-layer before-rows saved to {out}")

    content = json.loads(CONTENT.read_text(encoding="utf-8"))
    fixed = 0
    for p in plans:
        try:
            if p["new"] != p["old"]:
                cur.execute(f"alter view {p['old_fqn']} rename to {p['new_fqn']}")
            cur.execute(f"create or replace view {p['new_fqn']} copy grants comment = '{esc(p['comment'])}' "
                        f"as select * from {p['mart']}")
            for role in READ_ROLES:
                try:
                    cur.execute(f"grant select on view {p['new_fqn']} to role {role}")
                except Exception:  # noqa: BLE001  (role may not exist in this account)
                    pass
            cur.execute(
                """update LIBRARY_META.REGISTRY.FRIENDLY_LAYER
                      set FRIENDLY_NAME = %s, ONE_LINER = %s, COMMENT = %s, LAYER = 'mart',
                          ROW_COUNT = %s, THE_LIBRARY_FQN = %s
                    where LANDING_FQN = %s""",
                (p["new"], p["one_liner"], p["comment"], p["n_rows"],
                 f"THE_LIBRARY.{p['schema']}.{p['new']}", p["key"]))
            for c in content:
                if c["object_fqn"] == p["key"]:
                    c.update(friendly_name=p["new"], one_liner=p["one_liner"], comment=p["comment"])
            cur.execute(f"select * from {p['new_fqn']} limit 1")
            cur.fetchall()
            print(f"   FIXED  {p['new_fqn']}  ({len(cur.description)} columns, opens clean)")
            fixed += 1
        except Exception as e:  # noqa: BLE001
            print(f"   FAILED {p['old_fqn']} -- " + str(e).replace("\n", " ")[:160])
    CONTENT.write_text(json.dumps(content, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{fixed} of {len(plans)} views repaired.")
    return 0 if fixed == len(plans) else 1


if __name__ == "__main__":
    raise SystemExit(main())
