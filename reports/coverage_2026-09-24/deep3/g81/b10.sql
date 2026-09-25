-- S31 Wayback: the control case, full capture timeline of the data-set-9..12 base pages up to 2026-02-05 (status, bytes)
SELECT REGEXP_REPLACE(URLKEY, '^gov,justice[)]/epstein/doj-disclosures', '') path, CAPTURED_AT, CHANGE_KIND, PREV_HTTP_STATUS, HTTP_STATUS, CONTENT_BYTES, HOURS_SINCE_PREV_CAPTURE
FROM LIBRARY_MARTS.EPSTEIN.FCT_WAYBACK_PAGE_CHANGES
WHERE URLKEY IN ('gov,justice)/epstein/doj-disclosures/data-set-9-files', 'gov,justice)/epstein/doj-disclosures/data-set-10-files',
                 'gov,justice)/epstein/doj-disclosures/data-set-11-files', 'gov,justice)/epstein/doj-disclosures/data-set-12-files')
  AND CAPTURED_AT < '2026-02-05'
ORDER BY path, CAPTURED_AT;
