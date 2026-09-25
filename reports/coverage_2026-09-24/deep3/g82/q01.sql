-- MSHA mines: profile. Keys, status values, active flag agreement, coords, quoted-value trap, employees
select 'profile' k, count(*)::text a, count(distinct MINE_ID)::text b, count_if(MINE_ID like '"%')::text c,
  count_if(LATITUDE is null or LATITUDE=0)::text d, count_if(LONGITUDE>0)::text e,
  sum(NO_EMPLOYEES)::text f, count_if(IS_ACTIVE)::text g, min(CURRENT_STATUS_DT)::text h, max(CURRENT_STATUS_DT)::text i,
  count(distinct CURRENT_CONTROLLER_ID)::text j, count(distinct CURRENT_OPERATOR_ID)::text l
from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES
union all
select 'status', CURRENT_MINE_STATUS, count(*)::text, count_if(IS_ACTIVE)::text, count_if(COAL_METAL_IND='C')::text,
  count_if(NO_EMPLOYEES>0)::text, sum(NO_EMPLOYEES)::text, count_if(DAYS_PER_WEEK>0)::text,
  min(CURRENT_STATUS_DT)::text, max(CURRENT_STATUS_DT)::text, median(datediff('day',CURRENT_STATUS_DT,'2026-07-17'::date))::text, null
from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES group by 2
union all
select 'type', CURRENT_MINE_TYPE, count(*)::text, count_if(IS_ACTIVE)::text, null,null,null,null,null,null,null,null
from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES group by 2
union all
select 'statusdt_top', CURRENT_STATUS_DT::text, count(*)::text, null,null,null,null,null,null,null,null,null
from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES group by 2 qualify row_number() over (order by count(*) desc) <= 6
