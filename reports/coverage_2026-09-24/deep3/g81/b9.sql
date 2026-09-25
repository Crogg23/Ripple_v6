-- S30 Wayback: which pages ever got a full-size (themed, >5,000-byte) 403 instead of the ~937-byte edge block, plus the short-path 403s of 2026-02-19
WITH p AS (
  SELECT URLKEY, COUNT_IF(HTTP_STATUS = 403) n403, COUNT_IF(HTTP_STATUS = 403 AND CONTENT_BYTES > 5000) n403_big,
         MIN(IFF(HTTP_STATUS = 403, CONTENT_BYTES, NULL)) b403_min, MAX(IFF(HTTP_STATUS = 403, CONTENT_BYTES, NULL)) b403_max,
         MIN(IFF(HTTP_STATUS = 403 AND CONTENT_BYTES > 5000, CAPTURED_AT, NULL)) big_t0, MAX(IFF(HTTP_STATUS = 403 AND CONTENT_BYTES > 5000, CAPTURED_AT, NULL)) big_t1,
         LISTAGG(DISTINCT HTTP_STATUS::STRING, ',') statuses, MAX(IFF(HTTP_STATUS = 200, CAPTURED_AT, NULL)) last_200, MIN(IFF(HTTP_STATUS = 200, CAPTURED_AT, NULL)) first_200
  FROM LIBRARY_MARTS.EPSTEIN.FCT_WAYBACK_PAGE_CHANGES GROUP BY 1)
SELECT REGEXP_REPLACE(URLKEY, '^gov,justice[)]/epstein/doj-disclosures', '') path, n403, n403_big, b403_min, b403_max, big_t0, big_t1, statuses, first_200, last_200
FROM p
WHERE n403_big > 0 OR URLKEY IN ('gov,justice)/epstein/doj-disclosures/dat', 'gov,justice)/epstein/doj-disclosures/data-set', 'gov,justice)/epstein/doj-disclosures/data-set-1',
      'gov,justice)/epstein/doj-disclosures/data-set-11', 'gov,justice)/epstein/doj-disclosures/data-set-1-files?page=63')
ORDER BY big_t0 NULLS LAST, path;
