-- skeptic-g7, round 2, 2026-09-24. Python door (connect/db.py), read-only, query tag 'skeptic-r2-2026-09-24', 300s timeout.
-- Every connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300 and ALTER SESSION SET QUERY_TAG = 'skeptic-r2-2026-09-24'.
-- Statements: PHMSA 8 (2 failed at compile, fixed and rerun), NOAA 7 (1 failed at compile), VA 7. All under the 12-per-lead cap.
-- P3/P4 first ran with OPERATOR_ID and a string IYEAR filter; compile error; rerun as below with PHMSA_OPERATOR_ID.
-- N6 first ran with an ESCAPE clause; compile error; rerun as N6b.
-- V2 first tripped the local one-statement guard (a ';' inside a string literal) before reaching the warehouse; literal changed.

---------------- shared metadata ----------------
-- @P1 PHMSA columns
SELECT column_name, data_type FROM LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS WHERE table_schema='ENVIRONMENT' AND table_name='ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS' ORDER BY ordinal_position;
-- @V1 VA columns
SELECT column_name, data_type FROM LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS WHERE table_schema='HEALTH' AND table_name='HEALTH__FED_VA_SUICIDE_STATE' ORDER BY ordinal_position;

---------------- LEAD 1: PHMSA ----------------
-- @P2 PHMSA landing columns that carry cost, unit, system type, narrative
SELECT LISTAGG(column_name, ', ') WITHIN GROUP (ORDER BY ordinal_position) cols, COUNT(*) n FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS WHERE table_schema='LANDING' AND table_name='FED_PHMSA_FLAGGED_INCIDENTS' AND (column_name ILIKE '%COST%' OR column_name ILIKE '%GAS%' OR column_name ILIKE '%NARRATIVE%' OR column_name ILIKE '%SHORE%' OR column_name ILIKE '%SYSTEM%' OR column_name ILIKE '%TYPE%' OR column_name ILIKE '%RELEASE%' OR column_name ILIKE '%SIGNIFICANT%' OR column_name ILIKE '%SERIOUS%' OR column_name ILIKE '%FLAG%' OR column_name ILIKE '%CAUSE%' OR column_name ILIKE '%PIPE_FAC%' OR column_name ILIKE '%DESC%');

-- @P3 Sea Robin 2024+ from landing: types, cost-implied volume, system part, cause
SELECT REPORT_NUMBER, REPORT_TYPE, SUPPLEMENTAL_NUMBER, LOCAL_DATETIME, REPORT_RECEIVED_DATE, UNINTENTIONAL_RELEASE uv, INTENTIONAL_RELEASE iv,
       EST_COST_UNINTENTIONAL_RELEASE cost_uv, GAS_COST_IN_MCF price, ROUND(TRY_TO_DOUBLE(EST_COST_UNINTENTIONAL_RELEASE)/NULLIF(TRY_TO_DOUBLE(GAS_COST_IN_MCF),0)) implied_mcf,
       ON_OFF_SHORE, PIPE_FACILITY_TYPE, SYSTEM_PART_INVOLVED, CAUSE, CAUSE_DETAILS, RELEASE_TYPE, LEAK_TYPE, GAS_FLOW_IN_PIPE_IN_MCF, LOCATION_LATITUDE, LOCATION_LONGITUDE
FROM LIBRARY_RAW.LANDING.FED_PHMSA_FLAGGED_INCIDENTS
WHERE TRIM(PHMSA_OPERATOR_ID) = '18152' AND TRY_TO_NUMBER(IYEAR) >= 2024
ORDER BY LOCAL_DATETIME;
-- @P4 Sea Robin 2025 narratives
SELECT REPORT_NUMBER, LOCAL_DATETIME, LEFT(NARRATIVE, 1500) narr
FROM LIBRARY_RAW.LANDING.FED_PHMSA_FLAGGED_INCIDENTS
WHERE TRIM(PHMSA_OPERATOR_ID) = '18152' AND TRY_TO_NUMBER(IYEAR) = 2025
ORDER BY LOCAL_DATETIME;

