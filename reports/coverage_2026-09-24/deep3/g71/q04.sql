-- France: archiving over time. Month of ARCHIVED (parsed), harvested vs native, distinct orgs, top org share
with t as (select *, try_to_timestamp(ARCHIVED) arch_ts, iff(HARVEST_REMOTE_URL is not null and HARVEST_REMOTE_URL<>'', 'harv', 'native') src
  from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV where ARCHIVED not in ('False','false',''))
, m as (select to_char(date_trunc('month', arch_ts),'YYYY-MM') mon, ORGANIZATION_NAME org, count(*) n from t group by 1,2)
, top as (select mon, org, n, row_number() over (partition by mon order by n desc) rk from m)
select to_char(date_trunc('month', t.arch_ts),'YYYY-MM') mon, count(*) n, count_if(src='harv') harv, count_if(src='native') native,
  count(distinct t.ORGANIZATION_NAME) orgs, count_if(arch_ts is null) unparsed,
  max(iff(top.rk=1, top.org||' '||top.n, null)) top_org
from t left join top on top.mon=to_char(date_trunc('month', t.arch_ts),'YYYY-MM') and top.rk=1
group by 1 order by 1
