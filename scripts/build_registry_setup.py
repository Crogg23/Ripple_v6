#!/usr/bin/env python3
"""Create + seed LIBRARY_META.BUILD — Ripple's state about itself, as data.

Move 2 of RIPPLE_GOVERN_THYSELF (2026-07-12). V_STATE governs the data;
BUILD.V_BUILD_STATE governs the build. Four tables:

  DEFECTS          every defect carries EVIDENCE_SQL: rows>0 = still broken, 0 = clear
  PENDING_ACTIONS  §9 with the dependency graph explicit; VERIFY_SQL: rows>0 = it worked
  PARKED           §12, so an idea can be marked already_done instead of rotting
  POLICY           durable decisions + permanent data traps (append-only, latest wins)

Seed data = the verified GOVERN_RECON_2026-07-12 findings, NOT the prose of any doc.

    python3 scripts/build_registry_setup.py            # PREVIEW: DDL summary + every
                                                       # seed row + LIVE verification
                                                       # of each defect (read-only)
    python3 scripts/build_registry_setup.py --apply    # create schema/tables/view +
                                                       # MERGE-seed (idempotent)

Apply is idempotent and NEVER clobbers human state: on existing rows it updates
descriptions/evidence but leaves STATUS, CLOSED_*, APPLIED_* untouched.

Run --apply yourself — the agent's classifier blocks shared-infra writes.
NEEDS A WRITE-CAPABLE TOKEN (CREATE SCHEMA on LIBRARY_META): the READER PAT
cannot apply this. Preview runs fine on the reader lane.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "library-onboarding"))
sys.path.insert(0, str(REPO / "scripts"))

from verify_defects import FS_CHECKS, exec_evidence  # noqa: E402

RECON = "GOVERN_RECON_2026-07-12"
AUDIT = "FABLE_AUDIT_2026-07-06"


def did(area: str, title: str) -> str:
    return hashlib.md5(f"{area}|{title}".encode()).hexdigest()


# ── DDL (exactly the govern-brief spec; COPY GRANTS is doctrine) ─────────────
DDL = [
    ("schema BUILD", """CREATE SCHEMA IF NOT EXISTS LIBRARY_META.BUILD
        COMMENT = 'Ripple''s state about itself. V_STATE is for the data; this is for the build.'"""),
    ("table DEFECTS", """CREATE TABLE IF NOT EXISTS LIBRARY_META.BUILD.DEFECTS (
        DEFECT_ID        VARCHAR       NOT NULL,
        TITLE            VARCHAR       NOT NULL,
        AREA             VARCHAR       NOT NULL,
        SEVERITY         VARCHAR       NOT NULL,
        DESCRIPTION      VARCHAR,
        VERIFY_METHOD    VARCHAR       DEFAULT 'sql',
        EVIDENCE_SQL     VARCHAR,
        SOURCE_AUDIT     VARCHAR,
        FOUND_AT         TIMESTAMP_NTZ,
        STATUS           VARCHAR       DEFAULT 'open',
        LAST_VERIFIED_AT TIMESTAMP_NTZ,
        LAST_VERDICT     VARCHAR,
        LAST_ROWCOUNT    NUMBER,
        CLOSED_AT        TIMESTAMP_NTZ,
        CLOSED_BY        VARCHAR,
        NOTES            VARCHAR,
        PRIMARY KEY (DEFECT_ID))"""),
    ("table PENDING_ACTIONS", """CREATE TABLE IF NOT EXISTS LIBRARY_META.BUILD.PENDING_ACTIONS (
        ACTION_ID      VARCHAR       NOT NULL,
        SEQ            NUMBER,
        SCRIPT_PATH    VARCHAR       NOT NULL,
        DESCRIPTION    VARCHAR,
        DEPENDS_ON     VARCHAR,
        REVERSIBLE     BOOLEAN       DEFAULT TRUE,
        REQUIRES_HUMAN BOOLEAN       DEFAULT FALSE,
        STATUS         VARCHAR       DEFAULT 'pending',
        PREVIEWED_AT   TIMESTAMP_NTZ,
        APPLIED_AT     TIMESTAMP_NTZ,
        APPLIED_BY     VARCHAR,
        VERIFY_SQL     VARCHAR,
        NOTES          VARCHAR,
        PRIMARY KEY (ACTION_ID))"""),
    ("table PARKED", """CREATE TABLE IF NOT EXISTS LIBRARY_META.BUILD.PARKED (
        PARKED_ID     VARCHAR        NOT NULL,
        TITLE         VARCHAR        NOT NULL,
        HEAT          VARCHAR        DEFAULT 'someday',
        NOTE          VARCHAR,
        RAISED_AT     TIMESTAMP_NTZ,
        STATUS        VARCHAR        DEFAULT 'parked',
        SUPERSEDED_BY VARCHAR,
        PRIMARY KEY (PARKED_ID))"""),
    ("table POLICY", """CREATE TABLE IF NOT EXISTS LIBRARY_META.BUILD.POLICY (
        POLICY_KEY    VARCHAR        NOT NULL,
        STATEMENT     VARCHAR        NOT NULL,
        RATIONALE     VARCHAR,
        DECIDED_AT    TIMESTAMP_NTZ,
        STATUS        VARCHAR        DEFAULT 'active',
        SUPERSEDED_BY VARCHAR,
        RECORDED_AT   TIMESTAMP_NTZ  DEFAULT CURRENT_TIMESTAMP())"""),
    ("view V_BUILD_STATE", """CREATE OR REPLACE VIEW LIBRARY_META.BUILD.V_BUILD_STATE
        COPY GRANTS AS
        SELECT 'defects_open' AS METRIC, COUNT(*) AS VALUE
          FROM LIBRARY_META.BUILD.DEFECTS WHERE STATUS = 'open'
        UNION ALL SELECT 'defects_blocker', COUNT(*)
          FROM LIBRARY_META.BUILD.DEFECTS WHERE STATUS='open' AND SEVERITY='blocker'
        UNION ALL SELECT 'defects_unverified_7d', COUNT(*)
          FROM LIBRARY_META.BUILD.DEFECTS
          WHERE STATUS='open'
            AND (LAST_VERIFIED_AT IS NULL OR LAST_VERIFIED_AT < DATEADD('day', -7, CURRENT_TIMESTAMP()))
        UNION ALL SELECT 'actions_pending', COUNT(*)
          FROM LIBRARY_META.BUILD.PENDING_ACTIONS WHERE STATUS IN ('pending','previewed')
        UNION ALL SELECT 'actions_irreversible_pending', COUNT(*)
          FROM LIBRARY_META.BUILD.PENDING_ACTIONS
          WHERE STATUS IN ('pending','previewed') AND REVERSIBLE = FALSE
        UNION ALL SELECT 'parked_hot', COUNT(*)
          FROM LIBRARY_META.BUILD.PARKED WHERE STATUS='parked' AND HEAT='hot'"""),
    # read lanes: RIPPLE_READER already inherits via FUTURE grants on LIBRARY_META;
    # these are explicit + idempotent so the MCP lane sees BUILD too.
    ("grant usage reader", "GRANT USAGE ON SCHEMA LIBRARY_META.BUILD TO ROLE RIPPLE_READER"),
    ("grant select reader", "GRANT SELECT ON ALL TABLES IN SCHEMA LIBRARY_META.BUILD TO ROLE RIPPLE_READER"),
    ("grant select reader views", "GRANT SELECT ON ALL VIEWS IN SCHEMA LIBRARY_META.BUILD TO ROLE RIPPLE_READER"),
    ("grant usage mcp", "GRANT USAGE ON SCHEMA LIBRARY_META.BUILD TO ROLE CLAUDE_MCP_READONLY"),
    ("grant select mcp", "GRANT SELECT ON ALL TABLES IN SCHEMA LIBRARY_META.BUILD TO ROLE CLAUDE_MCP_READONLY"),
    ("grant select mcp views", "GRANT SELECT ON ALL VIEWS IN SCHEMA LIBRARY_META.BUILD TO ROLE CLAUDE_MCP_READONLY"),
]


# ── DEFECTS seed — every row verified live in GOVERN_RECON_2026-07-12 ───────
# EVIDENCE_SQL convention: returns rows WHILE BROKEN, zero rows when fixed.
# Rows the recon already measured as fixed are seeded OPEN on purpose: the
# verifier will say 'clear' and Chris closes them — that loop is the product.

DEFECTS = [
    dict(area="truth_layer", severity="high", found=AUDIT,
         title="OP-2022 load mislogged: 13.25M rows live, ledger says error/0",
         desc="Run 60f19a4a53054596 logged error/0 after an EOF crash post-write; "
              "catalog lifecycle 'failed' despite 13,250,000 physical rows. Fix = action A01.",
         sql="SELECT r.RUN_ID FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS r "
             "JOIN LIBRARY_RAW.INFORMATION_SCHEMA.TABLES t "
             "  ON t.TABLE_SCHEMA='LANDING' AND t.TABLE_NAME='FED_CMS_OPEN_PAYMENTS_2022' "
             "WHERE r.RUN_ID='60f19a4a53054596' AND r.STATUS='error' AND t.ROW_COUNT > 1000000"),
    dict(area="truth_layer", severity="high", found=AUDIT,
         title="FED_IRS_EO_BMF is an exact 2x duplicate of FED_IRS_BMF",
         desc="3,949,660 rows / 1,974,830 distinct EIN vs 1,974,830/1,974,830 — ratio exactly "
              "2.00, verified live 2026-07-12. Clears when quarantined to LIBRARY_RAW.RETIRED "
              "(action A04). Also kills the PARKED 'pour IRS EO BMF' idea: already_done.",
         sql="SELECT TABLE_NAME FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES "
             "WHERE TABLE_SCHEMA='LANDING' AND TABLE_NAME='FED_IRS_EO_BMF'"),
    dict(area="truth_layer", severity="medium", found=AUDIT,
         title="landed/modeled sources whose landing table holds <=3 rows",
         desc="Was ~31 at audit; 8 at recon (cdc_wonder, cms_hpt_mrf, doj_crt_cases, fbi_cde, "
              "fincen_boi, fra_safety, austlii, ge_datagov — all 1 row, all 'landed').",
         sql="SELECT c.SOURCE_ID FROM LIBRARY_META.REGISTRY.CATALOG c "
             "JOIN LIBRARY_RAW.INFORMATION_SCHEMA.TABLES t "
             "  ON t.TABLE_SCHEMA='LANDING' AND t.TABLE_NAME=UPPER(c.SOURCE_ID) "
             "WHERE c.LIFECYCLE IN ('landed','modeled') AND t.ROW_COUNT <= 3"),
    dict(area="truth_layer", severity="medium", found=AUDIT,
         title="FED_FHFA_NMDB (19M rows) misgraded in catalog lifecycle",
         desc="Audit found it 'sampled'. Recon measured lifecycle=landed with 19,054,246 rows — "
              "expect verdict CLEAR; close it and the loop is proven.",
         sql="SELECT c.SOURCE_ID FROM LIBRARY_META.REGISTRY.CATALOG c "
             "WHERE c.SOURCE_ID='fed_fhfa_nmdb' AND c.LIFECYCLE NOT IN ('landed','modeled')"),
    dict(area="truth_layer", severity="high", found="RIPPLE_GOVERN_THYSELF brief 2026-07-12",
         title="build-state.md is hand-typed, not generated",
         desc="1,629 hand-typed lines, no PK/refresh/updated-at; header 5 days stale at recon. "
              "Clears when gen_build_state.py owns the file (Move 3).",
         method="filesystem"),
    dict(area="typing", severity="medium", found=AUDIT,
         title="staging views that are 100% TEXT",
         desc="819 of 1,033 at recon (audit: 789). Zero may be unreachable; the trend is the "
              "signal — LAST_ROWCOUNT should only ever fall.",
         sql="SELECT v FROM (SELECT TABLE_SCHEMA||'.'||TABLE_NAME AS v, "
             "SUM(IFF(DATA_TYPE<>'TEXT',1,0)) AS nt FROM LIBRARY_STAGING.INFORMATION_SCHEMA.COLUMNS "
             "WHERE TABLE_SCHEMA<>'INFORMATION_SCHEMA' GROUP BY 1) WHERE nt=0"),
    dict(area="typing", severity="low", found=AUDIT,
         title="THE_LIBRARY reading-room views still zero-cast",
         desc="Audit: 171/233. Recon: 3/233 — the typed pass measurably landed (unrecorded?). "
              "Three stragglers left; close or wontfix is Chris's call.",
         sql="SELECT v FROM (SELECT TABLE_SCHEMA||'.'||TABLE_NAME AS v, "
             "SUM(IFF(DATA_TYPE<>'TEXT',1,0)) AS nt FROM THE_LIBRARY.INFORMATION_SCHEMA.COLUMNS "
             "WHERE TABLE_SCHEMA<>'INFORMATION_SCHEMA' GROUP BY 1) WHERE nt=0"),
    dict(area="typing", severity="medium", found=AUDIT,
         title="landed/modeled sources with no staging view at all",
         desc="99 of 199 at recon (audit: 95/199).",
         sql="SELECT c.SOURCE_ID FROM LIBRARY_META.REGISTRY.CATALOG c "
             "WHERE c.LIFECYCLE IN ('landed','modeled') AND NOT EXISTS "
             "(SELECT 1 FROM LIBRARY_STAGING.INFORMATION_SCHEMA.VIEWS s "
             " WHERE s.TABLE_NAME LIKE 'STG_'||UPPER(c.SOURCE_ID)||'%')"),
    dict(area="creds", severity="blocker", found=RECON,
         title="leaked/unrestricted ACCOUNTADMIN PATs still ACTIVE",
         desc="THE_LIBRARY (the 07-05 token pasted in a public chat) and Ripple_v6 (no role "
              "restriction) both ACTIVE at recon. Revoke in Snowsight (action A03 after list "
              "refresh, or manually). Any one of these is DROP DATABASE from anyone's laptop.",
         sql="SHOW USER PROGRAMMATIC ACCESS TOKENS; "
             "SELECT \"name\" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) "
             "WHERE \"name\" IN ('THE_LIBRARY','Ripple_v6') AND \"status\"='ACTIVE'"),
    dict(area="creds", severity="high", found=RECON,
         title="no scoped write lane exists (reader-only PAT)",
         desc="Every catalog/warehouse apply is gated on a write-capable token. Roles already "
              "exist (RIPPLE_INGEST_RW, RIPPLE_TRANSFORM_RW) — mint a PAT against one, never "
              "ACCOUNTADMIN. Clears when such a token exists.",
         sql="SHOW USER PROGRAMMATIC ACCESS TOKENS; "
             "SELECT 1 AS broken WHERE NOT EXISTS ("
             "SELECT 1 FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) "
             "WHERE \"role_restriction\" IN ('RIPPLE_INGEST_RW','RIPPLE_TRANSFORM_RW') "
             "AND \"status\"='ACTIVE')"),
    dict(area="creds", severity="medium", found="env rewrite 2026-07-05",
         title="source API keys still missing from .env",
         desc="CENSUS_API_KEY, COURTLISTENER_TOKEN, SOCRATA_APP_TOKEN, RIPPLE_CONTACT_UA — "
              "dropped in the 07-05 accidental rewrite, never restored. RIPPLE_CONTACT_UA is "
              "the one-line SEC-EDGAR/CIK unblock.",
         method="filesystem"),
    dict(area="creds", severity="medium", found=RECON,
         title="keys_ledger.json does not track the live PAT population",
         desc="Ledger PAT row points at LIBRARY_PAT's expiry, knows nothing of READER; 'updated' "
              "frozen at 2026-07-02. Clears when the programmatic_access_tokens section lands "
              "(revoke script's --apply writes it).",
         method="filesystem"),
    dict(area="creds", severity="high", found=RECON,
         title="evidence.dev read lane is dark (dead interim token)",
         desc="connection.options.yaml holds a revoked token; connection.yaml is still the "
              "INTERIM (ACCOUNTADMIN) variant. Fix = the connection.yaml.serve swap with the "
              "READER token + SNOWFLAKE_SERVE_PAT in .env (action A11).",
         method="filesystem"),
    dict(area="graph", severity="medium", found=AUDIT,
         title="V_CONNECTIONS_CORE (trustworthy-core view) does not exist",
         desc="Core tiers (STEEL+STRONG+CORROBORATED) sum to exactly 4,308 edges at recon. "
              "Fix = action A02.",
         sql="SELECT 1 AS broken WHERE NOT EXISTS ("
             "SELECT 1 FROM LIBRARY_META.INFORMATION_SCHEMA.VIEWS "
             "WHERE TABLE_SCHEMA='CONNECT' AND TABLE_NAME='V_CONNECTIONS_CORE')"),
    dict(area="loader", severity="medium", found=AUDIT,
         title="append-mode loaders leave silent partial loads on crash",
         desc="noaa_ais_backfill.py / noaa_storm_events_backfill.py admit it in their own "
              "docstrings ('a mid-run crash leaves a partial day/year'). Clears when the "
              "docstring marker goes away because the checkpointing is actually fixed.",
         method="filesystem"),
    dict(area="viz", severity="low", found=AUDIT,
         title="leads_overlay.html stale (4 detectors/353 leads vs live 6/1030)",
         desc="Rendered Jun 27; live system has 6 detectors / 1,030 active leads (V_STATE). "
              "Re-render before showing anyone.",
         method="filesystem"),
    dict(area="viz", severity="low", found=AUDIT,
         title="explorer/overlay HTML pull Plotly from CDN, die offline",
         desc="Vendored outputs/plotly.min.js (4.8MB) sits beside them, unwired.",
         method="filesystem"),
    dict(area="loader", severity="high", found=RECON,
         title="resolve.py PAIRS spec broken by NPPES re-land (column rename)",
         desc="FED_CMS_NPPES now has PROVIDER_LAST_NAME_LEGAL_NAME (single underscore); "
              "connect/resolve.py:55 still says PROVIDER_LAST_NAME__LEGAL_NAME — connect "
              "resolve AND calibrate die on 'invalid identifier' until the one-line fix. "
              "Found 2026-07-12 building the ladder fixture (which patched it locally). "
              "Bigger lesson: any re-land can silently rename columns under dependent code.",
         method="filesystem"),
    dict(area="ci", severity="high", found="RIPPLE_GOVERN_THYSELF brief 2026-07-12",
         title="no ladder regression tests (5 named gaps, no holdout fixture)",
         desc="~73 connect tests exist but none cover: auto-merge-unreachable, NPI leakage, "
              "calibrated precision band, blocking recall, end-to-end published() refusal. "
              "tests/fixtures/ladder_holdout.parquet does not exist. Clears when Move 4 ships "
              "tests/test_ladder_invariants.py + the fixture.",
         method="filesystem"),
    dict(area="politics", severity="medium", found="politics audit 2026-06-30",
         title="politics marts clobberable by selector-less dbt build",
         desc="24 POLITICS__* tables in LIBRARY_MARTS.POLITICS mirror Python-built canonical "
              "tables; only convention prevents a bare 'dbt build' from clobbering them. "
              "Needs eyes on whatever guard gets designed — no query can prove absence.",
         method="human"),
    dict(area="leads", severity="medium", found="READING_ROOM build 2026-07-12",
         title="banned_but_operating source table dropped; 11 leads' receipts irreproducible",
         desc="FED_CMS_FACILITY_AFFILIATION is gone from LIBRARY_RAW.LANDING (verified live "
              "2026-07-12), so the 11 active banned_but_operating leads' stored COMPILED_SQL "
              "fails with 'does not exist'. The leads stand (hard-NPI joins at detect time, "
              "facility evidence frozen in EVIDENCE) but cannot be re-run. Clears when the "
              "roster table is re-landed or the rule is re-pointed at a live source.",
         sql="SELECT 1 AS broken WHERE NOT EXISTS (SELECT 1 FROM "
             "LIBRARY_RAW.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='LANDING' "
             "AND TABLE_NAME='FED_CMS_FACILITY_AFFILIATION')"),
    dict(area="truth_layer", severity="medium", found="READING_ROOM build 2026-07-12",
         title="FED_SAM_EXCLUSIONS holds exactly 1,000 rows (suspected capped sample load)",
         desc="A suspiciously round count for a file that runs ~100k+ rows at the source; "
              "debarred_but_funded breadth is a floor, and ACTIVATION_DATE is blank on every "
              "row so no debarment-date timeline is possible. Clears when SAM lands fully.",
         sql="SELECT TABLE_NAME FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES "
             "WHERE TABLE_SCHEMA='LANDING' AND TABLE_NAME='FED_SAM_EXCLUSIONS' "
             "AND ROW_COUNT = 1000"),
    dict(area="leads", severity="medium", found="READING_ROOM build 2026-07-12",
         title="tripwire: CONNECT.DECISIONS resurrected by a stale checkout",
         desc="Decisions moved to LIBRARY_META.REVIEW.DECISIONS (Reading Room, A14) and the "
              "old stub was retired by rename. A machine on a pre-repoint checkout would "
              "silently recreate CONNECT.DECISIONS via safety.ensure() and write verdicts "
              "nobody reads (V_LEADS_PUBLISHED/V_STATE/panel all read REVIEW). This defect "
              "fires only if that happens; while REVIEW.DECISIONS doesn't exist yet (A14 "
              "pending) the pre-move stub is expected and this also fires — apply A14.",
         sql="SELECT 1 AS broken FROM LIBRARY_META.INFORMATION_SCHEMA.TABLES "
             "WHERE TABLE_SCHEMA='CONNECT' AND TABLE_NAME='DECISIONS'"),
    dict(area="leads", severity="medium", found="READING_ROOM build 2026-07-12",
         title="V_LEADS_PUBLISHED lacks the receipt columns (view predates LEADS ALTERs)",
         desc="The safe view was created 2026-07-03 with l.*; COMPILED_SQL / SQL_SHA256 / "
              "AS_OF_DATE / SOURCE_SNAPSHOTS were ALTER-added to LEADS later, and a view's "
              "star-list freezes at creation — so the enforced read lane cannot serve "
              "receipts and the LEAD_QUEUE mart is blocked. Fix = action A12.",
         sql="SELECT 1 AS broken WHERE NOT EXISTS (SELECT 1 FROM "
             "LIBRARY_META.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='CONNECT' "
             "AND TABLE_NAME='V_LEADS_PUBLISHED' AND COLUMN_NAME='COMPILED_SQL')"),
]


# ── PENDING_ACTIONS seed — §9, re-verified 2026-07-12 ────────────────────────
# VERIFY_SQL convention: returns rows AFTER the action worked, zero before.

ACTIONS = [
    dict(id="A00", seq=0, path="(Snowsight, manual)", human=True, reversible=True,
         desc="Mint the scoped WRITE PAT (RIPPLE_INGEST_RW or RIPPLE_TRANSFORM_RW, never "
              "ACCOUNTADMIN). Unblocks every --apply below. Companion to the READER mint of 07-12.",
         verify="SHOW USER PROGRAMMATIC ACCESS TOKENS; "
                "SELECT 1 FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) "
                "WHERE \"role_restriction\" IN ('RIPPLE_INGEST_RW','RIPPLE_TRANSFORM_RW') "
                "AND \"status\"='ACTIVE'"),
    dict(id="A01", seq=1, path="scripts/reconcile_op2022.py", depends="A00",
         desc="Flip run 60f19a4a53054596 error/0 -> success/13,250,000; registry upsert. "
              "13.25M Open Payments 2022 rows go live.",
         verify="SELECT 1 FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS "
                "WHERE RUN_ID='60f19a4a53054596' AND STATUS='success'"),
    dict(id="A02", seq=2, path="scripts/build_v_connections_core.py", depends="A00",
         desc="Create the trustworthy-core view (STEEL+STRONG+CORROBORATED = 4,308 edges at recon).",
         verify="SELECT 1 FROM LIBRARY_META.INFORMATION_SCHEMA.VIEWS "
                "WHERE TABLE_SCHEMA='CONNECT' AND TABLE_NAME='V_CONNECTIONS_CORE'"),
    dict(id="A03", seq=3, path="scripts/revoke_straggler_pats.py", depends="A00",
         human=True, reversible=False,
         desc="STALE AS WRITTEN — will fail-safe ABORT: DROP target LIBRARY_CLAUDE_PAT no longer "
              "exists and KEEP list doesn't know READER. Refresh lists, re-preview, then run "
              "manually. Targets still live: Ripple_v6, THE_LIBRARY, ripple_loader, RIPPLE_LOADER_PAT2.",
         verify="SHOW USER PROGRAMMATIC ACCESS TOKENS; "
                "SELECT 1 AS worked WHERE NOT EXISTS ("
                "SELECT 1 FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) WHERE \"name\" IN "
                "('Ripple_v6','THE_LIBRARY','ripple_loader','RIPPLE_LOADER_PAT2'))"),
    dict(id="A04", seq=4, path="scripts/dedup_irs_eo_bmf.py", depends="A01,A02",
         desc="Quarantine the 2x duplicate to LIBRARY_RAW.RETIRED (rename, never delete); "
              "--prune-edges drops its redundant graph edges. Mark PARKED 'pour IRS EO BMF' "
              "already_done when this lands.",
         verify="SELECT 1 FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES "
                "WHERE TABLE_SCHEMA='RETIRED' AND TABLE_NAME='FED_IRS_EO_BMF'"),
    dict(id="A05", seq=5, path="scripts/rebuild_frozen_marts.py", depends="A04",
         desc="RE-PREVIEW MANDATORY: of its 7 targets only 3 still exist (BORME=3 rows frozen, "
              "FCA=12 frozen, FED_REGISTER=5000); CRO survives only in _RESTORE_20260701; "
              "SLAVEVOYAGES/NAAG/TAGGS were dropped 07-01 and never rebuilt.",
         verify="SELECT 1 FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES "
                "WHERE TABLE_SCHEMA='DBT_CROGERS' "
                "AND TABLE_NAME='CORPORATE_REGISTRY__INTL_ES_BORME' AND ROW_COUNT > 3"),
    dict(id="A06", seq=6, path="scripts/build_giant_aggs.py", depends="A05",
         desc="14 pre-aggregated marts (<100k rows) in LIBRARY_MARTS.PUBLIC for the too-big tables. "
              "Zero %_AGG tables exist at recon.",
         verify="SELECT COUNT(*) FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES "
                "WHERE TABLE_SCHEMA='PUBLIC' AND TABLE_NAME LIKE '%_AGG' HAVING COUNT(*) >= 10"),
    dict(id="A07", seq=7, path="scripts/thelibrary_inventory.py && scripts/thelibrary_build.py --typed",
         depends="A06",
         desc="LIKELY ALREADY DONE: recon measured 230/233 reading-room views typed (audit had "
              "62/233). Chris: confirm whether you applied the 07-07 typed plan; if so flip this "
              "row applied with the real date.",
         verify="SELECT COUNT(*) FROM (SELECT TABLE_SCHEMA||'.'||TABLE_NAME AS v, "
                "SUM(IFF(DATA_TYPE<>'TEXT',1,0)) AS nt FROM THE_LIBRARY.INFORMATION_SCHEMA.COLUMNS "
                "WHERE TABLE_SCHEMA<>'INFORMATION_SCHEMA' GROUP BY 1) WHERE nt=0 "
                # <=10, amended from <=5 on 2026-07-12: the 6 zero-cast survivors are
                # identifier/crosswalk tables (FEC IDs, ZIP->county) that are correctly
                # all-TEXT — casting IDs/ZIPs is the bug the typing heuristics avoid.
                "HAVING COUNT(*) <= 10"),
    dict(id="A08", seq=8, path="scripts/backfill_join_keys_std.py", depends="A07",
         desc="Measure real join keys for the provisional sources (142 of 199 landed/modeled "
              "still provisional at recon — the exact figure the script was written against).",
         verify="SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.CATALOG "
                "WHERE LIFECYCLE IN ('landed','modeled') "
                "AND TO_BOOLEAN(JOIN_KEY_TIER_PROVISIONAL) HAVING COUNT(*) < 100"),
    dict(id="A09", seq=9, path="scripts/gen_evidence_pages.py", depends="A07,A08,A11",
         desc="226 evidence.dev pages. Deliberately last; also gated on the read-lane swap (A11) "
              "or the pages template against a dark lane. Verify is filesystem (evidence/pages/ "
              "count), not SQL.",
         verify=None),
    dict(id="A10", seq=10, path="scripts/regrade_empty_loads.py", depends="A00",
         desc="Lower priority, correct but slow (from §9's ALSO-PENDING list).", verify=None),
    dict(id="A11", seq=11, path="evidence/sources/library/connection.yaml.serve (manual swap)",
         human=True, depends="A00",
         desc="Move evidence.dev onto the enforced read lane: READER token as SNOWFLAKE_SERVE_PAT "
              "+ connection.options.yaml, cp connection.yaml.serve -> connection.yaml, "
              "npm run sources to confirm. Un-darks the reading room.",
         verify=None),
    dict(id="A12", seq=12, path="scripts/refresh_v_leads_published.sql (Snowsight, manual)",
         human=True,
         desc="Recreate V_LEADS_PUBLISHED with COPY GRANTS — same published() semantics, but "
              "the star-list now picks up the receipt columns ALTER-added to LEADS after the "
              "view's 2026-07-03 creation. Unblocks the LEAD_QUEUE mart's evidence_sql and "
              "the evidence smoke test. Idempotent; no new privileges granted.",
         verify="SELECT 1 FROM LIBRARY_META.INFORMATION_SCHEMA.COLUMNS "
                "WHERE TABLE_SCHEMA='CONNECT' AND TABLE_NAME='V_LEADS_PUBLISHED' "
                "AND COLUMN_NAME='COMPILED_SQL'"),
    dict(id="A13", seq=13,
         path="dbt build --select marts.review (library-onboarding/ripple_dbt)",
         depends="A00,A12",
         desc="Materialize the Reading Room LEAD_QUEUE mart + its full test battery "
              "(reconciliation, headline guards, total-order, receipt parity, evidence smoke). "
              "SELECTOR IS MANDATORY (policy no_selectorless_dbt_build).",
         verify="SELECT 1 FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES "
                "WHERE TABLE_SCHEMA='DBT_CROGERS' AND TABLE_NAME='LEAD_QUEUE' "
                "AND ROW_COUNT > 0"),
    dict(id="A14", seq=14, path="scripts/provision_review_lane.sql (Snowsight, manual)",
         human=True,
         desc="Provision the Reading Room write lane: LIBRARY_META.REVIEW.DECISIONS "
              "(append-only by grant design), role RIPPLE_REVIEW_WRITER (INSERT+SELECT on "
              "that one table, nothing else), V_LATEST_DECISIONS, and the consumer "
              "re-points (V_LEADS_PUBLISHED + V_STATE now read REVIEW.DECISIONS; "
              "SUPERSEDES A12's view refresh if not yet run). Then mint RIPPLE_REVIEW_PAT "
              "scoped to that role and prove the wall with scripts/verify_review_lane.sql "
              "(its two PERMISSION DENIEDs are the point).",
         verify="SELECT 1 FROM LIBRARY_META.INFORMATION_SCHEMA.TABLES "
                "WHERE TABLE_SCHEMA='REVIEW' AND TABLE_NAME='DECISIONS'"),
]


# ── PARKED seed — §12, with the rotted one resolved ──────────────────────────

PARKED = [
    dict(title="Pour IRS EO BMF (1.97M nonprofit EINs)", heat="someday", status="already_done",
         superseded="defect 'FED_IRS_EO_BMF is an exact 2x duplicate' + action A04",
         note="THE brief's founding receipt: the EINs are already in the Library — twice. "
              "Landed as FED_IRS_BMF (1,974,830 EINs). This idea rotted in §12 while §8 knew better."),
    dict(title="Tier-aware bridge dedup (weak GEO edge suppresses strong CCN->NPI bridge)", heat="hot",
         note="Fix: only dedup against equal-or-stronger-tier direct edges."),
    dict(title="Per-watchlist FANOUT_MAX relax for small curated watchlists", heat="hot",
         note="FANOUT_MAX=40 kills junk but drops legit hospital->banned-provider hops (LEIE 8,775 NPIs)."),
    dict(title="Materialize connect__banned_but_operating as a dbt mart", heat="hot",
         note="First shippable story from the connected Library (crosswalk x LEIE)."),
    dict(title="Land one new identifier (EIN wired, or CIK via User-Agent fix)", heat="hot",
         note="Breaks the 75%-of-leads-on-one-edge concentration. EIN is LANDED (see already_done "
              "row) but not wired into detectors; CIK needs RIPPLE_CONTACT_UA in .env first."),
    dict(title="Structurally exclude bare ZIP/FIPS edges from the graph (design call)", heat="someday",
         note="52.2% of edges are ZIP-key at recon. OUT OF SCOPE for the govern brief — "
              "recorded so it stops living in prose."),
    dict(title="Central sources.yml instead of per-model sources blocks", heat="someday", note="Cosmetic."),
    dict(title="dbt deprecation sweep (148 generic-test-arg + 57 severity warnings)", heat="someday",
         note="Become errors on a future dbt major bump."),
    dict(title="Wire the Library Map as 'ripple map' so it self-refreshes", heat="someday", note=None),
    dict(title="Hide raw-vs-cleaned duplicate objects in the Reading Room", heat="someday",
         note="Ugly collision-suffixed names when both exist."),
    dict(title="Vendor Plotly locally in explorer/overlay HTML", heat="someday",
         note="Tracked as an open viz defect too; file already on disk, just unwired."),
    dict(title="Sketch EIN/NAICS/DOCKET/ZIP detector templates", heat="someday",
         note="Design-brief open call; engineering templates only, no new detectors built."),
]


# ── POLICY seed — durable decisions + permanent data traps ───────────────────

POLICY = [
    dict(key="preview_then_apply",
         stmt="Every warehouse/catalog mutation ships as a preview-by-default script with --apply. "
              "The agent never executes DDL/DML against shared infra directly.",
         why="Foreman model; classifier-enforced since 2026-06.", decided="2026-06-25"),
    dict(key="agent_never_closes_defects",
         stmt="The verifier reports still_broken/clear; only a human sets STATUS/CLOSED_BY on a defect.",
         why="Fact-vs-lead applied to the build; a 'clear' is a recommendation, not a fact.",
         decided="2026-07-12"),
    dict(key="v_state_numbers_only",
         stmt="Scale numbers are quoted only from V_STATE (data) / V_BUILD_STATE (build) or a live "
              "query. Prose numbers rot and are untrusted, including in this table.",
         why="Every audited doc disagreed with the warehouse within days.", decided="2026-07-02"),
    dict(key="copy_grants_library_meta",
         stmt="Every CREATE OR REPLACE VIEW in LIBRARY_META carries COPY GRANTS.",
         why="Without it a rebuild silently strips the read-role SELECT grant. Every time.",
         decided="2026-07-06"),
    dict(key="fact_vs_lead",
         stmt="Same hard government ID across two sources = FACT. Shared name only = LEAD: "
              "human-review-only, never auto-merged, never stated as true.",
         why="The single design decision the credibility case rests on.", decided="2026-06-25"),
    dict(key="serve_surface_evidence_dev",
         stmt="SERVE surface is evidence.dev; serve/ (Streamlit) is legacy fallback.",
         why="Superseded 2026-07-06.", decided="2026-07-06"),
    dict(key="foundation_before_detectives",
         stmt="Land+wire+catalog only; no new detector/lead/pattern work; publishing layer deferred.",
         why="Alexandria pivot.", decided="2026-06-29"),
    dict(key="source_scope_clean_public",
         stmt="Clean public sources only; paid/ToS-grey dropped or deferred to a specific story need.",
         why="Land-everything sprint scope.", decided="2026-06-27"),
    dict(key="ordering_bridges_first",
         stmt="Crosswalk/bridge sources before domain spines; keyless-before-keyed; "
              "deterministic-before-agentic.",
         why="Connection compounds; LLM burn doesn't.", decided="2026-06-29"),
    dict(key="no_selectorless_dbt_build",
         stmt="Never run a selector-less dbt build: POLITICS__* marts mirror Python-built canonical "
              "tables and a bare build clobbers them.",
         why="24 live marts at risk; convention is the only guard (open defect).", decided="2026-06-30"),
    dict(key="trap_open_payments_split",
         stmt="Open Payments is split across THREE landing tables (base 15.4M / 2022 13.25M / "
              "2023 14.7M). Ad-hoc queries against one bare table under-count; the "
              "banned_but_paid detector already reads a unioned view.",
         why="Verified live 2026-07-12.", decided="2026-06-28"),
    dict(key="trap_ais_snapshot",
         stmt="FED_NOAA_AIS is a stale 8-day snapshot: 58,106,517 rows spanning exactly "
              "2024-01-01..2024-01-08. It pre-dates the 2025-26 sanctions wave — any 'sanctioned "
              "vessel in US waters' match off it is reverse-causality unless date-checked. "
              "Never draw it as a time series.",
         why="Verified live 2026-07-12.", decided="2026-06-28"),
    dict(key="trap_leie_npi_and_dates",
         stmt="FED_HHS_OIG_LEIE: NPI='0000000000' on 74,780/83,464 rows (89.6%) — a naive NPI join "
              "merges them all into one 'doctor' (the libel trap). EXCLDATE needs explicit date "
              "parsing; TRY_CAST collapses to 1970.",
         why="Verified live 2026-07-12.", decided="2026-06-26"),
    dict(key="trap_ofac_sdn_type",
         stmt="FED_OFAC_SDN.SDN_TYPE uses the literal sentinel '-0- ' (trailing space, 9,785 rows) "
              "for entities; also one empty-string row. Filter explicitly.",
         why="Verified live 2026-07-12.", decided="2026-06-25"),
    dict(key="trap_usaspending_grain",
         stmt="USASpending contracts are one row per TRANSACTION, not per award; a company "
              "fragments across child/parent UEIs (Lockheed: 77 child / 26 parent). "
              "Top-contractor rankings are floors, not truths.",
         why="Founder-doc data trap #4.", decided="2026-06-27"),
    dict(key="trap_rlike_whole_string",
         stmt="Snowflake RLIKE/REGEXP match the WHOLE string: 'catalog' RLIKE 'cat' is FALSE. "
              "Wrap patterns in .*...* or catalog searches silently return zero rows.",
         why="Demonstrated live 2026-07-12.", decided="2026-06-25"),
]


# ── merge writers (idempotent; never clobber human state) ────────────────────

MERGE_DEFECT = """MERGE INTO LIBRARY_META.BUILD.DEFECTS d USING (SELECT %s AS DEFECT_ID) s
ON d.DEFECT_ID = s.DEFECT_ID
WHEN MATCHED THEN UPDATE SET TITLE=%s, AREA=%s, SEVERITY=%s, DESCRIPTION=%s,
     VERIFY_METHOD=%s, EVIDENCE_SQL=%s, SOURCE_AUDIT=%s, NOTES=%s
