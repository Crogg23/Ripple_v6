-- SDWA inside North Carolina and Texas (the two biggest mobile-home-park gaps): split by operator size (systems per ORG_NAME in the peer set) to test the dull reason (big professional operators run the subdivisions); plus top rules behind MHP health violations
with sa as (select PWSID, min(SERVICE_AREA_TYPE_CODE) code from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EPA_SDWA_SDWA_SERVICE_AREAS where IS_PRIMARY_SERVICE_AREA_CODE = 'Y' group by 1 having count(*) = 1),
p as (select PWSID, PRIMACY_AGENCY_CODE st, upper(trim(ORG_NAME)) org from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS
      where PWS_ACTIVITY_CODE = 'A' and GW_SW_CODE = 'GW' and PWS_TYPE_CODE = 'CWS' and OWNER_TYPE_CODE = 'P' and POPULATION_SERVED_COUNT between 25 and 500 and PRIMACY_AGENCY_CODE in ('NC', 'TX')),
vv as (select PWSID, VIOLATION_ID, RULE_CODE, CONTAMINANT_CODE from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
      where COMPL_PER_BEGIN_DATE >= '2021-01-01' and COMPL_PER_BEGIN_DATE < '2026-01-01' and VIOLATION_ID is not null and IS_HEALTH_BASED_IND = 'Y' and (PWSID like 'NC%' or PWSID like 'TX%')),
v as (select PWSID, count(distinct VIOLATION_ID) hb from vv group by 1),
x as (select p.*, iff(sa.code in ('MH', 'MP'), 'MHP', 'RES') grp, coalesce(v.hb, 0) hb, count(*) over (partition by p.st, p.org) org_n
      from p join sa on sa.PWSID = p.PWSID left join v on v.PWSID = p.PWSID where sa.code in ('MH', 'MP', 'RA', 'SU', 'HA', 'OR', 'MU'))
select 'split' k, st, grp, iff(org_n >= 10, 'operator with 10+ systems', 'operator with <10') a, count(*)::text b, count_if(hb > 0)::text c, round(100 * count_if(hb > 0) / count(*), 1)::text d from x group by 2, 3, 4
union all select * from (select 'top_org', st, grp, org, count(*)::text, count_if(hb > 0)::text, sum(hb)::text from x group by 2, 3, 4 order by count(*) desc limit 16)
union all select * from (select 'mhp_rules', x.st, vv.RULE_CODE, vv.CONTAMINANT_CODE, count(distinct vv.PWSID||vv.VIOLATION_ID)::text, count(distinct vv.PWSID)::text, null from x join vv on vv.PWSID = x.PWSID where x.grp = 'MHP' group by 2, 3, 4 order by count(distinct vv.PWSID) desc limit 12)
