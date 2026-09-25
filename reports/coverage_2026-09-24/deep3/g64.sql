-- deep3/g64: deep pass 3, 2026-09-24. Python door (connect/db.py), read-only SELECT/WITH only, QUERY_TAG 'deep3-2026-09-24'.
-- Every connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'. Those two are not counted.
-- Tables: ENERGY__FED_EIA861_DISTRIBUTION_SYSTEMS, _UTILITY_DATA, _DYNAMIC_PRICING, _NET_METERING, _NON_NET_METERING_DISTRIBUTED.
-- 14 statements (S01-S14), all below, in run order. S01 returned 0 rows (LIKE pattern had no ESCAPE clause); it still counts.
-- S02-S09 pull whole small tables (all under 3K rows). Peer, time and join math on them ran locally in pandas (g64/ scratch).
-- S10-S14 redo each headline join inside the warehouse so the numbers are reproducible without the scratch.
-- Outside the warehouse: EIA's own source workbooks f8612024.zip, f8612019.zip, f8612014.zip (eia.gov), saved in g64/, used to
--   (a) check row completeness against the source sheets (g64/src_compare.py), (b) recover lost column labels,
--   (c) add 2014 and 2019 for the time comparison (g64/time_nm.py, g64/time_dp.py). Those are file reads, not statements.

-- S01 EIA-861 tables in the mart: row counts and every column, to find the denominator tables
SELECT c.TABLE_NAME, t.ROW_COUNT, COUNT(*) n_cols,
       LISTAGG(c.COLUMN_NAME || ':' || c.DATA_TYPE, ', ') WITHIN GROUP (ORDER BY c.ORDINAL_POSITION) cols
FROM LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS c
JOIN LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES t
  ON t.TABLE_SCHEMA = c.TABLE_SCHEMA AND t.TABLE_NAME = c.TABLE_NAME
WHERE c.TABLE_SCHEMA = 'ENERGY' AND c.TABLE_NAME LIKE 'ENERGY\\_\\_FED\\_EIA%861%'
GROUP BY 1, 2 ORDER BY 1;

-- S02 distribution systems: whole table (1,353 rows)
SELECT * FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DISTRIBUTION_SYSTEMS;

-- S03 utility data: whole table (1,701 rows)
SELECT * FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_UTILITY_DATA;

-- S04 dynamic pricing: whole table (857 rows)
SELECT * FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DYNAMIC_PRICING;

-- S05 net metering: whole table (1,004 rows)
SELECT * FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_NET_METERING;

-- S06 non-net-metering distributed: whole table (507 rows)
SELECT * FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_NON_NET_METERING_DISTRIBUTED;

-- S07 sales to ultimate customers: whole table, the customer-count and price denominator for every join
SELECT * FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST;

-- S08 reliability: whole table, outage minutes (SAIDI) and counts (SAIFI) per utility-state, the harm side
SELECT * FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_RELIABILITY;

-- S09 advanced meters: whole table, smart-meter counts per utility-state, the precondition for time-varying rates
SELECT * FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ADVANCED_METERS;

-- S10 net metering: Arizona residential solar installations per 1,000 residential customers (join to sales on utility number + state; sales rows Bundled + Delivery only; adjustment rows 99999 dropped)
WITH nm AS (
  SELECT UTILITY_NUMBER, STATE, MAX(UTILITY_NAME) name, LISTAGG(DISTINCT TECHNOLOGY_TYPE, ',') ac_dc,
         SUM(RESIDENTIAL_INSTALLATIONS) res_inst, SUM(RESIDENTIAL_CAPACITY_MW) res_mw
  FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_NET_METERING
  WHERE UTILITY_NUMBER <> 99999 GROUP BY 1, 2),
s AS (
  SELECT UTILITY_NUMBER, STATE, SUM(RESIDENTIAL_CUSTOMERS) res_cust
  FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST
  WHERE SERVICE_TYPE IN ('Bundled', 'Delivery') AND UTILITY_NUMBER <> 99999 GROUP BY 1, 2)
