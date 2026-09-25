-- @S17 crosswalk land rate: 2017 HMDA lenders (aggregated first) matched to ARID_2017 as agency code + respondent id with leading zeros stripped
WITH h AS (
  SELECT AGENCY_CODE, RESPONDENT_ID, COUNT(*) apps
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC
  WHERE AS_OF_YEAR = '2017'
  GROUP BY 1, 2),
k AS (SELECT h.*, TRIM(AGENCY_CODE) || LTRIM(TRIM(RESPONDENT_ID), '0') arid,
             TRIM(AGENCY_CODE) || LTRIM(REGEXP_REPLACE(RESPONDENT_ID, '[^0-9A-Za-z]', ''), '0') arid_clean FROM h),
x AS (SELECT ARID_2017, LEI_2020 FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF)
SELECT COUNT(*) lenders_2017, SUM(apps) apps_2017,
       COUNT_IF(x1.ARID_2017 IS NOT NULL) lenders_land, SUM(IFF(x1.ARID_2017 IS NOT NULL, apps, 0)) apps_land,
       COUNT_IF(x1.ARID_2017 IS NULL AND x2.ARID_2017 IS NOT NULL) extra_land_after_clean,
       (SELECT COUNT(*) FROM x WHERE ARID_2017 NOT IN (SELECT arid FROM k)) xref_not_in_2017,
       ARRAY_AGG(IFF(x1.ARID_2017 IS NULL AND x2.ARID_2017 IS NULL AND apps > 20000, arid || ':' || apps, NULL)) big_misses
FROM k LEFT JOIN x x1 ON x1.ARID_2017 = k.arid LEFT JOIN x x2 ON x2.ARID_2017 = k.arid_clean;
