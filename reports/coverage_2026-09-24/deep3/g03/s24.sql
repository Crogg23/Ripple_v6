-- S24 GUDID barcodes that repeat: top repeaters, how many record keys and version dates each, who labels them
WITH r AS (SELECT primary_di, COUNT(*) n FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID GROUP BY 1 HAVING COUNT(*) > 1)
SELECT 'summary' k, NULL di, COUNT(*) n_dis, SUM(n) rows_, MAX(n) max_rows, NULL keys_, NULL vers, NULL cos, NULL eg_desc FROM r
UNION ALL
SELECT 'top', g.primary_di, NULL, COUNT(*), NULL, COUNT(DISTINCT g.public_device_record_key), COUNT(DISTINCT g.public_version_date),
       ANY_VALUE(g.company_name), ANY_VALUE(LEFT(g.device_description, 60))
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID g JOIN (SELECT primary_di FROM r ORDER BY n DESC LIMIT 8) t ON t.primary_di = g.primary_di
GROUP BY 1,2 ORDER BY 1, 4 DESC
