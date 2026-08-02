-- ============================================================================
-- HYPOTHESIS_CATALOG — the Hunch Engine's durable feed (2026-08-01).
-- One-time DDL: CHRIS runs this in Snowsight as ACCOUNTADMIN (the role that
-- owns LIBRARY_META) — same pattern as 06_column_catalog.sql. Rows are written
-- by scripts/hunch_sieve.py on the standard loader lane; the A00 cutover PAT
-- is NOT involved.
--
-- WHY: the constitution's no-runtime-AI rule — discovery runs at build time,
-- results live in a control table, and the future Hunches room reads plain
-- SQL. One row = one comparable pairing with its surprise score and the
-- honesty apparatus (null used, range conditioning, expected flukes, traps).
-- Never an accusation: "S_CHANCE is a distance from boring, not a finding"
-- (reports/hunch_null_models_2026-08-01.md).
-- ============================================================================

CREATE TABLE IF NOT EXISTS LIBRARY_META.REGISTRY.HYPOTHESIS_CATALOG (
    PAIR_A            VARCHAR NOT NULL,   -- landing identifier (UPPER, unqualified)
    PAIR_B            VARCHAR NOT NULL,   -- canonical: PAIR_A < PAIR_B
    "KEY"             VARCHAR NOT NULL,   -- join key label (KEY_TOKENS vocabulary)
    TIER              VARCHAR,            -- STEEL|STRONG|GEO|PROBABILISTIC|BRIDGE|CORROBORATED
    A_COL             VARCHAR,
    B_COL             VARCHAR,
    A_DISTINCT        NUMBER,
    B_DISTINCT        NUMBER,
    MATCHED           NUMBER,             -- NULL until the pair is measured
    EXPECTED_CHANCE   FLOAT,              -- independence null over KEY_DOMAIN
    S_CHANCE          FLOAT,              -- log10((matched+1)/(expected+1)); NULL if unmeasured/unscorable
    BAND              VARCHAR,            -- excess|chance|absence|partitioned|absence-unscorable|unmeasured
    COVERAGE          FLOAT,              -- matched / min(distinct)
    RANGE_REASON      VARCHAR,            -- why absence is/isn't scorable (fmt-2 range check)
    ABSENCE_VALID     BOOLEAN,
    EXPECTED_FLUKES   FLOAT,              -- chance survivors at this row's S across the family
    PROMOTABLE        BOOLEAN,            -- S clears band AND expected flukes < 1
    SAME_FAMILY       BOOLEAN,            -- both sides share an agency prefix (feed diversity)
    TRAPS             ARRAY,              -- honesty/traps.py keys, both sides
    VERIFIED_TIER     VARCHAR,            -- connect/ edge tier if already verified
    STAGE             VARCHAR,            -- metadata | measured
    SCAFFOLD_SQL      VARCHAR,            -- ready-to-run join scaffold for the SQL editor
    RUN_ID            VARCHAR,
    BUILT_AT          TIMESTAMP_NTZ DEFAULT SYSDATE(),
    -- verdict loop (Pattern-Desk-style, written later by the review lane —
    -- NEVER by the sieve): boring | interesting | artifact
    VERDICT           VARCHAR,
    VERDICTED_AT      TIMESTAMP_NTZ
)
COMMENT = 'Hunch Engine feed: every comparable pairing with surprise score vs the dullest null, range-conditioned absence, family-wide expected-fluke count, and trap flags. Built by scripts/hunch_sieve.py (preview then --apply); scores are distances from boring, never findings. Human verdicts arrive via the review lane only. Regenerable except VERDICT/VERDICTED_AT.';

GRANT USAGE ON DATABASE LIBRARY_META TO ROLE RIPPLE_READER;
GRANT USAGE ON SCHEMA LIBRARY_META.REGISTRY TO ROLE RIPPLE_READER;
GRANT SELECT ON TABLE LIBRARY_META.REGISTRY.HYPOTHESIS_CATALOG TO ROLE RIPPLE_READER;

-- The MCP read lane sees it too (harmless if the role doesn't exist yet —
-- re-run the line after that role is provisioned).
GRANT SELECT ON TABLE LIBRARY_META.REGISTRY.HYPOTHESIS_CATALOG TO ROLE CLAUDE_MCP_READONLY;

-- VERIFY (comments — run by hand):
--   SELECT STAGE, BAND, COUNT(*) FROM LIBRARY_META.REGISTRY.HYPOTHESIS_CATALOG
--    GROUP BY 1, 2 ORDER BY 1, 2;
--   SELECT * FROM LIBRARY_META.REGISTRY.HYPOTHESIS_CATALOG
--    WHERE PROMOTABLE ORDER BY S_CHANCE DESC LIMIT 20;
