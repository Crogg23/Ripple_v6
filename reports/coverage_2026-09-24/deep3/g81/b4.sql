-- S15 Slave voyages: people landed by main landing region and period, intra-American (second voyage) vs transatlantic (first landing)
WITH i AS (
  SELECT TRY_TO_NUMBER(MJSELIMP) reg, CASE WHEN TRY_TO_NUMBER(YEARAM) < 1700 THEN 'a <1700' WHEN TRY_TO_NUMBER(YEARAM) < 1760 THEN 'b 1700-59'
         WHEN TRY_TO_NUMBER(YEARAM) < 1808 THEN 'c 1760-1807' ELSE 'd 1808+' END per,
         COUNT(*) v, SUM(TRY_TO_NUMBER(SLAMIMP)) landed, MODE(LEFT(SOURCEA, 30)) src
  FROM LIBRARY_MARTS.HISTORICAL_RECORDS.HISTORICAL_RECORDS__FED_SLAVEVOYAGES_INTRAAMERICAN GROUP BY 1, 2),
t AS (
  SELECT TRY_TO_NUMBER(MJSELIMP) reg, CASE WHEN TRY_TO_NUMBER(YEARAM) < 1700 THEN 'a <1700' WHEN TRY_TO_NUMBER(YEARAM) < 1760 THEN 'b 1700-59'
         WHEN TRY_TO_NUMBER(YEARAM) < 1808 THEN 'c 1760-1807' ELSE 'd 1808+' END per,
         COUNT(*) v, SUM(TRY_TO_NUMBER(SLAMIMP)) landed, MODE(LEFT(SOURCEA, 30)) src
  FROM LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC GROUP BY 1, 2)
SELECT COALESCE(i.reg, t.reg) reg, COALESCE(i.per, t.per) per, i.v intra_v, i.landed intra_landed, t.v ta_v, t.landed ta_landed,
       ROUND(i.landed / NULLIF(COALESCE(i.landed,0) + COALESCE(t.landed,0), 0), 3) intra_share, i.src intra_src, t.src ta_src
FROM i FULL OUTER JOIN t ON i.reg = t.reg AND i.per = t.per
ORDER BY 1, 2;

-- S16 Slave voyages: time, 1783-1815, voyages leaving the Carolinas region (21300) for Cuba (31300) and elsewhere, vs transatlantic landings in 21300
WITH o AS (
  SELECT TRY_TO_NUMBER(YEARAM) y, COUNT(*) out_v, SUM(TRY_TO_NUMBER(SLAMIMP)) out_landed,
         COUNT_IF(TRY_TO_NUMBER(MJSELIMP) = 31300) cuba_v, SUM(IFF(TRY_TO_NUMBER(MJSELIMP) = 31300, TRY_TO_NUMBER(SLAMIMP), 0)) cuba_landed,
         MODE(MJSLPTIMP) top_land_port, MODE(LEFT(SOURCEA, 30)) src
  FROM LIBRARY_MARTS.HISTORICAL_RECORDS.HISTORICAL_RECORDS__FED_SLAVEVOYAGES_INTRAAMERICAN
  WHERE TRY_TO_NUMBER(MAJBYIMP) = 21300 GROUP BY 1),
a AS (
  SELECT TRY_TO_NUMBER(YEARAM) y, COUNT(*) ta_v, SUM(TRY_TO_NUMBER(SLAMIMP)) ta_landed, MODE(MJSLPTIMP) ta_top_port, MODE(LEFT(SOURCEA, 30)) ta_src
  FROM LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC
  WHERE TRY_TO_NUMBER(MJSELIMP) = 21300 GROUP BY 1)
SELECT COALESCE(o.y, a.y) y, a.ta_v, a.ta_landed, a.ta_top_port, a.ta_src, o.out_v, o.out_landed, o.cuba_v, o.cuba_landed, o.top_land_port, o.src
FROM o FULL OUTER JOIN a ON o.y = a.y
WHERE COALESCE(o.y, a.y) BETWEEN 1783 AND 1815 ORDER BY 1;

-- S17 Slave voyages: concentration, owners and captains on the 21300 -> 31300 route, 1800-1810 (data match, not verified)
SELECT COALESCE(NULLIF(TRIM(OWNERA),''), '(no owner)') owner, COUNT(*) voyages, SUM(TRY_TO_NUMBER(SLAMIMP)) landed,
       COUNT(DISTINCT SHIPNAME) ships, MIN(TRY_TO_NUMBER(YEARAM)) y0, MAX(TRY_TO_NUMBER(YEARAM)) y1, MODE(CAPTAINA) top_captain,
       SUM(COUNT(*)) OVER () all_v, SUM(SUM(TRY_TO_NUMBER(SLAMIMP))) OVER () all_landed
FROM LIBRARY_MARTS.HISTORICAL_RECORDS.HISTORICAL_RECORDS__FED_SLAVEVOYAGES_INTRAAMERICAN
WHERE TRY_TO_NUMBER(MAJBYIMP) = 21300 AND TRY_TO_NUMBER(MJSELIMP) = 31300 AND TRY_TO_NUMBER(YEARAM) BETWEEN 1800 AND 1810
GROUP BY 1 ORDER BY landed DESC NULLS LAST LIMIT 20;

