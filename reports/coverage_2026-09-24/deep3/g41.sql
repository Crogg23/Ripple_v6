-- deep3/g41: deep pass 3, 2026-09-24. Python door (connect/db.py), read-only SELECT/WITH only, QUERY_TAG 'deep3-2026-09-24'.
-- Every connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'. Those two are not counted.
-- Tables: ENVIRONMENT__XC_OWID_FOSSIL_SHARE, ENVIRONMENT__XC_OWID_TEMP_ANOMALY, REFERENCE__FED_USGS_GNIS_ALL_NAMES, REFERENCE__INTL_EG_CAPMAS, REFERENCE__FED_ITIS_VERNACULARS.
-- Statements below in run order, numbered by the runner (g41/run.py). Raw results: g41/qNN.json.

-- [q01] statement 1
-- q01 EG CAPMAS: dump all 52 rows to confirm the failed pull
SELECT * FROM LIBRARY_MARTS.REFERENCE.REFERENCE__INTL_EG_CAPMAS;

-- [q04] statement 2
-- q04 ITIS vernaculars: lookup check. By language: rows, species IDs, name IDs, approved flag, update-date range, duplicate name rows
SELECT LANGUAGE, COUNT(*) n, COUNT(DISTINCT TSN) tsns, COUNT(DISTINCT VERN_ID) vern_ids,
       COUNT(DISTINCT ITIS_VERNACULARS_KEY) keys, COUNT(DISTINCT TSN, VERNACULAR_NAME) tsn_name_pairs,
       COUNT_IF(APPROVED_IND = 'Y') appr_y, COUNT_IF(APPROVED_IND = 'N') appr_n, COUNT_IF(APPROVED_IND NOT IN ('Y','N') OR APPROVED_IND IS NULL) appr_other,
       MIN(UPDATE_DATE) u0, MAX(UPDATE_DATE) u1, COUNT(DISTINCT _SOURCE_RUN_ID) runs, COUNT(DISTINCT _SRC_SHA256) files
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_VERNACULARS
GROUP BY ROLLUP(LANGUAGE) ORDER BY n DESC;

-- [q05] statement 3
-- q05 GNIS all names: shape. Official vs variant, features, citation ids, date sentinels, load runs
SELECT FEATURE_NAME_OFFICIAL, COUNT(*) n, COUNT(DISTINCT FEATURE_ID) features, COUNT(DISTINCT NAME_CITATION_ID) cit_ids,
       COUNT(DISTINCT FEATURE_ID, FEATURE_NAME) feat_names,
       MIN(PUBLICATION_DATE) p0, MAX(PUBLICATION_DATE) p1, COUNT_IF(PUBLICATION_DATE IS NULL) p_null,
       COUNT_IF(TO_CHAR(PUBLICATION_DATE,'MM-DD') = '12-31') p_dec31, COUNT_IF(TO_CHAR(PUBLICATION_DATE,'MM-DD') = '01-01') p_jan1,
       MIN(DATE_CREATED) c0, MAX(DATE_CREATED) c1, COUNT_IF(DATE_CREATED IS NULL) c_null,
       COUNT_IF(ENDING_DATE IS NOT NULL) end_filled,
       COUNT(DISTINCT SOURCE_RUN_ID) runs, COUNT(DISTINCT SRC_SHA256) files, MIN(INGESTED_AT) i0, MAX(INGESTED_AT) i1
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES
GROUP BY ROLLUP(FEATURE_NAME_OFFICIAL) ORDER BY n DESC;

