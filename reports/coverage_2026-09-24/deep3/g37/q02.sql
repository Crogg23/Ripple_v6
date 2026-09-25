-- NPDES quarterly noncompliance history: quarters covered, HLRNC codes, how many rows carry effluent violations
with q as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY)
select 'qtr' k, YEARQTR a, count(*) n, count(distinct NPDES_ID) m, count_if(try_to_number(NUME90_Q)>0) x, count_if(HLRNC in ('S','E')) y from q group by 2
union all select 'hlrnc', HLRNC, count(*), count(distinct NPDES_ID), count_if(try_to_number(NUME90_Q)>0), count_if(try_to_number(NUMD8090_Q)>0) from q group by 2
union all select 'e90vals', case when NUME90_Q is null then 'null' when try_to_number(NUME90_Q) is null then 'text:'||left(NUME90_Q,10) else 'num' end, count(*), max(try_to_number(NUME90_Q)), null, null from q group by 2
order by 1, 2;
