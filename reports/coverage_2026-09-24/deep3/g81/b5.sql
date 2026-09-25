-- S22 Wayback (S20 rerun, regex fixed): listing pages by data set, junk URL variants, highest page number, first/last capture
WITH p AS (
  SELECT URLKEY, REGEXP_SUBSTR(URLKEY, 'doj-disclosures/([a-z0-9-]+)', 1, 1, 'e', 1) sect,
         TRY_TO_NUMBER(REGEXP_SUBSTR(URLKEY, '[?&]page=([0-9]+)$', 1, 1, 'e', 1)) pg,
         IFF(REGEXP_LIKE(URLKEY, '.*(utm_|fbclid|%0a|%e|u003c|&data=|[?&]ref=|gclid).*'), 1, 0) junk,
         MIN(CAPTURED_AT) t0, MAX(CAPTURED_AT) t1, COUNT(*) n
  FROM LIBRARY_MARTS.EPSTEIN.FCT_WAYBACK_PAGE_CHANGES GROUP BY 1)
SELECT COALESCE(sect, '(root)') sect, COUNT(*) urlkeys, COUNT_IF(junk = 1) junk_variants, COUNT(DISTINCT pg) page_nums, MAX(pg) max_page,
       SUM(n) change_rows, MIN(t0) first_seen, MAX(t1) last_seen, MEDIAN(n) med_rows_per_page
FROM p GROUP BY 1 ORDER BY urlkeys DESC LIMIT 40;

-- S23 Slave voyages peer: second-voyage arrivals in Cuba (31300), 1800-1810, by main buying region
SELECT TRY_TO_NUMBER(MAJBYIMP) buy_region, COUNT(*) voyages, SUM(TRY_TO_NUMBER(SLAMIMP)) landed,
       SUM(IFF(TRY_TO_NUMBER(YEARAM) BETWEEN 1804 AND 1807, TRY_TO_NUMBER(SLAMIMP), 0)) landed_1804_07,
       SUM(IFF(TRY_TO_NUMBER(YEARAM) BETWEEN 1800 AND 1803, TRY_TO_NUMBER(SLAMIMP), 0)) landed_1800_03,
       SUM(IFF(TRY_TO_NUMBER(YEARAM) BETWEEN 1808 AND 1810, TRY_TO_NUMBER(SLAMIMP), 0)) landed_1808_10,
       COUNT_IF(TRY_TO_NUMBER(SLAARRIV) IS NOT NULL) recorded_landed_rows, MODE(LEFT(SOURCEA, 25)) src
FROM LIBRARY_MARTS.HISTORICAL_RECORDS.HISTORICAL_RECORDS__FED_SLAVEVOYAGES_INTRAAMERICAN
WHERE TRY_TO_NUMBER(MJSELIMP) = 31300 AND TRY_TO_NUMBER(YEARAM) BETWEEN 1800 AND 1810
GROUP BY 1 ORDER BY landed DESC NULLS LAST;

-- S24 Slave voyages peer: second-voyage arrivals in the Gulf coast region (21600), by buying region and period
SELECT TRY_TO_NUMBER(MAJBYIMP) buy_region, CASE WHEN TRY_TO_NUMBER(YEARAM) < 1760 THEN 'a <1760' WHEN TRY_TO_NUMBER(YEARAM) < 1790 THEN 'b 1760-89'
         WHEN TRY_TO_NUMBER(YEARAM) < 1808 THEN 'c 1790-1807' ELSE 'd 1808+' END per,
       COUNT(*) voyages, SUM(TRY_TO_NUMBER(SLAMIMP)) landed, COUNT_IF(TRY_TO_NUMBER(SLAARRIV) IS NOT NULL) recorded_landed_rows,
       MIN(TRY_TO_NUMBER(YEARAM)) y0, MAX(TRY_TO_NUMBER(YEARAM)) y1, MODE(MJSLPTIMP) top_land_port, MODE(LEFT(SOURCEA, 25)) src
FROM LIBRARY_MARTS.HISTORICAL_RECORDS.HISTORICAL_RECORDS__FED_SLAVEVOYAGES_INTRAAMERICAN
WHERE TRY_TO_NUMBER(MJSELIMP) = 21600
GROUP BY 1, 2 ORDER BY 2, landed DESC NULLS LAST;
