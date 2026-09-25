-- ICIS-Air informal actions: keys, flags, enforcement types, sentinel dates
with t as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS)
select 'profile' k, count(*)::text a, count(distinct ACTIVITY_ID)::text b, count(distinct PGM_SYS_ID)::text c, count(distinct ENF_IDENTIFIER)::text d,
  count(distinct PGM_SYS_ID||'|'||ACTIVITY_ID)::text e,
  count_if(ACHIEVED_DATE is null)::text || ' null / ' || count_if(year(ACHIEVED_DATE)<1970)::text || ' pre1970 / ' || count_if(ACHIEVED_DATE>'2026-09-24')::text || ' future' f,
  min(iff(year(ACHIEVED_DATE)>=1970, ACHIEVED_DATE, null))::text || ' to ' || max(iff(ACHIEVED_DATE<='2026-09-24', ACHIEVED_DATE, null))::text g
from t
union all select 'flag', STATE_EPA_FLAG, count(*)::text, count(distinct PGM_SYS_ID)::text, null, null, null, null from t group by 2
union all select 'official', OFFICIAL_FLG, count(*)::text, null, null, null, null, null from t group by 2
union all select * from (select 'enftype', ENF_TYPE_CODE, count(*)::text, any_value(ENF_TYPE_DESC), count_if(STATE_EPA_FLAG='E')::text, null, null, null from t group by 2 order by count(*) desc limit 15)
union all select * from (select 'baddate', ACHIEVED_DATE::text, count(*)::text, null, null, null, null, null from t where year(ACHIEVED_DATE)<1970 or ACHIEVED_DATE>'2026-09-24' group by 2 order by count(*) desc limit 8)
union all select * from (select 'bigenf', ENF_IDENTIFIER, count(*)::text, count(distinct PGM_SYS_ID)::text, count(distinct ACHIEVED_DATE)::text, min(ACHIEVED_DATE)::text||'..'||max(ACHIEVED_DATE)::text, any_value(ENF_TYPE_DESC), count(distinct ACTIVITY_ID)::text from t group by 2 order by count(*) desc limit 8)
