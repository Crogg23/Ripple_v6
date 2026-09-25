-- EPA informal: the 2025-2026 jumps. Region 6 SFDW drinking-water notices and Region 5 FIFRA warning letters: who, where, on how many days
with x as (select i.*, case when left(ENF_IDENTIFIER,2)='06' and PGM_SYS_ACRNM='SFDW' then 'R6 SFDW' else 'R5 FIFRA' end grp
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS i
  where year(ACHIEVED_DATE) >= 2025 and ((left(ENF_IDENTIFIER,2)='06' and PGM_SYS_ACRNM='SFDW') or (left(ENF_IDENTIFIER,2)='05' and STATUTE='FIFRA'))),
e as (select FRS_ID, max(FACILITY_NAME) nm, max(STATE) st, max(IS_ON_TRIBAL_LAND::int) tribal from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO
  where FRS_ID in (select REGISTRY_ID from x) group by 1)
select 'grp' k, grp a, null b, count(*) n, count(distinct ENF_IDENTIFIER) ids, count(distinct REGISTRY_ID) facs, count(distinct ACHIEVED_DATE) days,
  count(e.FRS_ID) echo_hit, sum(e.tribal) tribal, max(ACHIEVED_DATE)::text dmax
from x left join e on e.FRS_ID = x.REGISTRY_ID group by 2
union all
select 'st', grp, e.st, count(*), count(distinct ENF_IDENTIFIER), count(distinct REGISTRY_ID), count(distinct ACHIEVED_DATE), null, sum(e.tribal), null
from x left join e on e.FRS_ID = x.REGISTRY_ID group by 2, 3
union all
select 'day', grp, ACHIEVED_DATE::text, count(*), count(distinct ENF_IDENTIFIER), count(distinct REGISTRY_ID), null, null, null, null
from x group by 2, 3 qualify row_number() over (partition by grp order by count(*) desc) <= 5
union all
select 'name', grp, e.nm, count(*), count(distinct ENF_IDENTIFIER), count(distinct REGISTRY_ID), null, null, max(e.tribal), max(x.PGM_SYS_ID)
from x left join e on e.FRS_ID = x.REGISTRY_ID group by 2, 3 qualify row_number() over (partition by grp order by count(*) desc) <= 8
order by 1, 2, 4 desc
