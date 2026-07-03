-- ============================================================================
-- Investigator Instrument - Snowflake setup (CHRIS APPLIES, as ACCOUNTADMIN)
-- ============================================================================
-- The instrument runs TODAY without any of this (client-guard lane on
-- COMPUTE_WH, loud banner). Each step below upgrades one guarantee.
-- Run top to bottom in Snowsight; every statement is idempotent or guarded.
--
-- WHY a NEW role instead of hardening CLAUDE_MCP_READONLY: the live probe
-- (2026-07-03) showed CLAUDE_MCP_READONLY holds CREATE TABLE/VIEW/STAGE/FILE
-- FORMAT on 18 schemas, CREATE SCHEMA on 4 DBs and OPERATE on 2 warehouses -
-- and some as FUTURE grants, which a REVOKE sweep does not remove. A role that
-- was NEVER granted write is provably read-only; a scrubbed role is only as
-- read-only as the completeness of the scrub. So: fresh role, SELECT only.
-- ============================================================================

-- ---------------------------------------------------------------------------
-- STEP 0 - the capped serving lane (skip if SERVE_WH already exists)
--   Canonical DDL: serve/serve_wh.sql  (SERVE_WH XSMALL 60s autosuspend
--   + SERVE_MON monthly cap). Sizing: check live headroom first
--   (SHOW RESOURCE MONITORS - never trust a number written in prose); the
--   serve cap still covers hours of X-Small charting, and if it ever bites:
--   ALTER RESOURCE MONITOR SERVE_MON SET CREDIT_QUOTA = <new>;
-- ---------------------------------------------------------------------------
-- !source serve/serve_wh.sql   (or paste that file here)

-- ---------------------------------------------------------------------------
-- STEP 1 - the clean reader role
-- ---------------------------------------------------------------------------
CREATE ROLE IF NOT EXISTS RIPPLE_READER
  COMMENT = 'Provably read-only serving role for the Investigator Instrument. USAGE + SELECT only - never granted a write privilege. If you are about to GRANT CREATE/INSERT/OPERATE on this role: do not.';

GRANT ROLE RIPPLE_READER TO USER CROGG23;

-- ---------------------------------------------------------------------------
-- STEP 2 - read surface: USAGE + SELECT (current AND future) on the read DBs
-- ---------------------------------------------------------------------------
GRANT USAGE ON DATABASE LIBRARY_RAW      TO ROLE RIPPLE_READER;
GRANT USAGE ON DATABASE LIBRARY_META     TO ROLE RIPPLE_READER;
GRANT USAGE ON DATABASE LIBRARY_MARTS    TO ROLE RIPPLE_READER;
GRANT USAGE ON DATABASE LIBRARY_STAGING  TO ROLE RIPPLE_READER;
GRANT USAGE ON DATABASE THE_LIBRARY      TO ROLE RIPPLE_READER;

GRANT USAGE ON ALL    SCHEMAS IN DATABASE LIBRARY_RAW     TO ROLE RIPPLE_READER;
GRANT USAGE ON FUTURE SCHEMAS IN DATABASE LIBRARY_RAW     TO ROLE RIPPLE_READER;
GRANT USAGE ON ALL    SCHEMAS IN DATABASE LIBRARY_META    TO ROLE RIPPLE_READER;
GRANT USAGE ON FUTURE SCHEMAS IN DATABASE LIBRARY_META    TO ROLE RIPPLE_READER;
GRANT USAGE ON ALL    SCHEMAS IN DATABASE LIBRARY_MARTS   TO ROLE RIPPLE_READER;
GRANT USAGE ON FUTURE SCHEMAS IN DATABASE LIBRARY_MARTS   TO ROLE RIPPLE_READER;
GRANT USAGE ON ALL    SCHEMAS IN DATABASE LIBRARY_STAGING TO ROLE RIPPLE_READER;
GRANT USAGE ON FUTURE SCHEMAS IN DATABASE LIBRARY_STAGING TO ROLE RIPPLE_READER;
GRANT USAGE ON ALL    SCHEMAS IN DATABASE THE_LIBRARY     TO ROLE RIPPLE_READER;
GRANT USAGE ON FUTURE SCHEMAS IN DATABASE THE_LIBRARY     TO ROLE RIPPLE_READER;

