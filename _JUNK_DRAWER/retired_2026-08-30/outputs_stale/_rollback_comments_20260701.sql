-- Rollback of comments as they were before 2026-07-01 housekeeping.

COMMENT ON DATABASE LIBRARY_MARTS IS 'Ripple: analytics marts';
COMMENT ON DATABASE LIBRARY_META IS 'Ripple: source registry + ingest logs';
COMMENT ON DATABASE LIBRARY_RAW IS 'Ripple: raw landing zone';
COMMENT ON DATABASE LIBRARY_STAGING IS 'Ripple: dbt staging';
COMMENT ON DATABASE LIBRARY_TOOLS IS 'Container for agent tooling (Claude MCP server). No data -- do not drop.';
COMMENT ON SCHEMA LIBRARY_RAW.LANDING IS 'Loading dock: raw-faithful landing tables, one per registry source_id. Current snapshot only — history lives in INGEST_RUNS + preserved raw files.';
COMMENT ON TABLE LIBRARY_META.REGISTRY.PORTAL_DATASET_INDEX IS 'Wave-3 master index of harvested open-data-portal datasets (metadata only). One row = one dataset. column_names is the source column list; join_keys/top_tier (added post-load) confidence-tier what each dataset connects to.';