WHEN NOT MATCHED THEN INSERT (DEFECT_ID, TITLE, AREA, SEVERITY, DESCRIPTION, VERIFY_METHOD,
     EVIDENCE_SQL, SOURCE_AUDIT, FOUND_AT, STATUS, NOTES)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'open', %s)"""

MERGE_ACTION = """MERGE INTO LIBRARY_META.BUILD.PENDING_ACTIONS a USING (SELECT %s AS ACTION_ID) s
ON a.ACTION_ID = s.ACTION_ID
WHEN MATCHED THEN UPDATE SET SEQ=%s, SCRIPT_PATH=%s, DESCRIPTION=%s, DEPENDS_ON=%s,
     REVERSIBLE=%s, REQUIRES_HUMAN=%s, VERIFY_SQL=%s
WHEN NOT MATCHED THEN INSERT (ACTION_ID, SEQ, SCRIPT_PATH, DESCRIPTION, DEPENDS_ON,
     REVERSIBLE, REQUIRES_HUMAN, STATUS, VERIFY_SQL)
VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending', %s)"""

MERGE_PARKED = """MERGE INTO LIBRARY_META.BUILD.PARKED p USING (SELECT %s AS PARKED_ID) s
ON p.PARKED_ID = s.PARKED_ID
WHEN MATCHED THEN UPDATE SET TITLE=%s, HEAT=%s, NOTE=%s
WHEN NOT MATCHED THEN INSERT (PARKED_ID, TITLE, HEAT, NOTE, RAISED_AT, STATUS, SUPERSEDED_BY)
VALUES (%s, %s, %s, %s, %s, %s, %s)"""

