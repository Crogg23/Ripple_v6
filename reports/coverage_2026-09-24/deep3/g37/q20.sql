-- ICIS-Air peer check: facilities flagged Unaddressed HPV today (facility table CURRENT_HPV), per state,
-- against operating Title V sources and all operating facilities from the programs table; plus the national CURRENT_HPV value list
with p as (select PGM_SYS_ID, max(iff(PROGRAM_CODE = 'CAATVP' and AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) tv_opr,
             max(iff(AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) any_opr
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS group by 1),
f as (select PGM_SYS_ID, any_value(STATE) st, any_value(CURRENT_HPV) chpv from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES group by 1),
j as (select f.*, coalesce(p.tv_opr, 0) tv_opr, coalesce(p.any_opr, 0) any_opr from f left join p on f.PGM_SYS_ID = p.PGM_SYS_ID)
select 'state' k, st a, count_if(tv_opr = 1) tv_opr, count_if(any_opr = 1) any_opr, count_if(chpv ilike 'Unaddressed%') unaddr,
  count_if(chpv ilike 'Unaddressed%' and tv_opr = 1) unaddr_tv, count_if(chpv ilike 'Unaddressed-State%') unaddr_state,
  count_if(chpv ilike 'Unaddressed%' and any_opr = 0) unaddr_not_operating, count_if(chpv ilike 'Addressed%') addressed
from j group by 2 having count_if(chpv ilike 'Unaddressed%') > 0 or st in ('TX', 'PA', 'OH', 'IN', 'IA', 'KS', 'MO', 'SD', 'MN')
union all
select 'value', chpv, count(*), count_if(tv_opr = 1), count_if(any_opr = 1), null, null, null, null from j group by 2
order by 1, 5 desc;
