#!/usr/bin/env python3
"""GOVERN RECON battery (Move 1 of RIPPLE_GOVERN_THYSELF) — 2026-07-12.

READ-ONLY. Every statement is a SELECT / SHOW / DESC. No DDL, no DML, no --apply.
Runs the warehouse half of the recon that was blocked on 2026-07-12 by dead PATs.

    python3 outputs/govern_recon_battery_2026-07-12.py

Writes outputs/govern_recon_results_2026-07-12.json and prints a summary.
Prereq: a LIVE token in library-onboarding/.env SNOWFLAKE_PAT.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "library-onboarding"))

import snow  # noqa: E402

OUT = REPO / "outputs" / "govern_recon_results_2026-07-12.json"
RESULTS: dict = {}

FROZEN_MARTS = [
    "CORPORATE_REGISTRY__INTL_IE_CRO", "REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS",
    "HISTORY__FED_SLAVEVOYAGES_INTRAAMERICAN", "JUSTICE__FED_NAAG_MULTISTATE_SETTLEMENTS",
    "SPENDING__FED_HHS_TAGGS", "CORPORATE_REGISTRY__INTL_ES_BORME",
    "JUSTICE__FED_DOJ_FCA_SETTLEMENTS",
]


def q(cur, name, sql, max_rows=100):
    """Run one read-only statement; never let one failure kill the battery."""
    try:
        cur.execute(sql)
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchmany(max_rows) if cur.description else []
        RESULTS[name] = {"sql": sql, "columns": cols,
                         "rows": [[str(v) if v is not None else None for v in r] for r in rows]}
        print(f"  ok   {name}  ({len(rows)} rows)")
    except Exception as e:  # noqa: BLE001
        RESULTS[name] = {"sql": sql, "error": str(e).splitlines()[0]}
        print(f"  ERR  {name}: {str(e).splitlines()[0]}")


def main() -> int:
    conn = snow.connect()
    cur = conn.cursor()

    # ── session identity (HARD STOP check: must be ONEAFDA-UMB20733) ──────────
    q(cur, "session", "SELECT CURRENT_ACCOUNT(), CURRENT_ORGANIZATION_NAME(), "
                      "CURRENT_ACCOUNT_NAME(), CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()")

    # ── Move 0 / §9.3: the live PAT population ────────────────────────────────
    q(cur, "pats", "SHOW USER PROGRAMMATIC ACCESS TOKENS")
    q(cur, "resource_monitors", "SHOW RESOURCE MONITORS")
    q(cur, "warehouses", "SHOW WAREHOUSES")
    q(cur, "roles_ripple", "SHOW ROLES LIKE 'RIPPLE%'")

    # ── Move 1 Q1: does LIBRARY_META.BUILD already exist? ─────────────────────
    q(cur, "q1_build_schema", "SHOW SCHEMAS LIKE 'BUILD' IN DATABASE LIBRARY_META")
    q(cur, "q1_build_tables", "SHOW TABLES IN SCHEMA LIBRARY_META.BUILD")  # ERR = doesn't exist; fine

    # ── canonical live state ──────────────────────────────────────────────────
    q(cur, "v_state", "SELECT * FROM LIBRARY_META.REGISTRY.V_STATE")

    # ── §8.1 truth layer ──────────────────────────────────────────────────────
    q(cur, "d1a_lifecycle_vs_rows", """
        WITH t AS (SELECT TABLE_NAME, ROW_COUNT FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
                   WHERE TABLE_SCHEMA='LANDING')
        SELECT COUNT(*) AS landed_total,
               SUM(IFF(t.TABLE_NAME IS NULL,1,0)) AS no_physical_table,
               SUM(IFF(t.ROW_COUNT=0,1,0)) AS zero_rows,
               SUM(IFF(t.ROW_COUNT BETWEEN 1 AND 3,1,0)) AS rows_1_to_3
        FROM LIBRARY_META.REGISTRY.CATALOG c
        LEFT JOIN t ON t.TABLE_NAME = UPPER(c.SOURCE_ID)
        WHERE c.LIFECYCLE IN ('landed','modeled')""")
    q(cur, "d1a_junk_list", """
        WITH t AS (SELECT TABLE_NAME, ROW_COUNT FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
                   WHERE TABLE_SCHEMA='LANDING')
        SELECT c.SOURCE_ID, c.LIFECYCLE, t.ROW_COUNT
        FROM LIBRARY_META.REGISTRY.CATALOG c
        LEFT JOIN t ON t.TABLE_NAME = UPPER(c.SOURCE_ID)
        WHERE c.LIFECYCLE IN ('landed','modeled')
          AND (t.TABLE_NAME IS NULL OR t.ROW_COUNT <= 3)
        ORDER BY c.SOURCE_ID""")
    q(cur, "d1b_fhfa_nmdb", """
        SELECT c.SOURCE_ID, c.LIFECYCLE, t.ROW_COUNT
        FROM LIBRARY_META.REGISTRY.CATALOG c
        LEFT JOIN LIBRARY_RAW.INFORMATION_SCHEMA.TABLES t
          ON t.TABLE_SCHEMA='LANDING' AND t.TABLE_NAME='FED_FHFA_NMDB'
        WHERE c.SOURCE_ID='fed_fhfa_nmdb'""")
    q(cur, "d1c_op2022_catalog",
      "SELECT SOURCE_ID, LIFECYCLE FROM LIBRARY_META.REGISTRY.CATALOG "
      "WHERE SOURCE_ID='fed_cms_open_payments_2022'")
    q(cur, "d1c_op2022_run",
      "SELECT * FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS WHERE RUN_ID='60f19a4a53054596'")
    q(cur, "d1c_op2022_rows",
      "SELECT ROW_COUNT FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES "
      "WHERE TABLE_SCHEMA='LANDING' AND TABLE_NAME='FED_CMS_OPEN_PAYMENTS_2022'")
    q(cur, "d1d_irs_tables",
      "SELECT TABLE_SCHEMA, TABLE_NAME, ROW_COUNT FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES "
      "WHERE TABLE_NAME LIKE '%IRS%BMF%' ORDER BY 1,2")
    q(cur, "d1d_irs_dup_scan", """
        SELECT 'FED_IRS_EO_BMF' AS tbl, COUNT(*) AS n, COUNT(DISTINCT EIN) AS distinct_ein
        FROM LIBRARY_RAW.LANDING.FED_IRS_EO_BMF
        UNION ALL
        SELECT 'FED_IRS_BMF', COUNT(*), COUNT(DISTINCT EIN)
        FROM LIBRARY_RAW.LANDING.FED_IRS_BMF""")

    # ── §8.2 typed layer ──────────────────────────────────────────────────────
    q(cur, "d2a_staging_alltext", """
        SELECT COUNT(*) AS views_total, SUM(IFF(non_text=0,1,0)) AS all_text_views
        FROM (SELECT TABLE_SCHEMA||'.'||TABLE_NAME AS v,
                     SUM(IFF(DATA_TYPE<>'TEXT',1,0)) AS non_text
              FROM LIBRARY_STAGING.INFORMATION_SCHEMA.COLUMNS
              WHERE TABLE_SCHEMA<>'INFORMATION_SCHEMA' GROUP BY 1)""")
    q(cur, "d2b_thelibrary_zerocast", """
        SELECT COUNT(*) AS views_total, SUM(IFF(non_text=0,1,0)) AS zero_cast_views
        FROM (SELECT TABLE_SCHEMA||'.'||TABLE_NAME AS v,
                     SUM(IFF(DATA_TYPE<>'TEXT',1,0)) AS non_text
              FROM THE_LIBRARY.INFORMATION_SCHEMA.COLUMNS
              WHERE TABLE_SCHEMA<>'INFORMATION_SCHEMA' GROUP BY 1)""")
    q(cur, "d2c_unstaged_landed", """
        SELECT COUNT(*) AS landed_modeled,
               SUM(IFF(s.n IS NULL,1,0)) AS unstaged
        FROM LIBRARY_META.REGISTRY.CATALOG c
        LEFT JOIN (SELECT TABLE_NAME, 1 AS n FROM LIBRARY_STAGING.INFORMATION_SCHEMA.VIEWS) s
          ON s.TABLE_NAME LIKE 'STG_' || UPPER(c.SOURCE_ID) || '%'
        WHERE c.LIFECYCLE IN ('landed','modeled')""")

    # ── §8.4 connection graph ─────────────────────────────────────────────────
    q(cur, "d4_connect_tables", 'SHOW TABLES IN SCHEMA LIBRARY_META."CONNECT"')
    q(cur, "d4_connect_views", 'SHOW VIEWS IN SCHEMA LIBRARY_META."CONNECT"')
    q(cur, "d4_edges_columns", 'DESC TABLE LIBRARY_META."CONNECT".CONNECT_EDGES')
    edge_cols = [r[0] for r in RESULTS.get("d4_edges_columns", {}).get("rows", [])]
    tier_col = next((c for c in ("TIER", "CONFIDENCE_TIER", "EDGE_TIER") if c in edge_cols), None)
    key_col = next((c for c in ("JOIN_KEY", "KEY_NAME", "KEY", "MATCH_KEY") if c in edge_cols), None)
    if tier_col:
        q(cur, "d4_edges_by_tier",
          f'SELECT {tier_col}, COUNT(*) AS n FROM LIBRARY_META."CONNECT".CONNECT_EDGES '
          f"GROUP BY 1 ORDER BY 2 DESC")
    if key_col:
        q(cur, "d4_zip_share",
          f"SELECT COUNT(*) AS edges, SUM(IFF({key_col} IN ('ZIP','ZIP5','ZIP_CODE'),1,0)) AS zip_edges "
          f'FROM LIBRARY_META."CONNECT".CONNECT_EDGES')
    q(cur, "d4_v_connections_core_count",
      'SELECT COUNT(*) AS n FROM LIBRARY_META."CONNECT".V_CONNECTIONS_CORE')  # ERR = §9.2 not applied

    # ── §8.5 empty tables ─────────────────────────────────────────────────────
    q(cur, "d5_landing_empties",
      "SELECT COUNT(*) AS tables_total, SUM(IFF(ROW_COUNT=0,1,0)) AS zero_rows, "
      "SUM(IFF(ROW_COUNT BETWEEN 1 AND 3,1,0)) AS rows_1_to_3 "
      "FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='LANDING'")

    # ── §8.6 query traps (spot checks) ────────────────────────────────────────
    q(cur, "d6_open_payments_tables",
      "SELECT TABLE_NAME, ROW_COUNT FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES "
      "WHERE TABLE_SCHEMA='LANDING' AND TABLE_NAME LIKE '%OPEN_PAYMENTS%' ORDER BY 1")
    q(cur, "d6_leie_zero_npi", """
        SELECT COUNT(*) AS n, SUM(IFF(NPI='0000000000',1,0)) AS zero_npi
        FROM LIBRARY_RAW.LANDING.FED_OIG_LEIE""")
    q(cur, "d6_leie_find",
      "SELECT TABLE_NAME, ROW_COUNT FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES "
      "WHERE TABLE_SCHEMA='LANDING' AND TABLE_NAME LIKE '%LEIE%'")
    q(cur, "d6_ofac_sdn_type", """
        SELECT '[' || SDN_TYPE || ']' AS sdn_type_bracketed, COUNT(*) AS n
        FROM LIBRARY_RAW.LANDING.INTL_OFAC_SDN GROUP BY 1 ORDER BY 2 DESC LIMIT 10""")
    q(cur, "d6_ofac_find",
      "SELECT TABLE_NAME, ROW_COUNT FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES "
      "WHERE TABLE_SCHEMA='LANDING' AND (TABLE_NAME LIKE '%OFAC%' OR TABLE_NAME LIKE '%SDN%')")
    q(cur, "d6_ais_find",
      "SELECT TABLE_NAME, ROW_COUNT FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES "
      "WHERE TABLE_SCHEMA='LANDING' AND TABLE_NAME LIKE '%AIS%'")
    q(cur, "d6_ais_daterange",
      "SELECT MIN(BASEDATETIME) AS min_dt, MAX(BASEDATETIME) AS max_dt, COUNT(*) AS n "
      "FROM LIBRARY_RAW.LANDING.FED_NOAA_AIS")

    # ── §8.7 RLIKE anchoring (one-row demo) ───────────────────────────────────
    q(cur, "d7_rlike_demo",
      "SELECT 'catalog' RLIKE 'cat' AS unanchored_matches, "
      "'catalog' RLIKE '.*cat.*' AS anchored_matches")

    # ── §8.8 politics marts in the warehouse ──────────────────────────────────
    q(cur, "d8_politics_marts",
      "SELECT TABLE_SCHEMA, COUNT(*) AS n FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES "
      "WHERE TABLE_NAME ILIKE 'POLITICS__%' GROUP BY 1")

    # ── §8.10 live leads vs the stale overlay ─────────────────────────────────
    q(cur, "d10_leads_columns", 'DESC TABLE LIBRARY_META."CONNECT".LEADS')
    lead_cols = [r[0] for r in RESULTS.get("d10_leads_columns", {}).get("rows", [])]
    rule_col = next((c for c in ("RULE_NAME", "RULE", "JOB", "DETECTOR") if c in lead_cols), None)
    if rule_col:
        q(cur, "d10_leads_by_rule",
          f'SELECT {rule_col}, COUNT(*) AS n FROM LIBRARY_META."CONNECT".LEADS '
          f"GROUP BY 1 ORDER BY 2 DESC")
    if "REVIEW_STATE" in lead_cols:
        q(cur, "d10_leads_by_state",
          'SELECT REVIEW_STATE, COUNT(*) AS n FROM LIBRARY_META."CONNECT".LEADS '
          "GROUP BY 1 ORDER BY 2 DESC")

    # ── §9 apply-state verifies ───────────────────────────────────────────────
    marts = ",".join(f"'{m}'" for m in FROZEN_MARTS)
    q(cur, "a5_frozen_marts_rowcounts",
      f"SELECT TABLE_NAME, ROW_COUNT FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES "
      f"WHERE TABLE_SCHEMA='DBT_CROGERS' AND TABLE_NAME IN ({marts}) ORDER BY 1")
    q(cur, "a6_giant_aggs",
      "SELECT TABLE_NAME, ROW_COUNT FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES "
      "WHERE TABLE_SCHEMA='PUBLIC' AND TABLE_NAME LIKE '%_AGG' ORDER BY 1")
    q(cur, "a8_join_keys_provisional",
      "SELECT COUNT(*) AS landed_modeled, "
      "SUM(IFF(TO_BOOLEAN(JOIN_KEY_TIER_PROVISIONAL),1,0)) AS still_provisional "
      "FROM LIBRARY_META.REGISTRY.CATALOG WHERE LIFECYCLE IN ('landed','modeled')")

    # ── Move 1 Q4: the calibrated ladder as persisted ─────────────────────────
    q(cur, "match_model", 'SELECT * FROM LIBRARY_META."CONNECT".MATCH_MODEL')
    q(cur, "match_rungs", 'SELECT * FROM LIBRARY_META."CONNECT".MATCH_RUNGS')

    conn.close()
    OUT.write_text(json.dumps(RESULTS, indent=2))
    errs = sum(1 for v in RESULTS.values() if "error" in v)
    print(f"\nwrote {OUT}  ({len(RESULTS)} checks, {errs} errored)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
