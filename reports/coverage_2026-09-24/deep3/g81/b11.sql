-- S32 Wayback completeness: any address at all for data sets 13-40 (base page, listing pages, variants), and any 200 among them
SELECT TRY_TO_NUMBER(REGEXP_SUBSTR(URLKEY, 'data-set-([0-9]+)', 1, 1, 'e', 1)) ds, COUNT(DISTINCT URLKEY) urlkeys, COUNT(*) n,
       COUNT_IF(HTTP_STATUS = 200) n200, LISTAGG(DISTINCT HTTP_STATUS::STRING, ',') statuses, MIN(CAPTURED_AT) t0, MAX(CAPTURED_AT) t1,
       MIN(IFF(HTTP_STATUS = 200, CAPTURED_AT, NULL)) first_200
FROM LIBRARY_MARTS.EPSTEIN.FCT_WAYBACK_PAGE_CHANGES
WHERE REGEXP_LIKE(URLKEY, '.*data-set-[0-9]+.*')
GROUP BY 1 ORDER BY 1;
