-- S12 CPI: shape, then change from first comparable year to latest inside each OWID region; who hit a series low in the latest year
WITH t AS (SELECT entity, NULLIF(TRIM(code),'') code, year, corruption_perceptions_index s, NULLIF(world_region_according_to_owid,'') reg
           FROM LIBRARY_MARTS.POLITICS.POLITICS__XC_OWID_CPI),
shape AS (SELECT OBJECT_CONSTRUCT('rows', COUNT(*), 'entities', COUNT(DISTINCT entity), 'no_code', COUNT(DISTINCT IFF(code IS NULL, entity, NULL)),
            'years', MIN(year) || '-' || MAX(year), 'dup', COUNT(*) - COUNT(DISTINCT entity, year), 'null_score', COUNT_IF(s IS NULL),
            'min', MIN(s), 'max', MAX(s), 'non_integer', COUNT_IF(s <> ROUND(s)),
            'per_year', (SELECT OBJECT_AGG(year::VARCHAR, n) FROM (SELECT year, COUNT(*) n FROM t GROUP BY 1)),
            'no_code_list', (SELECT ARRAY_AGG(DISTINCT entity) FROM t WHERE code IS NULL),
            'usa', (SELECT ARRAY_AGG(year || ':' || s) WITHIN GROUP (ORDER BY year) FROM t WHERE code = 'USA')) o FROM t),
lastyr AS (SELECT MAX(year) y FROM t),
p AS (SELECT entity, reg, MAX(IFF(year = 2012, s, NULL)) s12, MAX(IFF(year = (SELECT y FROM lastyr), s, NULL)) sl,
             MIN(IFF(year < (SELECT y FROM lastyr), s, NULL)) prior_min, MAX(s) best, MAX_BY(year, s) best_yr
      FROM t WHERE code IS NOT NULL AND year >= 2012 GROUP BY 1,2),
g AS (SELECT *, sl - s12 d, MEDIAN(sl - s12) OVER (PARTITION BY reg) reg_med, COUNT(sl - s12) OVER (PARTITION BY reg) reg_n,
             RANK() OVER (PARTITION BY reg ORDER BY sl - s12) rk_drop FROM p WHERE s12 IS NOT NULL AND sl IS NOT NULL)
SELECT 'shape' kind, NULL reg, NULL entity, NULL a, NULL b, NULL c, NULL d, NULL e, (SELECT o FROM shape)::VARCHAR note FROM dual
UNION ALL SELECT 'drop_in_region', reg, entity, s12, sl, d, reg_med, reg_n, 'best ' || best || ' in ' || best_yr FROM g WHERE rk_drop <= 4
UNION ALL SELECT 'new_low_latest', reg, entity, s12, sl, d, prior_min, NULL, 'best ' || best || ' in ' || best_yr FROM g WHERE sl < prior_min AND s12 >= 60
UNION ALL SELECT 'counts', NULL, NULL, COUNT(*), COUNT_IF(sl < prior_min), COUNT_IF(d < 0), MEDIAN(d), COUNT_IF(d <= -10), NULL FROM g
ORDER BY 1, 2, 6