GRANT SELECT ON ALL    TABLES IN DATABASE LIBRARY_RAW     TO ROLE RIPPLE_READER;
GRANT SELECT ON FUTURE TABLES IN DATABASE LIBRARY_RAW     TO ROLE RIPPLE_READER;
GRANT SELECT ON ALL    TABLES IN DATABASE LIBRARY_META    TO ROLE RIPPLE_READER;
GRANT SELECT ON FUTURE TABLES IN DATABASE LIBRARY_META    TO ROLE RIPPLE_READER;
GRANT SELECT ON ALL    VIEWS  IN DATABASE LIBRARY_META    TO ROLE RIPPLE_READER;
GRANT SELECT ON FUTURE VIEWS  IN DATABASE LIBRARY_META    TO ROLE RIPPLE_READER;
GRANT SELECT ON ALL    TABLES IN DATABASE LIBRARY_MARTS   TO ROLE RIPPLE_READER;
GRANT SELECT ON FUTURE TABLES IN DATABASE LIBRARY_MARTS   TO ROLE RIPPLE_READER;
GRANT SELECT ON ALL    VIEWS  IN DATABASE LIBRARY_MARTS   TO ROLE RIPPLE_READER;
GRANT SELECT ON FUTURE VIEWS  IN DATABASE LIBRARY_MARTS   TO ROLE RIPPLE_READER;
GRANT SELECT ON ALL    TABLES IN DATABASE LIBRARY_STAGING TO ROLE RIPPLE_READER;
GRANT SELECT ON FUTURE TABLES IN DATABASE LIBRARY_STAGING TO ROLE RIPPLE_READER;
GRANT SELECT ON ALL    VIEWS  IN DATABASE LIBRARY_STAGING TO ROLE RIPPLE_READER;
GRANT SELECT ON FUTURE VIEWS  IN DATABASE LIBRARY_STAGING TO ROLE RIPPLE_READER;
GRANT SELECT ON ALL    VIEWS  IN DATABASE THE_LIBRARY     TO ROLE RIPPLE_READER;
GRANT SELECT ON FUTURE VIEWS  IN DATABASE THE_LIBRARY     TO ROLE RIPPLE_READER;

-- The libel firewall, server-side: the reader role must NOT see raw claim
-- tables (unreviewed accusations about named people) - only the published view.
-- NOTE: the FUTURE TABLES grant above re-covers any NEW claim table created in
-- "CONNECT" later; re-run these REVOKEs after adding one (the client-side scan
-- in viz/guard.py CLAIM_TABLES is the belt that covers the gap meanwhile).
REVOKE SELECT ON TABLE LIBRARY_META."CONNECT".LEADS         FROM ROLE RIPPLE_READER;
REVOKE SELECT ON TABLE LIBRARY_META."CONNECT".ENTITY_LINKS  FROM ROLE RIPPLE_READER;
REVOKE SELECT ON TABLE LIBRARY_META."CONNECT".ENTITY_MAP    FROM ROLE RIPPLE_READER;
REVOKE SELECT ON TABLE LIBRARY_META."CONNECT".ENTITY_GOLDEN FROM ROLE RIPPLE_READER;
REVOKE SELECT ON TABLE LIBRARY_META."CONNECT".MATCH_PAIRS   FROM ROLE RIPPLE_READER;
GRANT  SELECT ON VIEW  LIBRARY_META."CONNECT".V_LEADS_PUBLISHED TO ROLE RIPPLE_READER;

-- ---------------------------------------------------------------------------
-- STEP 3 - warehouses (USAGE only - no OPERATE) + budget visibility
-- ---------------------------------------------------------------------------
GRANT USAGE ON WAREHOUSE SERVE_WH   TO ROLE RIPPLE_READER;   -- after STEP 0
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE RIPPLE_READER;   -- the fallback lane

-- without MONITOR the instrument's budget meter goes blind under this role
GRANT MONITOR ON RESOURCE MONITOR SERVE_MON     TO ROLE RIPPLE_READER;  -- after STEP 0
GRANT MONITOR ON RESOURCE MONITOR RIPPLE_BUDGET TO ROLE RIPPLE_READER;

-- ---------------------------------------------------------------------------
-- STEP 4 - mint the serving PAT, bound to the reader role
--   (PAT sessions cannot USE ROLE - the binding IS the enforcement)
-- ---------------------------------------------------------------------------
ALTER USER CROGG23 ADD PROGRAMMATIC ACCESS TOKEN INSTRUMENT_READER
  ROLE_RESTRICTION = 'RIPPLE_READER'
  DAYS_TO_EXPIRY = 90
  COMMENT = 'Investigator Instrument read lane (viz/sqlrun.py). Rotate with the main PAT.';
-- Copy the token secret Snowsight shows you ONCE into library-onboarding/.env:
--     SNOWFLAKE_SERVE_PAT=<the token>
--     RIPPLE_SERVE_ROLE=RIPPLE_READER
-- (add the expiry to infra/keys_ledger.json so preflight tracks it)

-- ---------------------------------------------------------------------------
-- STEP 5 - verify (from the repo)
--     python ripple.py chart budget
--   Expected: "lane: enforced" + "[OK] read-only lane enforced (role RIPPLE_READER)".
--   The instrument VERIFIES the lane at connect time (CURRENT_ROLE, USE ROLE
--   must fail, SHOW GRANTS must be write-free) - if any check fails it stays
--   in client-guard mode and says so. It never trusts this file ran.
-- ============================================================================
