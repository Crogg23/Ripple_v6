-- France: profile. Key uniqueness, archived, owners, dates out of range, usage counters, harvest share
select count(*) n, count(distinct DATASET_ID) ids, count(distinct SLUG) slugs,
  count_if(ARCHIVED is null or ARCHIVED in ('','False','false')) live_rows, count_if(ARCHIVED not in ('','False','false') and ARCHIVED is not null) archived_rows,
  min(iff(ARCHIVED not in ('','False','false'), ARCHIVED, null)) arch_min, max(iff(ARCHIVED not in ('','False','false'), ARCHIVED, null)) arch_max,
  count_if(ORGANIZATION_NAME is null or ORGANIZATION_NAME in ('','None')) org_blank, count_if(OWNER like 'deleted%') owner_deleted,
  count_if(year(CREATED_AT)<1990) created_pre1990, count_if(CREATED_AT>'2026-08-12') created_future, min(CREATED_AT) cmin, max(CREATED_AT) cmax,
  count_if(LAST_MODIFIED>'2026-08-12') mod_future,
  count_if(NB_VIEWS is null) views_null, count_if(NB_VIEWS=0) views0, median(NB_VIEWS) views_med, sum(NB_VIEWS) views_sum, max(NB_VIEWS) views_max,
  count_if(NB_RESOURCE_DOWNLOADS is null) dl_null, count_if(NB_RESOURCE_DOWNLOADS=0) dl0, median(NB_RESOURCE_DOWNLOADS) dl_med, sum(NB_RESOURCE_DOWNLOADS) dl_sum, max(NB_RESOURCE_DOWNLOADS) dl_max,
  count_if(NB_RESOURCES=0) res0, count_if(HARVEST_REMOTE_URL is not null and HARVEST_REMOTE_URL<>'') harvested,
  min(QUALITY_SCORE) qmin, median(QUALITY_SCORE) qmed, max(QUALITY_SCORE) qmax, count(distinct ORGANIZATION_ID) orgs
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV
