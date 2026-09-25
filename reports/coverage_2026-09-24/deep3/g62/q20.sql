-- Generator eyeball: the big units not in plain OP status (nuclear OS/OA, coal/gas over 300 MW), every carbon-capture Y unit,
-- and hydro units with summer capacity over 1.2x nameplate (trap check: 5 biggest).
with t as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR)
select * from (select 'not_op' k, PLANT_NAME, UTILITY_NAME, STATE, GENERATOR_ID, TECHNOLOGY, STATUS, round(NAMEPLATE_CAPACITY_MW)::text mw, OPERATING_YEAR::text oy,
   PLANNED_RETIREMENT_YEAR::text ry, SUMMER_CAPACITY_MW::text summer from t
 where STATUS<>'OP' and (ENERGY_SOURCE_1='NUC' or NAMEPLATE_CAPACITY_MW>=300) order by NAMEPLATE_CAPACITY_MW desc limit 25)
union all
select 'ccs', PLANT_NAME, UTILITY_NAME, STATE, GENERATOR_ID, TECHNOLOGY, STATUS, round(NAMEPLATE_CAPACITY_MW)::text, OPERATING_YEAR::text, PLANNED_RETIREMENT_YEAR::text, SUMMER_CAPACITY_MW::text
 from t where CARBON_CAPTURE_TECHNOLOGY='Y'
union all
select * from (select 'hydro_summer', PLANT_NAME, UTILITY_NAME, STATE, GENERATOR_ID, TECHNOLOGY, STATUS, NAMEPLATE_CAPACITY_MW::text, OPERATING_YEAR::text, round(SUMMER_CAPACITY_MW/NAMEPLATE_CAPACITY_MW,2)::text, SUMMER_CAPACITY_MW::text
 from t where ENERGY_SOURCE_1='WAT' and SUMMER_CAPACITY_MW>1.2*NAMEPLATE_CAPACITY_MW order by SUMMER_CAPACITY_MW desc limit 5)