INSERT_POLICY = """INSERT INTO LIBRARY_META.BUILD.POLICY
(POLICY_KEY, STATEMENT, RATIONALE, DECIDED_AT, STATUS)
SELECT %s, %s, %s, %s, 'active'
WHERE NOT EXISTS (SELECT 1 FROM LIBRARY_META.BUILD.POLICY WHERE POLICY_KEY = %s)"""


def preview(conn) -> None:
    cur = conn.cursor()
    print(f"DDL: {len(DDL)} statements (schema BUILD, 4 tables, V_BUILD_STATE COPY GRANTS, "
          f"read-lane grants)\n")
    print(f"=== DEFECTS seed ({len(DEFECTS)}) — with LIVE verification ===")
    w = max(len(d["title"]) for d in DEFECTS)
    broken = clear = 0
    for d in DEFECTS:
        method = d.get("method", "sql")
        if method == "human":
            verdict, n = "needs_human", "-"
        elif method == "filesystem":
            n = FS_CHECKS[d["title"]]()
            verdict = "still_broken" if n else "clear"
        else:
            try:
                n = exec_evidence(cur, d["sql"])
                verdict = "still_broken" if n else "clear"
            except Exception as e:  # noqa: BLE001
                verdict, n = "error", str(e).splitlines()[0][:40]
        if verdict == "still_broken":
            broken += 1
        elif verdict == "clear":
            clear += 1
        print(f"  [{d['severity']:<7}] {d['title']:<{w}}  {method:<10} -> {verdict:<12} rows={n}")
    print(f"\n  live verdicts: {broken} still_broken, {clear} clear "
          f"(clear rows are seeded OPEN — the verifier recommends, Chris closes)")
    print(f"\n=== PENDING_ACTIONS seed ({len(ACTIONS)}) ===")
    for a in ACTIONS:
        flags = ("HUMAN " if a.get("human") else "") + ("IRREVERSIBLE" if not a.get("reversible", True) else "")
        print(f"  {a['id']} seq={a['seq']:<2} deps={a.get('depends','-'):<11} {flags:<18} {a['path']}")
    print(f"\n=== PARKED seed ({len(PARKED)}) ===")
    for p in PARKED:
        print(f"  [{p.get('status','parked'):<12}] [{p['heat']:<7}] {p['title']}")
    print(f"\n=== POLICY seed ({len(POLICY)}) ===")
    for pl in POLICY:
        print(f"  {pl['key']}")
    print("\nPREVIEW ONLY — nothing written. Apply needs a write-capable token:")
    print("    python3 scripts/build_registry_setup.py --apply")


