-- ============================================================================
-- A14 — Provision the Reading Room write lane (CHRIS APPLIES, in Snowsight,
-- as SECURITYADMIN/ACCOUNTADMIN). Run top to bottom; every statement is
-- idempotent or guarded. Reviewed at Reading Room Checkpoint 2.
-- ============================================================================
-- WHAT THIS BUILDS
--   Part 1  LIBRARY_META.REVIEW schema + DECISIONS table (append-only home
--           for human verdicts; supersedes the empty CONNECT.DECISIONS stub)
--   Part 2  RIPPLE_REVIEW_WRITER role — INSERT + SELECT on that ONE table
--           and nothing else. Append-only is enforced HERE, by the database:
--           the role simply has no UPDATE/DELETE/TRUNCATE/DDL to abuse.
--   Part 3  Consumer re-points: V_LATEST_DECISIONS (new), V_LEADS_PUBLISHED
--           (reads REVIEW.DECISIONS + picks up the receipt columns —
--           SUPERSEDES A12 if you haven't run that yet), V_STATE
--           (decisions.total from the new table).
--   Part 4  Retire the old CONNECT.DECISIONS stub (rename, never drop).
--           It has 0 rows (verified 2026-07-12) — zero-migration.
--
-- DESIGN NOTES (approved at Checkpoint 0/1)
--   * Column names keep the EXISTING decisions contract (connect/safety.py:
--     TARGET_KIND / TARGET_ID / DECISION / REASON / REVIEWER / MODEL_VERSION
--     / DECIDED_AT) plus two additions: DECISION_ID and QUEUE_SNAPSHOT.
--   * Verdict vocabulary keeps the existing lowercase set + needs_work:
--     'confirmed' | 'rejected' | 'retracted' | 'stale' | 'needs_work'.
--     needs_work is deliberately NON-suppressing: the lead stays visible in
--     V_LEADS_PUBLISHED (flagged), exactly the Reading Room's NEEDS_WORK.
--   * Every CREATE OR REPLACE VIEW carries COPY GRANTS (POLICY
--     copy_grants_library_meta).
--
-- AFTER RUNNING: mint a PAT restricted to role RIPPLE_REVIEW_WRITER (with an
-- expiry), add it to library-onboarding/.env as RIPPLE_REVIEW_PAT, then run
-- scripts/verify_review_lane.sql AS THAT ROLE (its two PERMISSION DENIEDs
-- are the point). The app halts its write path if the PAT is absent — it
-- never falls back to another credential.
--
-- VERIFY (expected: one row each):
--   SELECT 1 FROM LIBRARY_META.INFORMATION_SCHEMA.TABLES
--     WHERE TABLE_SCHEMA='REVIEW' AND TABLE_NAME='DECISIONS';
--   SHOW GRANTS TO ROLE RIPPLE_REVIEW_WRITER;  -- INSERT+SELECT on one table
-- ============================================================================

-- ── Part 1: schema + table ─────────────────────────────────────────────────

CREATE SCHEMA IF NOT EXISTS LIBRARY_META.REVIEW
  COMMENT = 'The human-review write lane. ONE table (DECISIONS), append-only by grant design; written only via the RIPPLE_REVIEW_PAT scoped to RIPPLE_REVIEW_WRITER.';

CREATE TABLE IF NOT EXISTS LIBRARY_META.REVIEW.DECISIONS (
    DECISION_ID    STRING        DEFAULT UUID_STRING(),
    TARGET_KIND    STRING        NOT NULL DEFAULT 'lead',  -- 'lead' | 'link' | 'entity'
    TARGET_ID      STRING        NOT NULL,                 -- LEAD_ID for leads
    DECISION       STRING        NOT NULL,                 -- confirmed|rejected|retracted|stale|needs_work
    REASON         STRING,                                 -- the reviewer's note
    REVIEWER       STRING        NOT NULL,
    MODEL_VERSION  STRING,                                 -- scoring model of the judged claim, if any
    QUEUE_SNAPSHOT VARIANT,                                -- headline + scores + rank at decision time
    DECIDED_AT     TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
)
COMMENT = 'Append-only audit log of human verdicts (who/when/what/why). The LATEST verdict per target wins. Corrections are NEW rows, never updates — the write role holds no UPDATE/DELETE. SMOKE_TEST row = permanent proof the wall holds.';

-- ── Part 2: the scoped write role ───────────────────────────────────────────

CREATE ROLE IF NOT EXISTS RIPPLE_REVIEW_WRITER
  COMMENT = 'Reading Room verdict writer. INSERT+SELECT on LIBRARY_META.REVIEW.DECISIONS and nothing else — append-only enforced by the database, not by app code.';

GRANT USAGE ON DATABASE LIBRARY_META TO ROLE RIPPLE_REVIEW_WRITER;
GRANT USAGE ON SCHEMA LIBRARY_META.REVIEW TO ROLE RIPPLE_REVIEW_WRITER;
GRANT INSERT, SELECT ON TABLE LIBRARY_META.REVIEW.DECISIONS
  TO ROLE RIPPLE_REVIEW_WRITER;
-- Deliberately NO UPDATE, DELETE, TRUNCATE, or DDL grants. If a statement
-- other than INSERT/SELECT succeeds as this role, the provisioning is wrong.

-- The writer needs a warehouse to execute its INSERT; SERVE_WH is the tiny
-- monitored one (SERVE_MON, 5-credit quota).
GRANT USAGE ON WAREHOUSE SERVE_WH TO ROLE RIPPLE_REVIEW_WRITER;

GRANT ROLE RIPPLE_REVIEW_WRITER TO USER CROGG23;
-- Now mint the PAT in Snowsight: restricted to RIPPLE_REVIEW_WRITER, with an
-- expiry, and add it to library-onboarding/.env as RIPPLE_REVIEW_PAT.

-- ── Part 3: consumer re-points (all COPY GRANTS) ───────────────────────────

-- 3a. Latest-decision view — the app's anti-join surface. Truth = latest row;
--     the SMOKE_TEST proof row is filtered out of every read path here.
CREATE OR REPLACE VIEW LIBRARY_META.REVIEW.V_LATEST_DECISIONS
COPY GRANTS
COMMENT = 'Latest verdict per lead (append-only means corrections are new rows; this view is the truth). SMOKE_TEST excluded. LEAD_ID aliased for the Reading Room app.'
AS
SELECT
    TARGET_ID                                   AS LEAD_ID,
    DECISION,
    REASON,
    REVIEWER,
    QUEUE_SNAPSHOT,
    DECIDED_AT,
    DECISION_ID
FROM LIBRARY_META.REVIEW.DECISIONS
WHERE TARGET_KIND = 'lead'
  AND TARGET_ID != 'SMOKE_TEST'
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY TARGET_ID ORDER BY DECIDED_AT DESC) = 1;

