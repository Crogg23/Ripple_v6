-- q09 GNIS: every official name still carrying SQUAW, plus freshness probes on famous renamings (Denali/McKinley 2015 and 2025, Mount Evans to Mount Blue Sky 2023, Gulf of Mexico/America 2025)
SELECT FEATURE_ID, FEATURE_NAME, FEATURE_NAME_OFFICIAL, SOURCE_ORIGINATOR, SOURCE_REF_TYPE, PUBLICATION_DATE, DATE_CREATED, CITATION
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES
WHERE (FEATURE_NAME_OFFICIAL = 'Official' AND REGEXP_LIKE(UPPER(FEATURE_NAME), '(^|[^A-Z])SQUAW.*'))
   OR FEATURE_NAME IN ('Denali','Mount McKinley','Mount Evans','Mount Blue Sky','Gulf of Mexico','Gulf of America')
ORDER BY FEATURE_NAME_OFFICIAL, FEATURE_ID
