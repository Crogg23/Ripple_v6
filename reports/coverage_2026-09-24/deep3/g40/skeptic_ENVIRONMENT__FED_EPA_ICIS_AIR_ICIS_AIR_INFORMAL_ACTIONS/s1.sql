-- Re-derive Tesla NOVs 2019-2026-07 on the plant ID: rows vs actions vs case numbers vs days; top days; sample; facility-table dup check
with t as (select * from {I} where PGM_SYS_ID='CABAA00006001A1438' and ACHIEVED_DATE between '2019-01-01' and '2026-07-31'),
d as (select ACHIEVED_DATE, count(distinct ACTIVITY_ID) n, row_number() over (order by count(distinct ACTIVITY_ID) desc, ACHIEVED_DATE) rk from t group by 1)
select 'yr' k, year(ACHIEVED_DATE)::text a, count(*)::text b, count(distinct ACTIVITY_ID)::text c, count(distinct ENF_IDENTIFIER)::text d, count(distinct ACHIEVED_DATE)::text e, listagg(distinct ENF_TYPE_CODE,'|') f, listagg(distinct OFFICIAL_FLG,'|') g, min(ENF_IDENTIFIER) h, max(ENF_IDENTIFIER) i from t group by 2
union all select 'days', null, count(*)::text, median(n)::text, max(n)::text, sum(iff(rk<=5,n,0))::text, sum(iff(rk<=10,n,0))::text, count_if(n=1)::text, sum(n)::text, null from d
union all select 'topday', ACHIEVED_DATE::text, n::text, rk::text, null, null, null, null, null, null from d where rk<=8
union all select * from (select 'sample', ACHIEVED_DATE::text, ENF_IDENTIFIER, ACTIVITY_ID::text, STATE_EPA_FLAG, ENF_TYPE_DESC, OFFICIAL_FLG, null, null, null from t order by ACHIEVED_DATE desc, ENF_IDENTIFIER limit 8)
union all select 'facdup', null, count(*)::text, count(distinct PGM_SYS_ID)::text, null, null, null, null, null, null from {F}
