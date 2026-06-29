-- The data-freshness ledger (Phase 0 keystone). Populated by scripts/build_freshness_ledger.py --apply.

CREATE TABLE IF NOT EXISTS LIBRARY_META.REGISTRY.SOURCE_FRESHNESS (
    SOURCE_ID         VARCHAR        NOT NULL COMMENT 'FK to REGISTRY.SOURCE_REGISTRY; landing table = LIBRARY_RAW.LANDING.<UPPER(SOURCE_ID)>',
    LANDING_FQN       VARCHAR        COMMENT 'Fully-qualified landing table measured',
    RECENCY_COL       VARCHAR        COMMENT 'The data-ABOUT column whose MAX gives recency (event/period/filing date). NULL = no such column exists. NEVER a load-stamp (_INGESTED_AT/_SOURCE_RUN_ID/_SRC_SHA256/_LOADED_AT/SRC_SHA256).',
    RECENCY_KIND      VARCHAR        COMMENT 'date | timestamp | yyyymmdd_text | year_text | year_int | mixed | none -- how RECENCY_COL was parsed',
    DATA_THROUGH_ISO  DATE           COMMENT 'MAX(parsed RECENCY_COL). Year-grain encoded as YYYY-12-31; current-year sources are intentionally future-dated (e.g. 2026-12-31). NULL = unmeasurable.',
    ROW_COUNT         NUMBER(38,0)   COMMENT 'Landed row count at measure time (0/degenerate => dead)',
    CADENCE_BUCKET    VARCHAR        COMMENT 'daily | weekly | monthly | quarterly | annual | irregular | static | real_time | unknown',
    FRESHNESS_STATE   VARCHAR        COMMENT 'fresh | due | overdue | stale | dead | unknown -- snapshot derived at LAST_MEASURED_AT (the live value lives in V_SOURCE_FRESHNESS)',
    LAST_MEASURED_AT  TIMESTAMP_NTZ  DEFAULT CURRENT_TIMESTAMP() COMMENT 'When recency was last measured by the Python builder',
    NOTE              VARCHAR        COMMENT 'Quirks: traps avoided, sentinels NULLIFed, partial loads, discontinued-upstream, etc.',
    CONSTRAINT PK_SOURCE_FRESHNESS PRIMARY KEY (SOURCE_ID)
)
COMMENT = 'Data-freshness ledger: measures how current each landed source DATA is (not when it was loaded). Kills the load-stamp-vs-data-stamp bug (e.g. NOAA AIS: recent load, Jan-2024 data).';;

CREATE OR REPLACE VIEW LIBRARY_META.REGISTRY.V_SOURCE_FRESHNESS AS
WITH last_run AS (
    SELECT
        SOURCE_ID,
        RUN_ID                                     AS LAST_RUN_ID,
        STATUS                                     AS LAST_RUN_STATUS,
        COALESCE(ENDED_AT, STARTED_AT, _LOADED_AT) AS LAST_RUN_AT,
        ROW_COUNT                                  AS LAST_RUN_ROWS,
        SHA256                                     AS LAST_RUN_SHA256
    FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY SOURCE_ID
        ORDER BY COALESCE(ENDED_AT, STARTED_AT, _LOADED_AT) DESC NULLS LAST
    ) = 1
),
base AS (
    SELECT
        f.*,
        DATEDIFF('day', f.DATA_THROUGH_ISO, CURRENT_DATE()) AS DATA_AGE_DAYS
    FROM LIBRARY_META.REGISTRY.SOURCE_FRESHNESS f
)
SELECT
    b.SOURCE_ID,
    b.LANDING_FQN,
    b.RECENCY_COL,
    b.RECENCY_KIND,
    b.DATA_THROUGH_ISO,
    b.ROW_COUNT,
    b.CADENCE_BUCKET,
    b.DATA_AGE_DAYS,
    CASE
        WHEN COALESCE(b.ROW_COUNT, 0) = 0 THEN 'dead'
        WHEN b.CADENCE_BUCKET = 'static'  THEN 'fresh'
        WHEN b.DATA_THROUGH_ISO IS NULL   THEN COALESCE(b.FRESHNESS_STATE, 'unknown')
        WHEN b.CADENCE_BUCKET = 'unknown' THEN 'unknown'
        WHEN b.CADENCE_BUCKET = 'daily'     THEN CASE WHEN b.DATA_AGE_DAYS <= 3   THEN 'fresh' WHEN b.DATA_AGE_DAYS <= 5   THEN 'due' WHEN b.DATA_AGE_DAYS <= 7   THEN 'overdue' ELSE 'stale' END
        WHEN b.CADENCE_BUCKET = 'real_time' THEN CASE WHEN b.DATA_AGE_DAYS <= 4   THEN 'fresh' WHEN b.DATA_AGE_DAYS <= 10  THEN 'due' WHEN b.DATA_AGE_DAYS <= 30  THEN 'overdue' ELSE 'stale' END
        WHEN b.CADENCE_BUCKET = 'weekly'    THEN CASE WHEN b.DATA_AGE_DAYS <= 11  THEN 'fresh' WHEN b.DATA_AGE_DAYS <= 17  THEN 'due' WHEN b.DATA_AGE_DAYS <= 21  THEN 'overdue' ELSE 'stale' END
        WHEN b.CADENCE_BUCKET = 'monthly'   THEN CASE WHEN b.DATA_AGE_DAYS <= 40  THEN 'fresh' WHEN b.DATA_AGE_DAYS <= 55  THEN 'due' WHEN b.DATA_AGE_DAYS <= 75  THEN 'overdue' ELSE 'stale' END
        WHEN b.CADENCE_BUCKET = 'quarterly' THEN CASE WHEN b.DATA_AGE_DAYS <= 100 THEN 'fresh' WHEN b.DATA_AGE_DAYS <= 125 THEN 'due' WHEN b.DATA_AGE_DAYS <= 150 THEN 'overdue' ELSE 'stale' END
        WHEN b.CADENCE_BUCKET = 'annual'    THEN CASE WHEN b.DATA_AGE_DAYS <= 400 THEN 'fresh' WHEN b.DATA_AGE_DAYS <= 425 THEN 'due' WHEN b.DATA_AGE_DAYS <= 450 THEN 'overdue' ELSE 'stale' END
        WHEN b.CADENCE_BUCKET = 'irregular' THEN CASE WHEN b.DATA_AGE_DAYS <= 270 THEN 'fresh' WHEN b.DATA_AGE_DAYS <= 455 THEN 'due' WHEN b.DATA_AGE_DAYS <= 730 THEN 'overdue' ELSE 'stale' END
        ELSE 'unknown'
    END AS FRESHNESS_STATE,
    b.FRESHNESS_STATE                                   AS FRESHNESS_STATE_AT_MEASURE,
    b.LAST_MEASURED_AT,
    lr.LAST_RUN_ID,
    lr.LAST_RUN_AT,
    lr.LAST_RUN_STATUS,
    lr.LAST_RUN_ROWS,
    DATEDIFF('day', b.DATA_THROUGH_ISO, lr.LAST_RUN_AT) AS LOAD_MINUS_DATA_DAYS,
    b.NOTE
FROM base b
LEFT JOIN last_run lr ON lr.SOURCE_ID = b.SOURCE_ID;;
