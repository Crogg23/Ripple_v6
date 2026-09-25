-- S17 990 index trap check: tax periods that cannot be right (return processed before its own tax year ended, far-future or very old periods)
SELECT REGEXP_LIKE(TRIM(SUB_DATE_RAW), '^[0-9]{4}$') year_only, COUNT(*) n,
  COUNT_IF(NOT year_only AND SUB_DATE < LAST_DAY(TRY_TO_DATE(TAX_PERIOD || '01', 'YYYYMMDD'))) sub_before_period_end,
  COUNT_IF(year_only AND YEAR(SUB_DATE) < TRY_TO_NUMBER(LEFT(TAX_PERIOD, 4))) sub_year_before_period_year,
  COUNT_IF(TRY_TO_DATE(TAX_PERIOD || '01', 'YYYYMMDD') IS NULL) tp_unparsed,
  COUNT_IF(TAX_PERIOD > '202612') tp_future, COUNT_IF(TAX_PERIOD < '201001') tp_pre2010,
  ARRAY_SLICE(ARRAY_AGG(DISTINCT IFF(TAX_PERIOD > '202612', TAX_PERIOD, NULL)), 0, 10) future_examples
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990_EFILE_INDEX
GROUP BY 1;
