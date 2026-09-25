-- g61 deep pass 3, 2026-09-24. Python door (connect/db.py), read-only.
-- 19 SELECT/WITH statements below, run through g61/run.py (refuses anything else).
-- Every connection (12 total) first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'
-- Results: g61/qNN.json. Local math on those pulls: g61/analyze.py (no warehouse calls).

-- [q01] statement 1
-- shape: rows, key uniqueness, years, load runs for all 5 tables + the generator table used for joins
SELECT 'OWNER' t, COUNT(*) n, COUNT(DISTINCT PLANT_CODE||'-'||GENERATOR_ID) k_gen, COUNT(DISTINCT PLANT_CODE||'-'||GENERATOR_ID||'-'||OWNERSHIP_ID) k_row, COUNT(DISTINCT OWNERSHIP_ID) owners, NULL yrs, COUNT(DISTINCT _SOURCE_RUN_ID) runs, LISTAGG(DISTINCT _SRC_FILE, ',') files FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER
UNION ALL SELECT 'GEN', COUNT(*), COUNT(DISTINCT PLANT_CODE||'-'||GENERATOR_ID), NULL, NULL, LISTAGG(DISTINCT STATUS, ','), COUNT(DISTINCT _SOURCE_RUN_ID), LISTAGG(DISTINCT _SRC_FILE, ',') FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR
UNION ALL SELECT 'OPS', COUNT(*), COUNT(DISTINCT UTILITY_NUMBER||'-'||STATE), COUNT(DISTINCT RECORD_ID), COUNT(DISTINCT UTILITY_NUMBER), LISTAGG(DISTINCT DATA_YEAR, ','), COUNT(DISTINCT _SOURCE_RUN_ID), LISTAGG(DISTINCT _SRC_FILE, ',') FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_OPERATIONAL_DATA
UNION ALL SELECT 'SHORT', COUNT(*), COUNT(DISTINCT UTILITY_NUMBER||'-'||STATE), COUNT(DISTINCT RECORD_ID), COUNT(DISTINCT UTILITY_NUMBER), LISTAGG(DISTINCT DATA_YEAR, ','), COUNT(DISTINCT _SOURCE_RUN_ID), LISTAGG(DISTINCT _SRC_FILE, ',') FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SHORT_FORM
UNION ALL SELECT 'CS', COUNT(*), COUNT(DISTINCT FACILITY_NUMBER), COUNT(DISTINCT RECORD_ID), COUNT(DISTINCT UTILITY_NUMBER), LISTAGG(DISTINCT DATA_YEAR, ','), COUNT(DISTINCT _SOURCE_RUN_ID), LISTAGG(DISTINCT _SRC_FILE, ',') FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST_CS
UNION ALL SELECT 'DR', COUNT(*), COUNT(DISTINCT UTILITY_NUMBER||'-'||STATE), COUNT(DISTINCT RECORD_ID), COUNT(DISTINCT UTILITY_NUMBER), LISTAGG(DISTINCT DATA_YEAR, ','), COUNT(DISTINCT _SOURCE_RUN_ID), LISTAGG(DISTINCT _SRC_FILE, ',') FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DEMAND_RESPONSE;

-- [q02] statement 2
-- OWNER: per generator, do the owner shares add to 100%? by status
WITH g AS (
  SELECT PLANT_CODE, GENERATOR_ID, MAX(STATUS) st, COUNT(DISTINCT STATUS) nst, COUNT(*) n_own,
         SUM(PERCENT_OWNED) s, MIN(PERCENT_OWNED) mn, MAX(PERCENT_OWNED) mx
  FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER GROUP BY 1,2)
SELECT st, COUNT(*) gens, SUM(n_own) rows_, SUM(IFF(ABS(s-1)<0.0051,1,0)) sum_1, SUM(IFF(s<0.9949,1,0)) under_1,
       SUM(IFF(s>1.0051,1,0)) over_1, SUM(IFF(nst>1,1,0)) mixed_status, ROUND(AVG(n_own),2) avg_owners, MAX(n_own) max_owners,
       SUM(IFF(n_own=1,1,0)) single_owner_rows, MIN(mn) min_pct, MAX(mx) max_pct, SUM(IFF(mn IS NULL,1,0)) null_pct
FROM g GROUP BY ROLLUP(st) ORDER BY gens DESC;

