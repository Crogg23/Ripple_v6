-- S02 MAUDE -> GUDID land rate on the device barcode (MAUDE.UDI_DI = GUDID.PRIMARY_DI), by event type
WITH m AS (
  SELECT NULLIF(TRIM(udi_di),'') di, event_type, YEAR(TRY_TO_DATE(date_received::string)) yr
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_MAUDE),
g AS (SELECT DISTINCT primary_di FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID)
SELECT m.event_type, MIN(yr) y0, MAX(yr) y1, COUNT(*) reports, COUNT(m.di) with_di,
       COUNT(g.primary_di) landed, COUNT(DISTINCT m.di) distinct_di, COUNT(DISTINCT g.primary_di) distinct_landed
FROM m LEFT JOIN g ON g.primary_di = m.di
GROUP BY 1 ORDER BY reports DESC
