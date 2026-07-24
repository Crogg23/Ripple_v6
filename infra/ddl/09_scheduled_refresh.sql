-- Server-side scheduled refresh (Phase 5): keep owned copies fresh unattended, in
-- the cloud (not on a laptop). First load = client (scripts/server_side_load.py,
-- discovers schema). Refresh = these server-side objects, driven by a TASK.
--
-- Chain: TASK RIPPLE_BULK_REFRESH_TASK -> RIPPLE_REFRESH_ENABLED() -> per source
--        RIPPLE_REFRESH_SOURCE(sid): re-fetch (RIPPLE_FETCH_TO_STAGE) -> content
--        change check (origin ETag/Last-Modified) -> COPY -> never-shrink guard ->
--        atomic swap -> INGEST_RUNS log.
-- Only non-resolver / non-keyed sources are SCHEDULABLE (others still need the client).
-- Everything is opt-in: the TASK is created SUSPENDED, and each source is ENABLED=FALSE
-- until turned on. All objects are DROP-able (teardown at bottom).

-- 1. Control table: the refresh config the server-side proc reads (schema known from
--    first load => no header re-parse). Written by server_side_load.py on each success.
CREATE TABLE IF NOT EXISTS LIBRARY_META.REGISTRY.BULK_REFRESH (
  SOURCE_ID        VARCHAR NOT NULL,
  URL              VARCHAR COMMENT 'Direct download URL used on refresh (resolver/keyed sources are NOT schedulable server-side).',
  KIND             VARCHAR COMMENT 'csv | zip',
  MEMBER_PATTERN   VARCHAR COMMENT 'zip member regex ("" = largest)',
  DELIMITER        VARCHAR DEFAULT ',',
  HAS_HEADER       BOOLEAN DEFAULT TRUE,
  COLUMNS          ARRAY   COMMENT 'Ordered source column names discovered at first load.',
  SCHEDULABLE      BOOLEAN DEFAULT TRUE COMMENT 'FALSE when the source needs the client loader (resolver hop or keyed auth).',
  ENABLED          BOOLEAN DEFAULT FALSE COMMENT 'Whether the refresh TASK should include this source (opt-in).',
  CADENCE_BUCKET   VARCHAR,
  LAST_REFRESH_AT  TIMESTAMP_NTZ,
  UPDATED_AT       TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
  CONSTRAINT PK_BULK_REFRESH PRIMARY KEY (SOURCE_ID)
)
COMMENT = 'Control table for server-side scheduled refresh of bulk sources (Phase 5).';

-- 2. Per-source refresh proc. Re-runs the pipeline server-side from the known schema,
--    with an ETag-based unchanged-skip and a never-shrink swap guard.
--    (Authoritative body maintained in the account; see git history for full text.)
--    Signature: RIPPLE_REFRESH_SOURCE(SOURCE_ID STRING) RETURNS STRING (JSON status).

-- 3. Driver proc: refresh every ENABLED + SCHEDULABLE source.
--    Signature: RIPPLE_REFRESH_ENABLED() RETURNS STRING (JSON summary).

-- NOTE: the two Python proc bodies (RIPPLE_REFRESH_SOURCE, RIPPLE_REFRESH_ENABLED)
-- are created live via scripts/server_side_load.py's companion DDL and are large;
-- they are intentionally not duplicated here to avoid drift. Recreate from the
-- account (GET_DDL) or the session that provisioned them if rebuilding from scratch.

-- 4. The scheduler: daily at 08:00 UTC on COMPUTE_WH. Created SUSPENDED. To activate:
--      ALTER TASK LIBRARY_META.REGISTRY.RIPPLE_BULK_REFRESH_TASK RESUME;
--    and enable specific sources:
--      UPDATE LIBRARY_META.REGISTRY.BULK_REFRESH SET ENABLED = TRUE WHERE SOURCE_ID = '...';
CREATE TASK IF NOT EXISTS LIBRARY_META.REGISTRY.RIPPLE_BULK_REFRESH_TASK
  WAREHOUSE = COMPUTE_WH
  SCHEDULE = 'USING CRON 0 8 * * * UTC'
  COMMENT = 'Daily server-side refresh of ENABLED bulk sources (Phase 5). Created SUSPENDED; RESUME to activate.'
AS
  CALL LIBRARY_META.REGISTRY.RIPPLE_REFRESH_ENABLED();

-- Teardown (reversibility):
--   DROP TASK      IF EXISTS LIBRARY_META.REGISTRY.RIPPLE_BULK_REFRESH_TASK;
--   DROP PROCEDURE IF EXISTS LIBRARY_META.REGISTRY.RIPPLE_REFRESH_ENABLED();
--   DROP PROCEDURE IF EXISTS LIBRARY_META.REGISTRY.RIPPLE_REFRESH_SOURCE(STRING);
--   DROP TABLE     IF EXISTS LIBRARY_META.REGISTRY.BULK_REFRESH;
