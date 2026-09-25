-- S08 990 index: return types by date format (what the 'other' types are), and duplicate returns across the whole table
SELECT RETURN_TYPE, REGEXP_LIKE(TRIM(SUB_DATE_RAW), '^[0-9]{4}$') year_only, COUNT(*) n, MIN(SUB_DATE) s0, MAX(SUB_DATE) s1,
  COUNT(DISTINCT OBJECT_ID) objs, COUNT(DISTINCT EIN, TAX_PERIOD) ein_periods
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990_EFILE_INDEX
GROUP BY 1, 2 ORDER BY 1, 2;

-- S09 990 index: duplicate checks over the whole table (object id, DLN, EIN+period+form repeats)
WITH k AS (
  SELECT EIN, TAX_PERIOD, RETURN_TYPE, COUNT(*) c, COUNT(DISTINCT YEAR(SUB_DATE)) sub_years
  FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990_EFILE_INDEX GROUP BY 1, 2, 3)
SELECT (SELECT COUNT(*) FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990_EFILE_INDEX) n_rows,
  (SELECT COUNT(DISTINCT OBJECT_ID) FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990_EFILE_INDEX) objs,
  (SELECT COUNT(DISTINCT DLN) FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990_EFILE_INDEX) dlns,
  COUNT(*) keys, COUNT_IF(c > 1) keys_multi, SUM(IFF(c > 1, c, 0)) rows_in_multi, COUNT_IF(c > 1 AND sub_years > 1) multi_across_years,
  COUNT_IF(c >= 5) keys_5plus, MAX(c) max_c
FROM k;

-- S10 JOIN: revoked nonprofits (auto-revocation list, revocation dated 2019 on) x their e-filed 990/990EZ/990PF returns.
-- Window = the three returns whose missed due dates trigger revocation: tax periods ending 5 to 40 months before the revocation date.
-- 'sure_before' = submitted in an earlier calendar year than the revocation (works for year-only rows), 'full_before' = full timestamp before it.
WITH r AS (
  SELECT EIN, LEGAL_NAME, CITY, STATE, EXEMPTION_TYPE, REVOCATION_DATE d, REVOCATION_POSTING_DATE pd, REINSTATEMENT_DATE rd
  FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_AUTO_REVOCATIONS WHERE REVOCATION_DATE >= '2019-01-01'),
i AS (
  SELECT EIN, TRY_TO_DATE(TAX_PERIOD || '01', 'YYYYMMDD') p, SUB_DATE, REGEXP_LIKE(TRIM(SUB_DATE_RAW), '^[0-9]{4}$') yo, RETURN_TYPE, OBJECT_ID, TAXPAYER_NAME
  FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990_EFILE_INDEX
  WHERE RETURN_TYPE IN ('990','990EZ','990PF') AND EIN IN (SELECT EIN FROM r))
SELECT r.EIN, r.LEGAL_NAME, r.CITY, r.STATE, r.EXEMPTION_TYPE, r.d, r.pd, r.rd, COUNT(*) n_ret,
  COUNT_IF(i.p BETWEEN DATEADD(month, -40, r.d) AND DATEADD(month, -5, r.d)) n_win,
  COUNT_IF(i.p BETWEEN DATEADD(month, -40, r.d) AND DATEADD(month, -5, r.d) AND YEAR(i.SUB_DATE) < YEAR(r.d)) n_win_sure_before,
  COUNT_IF(i.p BETWEEN DATEADD(month, -40, r.d) AND DATEADD(month, -5, r.d) AND NOT i.yo AND i.SUB_DATE < r.d) n_win_full_before,
  COUNT_IF(i.p BETWEEN DATEADD(month, -40, r.d) AND DATEADD(month, -5, r.d) AND YEAR(i.SUB_DATE) = YEAR(r.d) AND i.yo) n_win_same_year_unknown,
  COUNT(DISTINCT IFF(i.p BETWEEN DATEADD(month, -40, r.d) AND DATEADD(month, -5, r.d) AND YEAR(i.SUB_DATE) < YEAR(r.d), i.p, NULL)) periods_sure_before,
  COUNT_IF(i.p > r.d) n_after_period, COUNT_IF(YEAR(i.SUB_DATE) > YEAR(r.pd)) n_sub_after_posting_year,
  MIN(i.p) p0, MAX(i.p) p1, MIN(i.SUB_DATE) s0, MAX(i.SUB_DATE) s1, ARRAY_TO_STRING(ARRAY_AGG(DISTINCT i.RETURN_TYPE), ',') types,
  ANY_VALUE(i.TAXPAYER_NAME) idx_name
FROM r JOIN i ON i.EIN = r.EIN
GROUP BY 1,2,3,4,5,6,7,8;

-- S11 SEC EDGAR (US): pull the filing index without URLs (49K rows) for local peer and lateness work
SELECT CIK, TICKER, ENTITY_NAME, ACCESSION_NUMBER, FORM_TYPE, FILED_AT, PERIOD_OF_REPORT, IS_REGISTRATION_OR_PROSPECTUS, IS_ANNUAL_REPORT,
  IS_QUARTERLY_REPORT, EIN, ISIN, STATE_OF_INCORPORATION, SOURCE_ID, _INGESTED_AT::string ing
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_US_SEC_EDGAR;
