-- deep3/g47: deep pass 3, 2026-09-24. Python door, QUERY_TAG 'deep3-2026-09-24'.
-- Every connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'.
-- Tables: REFERENCE__XC_OWID_FERTILITY, REFERENCE__CENSUS_CB_STATE, REF__DIM_STATE, REFERENCE__FED_USGS_TOPOVIEW, REFERENCE__FED_ITIS_TAXON_UNIT_TYPES.

-- S01  (95 rows, 5.6s)
-- S01 where the five tables live and what columns they carry
SELECT table_schema, table_name, column_name, data_type, ordinal_position
FROM LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
WHERE table_name IN ('REFERENCE__XC_OWID_FERTILITY','REFERENCE__CENSUS_CB_STATE','REF__DIM_STATE',
                     'REFERENCE__FED_USGS_TOPOVIEW','REFERENCE__FED_ITIS_TAXON_UNIT_TYPES')
ORDER BY table_name, ordinal_position;

-- S02  (19402 rows, 1.2s)
-- S02 fertility: pull the whole REFERENCE copy (19.4K rows, 4 text columns) to rank locally
SELECT entity, code, year, total_fertility_rate
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__XC_OWID_FERTILITY;

-- S03  (1 rows, 0.6s)
-- S03 fertility: REFERENCE copy (text) vs TIMELINE copy (float): row counts, cast failures, value disagreements
WITH r AS (SELECT entity, code, TRY_TO_NUMBER(year) yr, total_fertility_rate tfr_txt,
                  TRY_TO_DOUBLE(total_fertility_rate) tfr
           FROM LIBRARY_MARTS.REFERENCE.REFERENCE__XC_OWID_FERTILITY),
t AS (SELECT entity, code, year yr, total_fertility_rate tfr
      FROM LIBRARY_MARTS.TIMELINE.REFERENCE__XC_OWID_FERTILITY)
SELECT (SELECT COUNT(*) FROM r) r_rows, (SELECT COUNT(*) FROM t) t_rows,
       (SELECT COUNT(*) FROM (SELECT entity, yr FROM r GROUP BY 1,2 HAVING COUNT(*)>1)) r_dup_entity_year,
       (SELECT COUNT_IF(tfr IS NULL) FROM r) r_tfr_nocast,
       (SELECT COUNT_IF(yr IS NULL) FROM r) r_year_nocast,
       (SELECT COUNT_IF(tfr_txt ILIKE 'nan' OR tfr_txt = '') FROM r) r_nan_or_blank,
       (SELECT COUNT(*) FROM r JOIN t ON r.entity=t.entity AND r.yr=t.yr) joined,
       (SELECT COUNT_IF(ABS(r.tfr - t.tfr) > 0.0005) FROM r JOIN t ON r.entity=t.entity AND r.yr=t.yr) value_diff,
       (SELECT MIN(yr)||'-'||MAX(yr) FROM r) r_years;

-- S04  (ran; fetch failed in Python: 'Python int too large to convert to C int' -- _INGESTED_AT holds an out-of-range timestamp; rerun as S05)
SELECT COALESCE(c.statefp, d.state_fips) fips, c.stusps, d.state_abbr, c.name cb_name, d.state_name dim_name,
       d.census_region, d.census_division, c.lsad, c.geoid, c.vintage,
       TRY_TO_NUMBER(c.aland) aland_m2, TRY_TO_NUMBER(c.awater) awater_m2,
       c._source_run_id, c._ingested_at, ST_NPOINTS(c.geometry) geom_points,
       LENGTH(d.state_fips) dim_fips_len
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_STATE c
FULL OUTER JOIN LIBRARY_MARTS.REFERENCE.REF__DIM_STATE d ON d.state_fips = c.statefp
ORDER BY 1
;

-- S05  (56 rows, 0.4s)
-- S05 = S04 rerun with _INGESTED_AT read as text and as epoch seconds (the timestamp would not fetch)
SELECT COALESCE(c.statefp, d.state_fips) fips, c.stusps, d.state_abbr, c.name cb_name, d.state_name dim_name,
       d.census_region, d.census_division, c.lsad, c.geoid, c.vintage,
       TRY_TO_NUMBER(c.aland) aland_m2, TRY_TO_NUMBER(c.awater) awater_m2,
       c._source_run_id, c._ingested_at::string ingested_txt, DATE_PART(epoch_second, c._ingested_at) ingested_epoch, ST_NPOINTS(c.geometry) geom_points,
       LENGTH(d.state_fips) dim_fips_len
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_STATE c
FULL OUTER JOIN LIBRARY_MARTS.REFERENCE.REF__DIM_STATE d ON d.state_fips = c.statefp
ORDER BY 1;

