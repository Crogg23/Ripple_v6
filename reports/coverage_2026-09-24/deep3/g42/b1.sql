-- @S01 ZCTA shape: distinct ZIP areas vs rows, leading zeros, load runs, land/water totals
SELECT COUNT(*) n, COUNT(DISTINCT zcta5ce20) d_zcta, COUNT(DISTINCT geoid20) d_geoid, COUNT(DISTINCT affgeoid20) d_aff,
       COUNT_IF(zcta5ce20 <> geoid20) zcta_ne_geoid, COUNT_IF(LENGTH(zcta5ce20) <> 5) bad_len,
       COUNT_IF(LEFT(zcta5ce20, 1) = '0') lead_zero, MIN(zcta5ce20) z_min, MAX(zcta5ce20) z_max,
       ARRAY_AGG(DISTINCT vintage) vint, ARRAY_AGG(DISTINCT lsad20) lsad,
       COUNT(DISTINCT _source_run_id) runs, COUNT(DISTINCT _src_sha256) shas, COUNT(DISTINCT _ingested_at) stamps,
       COUNT_IF(geometry IS NULL) geom_null, COUNT_IF(TRY_TO_NUMBER(aland20) IS NULL) aland_bad,
       COUNT_IF(TRY_TO_NUMBER(aland20) = 0) zero_land,
       ROUND(SUM(TRY_TO_NUMBER(aland20)) / 1e6) land_km2, ROUND(SUM(TRY_TO_NUMBER(awater20)) / 1e6) water_km2
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_ZCTA;

-- @S02 ZCTA repeats: how many rows each ZIP area has, and whether the repeats differ in shape or land size
WITH z AS (
  SELECT zcta5ce20 z, COUNT(*) n, COUNT(DISTINCT ST_NPOINTS(geometry)) shapes,
         COUNT(DISTINCT aland20) alands, COUNT(DISTINCT _source_run_id) runs
  FROM LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_ZCTA GROUP BY 1)
SELECT n rows_per_zcta, COUNT(*) zctas, SUM(n) total_rows, MAX(shapes) max_shapes, MAX(alands) max_alands,
       MAX(runs) max_runs, MIN(z) example_lo, MAX(z) example_hi
FROM z GROUP BY n ORDER BY n;

-- @S03 ZCTA completeness: the core ZIP-to-county crosswalk vs this map, both directions
WITH m AS (SELECT DISTINCT zcta5ce20 z FROM LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_ZCTA),
     x AS (SELECT DISTINCT LPAD(zcta5::string, 5, '0') z FROM LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY)
SELECT (SELECT COUNT(*) FROM m) map_zctas, (SELECT COUNT(*) FROM x) xwalk_zctas,
       (SELECT COUNT(*) FROM x JOIN m ON m.z = x.z) both_,
       (SELECT COUNT(*) FROM x LEFT JOIN m ON m.z = x.z WHERE m.z IS NULL) xwalk_not_in_map,
       (SELECT COUNT(*) FROM m LEFT JOIN x ON x.z = m.z WHERE x.z IS NULL) map_not_in_xwalk,
       (SELECT ARRAY_AGG(DISTINCT vintage) FROM LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY) xwalk_vintages,
       (SELECT ARRAY_AGG(DISTINCT xwalk_type) FROM LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY) xwalk_types;

-- @S04 ROR shape: rows vs ROR IDs, and whether each *_IDS_ALL list contains that row's own main ID
WITH r AS (
  SELECT ror_id, display_name, status, _source_run_id, _loaded_at, _src_sha256, record_created_date, continent_code, continent_name,
         NULLIF(NULLIF(TRIM(grid_id), ''), 'None') g1, NULLIF(NULLIF(TRIM(grid_ids_all), ''), 'None') ga,
         NULLIF(NULLIF(TRIM(isni_id), ''), 'None') i1, NULLIF(NULLIF(TRIM(isni_ids_all), ''), 'None') ia,
         NULLIF(NULLIF(TRIM(wikidata_id), ''), 'None') w1, NULLIF(NULLIF(TRIM(wikidata_ids_all), ''), 'None') wa
  FROM LIBRARY_MARTS.REFERENCE.REFERENCE__XC_ROR_RESEARCH_ORGANIZATIONS)