-- [q06] statement 4
-- q06 GNIS: slur and derogatory terms, official vs variant. Word-start match (Squaw also catches Squawbush); JAP/COON/CHINK need a word end.
WITH t(term, pat) AS (
  SELECT * FROM VALUES
   ('SQUAW','(^|[^A-Z])SQUAW.*'),
   ('NEGRO','(^|[^A-Z])NEGRO.*'),
   ('NIGGER','(^|[^A-Z])NIGGER.*'),
   ('JAP','(^|[^A-Z])JAPS?([^A-Z].*|$)'),
   ('CHINAMAN','(^|[^A-Z])CHINAM[AE]N.*'),
   ('CHINK','(^|[^A-Z])CHINKS?([^A-Z].*|$)'),
   ('REDSKIN','(^|[^A-Z])REDSKIN.*'),
   ('HALFBREED','(^|[^A-Z])HALF[- ]?BREED.*'),
   ('INJUN','(^|[^A-Z])INJUNS?([^A-Z].*|$)'),
   ('DARKEY','(^|[^A-Z])DARK(E)?YS?([^A-Z].*|$)'),
   ('PICKANINNY','(^|[^A-Z])PICKANINN.*'),
   ('COON (ambiguous: raccoon)','(^|[^A-Z])COONS?([^A-Z].*|$)'),
   ('WOP','(^|[^A-Z])WOPS?([^A-Z].*|$)'),
   ('DAGO','(^|[^A-Z])DAGOS?([^A-Z].*|$)'),
   ('KIKE','(^|[^A-Z])KIKES?([^A-Z].*|$)'),
   ('SPIC','(^|[^A-Z])SPICS?([^A-Z].*|$)'),
   ('GOOK','(^|[^A-Z])GOOKS?([^A-Z].*|$)'),
   ('SAMBO','(^|[^A-Z])SAMBOS?([^A-Z].*|$)')
)
SELECT t.term, g.FEATURE_NAME_OFFICIAL, COUNT(*) n, COUNT(DISTINCT g.FEATURE_ID) features,
       MIN(g.DATE_CREATED) c0, MAX(g.DATE_CREATED) c1,
       COUNT_IF(g.DATE_CREATED >= '2022-09-01') created_since_sep22,
       ARRAY_SLICE(ARRAY_AGG(DISTINCT g.FEATURE_NAME), 0, 6) sample
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES g
JOIN t ON REGEXP_LIKE(UPPER(g.FEATURE_NAME), t.pat)
GROUP BY 1,2 ORDER BY 1,2;

-- [q07] statement 5
-- q07 GNIS time: official and variant rows by DATE_CREATED year, plus publication-date year for variants (is the variant half frozen?)
SELECT FEATURE_NAME_OFFICIAL, YEAR(DATE_CREATED) yr, COUNT(*) n, COUNT(DISTINCT FEATURE_ID) features,
       COUNT_IF(DATE_CREATED = PUBLICATION_DATE) created_eq_pub
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES
WHERE DATE_CREATED IS NULL OR YEAR(DATE_CREATED) >= 1990 OR FEATURE_NAME_OFFICIAL = 'Official'
GROUP BY 1,2 ORDER BY 1,2;

-- [q06] statement 6
-- q06 (rerun after a reserved-word compile error) GNIS: slur and derogatory terms, official vs variant. Word-start match (Squaw also catches Squawbush); JAP/COON/CHINK need a word end.
WITH t(term, pat) AS (
  SELECT * FROM VALUES
   ('SQUAW','(^|[^A-Z])SQUAW.*'),
   ('NEGRO','(^|[^A-Z])NEGRO.*'),
   ('NIGGER','(^|[^A-Z])NIGGER.*'),
   ('JAP','(^|[^A-Z])JAPS?([^A-Z].*|$)'),
   ('CHINAMAN','(^|[^A-Z])CHINAM[AE]N.*'),
   ('CHINK','(^|[^A-Z])CHINKS?([^A-Z].*|$)'),
   ('REDSKIN','(^|[^A-Z])REDSKIN.*'),
   ('HALFBREED','(^|[^A-Z])HALF[- ]?BREED.*'),
   ('INJUN','(^|[^A-Z])INJUNS?([^A-Z].*|$)'),
   ('DARKEY','(^|[^A-Z])DARK(E)?YS?([^A-Z].*|$)'),
   ('PICKANINNY','(^|[^A-Z])PICKANINN.*'),
   ('COON (ambiguous: raccoon)','(^|[^A-Z])COONS?([^A-Z].*|$)'),
   ('WOP','(^|[^A-Z])WOPS?([^A-Z].*|$)'),
   ('DAGO','(^|[^A-Z])DAGOS?([^A-Z].*|$)'),
   ('KIKE','(^|[^A-Z])KIKES?([^A-Z].*|$)'),
   ('SPIC','(^|[^A-Z])SPICS?([^A-Z].*|$)'),
   ('GOOK','(^|[^A-Z])GOOKS?([^A-Z].*|$)'),
   ('SAMBO','(^|[^A-Z])SAMBOS?([^A-Z].*|$)')
)
SELECT t.term, g.FEATURE_NAME_OFFICIAL, COUNT(*) n, COUNT(DISTINCT g.FEATURE_ID) features,
       MIN(g.DATE_CREATED) c0, MAX(g.DATE_CREATED) c1,
       COUNT_IF(g.DATE_CREATED >= '2022-09-01') created_since_sep22,
       ARRAY_SLICE(ARRAY_AGG(DISTINCT g.FEATURE_NAME), 0, 6) name_sample,
       COUNT_IF(YEAR(g.PUBLICATION_DATE) >= 2021) pub_since_2021, ARRAY_SLICE(ARRAY_AGG(DISTINCT g.SOURCE_ORIGINATOR), 0, 5) originators
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES g
JOIN t ON REGEXP_LIKE(UPPER(g.FEATURE_NAME), t.pat)
GROUP BY 1,2 ORDER BY 1,2;

