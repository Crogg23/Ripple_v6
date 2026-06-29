-- Warehouses, the RIPPLE_BUDGET resource monitor, and custom roles.
-- AGENT-RECONSTRUCTED from SHOW output — review sizes/grants before relying on for DR.

-- RIPPLE_WH (warehouse)
-- Reconstructed from SHOW WAREHOUSES (GET_DDL not supported for warehouses).
CREATE WAREHOUSE IF NOT EXISTS RIPPLE_WH
  WAREHOUSE_SIZE = 'XSMALL'
  WAREHOUSE_TYPE = 'STANDARD'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  MIN_CLUSTER_COUNT = 1
  MAX_CLUSTER_COUNT = 1
  SCALING_POLICY = 'STANDARD'
  INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Ripple v3 compute. X-Small, auto-suspend 60s, auto-resume on query.';

-- DBT_WH (warehouse)
-- Reconstructed from SHOW WAREHOUSES (GET_DDL not supported for warehouses).
-- This is the ACCOUNT default warehouse (is_default = Y).
CREATE WAREHOUSE IF NOT EXISTS DBT_WH
  WAREHOUSE_SIZE = 'XSMALL'
  WAREHOUSE_TYPE = 'STANDARD'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  MIN_CLUSTER_COUNT = 1
  MAX_CLUSTER_COUNT = 1
  SCALING_POLICY = 'STANDARD'
  INITIALLY_SUSPENDED = TRUE;

-- COMPUTE_WH (warehouse)
-- Reconstructed from SHOW WAREHOUSES (GET_DDL not supported for warehouses).
CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH
  WAREHOUSE_SIZE = 'XSMALL'
  WAREHOUSE_TYPE = 'STANDARD'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  MIN_CLUSTER_COUNT = 1
  MAX_CLUSTER_COUNT = 1
  SCALING_POLICY = 'STANDARD'
  INITIALLY_SUSPENDED = TRUE;

-- RIPPLE_BUDGET (resource_monitor)
-- Reconstructed from SHOW RESOURCE MONITORS (GET_DDL not supported for resource monitors).
-- Level = ACCOUNT, so it is applied at the account level, not to a single warehouse.
CREATE RESOURCE MONITOR IF NOT EXISTS RIPPLE_BUDGET
  WITH
    CREDIT_QUOTA = 30
    FREQUENCY = MONTHLY
    START_TIMESTAMP = IMMEDIATELY
  TRIGGERS
    ON 75 PERCENT DO NOTIFY
    ON 90 PERCENT DO SUSPEND
    ON 100 PERCENT DO SUSPEND_IMMEDIATE;

-- Bind it to the account (matches level = ACCOUNT in SHOW RESOURCE MONITORS):
ALTER ACCOUNT SET RESOURCE_MONITOR = RIPPLE_BUDGET;

-- CLAUDE_MCP_READONLY (role)
-- Reconstructed from SHOW ROLES (GET_DDL not supported for roles). Grants NOT captured here.
CREATE ROLE IF NOT EXISTS CLAUDE_MCP_READONLY
  COMMENT = 'Read-only role for Claude MCP integration';

-- RIPPLE_INGEST_RW (role)
-- Reconstructed from SHOW ROLES (GET_DDL not supported for roles). Grants NOT captured here.
CREATE ROLE IF NOT EXISTS RIPPLE_INGEST_RW
  COMMENT = 'Intake loader: write landing tables + ingest receipts. Least privilege, used by GitHub Actions.';

-- RIPPLE_LOADER (role)
-- Reconstructed from SHOW ROLES (GET_DDL not supported for roles). Grants NOT captured here.
CREATE ROLE IF NOT EXISTS RIPPLE_LOADER
  COMMENT = 'Least-privilege pipeline role: read + append to RIPPLE.RAW + Cortex.';

-- RIPPLE_ROLE (role)
-- Reconstructed from SHOW ROLES (GET_DDL not supported for roles). Grants NOT captured here.
CREATE ROLE IF NOT EXISTS RIPPLE_ROLE
  COMMENT = 'Application role for Ripple v3 - ingestion, synthesis, dbt, web app.';

-- RIPPLE_TRANSFORM_RW (role)
-- Reconstructed from SHOW ROLES (GET_DDL not supported for roles). Grants NOT captured here.
CREATE ROLE IF NOT EXISTS RIPPLE_TRANSFORM_RW
  COMMENT = 'dbt transform: read RAW landing + META, build STAGING and MARTS. Least privilege, used by GitHub Actions.';

