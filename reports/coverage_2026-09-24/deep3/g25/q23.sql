-- EPA informal: Osage-county well set, month by month 2024-01 to 2026-07: notices vs EPA inspections; plus null-dated notices that could hide 2025 actions
with w as (select distinct REGISTRY_ID from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
           where left(ENF_IDENTIFIER,2) = '06' and STATUTE = 'SDWA' and PGM_SYS_ACRNM = 'ICIS'),
n as (select date_trunc('month', ACHIEVED_DATE)::date mo, count(distinct ENF_IDENTIFIER) notices
      from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS where REGISTRY_ID in (select REGISTRY_ID from w) group by 1),
i as (select date_trunc('month', ACTUAL_BEGIN_DATE)::date mo, count(distinct ACTIVITY_ID) insp, count(distinct REGISTRY_ID) wells
      from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS where REGISTRY_ID in (select REGISTRY_ID from w) group by 1)
select 'month' k, coalesce(n.mo, i.mo)::text mo, n.notices, i.insp, i.wells
from n full outer join i on i.mo = n.mo where coalesce(n.mo, i.mo) >= '2024-01-01'
union all
select 'nulldate', ENF_TYPE_DESC, count(*), count(distinct ENF_IDENTIFIER), count(distinct REGISTRY_ID)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS where REGISTRY_ID in (select REGISTRY_ID from w) and ACHIEVED_DATE is null group by 2
union all
select 'idyear', split_part(ENF_IDENTIFIER, '-', 2), count(*), count(distinct ENF_IDENTIFIER), count_if(ACHIEVED_DATE is null)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS where REGISTRY_ID in (select REGISTRY_ID from w) and split_part(ENF_IDENTIFIER, '-', 2) >= '2022' group by 2
order by 1, 2