-- [q08] statement 7
-- q08 GNIS chain: features that carry a slur as a VARIANT name. What is their OFFICIAL name now, and when was that official citation published?
WITH v AS (
  SELECT DISTINCT FEATURE_ID,
         CASE WHEN REGEXP_LIKE(UPPER(FEATURE_NAME), '(^|[^A-Z])SQUAW.*') AND NOT REGEXP_LIKE(UPPER(FEATURE_NAME), '(^|[^A-Z])SQUAWK.*') THEN 'SQUAW'
              WHEN REGEXP_LIKE(UPPER(FEATURE_NAME), '(^|[^A-Z])NIGGER.*') THEN 'NIGGER'
              WHEN REGEXP_LIKE(UPPER(FEATURE_NAME), '(^|[^A-Z])JAPS?([^A-Z].*|$)') THEN 'JAP'
              WHEN REGEXP_LIKE(UPPER(FEATURE_NAME), '(^|[^A-Z])NEGRO.*') THEN 'NEGRO' END term
  FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES
  WHERE FEATURE_NAME_OFFICIAL = 'Variant'
), o AS (
  SELECT FEATURE_ID, FEATURE_NAME, PUBLICATION_DATE, DATE_CREATED, SOURCE_ORIGINATOR, CITATION
  FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES WHERE FEATURE_NAME_OFFICIAL = 'Official'
)
SELECT v.term,
       CASE WHEN o.FEATURE_ID IS NULL THEN 'no official row'
            WHEN REGEXP_LIKE(UPPER(o.FEATURE_NAME), '(^|[^A-Z])(SQUAW|NIGGER|JAPS?[^A-Z]|JAPS?$).*') AND NOT REGEXP_LIKE(UPPER(o.FEATURE_NAME), '.*SQUAWK.*') THEN 'official still has a slur'
            WHEN REGEXP_LIKE(UPPER(o.FEATURE_NAME), '(^|[^A-Z])NEGRO.*') THEN 'official has NEGRO'
            WHEN REGEXP_LIKE(UPPER(o.FEATURE_NAME), '(^|[^A-Z])JAPANESE.*') THEN 'official has JAPANESE'
            ELSE 'official is something else' END bucket,
       COUNT(*) features,
       COUNT_IF(YEAR(o.PUBLICATION_DATE) = 2022) off_pub_2022, COUNT_IF(YEAR(o.PUBLICATION_DATE) = 2023) off_pub_2023,
       COUNT_IF(YEAR(o.PUBLICATION_DATE) < 2021) off_pub_pre2021, COUNT_IF(o.PUBLICATION_DATE IS NULL) off_pub_null,
       MODE(o.SOURCE_ORIGINATOR) top_originator, MODE(o.CITATION) top_citation,
       ARRAY_SLICE(ARRAY_AGG(o.FEATURE_NAME) WITHIN GROUP (ORDER BY o.FEATURE_ID), 0, 8) official_names
