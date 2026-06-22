-- ============================================================================
-- Wave 3 — example queries against the master portal-dataset index.
--
-- Table: LIBRARY_META.REGISTRY.PORTAL_DATASET_INDEX  (one row = one dataset)
--   column_names ARRAY  — the dataset's source column list (NULL = not exposed)
--   join_keys    ARRAY  — which join keys its columns carry (NULL = unassessable)
--   top_tier     STRING — strongest tier present: STEEL > STRONG > GEO >
--                         PROBABILISTIC ; 'NONE' = columns known but no key ;
--                         NULL = columns not exposed by the source (untaggable)
--
-- This is "step 3 of the peel" as a SQL query: find what connects to what.
-- Counts in the comments are the locally-verified values from the source index
-- (tag_portal_index.py --local) — the Snowflake queries return the same once the
-- table is loaded.
-- ============================================================================


-- [1] EVERY DATASET CARRYING EIN  — the org backbone (nonprofits/businesses).
--     Expected: 30 datasets.
SELECT portal_name, dataset_title, source_url, column_names
FROM LIBRARY_META.REGISTRY.PORTAL_DATASET_INDEX
WHERE ARRAY_CONTAINS('EIN'::VARIANT, join_keys)
ORDER BY portal_name, dataset_title;


-- [2] EVERY STEEL-TIER DATASET  — the precise, hard-ID connectable set.
--     Expected: 185 datasets (CCN, NPI, EIN, PATENT, DUNS, UEI).
SELECT portal_name, dataset_title, join_keys, source_url
FROM LIBRARY_META.REGISTRY.PORTAL_DATASET_INDEX
WHERE top_tier = 'STEEL'
ORDER BY portal_name, dataset_title;


-- [3] DATASETS BY PORTAL, RANKED  — which boxes are richest.
--     96 portals; the top ones are capped at 25,000 (the Wave-2 per-portal
--     harvest cap — those are floors, not true portal totals).
SELECT portal_name,
       platform,
       COUNT(*)                                             AS datasets,
       COUNT_IF(column_names IS NOT NULL)                   AS with_columns,
       COUNT_IF(top_tier = 'STEEL')                         AS steel,
       COUNT_IF(top_tier IN ('STEEL','STRONG','GEO','PROBABILISTIC')) AS carries_key
FROM LIBRARY_META.REGISTRY.PORTAL_DATASET_INDEX
GROUP BY portal_name, platform
ORDER BY datasets DESC;


-- [4] DATASETS CARRYING BOTH A GEO KEY AND A STEEL KEY  — cross-joinable gold.
--     A steel ID pins the entity; a geo key drops it on the map. top_tier='STEEL'
--     guarantees a steel key is present (steel is strongest), so we only need to
--     also require a geo key in join_keys.
--     Expected: 145 datasets.
SELECT portal_name, dataset_title, join_keys, source_url
FROM LIBRARY_META.REGISTRY.PORTAL_DATASET_INDEX
WHERE top_tier = 'STEEL'
  AND ARRAYS_OVERLAP(join_keys, ARRAY_CONSTRUCT('FIPS','ZIP','LATLON','COUNTRY','GEOM'))
ORDER BY portal_name, dataset_title;


-- ----------------------------------------------------------------------------
-- Bonus: the headline tier distribution (sanity check after load).
--   Expected: STEEL 185 | STRONG 563 | GEO 47,438 | PROBABILISTIC 9,834
--             NONE 20,631 | (NULL = columns unknown) 259,869 | total 338,520
-- ----------------------------------------------------------------------------
SELECT COALESCE(top_tier, 'UNKNOWN_COLUMNS') AS tier,
       COUNT(*)                              AS datasets
FROM LIBRARY_META.REGISTRY.PORTAL_DATASET_INDEX
GROUP BY 1
ORDER BY datasets DESC;
