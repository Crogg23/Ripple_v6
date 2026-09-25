-- deep3/g27: deep pass 3, 2026-09-24. Python door (connect/db.py), read-only SELECT/WITH only, QUERY_TAG 'deep3-2026-09-24'.
-- Every connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'. Those two are not counted.
-- Tables: FINANCE__FED_SEC_EDGAR_INSIDERS, FINANCE__INTL_WB_IDS, FINANCE__FED_SEC_13F_SUBMISSION, FINANCE__FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS, FINANCE__INTL_OSFI_REGULATED_FI.
-- Statements in run order below (Sxx). Small tables were pulled whole and analysed locally in pandas; scratch in g27/ (out_Sxx.pkl / .csv, an_*.py).

-- S01 WB IDS: pull whole table (63K rows) for local analysis  [62983 rows, 3.2s, qid 01c74b94-040b-a770-0026-eed301339c8e]
SELECT * FROM LIBRARY_MARTS.FINANCE.FINANCE__INTL_WB_IDS;

-- S02 EDGAR insiders: pull whole table (69K rows) for local analysis  [69259 rows, 1.6s, qid 01c74b94-040b-a028-0026-eed30133d72a]
SELECT * FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_INSIDERS;

-- S03 Series/class: pull whole table (43K rows)  [43123 rows, 1.7s, qid 01c74b94-040b-a07c-0026-eed30133e74a]
SELECT * FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS;

-- S04 OSFI: pull whole table (343 rows)  [343 rows, 0.7s, qid 01c74b94-040b-a5bb-0026-eed30133f622]
SELECT * FROM LIBRARY_MARTS.FINANCE.FINANCE__INTL_OSFI_REGULATED_FI;

-- S05 EDGAR insiders: accession overlap with the four other SEC insider tables  [1 rows, 2.7s, qid 01c74b98-040b-a770-0026-eed301339cbe]
-- EDGAR insiders: does it overlap the other SEC insider tables (dupe/coverage check), and do its CIKs look padded
WITH e AS (SELECT ACCESSION_NUMBER a, DOCUMENT_TYPE dt FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_INSIDERS)
SELECT
  (SELECT COUNT(*) FROM e) e_rows,
  (SELECT COUNT(*) FROM e WHERE a IN (SELECT ACCESSION_NUMBER FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION)) in_submission,
  (SELECT COUNT(*) FROM e WHERE a IN (SELECT ACCESSION_NUMBER FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER)) in_owner,
  (SELECT COUNT(*) FROM e WHERE a IN (SELECT ACCESSION_NUMBER FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS)) in_nonderiv,
  (SELECT COUNT(*) FROM e WHERE a IN (SELECT ACCESSION_NUMBER FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_DERIV_TRANS)) in_deriv,
  (SELECT MAX(FILING_DATE) FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION) sub_max_filed,
  (SELECT COUNT(*) FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION WHERE FILING_DATE >= '2026-01-01') sub_2026_rows;

