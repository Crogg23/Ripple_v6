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
ORDER BY ABS(x.v_fixed - x.v) DESC
