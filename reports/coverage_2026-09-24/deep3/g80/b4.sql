-- S10 Wayback listing replay: for every captured listing page, the pager's Last page, the highest page linked, and the PDF range shown
SELECT PAGE_URL, CAPTURE_TIMESTAMP_RAW, CAPTURED_AT,
       MAX(IFF(LINK_TEXT = 'Last', TRY_TO_NUMBER(REGEXP_SUBSTR(HREF, 'page=([0-9]+)', 1, 1, 'e', 1)), NULL)) last_pg,
       MAX(TRY_TO_NUMBER(REGEXP_SUBSTR(HREF, '^[?]page=([0-9]+)$', 1, 1, 'e', 1))) max_pg_link,
       COUNT_IF(RESOLVED_URL ILIKE '%.pdf%') pdfs, COUNT(*) links,
       MIN(TRY_TO_NUMBER(REGEXP_SUBSTR(RESOLVED_URL, 'EFTA0*([0-9]+)', 1, 1, 'e', 1))) efta_min,
       MAX(TRY_TO_NUMBER(REGEXP_SUBSTR(RESOLVED_URL, 'EFTA0*([0-9]+)', 1, 1, 'e', 1))) efta_max
FROM LIBRARY_MARTS.INVESTIGATIONS.INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_LISTING
GROUP BY 1, 2, 3 ORDER BY 1, 2
;

-- S11 Wayback CDX, data-set listing pages only: per data set and week, captures, distinct pages, highest page number captured, status mix
WITH p AS (
  SELECT TRY_TO_NUMBER(REGEXP_SUBSTR(ORIGINAL_URL, 'data-set-([0-9]+)-files', 1, 1, 'e', 1)) ds,
         TRY_TO_NUMBER(REGEXP_SUBSTR(ORIGINAL_URL, '[?&]page=([0-9]+)', 1, 1, 'e', 1)) pg,
         DATE_TRUNC('week', CAPTURED_AT)::date wk, STATUS_CODE::string st
  FROM LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__XC_WAYBACK_DOJ_EPSTEIN
  WHERE ORIGINAL_URL ILIKE '%/data-set-%-files%'
)
SELECT ds, wk, COUNT(*) captures, COUNT(DISTINCT pg) pages, MAX(pg) max_pg,
       MAX(IFF(st = '200', pg, NULL)) max_pg_200, COUNT_IF(st = '200') s200, COUNT_IF(st LIKE '3%') s3xx,
       COUNT_IF(st LIKE '4%') s4xx, COUNT_IF(st LIKE '5%') s5xx, COUNT_IF(st IS NULL OR st NOT RLIKE '[0-9]{3}') s_other
FROM p WHERE ds IS NOT NULL
GROUP BY 1, 2 ORDER BY 1, 2
;