-- S06 DERA 2025Q1-2026Q1 annual-report filers (10-K/20-F/40-F) + exchange tickers  [7118 rows, 2.1s, qid 01c74b98-040b-9feb-0026-eed30133c772]
-- Universe of annual-report filers (10-K domestic, 20-F / 40-F foreign private issuers) from DERA SUB 2025Q1-2026Q1, with exchange tickers attached
WITH f AS (
  SELECT CIK, NAME, COUNTRYBA, COUNTRYINC, FORM, FILED FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q1 WHERE FORM IN ('10-K','20-F','40-F')
  UNION ALL SELECT CIK, NAME, COUNTRYBA, COUNTRYINC, FORM, FILED FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q2 WHERE FORM IN ('10-K','20-F','40-F')
  UNION ALL SELECT CIK, NAME, COUNTRYBA, COUNTRYINC, FORM, FILED FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q3 WHERE FORM IN ('10-K','20-F','40-F')
  UNION ALL SELECT CIK, NAME, COUNTRYBA, COUNTRYINC, FORM, FILED FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q4 WHERE FORM IN ('10-K','20-F','40-F')
  UNION ALL SELECT CIK, NAME, COUNTRYBA, COUNTRYINC, FORM, FILED FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2026Q1 WHERE FORM IN ('10-K','20-F','40-F')
), g AS (
  SELECT TRY_TO_NUMBER(CIK) cikn, MAX(NAME) name, MAX(COUNTRYBA) countryba, MAX(COUNTRYINC) countryinc,
         LISTAGG(DISTINCT FORM, ',') forms, MAX(FILED) last_filed, COUNT(*) n_filings
  FROM f GROUP BY 1
), t AS (
  SELECT CIK, LISTAGG(DISTINCT TICKER, ',') tickers, LISTAGG(DISTINCT EXCHANGE, ',') exchanges
  FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE GROUP BY 1
)
SELECT g.*, t.tickers, t.exchanges FROM g LEFT JOIN t ON t.CIK = g.cikn;

-- S07 20-F/40-F filer size class (AFS) + ticker list load time  [1228 rows, 0.9s, qid 01c74b9a-040b-a6f8-0026-eed30133ac56]
-- Size proxy for the peer test: SEC filer status (AFS: 1-LAF large accelerated ... 5-SML) per 20-F/40-F filer, latest filing wins; plus when the ticker list was loaded
WITH f AS (
  SELECT CIK, AFS, FORM, FILED FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q1 WHERE FORM IN ('20-F','40-F')
  UNION ALL SELECT CIK, AFS, FORM, FILED FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q2 WHERE FORM IN ('20-F','40-F')
  UNION ALL SELECT CIK, AFS, FORM, FILED FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q3 WHERE FORM IN ('20-F','40-F')
  UNION ALL SELECT CIK, AFS, FORM, FILED FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q4 WHERE FORM IN ('20-F','40-F')
  UNION ALL SELECT CIK, AFS, FORM, FILED FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2026Q1 WHERE FORM IN ('20-F','40-F')
)
SELECT TRY_TO_NUMBER(CIK) cikn, MAX_BY(AFS, FILED) afs,
       (SELECT TO_TIMESTAMP(MAX(_LOADED_AT)::NUMBER, 6) FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE) tickers_loaded
FROM f GROUP BY 1;

-- S08 13F info table: filings/quarters held, units, dup lines, via 13F_SUBMISSIONS  [320 rows, 1.6s, qid 01c74b9d-040b-a5bb-0026-eed30133f69a]
-- 13F info table: which filings/quarters it holds (join accession to the 13F filings table), units, and duplicate lines
WITH h AS (
  SELECT ACCESSION_NUMBER a, COUNT(*) n, COUNT(DISTINCT INFOTABLE_SK) n_sk,
         SUM(TRY_TO_DOUBLE(VALUE_COL)) v, COUNT_IF(TRY_TO_DOUBLE(VALUE_COL) IS NULL) v_bad,
         COUNT_IF(SSHPRNAMTTYPE = 'PRN') prn, COUNT_IF(NULLIF(TRIM(PUTCALL),'') IS NOT NULL) opt,
         SUM(SSHPRNAMT) sh
  FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSION GROUP BY 1
)
SELECT s.PERIODOFREPORT, s.SUBMISSIONTYPE, s._SRC_FILE,
       MIN(s.FILING_DATE) f0, MAX(s.FILING_DATE) f1,
       COUNT(*) filings, COUNT(DISTINCT s.CIK) ciks, SUM(h.n) lines, SUM(h.n - h.n_sk) dup_sk, SUM(h.v) value_sum, SUM(h.v_bad) v_bad, SUM(h.prn) prn, SUM(h.opt) opt
