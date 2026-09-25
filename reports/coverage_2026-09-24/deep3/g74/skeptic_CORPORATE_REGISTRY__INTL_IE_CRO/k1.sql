-- K01 headline re-derive (builder's exact population and key) plus robustness: excluding the top 4 addresses, same-year concentration (addresses with 100+/50+ formations that year), top-10 share per year, a coarser first-part key, weekend-dated rows, and the rows the builder dropped for no address
WITH base AS (
  SELECT COMPANY_ID, INCORPORATION_DATE d, YEAR(INCORPORATION_DATE) y,
         IFF(REGISTERED_ADDRESS IS NULL OR REGISTERED_ADDRESS ILIKE '%NO ADDRESS%', 1, 0) noaddr,
         REGEXP_REPLACE(UPPER(SPLIT_PART(REGISTERED_ADDRESS, ',', 1) || SPLIT_PART(REGISTERED_ADDRESS, ',', 2)), '[^A-Z0-9]', '') a2,
         REGEXP_REPLACE(UPPER(SPLIT_PART(REGISTERED_ADDRESS, ',', 1)), '[^A-Z0-9]', '') a1
  FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_IE_CRO),
t AS (SELECT * FROM base WHERE d IS NOT NULL AND d <> '1901-01-01' AND noaddr = 0),
ac AS (SELECT a2, COUNT(*) an, COUNT_IF(y BETWEEN 1990 AND 1999) a90 FROM t GROUP BY 1),
top4 AS (SELECT a2 FROM ac QUALIFY ROW_NUMBER() OVER (ORDER BY a90 DESC) <= 4),
ya2 AS (SELECT y, a2, COUNT(*) k2, ROW_NUMBER() OVER (PARTITION BY y ORDER BY COUNT(*) DESC, a2) rk FROM t GROUP BY 1,2),
ya1 AS (SELECT y, a1, COUNT(*) k1 FROM t GROUP BY 1,2),
j AS (
  SELECT t.y, t.d, ac.an, ya2.k2, ya2.rk, ya1.k1, IFF(top4.a2 IS NULL, 0, 1) istop4
  FROM t JOIN ac ON ac.a2 = t.a2 JOIN ya2 ON ya2.y = t.y AND ya2.a2 = t.a2 JOIN ya1 ON ya1.y = t.y AND ya1.a1 = t.a1
  LEFT JOIN top4 ON top4.a2 = t.a2),
agg AS (
  SELECT y, COUNT(*) n, COUNT_IF(an >= 1000) at1000, COUNT_IF(an >= 1000 AND istop4 = 0) at1000_ex_top4, COUNT_IF(istop4 = 1) top4n,
         COUNT_IF(k2 >= 100) sy100, COUNT_IF(k2 >= 50) sy50, COUNT_IF(rk <= 10) top10, COUNT_IF(k1 >= 100) a1_sy100,
         COUNT_IF(DAYOFWEEKISO(d) >= 6) wkend, COUNT_IF(an >= 1000 AND DAYOFWEEKISO(d) >= 6) wkend_at1000
  FROM j GROUP BY 1),
den AS (SELECT y, COUNT(*) all_rows, SUM(noaddr) noaddr_n FROM base WHERE d IS NOT NULL AND d <> '1901-01-01' GROUP BY 1)
SELECT agg.y, agg.n, agg.at1000, agg.at1000_ex_top4, agg.top4n, agg.sy100, agg.sy50, agg.top10, agg.a1_sy100, agg.wkend, agg.wkend_at1000, den.all_rows, den.noaddr_n
FROM agg JOIN den ON den.y = agg.y WHERE agg.y >= 1960
UNION ALL
SELECT -1, COUNT(*), COUNT_IF(ac.an >= 1000), NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, COUNT(*), SUM(b.noaddr)
FROM base b LEFT JOIN ac ON ac.a2 = b.a2 WHERE b.d IS NULL OR b.d = '1901-01-01'
ORDER BY 1;

-- K02 completeness: company numbers are issued in sequence, so missing numbers inside each year's run show purged companies
WITH t AS (SELECT TRY_TO_NUMBER(COMPANY_ID) n, YEAR(INCORPORATION_DATE) y FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_IE_CRO),
s AS (SELECT n, y, n - LAG(n) OVER (ORDER BY n) - 1 gap, LAG(y) OVER (ORDER BY n) py FROM t WHERE n IS NOT NULL)
SELECT y, COUNT(*) cnt, MIN(n) lo, MAX(n) hi, APPROX_PERCENTILE(n, 0.01) p01, APPROX_PERCENTILE(n, 0.99) p99,
       SUM(IFF(py = y AND gap > 0, gap, 0)) missing_in_year, COUNT_IF(py = y AND gap > 0) gap_runs, MAX(IFF(py = y, gap, NULL)) maxgap
FROM s WHERE y BETWEEN 1980 AND 2026 OR y IS NULL GROUP BY 1
UNION ALL
SELECT -1, COUNT_IF(TRY_TO_NUMBER(COMPANY_ID) IS NULL), NULL, NULL, NULL, NULL, NULL, NULL, NULL FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_IE_CRO
ORDER BY 1;

-- K03 raw landing columns: a few rows from the 1992 and 1995 bulk-dated ranges
SELECT * FROM LIBRARY_RAW.LANDING.INTL_IE_CRO WHERE TRIM(COMPANY_NUM) IN ('188245', '188300', '229741', '229800', '700000')
