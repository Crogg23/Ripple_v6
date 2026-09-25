-- S19 Military spending breaks: year-on-year swings over 40% for countries spending over $5B, 2010-2025, plus Mexico's full recent series
WITH t AS (SELECT entity, NULLIF(TRIM(code),'') code, year, TRY_TO_DOUBLE(military_expenditure) v FROM LIBRARY_MARTS.POLITICS.POLITICS__INTL_OWID_MILSPEND),
x AS (SELECT entity, year, v, LAG(v) OVER (PARTITION BY entity ORDER BY year) pv, LEAD(v) OVER (PARTITION BY entity ORDER BY year) nv FROM t WHERE code IS NOT NULL)
SELECT 'swing' k, entity, year, ROUND(pv/1e9, 2) prev_b, ROUND(v/1e9, 2) b, ROUND(nv/1e9, 2) next_b, ROUND(100*(v/pv - 1), 1) pct_yoy,
       IFF(nv IS NOT NULL AND ABS(nv/pv - 1) < 0.15, 'spike-and-back', '') shape
FROM x WHERE year >= 2010 AND GREATEST(v, pv) > 5e9 AND pv > 0 AND ABS(v/pv - 1) > 0.40
UNION ALL
SELECT 'mexico', entity, year, NULL, ROUND(v/1e9, 2), NULL, ROUND(100*(v/pv - 1), 1), NULL FROM x WHERE entity = 'Mexico' AND year >= 2015
ORDER BY 1, 2, 3
