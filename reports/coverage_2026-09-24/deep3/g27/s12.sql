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
FROM x GROUP BY 1 ORDER BY 1
