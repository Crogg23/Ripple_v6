-- ============================================================================
-- COLUMN_CATALOG — the per-column data dictionary (Playground, 2026-08-01).
-- One-time DDL: CHRIS runs this in Snowsight as ACCOUNTADMIN (the role that
-- owns LIBRARY_META). Rows are written by scripts/build_column_catalog.py on
-- the standard loader lane (the same PAT that writes LIBRARY_META.REGISTRY);
-- the A00 cutover PAT is NOT involved.
--
-- WHY: dataset-level metadata is rich (SOURCE_REGISTRY / CATALOG /
-- FRIENDLY_LAYER) but nothing persisted per COLUMN — viz/catalog.py profile()
-- and thelibrary_typed_views.py both compute chart roles / populated% /
-- key detection per column and throw the result away. The Playground's
-- tailored dictionary needs it durable and queryable.
-- ============================================================================

CREATE TABLE IF NOT EXISTS LIBRARY_META.REGISTRY.COLUMN_CATALOG (
    FQN               VARCHAR NOT NULL,   -- fully qualified table/view name
    COLUMN_NAME       VARCHAR NOT NULL,
    ORDINAL           NUMBER,
    SF_TYPE           VARCHAR,            -- Snowflake type from DESCRIBE
    CHART_ROLE        VARCHAR,            -- numeric | date | category | text | empty
    DIGIT_DATE        BOOLEAN,            -- YYYYMMDD-in-TEXT: bare TRY_TO_DATE parses epoch — never
    NONNULL_PCT       FLOAT,
    DISTINCT_SAMPLED  NUMBER,
    DETECTED_KEY      VARCHAR,            -- connect/keys.py detect_key: NPI/EIN/BIOGUIDE/...
    KEY_TIER          VARCHAR,            -- STEEL | STRONG | PROBABILISTIC | GEO
    KEY_POPULATED_PCT FLOAT,              -- value-measured with the key's own normalizer
    PLAIN_GLOSS       VARCHAR,            -- resolved: curated (glossary/column_gloss.py) wins, else heuristic
    GLOSS_SOURCE      VARCHAR,            -- 'curated' | 'heuristic'
    SAMPLE_VALUES     ARRAY,              -- up to 5 distinct non-null values, truncated
    PROFILE_N         NUMBER,             -- rows sampled by the profiler
    PROFILED_AT       TIMESTAMP_NTZ DEFAULT SYSDATE()
)
COMMENT = 'Per-column data dictionary: type, chart role, fill rate, detected hard-ID key, plain-English gloss, sample values. Built by scripts/build_column_catalog.py (preview then --apply); curated glosses live in git at glossary/column_gloss.py and are re-merged on every rebuild. Regenerable.';

GRANT USAGE ON DATABASE LIBRARY_META TO ROLE RIPPLE_READER;
GRANT USAGE ON SCHEMA LIBRARY_META.REGISTRY TO ROLE RIPPLE_READER;
GRANT SELECT ON TABLE LIBRARY_META.REGISTRY.COLUMN_CATALOG TO ROLE RIPPLE_READER;

-- The MCP read lane sees it too (harmless if the role doesn't exist yet —
-- re-run the line after that role is provisioned).
GRANT SELECT ON TABLE LIBRARY_META.REGISTRY.COLUMN_CATALOG TO ROLE CLAUDE_MCP_READONLY;

-- VERIFY (comments — run by hand):
--   SELECT COUNT(*), COUNT(DISTINCT FQN) FROM LIBRARY_META.REGISTRY.COLUMN_CATALOG;
--   SELECT * FROM LIBRARY_META.REGISTRY.COLUMN_CATALOG
--    WHERE FQN = 'LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_MONEY_RAISED';
