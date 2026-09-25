-- NPDES formal enforcement actions: dates, agencies, penalties; and informal actions by year, to know what "enforcement" can mean
with fa as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS),
ia as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS)
select 'formal' k, iff(year(SETTLEMENT_ENTERED_DATE) < 2010, '<2010', coalesce(year(SETTLEMENT_ENTERED_DATE)::text, 'null')) a, AGENCY b,
  count(*) n, count(distinct NPDES_ID) permits, count(distinct ENF_IDENTIFIER) cases,
  sum(coalesce(FED_PENALTY_ASSESSED_AMT, 0)) fed_pen, sum(coalesce(STATE_LOCAL_PENALTY_AMT, 0)) st_pen, max(STATE_LOCAL_PENALTY_AMT) st_max
from fa group by 2, 3
union all
select 'informal', iff(year(ACHIEVED_DATE) < 2010, '<2010', coalesce(year(ACHIEVED_DATE)::text, 'null')), AGENCY, count(*), count(distinct NPDES_ID), count(distinct ENF_IDENTIFIER), null, null, null
from ia group by 2, 3
order by 1, 2, 3;
