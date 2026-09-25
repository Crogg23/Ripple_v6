-- Private airports: is each airport repeated? distinct codes, copies per code, states, status values
with t as (select PRIVATE_AIRPORT_LIST_FOR_WHICH_INFORMATION_HAS_NOT_BEEN_UPDATED_IN_THE_LAST_3_YEARS code, UNNAMED_1 nm, UNNAMED_2 site, UNNAMED_3 city, UNNAMED_4 st, UNNAMED_5 status
           from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FAA_ADIP_PRIVATE_AIRPORTS),
c as (select code, count(*) k from t group by 1)
select 'profile' k, count(*)::varchar a, count(distinct code)::varchar b, count(distinct code||'|'||nm||'|'||site||'|'||city||'|'||st||'|'||status)::varchar c,
  (select min(k)||'-'||max(k)||' median '||median(k) from c) d, listagg(distinct status, ',') e from t
union all select 'state', st, count(*)::varchar, count(distinct code)::varchar, null, null from t group by st
union all select 'sample', code, nm, site, city, st from (select * from t order by code limit 8);
