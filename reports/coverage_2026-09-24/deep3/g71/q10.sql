-- Greece: profile. Key uniqueness, date span, fill rates, placeholder descriptions, flags, languages, sample-source URL
select count(*) n, count(distinct DATASET_ID) ids, count(distinct lower(trim(TITLE))) titles, count(distinct ORGANISATION_ID) org_ids, count(distinct ORGANISATION_NAME) org_names,
  min(DATE_CREATED) c_min, max(DATE_CREATED) c_max, count(distinct DATE_CREATED::date) c_days,
  min(METADATA_MODIFIED) m_min, max(METADATA_MODIFIED) m_max,
  count_if(DESCRIPTION like 'Δεν παρέχεται%') desc_none, count_if(DESCRIPTION is null or DESCRIPTION='') desc_blank,
  count_if(IS_HVD is not null and IS_HVD not in ('','[]')) hvd, count_if(THEMATIC_CATEGORY is not null and THEMATIC_CATEGORY not in ('','[]')) theme,
  count_if(LICENSE_ID is not null and LICENSE_ID<>'') lic, listagg(distinct LICENSE_ID, '|') lic_vals,
  count_if(TAGS is null or TAGS in ('','[]')) tags_blank, count_if(NUM_RESOURCES=0) res0, max(NUM_RESOURCES) res_max, sum(NUM_RESOURCES) res_sum,
  left(listagg(distinct LANGUAGE, ' | '),300) langs, count(distinct _SOURCE_URL) src_urls, left(listagg(distinct _SOURCE_URL, ' | '),300) src, count(distinct _LOADED_AT) loads
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GR_DATAGOV
