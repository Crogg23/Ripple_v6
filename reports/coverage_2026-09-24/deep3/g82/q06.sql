-- MSHA mines: how long idle mines have been idle, which coal controllers hold the most long-idle mines, and idle share by state (peer)
with m as (select *, datediff('day', CURRENT_STATUS_DT, '2026-07-17'::date)/365.25 yrs,
             CURRENT_MINE_STATUS in ('Temporarily Idled','NonProducing') idle
           from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES)
select 'bucket' k, CURRENT_MINE_STATUS a, COAL_METAL_IND b,
  case when yrs<1 then '0-1' when yrs<3 then '1-3' when yrs<5 then '3-5' when yrs<10 then '5-10' else '10+' end c,
  count(*)::text d, sum(NO_EMPLOYEES)::text e, count_if(NO_EMPLOYEES>0)::text f, null g, null h
from m where idle group by 2,3,4
union all
select 'ctrl', CURRENT_CONTROLLER_NAME, CURRENT_CONTROLLER_ID, count_if(idle and yrs>=3)::text, count_if(idle)::text,
  count_if(CURRENT_MINE_STATUS='Active')::text, count_if(CURRENT_MINE_STATUS not in ('Abandoned','Abandoned and Sealed'))::text,
  listagg(distinct STATE, ','), round(max(iff(idle, yrs, null)),1)::text
from m where COAL_METAL_IND='C' group by 2,3
qualify row_number() over (order by count_if(idle and yrs>=3) desc) <= 15
union all
select 'state', STATE, COAL_METAL_IND, count_if(CURRENT_MINE_STATUS not in ('Abandoned','Abandoned and Sealed'))::text,
  count_if(idle)::text, count_if(idle and yrs>=3)::text, count_if(CURRENT_MINE_STATUS='Active')::text,
  round(100*count_if(idle and yrs>=3)/nullif(count_if(CURRENT_MINE_STATUS not in ('Abandoned','Abandoned and Sealed')),0),1)::text, null
from m where COAL_METAL_IND='C' group by 2,3 having count_if(CURRENT_MINE_STATUS not in ('Abandoned','Abandoned and Sealed')) >= 20
