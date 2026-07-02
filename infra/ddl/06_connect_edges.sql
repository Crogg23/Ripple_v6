-- 06_connect_edges.sql — the ONE canonical persisted edge store for the connect graph.
-- Why this exists (2026-07-02): the headline connection graph lived only in a gitignored
-- outputs/connect_graph.json — absent from fresh checkouts, unverifiable from the warehouse, and
-- the serve/plane/overlay products broke whenever the file was missing. Meanwhile the incremental
-- engine wrote a second store (CONNECT_EDGES_INC) that nothing read. One table ends the split:
--   * a FULL rebuild (python -m connect discover) REPLACES the contents (scoped by RUN_ID),
--   * the incremental engine (connect-one / reslice) MERGEs into it,
--   * V_STATE counts it, and the JSON becomes a regenerable projection of it.
-- Shape matches CONNECT_EDGES_INC exactly so the incremental writer can retarget without migration.
-- Idempotent: CREATE TABLE IF NOT EXISTS — never CREATE OR REPLACE (would wipe edges on re-run).

-- "KEY" and "SAMPLE" are Snowflake reserved words — quoted here, exactly as CONNECT_EDGES_INC has them.
CREATE TABLE IF NOT EXISTS LIBRARY_META."CONNECT".CONNECT_EDGES (
    A            VARCHAR,          -- landing table name (one side of the edge)
    B            VARCHAR,          -- landing table name (other side)
    "KEY"        VARCHAR,          -- the join key that connects them (NPI, EIN, IMO, ...)
    TIER         VARCHAR,          -- STEEL / STRONG / GEO / CORROBORATED / PROBABILISTIC / BRIDGE
    MATCHED      NUMBER,           -- distinct key values present on BOTH sides
    A_DISTINCT   NUMBER,
    B_DISTINCT   NUMBER,
    MATCH_RATE   FLOAT,
    CONFIDENCE   FLOAT,            -- heuristic fluke-gate score (uncalibrated — see discover.confidence)
    "SAMPLE"     VARIANT,          -- a few matched values as evidence
    RUN_ID       VARCHAR,          -- which rebuild/reslice wrote this row
    BUILT_AT     TIMESTAMP_NTZ
);

COMMENT ON TABLE LIBRARY_META."CONNECT".CONNECT_EDGES IS
'Canonical persisted connection graph: one row per (table A, table B, key) edge with measured overlap. Full rebuilds replace it; the incremental engine merges into it; outputs/connect_graph.json is a regenerable projection. Added 2026-07-02 so the graph is queryable and survives a fresh checkout.';
