-- FHLB: insurers by district and join era (peer = the district's other members); insurer names hinting at captives; the newest insurers
with m as (select *, case when year(MEM_DATE) > year(current_date()) then year(MEM_DATE) - 100 else year(MEM_DATE) end yr
           from LIBRARY_MARTS.FINANCE.FINANCE__FED_FHFA_FHLB_MEMBERSHIP)
select 'district' k, DISTRICT a, null b, count(*) n_all, count_if(MEM_TYPE = 'Insurance Company') ins, round(100*count_if(MEM_TYPE = 'Insurance Company')/count(*), 1) ins_pct,
  count_if(yr >= 2016) new16, count_if(yr >= 2016 and MEM_TYPE = 'Insurance Company') ins16, round(100*count_if(yr >= 2016 and MEM_TYPE = 'Insurance Company')/nullif(count_if(yr >= 2016), 0), 1) ins16_pct
from m group by 2
union all
select 'year', yr::text, null, count(*), count_if(MEM_TYPE = 'Insurance Company'), round(100*count_if(MEM_TYPE = 'Insurance Company')/count(*), 1),
  count_if(MEM_TYPE = 'Credit Union'), count_if(MEM_TYPE = 'Commercial Bank'), count_if(MEM_TYPE like 'Community Development%')
from m where yr >= 2005 group by 2
union all
select 'captive?', MEMBER_NAME, DISTRICT || ' ' || STATE || ' ' || MEM_DATE::text, null, null, null, null, null, null
from m where MEM_TYPE = 'Insurance Company' and (MEMBER_NAME ilike '%captive%' or MEMBER_NAME ilike '%reinsur%' or MEMBER_NAME ilike '% re %' or MEMBER_NAME ilike '% re' or MEMBER_NAME ilike '%mortgage%' or MEMBER_NAME ilike '%funding%')
order by 1, 2