-- [q03] statement 3
-- OWNER: top owners by generators held; is the owner also the operator; how many plant states
SELECT OWNERSHIP_ID, OWNER_NAME, OWNER_CITY, OWNER_STATE, COUNT(*) gens, COUNT(DISTINCT PLANT_CODE) plants,
       COUNT(DISTINCT STATE) plant_states, SUM(IFF(STATE<>OWNER_STATE,1,0)) gens_out_of_state,
       ROUND(SUM(PERCENT_OWNED),2) sum_pct, SUM(IFF(OWNERSHIP_ID=UTILITY_ID,1,0)) owner_is_operator,
       COUNT(DISTINCT OWNER_NAME) name_variants
FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER
GROUP BY 1,2,3,4 ORDER BY gens DESC LIMIT 40;

-- [q04] statement 4
-- OWNER join check: owner rows -> 2024 generator table (MW, fuel) -> eGRID 2022 plant (CO2). Land rate and owned MW by fuel.
WITH o AS (SELECT * FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER),
g AS (SELECT PLANT_CODE, GENERATOR_ID, NAMEPLATE_CAPACITY_MW mw, ENERGY_SOURCE_1 f FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR),
e AS (SELECT TRY_TO_NUMBER(TO_VARCHAR(DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE)) pc, COUNT(*) n, MAX(PLANT_ANNUAL_CO2_EMISSIONS_TONS) co2
      FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 GROUP BY 1)
SELECT o.STATUS IN ('OP','SB','OA','OS') operable,
       CASE WHEN g.f IN ('BIT','SUB','LIG','ANT','RC','WC','SGC') THEN 'coal' WHEN g.f='NG' THEN 'gas' WHEN g.f='NUC' THEN 'nuclear'
            WHEN g.f='SUN' THEN 'solar' WHEN g.f='WND' THEN 'wind' WHEN g.f='WAT' THEN 'hydro' WHEN g.f IS NULL THEN 'no_gen_match' ELSE 'other:'||g.f END fuel,
       COUNT(*) owner_rows, COUNT(DISTINCT o.PLANT_CODE) plants, COUNT(DISTINCT o.OWNERSHIP_ID) owners,
       ROUND(SUM(o.PERCENT_OWNED*g.mw)) owned_mw, ROUND(SUM(IFF(o.OWNERSHIP_ID<>o.UTILITY_ID, o.PERCENT_OWNED*g.mw, 0))) owned_mw_nonoperator,
       SUM(IFF(e.pc IS NULL,1,0)) rows_no_egrid, MAX(e.n) max_egrid_dupes
FROM o LEFT JOIN g ON g.PLANT_CODE=o.PLANT_CODE AND g.GENERATOR_ID=o.GENERATOR_ID
LEFT JOIN e ON e.pc=o.PLANT_CODE
GROUP BY 1,2 ORDER BY 1 DESC, owned_mw DESC NULLS LAST;

-- [q05] statement 5
-- OWNER x GENERATOR x eGRID 2022 x OPERATIONAL_DATA: every owner's owned MW by fuel, CO2 allocated by share of plant fossil MW,
-- coal output allocated by share of plant coal MW, and the owner's own 2024 retail sales (joined on EIA utility ID)
WITH g AS (SELECT PLANT_CODE, GENERATOR_ID, NAMEPLATE_CAPACITY_MW mw,
             CASE WHEN ENERGY_SOURCE_1 IN ('BIT','SUB','LIG','ANT','RC','WC','SGC') THEN 'coal'
                  WHEN ENERGY_SOURCE_1 IN ('NG','DFO','RFO','KER','JF','WO','PC','OG','BFG','SGP') THEN 'oilgas' ELSE 'clean_other' END fg
           FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR),
p AS (SELECT PLANT_CODE, SUM(IFF(fg<>'clean_other',mw,0)) plant_fossil_mw, SUM(IFF(fg='coal',mw,0)) plant_coal_mw FROM g GROUP BY 1),
e AS (SELECT TRY_TO_NUMBER(TO_VARCHAR(DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE)) pc, MAX(PLANT_ANNUAL_CO2_EMISSIONS_TONS) co2,
             MAX(PLANT_ANNUAL_COAL_NET_GENERATION_MWH) coal_gen
      FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 GROUP BY 1),
o AS (SELECT o.OWNERSHIP_ID, o.OWNER_NAME, o.OWNER_CITY, o.OWNER_STATE, o.STATE plant_state, o.PLANT_CODE, o.PLANT_NAME, o.UTILITY_ID,
             o.PERCENT_OWNED*g.mw own_mw, g.fg
      FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER o
      JOIN g ON g.PLANT_CODE=o.PLANT_CODE AND g.GENERATOR_ID=o.GENERATOR_ID),
