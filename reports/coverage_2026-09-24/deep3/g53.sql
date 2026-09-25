-- deep3/g53: deep pass 3, 2026-09-24. Python door (connect/db.py), read-only SELECT/WITH only, QUERY_TAG 'deep3-2026-09-24'.
-- Every connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'. Those two are not counted.
-- Tables: JUSTICE__INTL_AUSTLII, JUSTICE__INTL_EU_SOCTA_EUROPOL, JUSTICE__INTL_EURLEX_CELLAR, JUSTICE__FED_FTC_DATASETS, JUSTICE__FED_FBI_NICS_CHECKS.
-- 7 statements (S01-S07), all below, in run order. S01-S05 pull every row (all five tables are small);
-- the duplicate, step-change, peer and before/after math ran locally in pandas (scratch in g53/).
-- Outputs: g53/out_Sxx.txt and g53/out_Sxx.csv. Runner: g53/run.py.
-- Not warehouse statements, listed for the record: two web checks (ftc.gov BetterHelp case page; Vermont 13 V.S.A. 4019 and Act 94 of 2018).

-- S01 AustLII: every row (glance says 1)
SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_AUSTLII;

-- S02 Europol SOCTA: every row (glance says 26)
SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_EU_SOCTA_EUROPOL;

-- S03 EUR-Lex Cellar: every row (glance says 13)
SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_EURLEX_CELLAR;

-- S04 FTC datasets: every row (glance says 1,004), extract for local time and duplicate checks
SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FTC_DATASETS;

-- S05 FBI NICS: every row (glance says 16,445), extract for local duplicate, time and peer checks
SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FBI_NICS_CHECKS;

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
