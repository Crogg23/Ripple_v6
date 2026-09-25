-- S06 Landing vs mart: row counts and load dates for every table behind my five (is there a fresher NICS load, a fuller FTC or AustLII pull?)
SELECT 'raw' db, table_schema, table_name, row_count, created, last_altered
FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
WHERE table_name ILIKE ANY ('%NICS%', '%FTC%', '%AUSTLII%', '%EURLEX%', '%CELLAR%', '%SOCTA%', '%EUROPOL%')
UNION ALL
SELECT 'marts', table_schema, table_name, row_count, created, last_altered
FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
WHERE table_name ILIKE ANY ('%NICS%', '%FTC%', '%AUSTLII%', '%EURLEX%', '%CELLAR%', '%SOCTA%', '%EUROPOL%')
ORDER BY 3, 1;

-- S07 Denominator: 2020 population by state name, for per-resident private-sale checks
SELECT STATE_NAME, SUM(POPULATION_2020) pop_2020, COUNT(*) counties
FROM LIBRARY_MARTS.CORE.DIM_COUNTY
GROUP BY 1 ORDER BY 1;