op AS (SELECT o.OWNERSHIP_ID, o.PLANT_CODE, MAX(o.plant_state) plant_state, MAX(o.PLANT_NAME) plant_name,
              SUM(own_mw) own_mw, SUM(IFF(fg='coal',own_mw,0)) coal_mw, SUM(IFF(fg<>'clean_other',own_mw,0)) fossil_mw
       FROM o GROUP BY 1,2),
oa AS (SELECT op.OWNERSHIP_ID, SUM(op.own_mw) own_mw, SUM(op.coal_mw) coal_mw, SUM(op.fossil_mw) fossil_mw,
              SUM(IFF(p.plant_fossil_mw>0, op.fossil_mw/p.plant_fossil_mw*e.co2, 0)) co2_alloc,
              SUM(IFF(p.plant_coal_mw>0, op.coal_mw/p.plant_coal_mw*e.coal_gen, 0)) coal_gen_alloc,
              COUNT(DISTINCT IFF(op.coal_mw>0, op.PLANT_CODE, NULL)) coal_plants,
              LISTAGG(DISTINCT IFF(op.coal_mw>0, op.plant_state||':'||op.plant_name, NULL), '; ') coal_plant_list
       FROM op JOIN p ON p.PLANT_CODE=op.PLANT_CODE LEFT JOIN e ON e.pc=op.PLANT_CODE GROUP BY 1),
own AS (SELECT OWNERSHIP_ID, MAX(OWNER_NAME) owner_name, MAX(OWNER_CITY) owner_city, MAX(OWNER_STATE) owner_state,
               SUM(IFF(fg='coal' AND plant_state<>OWNER_STATE, own_mw, 0)) coal_mw_out_of_state,
               MAX(IFF(OWNERSHIP_ID=UTILITY_ID,1,0)) is_operator_somewhere
        FROM o GROUP BY 1),
ops AS (SELECT UTILITY_NUMBER, MAX(OWNERSHIP_TYPE) own_type, COUNT(*) ops_states, SUM(SALES_TO_ULTIMATE_CUSTOMERS_MWH) retail_mwh,
               SUM(SALES_FOR_RESALE_MWH) resale_mwh, SUM(NET_GENERATION_MWH) netgen_mwh, SUM(WHOLESALE_POWER_PURCHASES_MWH) purch_mwh
        FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_OPERATIONAL_DATA WHERE UTILITY_NUMBER<>99999 GROUP BY 1)
SELECT own.OWNERSHIP_ID, own.owner_name, own.owner_city, own.owner_state, ops.own_type, ROUND(oa.own_mw,1) own_mw, ROUND(oa.coal_mw,1) coal_mw,
       ROUND(own.coal_mw_out_of_state,1) coal_mw_oos, ROUND(oa.fossil_mw,1) fossil_mw, ROUND(oa.co2_alloc) co2_tons_2022,
       ROUND(oa.coal_gen_alloc) coal_gen_mwh_2022, oa.coal_plants, oa.coal_plant_list, ops.retail_mwh, ops.resale_mwh, ops.netgen_mwh, ops.purch_mwh,
       ops.ops_states, own.is_operator_somewhere
FROM own JOIN oa ON oa.OWNERSHIP_ID=own.OWNERSHIP_ID LEFT JOIN ops ON ops.UTILITY_NUMBER=own.OWNERSHIP_ID
ORDER BY co2_tons_2022 DESC NULLS LAST;

-- [q06] statement 6
-- OWNER peer test: coal units with several owners vs one owner vs operator-only. Share with a planned retirement date, by vintage.
WITH own AS (SELECT PLANT_CODE, GENERATOR_ID, COUNT(*) n_own FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER GROUP BY 1,2),
g AS (SELECT g.PLANT_CODE, g.GENERATOR_ID, g.NAMEPLATE_CAPACITY_MW mw, g.OPERATING_YEAR oy, g.PLANNED_RETIREMENT_YEAR ry, g.STATUS, g.SECTOR_NAME,
             CASE WHEN own.n_own>1 THEN 'joint' WHEN own.n_own=1 THEN 'one_nonop_owner' ELSE 'operator_only' END ownership
      FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR g
      LEFT JOIN own ON own.PLANT_CODE=g.PLANT_CODE AND own.GENERATOR_ID=g.GENERATOR_ID
      WHERE g.ENERGY_SOURCE_1 IN ('BIT','SUB','LIG','ANT','RC','WC','SGC') AND g.STATUS='OP' AND g.NAMEPLATE_CAPACITY_MW>=100)
