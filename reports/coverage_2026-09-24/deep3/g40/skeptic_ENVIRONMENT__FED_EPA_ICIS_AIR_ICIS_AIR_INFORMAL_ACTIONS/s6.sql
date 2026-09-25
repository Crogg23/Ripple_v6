-- What kinds of formal actions reach ICIS from Bay Area facilities since 2015, by agency: would a no-penalty abatement order ever show up?
with f as (select PGM_SYS_ID from {F} where LOCAL_CONTROL_REGION_NAME like 'Bay Area%'),
a1 as (select ACTIVITY_ID, any_value(STATE_EPA_FLAG) ag, any_value(ENF_TYPE_CODE) tc, any_value(ENF_TYPE_DESC) td, max(PENALTY_AMOUNT) pen, max(SETTLEMENT_ENTERED_DATE) d
   from {A} where PGM_SYS_ID in (select PGM_SYS_ID from f) group by 1)
select ag, tc, td, count(*) n, count_if(d>='2019-01-01') n19, count_if(coalesce(pen,0)=0) zero_pen, count_if(d is null) no_date, min(d) first_d, max(d) last_d
from a1 where d>='2015-01-01' or d is null group by 1,2,3 order by n desc