FROM h LEFT JOIN LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS s ON s.ACCESSION_NUMBER = h.a
GROUP BY ROLLUP(1, 2, 3) ORDER BY lines DESC NULLS LAST;

-- S09 13F info table vs 13F_HOLDINGS: same zip already loaded? (accession and line match)  [2 rows, 3.3s, qid 01c74b9d-040b-a5bb-0026-eed30133f6a6]
-- Is the 13F info table the same zip window already inside FINANCE__FED_SEC_13F_HOLDINGS? Compare accessions and lines
WITH s AS (SELECT ACCESSION_NUMBER a, COUNT(*) n, SUM(TRY_TO_DOUBLE(VALUE_COL)) v FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSION GROUP BY 1),
     h AS (SELECT ACCESSION_NUMBER a, SRC_FILE, COUNT(*) n, SUM(VALUE_USD) v, MAX(VALUE_UNIT) unit
           FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_HOLDINGS
           WHERE ACCESSION_NUMBER IN (SELECT a FROM s) OR SRC_FILE ILIKE '%2026%'
           GROUP BY 1, 2)
SELECT h.SRC_FILE, h.unit, COUNT(*) h_accessions, SUM(h.n) h_lines, SUM(h.v) h_value,
       COUNT(s.a) matched_accessions, SUM(s.n) s_lines_matched, SUM(s.v) s_value_matched,
       COUNT_IF(s.a IS NOT NULL AND s.n <> h.n) line_count_mismatch,
       (SELECT COUNT(*) FROM s) s_accessions_total, (SELECT SUM(n) FROM s) s_lines_total
FROM h LEFT JOIN s ON s.a = h.a
GROUP BY 1, 2 ORDER BY 1;

-- S10 13F filings: late original 13F-HR (180d+, 2y+) per filing window, time series  [46 rows, 0.8s, qid 01c74b9e-040b-9fb8-0026-eed30134365a]
-- Time: per filing window, how many ORIGINAL 13F-HR reports were filed 2+ quarters after their quarter ended (catch-up filings), and by how many managers
WITH f AS (
  SELECT _SRC_FILE w, CIK, SUBMISSIONTYPE t,
         TRY_TO_DATE(FILING_DATE, 'DD-MON-YYYY') fd, TRY_TO_DATE(PERIODOFREPORT, 'DD-MON-YYYY') pr
  FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS
)
SELECT w, MIN(fd) fd0, MAX(fd) fd1, COUNT(*) filings, COUNT_IF(t = '13F-HR') hr_orig,
       COUNT_IF(t = '13F-HR' AND DATEDIFF('day', pr, fd) > 180) hr_late_180d,
       COUNT(DISTINCT IFF(t = '13F-HR' AND DATEDIFF('day', pr, fd) > 180, CIK, NULL)) late_ciks,
       COUNT_IF(t = '13F-HR' AND DATEDIFF('day', pr, fd) > 730) hr_late_2y,
       COUNT_IF(fd IS NULL OR pr IS NULL) bad_dates
FROM f GROUP BY 1 ORDER BY fd0;

-- S11 13F spring-2026 window: filings typed in wrong units (same-CUSIP median price test)  [376 rows, 3.6s, qid 01c74b9e-040b-a029-0026-eed30133b87e]
-- Units check inside the spring-2026 window (dollars era): per CUSIP median price, then filings where most lines sit 300x+ below (thousands typed) or above the same-CUSIP median
WITH l AS (
  SELECT ACCESSION_NUMBER a, CUSIP, TRY_TO_DOUBLE(VALUE_COL) v, SSHPRNAMT sh
  FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSION
  WHERE SSHPRNAMTTYPE = 'SH' AND NULLIF(TRIM(PUTCALL), '') IS NULL AND SSHPRNAMT > 0 AND TRY_TO_DOUBLE(VALUE_COL) > 0
), m AS (
  SELECT CUSIP, MEDIAN(v / sh) mp FROM l GROUP BY 1 HAVING COUNT(*) >= 20
), x AS (
  SELECT l.a, COUNT(*) lines, COUNT_IF(l.v / l.sh < m.mp / 300) low, COUNT_IF(l.v / l.sh > m.mp * 300) high,
         SUM(l.v) v, SUM(IFF(l.v / l.sh < m.mp / 300, l.v * 1000, IFF(l.v / l.sh > m.mp * 300, l.v / 1000, l.v))) v_fixed
  FROM l JOIN m ON m.CUSIP = l.CUSIP GROUP BY 1
)
SELECT x.*, f.FILINGMANAGER_NAME, f.REPORTCALENDARORQUARTER, f.FILINGMANAGER_STATEORCOUNTRY,
       (SELECT COUNT(*) FROM x) filings_checked, (SELECT SUM(v) FROM x) v_all, (SELECT SUM(v_fixed) FROM x) v_all_fixed
