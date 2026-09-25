-- SDWA geographic areas: confirm it is a crosswalk; area types, fill by type, rows per system, coverage of active community systems
with g as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS),
p as (select PWSID, PWS_TYPE_CODE, PWS_ACTIVITY_CODE, POPULATION_SERVED_COUNT from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS),
gc as (select PWSID, count_if(AREA_TYPE_CODE = 'CN') cn, count(*) n from g group by 1)
select 'atype' k, AREA_TYPE_CODE a, count(*) b, count(distinct PWSID) c, count_if(nullif(trim(COUNTY_FIPS), '') is not null) d, count_if(ZIP_CODE_SERVED is not null) e, count_if(CITY_SERVED is not null) f from g group by 2
union all select 'quarter', SUBMISSIONYEARQUARTER, count(*), count(distinct PWSID), count(distinct GEO_ID), min(year(LAST_REPORTED_DATE)), max(year(LAST_REPORTED_DATE)) from g group by 2
union all select 'cws_cover', p.PWS_TYPE_CODE || '/' || p.PWS_ACTIVITY_CODE, count(*), count_if(gc.PWSID is not null), count_if(gc.cn > 0), sum(p.POPULATION_SERVED_COUNT), sum(iff(gc.cn > 0, p.POPULATION_SERVED_COUNT, 0)) from p left join gc on p.PWSID = gc.PWSID group by 2
union all select 'orphans', 'geo pwsid not in pws', count(distinct gc.PWSID), null, null, null, null from gc left join p on gc.PWSID = p.PWSID where p.PWSID is null;
