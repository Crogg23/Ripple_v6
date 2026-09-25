WITH p AS (
  SELECT COMPANY_NUMBER, TRY_TO_NUMBER(IFF(COMPANY_NUMBER RLIKE '[0-9]{8}', COMPANY_NUMBER, NULL)) n, _SOURCE_RUN_ID r, NOTIFIED_ON, CEASED_ON
  FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC),
pc AS (SELECT COMPANY_NUMBER, MAX(n) n, MAX(IFF(r LIKE 'manual%',1,0)) in_m, MAX(IFF(r LIKE 'resume%',1,0)) in_r,
              MAX(IFF(NOTIFIED_ON <= '2026-09-24', NOTIFIED_ON, NULL)) last_notified FROM p GROUP BY 1),
live AS (SELECT COMPANY_NUMBER FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE),
x AS (
  SELECT pc.*, IFF(live.COMPANY_NUMBER IS NULL, 'psc_only', 'in_live') st,
         CASE WHEN pc.n BETWEEN 16764035 AND 16858916 THEN 'a_oct6_nov16'
              WHEN pc.n BETWEEN 16858919 AND 16924562 THEN 'b_nov17_dec21'
              WHEN pc.n BETWEEN 16941281 AND 17005537 THEN 'c_jan5_feb1'
              WHEN pc.n BETWEEN 15000000 AND 16764034 THEN 'd_older_15m'
              WHEN pc.n > 17005537 THEN 'e_newer' ELSE 'f_other' END w
  FROM pc LEFT JOIN live USING (COMPANY_NUMBER))
SELECT * FROM (
  SELECT 'by_load' k, r v, COUNT(*) rows_, COUNT(DISTINCT COMPANY_NUMBER) cos, MAX(IFF(NOTIFIED_ON <= '2026-09-24', NOTIFIED_ON, NULL))::string max_notified, MIN(n)::string min_n, MAX(n)::string max_n
    FROM p GROUP BY 1,2
  UNION ALL SELECT 'overlap', 'm=' || in_m || ' r=' || in_r, COUNT(*), NULL, NULL, NULL, NULL FROM pc GROUP BY 1,2
  UNION ALL SELECT 'membership', w || ' | ' || st || ' | m=' || in_m || ' r=' || in_r, COUNT(*), NULL, MAX(last_notified)::string, MIN(n)::string, MAX(n)::string FROM x GROUP BY 1,2
) ORDER BY k, v