SELECT COUNT(*) n, COUNT(DISTINCT ror_id) d_ror, COUNT(DISTINCT display_name) d_name,
       COUNT(g1) grid_main, COUNT(ga) grid_all, COUNT(DISTINCT g1) d_grid_main, COUNT(DISTINCT ga) d_grid_all,
       COUNT_IF(g1 IS NOT NULL AND CONTAINS(ga, g1)) grid_main_in_all, COUNT_IF(g1 IS NOT NULL AND (ga IS NULL OR NOT CONTAINS(ga, g1))) grid_main_missing,
       COUNT_IF(g1 IS NULL AND ga IS NOT NULL) grid_all_no_main,
       COUNT(i1) isni_main, COUNT(ia) isni_all, COUNT(DISTINCT i1) d_isni_main, COUNT(DISTINCT ia) d_isni_all,
       COUNT_IF(i1 IS NOT NULL AND CONTAINS(ia, i1)) isni_main_in_all, COUNT_IF(i1 IS NULL AND ia IS NOT NULL) isni_all_no_main,
       COUNT(w1) wd_main, COUNT(wa) wd_all, COUNT(DISTINCT w1) d_wd_main, COUNT(DISTINCT wa) d_wd_all,
       COUNT_IF(w1 IS NOT NULL AND CONTAINS(wa, w1)) wd_main_in_all, COUNT_IF(w1 IS NULL AND wa IS NOT NULL) wd_all_no_main,
       ARRAY_AGG(DISTINCT status) statuses, COUNT(DISTINCT _source_run_id) runs, COUNT(DISTINCT _loaded_at) stamps,
       COUNT(DISTINCT _src_sha256) shas, MIN(record_created_date)::string c0, MAX(record_created_date)::string c1,
       SYSTEM$TYPEOF(MAX(record_created_date)) ctype,
       COUNT_IF(continent_code IS NULL OR TRIM(continent_code) = '') cont_blank, COUNT_IF(continent_name = 'North America') north_am
FROM r;

-- @S05 ROR: the three most-repeated values in each *_IDS_ALL column, with how many different orgs share them
WITH r AS (
  SELECT ror_id, display_name, country_code,
         NULLIF(NULLIF(TRIM(grid_ids_all), ''), 'None') ga, NULLIF(NULLIF(TRIM(isni_ids_all), ''), 'None') ia,
         NULLIF(NULLIF(TRIM(wikidata_ids_all), ''), 'None') wa
  FROM LIBRARY_MARTS.REFERENCE.REFERENCE__XC_ROR_RESEARCH_ORGANIZATIONS),
u AS (
  SELECT 'GRID' k, ga v, ror_id, display_name, country_code FROM r WHERE ga IS NOT NULL
  UNION ALL SELECT 'ISNI', ia, ror_id, display_name, country_code FROM r WHERE ia IS NOT NULL
  UNION ALL SELECT 'WIKIDATA', wa, ror_id, display_name, country_code FROM r WHERE wa IS NOT NULL),
g AS (
  SELECT k, v, COUNT(*) n, COUNT(DISTINCT ror_id) rors, COUNT(DISTINCT country_code) countries,
         MIN(display_name) name_a, MAX(display_name) name_z
  FROM u GROUP BY k, v)
SELECT k, LENGTH(v) v_len, LEFT(v, 140) v_head, n, rors, countries, name_a, name_z,
       SUM(IFF(n > 1, 1, 0)) OVER (PARTITION BY k) values_shared, SUM(IFF(n > 1, n, 0)) OVER (PARTITION BY k) rows_on_shared
FROM g QUALIFY ROW_NUMBER() OVER (PARTITION BY k ORDER BY n DESC) <= 3 ORDER BY k, n DESC;