-- S06  (compile error: invalid identifier _SOURCE_RUN_ID -- this table has no lineage columns at all; rerun as S07)
SELECT COUNT(*) n, COUNT(DISTINCT sourceid) ids, COUNT(DISTINCT title) titles, COUNT(DISTINCT downloadurl) urls,
       COUNT(DISTINCT sourceid, title, downloadurl, boundingbox) distinct_rows_4col,
       COUNT_IF(NULLIF(TRIM(mpdesc),'') IS NOT NULL) mpdesc_filled, COUNT_IF(NULLIF(TRIM(fileformat),'') IS NOT NULL) fmt_filled,
       COUNT_IF(NULLIF(TRIM(counties),'') IS NOT NULL) counties_filled, COUNT_IF(NULLIF(TRIM(mapscale),'') IS NOT NULL) scale_filled,
       COUNT_IF(NULLIF(TRIM(fips),'') IS NOT NULL) fips_filled, COUNT_IF(NULLIF(TRIM(state),'') IS NOT NULL) state_filled,
       COUNT_IF(NULLIF(TRIM(datasets),'') IS NOT NULL) datasets_filled,
       COUNT(DISTINCT state) states, COUNT(DISTINCT LEFT(publicationdate,4)) pub_years,
       MIN(LEFT(publicationdate,4)) pub0, MAX(LEFT(publicationdate,4)) pub1,
       MIN(datecreated) created0, MAX(datecreated) created1,
       COUNT(DISTINCT _source_run_id) runs,
       ARRAY_AGG(DISTINCT LEFT(publicationdate,4)) WITHIN GROUP (ORDER BY LEFT(publicationdate,4)) pub_year_list,
       (SELECT COUNT(*) FROM LIBRARY_MARTS.TIMELINE.REFERENCE__FED_USGS_TOPOVIEW) timeline_rows,
       (SELECT ARRAY_AGG(OBJECT_CONSTRUCT('id', sourceid, 'k', k, 'titles', t)) FROM
          (SELECT sourceid, COUNT(*) k, ARRAY_AGG(DISTINCT title) t FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_TOPOVIEW
           GROUP BY 1 HAVING COUNT(*)>1)) dup_ids,
       (SELECT ARRAY_AGG(OBJECT_CONSTRUCT('st', state, 'k', k)) FROM
          (SELECT state, COUNT(*) k FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_TOPOVIEW GROUP BY 1 ORDER BY 2 DESC LIMIT 8)) top_states,
       ANY_VALUE(title) sample_title
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_TOPOVIEW
;

-- S07  (1 rows, 0.8s)
-- S07 = S06 rerun without _SOURCE_RUN_ID (TopoView carries no lineage columns)
SELECT COUNT(*) n, COUNT(DISTINCT sourceid) ids, COUNT(DISTINCT title) titles, COUNT(DISTINCT downloadurl) urls,
       COUNT(DISTINCT sourceid, title, downloadurl, boundingbox) distinct_rows_4col,
       COUNT_IF(NULLIF(TRIM(mpdesc),'') IS NOT NULL) mpdesc_filled, COUNT_IF(NULLIF(TRIM(fileformat),'') IS NOT NULL) fmt_filled,
       COUNT_IF(NULLIF(TRIM(counties),'') IS NOT NULL) counties_filled, COUNT_IF(NULLIF(TRIM(mapscale),'') IS NOT NULL) scale_filled,
       COUNT_IF(NULLIF(TRIM(fips),'') IS NOT NULL) fips_filled, COUNT_IF(NULLIF(TRIM(state),'') IS NOT NULL) state_filled,
       COUNT_IF(NULLIF(TRIM(datasets),'') IS NOT NULL) datasets_filled,
       COUNT(DISTINCT state) states, COUNT(DISTINCT LEFT(publicationdate,4)) pub_years,
       MIN(LEFT(publicationdate,4)) pub0, MAX(LEFT(publicationdate,4)) pub1,
       MIN(datecreated) created0, MAX(datecreated) created1,
       ARRAY_AGG(DISTINCT LEFT(publicationdate,4)) WITHIN GROUP (ORDER BY LEFT(publicationdate,4)) pub_year_list,
       (SELECT COUNT(*) FROM LIBRARY_MARTS.TIMELINE.REFERENCE__FED_USGS_TOPOVIEW) timeline_rows,
       (SELECT ARRAY_AGG(OBJECT_CONSTRUCT('id', sourceid, 'k', k, 'titles', t)) FROM
          (SELECT sourceid, COUNT(*) k, ARRAY_AGG(DISTINCT title) t FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_TOPOVIEW
           GROUP BY 1 HAVING COUNT(*)>1)) dup_ids,
       (SELECT ARRAY_AGG(OBJECT_CONSTRUCT('st', state, 'k', k)) FROM
          (SELECT state, COUNT(*) k FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_TOPOVIEW GROUP BY 1 ORDER BY 2 DESC LIMIT 8)) top_states,
       ANY_VALUE(title) sample_title
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_TOPOVIEW;

-- S08  (250 rows, 0.3s)
-- S08 TopoView: pull all 250 titles, publication dates and sizes to see what the sample covers
SELECT title, LEFT(publicationdate,4) pub_year, filesize, LEFT(datecreated,10) created, LEFT(lastupdated,10) updated, boundingbox
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_TOPOVIEW;

-- S09  (182 rows, 0.4s)
-- S09 ITIS rank types: pull all 182 rows to confirm it is a rank lookup and check key, parent links and update dates
SELECT itis_taxon_unit_types_key, kingdom_id, rank_id, rank_name, dir_parent_rank_id, req_parent_rank_id, update_date,
       _source_run_id, _src_sha256, _loaded_at::string loaded_txt
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXON_UNIT_TYPES
ORDER BY kingdom_id, rank_id;

-- Total: 9 warehouse statements (S01-S09). S04 ran but its result would not fetch; S06 failed to compile. Both counted.
-- Local work, no warehouse statements: g47/fert.py, fert2.py, fert3.py (fertility ranking from S02.csv), g47/small.py (TopoView + ITIS from S08/S09 csv).
