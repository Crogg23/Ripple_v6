-- France: the big archive events (org-month with 300+ archived). Did the same org create a like number of new datasets
-- in that month or the next (re-harvest churn = dull), and how many live datasets does it hold now?
with t as (select *, try_to_timestamp(ARCHIVED) arch_ts, (HARVEST_REMOTE_URL is not null and HARVEST_REMOTE_URL<>'') harv
  from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV)
, ev as (select coalesce(ORGANIZATION_NAME,'(no org)') org, date_trunc('month', arch_ts) mon, count(*) arch_n, count_if(harv) arch_harv,
         min(arch_ts)::date first_day, max(arch_ts)::date last_day, count(distinct arch_ts::date) days,
         sum(NB_RESOURCE_DOWNLOADS) arch_dl, median(NB_RESOURCE_DOWNLOADS) arch_dl_med, min(CREATED_AT)::date cr_min, max(CREATED_AT)::date cr_max
       from t where arch_ts is not null group by 1,2 having count(*)>=300)
select ev.org, to_char(ev.mon,'YYYY-MM') mon, arch_n, arch_harv, first_day, last_day, days, cr_min, cr_max, arch_dl, arch_dl_med,
  (select count(*) from t t2 where coalesce(t2.ORGANIZATION_NAME,'(no org)')=ev.org and t2.CREATED_AT >= ev.mon and t2.CREATED_AT < dateadd(month,2,ev.mon)) created_same_2mo,
  (select count(*) from t t3 where coalesce(t3.ORGANIZATION_NAME,'(no org)')=ev.org and t3.arch_ts is null) live_now
from ev order by arch_n desc