FROM v LEFT JOIN o ON o.FEATURE_ID = v.FEATURE_ID
WHERE v.term IS NOT NULL
GROUP BY 1,2 ORDER BY 1, features DESC;

-- [q09] statement 8
-- q09 GNIS: every official name still carrying SQUAW, plus freshness probes on famous renamings (Denali/McKinley 2015 and 2025, Mount Evans to Mount Blue Sky 2023, Gulf of Mexico/America 2025)
SELECT FEATURE_ID, FEATURE_NAME, FEATURE_NAME_OFFICIAL, SOURCE_ORIGINATOR, SOURCE_REF_TYPE, PUBLICATION_DATE, DATE_CREATED, CITATION
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES
WHERE (FEATURE_NAME_OFFICIAL = 'Official' AND REGEXP_LIKE(UPPER(FEATURE_NAME), '(^|[^A-Z])SQUAW.*'))
   OR FEATURE_NAME IN ('Denali','Mount McKinley','Mount Evans','Mount Blue Sky','Gulf of Mexico','Gulf of America')
ORDER BY FEATURE_NAME_OFFICIAL, FEATURE_ID;

-- [q02] statement 9
-- q02 OWID temp anomaly: dump all 531 rows (tiny), analyze locally
SELECT * FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_OWID_TEMP_ANOMALY;

-- [q03] statement 10
-- q03 OWID fossil share: dump all 6,379 rows (small), analyze locally
SELECT * FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_OWID_FOSSIL_SHARE;

-- [q10] statement 11
-- q10 GNIS: split the NEGRO official names (historical? proven 1963 swap?) and date the renamings away from NEGRO and SQUAW by the official citation's year
WITH f AS (
  SELECT FEATURE_ID,
         MAX(IFF(FEATURE_NAME_OFFICIAL='Official', FEATURE_NAME, NULL)) off_name,
         MAX(IFF(FEATURE_NAME_OFFICIAL='Official', PUBLICATION_DATE, NULL)) off_pub,
         MAX(IFF(FEATURE_NAME_OFFICIAL='Official', SOURCE_ORIGINATOR, NULL)) off_src,
         MAX(IFF(FEATURE_NAME_OFFICIAL='Variant' AND REGEXP_LIKE(UPPER(FEATURE_NAME), '(^|[^A-Z])NIGGER.*'), 1, 0)) v_nword,
         MAX(IFF(FEATURE_NAME_OFFICIAL='Variant' AND REGEXP_LIKE(UPPER(FEATURE_NAME), '(^|[^A-Z])NEGRO.*'), 1, 0)) v_negro,
         MAX(IFF(FEATURE_NAME_OFFICIAL='Variant' AND REGEXP_LIKE(UPPER(FEATURE_NAME), '(^|[^A-Z])SQUAW.*') AND NOT REGEXP_LIKE(UPPER(FEATURE_NAME), '.*SQUAWK.*'), 1, 0)) v_squaw,
         COUNT_IF(FEATURE_NAME_OFFICIAL='Variant') n_var
  FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES
  GROUP BY 1
), s AS (
  SELECT *, CASE
     WHEN REGEXP_LIKE(UPPER(off_name), '(^|[^A-Z])NEGRO.*') THEN 'A official NEGRO now'
     WHEN (v_negro = 1 OR v_nword = 1) THEN 'B renamed away from NEGRO/n-word'
     WHEN v_squaw = 1 THEN 'C renamed away from SQUAW' END grp
  FROM f
)
SELECT grp,
       CASE WHEN off_pub IS NULL THEN 'no date' WHEN YEAR(off_pub) < 1990 THEN 'pre-1990' WHEN YEAR(off_pub) < 2000 THEN '1990s'
            WHEN YEAR(off_pub) < 2010 THEN '2000s' WHEN YEAR(off_pub) < 2020 THEN '2010s' ELSE TO_CHAR(YEAR(off_pub)) END off_pub_period,
       COUNT(*) features, COUNT_IF(off_name ILIKE '%(historical)%') historical, COUNT_IF(v_nword = 1) had_nword_variant,
       COUNT_IF(n_var = 0) no_variants, MODE(off_src) top_src
