-- Chile: per publisher. Datasets, created by year, contest-tagged rows (Concurso Transparenta), files per dataset, formats
select PUBLISHER_INSTITUTION pub, count(*) n, count_if(CATEGORY ilike '%Transparenta%') contest,
  count_if(year(METADATA_CREATED)<=2020) c_to2020, count_if(year(METADATA_CREATED) between 2021 and 2024) c_21_24, count_if(year(METADATA_CREATED)=2025) c_2025, count_if(year(METADATA_CREATED)=2026) c_2026,
  count(distinct METADATA_CREATED::date) c_days, median(NUM_RESOURCES) med_files, sum(NUM_RESOURCES) files,
  count_if(RESOURCE_FORMATS ilike '%pdf%') pdf, count_if(RESOURCE_FORMATS ilike '%csv%' or RESOURCE_FORMATS ilike '%xls%') tabular, left(any_value(TITLE),60) sample_title
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CL_DATOSGOB group by 1 order by 2 desc limit 12
