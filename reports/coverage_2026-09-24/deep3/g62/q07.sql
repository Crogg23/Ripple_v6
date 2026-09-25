-- Ash ponds: every plant that says it has one, bucketed by lined / status / what its generators burn in 2024 / whether eGRID 2022 shows coal output.
-- Join 1: plant -> generator on PLANT_CODE. Join 2: plant -> eGRID 2022 on ORIS code (text, cast to number).
with p as (select PLANT_CODE, ASH_IMPOUNDMENT_LINED lined, ASH_IMPOUNDMENT_STATUS ast from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT where ASH_IMPOUNDMENT='Y'),
g as (select PLANT_CODE,
    sum(iff(ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC'),NAMEPLATE_CAPACITY_MW,0)) coal_mw,
    sum(iff(ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC') and STATUS='OP',NAMEPLATE_CAPACITY_MW,0)) coal_op_mw,
    sum(iff(ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC') and STATUS='OP' and PLANNED_RETIREMENT_YEAR is not null,NAMEPLATE_CAPACITY_MW,0)) coal_op_dated_mw,
    sum(NAMEPLATE_CAPACITY_MW) all_mw
    from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR group by 1),
e as (select try_to_number(to_varchar(DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE)) pc, count(*) n, max(PLANT_ANNUAL_COAL_NET_GENERATION_MWH) coal_gen22
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 group by 1)
select p.lined, p.ast,
  case when g.PLANT_CODE is null then 'no generator row' when g.coal_op_mw>0 then 'coal running' when g.coal_mw>0 then 'coal all SB/OS/OA' else 'no coal generator' end gen_class,
  count(*) plants, round(sum(g.coal_op_mw)) coal_op_mw, round(sum(g.coal_op_dated_mw)) coal_op_dated_mw, round(sum(g.all_mw)) all_mw,
  count(e.pc) in_egrid, count_if(e.coal_gen22>0) coal_gen_2022, round(sum(e.coal_gen22)/1e6,1) coal_twh_2022, max(e.n) egrid_dupes
from p left join g on g.PLANT_CODE=p.PLANT_CODE left join e on e.pc=p.PLANT_CODE
group by 1,2,3 order by 1,2,3
