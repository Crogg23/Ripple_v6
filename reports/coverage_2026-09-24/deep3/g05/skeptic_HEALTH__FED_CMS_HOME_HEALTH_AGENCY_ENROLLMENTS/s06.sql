-- exact same suite shared by 2+ organizations (address line 1 + line 2 + ZIP), Valley vs rest for 2019+; and the 9 Friar St hospices: distinct orgs, overlap with HHA orgs
with e as (select ASSOCIATE_ID, STATE, left(trim(ZIP_CODE),5) z, left(trim(ZIP_CODE),3) z3, upper(regexp_replace(trim(ADDRESS_LINE_1),'[^A-Za-z0-9 ]','')) a1,
             upper(regexp_replace(trim(coalesce(ADDRESS_LINE_2,'')),'[^A-Za-z0-9]','')) a2, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') d
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
su as (select a1, z, a2, count(distinct ASSOCIATE_ID) orgs from e where a2<>'' group by 1,2,3),
ev as (select e.*, su.orgs suite_orgs, iff(STATE='CA' and z3 between '912' and '916','valley','rest') rg from e left join su using (a1,z,a2)),
hf as (select ASSOCIATE_ID, ADDRESS_LINE_2, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') d from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS
       where upper(regexp_replace(trim(ADDRESS_LINE_1),'[^A-Za-z0-9 ]',''))='14545 FRIAR ST' and left(trim(ZIP_CODE),5)='91411')
select 'same_suite_2019on' k, rg a, count(*) n, count_if(suite_orgs>=2) x, count_if(a2='') y, null w from ev where year(d)>=2019 group by 2
union all select * from (select 'top_shared_suite', a1||' / '||a2||' / '||z, orgs, null, null, null from su where orgs>=2 order by orgs desc limit 8)
union all select 'friar_hospice', min(d)::text||'..'||max(d)::text, count(*), count(distinct ASSOCIATE_ID),
  count_if(ASSOCIATE_ID in (select ASSOCIATE_ID from e)), listagg(distinct ADDRESS_LINE_2, ',') from hf
