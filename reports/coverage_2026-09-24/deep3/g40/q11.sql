-- RCRA NAICS: keys, duplicates, code lengths, and what share of each state's RCRA sites carry any industry code
with n as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_RCRA_NAICS),
f as (select ACTIVITY_LOCATION st, ID_NUMBER from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_FACILITIES group by 1,2),
ns as (select distinct ID_NUMBER from n)
select 'profile' k, count(*)::text a, count(distinct ID_NUMBER)::text b, count(distinct FACILITY_NAICS_ID)::text c,
  count(distinct ID_NUMBER||'|'||NAICS_CODE)::text d, count(distinct _SOURCE_RUN_ID)::text e,
  count_if(NAICS_CODE is null or trim(NAICS_CODE)='')::text f, count_if(ACTIVITY_LOCATION <> left(ID_NUMBER,2))::text g,
  (select count(*) from ns where ID_NUMBER in (select ID_NUMBER from f))::text h
from n
union all select 'len', length(NAICS_CODE)::text, count(*)::text, count(distinct NAICS_CODE)::text, left(listagg(distinct NAICS_CODE,' '),60), null, null, null, null from n group by 2
union all select * from (select 'state', f.st, count(*)::text, count_if(ns.ID_NUMBER is not null)::text,
  round(100*count_if(ns.ID_NUMBER is not null)/count(*),1)::text, null, null, null, null
  from f left join ns using (ID_NUMBER) group by 2 order by count(*) desc limit 25)
union all select * from (select 'codes_per_site', c::text, count(*)::text, null, null, null, null, null, null
  from (select ID_NUMBER, count(*) c from n group by 1) group by 2 order by 2::int limit 8)
