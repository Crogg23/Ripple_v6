-- HHA owners behind 2019+ enrollments (HOME_HEALTH_OWNERS by ENROLLMENT_ID): Valley/Glendale/Burbank ZIP3 912-916 vs rest of US; how many agencies sit with an individual owner who holds 3+ agencies anywhere
with t as (select ENROLLMENT_ID, STATE, left(ZIP_CODE,3) z3, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enr_dt
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
o as (select ENROLLMENT_ID, ASSOCIATE_ID_OWNER, TYPE_OWNER, OWNER_NAME, ROLE_TEXT_OWNER from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_OWNERS),
reach as (select ASSOCIATE_ID_OWNER, count(distinct ENROLLMENT_ID) n_agencies from o where TYPE_OWNER='I' group by 1),
nt as (select t.*, iff(STATE='CA' and z3 between '912' and '916','valley','restUS') rg from t where year(enr_dt)>=2019),
jo as (select nt.rg, nt.ENROLLMENT_ID, o.ASSOCIATE_ID_OWNER, o.OWNER_NAME, r.n_agencies from nt join o using (ENROLLMENT_ID) join reach r using (ASSOCIATE_ID_OWNER) where o.TYPE_OWNER='I'),
per as (select rg, ENROLLMENT_ID, count(distinct ASSOCIATE_ID_OWNER) owners, max(n_agencies) max_reach from jo group by 1,2)
select 'grp' k, rg a, (select count(*) from nt where nt.rg=per.rg)::text b, count(*)::text c, round(median(owners),1)::text d,
  count_if(max_reach>=3)::text e, round(100*count_if(max_reach>=3)/count(*),1)::text f, null g
from per group by rg
union all select * from (select 'top_owner', any_value(OWNER_NAME), rg, count(distinct ENROLLMENT_ID)::text, max(n_agencies)::text, null, null, null
  from jo group by ASSOCIATE_ID_OWNER, rg order by count(distinct ENROLLMENT_ID) desc limit 12)