-- @P5 PHMSA per year: total, top report, total after collapsing same-operator same-volume copies, offshore share, cost-implied unit check
WITH t AS (
  SELECT TRY_TO_NUMBER(IYEAR) y, TRIM(PHMSA_OPERATOR_ID) op, TRIM(REPORT_NUMBER) rn, TRY_TO_DOUBLE(UNINTENTIONAL_RELEASE) uv,
         TRY_TO_DOUBLE(EST_COST_UNINTENTIONAL_RELEASE) c, TRY_TO_DOUBLE(GAS_COST_IN_MCF) p, ON_OFF_SHORE oo, PIPE_FACILITY_TYPE pft, TRIM(REPORT_TYPE) rt
  FROM LIBRARY_RAW.LANDING.FED_PHMSA_FLAGGED_INCIDENTS
), d AS (SELECT y, op, uv, COUNT(*) k FROM t WHERE uv > 0 GROUP BY 1,2,3)
SELECT t.y, COUNT(*) n, COUNT(DISTINCT rn) rns, ROUND(SUM(uv)) total, ROUND(MAX(uv)) top1,
       ROUND(SUM(uv) - MAX(uv)) total_minus_top1,
       (SELECT ROUND(SUM(uv)) FROM d WHERE d.y = t.y) total_copies_collapsed,
       ROUND(SUM(IFF(oo = 'OFFSHORE', uv, 0))) offshore,
       ROUND(SUM(IFF(op = '18152', uv, 0))) sea_robin,
       ROUND(MEDIAN(IFF(uv > 100 AND p > 0 AND c > 0, c / (uv * p), NULL)), 3) med_cost_ratio,
       COUNT(IFF(uv > 100 AND p > 0 AND c > 0 AND c / (uv * p) BETWEEN 0.5 AND 2, 1, NULL)) n_ratio_ok,
       COUNT(IFF(uv > 100 AND p > 0 AND c > 0, 1, NULL)) n_ratio_tested,
       COUNT(IFF(rt ILIKE 'ORIGINAL%' AND rt NOT ILIKE '%FINAL%', 1, NULL)) not_final
FROM t GROUP BY t.y ORDER BY t.y;
-- @P6 PHMSA biggest 12 reports all years: facility type, system part, operator, cause
SELECT TRY_TO_NUMBER(IYEAR) y, TRIM(REPORT_NUMBER) rn, NAME, TRY_TO_DOUBLE(UNINTENTIONAL_RELEASE) uv, ON_OFF_SHORE, PIPE_FACILITY_TYPE, SYSTEM_PART_INVOLVED, CAUSE, REPORT_TYPE, GAS_FLOW_IN_PIPE_IN_MCF
FROM LIBRARY_RAW.LANDING.FED_PHMSA_FLAGGED_INCIDENTS
ORDER BY TRY_TO_DOUBLE(UNINTENTIONAL_RELEASE) DESC NULLS LAST LIMIT 12;

---------------- LEAD 2: NOAA ----------------
-- @N1 NOAA mart columns
SELECT LISTAGG(column_name, ', ') WITHIN GROUP (ORDER BY ordinal_position) FROM LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS WHERE table_schema='ENVIRONMENT' AND table_name='ENVIRONMENT__FED_NOAA_STORM_EVENTS';

