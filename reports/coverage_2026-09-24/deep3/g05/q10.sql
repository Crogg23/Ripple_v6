-- HHA owners at the addresses with 8+ organizations (HOME_HEALTH_OWNERS by ENROLLMENT_ID): do the agencies share owners?
with t as (select ENROLLMENT_ID, CCN, ORGANIZATION_NAME,
             upper(regexp_replace(trim(ADDRESS_LINE_1),'[^A-Za-z0-9 ]','')) a1, left(ZIP_CODE,5) z, ADDRESS_LINE_2, ASSOCIATE_ID
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
g as (select a1, z from t group by 1,2 having count(distinct ASSOCIATE_ID)>=8),
tc as (select t.* from t join g using (a1, z)),
o as (select ENROLLMENT_ID, ASSOCIATE_ID_OWNER, TYPE_OWNER, OWNER_NAME, ROLE_TEXT_OWNER, PERCENTAGE_OWNERSHIP from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_OWNERS),
jo as (select tc.a1, tc.z, tc.ENROLLMENT_ID, o.ASSOCIATE_ID_OWNER, o.TYPE_OWNER, o.OWNER_NAME, o.ROLE_TEXT_OWNER from tc join o using (ENROLLMENT_ID)),
own_anywhere as (select ASSOCIATE_ID_OWNER, count(distinct ENROLLMENT_ID) n_any from o group by 1),
peraddr as (select a1, z, count(distinct ENROLLMENT_ID) agencies_with_owner_rows, count(distinct ASSOCIATE_ID_OWNER) owners,
   count(distinct iff(TYPE_OWNER='I', ASSOCIATE_ID_OWNER, null)) indiv_owners from jo group by 1,2),
shared as (select a1, z, ASSOCIATE_ID_OWNER, any_value(OWNER_NAME) nm, any_value(TYPE_OWNER) ty, count(distinct ENROLLMENT_ID) n_here from jo group by 1,2,3 having count(distinct ENROLLMENT_ID)>=2)
select 'addr' k, g.a1||' '||g.z a, (select count(*) from tc where tc.a1=g.a1 and tc.z=g.z)::text b,
  (select count(distinct ADDRESS_LINE_2) from tc where tc.a1=g.a1 and tc.z=g.z)::text c,
  p.agencies_with_owner_rows::text d, p.owners::text e, p.indiv_owners::text f,
  (select count(*) from shared s where s.a1=g.a1 and s.z=g.z)::text g2,
  (select max(n_here) from shared s where s.a1=g.a1 and s.z=g.z)::text h
from g left join peraddr p using (a1, z)
union all
select * from (select 'owner', s.a1||' '||s.z, s.nm, s.ty, s.n_here::text, oa.n_any::text, null, null, null
  from shared s join own_anywhere oa using (ASSOCIATE_ID_OWNER) order by s.n_here desc, oa.n_any desc limit 20)
