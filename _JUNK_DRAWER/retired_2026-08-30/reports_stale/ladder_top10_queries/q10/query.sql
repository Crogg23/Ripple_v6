-- Q10 main chain (result.csv):

-- Q10 chain: OSHA 2024 injury filings (EIN) -> SEC EDGAR filers (EIN->CIK) -> insider filings (CIK)
-- PBGC leg BLOCKED: ECONOMICS__FED_PBGC_DATA has no EIN (aggregate Data Book stats only)
-- EDGAR_FINANCIALS is the submissions metadata table: NO revenue/income columns exist, so we carry name/SIC/latest FY instead
-- injury rate = total recordable cases * 200,000 / hours worked (per 100 FTE); OSHA numerics stored as text -> TRY_TO_NUMBER
WITH o AS (
  SELECT REGEXP_REPLACE(EIN,'[^0-9]','') ein,
         COUNT(*) establishments,
         SUM(TRY_TO_NUMBER(ANNUAL_AVERAGE_EMPLOYEES)) employees,
         SUM(TRY_TO_NUMBER(TOTAL_HOURS_WORKED)) hours,
         SUM(COALESCE(TRY_TO_NUMBER(TOTAL_DAFW_CASES),0)+COALESCE(TRY_TO_NUMBER(TOTAL_DJTR_CASES),0)+COALESCE(TRY_TO_NUMBER(TOTAL_OTHER_CASES),0)) total_cases,
         SUM(COALESCE(TOTAL_DEATHS,0)) deaths
  FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
  WHERE LENGTH(REGEXP_REPLACE(EIN,'[^0-9]',''))=9
  GROUP BY 1
),
e AS (
  SELECT REGEXP_REPLACE(EIN,'[^0-9]','') ein, LTRIM(CIK,'0') cik,
         MAX_BY(NAME, FILED) company_name, MAX_BY(SIC, FILED) sic, MAX(FY) latest_fy, COUNT(*) sec_filings
  FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_FINANCIALS
  WHERE LENGTH(REGEXP_REPLACE(EIN,'[^0-9]',''))=9
  GROUP BY 1,2
),
i AS (
  SELECT LTRIM(CIK,'0') cik, COUNT(*) insider_filings,
         SUM(IFF(DOCUMENT_TYPE='4',1,0)) form4_filings,
         MAX(FILING_DATE) latest_insider_filing
  FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_INSIDERS
  GROUP BY 1
)
SELECT e.company_name, o.ein, e.cik, e.sic, e.latest_fy,
       o.establishments, o.employees, o.hours, o.total_cases, o.deaths,
       ROUND(IFF(o.hours>0, o.total_cases*200000/o.hours, NULL),2) injury_rate_per_100_fte,
       e.sec_filings, COALESCE(i.insider_filings,0) insider_filings,
       COALESCE(i.form4_filings,0) form4_filings, i.latest_insider_filing
FROM o JOIN e ON o.ein=e.ein
LEFT JOIN i ON e.cik=i.cik
ORDER BY injury_rate_per_100_fte DESC NULLS LAST


-- funnel (funnel.csv):

-- funnel step counts
WITH o AS (SELECT DISTINCT REGEXP_REPLACE(EIN,'[^0-9]','') ein FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024 WHERE LENGTH(REGEXP_REPLACE(EIN,'[^0-9]',''))=9),
e AS (SELECT DISTINCT REGEXP_REPLACE(EIN,'[^0-9]','') ein, LTRIM(CIK,'0') cik FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_FINANCIALS WHERE LENGTH(REGEXP_REPLACE(EIN,'[^0-9]',''))=9),
i AS (SELECT DISTINCT LTRIM(CIK,'0') cik FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_INSIDERS)
SELECT 'osha_employers_with_ein' step, COUNT(*) n, 1 ord FROM o
UNION ALL SELECT 'sec_filers_with_ein', COUNT(DISTINCT ein), 2 FROM e
UNION ALL SELECT 'osha_x_sec (EIN match)', COUNT(DISTINCT o.ein), 3 FROM o JOIN e ON o.ein=e.ein
UNION ALL SELECT 'osha_x_sec_x_insiders (CIK match)', COUNT(DISTINCT o.ein), 4 FROM o JOIN e ON o.ein=e.ein JOIN i ON e.cik=i.cik
UNION ALL SELECT 'osha_x_sec_x_pension_failure', NULL, 5
ORDER BY ord
