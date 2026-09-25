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
FROM f GROUP BY 1 ORDER BY fd0