def apply(conn) -> None:
    cur = conn.cursor()
    for name, stmt in DDL:
        cur.execute(stmt)
        print(f"  ddl ok: {name}")
    for d in DEFECTS:
        i = did(d["area"], d["title"])
        m = d.get("method", "sql")
        note = d.get("note")
        cur.execute(MERGE_DEFECT, (
            i, d["title"], d["area"], d["severity"], d["desc"], m, d.get("sql"), d["found"], note,
            i, d["title"], d["area"], d["severity"], d["desc"], m, d.get("sql"), d["found"],
            "2026-07-12", note))
    print(f"  seeded DEFECTS: {len(DEFECTS)}")
    for a in ACTIONS:
        cur.execute(MERGE_ACTION, (
            a["id"], a["seq"], a["path"], a["desc"], a.get("depends"),
            a.get("reversible", True), a.get("human", False), a.get("verify"),
            a["id"], a["seq"], a["path"], a["desc"], a.get("depends"),
            a.get("reversible", True), a.get("human", False), a.get("verify")))
    print(f"  seeded PENDING_ACTIONS: {len(ACTIONS)}")
    for p in PARKED:
        i = hashlib.md5(p["title"].encode()).hexdigest()
        cur.execute(MERGE_PARKED, (
            i, p["title"], p["heat"], p.get("note"),
            i, p["title"], p["heat"], p.get("note"), "2026-07-12",
            p.get("status", "parked"), p.get("superseded")))
    print(f"  seeded PARKED: {len(PARKED)}")
    for pl in POLICY:
        cur.execute(INSERT_POLICY, (pl["key"], pl["stmt"], pl["why"], pl["decided"], pl["key"]))
    print(f"  seeded POLICY: {len(POLICY)}")
    cur.execute("SELECT METRIC, VALUE FROM LIBRARY_META.BUILD.V_BUILD_STATE ORDER BY 1")
    print("\n  V_BUILD_STATE:")
    for m, v in cur.fetchall():
        print(f"    {m:<30} {v}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Create + seed LIBRARY_META.BUILD (preview by default).")
    ap.add_argument("--apply", action="store_true", help="execute DDL + seed (needs write lane)")
    args = ap.parse_args()

    import snow  # noqa: E402
    conn = snow.connect()
    try:
        cur = conn.cursor()
        cur.execute("SELECT CURRENT_ORGANIZATION_NAME()||'-'||CURRENT_ACCOUNT_NAME(), CURRENT_ROLE()")
        acct, role = cur.fetchone()
        print(f"session: {acct} as {role}\n")
        if args.apply:
            apply(conn)
        else:
            preview(conn)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
