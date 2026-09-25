-- Generator time series: MW brought online per year (2000-2024) by fuel, and MW with a planned retirement per year (2025-2040) by fuel. Operable units only (this table).
with t as (select *, case when ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC') then 'coal' when ENERGY_SOURCE_1='NG' then 'gas'
   when ENERGY_SOURCE_1 in ('DFO','RFO','KER','JF','WO','PC') then 'oil' when ENERGY_SOURCE_1='SUN' then 'solar'
   when ENERGY_SOURCE_1='WND' then 'wind' when ENERGY_SOURCE_1='MWH' then 'battery' else 'other' end fuel
   from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR),
b as (select 'built' k, OPERATING_YEAR yr, fuel, NAMEPLATE_CAPACITY_MW mw from t where OPERATING_YEAR>=2000
      union all select 'retire', PLANNED_RETIREMENT_YEAR, fuel, NAMEPLATE_CAPACITY_MW from t where PLANNED_RETIREMENT_YEAR is not null and PLANNED_RETIREMENT_YEAR<=2040)
select k, yr, round(sum(iff(fuel='gas',mw,0))) gas, round(sum(iff(fuel='coal',mw,0))) coal, round(sum(iff(fuel='oil',mw,0))) oil, round(sum(iff(fuel='solar',mw,0))) solar,
  round(sum(iff(fuel='wind',mw,0))) wind, round(sum(iff(fuel='battery',mw,0))) battery, round(sum(iff(fuel='other',mw,0))) other, count(*) gens
from b group by 1,2 order by 1,2