SELECT nm.STATE, nm.name, nm.ac_dc, nm.res_inst, ROUND(nm.res_mw, 1) res_mw, s.res_cust,
       ROUND(1000 * nm.res_inst / NULLIF(s.res_cust, 0), 1) inst_per_1k
FROM nm LEFT JOIN s ON s.UTILITY_NUMBER = nm.UTILITY_NUMBER AND s.STATE = nm.STATE
WHERE nm.STATE = 'AZ' AND s.res_cust >= 10000
ORDER BY inst_per_1k;

-- S11 dynamic pricing: residential enrolled vs residential customers and smart meters, default-TOU utilities, the Evergy Kansas twin, and the suspect reporters
WITH dp AS (
  SELECT UTILITY_NUMBER, STATE, MAX(UTILITY_NAME) name, SUM(RESIDENTIAL_CUSTOMERS_ENROLLED) enrolled,
         MAX(RESIDENTIAL_TIME_OF_USE_PRICING) tou, MAX(RESIDENTIAL_CRITICAL_PEAK_REBATE) cpr
  FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DYNAMIC_PRICING GROUP BY 1, 2),
s AS (
  SELECT UTILITY_NUMBER, STATE, SUM(RESIDENTIAL_CUSTOMERS) res_cust
  FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST
  WHERE SERVICE_TYPE IN ('Bundled', 'Delivery') GROUP BY 1, 2),
am AS (
  SELECT UTILITY_NUMBER, STATE, SUM(RESIDENTIAL_AMI_METERS) res_ami, SUM(RESIDENTIAL_TOTAL_METERS) res_meters
  FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ADVANCED_METERS GROUP BY 1, 2)
SELECT dp.STATE, dp.name, dp.tou, dp.cpr, dp.enrolled, s.res_cust, ROUND(dp.enrolled / NULLIF(s.res_cust, 0), 3) share_enrolled,
       am.res_ami, am.res_meters
FROM dp LEFT JOIN s ON s.UTILITY_NUMBER = dp.UTILITY_NUMBER AND s.STATE = dp.STATE
LEFT JOIN am ON am.UTILITY_NUMBER = dp.UTILITY_NUMBER AND am.STATE = dp.STATE
WHERE dp.name ILIKE ANY ('Evergy%', 'Union Electric%', 'Public Service Co of Colorado', 'Consumers Energy%', 'Southern California Edison%',
                         'Pacific Gas%', 'San Diego Gas%', 'DTE Electric%', 'Public Service Co of Oklahoma', 'Southwestern Electric Power%')
ORDER BY dp.name, dp.STATE;

-- S12 non-net + net metering: residential solar MW per residential customer, Southern Co. and TVA-area utilities (AL, GA, MS, TN) with 100K+ homes
WITH nm AS (
  SELECT UTILITY_NUMBER, STATE, SUM(RESIDENTIAL_CAPACITY_MW) nm_res_mw, SUM(RESIDENTIAL_INSTALLATIONS) nm_res_inst
  FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_NET_METERING WHERE UTILITY_NUMBER <> 99999 GROUP BY 1, 2),
nn AS (
  SELECT UTILITY_NUMBER, STATE, SUM(RESIDENTIAL_CAPACITY_MW_TECH_01) nn_res_pv_mw, SUM(NUMBER_OF_GENERATORS) nn_generators
  FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_NON_NET_METERING_DISTRIBUTED WHERE UTILITY_NUMBER <> 99999 GROUP BY 1, 2),
s AS (
  SELECT UTILITY_NUMBER, STATE, MAX(UTILITY_NAME) name, SUM(RESIDENTIAL_CUSTOMERS) res_cust
  FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST
  WHERE SERVICE_TYPE IN ('Bundled', 'Delivery') AND UTILITY_NUMBER <> 99999 GROUP BY 1, 2)
SELECT s.STATE, s.name, s.res_cust, nm.nm_res_inst, ROUND(nm.nm_res_mw, 3) nm_res_mw, ROUND(nn.nn_res_pv_mw, 3) nn_res_pv_mw, nn.nn_generators,
       ROUND(1e6 * (COALESCE(nm.nm_res_mw, 0) + COALESCE(nn.nn_res_pv_mw, 0)) / s.res_cust, 1) res_solar_watts_per_home