-- @N2 NOAA heat by year 2010-2025: US, Phoenix office, Arizona, rows, summer rows, event-id dupes
SELECT YEAR,
  SUM(IFF(EVENT_TYPE IN ('Heat','Excessive Heat'), DEATHS_DIRECT, 0)) us_dd,
  SUM(IFF(EVENT_TYPE IN ('Heat','Excessive Heat') AND WFO = 'PSR', DEATHS_DIRECT, 0)) psr_dd,
  SUM(IFF(EVENT_TYPE IN ('Heat','Excessive Heat') AND STATE = 'ARIZONA', DEATHS_DIRECT, 0)) az_dd,
  SUM(IFF(EVENT_TYPE IN ('Heat','Excessive Heat'), DEATHS_INDIRECT, 0)) us_di,
  COUNT(IFF(EVENT_TYPE IN ('Heat','Excessive Heat'), 1, NULL)) us_heat_rows,
  COUNT(IFF(EVENT_TYPE IN ('Heat','Excessive Heat') AND WFO = 'PSR', 1, NULL)) psr_heat_rows,
  COUNT(IFF(EVENT_TYPE IN ('Heat','Excessive Heat') AND WFO <> 'PSR' AND MONTH_NAME IN ('June','July','August','September'), 1, NULL)) nonpsr_summer_heat_rows,
  COUNT(IFF(WFO = 'PSR', 1, NULL)) psr_all_rows,
  COUNT(*) all_rows, COUNT(DISTINCT EVENT_ID) ids,
  COUNT(IFF(EVENT_TYPE IN ('Heat','Excessive Heat') AND WFO = 'PSR' AND DEATHS_DIRECT > 0, 1, NULL)) psr_rows_w_deaths,
  COUNT(DISTINCT IFF(EVENT_TYPE IN ('Heat','Excessive Heat') AND WFO = 'PSR' AND DEATHS_DIRECT > 0, EPISODE_ID, NULL)) psr_episodes_w_deaths
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NOAA_STORM_EVENTS
WHERE YEAR >= 2010
GROUP BY YEAR ORDER BY YEAR;
-- @N3 NOAA 2018-2023 totals and top-row lumping: how many PSR deaths sit on rows with 20+ deaths, and do narratives cite Maricopa
SELECT
  SUM(IFF(EVENT_TYPE IN ('Heat','Excessive Heat'), DEATHS_DIRECT, 0)) us_dd,
  SUM(IFF(EVENT_TYPE IN ('Heat','Excessive Heat') AND WFO = 'PSR', DEATHS_DIRECT, 0)) psr_dd,
  SUM(IFF(EVENT_TYPE IN ('Heat','Excessive Heat') AND WFO = 'PSR' AND DEATHS_DIRECT >= 20, DEATHS_DIRECT, 0)) psr_dd_on_20plus_rows,
  COUNT(IFF(EVENT_TYPE IN ('Heat','Excessive Heat') AND WFO = 'PSR' AND DEATHS_DIRECT >= 20, 1, NULL)) psr_20plus_rows,
  SUM(IFF(EVENT_TYPE IN ('Heat','Excessive Heat') AND WFO = 'PSR' AND (EVENT_NARRATIVE ILIKE '%MARICOPA%' OR EPISODE_NARRATIVE ILIKE '%MARICOPA%'), DEATHS_DIRECT, 0)) psr_dd_maricopa_cited,
  SUM(IFF(EVENT_TYPE IN ('Heat','Excessive Heat') AND WFO = 'PSR' AND CZ_NAME ILIKE '%PHOENIX%', DEATHS_DIRECT, 0)) psr_dd_phoenix_zones,
  COUNT(DISTINCT IFF(EVENT_TYPE IN ('Heat','Excessive Heat') AND WFO = 'PSR' AND DEATHS_DIRECT > 0, CZ_NAME, NULL)) psr_zones_w_deaths,
  SUM(IFF(EVENT_TYPE IN ('Heat','Excessive Heat') AND WFO = 'VEF', DEATHS_DIRECT, 0)) vef_dd,
  SUM(IFF(EVENT_TYPE IN ('Heat','Excessive Heat') AND WFO = 'VEF' AND (EVENT_NARRATIVE ILIKE '%CLARK COUNTY%' OR EPISODE_NARRATIVE ILIKE '%CLARK COUNTY%' OR EVENT_NARRATIVE ILIKE '%CORONER%' OR EPISODE_NARRATIVE ILIKE '%CORONER%'), DEATHS_DIRECT, 0)) vef_dd_coroner_cited
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NOAA_STORM_EVENTS
WHERE YEAR BETWEEN 2018 AND 2023;
-- @N4 NOAA Phoenix office 2024-2025: every heat row, plus any row of any type carrying deaths Jun-Sep
SELECT BEGIN_YEARMONTH, EVENT_TYPE, CZ_NAME, DEATHS_DIRECT, DEATHS_INDIRECT, LEFT(EVENT_NARRATIVE, 250) ev, LEFT(EPISODE_NARRATIVE, 250) ep
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NOAA_STORM_EVENTS
WHERE WFO = 'PSR' AND YEAR >= 2024 AND (EVENT_TYPE ILIKE '%HEAT%' OR ((DEATHS_DIRECT > 0 OR DEATHS_INDIRECT > 0) AND MONTH_NAME IN ('May','June','July','August','September')))
ORDER BY BEGIN_YEARMONTH, DEATHS_DIRECT DESC;

