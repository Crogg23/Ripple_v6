-- SDWA service areas: shape, codes x primary flag, duplicates, orphans vs PUB_WATER_SYSTEMS, primaries per system, sibling tables named like it
with t as (select * from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EPA_SDWA_SDWA_SERVICE_AREAS),
p as (select PWSID, PWS_TYPE_CODE, PWS_ACTIVITY_CODE from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS)
select 'profile' k, count(*)::text a, count(distinct PWSID)::text b, count(distinct PWSID||'|'||SERVICE_AREA_TYPE_CODE)::text c, count(distinct SUBMISSIONYEARQUARTER)::text d, min(FIRST_REPORTED_DATE)::text e, max(LAST_REPORTED_DATE)::text f from t
union all select 'orphans', count(*)::text, count(distinct t.PWSID)::text, null, null, null, null from t left join p on p.PWSID = t.PWSID where p.PWSID is null
union all select 'pws_total_active_without_sa', count(*)::text, count_if(PWS_ACTIVITY_CODE = 'A')::text, count_if(PWS_ACTIVITY_CODE = 'A' and PWSID not in (select PWSID from t))::text, count_if(PWSID not in (select PWSID from t))::text, null, null from p
union all select * from (select 'code', SERVICE_AREA_TYPE_CODE, count(*)::text, count_if(IS_PRIMARY_SERVICE_AREA_CODE = 'Y')::text, count_if(IS_PRIMARY_SERVICE_AREA_CODE = 'N')::text, count_if(IS_PRIMARY_SERVICE_AREA_CODE is null or trim(IS_PRIMARY_SERVICE_AREA_CODE) = '')::text, count(distinct PWSID)::text from t group by 2 order by count(*) desc limit 60)
union all select 'primaries_per_pws', n::text, count(*)::text, null, null, null, null from (select PWSID, count_if(IS_PRIMARY_SERVICE_AREA_CODE = 'Y') n from t group by 1) group by 2
union all select 'sibling', TABLE_CATALOG||'.'||TABLE_SCHEMA||'.'||TABLE_NAME, ROW_COUNT::text, null, null, null, null from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES where TABLE_NAME ilike '%SERVICE_AREA%'