FROM s LEFT JOIN nm ON nm.UTILITY_NUMBER = s.UTILITY_NUMBER AND nm.STATE = s.STATE
LEFT JOIN nn ON nn.UTILITY_NUMBER = s.UTILITY_NUMBER AND nn.STATE = s.STATE
WHERE s.STATE IN ('AL', 'GA', 'MS', 'TN') AND s.res_cust >= 100000
ORDER BY res_solar_watts_per_home;

-- S13 distribution systems: the zero-VVO big utilities, the round-100% reporters, and customers per circuit (join to sales)
WITH s AS (
  SELECT UTILITY_NUMBER, STATE, SUM(TOTAL_CUSTOMERS) cust
  FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST
  WHERE SERVICE_TYPE IN ('Bundled', 'Delivery') GROUP BY 1, 2)
SELECT d.STATE, d.UTILITY_NAME, d.DISTRIBUTION_CIRCUITS, d.CIRCUITS_WITH_VOLTAGE_OPTIMIZATION,
       ROUND(d.CIRCUITS_WITH_VOLTAGE_OPTIMIZATION / d.DISTRIBUTION_CIRCUITS, 3) vo_share, s.cust,
       ROUND(s.cust / d.DISTRIBUTION_CIRCUITS) cust_per_circuit
FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DISTRIBUTION_SYSTEMS d
LEFT JOIN s ON s.UTILITY_NUMBER = d.UTILITY_NUMBER AND s.STATE = d.STATE
WHERE d.DISTRIBUTION_CIRCUITS >= 1000 OR d.UTILITY_NAME ILIKE 'Northern Indiana%' OR d.UTILITY_NAME ILIKE 'Duke Energy%'
ORDER BY vo_share NULLS LAST, d.DISTRIBUTION_CIRCUITS DESC;

-- S14 trap sweep: filler rows per table (adjustment 99999, withheld 88888, all-null note rows) and the negative sums they carry
SELECT 'NET_METERING' t, COUNT_IF(UTILITY_NUMBER = 99999) adj_rows, COUNT_IF(UTILITY_NUMBER = 88888) withheld, COUNT_IF(UTILITY_NUMBER IS NULL) null_rows,
       ROUND(SUM(IFF(UTILITY_NUMBER = 99999, TOTAL_CAPACITY_MW, 0)), 1) adj_mw, COUNT_IF(TOTAL_CAPACITY_MW < 0 AND UTILITY_NUMBER <> 99999) neg_real
FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_NET_METERING
UNION ALL
SELECT 'NON_NET', COUNT_IF(UTILITY_NUMBER = 99999), COUNT_IF(UTILITY_NUMBER = 88888), COUNT_IF(UTILITY_NUMBER IS NULL),
       ROUND(SUM(IFF(UTILITY_NUMBER = 99999, TOTAL_CAPACITY_MW, 0)), 1), COUNT_IF(TOTAL_CAPACITY_MW < 0 AND UTILITY_NUMBER <> 99999)
FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_NON_NET_METERING_DISTRIBUTED
UNION ALL
SELECT 'DYNAMIC_PRICING', COUNT_IF(UTILITY_NUMBER = 99999), COUNT_IF(UTILITY_NUMBER = 88888), COUNT_IF(UTILITY_NUMBER IS NULL), NULL, NULL
FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DYNAMIC_PRICING
UNION ALL
SELECT 'DISTRIBUTION_SYSTEMS', COUNT_IF(UTILITY_NUMBER = 99999), COUNT_IF(UTILITY_NUMBER = 88888), COUNT_IF(UTILITY_NUMBER IS NULL), NULL, NULL
FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DISTRIBUTION_SYSTEMS
UNION ALL
SELECT 'UTILITY_DATA', COUNT_IF(UTILITY_NUMBER = 99999), COUNT_IF(UTILITY_NUMBER = 88888), COUNT_IF(UTILITY_NUMBER IS NULL), NULL, NULL
FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_UTILITY_DATA;
