-- S14 MAUDE barcodes that miss GUDID: what they look like (length, prefix), top makers; tests whether the miss is format or absence
WITH m AS (SELECT NULLIF(TRIM(udi_di),'') di, manufacturer_name mfr, event_type FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_MAUDE),
g AS (SELECT DISTINCT primary_di FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID),
x AS (SELECT m.* FROM m LEFT JOIN g ON g.primary_di = m.di WHERE m.di IS NOT NULL AND g.primary_di IS NULL)
SELECT 'len' k, LENGTH(di)::string v, COUNT(*) n, COUNT(DISTINCT di) d, ANY_VALUE(di) eg FROM x GROUP BY 1,2
UNION ALL SELECT 'mfr', mfr, COUNT(*), COUNT(DISTINCT di), ANY_VALUE(di) FROM x GROUP BY 1,2 QUALIFY ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) <= 12
UNION ALL SELECT 'strip_lead0_hits', NULL, COUNT(*), COUNT(DISTINCT x.di), ANY_VALUE(x.di) FROM x JOIN g ON LTRIM(g.primary_di,'0') = LTRIM(x.di,'0')
ORDER BY 1, 3 DESC