-- @S06 ITIS trio shape: rows vs keys, duplicate loads, date ranges
SELECT 'TU_COMMENTS_LINKS' t, COUNT(*) n, COUNT(DISTINCT itis_tu_comments_links_key) d_key, COUNT(DISTINCT tsn) d_a,
       COUNT(DISTINCT comment_id) d_b, COUNT(DISTINCT tsn, comment_id) d_content, COUNT(DISTINCT _source_run_id) runs,
       COUNT(DISTINCT _src_sha256) shas, MIN(update_date)::string date0, MAX(update_date)::string date1, MAX(_loaded_at)::string loaded
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TU_COMMENTS_LINKS
UNION ALL
SELECT 'COMMENTS', COUNT(*), COUNT(DISTINCT comment_id), COUNT(DISTINCT commentator), COUNT(DISTINCT HASH(comment_detail)),
       COUNT(DISTINCT HASH(commentator, comment_detail, comment_time_stamp)), COUNT(DISTINCT _source_run_id),
       COUNT(DISTINCT _src_sha256), MIN(comment_time_stamp)::string, MAX(comment_time_stamp)::string, MAX(_loaded_at)::string
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_COMMENTS
UNION ALL
SELECT 'PUBLICATIONS', COUNT(*), COUNT(DISTINCT itis_publications_key), COUNT(DISTINCT publication_id),
       COUNT_IF(TRY_TO_DATE(listed_pub_date::string) > CURRENT_DATE() OR TRY_TO_DATE(actual_pub_date::string) > CURRENT_DATE()),
       COUNT(DISTINCT HASH(reference_author, title, publication_name, listed_pub_date, pages)), COUNT(DISTINCT _source_run_id),
       COUNT(DISTINCT _src_sha256), MIN(listed_pub_date)::string, MAX(listed_pub_date)::string, MAX(_loaded_at)::string
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_PUBLICATIONS;

-- @S07 ITIS link integrity: comment links to missing comments or missing species; comments and publications nobody cites
WITH l AS (SELECT DISTINCT tsn, comment_id FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TU_COMMENTS_LINKS),
     c AS (SELECT DISTINCT comment_id FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_COMMENTS),
     t AS (SELECT DISTINCT tsn FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS),
     p AS (SELECT DISTINCT publication_id FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_PUBLICATIONS),
     rl AS (SELECT DISTINCT documentation_id FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_REFERENCE_LINKS WHERE TRIM(doc_id_prefix) = 'PUB')
SELECT (SELECT COUNT(*) FROM l) link_pairs,
       (SELECT COUNT(*) FROM l LEFT JOIN c ON c.comment_id = l.comment_id WHERE c.comment_id IS NULL) links_to_missing_comment,
       (SELECT COUNT(*) FROM l LEFT JOIN t ON t.tsn = l.tsn WHERE t.tsn IS NULL) links_to_missing_species,
       (SELECT COUNT(*) FROM c LEFT JOIN (SELECT DISTINCT comment_id FROM l) lc ON lc.comment_id = c.comment_id WHERE lc.comment_id IS NULL) comments_never_linked,
       (SELECT COUNT(*) FROM p) pubs,
       (SELECT COUNT(*) FROM p LEFT JOIN rl ON rl.documentation_id = p.publication_id WHERE rl.documentation_id IS NULL) pubs_never_cited,
       (SELECT COUNT(*) FROM rl LEFT JOIN p ON p.publication_id = rl.documentation_id WHERE p.publication_id IS NULL) cited_pub_ids_missing;

-- @S08 ITIS comments by year written: bulk imports vs steady curation, and the lead writer each year
SELECT YEAR(comment_time_stamp) yr, COUNT(*) n, COUNT(DISTINCT commentator) writers, MODE(commentator) top_writer,
       COUNT_IF(commentator = 'DSMZ') dsmz, MIN(comment_time_stamp)::string first_ts, MAX(comment_time_stamp)::string last_ts,
       COUNT(DISTINCT comment_time_stamp) distinct_ts
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_COMMENTS GROUP BY 1 ORDER BY 1;
