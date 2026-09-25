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
ORDER BY o.FEATURE_NAME
