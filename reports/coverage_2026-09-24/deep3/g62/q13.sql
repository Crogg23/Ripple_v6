-- Generator x eGRID 2022: plants whose every 2024-operable unit was online by 2021, grouped by main fuel. How much "OP" capacity sat at plants
-- that made zero or negative net power in 2022, and the capacity factor spread per fuel. Land rate on the ORIS code first.
with g as (select PLANT_CODE, max(OPERATING_YEAR) newest_unit, sum(NAMEPLATE_CAPACITY_MW) mw,
    max_by(case when ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC') then 'coal' when ENERGY_SOURCE_1='NG' then 'gas'
      when ENERGY_SOURCE_1 in ('DFO','RFO','KER','JF','WO','PC') then 'oil' when ENERGY_SOURCE_1='SUN' then 'solar' when ENERGY_SOURCE_1='WND' then 'wind'
      when ENERGY_SOURCE_1='NUC' then 'nuclear' when ENERGY_SOURCE_1='WAT' then 'hydro' when ENERGY_SOURCE_1='MWH' then 'battery' else 'other' end, NAMEPLATE_CAPACITY_MW) fuel,
    count_if(STATUS<>'OP') not_op_units, count(*) units
    from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR group by 1),
e as (select try_to_number(to_varchar(DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE)) pc, max(PLANT_ANNUAL_NET_GENERATION_MWH) gen22, max(try_to_double(PLANT_NAMEPLATE_CAPACITY_MW)) mw22
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 group by 1),
j as (select g.*, e.pc, e.gen22, e.mw22, iff(e.mw22>0, e.gen22/(e.mw22*8760), null) cf from g left join e on e.pc=g.PLANT_CODE where g.newest_unit<=2021)
select fuel, count(*) plants, count(pc) in_egrid, round(sum(mw)) mw, count_if(pc is not null and coalesce(gen22,0)<=0) zero_gen_plants,
  round(sum(iff(pc is not null and coalesce(gen22,0)<=0, mw, 0))) zero_gen_mw, count_if(pc is not null and coalesce(gen22,0)<=0 and not_op_units=0) zero_gen_all_op,
  round(sum(iff(pc is not null and coalesce(gen22,0)<=0 and not_op_units=0, mw, 0))) zero_gen_all_op_mw,
  round(median(cf),3) med_cf, round(percentile_cont(0.1) within group (order by cf),3) p10_cf, count_if(abs(mw-mw22)/nullif(mw22,0)>0.2) mw_mismatch_20pct
from j group by 1 order by mw desc
