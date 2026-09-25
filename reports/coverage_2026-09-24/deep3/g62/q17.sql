-- FERC qualifying-facility flags vs the plant's own generators. (1) Small power producer = Y but operable nameplate over 80 MW.
-- (2) Cogeneration = Y but no generator flagged combined heat and power and a non-CHP sector. (3) One FERC docket number on several plants.
with p as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT),
g as (select PLANT_CODE, sum(iff(STATUS='OP',NAMEPLATE_CAPACITY_MW,0)) op_mw, count_if(ASSOCIATED_WITH_COMBINED_HEAT_AND_POWER_SYSTEM='Y') chp_units, count(*) units,
        max_by(ENERGY_SOURCE_1, NAMEPLATE_CAPACITY_MW) fuel, min(OPERATING_YEAR) first_yr
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR group by 1),
j as (select p.PLANT_CODE, p.PLANT_NAME, p.UTILITY_NAME, p.STATE, p.SECTOR_NAME, p.FERC_SMALL_POWER_PRODUCER_STATUS spp, p.FERC_SMALL_POWER_PRODUCER_DOCKET_NUMBER spp_dk,
        p.FERC_COGENERATION_STATUS cog, p.FERC_COGENERATION_DOCKET_NUMBER cog_dk, g.op_mw, g.chp_units, g.units, g.fuel, g.first_yr
      from p left join g on g.PLANT_CODE=p.PLANT_CODE),
d as (select dk, count(distinct PLANT_CODE) plants from (select PLANT_CODE, spp_dk dk from j where spp='Y' and spp_dk is not null and upper(spp_dk) not like '%PEND%'
        union all select PLANT_CODE, cog_dk from j where cog='Y' and cog_dk is not null and upper(cog_dk) not like '%PEND%') group by 1)
select 'spp_summary' k, count_if(spp='Y')::text a, count_if(spp='Y' and op_mw>80)::text b, round(sum(iff(spp='Y' and op_mw>80, op_mw, 0)))::text c,
  count_if(spp='Y' and op_mw>80 and fuel='WND')::text d, count_if(spp='Y' and op_mw>80 and fuel='SUN')::text e, count_if(spp='Y' and op_mw>80 and fuel not in ('WND','SUN'))::text f,
  count_if(spp='Y' and spp_dk is null)::text g, null h, null i from j
union all
select 'cog_summary', count_if(cog='Y')::text, count_if(cog='Y' and coalesce(chp_units,0)=0 and units>0)::text, count_if(cog='Y' and coalesce(chp_units,0)=0 and SECTOR_NAME ilike '%Non-CHP%')::text,
  round(sum(iff(cog='Y' and coalesce(chp_units,0)=0 and SECTOR_NAME ilike '%Non-CHP%', op_mw, 0)))::text, count_if(cog='Y' and units is null)::text, null, null, null, null from j
union all
select 'docket_summary', count(*)::text, count_if(plants>1)::text, max(plants)::text, null, null, null, null, null, null from d
union all
select * from (select 'spp_big', PLANT_NAME, UTILITY_NAME, STATE, fuel, round(op_mw)::text, first_yr::text, spp_dk, (select max(plants) from d where d.dk=j.spp_dk)::text, SECTOR_NAME
  from j where spp='Y' and op_mw>80 order by op_mw desc limit 25)
union all
select * from (select 'cog_nochp', PLANT_NAME, UTILITY_NAME, STATE, fuel, round(op_mw)::text, first_yr::text, cog_dk, (select max(plants) from d where d.dk=j.cog_dk)::text, SECTOR_NAME
  from j where cog='Y' and coalesce(chp_units,0)=0 and SECTOR_NAME ilike '%Non-CHP%' order by op_mw desc nulls last limit 25)
union all
select * from (select 'docket_multi', dk, null, null, null, plants::text, null, null, null, null from d where plants>1 order by plants desc limit 10)
