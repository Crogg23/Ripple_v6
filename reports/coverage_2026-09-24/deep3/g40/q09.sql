-- Program subparts: keys, duplicates, land rate, and how completely each state fills subparts for its major sources
with s as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAM_SUBPARTS),
fac as (select PGM_SYS_ID, STATE, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES),
sp as (select distinct PGM_SYS_ID from s)
select 'profile' k, count(*)::text a, count(distinct PGM_SYS_ID)::text b, count(distinct AIR_PROGRAM_SUBPART_CODE)::text c,
  count(distinct PGM_SYS_ID||'|'||AIR_PROGRAM_SUBPART_CODE)::text d, count_if(AIR_PROGRAM_SUBPART_CODE is null or trim(AIR_PROGRAM_SUBPART_CODE)='')::text e,
  count_if(not startswith(AIR_PROGRAM_SUBPART_CODE, PROGRAM_CODE))::text f,
  (select count(*) from sp join fac using (PGM_SYS_ID))::text g
from s
union all
select * from (select 'state_maj_op', STATE, count(*)::text, count_if(sp.PGM_SYS_ID is not null)::text,
  round(100*count_if(sp.PGM_SYS_ID is not null)/count(*),1)::text, null, null, null
from fac left join sp using (PGM_SYS_ID) where cls='MAJ' and op='OPR' group by 2 order by round(100*count_if(sp.PGM_SYS_ID is not null)/count(*),1) asc limit 60)
union all
select * from (select 'top_sub', AIR_PROGRAM_SUBPART_CODE, count(distinct PGM_SYS_ID)::text, left(any_value(AIR_PROGRAM_SUBPART_DESC),90), null, null, null, null
from s group by 2 order by count(distinct PGM_SYS_ID) desc limit 12)
