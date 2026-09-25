-- owner claim re-check: reach by owner NAME (upper bound, name-only) vs by ASSOCIATE_ID_OWNER, Valley 2019+ vs rest 2019+
with e as (select ENROLLMENT_ID, STATE, left(trim(ZIP_CODE),3) z3, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') d
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
o as (select ENROLLMENT_ID, ASSOCIATE_ID_OWNER, upper(trim(OWNER_NAME)) nm from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_OWNERS where TYPE_OWNER='I'),
rn as (select nm, count(distinct ENROLLMENT_ID) n_nm, count(distinct ASSOCIATE_ID_OWNER) ids from o group by 1),
ri as (select ASSOCIATE_ID_OWNER, count(distinct ENROLLMENT_ID) n_id from o group by 1),
v as (select e.*, iff(STATE='CA' and z3 between '912' and '916','valley','rest') rg from e where year(d)>=2019),
jo as (select v.rg, v.ENROLLMENT_ID, o.nm, o.ASSOCIATE_ID_OWNER, rn.n_nm, rn.ids, ri.n_id from v join o using (ENROLLMENT_ID) join rn using (nm) join ri using (ASSOCIATE_ID_OWNER)),
per as (select rg, ENROLLMENT_ID, count(distinct ASSOCIATE_ID_OWNER) owners, max(n_id) mx_id, max(n_nm) mx_nm from jo group by 1,2)
select 'grp' k, rg a, count(*) n, median(owners) med_owners, count_if(mx_id>=3) reach3_id, count_if(mx_nm>=3) reach3_name, round(100*count_if(mx_nm>=3)/count(*),1) pct_name from per group by 2
union all select 'names_on_2plus_ids', null, count(*), null, null, null, null from rn where ids>1
union all select * from (select 'top_valley_name', nm, count(distinct ENROLLMENT_ID), max(n_nm), max(ids), null, null from jo where rg='valley' group by nm order by 3 desc, 4 desc limit 8)
