-- France: the dull test. For each big archive event, how many archived titles have a LIVE twin
-- (same org + same normalized title), and when was the twin created? Replaced = housekeeping; no twin = gone from the portal.
with t as (select *, try_to_timestamp(ARCHIVED) arch_ts, lower(regexp_replace(trim(TITLE),'\s+',' ')) nt, coalesce(ORGANIZATION_NAME,'(no org)') org
  from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV)
, live as (select org, nt, min(CREATED_AT) twin_created, count(*) k from t where arch_ts is null and ARCHIVED='False' group by 1,2)
, ev as (select org, date_trunc('month', arch_ts) mon from t where arch_ts is not null group by 1,2 having count(*)>=300)
, a as (select t.org, to_char(date_trunc('month', t.arch_ts),'YYYY-MM') mon, t.nt, t.NB_RESOURCE_DOWNLOADS dl, l.twin_created
        from t join ev on ev.org=t.org and ev.mon=date_trunc('month', t.arch_ts) left join live l on l.org=t.org and l.nt=t.nt)
select org, mon, count(*) arch_n, count_if(twin_created is not null) with_live_twin,
  round(100*count_if(twin_created is not null)/count(*),1) twin_pct,
  min(twin_created)::date twin_first, median(year(twin_created)) twin_med_year, max(twin_created)::date twin_last,
  sum(iff(twin_created is null, dl, 0)) dl_on_untwinned
from a group by 1,2 order by arch_n desc limit 25
