-- SDWA peer test: mobile home park (MH+MP) vs other residential community systems, and schools/daycares vs other non-transient systems; active groundwater systems; health-based and monitoring violations with compliance periods starting 2021-2025, deduped by VIOLATION_ID
with sa as (select PWSID, min(SERVICE_AREA_TYPE_CODE) code from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EPA_SDWA_SDWA_SERVICE_AREAS where IS_PRIMARY_SERVICE_AREA_CODE = 'Y' group by 1 having count(*) = 1),
p as (select PWSID, PWS_TYPE_CODE, POPULATION_SERVED_COUNT pop, OWNER_TYPE_CODE from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS where PWS_ACTIVITY_CODE = 'A' and GW_SW_CODE = 'GW'),
v as (select PWSID, count(distinct iff(IS_HEALTH_BASED_IND = 'Y', VIOLATION_ID, null)) hb, count(distinct iff(VIOLATION_CATEGORY_CODE in ('MR', 'MON'), VIOLATION_ID, null)) mr
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
      where COMPL_PER_BEGIN_DATE >= '2021-01-01' and COMPL_PER_BEGIN_DATE < '2026-01-01' and VIOLATION_ID is not null group by 1),
x as (select p.*, case when sa.code in ('MH', 'MP') then 'MHP' when sa.code in ('RA', 'SU', 'HA', 'OR', 'MU') then 'RES' else sa.code end grp,
        iff(OWNER_TYPE_CODE = 'P', 'private', 'other') own,
        case when pop <= 100 then 'a 25-100' when pop <= 500 then 'b 101-500' when pop <= 3300 then 'c 501-3300' else 'd 3301+' end band,
        coalesce(v.hb, 0) hb, coalesce(v.mr, 0) mr
      from p join sa on sa.PWSID = p.PWSID left join v on v.PWSID = p.PWSID)
select PWS_TYPE_CODE, grp, iff(PWS_TYPE_CODE = 'CWS', own, 'all') own, band, count(*) systems, sum(pop) people,
  count_if(hb > 0) any_hb, round(100 * count_if(hb > 0) / count(*), 1) pct_hb, sum(hb) hb_viol, count_if(mr > 0) any_mr, round(100 * count_if(mr > 0) / count(*), 1) pct_mr
from x where (PWS_TYPE_CODE = 'CWS' and grp in ('MHP', 'RES')) or (PWS_TYPE_CODE = 'NTNCWS' and grp in ('SC', 'DC', 'IA', 'ON', 'OA', 'MF'))
group by 1, 2, 3, 4 order by 1, 4, 3, 2
