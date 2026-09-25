-- CIP codes: confirm it is a lookup; why CIP_CODE repeats; ACTION mix
with c as (select * from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_ED_NCES_CIP_CODES),
dup as (select CIP_CODE, count(*) k, count(distinct CIP_TITLE) t, count(distinct _SOURCE_RUN_ID) runs, count(distinct CIP_DEFINITION) defs
        from c group by 1 having count(*)>1)
select 'profile' k, count(*)::text a, count(distinct CIP_CODE)::text b, count(distinct CIP_CODE||'|'||CIP_TITLE)::text c,
  count(distinct _SOURCE_RUN_ID)::text d, count(distinct _SRC_SHA256)::text e,
  (select listagg(ACTION||':'||n, ' | ') from (select ACTION, count(*) n from c group by 1 order by n desc)) f
from c
union all
select 'dup_codes', count(*)::text, sum(k)::text, max(k)::text, max(t)::text, max(runs)::text, max(defs)::text from dup
union all
select * from (select 'dup_sample', CIP_CODE, k::text, t::text, runs::text, defs::text, null from dup order by k desc, CIP_CODE limit 4)
union all
select * from (select 'rows_60.0602', CIP_CODE, left(CIP_TITLE,50), ACTION, left(CIP_DEFINITION,60), _SOURCE_RUN_ID, left(_LOADED_AT::text,19) from c where CIP_CODE='60.0602' limit 6)