-- @N5 NOAA Phoenix office heat rows and deaths by month 2024-2025, plus all-type rows that month
SELECT BEGIN_YEARMONTH, COUNT(*) psr_rows_all_types,
       COUNT(IFF(EVENT_TYPE ILIKE '%HEAT%', 1, NULL)) psr_heat_rows,
       SUM(IFF(EVENT_TYPE ILIKE '%HEAT%', DEATHS_DIRECT, 0)) psr_heat_dd,
       SUM(DEATHS_DIRECT) psr_all_dd,
       LEFT(LISTAGG(DISTINCT IFF(EVENT_TYPE ILIKE '%HEAT%', LEFT(EVENT_NARRATIVE, 120), NULL), ' ## '), 400) heat_note
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NOAA_STORM_EVENTS
WHERE WFO = 'PSR' AND YEAR >= 2024
GROUP BY 1 ORDER BY 1;
-- @N6 NOAA landing: load stamp and source columns per year 2023-2025 (is 2024 an old file revision?)
SELECT column_name FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS WHERE table_schema='LANDING' AND table_name ILIKE '%NOAA_STORM%' AND column_name ILIKE '\_%' ESCAPE '\';

-- @N6b NOAA landing lineage columns
SELECT table_name, LISTAGG(column_name, ', ') FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS WHERE table_schema='LANDING' AND table_name ILIKE '%NOAA_STORM%' AND LEFT(column_name,1) = '_' GROUP BY 1;

---------------- LEAD 3: VA suicide ----------------
-- @V2 Other state-level suicide or mortality tables to check the general-population line; plus VA general-pop column fill
SELECT 'table' k, table_schema||'.'||table_name v, row_count::string n FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
WHERE (table_name ILIKE '%SUICIDE%' OR table_name ILIKE '%NCHS%' OR table_name ILIKE '%CAUSE%DEATH%' OR table_name ILIKE '%MORTALITY%' OR table_name ILIKE '%LEADING%')
UNION ALL
SELECT 'va_genpop_fill', COUNT(IFF(NULLIF(TRIM(GENERAL_POPULATION_SUICIDES),'') IS NOT NULL,1,NULL))::string||' non-blank gen suicides, '||COUNT(GENERAL_POPULATION_RATE_PER_100K)||' gen rates, rows '||COUNT(*), LISTAGG(DISTINCT LEFT(GENERAL_POPULATION_SUICIDES,10), ',') FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_VA_SUICIDE_STATE;
-- @V3 Empirical null: every state, every window pair (y,y+1) vs (y+3,y+4), z of later deaths vs earlier rate times later veteran pop
WITH v AS (
  SELECT STATE st, YEAR_OF_DEATH y, VETERAN_SUICIDES d, VETERAN_POPULATION_ESTIMATE p
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_VA_SUICIDE_STATE WHERE STATE <> 'U.S. Total' AND VETERAN_SUICIDES IS NOT NULL AND VETERAN_POPULATION_ESTIMATE > 0
), w AS (
  SELECT a.st, a.y y0, a.d + b.d d1, a.p + b.p p1, c.d + e.d d2, c.p + e.p p2
  FROM v a JOIN v b ON b.st = a.st AND b.y = a.y + 1
           JOIN v c ON c.st = a.st AND c.y = a.y + 3
           JOIN v e ON e.st = a.st AND e.y = a.y + 4
), z AS (SELECT *, d1 * p2 / p1 expd, (d2 - d1 * p2 / p1) / SQRT(d1 * p2 / p1) z FROM w WHERE d1 >= 20)
SELECT * FROM (
SELECT 'summary' k, NULL st, NULL y0, COUNT(*) n_pairs, COUNT(IFF(z >= 4.9,1,NULL)) n_z_ge_4_9, COUNT(IFF(z >= 3,1,NULL)) n_z_ge_3, COUNT(IFF(z <= -3,1,NULL)) n_z_le_neg3,
       ROUND(STDDEV(z),2) sd_z, NULL d1, NULL d2
FROM z
UNION ALL
SELECT 'window_2019', NULL, 2019, COUNT(*), COUNT(IFF(z >= 4.9,1,NULL)), COUNT(IFF(z >= 3,1,NULL)), COUNT(IFF(z <= -3,1,NULL)), ROUND(STDDEV(z),2), NULL, NULL FROM z WHERE y0 = 2019
UNION ALL
(SELECT 'top', st, y0, NULL, NULL, NULL, NULL, ROUND(z,2), d1, d2 FROM z ORDER BY z DESC LIMIT 15)
UNION ALL
(SELECT 'top_2019', st, y0, NULL, NULL, NULL, NULL, ROUND(z,2), d1, d2 FROM z WHERE y0 = 2019 ORDER BY z DESC LIMIT 8)
UNION ALL
(SELECT 'bottom_2019', st, y0, NULL, NULL, NULL, NULL, ROUND(z,2), d1, d2 FROM z WHERE y0 = 2019 ORDER BY z ASC LIMIT 5)
) ORDER BY k, 8 DESC;
-- @V4 Oklahoma and nation by year 2015-2023: deaths, vet pop, published rate vs deaths/pop, pop year-over-year change
SELECT STATE, YEAR_OF_DEATH, VETERAN_SUICIDES, VETERAN_POPULATION_ESTIMATE, VETERAN_SUICIDE_RATE_PER_100K,
       ROUND(1e5 * VETERAN_SUICIDES / NULLIF(VETERAN_POPULATION_ESTIMATE,0),1) crude,
       ROUND(VETERAN_POPULATION_ESTIMATE / NULLIF(LAG(VETERAN_POPULATION_ESTIMATE) OVER (PARTITION BY STATE ORDER BY YEAR_OF_DEATH),0),3) pop_yoy,
       _SOURCE_RUN_ID
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_VA_SUICIDE_STATE
WHERE STATE IN ('Oklahoma','U.S. Total') AND YEAR_OF_DEATH >= 2015
ORDER BY STATE, YEAR_OF_DEATH;