-- The app's reader lane needs to see decisions (queue anti-join).
GRANT USAGE ON SCHEMA LIBRARY_META.REVIEW TO ROLE RIPPLE_READER;
GRANT SELECT ON VIEW LIBRARY_META.REVIEW.V_LATEST_DECISIONS TO ROLE RIPPLE_READER;
-- (The LEAD_QUEUE mart grant lives at the very END of this script: it can
--  error before A13 has built the mart, and a mid-script error under
--  Snowsight "Run All" would abort the view re-points below.)

-- 3b. V_LEADS_PUBLISHED — same published() semantics, now reading the new
--     DECISIONS home; l.* also picks up the receipt columns ALTER-added
--     after the view's 2026-07-03 creation (this SUPERSEDES A12).
CREATE OR REPLACE VIEW LIBRARY_META."CONNECT".V_LEADS_PUBLISHED
COPY GRANTS
COMMENT = 'The SAFE way to read leads in SQL: published()-semantics as a view. Drops leads whose latest human verdict is rejected/retracted/stale, drops leads absent from the latest run (STATUS<>active), and stamps every survivor with REVIEW_STATE + PUBLISHED so an unreviewed lead can never read as fact. Verdicts live in LIBRARY_META.REVIEW.DECISIONS since 2026-07-12 (Reading Room). Mirrors connect/leads.py published(). Regenerable.'
AS
WITH latest_verdict AS (
    SELECT TARGET_ID, DECISION
    FROM LIBRARY_META.REVIEW.DECISIONS
    WHERE TARGET_KIND = 'lead'
      AND TARGET_ID != 'SMOKE_TEST'
    QUALIFY ROW_NUMBER() OVER (PARTITION BY TARGET_ID ORDER BY DECIDED_AT DESC) = 1
)
SELECT
    l.*,
    COALESCE(v.DECISION, 'pending')                    AS REVIEW_STATE,
    COALESCE(v.DECISION, 'pending') = 'confirmed'      AS PUBLISHED
FROM LIBRARY_META."CONNECT".LEADS l
LEFT JOIN latest_verdict v ON v.TARGET_ID = l.LEAD_ID
WHERE COALESCE(l.STATUS, 'active') = 'active'
  AND COALESCE(v.DECISION, 'pending') NOT IN ('rejected', 'retracted', 'stale');

