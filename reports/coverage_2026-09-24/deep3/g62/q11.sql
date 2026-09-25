-- Ash ponds, named: every ash-pond plant with coal generators still OP in 2024 (lined and unlined), coal MW, how much of it has any planned
-- retirement date, the latest such date, the oldest unit, eGRID 2022 coal output. Plus the state's lined/unlined split among these peers.
with p as (select PLANT_CODE, PLANT_NAME, UTILITY_NAME, STATE, COUNTY, SECTOR_NAME, REGULATORY_STATUS reg, ASH_IMPOUNDMENT_LINED lined, ASH_IMPOUNDMENT_STATUS ast
           from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT where ASH_IMPOUNDMENT='Y'),
g as (select PLANT_CODE,
    sum(iff(STATUS='OP',NAMEPLATE_CAPACITY_MW,0)) coal_op_mw,
    sum(iff(STATUS='OP' and PLANNED_RETIREMENT_YEAR is not null,NAMEPLATE_CAPACITY_MW,0)) coal_dated_mw,
    count_if(STATUS='OP') coal_units, count_if(STATUS='OP' and PLANNED_RETIREMENT_YEAR is null) undated_units,
    min(PLANNED_RETIREMENT_YEAR) first_ret, max(PLANNED_RETIREMENT_YEAR) last_ret, min(OPERATING_YEAR) oldest_unit
    from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR where ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC') group by 1 having coal_op_mw>0),
e as (select try_to_number(to_varchar(DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE)) pc, max(PLANT_ANNUAL_COAL_NET_GENERATION_MWH) coal_gen22
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 group by 1),
j as (select p.*, g.coal_op_mw, g.coal_dated_mw, g.coal_units, g.undated_units, g.first_ret, g.last_ret, g.oldest_unit, e.coal_gen22,
        count(*) over (partition by p.STATE) st_peers, count_if(p.lined='N' and p.ast='OP') over (partition by p.STATE) st_unlined_op
      from p join g on g.PLANT_CODE=p.PLANT_CODE left join e on e.pc=p.PLANT_CODE)
select lined, ast, PLANT_CODE, PLANT_NAME, UTILITY_NAME, STATE, COUNTY, SECTOR_NAME, reg, round(coal_op_mw) coal_mw, round(coal_dated_mw) dated_mw,
  coal_units, undated_units, first_ret, last_ret, oldest_unit, round(coal_gen22/1e3) coal_gwh_2022, st_peers, st_unlined_op
from j order by (lined='N' and ast='OP') desc, (coal_dated_mw=0) desc, coal_op_mw desc
