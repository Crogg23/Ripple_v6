-- France: the most-used datasets that left the portal. Archived, native (not harvested), no live dataset with the same title anywhere; top 25 by downloads
with t as (select *, lower(regexp_replace(trim(TITLE),'\s+',' ')) nt, try_to_timestamp(ARCHIVED) arch_ts from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV)
, live as (select distinct nt from t where ARCHIVED='False')
select left(t.TITLE,80) title, coalesce(t.ORGANIZATION_NAME, t.OWNER) org, t.arch_ts::date archived, t.CREATED_AT::date created, t.NB_RESOURCE_DOWNLOADS dl, t.NB_VIEWS views, t.NB_REUSES reuses,
  t.LAST_MODIFIED::date last_mod
from t left join live l on l.nt=t.nt
where t.arch_ts is not null and (t.HARVEST_REMOTE_URL is null or t.HARVEST_REMOTE_URL='') and l.nt is null
order by t.NB_RESOURCE_DOWNLOADS desc nulls last limit 25
