create or replace view CATALOG(
	SOURCE_ID,
	NAME,
	DOMAIN_PRIMARY,
	DOMAIN_SECONDARY,
	JURISDICTION,
	ENTITY_TYPES,
	JOIN_KEYS_STD,
	JOIN_KEY_TIER,
	JOIN_KEY_TIER_PROVISIONAL,
	THEMES,
	HAS_EVENTS,
	PRIORITY_TIER,
	_REAL_MART,
	LIFECYCLE,
	LANDED_ROW_COUNT,
	MART_ROW_COUNT,
	RUN_ROWS,
	IS_SAMPLE,
	TRUST_LAYER,
	LANDING_FQN,
	IS_ORPHAN,
	URL,
	PUBLISHER,
	DESCRIPTION,
	LAST_INGESTED_AT
) as
WITH reg AS (
    SELECT *
    FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY LOWER(SOURCE_ID)
        ORDER BY IFF(SOURCE_ID = UPPER(SOURCE_ID), 0, 1), _LOADED_AT DESC
    ) = 1
),
latest_run AS (
    SELECT LOWER(SOURCE_ID) AS sid, STATUS, ROW_COUNT AS run_rows, MESSAGE, ENDED_AT
    FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS
    QUALIFY ROW_NUMBER() OVER (PARTITION BY LOWER(SOURCE_ID) ORDER BY ENDED_AT DESC, _LOADED_AT DESC) = 1
),
landed AS (
    SELECT LOWER(TABLE_NAME) AS sid, TABLE_NAME, ROW_COUNT AS land_rows
    FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='LANDING'
),
marts AS (
    SELECT LOWER(SPLIT_PART(TABLE_NAME,'__',2)) AS sid,
           SUM(ROW_COUNT) AS mart_rows,
           MAX(IFF(TABLE_TYPE='VIEW', 1, 0)) = 1 AS is_view
    FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
    WHERE POSITION('__' IN TABLE_NAME) > 0 AND TABLE_SCHEMA <> 'INFORMATION_SCHEMA'
    GROUP BY 1
),
staging AS (
    SELECT DISTINCT LOWER(SPLIT_PART(REGEXP_REPLACE(TABLE_NAME,'^STG_',''),'__',1)) AS sid
    FROM LIBRARY_STAGING.INFORMATION_SCHEMA.TABLES
    WHERE TABLE_NAME LIKE 'STG_%' AND POSITION('__' IN TABLE_NAME) > 0 AND TABLE_SCHEMA <> 'INFORMATION_SCHEMA'
),
probe AS (
    SELECT LOWER(SOURCE_ID) AS sid, NONEMPTY_RATIO
    FROM LIBRARY_META.REGISTRY.LANDING_DENSITY_PROBE
    QUALIFY ROW_NUMBER() OVER (PARTITION BY LOWER(SOURCE_ID) ORDER BY NONEMPTY_RATIO DESC) = 1
),
ids AS (
    SELECT LOWER(SOURCE_ID) AS sid FROM reg
    UNION SELECT sid FROM latest_run
    UNION SELECT sid FROM landed
),
flagged AS (
    SELECT i.sid,
           (m.sid IS NOT NULL AND (m.is_view OR NOT (
                COALESCE(m.mart_rows,0) <= 1
                OR (COALESCE(m.mart_rows,0) <= 3 AND COALESCE(l.land_rows,0) > COALESCE(m.mart_rows,0) * 4)
           ))) AS real_mart
    FROM ids i
    LEFT JOIN landed l ON l.sid = i.sid
    LEFT JOIN marts m  ON m.sid = i.sid
)
SELECT
    COALESCE(r.SOURCE_ID, i.sid) AS SOURCE_ID,
    COALESCE(r.NAME, UPPER(i.sid)) AS NAME,
    r.DOMAIN_PRIMARY, r.DOMAIN_SECONDARY, r.JURISDICTION,
    r.ENTITY_TYPES, r.JOIN_KEYS_STD, r.JOIN_KEY_TIER, r.JOIN_KEY_TIER_PROVISIONAL,
    r.THEMES, r.HAS_EVENTS, r.PRIORITY_TIER,
    f.real_mart AS _REAL_MART,
    CASE
        WHEN f.real_mart THEN 'modeled'
        WHEN lr.STATUS='success' AND l.land_rows IS NULL THEN 'stale'
        WHEN lr.STATUS='success' AND (
                 LOWER(lr.MESSAGE) LIKE 'bulk portal load%of % rows.'
              OR lr.run_rows IN (500,1000,2000,5000,10000,25000,50000,100000)
              OR ((LOWER(lr.MESSAGE) LIKE '%proof slice%' OR LOWER(lr.MESSAGE) LIKE '% sample%')
                   AND COALESCE(l.land_rows, lr.run_rows, 0) <= 200000)
             ) THEN 'sampled'
        WHEN lr.STATUS='success' AND dp.NONEMPTY_RATIO IS NOT NULL AND dp.NONEMPTY_RATIO < 0.02 THEN 'empty'
        WHEN lr.STATUS='success' THEN 'landed'
        WHEN lr.sid IS NULL AND l.land_rows IS NOT NULL THEN 'landed'
        WHEN lr.STATUS='failed' THEN 'failed'
        WHEN lr.STATUS='empty' THEN 'empty'
        WHEN lr.STATUS IS NOT NULL THEN 'failed'
        WHEN r.INCLUDE='Y' THEN 'queued'
        ELSE 'scouted'
    END AS LIFECYCLE,
    l.land_rows AS LANDED_ROW_COUNT,
    m.mart_rows AS MART_ROW_COUNT,
    lr.run_rows AS RUN_ROWS,
    -- IS_SAMPLE: true when the landing data is known or likely to be truncated.
    -- Original heuristic caught ingest runs with known sample-size row counts (<=100K)
    -- or messages mentioning "proof slice"/"sample". Added 2026-07-30: also flag any
    -- source whose landing table has EXACTLY 500,000 rows -- that's the portal bulk-load
    -- cap, and 35 modeled sources hit it. Without this flag, "entity X is not in dataset Y"
    -- reads as a fact when we simply never loaded the rest of Y.
    (COALESCE(lr.STATUS='success' AND (
         lr.run_rows IN (500,1000,2000,5000,10000,25000,50000,100000,500000)
      OR ((LOWER(lr.MESSAGE) LIKE '%proof slice%' OR LOWER(lr.MESSAGE) LIKE '% sample%')
           AND COALESCE(l.land_rows, lr.run_rows, 0) <= 200000)), FALSE)
     OR l.land_rows = 500000) AS IS_SAMPLE,
    CASE
        WHEN f.real_mart THEN 'mart'
        WHEN s.sid IS NOT NULL THEN 'staging'
        WHEN l.land_rows IS NOT NULL THEN 'raw'
        ELSE 'none'
    END AS TRUST_LAYER,
    'LIBRARY_RAW.LANDING.' || UPPER(i.sid) AS LANDING_FQN,
    IFF(r.SOURCE_ID IS NULL, TRUE, FALSE) AS IS_ORPHAN,
    r.URL, r.PUBLISHER, r.DESCRIPTION,
    lr.ENDED_AT AS LAST_INGESTED_AT
FROM ids i
JOIN flagged f          ON f.sid = i.sid
LEFT JOIN reg r         ON LOWER(r.SOURCE_ID) = i.sid
LEFT JOIN latest_run lr ON lr.sid = i.sid
LEFT JOIN landed l      ON l.sid  = i.sid
LEFT JOIN probe dp      ON dp.sid = i.sid
LEFT JOIN marts m       ON m.sid  = i.sid
LEFT JOIN staging s     ON s.sid  = i.sid;