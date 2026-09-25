-- S25 Wayback: every page that ever answered 404 or ended on 403, excluding junk URL variants, with dates
WITH p AS (
  SELECT URLKEY, MIN(CAPTURED_AT) t0, MAX(CAPTURED_AT) t1, MAX_BY(HTTP_STATUS, CAPTURED_AT) last_status,
         MIN(IFF(HTTP_STATUS = 404, CAPTURED_AT, NULL)) first_404, MAX(IFF(HTTP_STATUS = 200, CAPTURED_AT, NULL)) last_200,
         LISTAGG(DISTINCT HTTP_STATUS::STRING, ',') statuses
  FROM LIBRARY_MARTS.EPSTEIN.FCT_WAYBACK_PAGE_CHANGES GROUP BY 1)
SELECT REGEXP_REPLACE(URLKEY, '^gov,justice[)]/epstein/doj-disclosures', '') path, t0, t1, last_status, first_404, last_200, statuses
FROM p
WHERE (first_404 IS NOT NULL OR last_status IN (403, 401))
  AND NOT REGEXP_LIKE(URLKEY, '.*(utm_|fbclid|%0a|%e|%c2|u003c|&data=|[?&]ref=|gclid|[.]$|[)][.]?$|[\\]).*')
ORDER BY first_404 NULLS LAST, path;

-- S26 Oyez: the 7 dockets that missed SCDB on docket+term, looked up by case name
SELECT TERM, DOCKET, CASE_NAME, US_CITATION, DATE_DECISION, COUNT(*) votes
FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_SCDB
WHERE (TERM BETWEEN 1965 AND 1972 AND (CASE_NAME ILIKE 'GILLS%' OR CASE_NAME ILIKE 'AMERICAN TRUCKING%' OR CASE_NAME ILIKE 'CENTRAL BANK%'
       OR CASE_NAME ILIKE 'CALIFORNIA v. PHILLIPS%' OR CASE_NAME ILIKE 'CHICAGO v. UNITED%' OR CASE_NAME ILIKE 'BOSTON % MAINE%'
       OR CASE_NAME ILIKE 'WASHINGTON v. GENERAL MOTORS%'))
   OR CASE_NAME ILIKE 'ROE %v. WADE%'
GROUP BY 1, 2, 3, 4, 5 ORDER BY 1, 3;

-- S27 Revolving door trap: are the sector slots in alphabetical order (so SECTOR1 / INDUSTRY_SECTOR is list order, not the main tie)?
SELECT COUNT_IF(LOWER(SECTOR2) <> 'nan') multi, COUNT_IF(LOWER(SECTOR2) <> 'nan' AND SECTOR1 < SECTOR2) s1_lt_s2,
       COUNT_IF(LOWER(SECTOR3) <> 'nan' AND LOWER(SECTOR2) <> 'nan') multi3, COUNT_IF(LOWER(SECTOR3) <> 'nan' AND SECTOR2 < SECTOR3) s2_lt_s3,
       COUNT_IF(INDUSTRY_SECTOR = SECTOR1) ind_eq_s1, COUNT_IF(LOWER(SECTOR2) <> 'nan' AND SECTOR1 = 'Agriculture/Big Food') ag_first_multi,
       COUNT_IF(LOWER(SECTOR2) <> 'nan' AND SECTOR1_INTEREST LIKE '3%') multi_s1_i3, COUNT_IF(LOWER(SECTOR2) <> 'nan' AND SECTOR2_INTEREST > SECTOR1_INTEREST) s2_stronger
FROM LIBRARY_MARTS.GOVERNANCE.GOVERNANCE__FED_REVOLVINGDOOR_PROJECT;
