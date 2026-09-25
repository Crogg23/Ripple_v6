-- S22 UK Companies House survivorship check: England & Wales company numbers are issued in sequence, so the number range per incorporation day counts companies issued that day, dissolved ones included. Oct-Mar in 2024-25 and 2025-26
WITH t AS (
  SELECT INCORPORATION_DATE d, TO_NUMBER(COMPANY_NUMBER) n
  FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE
  WHERE COMPANY_NUMBER RLIKE '[0-9]{8}'
    AND (INCORPORATION_DATE BETWEEN '2024-10-01' AND '2025-03-31' OR INCORPORATION_DATE BETWEEN '2025-10-01' AND '2026-03-31'))
SELECT d, DAYNAME(d) dow, COUNT(*) live, MIN(n) n_min, MAX(n) n_max, APPROX_PERCENTILE(n, 0.02) n_p02, APPROX_PERCENTILE(n, 0.98) n_p98
FROM t GROUP BY 1,2 ORDER BY 1;
