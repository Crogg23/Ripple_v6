-- Run as ACCOUNTADMIN. Dedicated read-only serving warehouse with its OWN budget
-- monitor so the reading room can never drain the account-level RIPPLE_BUDGET
-- (30 cr/mo, ~9 left) and suspend ETL. Reads run on CLAUDE_MCP_READONLY (verified
-- to already SELECT the full backbone + CATALOG + INGEST_RUNS).
USE ROLE ACCOUNTADMIN;

CREATE WAREHOUSE IF NOT EXISTS SERVE_WH
    WAREHOUSE_SIZE       = 'XSMALL'
    AUTO_SUSPEND         = 60
    AUTO_RESUME          = TRUE
    INITIALLY_SUSPENDED  = TRUE
    COMMENT = 'Read-only reading-room serving WH; isolates analyst reads from ETL (RIPPLE_WH/DBT_WH).';

CREATE RESOURCE MONITOR IF NOT EXISTS SERVE_MON
    WITH CREDIT_QUOTA   = 5
         FREQUENCY       = MONTHLY
         START_TIMESTAMP = IMMEDIATELY
    TRIGGERS
         ON 80  PERCENT DO NOTIFY
         ON 100 PERCENT DO SUSPEND
         ON 110 PERCENT DO SUSPEND_IMMEDIATE;

ALTER WAREHOUSE SERVE_WH SET RESOURCE_MONITOR = SERVE_MON;

GRANT USAGE ON WAREHOUSE SERVE_WH TO ROLE CLAUDE_MCP_READONLY;

SHOW WAREHOUSES LIKE 'SERVE_WH';