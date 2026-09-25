-- Germany: profile. Keys, date spans, fill rates, HVD, publishers, source URL, load count
select count(*) n, count(distinct DATASET_ID) ids, count(distinct NAME) names, count(distinct lower(trim(TITLE))) titles, count(distinct PUBLISHER) pubs,
  min(METADATA_CREATED) c_min, max(METADATA_CREATED) c_max, min(METADATA_MODIFIED) m_min, max(METADATA_MODIFIED) m_max,
  count_if(TEMPORAL_START is not null) t_start, min(TEMPORAL_START) ts_min, max(TEMPORAL_END) te_max,
  count_if(IS_HVD is not null and IS_HVD not in ('','[]','null')) hvd, count_if(LICENSE_ID is not null and LICENSE_ID<>'') lic,
  count_if(SPATIAL is not null and SPATIAL not in ('','null')) spatial, count_if(RESOURCES is null or RESOURCES in ('','[]')) res_blank,
  count_if(PUBLISHER is null or PUBLISHER='') pub_blank, count(distinct _SOURCE_URL) src_n, left(listagg(distinct _SOURCE_URL,' | '),200) src, count(distinct _LOADED_AT) loads
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_DE_GOVDATA