FROM x LEFT JOIN LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS f ON f.ACCESSION_NUMBER = x.a
WHERE x.low >= 0.5 * x.lines OR x.high >= 0.5 * x.lines OR x.low + x.high >= 50
ORDER BY ABS(x.v_fixed - x.v) DESC;

-- S12 13F_HOLDINGS dollars-era windows: thousands-typed filings over time, T. Rowe tracked  [10 rows, 10.9s, qid 01c74b9f-040b-a911-0026-eed301344636]
-- Time: same units test on every dollars-era window in FINANCE__FED_SEC_13F_HOLDINGS (Jan 2024 - May 2026). Per window: filings with most lines 300x+ below same-CUSIP median, value as reported vs x1000; T. Rowe Price Associates (CIK 80255 accession prefix) tracked
WITH l AS (
  SELECT SRC_FILE w, ACCESSION_NUMBER a, CUSIP, VALUE_USD v, SSHPRNAMT sh
  FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_HOLDINGS
  WHERE VALUE_UNIT = 'dollars' AND SSHPRNAMTTYPE = 'SH' AND NULLIF(TRIM(PUTCALL), '') IS NULL AND SSHPRNAMT > 0 AND VALUE_USD > 0
), m AS (
  SELECT w, CUSIP, MEDIAN(v / sh) mp FROM l GROUP BY 1, 2 HAVING COUNT(*) >= 20
), x AS (
  SELECT l.w, l.a, COUNT(*) lines, COUNT_IF(l.v / l.sh < m.mp / 300) low, SUM(l.v) v
  FROM l JOIN m ON m.w = l.w AND m.CUSIP = l.CUSIP GROUP BY 1, 2
)
SELECT w, COUNT(*) filings, COUNT_IF(low >= 0.5 * lines) thousands_filings,
       SUM(v) v_reported, SUM(IFF(low >= 0.5 * lines, v, 0)) v_thousands_filings,
       SUM(IFF(low >= 0.5 * lines, v * 999, 0)) understatement,
       MAX(IFF(a LIKE '0000080255-%', a, NULL)) trowe_acc, MAX(IFF(a LIKE '0000080255-%', v, NULL)) trowe_v, MAX(IFF(a LIKE '0000080255-%', ROUND(low / lines, 3), NULL)) trowe_low_share
FROM x GROUP BY 1 ORDER BY 1;

-- Not warehouse statements (no budget): six EDGAR pages read by hand to check the table against primary records:
--   Form 3 lists (browse-edgar type=3) for CIK 1759783 EHang, 1723935 Sunlands, 1770088 WiMi, 1976908 Jiade;
--   filing index + primary_doc.xml of 13F accession 0000080255-26-000381 (T. Rowe Price Associates, tableValueTotal 864,926,710).
-- Local analysis scripts: g27/an_wb.py, an_wb2.py, an_wb3.py (World Bank), an_ins.py, an_ins2.py, an_fpi.py, an_fpi2.py, an_fpi3.py (insiders/FPI).
