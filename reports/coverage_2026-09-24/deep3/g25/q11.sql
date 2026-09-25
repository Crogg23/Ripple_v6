-- EPA informal: facilities with the most informal actions: name, state, span, statutes; ECHO formal actions and penalties; EPA formal case count
with i as (select REGISTRY_ID, count(*) n, count(distinct ENF_IDENTIFIER) ids, min(ACHIEVED_DATE) d0, max(ACHIEVED_DATE) d1,
  listagg(distinct STATUTE, ',') sts, listagg(distinct PGM_SYS_ACRNM, ',') pgms, count_if(ACHIEVED_DATE >= '2021-01-01') n_since21,
  max(left(ENF_IDENTIFIER,2)) reg
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS group by 1 order by n desc limit 30),
e as (select FRS_ID, max(FACILITY_NAME) nm, max(CITY) city, max(STATE) st, max(FORMAL_ACTION_COUNT) formal, max(TOTAL_PENALTIES) pen,
  max(INFORMAL_ACTION_COUNT) echo_inf, max(IS_ON_TRIBAL_LAND::int) tribal, max(HAS_DRINKING_WATER_PROGRAM::int) dw, count(*) echo_rows
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO where FRS_ID in (select REGISTRY_ID from i) group by 1),
c as (select REGISTRY_ID, count(distinct CASE_NUMBER) cases, max(FACILITY_NAME) cnm, max(STATE_CODE) cst
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES where REGISTRY_ID in (select REGISTRY_ID from i) group by 1)
select i.*, e.nm, e.city, e.st, e.formal, e.pen, e.echo_inf, e.tribal, e.dw, e.echo_rows, c.cases, c.cnm, c.cst
from i left join e on e.FRS_ID = i.REGISTRY_ID left join c on c.REGISTRY_ID = i.REGISTRY_ID order by i.n desc