-- S18 Slave voyages trap check: how much of the people count is the editors' estimate, not a recorded number
SELECT IFF(TRY_TO_NUMBER(TSLAVESD) IS NOT NULL, 'rec_embark', 'no_rec_embark') re, IFF(TRY_TO_NUMBER(SLAARRIV) IS NOT NULL, 'rec_land', 'no_rec_land') rl,
       COUNT(*) v, SUM(TRY_TO_NUMBER(SLAXIMP)) est_embark, SUM(TRY_TO_NUMBER(SLAMIMP)) est_landed,
       MODE(ROUND(TRY_TO_NUMBER(SLAMIMP, 12, 2) / NULLIF(TRY_TO_NUMBER(SLAXIMP, 12, 2), 0), 3)) mode_ratio,
       MEDIAN(TRY_TO_NUMBER(SLAMIMP, 12, 2) / NULLIF(TRY_TO_NUMBER(SLAXIMP, 12, 2), 0)) med_ratio,
       COUNT_IF(TRY_TO_NUMBER(SLAMIMP) = TRY_TO_NUMBER(SLAXIMP)) same, COUNT_IF(TRY_TO_NUMBER(SLAXIMP) = 0) zero_embark,
       MEDIAN(TRY_TO_NUMBER(SLAXIMP)) med_embark, MAX(TRY_TO_NUMBER(SLAXIMP)) max_embark, COUNT_IF(TRY_TO_NUMBER(VYMRTRAT, 12, 4) IS NOT NULL) mort_n,
       MEDIAN(TRY_TO_NUMBER(VYMRTRAT, 12, 4)) med_mort
FROM LIBRARY_MARTS.HISTORICAL_RECORDS.HISTORICAL_RECORDS__FED_SLAVEVOYAGES_INTRAAMERICAN
GROUP BY 1, 2 ORDER BY v DESC;

-- S19 Wayback: every content change over 2,000 bytes on a 200 page (the only big edits), page and date
WITH x AS (
  SELECT URLKEY, CAPTURED_AT, HTTP_STATUS, PREV_HTTP_STATUS, CONTENT_BYTES, LAG(CONTENT_BYTES) OVER (PARTITION BY URLKEY ORDER BY CAPTURED_AT) pb
  FROM LIBRARY_MARTS.EPSTEIN.FCT_WAYBACK_PAGE_CHANGES)
SELECT TO_DATE(CAPTURED_AT) d, REGEXP_REPLACE(URLKEY, '^gov,justice[)]/epstein/doj-disclosures', '') path, pb bytes_before, CONTENT_BYTES bytes_after, CONTENT_BYTES - pb delta
FROM x WHERE HTTP_STATUS = 200 AND PREV_HTTP_STATUS = 200 AND ABS(CONTENT_BYTES - pb) > 2000
ORDER BY d, path;

-- S20 Wayback: listing pages by data set: page variants, junk variants, highest page number, first/last capture
WITH p AS (
  SELECT URLKEY, REGEXP_SUBSTR(URLKEY, 'doj-disclosures/([a-z0-9-]+)', 1, 1, 'e', 1) sect,
         TRY_TO_NUMBER(REGEXP_SUBSTR(URLKEY, '[?&]page=([0-9]+)$', 1, 1, 'e', 1)) pg,
         IFF(REGEXP_LIKE(URLKEY, '.*(utm_|fbclid|%0a|%e|\\u00|&data=).*'), 1, 0) junk,
         MIN(CAPTURED_AT) t0, MAX(CAPTURED_AT) t1, COUNT(*) n
  FROM LIBRARY_MARTS.EPSTEIN.FCT_WAYBACK_PAGE_CHANGES GROUP BY 1)
SELECT COALESCE(sect, '(root)') sect, COUNT(*) urlkeys, COUNT_IF(junk = 1) junk_variants, COUNT(DISTINCT pg) page_nums, MAX(pg) max_page,
       SUM(n) change_rows, MIN(t0) first_seen, MAX(t1) last_seen, MEDIAN(n) med_rows_per_page
FROM p GROUP BY 1 ORDER BY urlkeys DESC LIMIT 40;

-- S21 Revolving door: what a row is, read the words. The 6 jobs with most industries and 4 with one
(SELECT 'most' grp, POSITION_NAME, POSITION_DEPARTMENT, POSITION_TYPE, LEFT(POSITION_DESCRIPTION, 160) descr, INDUSTRY_SECTOR, SECTOR1_INTEREST, SECTOR2, SECTOR16, _SOURCE_ID
 FROM LIBRARY_MARTS.GOVERNANCE.GOVERNANCE__FED_REVOLVINGDOOR_PROJECT WHERE LOWER(SECTOR16) <> 'nan' LIMIT 6)
UNION ALL
(SELECT 'one', POSITION_NAME, POSITION_DEPARTMENT, POSITION_TYPE, LEFT(POSITION_DESCRIPTION, 160), INDUSTRY_SECTOR, SECTOR1_INTEREST, SECTOR2, SECTOR16, _SOURCE_ID
 FROM LIBRARY_MARTS.GOVERNANCE.GOVERNANCE__FED_REVOLVINGDOOR_PROJECT WHERE LOWER(SECTOR2) = 'nan' LIMIT 4);
