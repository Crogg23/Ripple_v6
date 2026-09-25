WITH t AS (
  SELECT *, CASE WHEN SUBSTR(ccn,3,1) IN ('T','R') THEN 'unit'
                 WHEN TRY_TO_NUMBER(SUBSTR(ccn,3,4)) BETWEEN 3025 AND 3099 THEN 'freestanding' ELSE 'other' END kind
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF)
SELECT state, COUNT(*) now_total,
       COUNT_IF(certification_date < '2019-07-01') before_2019h2,
       COUNT_IF(certification_date >= '2014-07-01' AND certification_date < '2019-07-01') new_5y_before,
       COUNT_IF(certification_date >= '2019-07-01' AND certification_date < '2024-07-01') new_5y_after,
       COUNT_IF(certification_date >= '2024-07-01') new_since_2024h2,
       COUNT_IF(certification_date >= '2019-07-01' AND kind = 'freestanding') new_fs_after,
       COUNT_IF(certification_date >= '2019-07-01' AND kind = 'unit') new_unit_after,
       COUNT_IF(certification_date >= '2019-07-01' AND ownership_type = 'For profit') new_fp_after,
       COUNT_IF(certification_date >= '2019-07-01' AND provider_name ILIKE '%ENCOMPASS%') new_enc_after,
       ROUND(COUNT_IF(certification_date >= '2019-07-01') / NULLIF(COUNT_IF(certification_date < '2019-07-01'),0), 2) growth_ratio
FROM t GROUP BY 1 ORDER BY COUNT_IF(certification_date >= '2019-07-01') DESC, 1
