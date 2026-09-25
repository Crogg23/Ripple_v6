-- France peer check: every regional council (Région ...). Live vs archived now, archived in 2026, harvested share, live downloads
with t as (select *, try_to_timestamp(ARCHIVED) arch_ts, (HARVEST_REMOTE_URL is not null and HARVEST_REMOTE_URL<>'') harv
  from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV where ORGANIZATION_NAME ilike 'R_gion %')
select ORGANIZATION_NAME org, count(distinct ORGANIZATION_ID) org_ids, count(*) n, count_if(ARCHIVED='False') live, count_if(arch_ts is not null) archived,
  count_if(year(arch_ts)=2026) arch_2026, round(100*count_if(year(arch_ts)=2026)/nullif(count_if(ARCHIVED='False')+count_if(year(arch_ts)=2026),0),1) pct_lost_2026,
  count_if(harv) harvested, count_if(ARCHIVED='False' and CREATED_AT>='2026-01-01') live_new_2026,
  sum(iff(ARCHIVED='False', NB_RESOURCE_DOWNLOADS, 0)) live_dl
from t group by 1 having count(*)>=20 order by arch_2026 desc
