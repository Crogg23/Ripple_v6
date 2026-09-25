-- Generator: by fuel group and status, capacity, retirement dates (incl. dates already past), vintage, sanity traps, duplicate keys
with t as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR),
fg as (select *, case when ENERGY_SOURCE_1 in ('BIT','SUB','LIG','ANT','RC','WC','SGC') then 'coal' when ENERGY_SOURCE_1='NG' then 'gas'
   when ENERGY_SOURCE_1 in ('DFO','RFO','KER','JF','WO','PC') then 'oil' when ENERGY_SOURCE_1='NUC' then 'nuclear' when ENERGY_SOURCE_1='SUN' then 'solar'
   when ENERGY_SOURCE_1='WND' then 'wind' when ENERGY_SOURCE_1='WAT' then 'hydro' when ENERGY_SOURCE_1='MWH' then 'battery' else 'other' end fuel from t)
select fuel, STATUS, count(*) gens, round(sum(NAMEPLATE_CAPACITY_MW)) mw, count(PLANNED_RETIREMENT_YEAR) w_ret, round(sum(iff(PLANNED_RETIREMENT_YEAR is not null,NAMEPLATE_CAPACITY_MW,0))) ret_mw,
 count_if(PLANNED_RETIREMENT_YEAR<=2024) ret_past, min(PLANNED_RETIREMENT_YEAR) min_ry, max(PLANNED_RETIREMENT_YEAR) max_ry,
 min(OPERATING_YEAR) min_oy, median(OPERATING_YEAR) med_oy, count_if(SUMMER_CAPACITY_MW>NAMEPLATE_CAPACITY_MW*1.2) summer_gt, count_if(MINIMUM_LOAD_MW>NAMEPLATE_CAPACITY_MW) minload_gt,
 count_if(NAMEPLATE_CAPACITY_MW<=0 or NAMEPLATE_CAPACITY_MW is null) cap0, count(distinct PLANT_CODE) plants,
 (select count(*)-count(distinct PLANT_CODE||'|'||GENERATOR_ID) from t) dupkey_all, listagg(distinct _SRC_FILE,'|') src
from fg group by 1,2 order by mw desc
