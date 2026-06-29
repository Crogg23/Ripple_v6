-- =====================================================================
-- SERVE_WH — the reading room's own read-only warehouse + budget guard.
-- Run as ACCOUNTADMIN (warehouses + resource monitors require it).
--
-- WHY: the PAT today connects as ACCOUNTADMIN on RIPPLE_WH (the ETL warehouse).
-- A serving app must (a) NOT be ACCOUNTADMIN and (b) NOT contend with ETL. So:
--   • analyst reads run on the existing read-only role CLAUDE_MCP_READONLY
--     (already verified to SELECT the full backbone + CATALOG + INGEST_RUNS),
--   • on a dedicated X-Small SERVE_WH that auto-suspends fast,
--   • capped by its OWN resource monitor so a runaway query can't drain the
--     account-level RIPPLE_BUDGET (30 cr/mo, ~9 left at probe time) and suspend ETL.
-- =====================================================================

USE ROLE ACCOUNTADMIN;

-- 1) Dedicated serving warehouse ---------------------------------------
CREATE WAREHOUSE IF NOT EXISTS SERVE_WH
    WAREHOUSE_SIZE       = 'XSMALL'
    AUTO_SUSPEND         = 60          -- seconds; one analyst, bursty reads
    AUTO_RESUME          = TRUE
    INITIALLY_SUSPENDED  = TRUE
    COMMENT = 'Read-only reading-room serving WH; isolates analyst reads from ETL (RIPPLE_WH/DBT_WH).';

-- 2) Its own budget guard (separate from the account-level RIPPLE_BUDGET) ---
--    Small monthly cap so the reading room can never starve the ETL budget.
CREATE RESOURCE MONITOR IF NOT EXISTS SERVE_MON
    WITH CREDIT_QUOTA   = 5            -- credits/month for serving; raise if needed
         FREQUENCY       = MONTHLY
         START_TIMESTAMP = IMMEDIATELY
    TRIGGERS
         ON 80  PERCENT DO NOTIFY
         ON 100 PERCENT DO SUSPEND
         ON 110 PERCENT DO SUSPEND_IMMEDIATE;

ALTER WAREHOUSE SERVE_WH SET RESOURCE_MONITOR = SERVE_MON;

-- 3) Let the read-only serving role use it (USAGE only — no OPERATE; the role
--    should run queries, not suspend/resume the warehouse) -----------------
GRANT USAGE ON WAREHOUSE SERVE_WH TO ROLE CLAUDE_MCP_READONLY;

-- 4) Sanity check ------------------------------------------------------
SHOW WAREHOUSES LIKE 'SERVE_WH';
-- Expect: one row, state SUSPENDED, size X-Small, resource_monitor SERVE_MON.
