-- Canada: profile, dupes, sentinel coverage dates, created/modified span, resource files per package
with t as (select * from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CA_OPEN_CANADA)
select count(*) n, count(distinct DATASET_ID) ids,
  min(METADATA_CREATED)::text created_min, max(METADATA_CREATED)::text created_max,
  min(METADATA_MODIFIED)::text mod_min, max(METADATA_MODIFIED)::text mod_max,
  count_if(TIME_PERIOD_COVERAGE_START::text like '0001%') cov_start_0001, count_if(TIME_PERIOD_COVERAGE_START is null) cov_start_null,
  count_if(nullif(trim(TIME_PERIOD_COVERAGE_END::text),'') is null) cov_end_blank,
  count_if(nullif(trim(NOTES_EN),'') is null) notes_en_blank, count_if(nullif(trim(TITLE_FR),'') is null) title_fr_blank,
  count_if(nullif(trim(DATE_PUBLISHED::text),'') is null) datepub_blank,
  count_if(TAGS = '[]') tags_empty, count(distinct LICENSE_ID) lics, listagg(distinct LICENSE_ID,'|') lic_vals,
  listagg(distinct FREQUENCY,'|') freq_vals,
  sum(array_size(try_parse_json(RESOURCES))) resource_files, count_if(try_parse_json(RESOURCES) is null) res_unparsed,
  max(array_size(try_parse_json(RESOURCES))) max_files, median(array_size(try_parse_json(RESOURCES))) med_files,
  count(distinct _SOURCE_URL) src_urls, any_value(_SOURCE_URL) src
from t;
