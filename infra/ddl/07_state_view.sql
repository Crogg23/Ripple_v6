-- 07_state_view.sql — V_STATE: the single derived source of truth for every headline number.
-- Why (2026-07-02 audit): every scale claim hand-transcribed into prose (CLAUDE.md, OVERVIEW,
-- build-state) rotted within days, while numbers behind acceptance queries verified exactly.
-- Rule going forward: docs cite this view; nobody pastes a count into markdown again.
-- Grain: one row per metric (METRIC, VALUE, AS_OF). Cheap — metadata + small aggregates only.
-- Caveats (measured, accepted):
--   * INFORMATION_SCHEMA is filtered by the CALLER's role — counts are role-relative (ACCOUNTADMIN
--     sees everything; a restricted role sees only what it can read). Same caveat as CATALOG.
--   * marts.stale_vs_landing uses LAST_ALTERED (TIMESTAMP_LTZ, bumps on metadata-only ALTERs) vs the
--     source's last successful ingest — an hours-level, occasionally-noisy drift signal, not a proof.
--   * Multi-source marts (no single <domain>__<source_id> parse) are skipped by the drift check —
--     the same known limitation as CATALOG's mart matching.

CREATE OR REPLACE VIEW LIBRARY_META.REGISTRY.V_STATE
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
    SELECT 'decisions.total', COUNT(*)::VARCHAR FROM LIBRARY_META."CONNECT".DECISIONS
), edges AS (
    -- CONNECT_EDGES is the canonical store (full rebuild replaces, incremental merges);
    -- CONNECT_EDGES_INC reported separately until the incremental writer is retargeted.
    SELECT 'connect.edges', COUNT(*)::VARCHAR FROM LIBRARY_META."CONNECT".CONNECT_EDGES
    UNION ALL
    SELECT 'connect.edges_inc', COUNT(*)::VARCHAR FROM LIBRARY_META."CONNECT".CONNECT_EDGES_INC
    UNION ALL
    SELECT 'connect.entities', COUNT(*)::VARCHAR FROM LIBRARY_META."CONNECT".ENTITY_GOLDEN
), rooms AS (
    SELECT 'reading_room.views', COUNT(*)::VARCHAR
    FROM THE_LIBRARY.INFORMATION_SCHEMA.VIEWS WHERE TABLE_SCHEMA <> 'INFORMATION_SCHEMA'
), drift AS (
    -- Marts older than their source's last successful ingest = stale derived data.
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