-- @V5 Columns of the two CDC state-level candidates
SELECT table_name, LISTAGG(column_name, ', ') WITHIN GROUP (ORDER BY ordinal_position) FROM LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS WHERE table_schema='HEALTH' AND table_name IN ('HEALTH__FED_CDC_SUICIDE_RATES','HEALTH__FED_CDC_LEADING_CAUSES_STATE','HEALTH__FED_VA_SUICIDE_APPENDIX') GROUP BY 1;

-- @V6 CDC leading causes by state: Oklahoma and US suicide deaths by year (independent full-state general-population count), and year range
SELECT STATE, YEAR, DEATHS, AGE_ADJUSTED_DEATH_RATE, (SELECT MAX(YEAR) FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_LEADING_CAUSES_STATE) max_year
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_LEADING_CAUSES_STATE
WHERE CAUSE_NAME ILIKE '%SUICIDE%' AND STATE IN ('Oklahoma','Kansas','United States') AND YEAR >= 2011
ORDER BY STATE, YEAR;
-- @V7 CDC county file, Oklahoma: all counties with a count vs the four-year panel, per year 2019-2023, and how many OK counties exist
WITH c AS (
  SELECT GEOID::string g, PERIOD, COUNT_SUP cnt, COUNT_SUP / NULLIF(RATE,0) * 1e5 pop
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY
  WHERE INTENT = 'All_Suicide' AND ST_NAME = 'Oklahoma' AND PERIOD IN ('2019','2020','2021','2022','2023')
), panel AS (SELECT g FROM c WHERE cnt IS NOT NULL AND pop > 0 AND PERIOD IN ('2019','2020','2022','2023') GROUP BY g HAVING COUNT(DISTINCT PERIOD) = 4)
SELECT PERIOD, COUNT(DISTINCT g) county_rows, COUNT(IFF(cnt IS NOT NULL, 1, NULL)) counted, SUM(cnt) counted_deaths,
       SUM(IFF(g IN (SELECT g FROM panel), cnt, 0)) panel_deaths,
       ROUND(1e5 * SUM(IFF(g IN (SELECT g FROM panel), cnt, 0)) / NULLIF(SUM(IFF(g IN (SELECT g FROM panel), pop, 0)),0),1) panel_rate,
       ROUND(SUM(IFF(g IN (SELECT g FROM panel), pop, 0))) panel_pop
FROM c GROUP BY PERIOD ORDER BY PERIOD;
