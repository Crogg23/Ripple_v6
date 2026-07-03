"""Workstream B — Ripple Snowflake housekeeping cleanup.

Preview-first (default) / --apply gated. Snapshot BEFORE every drop. Per-step verify.
Reflects Chris's decisions (2026-07-01):
  B1  DROP DATABASE SNOWFLAKE_SAMPLE_DATA            (sample mount; reverse = re-create from share)
  B2  DROP DATABASE SNOWFLAKE_PUBLIC_DATA_PAID       (expired paid trial; reverse = re-subscribe)
  B3  fresh registry backup -> verify -> drop the stale _BAK_20260625
  B5  snapshot + drop 10 one-row dbt stubs + GOVERNMENT_RECORDS__FED_NARA_AAD (9-row degenerate)
      + MART_EPSTEIN_COMPLIANCE_LEDGER (hand-built, snapshot is the ONLY restore path)
      KEEP: CORPORATE_REGISTRY__INTL_ES_BORME (3 rows, thin-but-real)
  B4  no-op (scratch tables are live TRANSIENTs — do NOT drop)

Snapshots land in LIBRARY_MARTS._RESTORE_20260701 (drop that schema once you're confident).
dbt model resurrection is prevented separately in ripple_dbt/dbt_project.yml (+enabled: false).

Usage:
  python scripts/housekeeping_cleanup.py            # preview
  python scripts/housekeeping_cleanup.py --apply    # execute
"""
from __future__ import annotations

import sys
from pathlib import Path

_LIB = Path(__file__).resolve().parents[1] / "library-onboarding"
sys.path.insert(0, str(_LIB))

from snow import connect  # noqa: E402

APPLY = "--apply" in sys.argv
TAG = "20260701"
RESTORE_SCHEMA = f"LIBRARY_MARTS._RESTORE_{TAG}"

# The 10 genuine one-row stubs (auto-detected + asserted against this expected set)
EXPECTED_STUBS = {
    "JUSTICE__FED_FJC_IDB",
    "JUSTICE__FED_DOJ_CRT_CASES",
    "LEGAL_ENFORCEMENT__FED_NAAG_MULTISTATE_SETTLEMENTS",
    "ECONOMICS__INTL_CH_ZEFIX",
    "ECONOMICS__INTL_GR_GEMI",
    "CORPORATE_REGISTRY__INTL_IE_CRO",
    "ECONOMICS__FED_HHS_TAGGS",
    "REGULATION__FED_FDIC_ENFORCEMENT",
    "CIVIL_RIGHTS__FED_NARA_WRA_AAD",
    "HISTORICAL_RECORDS__FED_SLAVEVOYAGES_INTRAAMERICAN",
}
# Explicitly added broken/degenerate marts (schema, table)
EXPLICIT_DROP = [
    ("DBT_CROGERS", "GOVERNMENT_RECORDS__FED_NARA_AAD"),   # 9-row degenerate stub
    ("EPSTEIN", "MART_EPSTEIN_COMPLIANCE_LEDGER"),          # hand-built; snapshot-only reverse
]
KEEP = {"CORPORATE_REGISTRY__INTL_ES_BORME"}                # D3: keep


def rows(cur, sql):
    cur.execute(sql)
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def scalar(cur, sql):
    cur.execute(sql)
    r = cur.fetchone()
    return r[0] if r else None


def do(cur, label, sql, verify=None, expect=None):
    """Print + (if --apply) execute one statement; optional verify query."""
    print(f"\n  [{'APPLY' if APPLY else 'PREVIEW'}] {label}")
    print(f"      SQL: {sql}")
    if not APPLY:
        return
    try:
        cur.execute(sql)
        print("      -> ok")
        if verify is not None:
            got = scalar(cur, verify)
            ok = (got == expect) if expect is not None else bool(got)
            print(f"      -> verify: {verify}  => {got}  {'PASS' if ok else 'FAIL'}")
    except Exception as e:
        print(f"      -> ERROR: {str(e)[:200]}")


