-- Slave voyages: grain check. Distinct voyage ids, copies per id, are copies identical rows, flag and status values
with t as (select * from LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC),
c as (select VOYAGEID, count(*) k from t group by 1)
select 'profile' k, count(*)::varchar a, count(distinct VOYAGEID)::varchar b, (select count_if(k>1)||' ids repeat; max '||max(k) from c) c,
  count(distinct hash(*))::varchar d, listagg(distinct INTRAAMER::varchar, ',') e, listagg(distinct STATUS::varchar, ',') f,
  min(try_to_number(YEARAM))||'-'||max(try_to_number(YEARAM)) g from t
union all select 'topid', VOYAGEID, k::varchar, null, null, null, null, null from (select * from c order by k desc limit 5)
union all select 'idlen', length(VOYAGEID)::varchar, count(*)::varchar, min(VOYAGEID), max(VOYAGEID), null, null, null from t group by 2;
