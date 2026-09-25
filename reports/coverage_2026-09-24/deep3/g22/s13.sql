-- S13 DOJ Epstein library crawl: pages, link kinds, file links per page, EFTA number range per page (tests the page-1-only cap)
WITH t AS (SELECT page_url, href, resolved_url, link_text, fetched_at_utc, _loaded_at,
                  CASE WHEN resolved_url ILIKE '%/epstein/files/%' THEN 'file'
                       WHEN resolved_url ILIKE '%/media/%' THEN 'media'
                       WHEN resolved_url ILIKE '%facebook%' OR resolved_url ILIKE '%twitter%' OR resolved_url ILIKE '%x.com%' OR resolved_url ILIKE '%linkedin%' THEN 'share'
                       WHEN resolved_url ILIKE '%justice.gov%' THEN 'doj_other' ELSE 'other' END kind,
                  TRY_TO_NUMBER(REGEXP_SUBSTR(resolved_url, 'EFTA0*([0-9]+)', 1, 1, 'ie', 1)) efta
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_DOJ_EPSTEIN_LIBRARY)
SELECT 'page' k, REGEXP_REPLACE(page_url, '^https?://[^/]+', '') item, COUNT(*) n, COUNT_IF(kind = 'file') files, COUNT_IF(kind = 'media') media,
       COUNT_IF(kind = 'share') share, MIN(efta) efta_min, MAX(efta) efta_max, COUNT(DISTINCT efta) efta_nd, MIN(fetched_at_utc)::VARCHAR t0, MAX(fetched_at_utc)::VARCHAR t1
FROM t GROUP BY 1,2
UNION ALL
SELECT 'kind', kind, COUNT(*), COUNT(DISTINCT resolved_url), COUNT(DISTINCT page_url), NULL, NULL, NULL, NULL,
       ANY_VALUE(LEFT(resolved_url, 90)), NULL FROM t GROUP BY 1,2
UNION ALL
SELECT 'file_ext', LOWER(REGEXP_SUBSTR(resolved_url, '\.([a-zA-Z0-9]{2,4})(\?|$)', 1, 1, 'e', 1)), COUNT(*), COUNT(DISTINCT resolved_url), NULL, NULL, NULL, NULL, NULL, NULL, NULL
FROM t WHERE kind = 'file' GROUP BY 1,2
UNION ALL
SELECT 'loads', NULL, COUNT(*), COUNT(DISTINCT _loaded_at), COUNT(DISTINCT fetched_at_utc), COUNT(DISTINCT page_url, href), NULL, NULL, NULL, MIN(_loaded_at)::VARCHAR, MAX(_loaded_at)::VARCHAR FROM t
ORDER BY 1, 2
