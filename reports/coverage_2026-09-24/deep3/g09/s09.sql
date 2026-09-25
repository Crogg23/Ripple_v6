WITH t AS (
  SELECT *, CASE WHEN SUBSTR(ccn,3,1) IN ('T','R') THEN 'unit'
                 WHEN TRY_TO_NUMBER(SUBSTR(ccn,3,4)) BETWEEN 3025 AND 3099 THEN 'freestanding' ELSE 'other' END kind
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF)
SELECT YEAR(certification_date) y, COUNT(*) all_irf,
       COUNT_IF(kind = 'freestanding' AND ownership_type = 'For profit') fs_forprofit,
       COUNT_IF(kind = 'freestanding' AND ownership_type <> 'For profit') fs_other,
       COUNT_IF(kind = 'unit' AND ownership_type = 'For profit') unit_forprofit,
       COUNT_IF(kind = 'unit' AND ownership_type <> 'For profit') unit_other,
       COUNT_IF(provider_name ILIKE '%ENCOMPASS%') encompass_named,
       COUNT_IF(state = 'FL') fl_all, COUNT_IF(state = 'FL' AND kind = 'freestanding') fl_fs,
       COUNT_IF(state = 'FL' AND kind = 'unit') fl_unit, COUNT_IF(state = 'TX') tx_all,
       COUNT_IF(state NOT IN ('FL')) not_fl
FROM t WHERE certification_date >= '2008-01-01'
GROUP BY 1 ORDER BY 1