def main():
    conn = connect()
    cur = conn.cursor()
    print("=" * 72)
    print(f"HOUSEKEEPING CLEANUP — {'APPLY (executing)' if APPLY else 'PREVIEW (no changes)'}")
    print("=" * 72)

    # -- detect the stub set live (safety: must equal EXPECTED_STUBS) -------
    stubs = rows(cur, """
        SELECT TABLE_SCHEMA, TABLE_NAME, ROW_COUNT
        FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='DBT_CROGERS' AND ROW_COUNT<=1
        ORDER BY TABLE_NAME""")
    found = {s["TABLE_NAME"] for s in stubs}
    print(f"\nAuto-detected 1-row DBT_CROGERS stubs: {len(found)}")
    for s in stubs:
        print(f"   - {s['TABLE_NAME']} (rows={s['ROW_COUNT']})")
    if found != EXPECTED_STUBS:
        print("\n  !! SAFETY ABORT: detected stub set != expected set.")
        print(f"     unexpected extra: {sorted(found - EXPECTED_STUBS)}")
        print(f"     expected missing: {sorted(EXPECTED_STUBS - found)}")
        print("     Review before running. No changes made.")
        return

    drop_targets = [("DBT_CROGERS", n) for n in sorted(found)] + EXPLICIT_DROP
    print(f"\nDROP targets ({len(drop_targets)}): {[t[1] for t in drop_targets]}")
    print(f"KEEP (not touched): {sorted(KEEP)}")

    # -- restore schema ----------------------------------------------------
    print("\n--- restore schema for snapshots ---")
    do(cur, "create restore schema", f"CREATE SCHEMA IF NOT EXISTS {RESTORE_SCHEMA}")

    # -- B5: snapshot + drop broken marts ----------------------------------
    print("\n--- B5: snapshot + drop broken marts ---")
    for sch, tbl in drop_targets:
        src = f"LIBRARY_MARTS.{sch}.{tbl}"
        bak = f"{RESTORE_SCHEMA}.{tbl}"
        do(cur, f"snapshot {tbl}", f"CREATE OR REPLACE TABLE {bak} AS SELECT * FROM {src}")
        do(cur, f"drop {tbl}", f"DROP TABLE IF EXISTS {src}")

    # -- B3: registry backup -> verify -> drop stale -----------------------
    print("\n--- B3: registry backup rotation ---")
    bak_new = f"LIBRARY_META.REGISTRY._SOURCE_REGISTRY_BAK_{TAG}"
    do(cur, "fresh registry backup",
       f"CREATE OR REPLACE TABLE {bak_new} AS SELECT * FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY")
    if APPLY:
        a = scalar(cur, "SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY")
        b = scalar(cur, f"SELECT COUNT(*) FROM {bak_new}")
        print(f"      -> registry={a}  backup={b}  {'PASS' if a == b else 'FAIL'}")
        if a == b:
            do(cur, "drop stale backup",
               "DROP TABLE IF EXISTS LIBRARY_META.REGISTRY._SOURCE_REGISTRY_BAK_20260625")
        else:
            print("      !! count mismatch — keeping stale backup, NOT dropping.")
    else:
        print("      [PREVIEW] would verify counts then DROP _SOURCE_REGISTRY_BAK_20260625")

    # -- B1 / B2: drop the non-Ripple database mounts ----------------------
    print("\n--- B1/B2: drop marketplace/sample mounts ---")
    do(cur, "B1 drop sample-data mount", "DROP DATABASE IF EXISTS SNOWFLAKE_SAMPLE_DATA")
    do(cur, "B2 drop paid-marketplace mount", "DROP DATABASE IF EXISTS SNOWFLAKE_PUBLIC_DATA_PAID")

    # -- B4: no-op ---------------------------------------------------------
    print("\n--- B4: scratch tables — NO ACTION (live TRANSIENTs, do not drop) ---")

    # -- final verify ------------------------------------------------------
    if APPLY:
        print("\n--- post-apply verification ---")
        dbs = [d["name"] for d in rows(cur, "SHOW DATABASES")]
        print(f"   databases now: {dbs}")
        print(f"   SNOWFLAKE_SAMPLE_DATA gone: {'SNOWFLAKE_SAMPLE_DATA' not in dbs}")
        print(f"   SNOWFLAKE_PUBLIC_DATA_PAID gone: {'SNOWFLAKE_PUBLIC_DATA_PAID' not in dbs}")
        left = rows(cur, """SELECT TABLE_NAME FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
                            WHERE TABLE_TYPE='BASE TABLE' AND ROW_COUNT<=1 AND TABLE_SCHEMA<>'_RESTORE_20260701'""")
        print(f"   remaining <=1-row marts (should be 0 or only kept): {[r['TABLE_NAME'] for r in left]}")
        snaps = rows(cur, f"SELECT TABLE_NAME FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='_RESTORE_{TAG}'")
        print(f"   snapshots saved ({len(snaps)}): {[s['TABLE_NAME'] for s in snaps]}")

    print("\nDONE." + ("" if APPLY else "  (preview only — re-run with --apply to execute)"))
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
