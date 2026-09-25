WITH t AS (
  SELECT *, CASE WHEN SUBSTR(ccn,3,1) = 'T' THEN 'unit_in_hospital' WHEN SUBSTR(ccn,3,1) = 'R' THEN 'unit_in_CAH'
                 WHEN TRY_TO_NUMBER(SUBSTR(ccn,3,4)) BETWEEN 3025 AND 3099 THEN 'freestanding' ELSE 'other:' || SUBSTR(ccn,3,2) END kind
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF)
SELECT kind, ownership_type, COUNT(*) n, COUNT(DISTINCT ccn) ccns, MIN(certification_date) c0, MAX(certification_date) c1,
       COUNT_IF(certification_date > CURRENT_DATE) future_dated, COUNT_IF(certification_date >= '2019-07-01') since_2019h2,
       COUNT_IF(certification_date >= '2014-07-01' AND certification_date < '2019-07-01') y2014h2_2019h1,
       COUNT_IF(provider_name ILIKE '%ENCOMPASS%') encompass_named, COUNT_IF(state = 'FL') fl,
       COUNT_IF(TRIM(telephone_number) IN ('-','')) phone_dash,
       ARRAY_AGG(IFF(ownership_type = 'Physician' OR certification_date > CURRENT_DATE,
                     ccn || ' ' || state || ' ' || certification_date || ' ' || LEFT(provider_name,45), NULL)) odd_rows
FROM t GROUP BY 1,2 ORDER BY 1,2
