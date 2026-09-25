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
GROUP BY 1,2 ORDER BY 1,2
