-- S24 UK company-number holes, 6 Oct 2025-1 Feb 2026: per incorporation day, numbers on the live register, numbers found only in the PSC file (dissolved), and holes that match no company in either file; with hole-run sizes (scattered singles vs blocks)
WITH live AS (
  SELECT TO_NUMBER(COMPANY_NUMBER) n, INCORPORATION_DATE d
  FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE
  WHERE COMPANY_NUMBER RLIKE '[0-9]{8}' AND TO_NUMBER(COMPANY_NUMBER) BETWEEN 16764035 AND 17005537),
pscn AS (
  SELECT DISTINCT TO_NUMBER(COMPANY_NUMBER) n
  FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC
  WHERE COMPANY_NUMBER RLIKE '[0-9]{8}' AND TRY_TO_NUMBER(COMPANY_NUMBER) BETWEEN 16764035 AND 17005537),
allp AS (
  SELECT n, 1 is_live FROM live
  UNION ALL
  SELECT n, 0 FROM pscn WHERE n NOT IN (SELECT n FROM live)),
s AS (SELECT n, is_live, n - LAG(n) OVER (ORDER BY n) - 1 gap_before FROM allp),
dr AS (SELECT d, MIN(n) lo, MAX(n) hi FROM live GROUP BY d),
j AS (SELECT dr.d, dr.lo, dr.hi, s.* FROM s JOIN dr ON s.n BETWEEN dr.lo AND dr.hi)
SELECT d, DAYNAME(d) dow, MAX(hi) - MIN(lo) + 1 numbers, SUM(is_live) live, COUNT_IF(is_live = 0) psc_only,
       MAX(hi) - MIN(lo) + 1 - COUNT(*) holes,
       COUNT_IF(gap_before > 0 AND n > lo) hole_runs,
       COUNT_IF(gap_before = 1 AND n > lo) single_holes,
       MAX(IFF(n > lo, gap_before, 0)) max_run
FROM j GROUP BY 1,2 ORDER BY 1;
