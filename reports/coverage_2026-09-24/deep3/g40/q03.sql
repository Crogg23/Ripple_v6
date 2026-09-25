-- Time: informal (ACHIEVED_DATE) and formal (SETTLEMENT_ENTERED_DATE) air actions per year by agency, full year and Jan-Jul only
with i as (select year(ACHIEVED_DATE) y, STATE_EPA_FLAG f, count(distinct ACTIVITY_ID) inf_acts, count(*) inf_rows,
             count(distinct iff(month(ACHIEVED_DATE)<=7, ACTIVITY_ID, null)) inf_jj
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
           where ACHIEVED_DATE between '2005-01-01' and '2026-07-31' group by 1,2),
fa as (select year(SETTLEMENT_ENTERED_DATE) y, STATE_EPA_FLAG f, count(distinct ACTIVITY_ID) f_acts,
             count(distinct iff(month(SETTLEMENT_ENTERED_DATE)<=7, ACTIVITY_ID, null)) f_jj,
             sum(iff(month(SETTLEMENT_ENTERED_DATE)<=7, PENALTY_AMOUNT, 0)) f_pen_jj, max(SETTLEMENT_ENTERED_DATE) fmax
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS
           where SETTLEMENT_ENTERED_DATE between '2005-01-01' and '2026-09-24' group by 1,2)
select coalesce(i.y,fa.y) y, coalesce(i.f,fa.f) f, inf_acts, inf_rows, inf_jj, f_acts, f_jj, round(f_pen_jj) f_pen_jj, fmax
from i full outer join fa on i.y=fa.y and i.f=fa.f
order by 2,1
