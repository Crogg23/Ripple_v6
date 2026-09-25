-- France: whole-wave dull test for 2024-03-21. Share of the 12,190 archived with a live same-title twin (same office / any publisher)
with t as (select *, try_to_timestamp(ARCHIVED) arch_ts, lower(regexp_replace(trim(TITLE),'\s+',' ')) nt, coalesce(ORGANIZATION_NAME,'(no org)') org
  from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV)
, live_same as (select distinct org, nt from t where ARCHIVED='False')
, live_any as (select distinct nt from t where ARCHIVED='False')
, w as (select t.*, (s.nt is not null) twin_same, (a.nt is not null) twin_any from t left join live_same s on s.org=t.org and s.nt=t.nt left join live_any a on a.nt=t.nt
        where t.arch_ts::date='2024-03-21')
select count(*) n, count_if(twin_same) twin_same, round(100*count_if(twin_same)/count(*),1) pct_same, count_if(twin_any) twin_any, round(100*count_if(twin_any)/count(*),1) pct_any,
  count_if(TITLE ilike 'PPR%' or TITLE ilike '%risque%inond%' or TITLE ilike '%PPRI%') flood_risk, count_if((TITLE ilike 'PPR%' or TITLE ilike '%risque%inond%' or TITLE ilike '%PPRI%') and twin_any) flood_twin,
  sum(NB_RESOURCE_DOWNLOADS) dl, sum(iff(twin_any, 0, NB_RESOURCE_DOWNLOADS)) dl_no_twin
from w
