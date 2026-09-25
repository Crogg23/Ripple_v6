-- HHA vs hospice enrollments: same street address + ZIP (two fields agree) at the biggest HHA clusters; and share of each file's 2019+ enrollments in LA-area ZIP3s
with norm as (select 'HHA' src, upper(regexp_replace(trim(ADDRESS_LINE_1),'[^A-Za-z0-9 ]','')) a1, left(ZIP_CODE,5) z, left(ZIP_CODE,3) z3, STATE, ASSOCIATE_ID,
                try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enr_dt from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS
              union all
              select 'HOSPICE', upper(regexp_replace(trim(ADDRESS_LINE_1),'[^A-Za-z0-9 ]','')), left(ZIP_CODE,5), left(ZIP_CODE,3), STATE, ASSOCIATE_ID,
                try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS),
n2 as (select *, (STATE='CA' and (z3 between '900' and '916' or z3 in ('918','935'))) la from norm),
top as (select a1, z from n2 where src='HHA' group by 1,2 order by count(distinct ASSOCIATE_ID) desc limit 12)
select 'addr' k, top.a1||' '||top.z a, count_if(src='HHA') hha, count_if(src='HOSPICE') hospice, null d, null e, null f
from top join n2 using (a1, z) group by 2
union all select 'share', src, count(*), count_if(year(enr_dt)>=2019), count_if(la and year(enr_dt)>=2019), count_if(la and year(enr_dt)<2013), count_if(year(enr_dt)<2013) from n2 group by 2
order by 1, 3 desc
