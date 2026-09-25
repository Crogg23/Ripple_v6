-- Chile: profile. Keys, date spans, fills, publishers, STATE values, formats, source URL
select count(*) n, count(distinct DATASET_ID) ids, count(distinct NAME) names, count(distinct lower(trim(TITLE))) titles, count(distinct PUBLISHER_INSTITUTION) pubs,
  min(METADATA_CREATED) c_min, max(METADATA_CREATED) c_max, min(METADATA_MODIFIED) m_min, max(METADATA_MODIFIED) m_max,
  listagg(distinct STATE,'|') states, count_if(CATEGORY is not null and CATEGORY<>'') cat, count_if(LICENSE_ID is not null and LICENSE_ID<>'') lic, left(listagg(distinct LICENSE_ID,'|'),200) lics,
  count_if(NUM_RESOURCES=0) res0, median(NUM_RESOURCES) res_med, max(NUM_RESOURCES) res_max,
  count_if(DESCRIPTION is null or DESCRIPTION='') desc_blank, count(distinct _SOURCE_URL) src_n, left(listagg(distinct _SOURCE_URL,' | '),200) src, count(distinct _LOADED_AT) loads
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CL_DATOSGOB
