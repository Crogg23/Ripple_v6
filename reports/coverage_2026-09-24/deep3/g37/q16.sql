-- ICIS-Air eyeball: Nebraska's 2019-2022 HPVs (who found them, dates, programs, status), Nebraska and Wisconsin formal actions by year,
-- and which states the bulk BEGIN_DATE values belong to
with v as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY where ENF_RESPONSE_POLICY_CODE = 'HPV'),
f as (select PGM_SYS_ID, any_value(STATE) st, any_value(FACILITY_NAME) nm, any_value(CITY) city, any_value(CURRENT_HPV) chpv, any_value(NAICS_CODES) naics
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES group by 1),
p as (select PGM_SYS_ID, listagg(distinct PROGRAM_CODE || ':' || AIR_OPERATING_STATUS_CODE, ',') within group (order by PROGRAM_CODE || ':' || AIR_OPERATING_STATUS_CODE) pgms
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS group by 1),
a as (select a.*, f.st from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS a left join f on a.PGM_SYS_ID = f.PGM_SYS_ID)
select * from (select 'ne_hpv' k, v.PGM_SYS_ID a, f.nm b, f.city || ' / ' || coalesce(f.naics, '') c, v.AGENCY_TYPE_DESC d, v.HPV_DAYZERO_DATE::text e,
  coalesce(v.HPV_RESOLVED_DATE::text, 'open') g, left(v.PROGRAM_DESCS, 60) || ' | ' || left(coalesce(v.POLLUTANT_DESCS, ''), 40) h, p.pgms || ' | hpv=' || coalesce(f.chpv, '') i
  from v left join f on v.PGM_SYS_ID = f.PGM_SYS_ID left join p on v.PGM_SYS_ID = p.PGM_SYS_ID
  where f.st = 'NE' and v.HPV_DAYZERO_DATE >= '2015-01-01' order by v.HPV_DAYZERO_DATE limit 45)
union all
select 'fa_by_year', st, year(SETTLEMENT_ENTERED_DATE)::text, count(*)::text, count(distinct PGM_SYS_ID)::text, sum(coalesce(PENALTY_AMOUNT, 0))::text, listagg(distinct STATE_EPA_FLAG, ','), null, null
from a where st in ('NE', 'WI') and (SETTLEMENT_ENTERED_DATE >= '2015-01-01' or SETTLEMENT_ENTERED_DATE is null) group by 2, 3
union all
select * from (select 'bulkdate', pr.BEGIN_DATE, f.st, count(*)::text, count(distinct pr.PGM_SYS_ID)::text, listagg(distinct pr.PROGRAM_CODE, ',') within group (order by pr.PROGRAM_CODE), null, null, null
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS pr left join f on pr.PGM_SYS_ID = f.PGM_SYS_ID
  where pr.BEGIN_DATE in ('09/29/2025', '03/19/2026', '10/27/2015', '01/01/1969') group by 2, 3 qualify row_number() over (partition by pr.BEGIN_DATE order by count(*) desc) <= 3);
