-- France: March 2024 archive wave by day, harvested flag, org families (DDT/DDTM/DREAL/other), downloads
with t as (select *, try_to_timestamp(ARCHIVED) arch_ts from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV)
select arch_ts::date d, count(*) n, count(distinct ORGANIZATION_NAME) orgs,
  count_if(ORGANIZATION_NAME ilike 'Direction D%partementale%' or ORGANIZATION_NAME ilike 'DDT%') ddt,
  count_if(ORGANIZATION_NAME ilike 'DREAL%' or ORGANIZATION_NAME ilike 'Direction R%gionale%') dreal,
  count_if(RESOURCES_FORMATS ilike '%ogc:w%' or RESOURCES_FORMATS ilike '%wms%' or RESOURCES_FORMATS ilike '%wfs%') ogc,
  min(CREATED_AT)::date cr_min, median(year(CREATED_AT)) cr_med_year, max(CREATED_AT)::date cr_max,
  sum(NB_RESOURCE_DOWNLOADS) dl_sum, median(NB_RESOURCE_DOWNLOADS) dl_med, sum(NB_REUSES) reuses,
  any_value(TITLE) sample_title
from t where arch_ts >= '2024-03-01' and arch_ts < '2024-04-01' group by 1 order by 2 desc limit 12
