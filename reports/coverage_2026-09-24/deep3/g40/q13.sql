-- OWID CO2: duplicates, text-number parse, zeros, repeated values, which rows are regions not countries
with o as (select ENTITY, CODE, YEAR, ANNUAL_CO_EMISSIONS v, try_to_number(YEAR) y, try_to_double(ANNUAL_CO_EMISSIONS) x from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_OWID_CO2)
select 'profile' k, count(*)::text a, count(distinct ENTITY)::text b, count(distinct ENTITY||'|'||YEAR)::text c,
  min(y)::text||'..'||max(y)::text d, count_if(y is null)::text e, count_if(x is null and v is not null)::text f,
  count_if(x=0)::text||' zero / '||count_if(x<0)::text||' neg' g, count_if(CODE is null or trim(CODE)='')::text h, count_if(CODE like 'OWID%')::text i
from o
union all select * from (select 'repeat', v, count(*)::text, count(distinct ENTITY)::text, min(y)::text||'..'||max(y)::text, left(listagg(distinct ENTITY,'|'),80), null, null, null, null
  from o group by 2 order by count(*) desc limit 6)
union all select * from (select 'nocode', ENTITY, count(*)::text, min(y)::text||'..'||max(y)::text, null, null, null, null, null, null from o where CODE is null or trim(CODE)='' group by 2 order by 2 limit 40)
union all select * from (select 'owid', ENTITY, CODE, count(*)::text, null, null, null, null, null, null from o where CODE like 'OWID%' group by 2,3 order by 2)