SELECT CASE WHEN oy<1970 THEN 'a <1970' WHEN oy<1980 THEN 'b 1970s' WHEN oy<1990 THEN 'c 1980s' ELSE 'd 1990+' END vintage, ownership,
       COUNT(*) units, ROUND(SUM(mw)) mw, SUM(IFF(ry IS NOT NULL,1,0)) units_with_date, ROUND(SUM(IFF(ry IS NOT NULL,mw,0))) mw_with_date,
       ROUND(100*SUM(IFF(ry IS NOT NULL,mw,0))/SUM(mw),1) pct_mw_dated, ROUND(MEDIAN(mw)) med_mw, MIN(ry) min_ry, MAX(ry) max_ry,
       SUM(IFF(ry<=2030,1,0)) units_by_2030
FROM g GROUP BY ROLLUP(1,2) ORDER BY 1,2;

-- [q07] statement 7
-- OPERATIONAL_DATA whole table (1,711 rows), analyzed locally
SELECT * FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_OPERATIONAL_DATA;

-- [q08] statement 8
-- SHORT_FORM whole table (1,724 rows), analyzed locally
SELECT * FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SHORT_FORM;

-- [q09] statement 9
-- SALES_ULT_CUST_CS whole table (674 rows), analyzed locally
SELECT * FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST_CS;

-- [q10] statement 10
-- DEMAND_RESPONSE whole table (339 rows), analyzed locally
SELECT * FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DEMAND_RESPONSE;

-- [q11] statement 11
-- peer table: full-form SALES_ULT_CUST (2,815 rows) for state/class price benchmarks and customer counts
SELECT * FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST;

-- [q12] statement 12
-- CS join check: is FACILITY_NUMBER an EIA plant code? Pull each CS facility's 2024 generator-table capacity, tech and first/last online date
WITH cs AS (SELECT DISTINCT FACILITY_NUMBER FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST_CS)
SELECT cs.FACILITY_NUMBER, COUNT(g.GENERATOR_ID) gens, ROUND(SUM(g.NAMEPLATE_CAPACITY_MW),3) mw,
       MIN(g.OPERATING_YEAR*100+g.OPERATING_MONTH) first_online, MAX(g.OPERATING_YEAR*100+g.OPERATING_MONTH) last_online,
       LISTAGG(DISTINCT g.TECHNOLOGY, '; ') tech, MAX(g.PLANT_NAME) plant_name, MAX(g.STATE) plant_state, MAX(g.UTILITY_NAME) operator
FROM cs LEFT JOIN LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR g ON g.PLANT_CODE = cs.FACILITY_NUMBER
GROUP BY 1;

-- [q13] statement 13
-- time check: does any other year of EIA-861 / EIA-860 exist in the warehouse (landing or marts)?
SELECT 'LANDING' db, TABLE_SCHEMA, TABLE_NAME, ROW_COUNT FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME ILIKE '%EIA%86%' OR TABLE_NAME ILIKE '%EIA_861%' OR TABLE_NAME ILIKE '%EIA861%'
UNION ALL
SELECT 'MARTS', TABLE_SCHEMA, TABLE_NAME, ROW_COUNT FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES WHERE (TABLE_NAME ILIKE '%EIA%86%') AND TABLE_NAME NOT ILIKE 'ENERGY__FED_EIA86%';

-- [q14] statement 14
-- Holly Springs corroboration: meters and AMI-metered energy vs customers and billed MWh, for every MS/TN/AL/KY/GA municipal utility
SELECT UTILITY_NUMBER, UTILITY_NAME, STATE, OWNERSHIP, SHORT_FORM, TOTAL_TOTAL_METERS, TOTAL_AMI_METERS, TOTAL_AMR_METERS, TOTAL_NON_AMR_AMI_METERS,
       RESIDENTIAL_TOTAL_METERS, COMMERCIAL_TOTAL_METERS, TOTAL_ENERGY_SERVED_AMI_MWH
FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ADVANCED_METERS
WHERE STATE IN ('MS','TN','AL','KY','GA') AND OWNERSHIP ILIKE 'Municipal%';

-- [q15] statement 15
-- column names of the 2023 generator file in landing, to line it up with 2024
SELECT COLUMN_NAME, DATA_TYPE, ORDINAL_POSITION FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA='LANDING' AND TABLE_NAME='FED_EIA860_GENERATOR_Y2023' ORDER BY ORDINAL_POSITION;

