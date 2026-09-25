-- S11 Military spending 2021 -> 2025 (constant dollars) by country, ranked inside its OWID region; region medians; 2024 -> 2025 fallers
WITH t AS (SELECT entity, NULLIF(TRIM(code),'') code, year, TRY_TO_DOUBLE(military_expenditure) v, NULLIF(world_region_according_to_owid,'') reg
           FROM LIBRARY_MARTS.POLITICS.POLITICS__INTL_OWID_MILSPEND),
p AS (SELECT entity, reg, MAX(IFF(year = 2021, v, NULL)) v21, MAX(IFF(year = 2024, v, NULL)) v24, MAX(IFF(year = 2025, v, NULL)) v25
      FROM t WHERE code IS NOT NULL AND code NOT LIKE 'OWID%' GROUP BY 1,2),
g AS (SELECT *, v25 / NULLIF(v21, 0) - 1 g2125, v25 / NULLIF(v24, 0) - 1 g2425,
             MEDIAN(v25 / NULLIF(v21, 0) - 1) OVER (PARTITION BY reg) reg_med, COUNT(v25 / NULLIF(v21, 0)) OVER (PARTITION BY reg) reg_n,
             RANK() OVER (PARTITION BY reg ORDER BY v25 / NULLIF(v21, 0) DESC NULLS LAST) rk,
             v25 / SUM(v25) OVER () share25
      FROM p WHERE v21 > 0 AND v25 > 0)
SELECT 'top_in_region' kind, reg, entity, rk, ROUND(v21/1e9, 2) b21, ROUND(v24/1e9, 2) b24, ROUND(v25/1e9, 2) b25, ROUND(g2125*100, 1) pct_21_25, ROUND(reg_med*100, 1) reg_med_pct, reg_n, ROUND(g2425*100,1) pct_24_25
FROM g WHERE rk <= 5
UNION ALL
SELECT 'biggest_2425_fall', reg, entity, NULL, ROUND(v21/1e9,2), ROUND(v24/1e9,2), ROUND(v25/1e9,2), ROUND(g2125*100,1), ROUND(reg_med*100,1), reg_n, ROUND(g2425*100,1)
FROM g WHERE v24 > 5e9 QUALIFY ROW_NUMBER() OVER (ORDER BY g2425) <= 8
UNION ALL
SELECT 'top_share_2025', reg, entity, ROW_NUMBER() OVER (ORDER BY v25 DESC), NULL, ROUND(v24/1e9,2), ROUND(v25/1e9,2), ROUND(g2125*100,1), ROUND(share25*100,1), NULL, ROUND(g2425*100,1)
FROM g QUALIFY ROW_NUMBER() OVER (ORDER BY v25 DESC) <= 8
UNION ALL
SELECT 'counts', 'all', NULL, COUNT(*), NULL, NULL, NULL, ROUND(MEDIAN(g2125)*100,1), NULL, COUNT_IF(g2425 < 0), ROUND(MEDIAN(g2425)*100,1) FROM g
ORDER BY 1, 2, 4
