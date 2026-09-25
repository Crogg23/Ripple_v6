-- Slave voyages: label the North American departure ports (codes need a lookup that is not in the warehouse).
-- Each port code that starts with 2 (mainland North America): voyages, years, flags, commonest owner and captain, captives embarked
with t as (select * from LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC where left(PTDEPIMP,1)='2')
select PTDEPIMP port, max(DEPTREGIMP) reg, count(*) voyages, min(try_to_number(YEARAM)) y0, max(try_to_number(YEARAM)) y1,
  count_if(try_to_number(YEARAM) >= 1808) v_1808on, mode(NATINIMP) flag, mode(OWNERA) top_owner, mode(CAPTAINA) top_captain,
  round(sum(try_to_number(SLAXIMP))) embarked, count_if(OWNERA ilike '%wolf%' or OWNERB ilike '%wolf%') dewolf_like, count_if(OWNERA ilike 'Brown,%' or OWNERB ilike 'Brown,%') brown_like
from t group by 1 order by voyages desc limit 20;
