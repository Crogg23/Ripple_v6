-- S15 Leadership PACs, same-PAC panel: PACs with $250K+ spending in two back-to-back cycles, share going to others in each, excluding the two Trump committees
WITH p AS (SELECT CMTE_ID, YEAR(COVERAGE_END_DATE) + MOD(YEAR(COVERAGE_END_DATE), 2) cyc, TOTAL_DISBURSEMENTS disb,
                  (COALESCE(CONTRIBUTIONS_TO_OTHER_COMMITTEES,0) + COALESCE(INDEPENDENT_EXPENDITURES,0) + COALESCE(TRANSFERS_TO_AFFILIATES,0)) / NULLIF(TOTAL_DISBURSEMENTS,0) share
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY
           WHERE COMMITTEE_DESIGNATION = 'D' AND COVERAGE_END_DATE IS NOT NULL AND CMTE_ID NOT IN ('C00828541','C00762591')),
pairs AS (SELECT a.cyc c0, b.cyc c1, a.CMTE_ID, a.share s0, b.share s1, a.disb d0, b.disb d1
          FROM p a JOIN p b ON a.CMTE_ID = b.CMTE_ID AND b.cyc = a.cyc + 2
          WHERE a.disb >= 250000 AND b.disb >= 250000)
SELECT c0, c1, COUNT(*) pacs, ROUND(MEDIAN(s0),3) med_s0, ROUND(MEDIAN(s1),3) med_s1, ROUND(MEDIAN(s1 - s0),3) med_change,
       COUNT_IF(s1 < s0 - 0.25) fell_25pts, COUNT_IF(s1 > s0 + 0.25) rose_25pts, COUNT_IF(s1 < 0.10) under10_after, COUNT_IF(s0 < 0.10) under10_before,
       ROUND(SUM(d0)/1e6,1) d0_m, ROUND(SUM(d1)/1e6,1) d1_m,
       ROUND(SUM(s0*d0)/SUM(d0),3) wshare0, ROUND(SUM(s1*d1)/SUM(d1),3) wshare1
FROM pairs GROUP BY 1,2 ORDER BY 1;

-- S16 Big filers (large accelerated and accelerated) whose 10-K or 10-Q came in past the extended deadline, all nine quarters: exchange listing, and insider open-market trades between the extended deadline and the filing
WITH s AS (
  SELECT '2024Q1' q, * FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q1 UNION ALL
  SELECT '2024Q2', * FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q2 UNION ALL
  SELECT '2024Q3', * FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q3 UNION ALL
  SELECT '2024Q4', * FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q4 UNION ALL
  SELECT '2025Q1', * FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q1 UNION ALL
  SELECT '2025Q2', * FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q2 UNION ALL
  SELECT '2025Q3', * FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q3 UNION ALL
  SELECT '2025Q4', * FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q4 UNION ALL
  SELECT '2026Q1', * FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2026Q1),
l AS (SELECT q, ADSH, TRY_TO_NUMBER(CIK) cik, NAME, FORM, AFS, SIC, STPRBA, TRY_TO_DATE(PERIOD,'YYYYMMDD') pd, TRY_TO_DATE(FILED,'YYYYMMDD') fd, PREVRPT,
             IFF(FORM = '10-K', IFF(LEFT(AFS,1) = '1', 60, 75) + 15, 40 + 5) ext_days
      FROM s WHERE FORM IN ('10-K','10-Q') AND LEFT(AFS,1) IN ('1','2')),
late AS (SELECT *, DATEDIFF(day, pd, fd) lag, DATEADD(day, ext_days, pd) ext_due FROM l WHERE DATEDIFF(day, pd, fd) > ext_days + 3),
tk AS (SELECT CIK, LISTAGG(DISTINCT EXCHANGE, '/') exch, MIN(TICKER) tick FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE GROUP BY 1),
sub AS (SELECT ACCESSION_NUMBER, TRY_TO_NUMBER(ISSUER_CIK) cik FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION
        WHERE TRY_TO_NUMBER(ISSUER_CIK) IN (SELECT cik FROM late)),
tr AS (SELECT s2.cik, t.TRANSACTION_DATE d, t.TRANSACTION_CODE code, t.TRANSACTION_VALUE v
       FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS t JOIN sub s2 ON s2.ACCESSION_NUMBER = t.ACCESSION_NUMBER
       WHERE t.TRANSACTION_CODE IN ('S','P'))
SELECT late.q, late.NAME, late.cik, late.FORM, late.AFS, late.SIC, late.STPRBA, late.pd, late.ext_due, late.fd, late.lag, late.PREVRPT, tk.exch, tk.tick,
       COUNT_IF(tr.code = 'S' AND tr.d >= late.ext_due AND tr.d < late.fd) sales_in_gap, ROUND(SUM(IFF(tr.code = 'S' AND tr.d >= late.ext_due AND tr.d < late.fd, tr.v, 0))) sale_usd_in_gap,
       COUNT_IF(tr.code = 'P' AND tr.d >= late.ext_due AND tr.d < late.fd) buys_in_gap,
       COUNT_IF(tr.code = 'S' AND tr.d >= DATEADD(day, -365, late.ext_due) AND tr.d < late.ext_due) sales_prior_365,
       ROUND(SUM(IFF(tr.code = 'S' AND tr.d >= DATEADD(day, -365, late.ext_due) AND tr.d < late.ext_due, tr.v, 0))) sale_usd_prior_365,
       MIN(tr.d) ins_d0, MAX(tr.d) ins_d1
FROM late LEFT JOIN tk ON tk.CIK = late.cik LEFT JOIN tr ON tr.cik = late.cik
GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14
ORDER BY late.AFS, late.lag DESC;

-- S17 Ticker table check and join land rate: the battery's CPTKF count, and how many 2024Q1 10-K filers have a ticker, by filer size
WITH tk AS (SELECT CIK, LISTAGG(DISTINCT EXCHANGE, '/') exch FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE GROUP BY 1)
SELECT LEFT(s.AFS,1) afs1, COUNT(*) k10, COUNT(tk.CIK) with_ticker, COUNT_IF(tk.exch ILIKE '%nasdaq%' OR tk.exch ILIKE '%nyse%') on_nasdaq_nyse,
       COUNT_IF(tk.exch = 'OTC') otc_only,
       (SELECT COUNT_IF(TICKER = 'CPTKF') FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE) cptkf_rows,
       (SELECT COUNT_IF(EXCHANGE IS NULL OR EXCHANGE = '') FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE) blank_exch,
       (SELECT MAX(_LOADED_AT) FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE) loaded_micros
FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q1 s LEFT JOIN tk ON tk.CIK = TRY_TO_NUMBER(s.CIK)
WHERE s.FORM = '10-K' GROUP BY 1 ORDER BY 1;
