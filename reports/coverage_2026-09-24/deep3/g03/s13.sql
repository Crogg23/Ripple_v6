-- S13 GUDID time: barcodes first published per year and share now not sold, plus the duplicate-row split
SELECT YEAR(publish_date) yr, COUNT(*) rows_, COUNT(DISTINCT primary_di) dis,
       ROUND(AVG(IFF(commercial_distribution_status='Not in Commercial Distribution',1,0))*100,1) pct_not_sold,
       COUNT(DISTINCT labeler_duns_number) labelers
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID GROUP BY 1 ORDER BY 1
