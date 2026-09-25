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
ORDER BY co2_tons_2022 DESC NULLS LAST
