WITH c AS (
  SELECT UPPER(REPLACE(POST_CODE,' ','')) pc, REGEXP_SUBSTR(UPPER(TRIM(POST_CODE)), '^[A-Z]{1,2}[0-9][0-9A-Z]?') od,
         IFF(INCORPORATION_DATE <= '2025-11-16', 'pre', 'post') w
  FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE
  WHERE INCORPORATION_DATE BETWEEN '2025-10-06' AND '2025-11-16' OR INCORPORATION_DATE BETWEEN '2025-11-18' AND '2025-12-22'),
p AS (SELECT pc, COUNT_IF(w='pre')/6.0 pre_wk, COUNT_IF(w='post')/5.0 post_wk FROM c GROUP BY 1),
o AS (SELECT od, COUNT_IF(w='pre')/6.0 pre_wk, COUNT_IF(w='post')/5.0 post_wk FROM c WHERE od IS NOT NULL GROUP BY 1),
tot AS (SELECT SUM(pre_wk) tpre, SUM(post_wk) tpost FROM p),
rk AS (SELECT p.*, pre_wk - post_wk drop_wk, ROW_NUMBER() OVER (ORDER BY pre_wk - post_wk DESC) r, ROW_NUMBER() OVER (ORDER BY pre_wk DESC) rsize FROM p)
SELECT 'total' k, NULL v, tpre a, tpost b, tpost/tpre - 1 c FROM tot
UNION ALL SELECT 'top10_drop_share', 'share of national weekly drop carried by the 10 postcodes that fell most', SUM(drop_wk), (SELECT tpre - tpost FROM tot), SUM(drop_wk)/(SELECT tpre - tpost FROM tot) FROM rk WHERE r <= 10
UNION ALL SELECT 'excl_top50_size', 'all postcodes except the 50 biggest pre-window: pre, post, change', SUM(pre_wk), SUM(post_wk), SUM(post_wk)/SUM(pre_wk) - 1 FROM rk WHERE rsize > 50
UNION ALL SELECT 'outward_median', 'outward codes with 30+ a week pre: count, median post/pre, share that fell', COUNT(*), MEDIAN(post_wk/pre_wk), COUNT_IF(post_wk < pre_wk)/COUNT(*) FROM o WHERE pre_wk >= 30
UNION ALL SELECT 'outward_median_small', 'outward codes with 5-30 a week pre: count, median post/pre, share that fell', COUNT(*), MEDIAN(post_wk/pre_wk), COUNT_IF(post_wk < pre_wk)/COUNT(*) FROM o WHERE pre_wk >= 5 AND pre_wk < 30
UNION ALL SELECT 'top_droppers', pc, pre_wk, post_wk, drop_wk FROM rk WHERE r <= 10
ORDER BY 1, 5 DESC
