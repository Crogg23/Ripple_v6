-- HHA: new Medicare enrollments per year (date inside ENROLLMENT_ID), in the six 2013-2019 moratorium metros (approx by ZIP3), LA County (approx ZIP3), and the rest
with t as (select try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enr_dt, left(ZIP_CODE,3) z3, STATE, INCORPORATION_DATE
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
r as (select *, case
   when STATE='FL' and z3 in ('330','331','332','333') then 'MIA_FTL'
   when STATE='IL' and z3 between '600' and '608' then 'CHICAGO'
   when STATE='TX' and z3 in ('770','772','773','774','775') then 'HOUSTON'
   when STATE='TX' and z3 in ('750','751','752','753','760','761','762') then 'DALLAS'
   when STATE='MI' and z3 between '480' and '483' then 'DETROIT'
   when STATE='CA' and (z3 between '900' and '916' or z3 in ('918','935')) then 'LA_COUNTY'
   else 'REST' end rg from t)
select year(enr_dt) yr,
  count_if(rg='MIA_FTL') mia_ftl, count_if(rg='CHICAGO') chicago, count_if(rg='HOUSTON') houston, count_if(rg='DALLAS') dallas, count_if(rg='DETROIT') detroit,
  count_if(rg='LA_COUNTY') la_county, count_if(rg='REST') rest, count(*) total,
  count_if(enr_dt is null) bad_id, count_if(year(INCORPORATION_DATE)=year(enr_dt)) inc_same_yr
from r group by 1 order by 1
