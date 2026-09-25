-- EPA informal: what the 2025-2026 Region 6 drinking-water notices (SFDW) are about. PWSID join to SDWIS violations with a federal enforcement action dated 2024 on
with p as (select distinct PGM_SYS_ID pwsid from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
           where year(ACHIEVED_DATE) >= 2025 and left(ENF_IDENTIFIER,2) = '06' and PGM_SYS_ACRNM = 'SFDW'),
v as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
      where PWSID in (select pwsid from p) and ENFORCEMENT_DATE >= '2024-01-01')
select 'sum' k, null a, null b, null c, (select count(*) from p) n1, count(distinct PWSID) n2, count(*) n3, count_if(ENF_ORIGINATOR_CODE = 'F') n4
from v
union all
select 'rule_viol', RULE_CODE, VIOLATION_CODE, ENF_ORIGINATOR_CODE, count(distinct PWSID), count(distinct VIOLATION_ID), count(*), count_if(IS_HEALTH_BASED_IND = 'Y')
from v where ENF_ORIGINATOR_CODE = 'F' group by 2, 3, 4 qualify row_number() over (order by count(distinct PWSID) desc) <= 12
union all
select 'enf_type', ENFORCEMENT_ACTION_TYPE_CODE, year(ENFORCEMENT_DATE)::text, ENF_ORIGINATOR_CODE, count(distinct PWSID), count(distinct ENFORCEMENT_ID), count(*), null
from v group by 2, 3, 4 qualify row_number() over (order by count(distinct PWSID) desc) <= 12
order by 1, 5 desc