-- 3c. V_STATE — decisions.total now counts the new table (SMOKE_TEST
--     excluded). Full view reproduced from the live DDL captured 2026-07-12;
--     ONLY the decisions CTE changed.
CREATE OR REPLACE VIEW LIBRARY_META.REGISTRY.V_STATE
COPY GRANTS
COMMENT = 'One row per platform metric, derived live. Cite THIS in docs — never paste numbers into prose. Added 2026-07-02 (Fable audit: prose numbers rot, derived numbers survive).'
AS
WITH taps AS (
    SELECT 'taps.' || LIFECYCLE AS metric, COUNT(*)::VARCHAR AS value
    FROM LIBRARY_META.REGISTRY.CATALOG GROUP BY LIFECYCLE
), cat AS (
    SELECT 'catalog.sources', COUNT(DISTINCT SOURCE_ID)::VARCHAR FROM LIBRARY_META.REGISTRY.CATALOG
    UNION ALL
    SELECT 'catalog.orphans', COUNT(*)::VARCHAR FROM LIBRARY_META.REGISTRY.CATALOG WHERE IS_ORPHAN
    UNION ALL
    SELECT 'registry.sources', COUNT(*)::VARCHAR FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY
), landing AS (
    SELECT 'landing.tables', COUNT(*)::VARCHAR
    FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'LANDING'
    UNION ALL
    SELECT 'landing.rows', COALESCE(SUM(ROW_COUNT), 0)::VARCHAR
    FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'LANDING'
), leads AS (
    SELECT 'leads.' || RULE_NAME || '.' || COALESCE(STATUS, 'active') AS metric, COUNT(*)::VARCHAR
    FROM LIBRARY_META."CONNECT".LEADS GROUP BY RULE_NAME, STATUS
), decisions AS (
    SELECT 'decisions.total', COUNT(*)::VARCHAR
    FROM LIBRARY_META.REVIEW.DECISIONS
    WHERE TARGET_ID != 'SMOKE_TEST'
), edges AS (
    SELECT 'connect.edges', COUNT(*)::VARCHAR FROM LIBRARY_META."CONNECT".CONNECT_EDGES
    UNION ALL
    SELECT 'connect.edges_inc', COUNT(*)::VARCHAR FROM LIBRARY_META."CONNECT".CONNECT_EDGES_INC
    UNION ALL
    SELECT 'connect.entities', COUNT(*)::VARCHAR FROM LIBRARY_META."CONNECT".ENTITY_GOLDEN
), rooms AS (
    SELECT 'reading_room.views', COUNT(*)::VARCHAR
    FROM THE_LIBRARY.INFORMATION_SCHEMA.VIEWS WHERE TABLE_SCHEMA <> 'INFORMATION_SCHEMA'
), drift AS (
    SELECT 'marts.stale_vs_landing', COUNT(*)::VARCHAR
    FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES t
    JOIN (
        SELECT UPPER(SOURCE_ID) AS sid, MAX(COALESCE(ENDED_AT, STARTED_AT)) AS last_ingest
        FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS WHERE STATUS = 'success' GROUP BY 1
    ) r ON UPPER(SPLIT_PART(t.TABLE_NAME, '__', 2)) = r.sid
    WHERE t.TABLE_SCHEMA <> 'INFORMATION_SCHEMA'
      AND t.TABLE_SCHEMA NOT LIKE '\\_RESTORE%'
      AND POSITION('__' IN t.TABLE_NAME) > 0
      AND CONVERT_TIMEZONE('UTC', t.LAST_ALTERED)::TIMESTAMP_NTZ < r.last_ingest
)
SELECT metric AS METRIC, value AS VALUE, CURRENT_TIMESTAMP() AS AS_OF FROM (
    SELECT * FROM taps
    UNION ALL SELECT * FROM cat
    UNION ALL SELECT * FROM landing
    UNION ALL SELECT * FROM leads
    UNION ALL SELECT * FROM decisions
    UNION ALL SELECT * FROM edges
    UNION ALL SELECT * FROM rooms
    UNION ALL SELECT * FROM drift
);

-- ── Part 4: retire the old stub (rename, never drop) ───────────────────────
-- CONNECT.DECISIONS holds 0 rows (verified 2026-07-12). Repo code on THIS
-- branch is re-pointed at REVIEW.DECISIONS (connect/safety.py) — but a
-- STALE CHECKOUT on another machine could silently recreate the stub and
-- write verdicts nobody reads. A tripwire defect in LIBRARY_META.BUILD
-- (build_registry_setup.py) fires if CONNECT.DECISIONS ever reappears.

ALTER TABLE IF EXISTS LIBRARY_META."CONNECT".DECISIONS
  RENAME TO LIBRARY_META."CONNECT".ZZ_RETIRED_DECISIONS_20260712;

-- ── Part 5 (LAST, may error harmlessly before A13): the queue-mart grant ───
-- Errors with 'does not exist' if the LEAD_QUEUE mart hasn't been built yet
-- (action A13) — everything above has already applied; just re-run this one
-- line after the first mart build. lead_queue.sql sets copy_grants=true so
-- dbt rebuilds keep the grant afterwards.

GRANT SELECT ON TABLE LIBRARY_MARTS.DBT_CROGERS.LEAD_QUEUE TO ROLE RIPPLE_READER;
