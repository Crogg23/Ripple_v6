-- S12 GUDID labelers: top 15 by distinct barcodes, with name spellings, share no longer sold, kit share, first/last publish
SELECT labeler_duns_number duns, ANY_VALUE(company_name) nm, COUNT(DISTINCT company_name) spellings,
       COUNT(DISTINCT primary_di) dis, ROUND(COUNT(DISTINCT primary_di)/5061910*100,2) pct_all,
       ROUND(AVG(IFF(commercial_distribution_status='Not in Commercial Distribution',1,0))*100,1) pct_not_sold,
       ROUND(AVG(IFF(is_kit,1,0))*100,1) pct_kit, COUNT(DISTINCT primary_product_code) codes,
       MIN(publish_date) p0, MAX(publish_date) p1,
       MODE(primary_product_code) top_code
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID
GROUP BY 1 ORDER BY dis DESC LIMIT 15
