-- S28 Wayback (S25 rerun, regex fixed): every page that ever answered 404 or ended on 403/401, junk URL variants excluded, with dates
WITH p AS (
  SELECT URLKEY, MIN(CAPTURED_AT) t0, MAX(CAPTURED_AT) t1, MAX_BY(HTTP_STATUS, CAPTURED_AT) last_status,
         MIN(IFF(HTTP_STATUS = 404, CAPTURED_AT, NULL)) first_404, MAX(IFF(HTTP_STATUS = 200, CAPTURED_AT, NULL)) last_200,
         LISTAGG(DISTINCT HTTP_STATUS::STRING, ',') statuses
  FROM LIBRARY_MARTS.EPSTEIN.FCT_WAYBACK_PAGE_CHANGES GROUP BY 1)
SELECT REGEXP_REPLACE(URLKEY, '^gov,justice[)]/epstein/doj-disclosures', '') path, t0, t1, last_status, first_404, last_200, statuses
FROM p
WHERE (first_404 IS NOT NULL OR last_status IN (403, 401))
  AND NOT REGEXP_LIKE(URLKEY, '.*(utm_|fbclid|%0a|%e|%c2|u003c|&data=|[?&]ref=|gclid).*')
  AND NOT (URLKEY LIKE '%.' OR URLKEY LIKE '%)' OR URLKEY LIKE '%).' OR CONTAINS(URLKEY, CHR(92)))
ORDER BY first_404 NULLS LAST, path;