FROM s WHERE grp IS NOT NULL
GROUP BY 1,2 ORDER BY 1,2;

-- [q11] statement 12
-- q11 Is there a GNIS table with state/county/feature class anywhere (marts or landing) to give GNIS a peer group?
SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, ROW_COUNT FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME ILIKE '%GNIS%'
UNION ALL
SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, ROW_COUNT FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME ILIKE '%GNIS%';

-- [q12] statement 13
-- q12 GNIS: every official name containing NEGRO, with its citation, and whether the same feature carries an n-word or NEGRO variant (to split English racial use from Spanish 'negro' = black)
WITH v AS (
  SELECT FEATURE_ID,
         MAX(IFF(REGEXP_LIKE(UPPER(FEATURE_NAME), '(^|[^A-Z])NIGGER.*'), FEATURE_NAME, NULL)) nword_variant,
         COUNT(*) n_var
  FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES WHERE FEATURE_NAME_OFFICIAL = 'Variant' GROUP BY 1
)
SELECT o.FEATURE_ID, o.FEATURE_NAME, o.SOURCE_ORIGINATOR, o.SOURCE_REF_TYPE, o.PUBLICATION_DATE, o.DATE_CREATED, LEFT(o.CITATION, 120) citation,
       v.nword_variant, COALESCE(v.n_var, 0) n_var
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES o LEFT JOIN v ON v.FEATURE_ID = o.FEATURE_ID
WHERE o.FEATURE_NAME_OFFICIAL = 'Official' AND REGEXP_LIKE(UPPER(o.FEATURE_NAME), '(^|[^A-Z])NEGRO.*')
ORDER BY o.FEATURE_NAME;

-- [q13] statement 14
-- q13 GNIS FIX: q06/q08/q10/q12 used REGEXP_LIKE patterns anchored at the start of the name, so they only caught names that BEGIN with the term
-- ("Big Squaw Creek", "Cerro Negro" were missed). This extract pulls every row (official and variant) for every feature where ANY name
-- has one of the terms anywhere as a word start; all counts are redone locally from this file.
WITH hit AS (
  SELECT DISTINCT FEATURE_ID
  FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES
  WHERE REGEXP_LIKE(UPPER(FEATURE_NAME),
    '.*(^|[^A-Z])(SQUAW|NIGGER|NEGRO|JAPS?([^A-Z]|$)|CHINAM[AE]N|CHINKS?([^A-Z]|$)|DAGOS?([^A-Z]|$)|DARKE?YS?([^A-Z]|$)|HALF[- ]?BREED|REDSKIN|SAMBOS?([^A-Z]|$)|INJUNS?([^A-Z]|$)|WOPS?([^A-Z]|$)|GOOKS?([^A-Z]|$)|PICKANINN).*')
)
SELECT g.FEATURE_ID, g.FEATURE_NAME, g.FEATURE_NAME_OFFICIAL, g.SOURCE_ORIGINATOR, g.SOURCE_REF_TYPE,
       g.PUBLICATION_DATE, g.DATE_CREATED, LEFT(g.CITATION, 160) citation
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES g JOIN hit ON hit.FEATURE_ID = g.FEATURE_ID;

-- ============================================================================
-- Notes on the log above (added after the run):
-- * 14 statements total. Statement 4 (q06, first try) was a compile error: SAMPLE is a reserved word. Statement 6 is its rerun.
-- * MY ERROR, disclosed: q06, q08, q10 and q12 use REGEXP_LIKE patterns like '(^|[^A-Z])SQUAW.*'. Snowflake's REGEXP_LIKE
--   matches the WHOLE string, so those patterns only caught names that START with the term. "Big Squaw Creek" and
--   "Cerro Negro" were missed. q13 fixes it with a leading '.*' and pulls every name for every hit feature (3,941 rows,
--   1,855 features). All GNIS numbers in g41.md are recomputed locally from q13 (g41/an13.py, g41/an13b.py).
--   q06/q08/q10/q12 results are kept for the record but are superseded.
-- * q02 and q03 are full dumps of two small tables (531 and 6,379 rows); the peer and time math ran locally in pandas.
