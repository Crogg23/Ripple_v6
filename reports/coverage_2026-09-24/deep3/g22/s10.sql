-- S10 OWID military spending: shape, units, zeros, repeated values, series that stop
WITH t AS (SELECT entity, NULLIF(TRIM(code),'') code, year, military_expenditure raw, TRY_TO_DOUBLE(military_expenditure) v, world_region_according_to_owid reg
           FROM LIBRARY_MARTS.POLITICS.POLITICS__INTL_OWID_MILSPEND),
e AS (SELECT entity, code, MIN(year) y0, MAX(year) y1, COUNT(*) n, COUNT_IF(v = 0) zeros, MAX_BY(v, year) last_v FROM t GROUP BY 1,2),
rep AS (SELECT entity, v, COUNT(*) n, MIN(year) y0, MAX(year) y1 FROM t WHERE v > 0 GROUP BY 1,2 HAVING COUNT(*) >= 3)
SELECT OBJECT_CONSTRUCT(
 'rows', (SELECT COUNT(*) FROM t), 'entities', (SELECT COUNT(DISTINCT entity) FROM t), 'with_code', (SELECT COUNT(DISTINCT entity) FROM t WHERE code IS NOT NULL),
 'dup_entity_year', (SELECT COUNT(*) - COUNT(DISTINCT entity, year) FROM t),
 'year_range', (SELECT MIN(year) || '-' || MAX(year) FROM t), 'rows_by_decade', (SELECT OBJECT_AGG(dec::VARCHAR, n) FROM (SELECT FLOOR(year/10)*10 dec, COUNT(*) n FROM t GROUP BY 1)),
 'non_numeric', (SELECT COUNT(*) FROM t WHERE v IS NULL), 'non_numeric_sample', (SELECT ARRAY_AGG(DISTINCT raw) WITHIN GROUP (ORDER BY raw) FROM (SELECT raw FROM t WHERE v IS NULL LIMIT 20)),
 'no_code_entities', (SELECT ARRAY_AGG(entity || ' ' || y0 || '-' || y1) FROM e WHERE code IS NULL),
 'zeros_total', (SELECT COUNT_IF(v = 0) FROM t), 'zeros_top', (SELECT ARRAY_AGG(entity || ':' || zeros || ' (' || y0 || '-' || y1 || ')') FROM (SELECT * FROM e WHERE zeros > 0 ORDER BY zeros DESC LIMIT 12)),
 'repeated_values', (SELECT COUNT(*) FROM rep), 'repeated_rows', (SELECT SUM(n) FROM rep),
 'repeated_top', (SELECT ARRAY_AGG(entity || ' ' || v || ' x' || n || ' ' || y0 || '-' || y1) FROM (SELECT * FROM rep ORDER BY n DESC LIMIT 12)),
 'series_stop_before_2020', (SELECT ARRAY_AGG(entity || ' ' || y1) FROM (SELECT * FROM e WHERE code IS NOT NULL AND y1 < 2020 ORDER BY y1 DESC LIMIT 25)),
 'n_stop_before_2020', (SELECT COUNT(*) FROM e WHERE code IS NOT NULL AND y1 < 2020),
 'entities_in_max_year', (SELECT COUNT(*) FROM t WHERE year = (SELECT MAX(year) FROM t)),
 'usa', (SELECT ARRAY_AGG(year || ':' || raw) WITHIN GROUP (ORDER BY year DESC) FROM (SELECT * FROM t WHERE code = 'USA' ORDER BY year DESC LIMIT 6)),
 'world', (SELECT ARRAY_AGG(year || ':' || raw) WITHIN GROUP (ORDER BY year DESC) FROM (SELECT * FROM t WHERE entity = 'World' ORDER BY year DESC LIMIT 4)),
 'usa_1950_1970', (SELECT ARRAY_AGG(year || ':' || raw) WITHIN GROUP (ORDER BY year) FROM t WHERE code = 'USA' AND year IN (1949,1950,1960,1968,1980,2000)),
 'regions', (SELECT OBJECT_AGG(COALESCE(reg,'(null)'), n) FROM (SELECT reg, COUNT(DISTINCT entity) n FROM t GROUP BY 1))
) o
