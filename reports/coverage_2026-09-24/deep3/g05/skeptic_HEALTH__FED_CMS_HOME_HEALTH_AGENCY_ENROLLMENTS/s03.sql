-- median unit: how spread out are the 1,259 Valley 2019+ agencies across addresses and ZIP5s; what do the top 3/10 addresses carry
with t as (select upper(regexp_replace(trim(ADDRESS_LINE_1),'[^A-Za-z0-9 ]','')) a1, left(trim(ZIP_CODE),5) z, ASSOCIATE_ID, STATE, left(trim(ZIP_CODE),3) z3,
             try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') d
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
g as (select a1, z, count(distinct ASSOCIATE_ID) orgs from t group by 1,2),
v as (select t.*, g.orgs, iff(STATE='CA' and z3 between '912' and '916','valley','rest') rg from t join g using (a1,z) where year(d)>=2019),
va as (select rg, a1, z, count(*) n from v group by 1,2,3),
rk as (select va.*, row_number() over (partition by rg order by n desc) r from va)
select 'addr_view' k, rg, (select count(*) from v v2 where v2.rg=rk.rg) agencies, count(*) addresses, count(distinct z) zip5s, median(n) med_per_addr,
  sum(iff(r<=3,n,0)) top3, sum(iff(r<=10,n,0)) top10, sum(iff(r<=50,n,0)) top50, count_if(n=1) solo_addr
from rk group by 2
union all
select 'agency_view', rg, count(*), median(orgs), count_if(orgs=1), count_if(orgs>=3), count_if(orgs>=10), null, null, null from v group by 2
