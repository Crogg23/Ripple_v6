-- France: usage concentration on LIVE datasets (downloads), harvested vs native, plus the top 8 by downloads and the date sentinels
with t as (select *, (HARVEST_REMOTE_URL is not null and HARVEST_REMOTE_URL<>'') harv from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV where ARCHIVED='False')
, r as (select *, row_number() over (order by NB_RESOURCE_DOWNLOADS desc nulls last) rk, sum(NB_RESOURCE_DOWNLOADS) over () tot from t)
select 'split' k, iff(harv,'harvested','native') a, count(*)::text b, median(NB_RESOURCE_DOWNLOADS)::text c, count_if(coalesce(NB_RESOURCE_DOWNLOADS,0)=0)::text d,
  count_if(coalesce(NB_RESOURCE_DOWNLOADS,0)<10)::text e, round(100*sum(NB_RESOURCE_DOWNLOADS)/any_value(tot),1)::text f, median(NB_VIEWS)::text g
from r group by 2
union all select 'top', left(TITLE,70), coalesce(ORGANIZATION_NAME, OWNER), NB_RESOURCE_DOWNLOADS::text, NB_VIEWS::text, CREATED_AT::date::text, round(100*NB_RESOURCE_DOWNLOADS/tot,2)::text, rk::text from r where rk<=8
union all select 'top10share', null, null, round(100*sum(iff(rk<=10,NB_RESOURCE_DOWNLOADS,0))/any_value(tot),1)::text, round(100*sum(iff(rk<=100,NB_RESOURCE_DOWNLOADS,0))/any_value(tot),1)::text, any_value(tot)::text, null, count(*)::text from r
union all select 'datesent', left(TITLE,70), coalesce(ORGANIZATION_NAME, OWNER), CREATED_AT::text, harv::text, ARCHIVED, null, null
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV x, lateral (select (x.HARVEST_REMOTE_URL is not null and x.HARVEST_REMOTE_URL<>'') harv)
where year(CREATED_AT)<1970 or CREATED_AT>'2026-08-12'
