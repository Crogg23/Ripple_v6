-- Dull-explanation test for the ash-pond status: what burns at the plants whose UNLINED pond is 'OP' but that have no coal unit running in 2024?
-- If OP meant "receiving coal ash now", these plants should not exist. Grouped by main 2024 fuel, with eGRID 2022 coal output and names.
with p as (select PLANT_CODE, PLANT_NAME, UTILITY_NAME, STATE from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT
           where ASH_IMPOUNDMENT='Y' and ASH_IMPOUNDMENT_LINED='N' and ASH_IMPOUNDMENT_STATUS='OP'),
g as (select PLANT_CODE, sum(iff(ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC') and STATUS='OP',NAMEPLATE_CAPACITY_MW,0)) coal_op_mw,
        max_by(ENERGY_SOURCE_1, NAMEPLATE_CAPACITY_MW) main_fuel, sum(iff(STATUS='OP',NAMEPLATE_CAPACITY_MW,0)) op_mw
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR group by 1),
e as (select try_to_number(to_varchar(DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE)) pc, max(PLANT_ANNUAL_COAL_NET_GENERATION_MWH) coal22, max(PLANT_PRIMARY_FUEL) pf22
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 group by 1)
select coalesce(g.main_fuel,'(no generator row)') main_fuel_2024, count(*) plants, round(sum(g.op_mw)) op_mw, count_if(e.coal22>0) coal_in_2022,
  listagg(distinct e.pf22, ',') egrid_fuel_2022, listagg(p.PLANT_NAME||' ('||p.STATE||')', '; ') within group (order by p.PLANT_NAME) names
from p left join g on g.PLANT_CODE=p.PLANT_CODE left join e on e.pc=p.PLANT_CODE
where coalesce(g.coal_op_mw,0)=0
group by 1 order by plants desc