-- [q16] statement 16
-- OWNER time check: every coal unit >=100 MW operable in the 2023 EIA-860 file, its planned retirement year in 2023 vs 2024, and its 2024 owner count
WITH y23 AS (SELECT TRY_TO_NUMBER(PLANT_CODE) pc, TRIM(GENERATOR_ID) gid, MAX(PLANT_NAME) plant_name, MAX(STATE) st, MAX(UTILITY_NAME) operator,
                    MAX(TRY_TO_DOUBLE(NAMEPLATE_CAPACITY_MW)) mw23, MAX(TRY_TO_NUMBER(PLANNED_RETIREMENT_YEAR)) ry23, MAX(TRY_TO_NUMBER(OPERATING_YEAR)) oy,
                    COUNT(*) n23
             FROM LIBRARY_RAW.LANDING.FED_EIA860_GENERATOR_Y2023
             WHERE SHEET_NAME ILIKE 'Operable%' AND ENERGY_SOURCE_1 IN ('BIT','SUB','LIG','ANT','RC','WC','SGC')
               AND TRY_TO_DOUBLE(NAMEPLATE_CAPACITY_MW) >= 100
             GROUP BY 1,2),
g24 AS (SELECT PLANT_CODE, GENERATOR_ID, PLANNED_RETIREMENT_YEAR ry24, STATUS st24, ENERGY_SOURCE_1 f24
        FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR),
own AS (SELECT PLANT_CODE, GENERATOR_ID, COUNT(*) n_own, SUM(IFF(OWNERSHIP_ID<>UTILITY_ID,1,0)) nonop_owners
        FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER GROUP BY 1,2)
SELECT y23.pc, y23.gid, y23.plant_name, y23.st, y23.operator, y23.mw23, y23.oy, y23.ry23, g24.ry24, g24.st24, g24.f24, y23.n23,
       COALESCE(own.n_own,0) n_own, COALESCE(own.nonop_owners,0) nonop_owners
FROM y23 LEFT JOIN g24 ON g24.PLANT_CODE=y23.pc AND g24.GENERATOR_ID=y23.gid
LEFT JOIN own ON own.PLANT_CODE=y23.pc AND own.GENERATOR_ID=y23.gid;

-- [q17] statement 17
-- dull-explanation test: are the coal units whose retirement date was dropped or pushed back simply converting to gas?
SELECT PLANT_NAME, STATE, GENERATOR_ID, UTILITY_NAME, NAMEPLATE_CAPACITY_MW, ENERGY_SOURCE_1, ENERGY_SOURCE_2, PLANNED_RETIREMENT_YEAR,
       PLANNED_ENERGY_SOURCE_1, PLANNED_NEW_PRIME_MOVER, PLANNED_REPOWER_YEAR, OTHER_PLANNED_MODIFICATIONS, OTHER_MODIFICATIONS_YEAR, COFIRE_FUELS, MULTIPLE_FUELS
FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR
WHERE (PLANT_CODE, GENERATOR_ID) IN ((6076,'1'),(602,'1'),(602,'2'),(889,'1'),(889,'2'),(6178,'1'),(8066,'1'),(8066,'2'),(8066,'3'),(8066,'4'),
      (6139,'1'),(6139,'3'),(8023,'1'),(8023,'2'),(8042,'1'),(8042,'2'),(564,'1'),(4050,'5'),(6101,'BW91'),(4041,'7'),(4041,'8'),(4158,'1'),(4158,'2'),(4158,'4'))
   OR (PLANT_NAME IN ('Jim Bridger','Huntington','Naughton','Dave Johnston','Wyodak','Coleto Creek','Welsh','Stanton Energy Center','Edgewater','Columbia (WI)','South Oak Creek','Brandon Shores','Baldwin Energy Complex','Sherburne County')
       AND ENERGY_SOURCE_1 IN ('BIT','SUB','LIG','NG','RC','WC'))
ORDER BY PLANT_NAME, GENERATOR_ID;

-- [q18] statement 18
-- OWNER whole table (5,495 rows) for address and filler checks, analyzed locally
SELECT PLANT_CODE, GENERATOR_ID, OWNERSHIP_ID, UTILITY_ID, UTILITY_NAME, PLANT_NAME, STATE, STATUS, OWNER_NAME, OWNER_STREET_ADDRESS, OWNER_CITY, OWNER_STATE, OWNER_ZIP, PERCENT_OWNED FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER;

-- [q19] statement 19
-- geography for the Mississippi loss cluster: every county each Mississippi utility serves (EIA-861 service territory)
SELECT UTILITY_NUMBER, UTILITY_NAME, LISTAGG(DISTINCT COUNTY, ', ') WITHIN GROUP (ORDER BY COUNTY) counties, COUNT(DISTINCT COUNTY) n_counties
FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SERVICE_TERRITORY WHERE STATE='MS' GROUP BY 1,2;
