-- ICIS-Air violation history joined to the programs table: HPV vs FRV rows by year, resolved share, and how many sit on operating Title V sources
with v as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY),
p as (select PGM_SYS_ID, max(iff(PROGRAM_CODE = 'CAATVP', 1, 0)) tv, max(iff(PROGRAM_CODE = 'CAATVP' and AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) tv_opr,
        max(iff(AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) any_opr, min(iff(AIR_OPERATING_STATUS_CODE = 'CLS', 1, 0)) all_cls
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS group by 1)
select v.ENF_RESPONSE_POLICY_CODE k, year(coalesce(v.HPV_DAYZERO_DATE, v.EARLIEST_FRV_DETERM_DATE)) yr, count(*) n, count(distinct v.PGM_SYS_ID) fac,
  count(distinct v.ACTIVITY_ID) acts, count_if(v.HPV_DAYZERO_DATE is not null) dz, count_if(v.HPV_RESOLVED_DATE is not null) resolved,
  count_if(p.PGM_SYS_ID is not null) in_programs, count_if(p.tv_opr = 1) on_tv_opr, count_if(p.all_cls = 1) on_all_closed,
  count(distinct v.STATE_CODE) states, min(v.AGENCY_TYPE_DESC) ag_min, max(v.AGENCY_TYPE_DESC) ag_max
from v left join p on v.PGM_SYS_ID = p.PGM_SYS_ID
group by 1, 2 order by 1, 2;
